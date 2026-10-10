using System;
using System.IO;

namespace Mir3.Mobile
{
    public static class ConnectionDiagnostics
    {
        private static readonly object Sync = new object();
        private static string path;
        private static int count;
        private static int mapCount;

        public static void Initialize(string root)
        {
#if ANDROID && BUNDLED_RESOURCE_TEST
            lock (Sync)
            {
                Directory.CreateDirectory(root);
                path = Path.Combine(root, "connection-debug.txt");
                count = 0;
                mapCount = 0;
                File.AppendAllText(path, $"\n=== 进入游戏诊断 v1 {DateTime.Now:O} ===\n");
            }
#endif
        }

        // Log metadata and state only. Never log packet payloads or credentials.
        public static void Record(string message)
        {
#if ANDROID && BUNDLED_RESOURCE_TEST
            lock (Sync)
            {
                if (path == null) return;
                // Preserve map timings after the packet trace fills its budget.
                bool map = message.StartsWith("map-cache", StringComparison.Ordinal);
                if (map ? mapCount++ >= 600 : count++ >= 5000) return;
                try { File.AppendAllText(path, $"[{DateTime.Now:HH:mm:ss.fff}] {message}\n"); }
                catch { /* Diagnostics must not stop networking. */ }
            }
#endif
        }
    }
}
