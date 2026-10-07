using System;
using System.Collections.Generic;
using System.IO;
using System.IO.Compression;
using System.Security.Cryptography;

namespace Patch
{
    // Streams APK assets to disk: large asset streams need not support Seek.
    public static class BundledResources
    {
        const string Marker = ".bundled-resources.sha256";

        public static bool Install(Func<string, Stream> openAsset, string root, bool repair, Action<string> progress)
        {
            byte[] manifest;
            try
            {
                using (var stream = openAsset("LocalUpdate/PList.Bin"))
                using (var buffer = new MemoryStream())
                {
                    stream.CopyTo(buffer);
                    manifest = buffer.ToArray();
                }
            }
            catch (FileNotFoundException) { return false; } // Existing online-only APK.

            byte[] package;
            using (var stream = openAsset("LocalUpdate/APKVersion.bin"))
            using (var buffer = new MemoryStream())
            {
                stream.CopyTo(buffer);
                package = buffer.ToArray();
            }
            string fingerprint;
            using (var sha = SHA256.Create())
            using (var buffer = new MemoryStream())
            {
                buffer.Write(manifest, 0, manifest.Length);
                buffer.Write(package, 0, package.Length);
                fingerprint = BitConverter.ToString(sha.ComputeHash(buffer.ToArray()));
            }
            var patches = new List<PatchInformation>();
            using (var reader = new BinaryReader(new MemoryStream(manifest)))
                while (reader.BaseStream.Position < reader.BaseStream.Length)
                {
                    var patch = new PatchInformation(reader);
                    Resolve(root, patch.FileName);
                    if (patch.CheckSum.Length != 16 || patch.CompressedLength < 0)
                        throw new InvalidDataException("Invalid bundled patch manifest.");
                    patches.Add(patch);
                }

            string marker = Path.Combine(root, Marker);
            bool installed = File.Exists(marker) && File.ReadAllText(marker) == fingerprint;
            if (installed && !repair && Directory.Exists(Path.Combine(root, "Map")) &&
                patches.TrueForAll(p => File.Exists(Resolve(root, p.FileName))))
                return true; // Do not downgrade newer files downloaded from the server.

            string baseName;
            long baseLength;
            byte[] baseHash;
            using (var reader = new BinaryReader(new MemoryStream(package)))
            {
                reader.ReadString(); // APK version, owned by the APK installer.
                reader.ReadString();
                reader.ReadInt64();
                int hashLength = reader.ReadInt32();
                if (hashLength != 16) throw new InvalidDataException("Invalid APK checksum.");
                reader.ReadBytes(hashLength);
                baseName = reader.ReadString();
                baseLength = reader.ReadInt64();
                hashLength = reader.ReadInt32();
                if (hashLength != 16 || baseLength < 0 || baseName != Path.GetFileName(baseName) || baseName.Contains("\\"))
                    throw new InvalidDataException("Invalid bundled base package.");
                baseHash = reader.ReadBytes(hashLength);
                if (baseHash.Length != 16 || reader.BaseStream.Position != reader.BaseStream.Length)
                    throw new InvalidDataException("Truncated bundled package manifest.");
            }

            Directory.CreateDirectory(root);
            progress?.Invoke("正在安装内置基础资源...");
            InstallZip(() => openAsset("LocalUpdate/" + baseName), root, baseLength, baseHash);
            if (!Directory.Exists(Path.Combine(root, "Map")))
                throw new InvalidDataException("Bundled base package has no Map directory.");

            foreach (var patch in patches)
            {
                progress?.Invoke("正在安装内置资源: " + patch.FileName);
                string destination = Resolve(root, patch.FileName);
                if (!repair && File.Exists(destination) && Matches(destination, patch.CheckSum)) continue;
                Directory.CreateDirectory(Path.GetDirectoryName(destination));
                string temp = destination + "." + Guid.NewGuid().ToString("N") + ".tmp";
                try
                {
                    string asset = "LocalUpdate/" + patch.FileName.Replace("\\", "-").Replace("/", "-") + ".gz";
                    using (var input = openAsset(asset))
                    using (var gzip = new GZipStream(input, CompressionMode.Decompress))
                    using (var output = File.Create(temp)) gzip.CopyTo(output);
                    if (!Matches(temp, patch.CheckSum)) throw new InvalidDataException("Bundled checksum mismatch: " + patch.FileName);
                    File.Move(temp, destination, true);
                }
                finally { if (File.Exists(temp)) File.Delete(temp); }
            }
            WriteAtomic(Path.Combine(root, "Version.bin"), manifest);
            WriteAtomic(Path.Combine(root, "APKVersion.bin"), package);
            WriteAtomic(marker, System.Text.Encoding.UTF8.GetBytes(fingerprint));
            return true;
        }

        public static void InstallZip(Func<Stream> open, string root, long expectedLength = -1, byte[] expectedHash = null)
        {
            Directory.CreateDirectory(root);
            string archive = Path.Combine(root, ".resource-" + Guid.NewGuid().ToString("N") + ".zip");
            try
            {
                using (var input = open())
                using (var output = File.Create(archive)) input.CopyTo(output);
                if (expectedLength >= 0 && new FileInfo(archive).Length != expectedLength)
                    throw new InvalidDataException("Bundled ZIP length mismatch.");
                if (expectedHash != null && !Matches(archive, expectedHash))
                    throw new InvalidDataException("Bundled ZIP checksum mismatch.");
                using (var zip = ZipFile.OpenRead(archive))
                {
                    foreach (var entry in zip.Entries) Resolve(root, entry.FullName); // Validate before writing.
                    foreach (var entry in zip.Entries)
                    {
                        string destination = Resolve(root, entry.FullName);
                        if (entry.FullName.EndsWith("/") || entry.FullName.EndsWith("\\"))
                        { Directory.CreateDirectory(destination); continue; }
                        Directory.CreateDirectory(Path.GetDirectoryName(destination));
                        string temp = destination + "." + Guid.NewGuid().ToString("N") + ".tmp";
                        try
                        {
                            using (var input = entry.Open())
                            using (var output = File.Create(temp)) input.CopyTo(output);
                            File.Move(temp, destination, true);
                        }
                        finally { if (File.Exists(temp)) File.Delete(temp); }
                    }
                }
            }
            finally { if (File.Exists(archive)) File.Delete(archive); }
        }

        static string Resolve(string root, string relative)
        {
            relative = relative.Replace('\\', '/');
            if (string.IsNullOrWhiteSpace(relative) || relative.StartsWith("/") || relative.Contains(":"))
                throw new InvalidDataException("Invalid resource path.");
            foreach (var part in relative.Split('/'))
                if (part == ".." || part.StartsWith(".bundled-resources") || part.StartsWith(".resource-"))
                    throw new InvalidDataException("Resource path escapes its directory.");
            string prefix = Path.GetFullPath(root).TrimEnd(Path.DirectorySeparatorChar) + Path.DirectorySeparatorChar;
            string path = Path.GetFullPath(Path.Combine(prefix, relative));
            if (!path.StartsWith(prefix, StringComparison.Ordinal)) throw new InvalidDataException("Invalid resource path.");
            return path;
        }

        static bool Matches(string file, byte[] expected)
        {
            using (var md5 = MD5.Create())
            using (var stream = File.OpenRead(file))
            {
                byte[] actual = md5.ComputeHash(stream);
                if (actual.Length != expected.Length) return false;
                for (int i = 0; i < actual.Length; i++) if (actual[i] != expected[i]) return false;
                return true;
            }
        }

        static void WriteAtomic(string destination, byte[] data)
        {
            string temp = destination + "." + Guid.NewGuid().ToString("N") + ".tmp";
            try { File.WriteAllBytes(temp, data); File.Move(temp, destination, true); }
            finally { if (File.Exists(temp)) File.Delete(temp); }
        }
    }
}
