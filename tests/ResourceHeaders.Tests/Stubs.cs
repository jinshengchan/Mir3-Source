using System.Collections.Concurrent;
namespace Library { public static class Time { public static DateTime Now => DateTime.UtcNow; } }
namespace Client.Controls
{
    public class DXMessageBox
    {
        public bool IsDisposed;
        public static DXMessageBox Show(string a, string b) => new();
        public void TryDispose() => IsDisposed = true;
    }
}
namespace Client.Envir
{
    public static class Config { public static string MicroClientIP = "127.0.0.1"; public static int MicroClientPort; }
    public sealed class MirLibrary { public string FullPathName; public int Resets; public void ResetResourceReader() => Resets++; }
    public static class CEnvir
    {
        public static string MobileClientPath;
        public static Dictionary<int, MirLibrary> LibraryList = new();
        public static ConcurrentQueue<string> Errors = new();
        public static void SaveError(string value) => Errors.Enqueue(value);
    }
}
namespace Mir3.Mobile
{
    public static class ConnectionDiagnostics { public static void Record(string value) { } }
    public class NativeStub { public string SafeCode => "test"; }
    public static class Game1 { public static NativeStub Native = new(); }
}
namespace Client.Scenes
{
    public class TextureStub { public bool TextureValid = true; }
    public class MapStub : TextureStub { public TextureStub FLayer = new(); }
    public class GameStub { public MapStub MapControl = new(); }
    public static class GameScene { public static GameStub Game = new(); }
}
