using System.Collections.Concurrent;
using System.Net;
using System.Net.Sockets;
using Library.Network;
using G = Library.Network.GeneralPackets;

int passed = 0;
async Task Check(string name, Func<Task> check)
{
    await check();
    Console.WriteLine("PASS " + name);
    passed++;
}
void Require(bool condition, string message)
{
    if (!condition) throw new Exception(message);
}

await Check("heartbeats continue without game frames; world state stays ordered until resume", async () =>
{
    using var pair = await SocketPair.Create();
    pair.Connection.BeginBackgroundKeepAlive(TimeSpan.FromMinutes(3));
    for (int i = 0; i < 20; i++)
    {
        await pair.Send(new RegressionPackets.State { Sequence = i });
        await pair.Send(new G.Ping());
        Require(await pair.Read() is G.Ping, "Missing heartbeat while Process is paused");
    }
    Require(pair.Connection.States.Count == 0, "Game handler ran on socket thread");
    Require(pair.Connection.GetReceiveListQueueLength() == 20, "World state lost");
    pair.Connection.EndBackgroundKeepAlive();
    int thread = Environment.CurrentManagedThreadId;
    pair.Connection.Process();
    Require(pair.Connection.States.Select(x => x.Sequence).SequenceEqual(Enumerable.Range(0, 20)), "Resume order differs");
    Require(pair.Connection.States.All(x => x.Thread == thread), "Handlers ran outside the resume thread");
    pair.AssertHealthy();
});

await Check("foreground heartbeat arriving just before pause also gets a reply", async () =>
{
    using var pair = await SocketPair.Create();
    await pair.Send(new G.Ping());
    Require(await pair.Read() is G.Ping, "Pre-pause Ping waits for a stopped frame");
    Require(pair.Connection.GetReceiveListQueueLength() == 0, "Heartbeat leaked into UI queue");
    pair.AssertHealthy();
});

await Check("background deadline stops heartbeats; resume before the deadline restores normal processing", async () =>
{
    using var pair = await SocketPair.Create();
    pair.Connection.BeginBackgroundKeepAlive(TimeSpan.Zero);
    pair.Connection.EndBackgroundKeepAlive();
    await pair.Send(new G.Ping());
    Require(await pair.Read() is G.Ping, "Resume did not clear the deadline");
    pair.Connection.BeginBackgroundKeepAlive(TimeSpan.Zero);
    await pair.Send(new G.Ping());
    await pair.Wait(() => pair.Connection.Disconnecting);
    Require(pair.Connection.SendList.IsEmpty, "Expired background session enqueued a Ping");
    Require(!pair.Connection.DisconnectedByFrame, "Socket callback invoked UI disconnect");
    pair.AssertHealthy();
});

await Check("background world queue has a bound and never dispatches game handlers", async () =>
{
    using var pair = await SocketPair.Create();
    pair.Connection.BeginBackgroundKeepAlive(TimeSpan.FromMinutes(3));
    for (int i = 0; i < 4097; i++)
        await pair.Send(new RegressionPackets.State { Sequence = i });
    await pair.Wait(() => pair.Connection.Disconnecting);
    Require(pair.Connection.GetReceiveListQueueLength() == 4096, "Background queue is unbounded");
    Require(pair.Connection.States.Count == 0, "Background dispatched world state");
    pair.AssertHealthy();
});

await Check("heartbeat and frame sends share one ordered stream, including large sends", async () =>
{
    using var pair = await SocketPair.Create();
    pair.Connection.LimitSendBuffer();
    const int count = 100;
    var receiving = Task.Run(async () =>
    {
        var sequences = new List<int>();
        int pings = 0;
        while (sequences.Count < count || pings < 20)
        {
            Packet packet = await pair.Read();
            if (packet is G.Ping) pings++;
            else if (packet is RegressionPackets.State state)
            {
                Require(state.Data.All(x => x == (byte)state.Sequence), "Send payload corrupted or interleaved");
                sequences.Add(state.Sequence);
            }
            else throw new Exception("Unexpected packet");
        }
        Require(sequences.SequenceEqual(Enumerable.Range(0, count)), "Concurrent sends reordered game packets");
    });
    var heartbeat = Task.Run(async () =>
    {
        for (int i = 0; i < 20; i++) await pair.Send(new G.Ping());
    });
    for (int i = 0; i < count; i++)
    {
        pair.Connection.Enqueue(new RegressionPackets.State { Sequence = i, Data = Enumerable.Repeat((byte)i, 32768).ToArray() });
        pair.Connection.Process();
    }
    // No further Process calls: a Ping queued behind an in-flight send must finish.
    pair.Connection.BeginBackgroundKeepAlive(TimeSpan.FromMinutes(3));
    await Task.WhenAll(heartbeat, receiving).WaitAsync(TimeSpan.FromSeconds(15));
    pair.AssertHealthy();
});

Console.WriteLine($"{passed} background transport checks passed.");

public sealed class TestConnection : BaseConnection
{
    protected override bool TransportHeartbeatEnabled => true;
    protected override TimeSpan TimeOutDelay => TimeSpan.FromSeconds(15);
    public readonly List<(int Sequence, int Thread)> States = new();
    public readonly ConcurrentQueue<Exception> Errors = new();
    public bool DisconnectedByFrame;
    public TestConnection(TcpClient client) : base(client)
    {
        AdditionalLogging = true;
        OnException = (_, error) => Errors.Enqueue(error);
        UpdateTimeOut();
        BeginReceive();
    }
    public void Process(RegressionPackets.State packet) => States.Add((packet.Sequence, Environment.CurrentManagedThreadId));
    public void Process(G.Ping packet) => throw new Exception("Ping reached game thread");
    public override void TryDisconnect() { DisconnectedByFrame = true; Disconnect(); }
    public override void TrySendDisconnect(Packet packet) => SendDisconnect(packet);
    public void LimitSendBuffer() => Client.SendBufferSize = 1024;
}

public sealed class SocketPair : IDisposable
{
    private TcpClient Peer;
    public TestConnection Connection;
    private byte[] Buffered = Array.Empty<byte>();
    public static async Task<SocketPair> Create()
    {
        var listener = new TcpListener(IPAddress.Loopback, 0);
        listener.Start();
        try
        {
            var client = new TcpClient();
            var accepted = listener.AcceptTcpClientAsync();
            await client.ConnectAsync(IPAddress.Loopback, ((IPEndPoint)listener.LocalEndpoint).Port);
            return new SocketPair { Peer = await accepted, Connection = new TestConnection(client) };
        }
        finally { listener.Stop(); }
    }
    public async Task Send(Packet packet)
    {
        byte[] bytes = packet.GetPacketBytes();
        // Exercise receive framing across multiple reads.
        await Peer.GetStream().WriteAsync(bytes.AsMemory(0, 3));
        await Peer.GetStream().WriteAsync(bytes.AsMemory(3));
    }
    public async Task<Packet> Read()
    {
        using var deadline = new CancellationTokenSource(TimeSpan.FromSeconds(10));
        while (true)
        {
            if (Packet.CheckPacketLength(Buffered) >= 0)
            {
                var packet = Packet.ReceivePacket(Buffered, out Buffered);
                if (packet == null) throw new Exception("Invalid wire checksum");
                return packet;
            }
            var chunk = new byte[8192];
            int count = await Peer.GetStream().ReadAsync(chunk, deadline.Token);
            if (count == 0) throw new Exception("Unexpected socket EOF");
            Buffered = Buffered.Concat(chunk.Take(count)).ToArray();
        }
    }
    public async Task Wait(Func<bool> condition)
    {
        var deadline = DateTime.UtcNow.AddSeconds(5);
        while (!condition())
        {
            if (DateTime.UtcNow >= deadline) throw new Exception("Condition timed out");
            await Task.Delay(10);
        }
    }
    public void AssertHealthy()
    {
        if (Connection.Errors.TryPeek(out var error)) throw new Exception("Transport error", error);
    }
    public void Dispose() { Connection.Disconnect(); Peer.Dispose(); }
}

namespace RegressionPackets
{
    public sealed class State : Packet
    {
        public int Sequence { get; set; }
        public byte[] Data { get; set; } = Array.Empty<byte>();
    }
}

// General packet dependencies; packet serializer, framing, encryption and socket
// transport above are all linked from production sources.
namespace Library
{
    public enum DisconnectReason : byte { TimedOut }
    public enum Platform : byte { Android }
}
