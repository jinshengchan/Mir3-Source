using System;
using System.Collections.Generic;
using System.Diagnostics;

namespace Client.Envir
{
    // Only used on the game thread. Visible drawing takes priority over this queue.
    internal sealed class BudgetedPreloadQueue<T>
    {
        private readonly Queue<T> _pending = new Queue<T>();
        private readonly HashSet<T> _seen = new HashSet<T>();
        public int Count => _pending.Count;

        public void Clear()
        {
            _pending.Clear();
            _seen.Clear();
        }

        public void Add(T item)
        {
            if (_seen.Count < 512 && _seen.Add(item)) _pending.Enqueue(item);
        }

        public void Process(Func<T, bool> prepare, int maxAttempts, TimeSpan budget)
        {
            int attempts = Math.Min(maxAttempts, _pending.Count);
            long start = Stopwatch.GetTimestamp();
            for (int i = 0; i < attempts; i++)
            {
                if ((Stopwatch.GetTimestamp() - start) / (double)Stopwatch.Frequency >= budget.TotalSeconds) break;
                T item = _pending.Dequeue();
                if (!prepare(item)) _pending.Enqueue(item);
            }
        }
    }
}
