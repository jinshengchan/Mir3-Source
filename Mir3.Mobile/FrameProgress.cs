using System;
using System.Diagnostics;
using System.Threading;

namespace Mir3.Mobile
{
    // Thread-safe metadata only. The observer never touches the scene or GPU.
    internal sealed class FrameProgress
    {
        private readonly Func<long> _clock;
        private long _updates, _draws, _presents, _lastUpdate, _lastDraw, _lastPresent;
        private long _phaseSince, _nextState;
        private string _phase = "startup", _state = "not-sampled";
        private int _paused, _focused = 1;
        internal FrameProgress(Func<long> clock = null)
        {
            _clock = clock ?? (() => (long)(Stopwatch.GetTimestamp() * (1000d / Stopwatch.Frequency)));
            _lastUpdate = _lastDraw = _lastPresent = _phaseSince = _clock();
        }
        internal void Enter(string phase)
        {
            Interlocked.Exchange(ref _phaseSince, _clock());
            Volatile.Write(ref _phase, phase);
        }
        internal void Updated() { Interlocked.Increment(ref _updates); Interlocked.Exchange(ref _lastUpdate, _clock()); Enter("after-update"); }
        internal void Drawn() { Interlocked.Increment(ref _draws); Interlocked.Exchange(ref _lastDraw, _clock()); Enter("after-draw"); }
        internal void Presented() { Interlocked.Increment(ref _presents); Interlocked.Exchange(ref _lastPresent, _clock()); Enter("between-frames"); }
        internal void SetPaused(bool paused) => Volatile.Write(ref _paused, paused ? 1 : 0);
        internal void SetFocused(bool focused) => Volatile.Write(ref _focused, focused ? 1 : 0);
        internal bool ShouldSampleState()
        {
            long now = _clock();
            if (now < _nextState) return false;
            _nextState = now + 5000;
            return true;
        }
        internal void SetState(string state) => Volatile.Write(ref _state, state);
        internal string Report()
        {
            long now = _clock();
            return $"runtime update={Interlocked.Read(ref _updates)} draw={Interlocked.Read(ref _draws)} present={Interlocked.Read(ref _presents)} " +
                $"updateAgeMs={now - Interlocked.Read(ref _lastUpdate)} drawAgeMs={now - Interlocked.Read(ref _lastDraw)} presentAgeMs={now - Interlocked.Read(ref _lastPresent)} " +
                $"phase={Volatile.Read(ref _phase)} phaseMs={now - Interlocked.Read(ref _phaseSince)} paused={Volatile.Read(ref _paused)} focused={Volatile.Read(ref _focused)} {Volatile.Read(ref _state)}";
        }
    }
}
