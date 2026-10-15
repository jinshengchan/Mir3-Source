using System;
using System.Threading;
using System.Threading.Tasks;

namespace Client.Envir
{
    // Owned by the game thread. Workers only produce a result; they never edit
    // the path being followed or the map/minimap controls.
    internal sealed class BackgroundPathSearch<T> where T : class
    {
        private Task<T> _task;
        private CancellationTokenSource _cancellation;
        private bool _discard;
        public bool IsBusy => _task != null;

        public bool TryStart(Func<CancellationToken, T> search, TimeSpan timeout)
        {
            if (_task != null) return false;
            _discard = false;
            _cancellation = new CancellationTokenSource(timeout);
            var token = _cancellation.Token;
            _task = Task.Run(() => search(token), token);
            return true;
        }

        public void Cancel()
        {
            _discard = true;
            _cancellation?.Cancel();
        }

        public bool TryTake(out T result)
        {
            result = null;
            if (_task == null || !_task.IsCompleted) return false;
            try
            {
                T completed = _task.GetAwaiter().GetResult();
                if (_discard || _cancellation.IsCancellationRequested) return false;
                result = completed;
                return true;
            }
            catch (OperationCanceledException) { return false; }
            finally
            {
                _task = null;
                _cancellation.Dispose();
                _cancellation = null;
            }
        }
    }
}
