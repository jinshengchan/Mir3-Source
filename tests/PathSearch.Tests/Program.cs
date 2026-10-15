using Client.Envir;
using Client.Models;
using Client.Scenes.Views;
using Mir3.Mobile;
using System.Drawing;

int passed = 0;
void Check(bool condition, string label)
{
    if (!condition) throw new Exception(label);
    passed++; Console.WriteLine("PASS " + label);
}
async Task<string> Take(BackgroundPathSearch<string> search)
{
    var deadline = DateTime.UtcNow.AddSeconds(5);
    while (search.IsBusy)
    {
        if (search.TryTake(out var result)) return result;
        if (DateTime.UtcNow > deadline) throw new Exception("Search timed out in fixture.");
        await Task.Delay(1);
    }
    return null;
}
var search = new BackgroundPathSearch<string>();
using var started = new ManualResetEventSlim();
using var release = new ManualResetEventSlim();
Check(search.TryStart(token => { started.Set(); release.Wait(token); return "path"; }, TimeSpan.FromSeconds(5)), "Start one background search");
Check(started.Wait(2000) && search.IsBusy, "Worker running without changing foreground state");
Check(!search.TryStart(_ => "second", TimeSpan.FromSeconds(5)), "Do not overlap searches on a shared grid");
Check(!search.TryTake(out _), "Polling incomplete work never blocks the game thread");
release.Set();
Check(await Take(search) == "path" && !search.IsBusy, "Hand completed result to the game thread exactly once");
Check(!search.TryTake(out _), "Consumed result is not applied twice");
started.Reset(); release.Reset();
search.TryStart(_ => { started.Set(); release.Wait(); return "old-map-path"; }, TimeSpan.FromSeconds(5));
Check(started.Wait(2000), "Start a map-change cancellation fixture");
search.Cancel();
Check(search.IsBusy && !search.TryStart(_ => "new", TimeSpan.FromSeconds(5)), "Cancelled worker retains its slot until it actually finishes");
release.Set();
Check(await Take(search) == null && !search.IsBusy, "Discard completed old-map result after cancellation");
search.TryStart(token => { token.WaitHandle.WaitOne(); token.ThrowIfCancellationRequested(); return "unreachable"; }, TimeSpan.FromMilliseconds(30));
Check(await Take(search) == null && !search.IsBusy, "Timed-out search releases its busy state");
search.TryStart(_ => throw new InvalidOperationException("fixture failure"), TimeSpan.FromSeconds(5));
try { await Take(search); throw new Exception("Failure was swallowed."); }
catch (InvalidOperationException) { Check(!search.IsBusy, "Failed worker cannot leave searching permanently latched"); }
search.TryStart(_ => "retry", TimeSpan.FromSeconds(5));
Check(await Take(search) == "retry", "Search can retry after cancellation, timeout and failure");
var map = new MapControl(20, 20);
var finder = new PathFinder(map);
var path = finder.FindPath(new Point(1, 1), new Point(18, 18));
Check(path.First().Location == new Point(1, 1) && path.Last().Location == new Point(18, 18), "Actual A-star still finds an ordinary path");
Check(path.Zip(path.Skip(1)).All(pair => Math.Abs(pair.First.Location.X - pair.Second.Location.X) <= 1 && Math.Abs(pair.First.Location.Y - pair.Second.Location.Y) <= 1), "Every returned step is adjacent");
var originalCells = map.Cells;
map.Cells = new MapCells(20, 20);
for (int x = 0; x < 20; x++) for (int y = 0; y < 20; y++) map.Cells.Block(x, y);
Check(finder.FindPath(new Point(1, 1), new Point(18, 18), default, originalCells)?.Count > 0, "Map replacement cannot switch cells underneath a running search");
using var cancelled = new CancellationTokenSource(); cancelled.Cancel();
try { finder.FindPath(new Point(1, 1), new Point(18, 18), cancelled.Token); throw new Exception("Cancelled search ran."); }
catch (OperationCanceledException) { Check(true, "Actual A-star honors cancellation"); }
var loopA = new Node(2, 2); var loopB = new Node(3, 3); loopA.Parent = loopB; loopB.Parent = loopA;
try { finder.RetracePath(new Node(0, 0), loopA); throw new Exception("Cyclic parent chain ran forever."); }
catch (InvalidOperationException) { Check(true, "Corrupt parent chain cannot loop forever"); }
var large = new MapControl(1000, 1000);
for (int x = 0; x < 1000; x++) large.Cells.Block(x, 500);
using var bounded = new CancellationTokenSource(TimeSpan.FromMilliseconds(30));
try { new PathFinder(large).FindPath(new Point(1, 1), new Point(900, 900), bounded.Token); throw new Exception("Expected cancellation of disconnected large search."); }
catch (OperationCanceledException) { Check(true, "Large unreachable search is cancelled during A-star expansion"); }
long now = 1000;
var frames = new FrameProgress(() => now);
frames.Enter("update"); frames.Updated(); frames.Enter("draw"); frames.Drawn(); frames.Enter("present");
now = 9000;
string report = frames.Report();
Check(report.Contains("update=1 draw=1 present=0") && report.Contains("phase=present phaseMs=8000"), "Background observer identifies a stuck presentation stage");
frames.Presented(); now = 10000;
Check(frames.Report().Contains("present=1") && frames.Report().Contains("presentAgeMs=1000"), "Report completed frames separately from cache generation");
frames.SetPaused(true); frames.SetFocused(false);
Check(frames.Report().Contains("paused=1 focused=0"), "Report real lifecycle and focus independently of frame progress");
frames.SetState("auto=True queue=1");
Check(frames.Report().Contains("auto=True queue=1"), "Observer uses a thread-safe game-thread state snapshot");
Check(frames.ShouldSampleState() && !frames.ShouldSampleState(), "Limit detailed state sampling to once per five seconds");
now += 5000; Check(frames.ShouldSampleState(), "Resume state sampling after its interval");
Console.WriteLine($"PASS: {passed} path handoff and frame progress checks");
