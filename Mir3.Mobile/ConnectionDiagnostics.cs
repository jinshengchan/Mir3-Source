using System;
using System.IO;

namespace Mir3.Mobile
{
    public static class ConnectionDiagnostics
    {
        private static readonly object Sync = new object();
        private static string path;
        private static int count;

        public static void Initialize(string root)
        {
#if ANDROID && BUNDLED_RESOURCE_TEST
            lock (Sync)
            {
                Directory.CreateDirectory(root);
                path = Path.Combine(root, "connection-debug.txt");
                count = 0;
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
                if (path == null || count++ >= 5000) return;
                try { File.AppendAllText(path, $"[{DateTime.Now:HH:mm:ss.fff}] {message}\n"); }
                catch { /* Diagnostics must not stop networking. */ }
            }
#endif
        }
    }
}
