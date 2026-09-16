using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;

namespace LibraryEditor
{
    internal sealed class WtlConversionFailure
    {
        public string FileName { get; private set; }
        public string Message { get; private set; }

        public WtlConversionFailure(string fileName, string message)
        {
            FileName = fileName;
            Message = message;
        }
    }

    internal sealed class WtlConversionBatchResult
    {
        public int SuccessCount { get; set; }
        public List<WtlConversionFailure> Failures { get; private set; }
        public List<string> OutputFiles { get; private set; }

        public WtlConversionBatchResult()
        {
            Failures = new List<WtlConversionFailure>();
            OutputFiles = new List<string>();
        }
    }

    internal static class WtlConversionBatch
    {
        internal static string[] GetTopLevelWtlFiles(string folderPath)
        {
            return Directory.GetFiles(folderPath, "*.wtl", SearchOption.TopDirectoryOnly)
                .OrderBy(x => x, StringComparer.OrdinalIgnoreCase)
                .ToArray();
        }

        internal static WtlConversionBatchResult ConvertFiles(IEnumerable<string> fileNames, bool crypt)
        {
            WtlConversionBatchResult result = new WtlConversionBatchResult();
            foreach (string fileName in fileNames)
            {
                string outputDirectory = Path.Combine(Path.GetDirectoryName(fileName), "ConvertedZL");
                Directory.CreateDirectory(outputDirectory);
                string outputFile = Path.Combine(outputDirectory, Path.GetFileNameWithoutExtension(fileName) + ".Zl");

                WTL1to1ZL library = null;
                try
                {
                    library = new WTL1to1ZL(fileName);
                    library.ToMLibrary(crypt, outputFile);
                    result.SuccessCount++;
                    result.OutputFiles.Add(outputFile);
                }
                catch (Exception ex)
                {
                    result.Failures.Add(new WtlConversionFailure(fileName, ex.GetBaseException().Message));
                }
                finally
                {
                    if (library != null)
                        library.Dispose();
                }
            }

            return result;
        }
    }
}
