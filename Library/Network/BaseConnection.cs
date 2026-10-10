using System;
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.Net.Sockets;
using System.Reflection;
using G = Library.Network.GeneralPackets;


namespace Library.Network
{
    /// <summary>
    /// 关联
    /// </summary>
    public abstract class BaseConnection
    {
        /// <summary>
        /// 诊断值
        /// </summary>
        public static Dictionary<string, DiagnosticValue> Diagnostics = new Dictionary<string, DiagnosticValue>();
        /// <summary>
        /// 数据包方法
        /// </summary>
        public static Dictionary<Type, MethodInfo> PacketMethods = new Dictionary<Type, MethodInfo>();
        /// <summary>
        /// 效验检查
        /// </summary>
        public static bool Monitor;
        /// <summary>
        /// 有联系的
        /// </summary>
        public bool Connected { get; set; }
        /// <summary>
        /// 发送
        /// </summary>
        protected bool Sending { get; set; }
        /// <summary>
        /// 总字节数
        /// </summary>
        public int TotalBytesSent { get; set; }
        /// <summary>
        /// 接受的总字节数
        /// </summary>
        public int TotalBytesReceived { get; set; }
        /// <summary>
        /// 附加日志记录
        /// </summary>
        public bool AdditionalLogging;
        /// <summary>
        /// 客户端TCP协议
        /// </summary>
        protected TcpClient Client;
#if ANDROID
        private readonly object _sendLock = new object();
        private long _backgroundUntilTicks = long.MaxValue;
        protected virtual bool TransportHeartbeatEnabled => false;

        // Only the Android game connection opts in. World/UI packets remain queued
        // for Process on the game thread; the existing Ping wire format is unchanged.
        public void BeginBackgroundKeepAlive(TimeSpan duration)
        {
            if (duration < TimeSpan.Zero) throw new ArgumentOutOfRangeException(nameof(duration));
            System.Threading.Interlocked.Exchange(ref _backgroundUntilTicks, (Time.Now + duration).Ticks);
        }

        public void EndBackgroundKeepAlive()
        {
            System.Threading.Interlocked.Exchange(ref _backgroundUntilTicks, long.MaxValue);
        }

        private sealed class PendingSend
        {
            public byte[] Bytes;
            public int Offset;
        }
#endif
        /// <summary>
        /// 连接时间
        /// </summary>
        public DateTime TimeConnected { get; set; }
        /// <summary>
        /// 持续时间=系统时间-连接时间
        /// </summary>
        public TimeSpan Duration => Time.Now - TimeConnected;
        /// <summary>
        /// 超时延迟
        /// </summary>
        protected abstract TimeSpan TimeOutDelay { get; }
        /// <summary>
        /// 超时时间
        /// </summary>
        public DateTime TimeOutTime { get; set; }
        /// <summary>
        /// 断开
        /// </summary>
        private bool _disconnecting;
        /// <summary>
        /// 断开延迟
        /// </summary>
        public bool Disconnecting
        {
            get { return _disconnecting; }
            set
            {
                if (_disconnecting == value) return;
                _disconnecting = value;
                TimeOutTime = Time.Now.AddSeconds(5);
            }
        }
        /// <summary>
        /// 接受数据包列表
        /// </summary>
        public ConcurrentQueue<Packet> ReceiveList = new ConcurrentQueue<Packet>();
        /// <summary>
        /// 发送数据包列表
        /// </summary>
        public ConcurrentQueue<Packet> SendList = new ConcurrentQueue<Packet>();
        /// <summary>
        /// 原始数据
        /// </summary>
        public byte[] _rawData = new byte[0];
        /// <summary>
        /// 异常时的事件处理
        /// </summary>
        public EventHandler<Exception> OnException;
        /// <summary>
        /// 异常时的事件处理输出
        /// </summary>
        public EventHandler<string> Output;
#if ANDROID && BUNDLED_RESOURCE_TEST
        public Action<string> PacketTrace;
        private void Trace(string message)
        {
            try { PacketTrace?.Invoke(message); } catch { }
        }
#endif
        protected BaseConnection(TcpClient client)
        {
            Client = client;
            Client.NoDelay = true;


            Connected = true;
            TimeConnected = Time.Now;
        }

        /// <summary>
        /// 是否为假人连接（无真实 TcpClient）
        /// </summary>
        public bool IsBot { get; private set; }

        /// <summary>
        /// 假人专用构造函数（不需要真实 TcpClient 连接）
        /// </summary>
        protected BaseConnection(bool isBotConnection)
        {
            IsBot = true;
            Connected = true;
            TimeConnected = Time.Now;
        }
        /// <summary>
        /// 获取接收列表队列长度
        /// </summary>
        /// <returns></returns>
        public int GetReceiveListQueueLength()
        {
            if (ReceiveList != null)
                return ReceiveList.Count;
            return 0;
        }
        /// <summary>
        /// 获取发送列表队列长度
        /// </summary>
        /// <returns></returns>
        public int GetSendListQueueLength()
        {
            if (SendList != null)
                return SendList.Count;
            return 0;
        }
        /// <summary>
        /// 开始接收
        /// </summary>
        protected void BeginReceive()
        {
            try
            {
#if ANDROID
                if (Disconnecting) return;
#endif
                if (Client == null || !Client.Connected) return;

                byte[] rawBytes = new byte[8 * 1024];

                Client.Client.BeginReceive(rawBytes, 0, rawBytes.Length, SocketFlags.None, ReceiveData, rawBytes);
            }
            catch (Exception ex)
            {
                if (AdditionalLogging)
                    OnException(this, ex);
                Disconnecting = true;
            }
        }
        /// <summary>
        /// 接收数据
        /// </summary>
        /// <param name="result"></param>
        private void ReceiveData(IAsyncResult result)
        {
            try
            {
                if (!Connected) return;

                int dataRead = Client.Client.EndReceive(result);

                if (dataRead == 0)
                {
#if ANDROID && BUNDLED_RESOURCE_TEST
                    Trace("remote socket closed (EOF)");
#endif
                    Disconnecting = true;
                    return;
                }
                TotalBytesReceived += dataRead;

                UpdateTimeOut();

                byte[] rawBytes = result.AsyncState as byte[];

                byte[] temp = _rawData;
                _rawData = new byte[dataRead + temp.Length];
                Buffer.BlockCopy(temp, 0, _rawData, 0, temp.Length);
                Buffer.BlockCopy(rawBytes, 0, _rawData, temp.Length, dataRead);

                //封包处理单独拆出来
                ReceivePacket();

                BeginReceive();
            }
            catch (Exception ex)
            {
                if (AdditionalLogging)
                    OnException(this, ex);
                Disconnecting = true;
            }
        }

        public virtual void ReceivePacket()
        {
            Packet p;

            while ((p = Packet.ReceivePacket(_rawData, out _rawData)) != null)
            {
#if ANDROID && BUNDLED_RESOURCE_TEST
                Trace($"receive {p.GetType().FullName} id={Packet.Packets.IndexOf(p.GetType())} length={p.Length}");
#endif
#if ANDROID
                if (TransportHeartbeatEnabled)
                {
                    long deadline = System.Threading.Interlocked.Read(ref _backgroundUntilTicks);
                    // Bound both background time and queued world state. Do not drop
                    // selected packets and then continue a desynchronised session.
                    if (Time.Now.Ticks >= deadline ||
                        (deadline != long.MaxValue && GetReceiveListQueueLength() >= 4096))
                    {
#if BUNDLED_RESOURCE_TEST
                        Trace("background keepalive ended: time or receive queue limit");
#endif
                        Disconnecting = true;
                        return;
                    }
                    if (p is G.Ping && !Disconnecting)
                    {
                        Enqueue(new G.Ping());
                        FlushSendQueue();
                        continue;
                    }
                }
#endif
                ReceiveList.Enqueue(p);
            }
        }
        /// <summary>
        /// 开始发送
        /// </summary>
        /// <param name="data"></param>
        private void BeginSend(List<byte> data)
        {
            if (!Connected || data.Count == 0) return;

            // 假人无真实网络连接，跳过网络发送
            if (IsBot) return;

            try
            {
                Sending = true;
                TotalBytesSent += data.Count;
#if ANDROID
                var pending = new PendingSend { Bytes = data.ToArray() };
                Client.Client.BeginSend(pending.Bytes, 0, pending.Bytes.Length, SocketFlags.None, SendData, pending);
#else
                Client.Client.BeginSend(data.ToArray(), 0, data.Count, SocketFlags.None, SendData, null);
#endif
#if ANDROID && BUNDLED_RESOURCE_TEST
                Trace($"socket send scheduled bytes={data.Count}");
#endif
                UpdateTimeOut();
            }
            catch (Exception ex)
            {
                if (AdditionalLogging)
                    OnException(this, ex);
                Disconnecting = true;
                Sending = false;
            }
        }
        /// <summary>
        /// 发送日期
        /// </summary>
        /// <param name="result"></param>
        private void SendData(IAsyncResult result)
        {
#if ANDROID
            lock (_sendLock)
            {
                if (!Connected) return;
                try
                {
                    var pending = (PendingSend)result.AsyncState;
                    int completedBytes = Client.Client.EndSend(result);
                    if (completedBytes == 0) throw new SocketException((int)SocketError.ConnectionReset);
                    pending.Offset += completedBytes;
#if BUNDLED_RESOURCE_TEST
                    Trace($"socket send completed bytes={completedBytes}");
#endif
                    UpdateTimeOut();
                    if (pending.Offset < pending.Bytes.Length)
                    {
                        Client.Client.BeginSend(pending.Bytes, pending.Offset, pending.Bytes.Length - pending.Offset,
                            SocketFlags.None, SendData, pending);
                        return;
                    }
                    Sending = false;
                    // A Ping can arrive while a foreground send is still in flight.
                    // Flush its queued reply even when the frame loop is paused.
                    FlushSendQueueCore();
                }
                catch (Exception ex)
                {
                    if (AdditionalLogging) OnException?.Invoke(this, ex);
                    Disconnecting = true;
                    Sending = false;
                }
            }
#else
            try
            {
                Sending = false;
                int completedBytes = Client.Client.EndSend(result);
#if ANDROID && BUNDLED_RESOURCE_TEST
                Trace($"socket send completed bytes={completedBytes}");
#endif
                UpdateTimeOut();
            }
            catch (Exception ex)
            {
                if (AdditionalLogging)
                    OnException(this, ex);
                Disconnecting = true;
            }
#endif
        }
        /// <summary>
        /// 队列
        /// </summary>
        /// <param name="p"></param>
        public virtual void Enqueue(Packet p)
        {
            if (!Connected || p == null) return;
            // 假人无真实客户端，丢弃所有下行包，避免序列化 Stats.Values（SortedDictionary）
            // 时主线程并发修改导致 InvalidOperationException。
            if (IsBot) return;

            SendList.Enqueue(p);
#if ANDROID && BUNDLED_RESOURCE_TEST
            Trace($"queued {p.GetType().FullName} id={Packet.Packets.IndexOf(p.GetType())}");
#endif
        }
        /// <summary>
        /// 尝试断开连接
        /// </summary>
        public abstract void TryDisconnect();
        /// <summary>
        /// 断开
        /// </summary>
        public virtual void Disconnect()
        {
#if ANDROID
            lock (_sendLock)
            {
#endif
            if (!Connected) return;

            Connected = false;

            SendList = null;
            ReceiveList = null;
            _rawData = null;

            // 假人无真实网络连接，跳过 Client 操作
            if (!IsBot && Client != null)
            {
                Client.Client.Dispose();
                Client = null;
            }
#if ANDROID
            }
#endif
        }
        /// <summary>
        /// 尝试发送断开连接
        /// </summary>
        /// <param name="p"></param>
        public abstract void TrySendDisconnect(Packet p);
        /// <summary>
        /// 发送断开链接
        /// </summary>
        /// <param name="p"></param>
        public virtual void SendDisconnect(Packet p)
        {
            if (!Connected || Disconnecting)
            {
                Disconnecting = true;
                return;
            }

            List<byte> data = new List<byte>();

            data.AddRange(p.GetPacketBytes());

            BeginSendDisconnect(data);
        }
        /// <summary>
        /// 开始断开链接
        /// </summary>
        /// <param name="data"></param>
        private void BeginSendDisconnect(List<byte> data)
        {
            if (!Connected || data.Count == 0) return;

            if (Disconnecting) return;

            // 假人无真实网络连接，跳过网络发送
            if (IsBot)
            {
                Disconnecting = true;
                return;
            }

            try
            {
                Disconnecting = true;

                TotalBytesSent += data.Count;
                Client.Client.BeginSend(data.ToArray(), 0, data.Count, SocketFlags.None, SendDataDisconnect, null);
            }
            catch (Exception ex)
            {
                if (AdditionalLogging)
                    OnException(this, ex);
            }
        }
        /// <summary>
        /// 发送数据断开连接
        /// </summary>
        /// <param name="result"></param>
        private void SendDataDisconnect(IAsyncResult result)
        {
            try
            {
                Client.Client.EndSend(result);
            }
            catch (Exception ex)
            {
                if (AdditionalLogging)
                    OnException(this, ex);
            }
        }
        /// <summary>
        /// 过程
        /// </summary>
        public virtual void Process()
        {
            // 假人无真实网络连接，跳过 Client 状态检测
            if (!IsBot && (Client == null || !Client.Connected))
            {
                TryDisconnect();
                return;
            }

            while (ReceiveList != null && !ReceiveList.IsEmpty && !Disconnecting)
            {
                Packet p = null;
                try
                {
                    if (!ReceiveList.TryDequeue(out p)) continue;

                    ProcessPacket(p);
                }
                catch (NotImplementedException ex)
                {
                    Output?.Invoke(p, $"Process->ProcessPacket {p?.GetType().Name} catch NotImplementedException");
                    OnException(this, ex);
                }
                catch (Exception ex)
                {
                    Output?.Invoke(p, $"Process->ProcessPacket {p?.GetType().Name} catch Exception");
                    OnException(this, ex);
                    //throw ex;
                }
            }

            // 假人连接永不超时，跳过超时检测
            if (!IsBot && Time.Now >= TimeOutTime)
            {
#if ANDROID && BUNDLED_RESOURCE_TEST
                Trace($"local receive timeout disconnecting={Disconnecting} sent={TotalBytesSent} received={TotalBytesReceived} buffered={_rawData?.Length}");
#endif
                if (!Disconnecting)
                    TrySendDisconnect(new G.Disconnect { Reason = DisconnectReason.TimedOut });
                else
                    TryDisconnect();

                return;
            }

            if (!Disconnecting && Sending)
                UpdateTimeOut();

            FlushSendQueue();
        }

        private void FlushSendQueue()
        {
#if ANDROID
            lock (_sendLock) { FlushSendQueueCore(); }
#else
            FlushSendQueueCore();
#endif
        }

        private void FlushSendQueueCore()
        {
#if ANDROID
            if (!Connected || Disconnecting) return;
#endif
            if (SendList == null || SendList.IsEmpty || Sending) return;

            List<byte> data = new List<byte>();
            while (!SendList.IsEmpty)
            {
                Packet p = null;

                if (!SendList.TryDequeue(out p)) continue;

                if (p == null) continue;

                try
                {
                    byte[] bytes = p.GetPacketBytes();

                    data.AddRange(bytes);
#if ANDROID && BUNDLED_RESOURCE_TEST
                    Trace($"serialized {p.GetType().FullName} bytes={bytes.Length}");
#endif
                }
                catch (Exception ex)
                {
                    Output?.Invoke(p, $"Process->GetPacketBytes ->AddRange  {p?.GetType().Name} catch Exception");
                    OnException?.Invoke(this, ex);
                    Disconnecting = true;
                    return;
                }

                if (!Monitor) continue;

#if ANDROID
                lock (Diagnostics)
                {
#endif
                DiagnosticValue value;
                Type type = p.GetType();

                if (!Diagnostics.TryGetValue(type.FullName, out value))
                    Diagnostics[type.FullName] = value = new DiagnosticValue { Name = type.FullName };

                value.Count++;
                value.TotalSize += p.Length;

                if (p.Length > value.LargestSize)
                    value.LargestSize = p.Length;
#if ANDROID
                }
#endif
            }

            BeginSend(data);
        }
        /// <summary>
        /// 处理封包
        /// </summary>
        /// <param name="p"></param>
        private void ProcessPacket(Packet p)
        {
            if (p == null) return;

            DateTime start = Time.Now;

            MethodInfo info;
            if (!PacketMethods.TryGetValue(p.PacketType, out info))
                PacketMethods[p.PacketType] = info = GetType().GetMethod("Process", new[] { p.PacketType });

            if (info == null)
            {
                Output?.Invoke(p, $"未执行异常: 方式过程({p.PacketType}).");
                return;
            }
            try
            {
                info.Invoke(this, new object[] { p });
            }
            catch
            {
                //todo 保存错误日志
                Output?.Invoke(p, $"封包发生错误： {p?.GetType().Name}");
            }
            Monitor = true;
            if (!Monitor) return;

            TimeSpan execution = Time.Now - start;

#if ANDROID
            lock (Diagnostics)
            {
#endif
            DiagnosticValue value;

            if (!Diagnostics.TryGetValue(p.PacketType.FullName, out value))
                Diagnostics[p.PacketType.FullName] = value = new DiagnosticValue { Name = p.PacketType.FullName };

            value.Count++;
            value.TotalTime += execution;
            value.TotalSize += p.Length;

            if (execution > value.LargestTime)
                value.LargestTime = execution;

            if (p.Length > value.LargestSize)
                value.LargestSize = p.Length;
#if ANDROID
            }
#endif
        }
        /// <summary>
        /// 更新超时
        /// </summary>
        public void UpdateTimeOut()
        {
            if (Disconnecting) return;

            TimeOutTime = Time.Now + TimeOutDelay;
        }
    }

    /// <summary>
    /// 诊断值
    /// </summary>
    public class DiagnosticValue
    {
        /// <summary>
        /// 名字
        /// </summary>
        public string Name { get; set; }
        /// <summary>
        /// 总时间
        /// </summary>
        public TimeSpan TotalTime { get; set; }
        /// <summary>
        /// 最终时间
        /// </summary>
        public TimeSpan LargestTime { get; set; }
        /// <summary>
        /// 计数
        /// </summary>
        public int Count { get; set; }
        /// <summary>
        /// 总大小
        /// </summary>
        public long TotalSize { get; set; }
        /// <summary>
        /// 最后大小
        /// </summary>
        public long LargestSize { get; set; }
        /// <summary>
        /// 总滴答数
        /// </summary>
        public long TotalTicks => TotalTime.Ticks;
        /// <summary>
        /// 总计毫秒
        /// </summary>
        public long TotalMilliseconds => TotalTicks / TimeSpan.TicksPerMillisecond;
        /// <summary>
        /// 最后地大叔
        /// </summary>
        public long LargestTicks => LargestTime.Ticks;
        /// <summary>
        /// 最后计数毫秒
        /// </summary>
        public long LargestMilliseconds => LargestTicks / TimeSpan.TicksPerMillisecond;
    }
}
