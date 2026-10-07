using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Net.Http;
using Client.Envir;
using Client.Helpers;

static class RecoveryChecks
{
    public static async Task<int> Run()
    {
        string root = Path.Combine(Path.GetTempPath(), "mir3-refresh-" + Guid.NewGuid());
        Directory.CreateDirectory(Path.Combine(root, "Data"));
        CEnvir.MobileClientPath = root + Path.DirectorySeparatorChar;
        string file = Path.Combine(root, "Data", "Test.Zl");
        File.WriteAllText(file, "old resource cache");
        var library = new MirLibrary { FullPathName = file };
        CEnvir.LibraryList[0] = library;
        var tcp = new TcpListener(IPAddress.Loopback, 0); tcp.Start();
        Config.MicroClientPort = ((IPEndPoint)tcp.LocalEndpoint).Port; tcp.Stop();
        // Only the in-process loopback fixture bypasses the session HTTP proxy.
        // All nonlocal destinations retain the inherited proxy and credentials.
        HttpClient.DefaultProxy = new LoopbackProxy(HttpClient.DefaultProxy);
        using var server = new HttpListener();
        server.Prefixes.Add($"http://127.0.0.1:{Config.MicroClientPort}/"); server.Start();
        int headers = 0;
        using var records = new MemoryStream();
        using (var writer = new BinaryWriter(records, Encoding.UTF8, true))
        {
            writer.Write(1); writer.Write((byte)1); writer.Write(64); writer.Write(16);
            for (int i = 0; i < 6; i++) writer.Write((short)4);
            writer.Write(new byte[3]);
        }
        using var head = new MemoryStream();
        using (var writer = new BinaryWriter(head, Encoding.UTF8, true))
        {
            writer.Write(Encoding.ASCII.GetBytes("BlackDragon Version")); writer.Write((byte)3);
            writer.Write((int)records.Length); writer.Write(records.ToArray());
        }
        byte[] header = head.ToArray();
        var serving = Task.Run(async () =>
        {
            while (server.IsListening)
            {
                HttpListenerContext context;
                try { context = await server.GetContextAsync(); } catch { break; }
                using var bytes = new MemoryStream();
                using (var w = new BinaryWriter(bytes, Encoding.UTF8, true))
                {
                    if (context.Request.RawUrl!.Contains("libheader"))
                    {
                        Interlocked.Increment(ref headers);
                        w.Write(80L);
                        var data = context.Request.RawUrl.Contains("Bad.Zl") ? new byte[3] : header;
                        w.Write(data.Length); w.Write(data);
                    }
                    else { w.Write(64); w.Write(16); w.Write(Enumerable.Repeat((byte)1, 16).ToArray()); }
                }
                context.Response.ContentLength64 = bytes.Length;
                await context.Response.OutputStream.WriteAsync(bytes.ToArray()); context.Response.Close();
            }
        });
        async Task Wait(Func<bool> predicate)
        {
            var deadline = DateTime.UtcNow.AddSeconds(5);
            while (!predicate()) { if (DateTime.UtcNow >= deadline) throw new Exception("Recovery timed out: " + string.Join("; ", CEnvir.Errors)); await Task.Delay(10); }
        }
        try
        {
            if (await LibraryHelper.GetImageAsync("Data/Test.Zl", 0, 8, 52) != null)
                throw new Exception("Mismatched image was accepted.");
            await Wait(() => { LibraryHelper.ApplyResourceRefreshes(); return library.Resets == 1; });
            var current = File.ReadAllBytes(file);
            if (current.Length != 80 || !current.Take(header.Length).SequenceEqual(header))
                throw new Exception("Validated header not applied atomically.");
            if (Client.Scenes.GameScene.Game.MapControl.TextureValid || Client.Scenes.GameScene.Game.MapControl.FLayer.TextureValid)
                throw new Exception("Stale map textures retained.");
            var image = await LibraryHelper.GetImageAsync("Data/Test.Zl", 0, 16, 64);
            if (image?.Length != 16) throw new Exception("Correct indexed image rejected.");
            if (await LibraryHelper.GetImageAsync("Data/Test.Zl", 0, 16, 60) != null)
                throw new Exception("Wrong-offset image accepted.");
            LibraryHelper.RequestResourceRefresh("Data/Test.Zl", "duplicate");
            if (headers != 1) throw new Exception("Refresh cooldown failed.");
            string bad = Path.Combine(root, "Data", "Bad.Zl"); File.WriteAllText(bad, "preserve me");
            LibraryHelper.RequestResourceRefresh("Data/Bad.Zl", "invalid header test");
            await Wait(() => !LibraryHelper.IsResourceRefreshing("Data/Bad.Zl"));
            if (File.ReadAllText(bad) != "preserve me" || !CEnvir.Errors.Any(x => x.Contains("header refresh failed")))
                throw new Exception("Bad server header overwrote existing resource.");
            return 7;
        }
        finally { server.Stop(); await serving; Directory.Delete(root, true); }
    }

    sealed class LoopbackProxy(IWebProxy inherited) : IWebProxy
    {
        public ICredentials? Credentials { get => inherited.Credentials; set => inherited.Credentials = value; }
        public Uri? GetProxy(Uri destination) => destination.IsLoopback ? destination : inherited.GetProxy(destination);
        public bool IsBypassed(Uri destination) => destination.IsLoopback || inherited.IsBypassed(destination);
    }
}
