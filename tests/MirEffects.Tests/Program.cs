using Client.Envir;
using Client.Models;
using Client.Scenes;
using Library;
using System.Drawing;

int passed = 0;
void Check(bool result, string message)
{
    if (!result) throw new Exception(message);
    passed++;
}
TestEffect Create(int count, int milliseconds = 150)
{
    CEnvir.Now = new DateTime(2026, 10, 8);
    return new TestEffect(count, milliseconds) { Loop = true, Target = MapObject.User };
}

// Reproduce the server's zero-frame overhead title without starting Android.
var empty = Create(0);
Check(empty.Frame() == 0, "Zero-frame loop must complete without dividing by zero");
Check(empty.FrameLight == 0, "Zero-frame light must remain off");
empty.Process();
Check(!GameScene.Game.MapControl.Effects.Contains(empty), "Invalid effect must be removed from the update list");

var zeroDelay = Create(3, 0);
Check(zeroDelay.Frame() == 3, "Zero-duration loop must complete");
Check(zeroDelay.FrameLight == 0, "Zero-duration light must remain off");
zeroDelay.Process();
Check(!GameScene.Game.MapControl.Effects.Contains(zeroDelay), "Zero-duration effect must be removed");

var normal = Create(3);
normal.StartLight = 0;
normal.EndLight = 9;
CEnvir.Now = normal.StartTime.AddMilliseconds(225);
Check(normal.Frame() == 1, "Valid loop must advance to frame one");
normal.Process();
Check(normal.FrameIndex == 1 && normal.DrawFrame == 101, "Valid effect must publish its current sprite frame");
Check(normal.FrameLight == 4f, "Valid light must retain its existing integer interpolation");
CEnvir.Now = normal.StartTime.AddMilliseconds(450);
Check(normal.Frame() == 0, "Valid loop must wrap to its first frame");
normal.Loop = false;
normal.Process();
Check(!GameScene.Game.MapControl.Effects.Contains(normal), "Completed non-looping effect must be removed");

var reverse = Create(3);
reverse.Reversed = true;
CEnvir.Now = reverse.StartTime.AddMilliseconds(150);
reverse.Process();
Check(reverse.DrawFrame == 101, "Reversed valid animation must still advance");
Console.WriteLine($"PASS: {passed} effect animation checks (actual MirEffect implementation)");

sealed class TestEffect : MirEffect
{
    public TestEffect(int count, int milliseconds)
        : base(100, count, TimeSpan.FromMilliseconds(milliseconds), LibraryFile.Title, 0, 0, Color.White) { }
    public int Frame() => GetFrame();
}
