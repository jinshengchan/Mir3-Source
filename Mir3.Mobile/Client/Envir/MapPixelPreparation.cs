using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;

namespace Client.Envir
{
    // Bounded CPU work and completed pixels. GPU operations remain on the game thread.
    internal sealed class MapPixelPreparation
    {
        private readonly object _sync = new object();
        private readonly HashSet<Pending> _pending = new HashSet<Pending>();
        private readonly SemaphoreSlim _workers = new SemaphoreSlim(2);
        private long _bytes;
        internal const long ByteLimit = 32 * 1024 * 1024;
        public int Count { get { lock (_sync) return _pending.Count; } }

        public void CancelAll()
        {
            Pending[] pending;
            lock (_sync) pending = _pending.ToArray();
            foreach (var p in pending) p.Dispose();
        }

        public Pending TryStart(byte[] bytes, bool zircon, MapImagePixels.Plane image,
            MapImagePixels.Plane shadow, MapImagePixels.Plane overlay, DateTime now)
        {
            Pending[] expired;
            lock (_sync) expired = _pending.Where(p => now >= p.Expires).ToArray();
            foreach (var p in expired) p.Dispose();
            long size = Estimate(image) + Estimate(shadow) + Estimate(overlay);
            Pending pending;
            lock (_sync)
            {
                if (_pending.Count >= 32 || _bytes + size > ByteLimit) return null;
                pending = new Pending(this, size, now.AddSeconds(5));
                _pending.Add(pending);
                _bytes += size;
            }
            pending.Task = System.Threading.Tasks.Task.Run(async () =>
            {
                await _workers.WaitAsync().ConfigureAwait(false);
                try
                {
                    if (pending.Cancelled) return null;
                    return MapImagePixels.Decode(bytes, zircon, image, shadow, overlay);
                }
                finally { _workers.Release(); }
            });
            return pending;
        }

        public static long Estimate(MapImagePixels.Plane plane) => plane.Length == 0 ? 0 :
            ((long)plane.Width + 3) / 4 * 4 * (((long)plane.Height + 3) / 4 * 4) * 4;

        private void Release(Pending pending)
        {
            lock (_sync)
                if (_pending.Remove(pending)) _bytes -= pending.Bytes;
            // Drop the Task's retained decoded result as well as the lease.
            pending.Task = null;
        }

        internal sealed class Pending : IDisposable
        {
            private readonly MapPixelPreparation _owner;
            private int _cancelled;
            internal readonly long Bytes;
            internal readonly DateTime Expires;
            internal Task<MapImagePixels> Task;
            public bool Cancelled => Volatile.Read(ref _cancelled) != 0;
            public bool Finished { get { var task = Task; return task == null || task.IsCompleted; } }
            internal Pending(MapPixelPreparation owner, long bytes, DateTime expires)
            { _owner = owner; Bytes = bytes; Expires = expires; }

            public MapImagePixels Take()
            {
                var task = Task;
                if (Cancelled || task == null) return null;
                if (!task.IsCompleted) throw new InvalidOperationException("Pixels are not ready.");
                try { return task.GetAwaiter().GetResult(); }
                finally { Dispose(); }
            }

            public void Dispose()
            {
                if (Interlocked.Exchange(ref _cancelled, 1) != 0) return;
                var task = Task;
                if (task == null) return;
                // Keep running/cancelled jobs charged until completion. This
                // prevents rapid teleports from creating an unbounded backlog.
                task.ContinueWith(completed =>
                {
                    _ = completed.Exception;
                    _owner.Release(this);
                }, CancellationToken.None, TaskContinuationOptions.ExecuteSynchronously, TaskScheduler.Default);
            }
        }
    }
}
