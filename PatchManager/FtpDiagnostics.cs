using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Net;
using System.Text;

namespace PatchManager
{
    internal sealed class FtpFailureReport
    {
        internal string UserMessage { get; }
        internal string LogPath { get; }
        internal string LogWriteError { get; }

        internal FtpFailureReport(string userMessage, string logPath, string logWriteError)
        {
            UserMessage = userMessage;
            LogPath = logPath;
            LogWriteError = logWriteError;
        }
    }

    internal static class FtpDiagnostics
    {
        private static readonly object LogSync = new object();

        internal static string LogPath
        {
            get
            {
                string assemblyDirectory = Path.GetDirectoryName(typeof(FtpDiagnostics).Assembly.Location);
                if (string.IsNullOrEmpty(assemblyDirectory))
                    assemblyDirectory = AppDomain.CurrentDomain.BaseDirectory;

                return Path.GetFullPath(Path.Combine(assemblyDirectory, "PatchManager.log"));
            }
        }

        internal static FtpFailureReport RecordFailure(string mode, string stage, Uri target, Exception error, string password)
        {
            string logPath = LogPath;
            Exception actualError = error ?? new InvalidOperationException("未知 FTP 错误");
            WebException webError = FindWebException(actualError);
            FtpWebResponse ftpResponse = webError == null ? null : webError.Response as FtpWebResponse;
            string safeMode = Redact(mode, password);
            string safeStage = Redact(stage, password);
            string safeTarget = SanitizeTarget(target, password);
            string safeErrorType = Redact(actualError.GetType().FullName, password);
            string safeErrorMessage = Redact(actualError.Message, password);
            string webStatus = webError == null ? "无" : Redact(webError.Status.ToString(), password);

            StringBuilder userMessage = new StringBuilder();
            userMessage.AppendFormat(CultureInfo.InvariantCulture,
                "{0}：{1}失败。目标：{2}；异常：{3}：{4}；WebExceptionStatus：{5}",
                safeMode, safeStage, safeTarget, safeErrorType, safeErrorMessage, webStatus);

            if (ftpResponse != null)
            {
                userMessage.AppendFormat(CultureInfo.InvariantCulture,
                    "；FTP状态码：{0}；状态说明：{1}",
                    Redact(ftpResponse.StatusCode.ToString(), password),
                    Redact(ftpResponse.StatusDescription, password));
            }

            string logWriteError = null;
            string logEntry = BuildLogEntry(safeMode, safeStage, safeTarget, actualError, webError, ftpResponse, password);
            try
            {
                AppendLog(logEntry);
            }
            catch (Exception logError)
            {
                logWriteError = Redact(logError.Message, password);
            }

            if (!string.IsNullOrEmpty(logWriteError))
                userMessage.Append("；日志写入失败：").Append(logWriteError);

            userMessage.Append("；日志：").Append(logPath);
            return new FtpFailureReport(userMessage.ToString(), logPath, logWriteError);
        }

        internal static void RecordConnectionStep(string mode, string stage, Uri target, string detail, string password)
        {
            string entry = string.Format(CultureInfo.InvariantCulture,
                "[{0}] Mode={1}; Stage={2}; Target={3}; Detail={4}{5}",
                DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss.fff", CultureInfo.InvariantCulture),
                Redact(mode, password),
                Redact(stage, password),
                SanitizeTarget(target, password),
                Environment.NewLine + "  Result=" + Redact(detail, password),
                Environment.NewLine);

            try
            {
                AppendLog(entry);
            }
            catch
            {
                // A diagnostic write must never replace the FTP operation result.
            }
        }

        private static string BuildLogEntry(string mode, string stage, string target, Exception error, WebException webError, FtpWebResponse ftpResponse, string password)
        {
            StringBuilder entry = new StringBuilder();
            entry.Append('[').Append(DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss.fff", CultureInfo.InvariantCulture)).AppendLine("]");
            entry.Append("Mode: ").AppendLine(Redact(mode, password));
            entry.Append("Stage: ").AppendLine(Redact(stage, password));
            entry.Append("Target: ").AppendLine(Redact(target, password));
            entry.Append("ExceptionType: ").AppendLine(Redact(error.GetType().FullName, password));
            entry.Append("ExceptionMessage: ").AppendLine(Redact(error.Message, password));
            entry.Append("WebExceptionStatus: ").AppendLine(webError == null ? "无" : Redact(webError.Status.ToString(), password));

            if (ftpResponse != null)
            {
                entry.Append("FtpStatusCode: ").AppendLine(Redact(ftpResponse.StatusCode.ToString(), password));
                entry.Append("FtpStatusDescription: ").AppendLine(Redact(ftpResponse.StatusDescription, password));
            }
            else
            {
                entry.AppendLine("FtpStatusCode: 无");
                entry.AppendLine("FtpStatusDescription: 无");
            }

            entry.Append("InnerExceptionChain: ").AppendLine(FormatInnerExceptionChain(error, password));
            entry.AppendLine("Stack:");
            entry.AppendLine(Redact(error.ToString(), password));
            entry.AppendLine();
            return entry.ToString();
        }

        private static string FormatInnerExceptionChain(Exception error, string password)
        {
            List<string> chain = new List<string>();
            Exception current = error;
            while (current != null)
            {
                chain.Add(Redact(current.GetType().FullName + ": " + current.Message, password));
                current = current.InnerException;
            }

            return string.Join(" -> ", chain.ToArray());
        }

        private static WebException FindWebException(Exception error)
        {
            WebException webError = error as WebException;
            if (webError != null)
                return webError;

            AggregateException aggregate = error as AggregateException;
            if (aggregate != null)
            {
                foreach (Exception inner in aggregate.Flatten().InnerExceptions)
                {
                    webError = FindWebException(inner);
                    if (webError != null)
                        return webError;
                }
            }

            return error.InnerException == null ? null : FindWebException(error.InnerException);
        }

        private static string SanitizeTarget(Uri target, string password)
        {
            if (target == null)
                return "<null>";

            try
            {
                UriBuilder builder = new UriBuilder(target)
                {
                    UserName = string.Empty,
                    Password = string.Empty
                };
                return Redact(builder.Uri.AbsoluteUri, password);
            }
            catch
            {
                return Redact(target.ToString(), password);
            }
        }

        private static string Redact(string value, string password)
        {
            if (value == null)
                return string.Empty;
            if (string.IsNullOrEmpty(password))
                return value;

            string redacted = value.Replace(password, "***");
            string encodedPassword = Uri.EscapeDataString(password);
            if (!string.Equals(encodedPassword, password, StringComparison.Ordinal))
                redacted = redacted.Replace(encodedPassword, "***");
            return redacted;
        }

        private static void AppendLog(string entry)
        {
            lock (LogSync)
            {
                File.AppendAllText(LogPath, entry, new UTF8Encoding(false));
            }
        }
    }

    internal sealed class FtpProbeResult
    {
        internal bool Success { get; }
        internal string FailedStage { get; }
        internal Exception Error { get; }
        internal string RemoteFileName { get; }
        internal bool RemoteFileMayRemain { get; }

        internal FtpProbeResult(bool success, string failedStage, Exception error, string remoteFileName, bool remoteFileMayRemain)
        {
            Success = success;
            FailedStage = failedStage;
            Error = error;
            RemoteFileName = remoteFileName;
            RemoteFileMayRemain = remoteFileMayRemain;
        }
    }

    internal static class FtpConnectionProbe
    {
        internal static string CreateRemoteFileName()
        {
            return ".patchmanager-test-" + Guid.NewGuid().ToString("N") + ".tmp";
        }

        internal static FtpProbeResult Execute(Uri target, byte[] expected, Action<Uri, byte[]> upload, Func<Uri, byte[]> download, Action<Uri> delete)
        {
            string remoteFileName = CreateRemoteFileName();
            Uri remoteTarget = CreateRemoteTarget(target, remoteFileName);
            byte[] expectedBytes = expected ?? new byte[0];
            Exception primaryError = null;
            string failedStage = null;
            bool uploadAttempted = false;
            bool uploadCompleted = false;

            try
            {
                uploadAttempted = true;
                upload(remoteTarget, expectedBytes);
                uploadCompleted = true;
            }
            catch (Exception error)
            {
                failedStage = "上传测试文件";
                primaryError = error;
            }

            if (uploadCompleted)
            {
                try
                {
                    byte[] actualBytes = download(remoteTarget);
                    if (!BytesEqual(expectedBytes, actualBytes))
                    {
                        failedStage = "回读校验";
                        primaryError = new InvalidOperationException("回读校验失败");
                    }
                }
                catch (Exception error)
                {
                    failedStage = "回读校验";
                    primaryError = error;
                }
            }

            Exception cleanupError = null;
            if (uploadAttempted)
            {
                try
                {
                    delete(remoteTarget);
                }
                catch (Exception error)
                {
                    cleanupError = error;
                }
            }

            if (primaryError == null && cleanupError == null)
                return new FtpProbeResult(true, null, null, remoteFileName, false);

            if (cleanupError != null)
            {
                string cleanupMessage = "删除测试文件失败，远端可能残留：" + remoteFileName;
                if (primaryError == null)
                {
                    primaryError = new InvalidOperationException(cleanupMessage, cleanupError);
                    failedStage = "删除测试文件";
                }
                else
                {
                    primaryError = new AggregateException(cleanupMessage, primaryError, cleanupError);
                }
            }

            return new FtpProbeResult(false, failedStage, primaryError, remoteFileName, cleanupError != null);
        }

        private static Uri CreateRemoteTarget(Uri target, string remoteFileName)
        {
            if (target == null)
                throw new ArgumentNullException("target");

            string baseUri = target.AbsoluteUri;
            if (!baseUri.EndsWith("/", StringComparison.Ordinal))
                baseUri += "/";

            return new Uri(baseUri + remoteFileName, UriKind.Absolute);
        }

        private static bool BytesEqual(byte[] expected, byte[] actual)
        {
            if (actual == null || expected.Length != actual.Length)
                return false;

            for (int i = 0; i < expected.Length; i++)
            {
                if (expected[i] != actual[i])
                    return false;
            }

            return true;
        }
    }
}
