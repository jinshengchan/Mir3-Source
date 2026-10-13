using System;
using System.IO;
using System.Reflection;

namespace Mir3.Mobile
{
    public static class ConnectionDiagnostics
    {
        private static readonly object Sync = new object();
        private static string path;
        private static int count;
        private static int mapCount;
        private static int errorCount;
        public static string BuildLabel
        {
            get
            {
                string version = typeof(ConnectionDiagnostics).Assembly
                    .GetCustomAttribute<AssemblyInformationalVersionAttribute>()?.InformationalVersion ?? "unknown";
                int separator = version.IndexOf('+');
                string revision = separator >= 0 ? version.Substring(separator + 1) : version;
                return revision.Length > 12 ? revision.Substring(0, 12) : revision;
            }
        }

        public static void Initialize(string root)
        {
#if ANDROID && BUNDLED_RESOURCE_TEST
            lock (Sync)
            {
                Directory.CreateDirectory(root);
                path = Path.Combine(root, "connection-debug.txt");
                count = 0;
                mapCount = 0;
                errorCount = 0;
                File.AppendAllText(path, $"\n=== 进入游戏诊断 v2 build={BuildLabel} {DateTime.Now:O} ===\n");
            }
#endif
        }

        // Log metadata and state only. Never log packet payloads or credentials.
        public static void Record(string message) => Write(message, false);
        public static void RecordError(string message) => Write(message, true);

        private static void Write(string message, bool error)
        {
#if ANDROID && BUNDLED_RESOURCE_TEST
            lock (Sync)
            {
                if (path == null) return;
                // Preserve map timings after the packet trace fills its budget.
                bool map = message.StartsWith("map-cache", StringComparison.Ordinal);
                if (error ? errorCount++ >= 100 : map ? mapCount++ >= 600 : count++ >= 5000) return;
                try { File.AppendAllText(path, $"[{DateTime.Now:HH:mm:ss.fff}] {message}\n"); }
                catch { /* Diagnostics must not stop networking. */ }
            }
#endif
        }
    }
}
