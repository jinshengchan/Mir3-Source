using System.IO.Compression;
using System.Security.Cryptography;
using Patch;

if (args.Length == 3 && args[0] == "--assets")
{
    var source = Path.GetFullPath(args[1]);
    var destination = Path.GetFullPath(args[2]);
    BundledResources.InstallZip(() => File.OpenRead(Path.Combine(source, "Data.zip")), destination);
    if (!BundledResources.Install(path => File.OpenRead(Path.Combine(source, path)), destination, false, Console.WriteLine))
        throw new Exception("Bundled manifest missing");
    Console.WriteLine("PASS: real bundled resources installed and checksums verified");
    return;
}

int passed = 0;
void Check(bool condition, string message) { if (!condition) throw new Exception(message); passed++; }
byte[] Zip(string name, byte[] content)
{
    using var buffer = new MemoryStream();
    using (var zip = new ZipArchive(buffer, ZipArchiveMode.Create, true))
    using (var stream = zip.CreateEntry(name).Open()) stream.Write(content);
    return buffer.ToArray();
}
byte[] Gzip(byte[] content)
{
    using var buffer = new MemoryStream();
    using (var gzip = new GZipStream(buffer, CompressionMode.Compress, true)) gzip.Write(content);
    return buffer.ToArray();
}
void Fails(Action action, string message)
{
    try { action(); } catch (InvalidDataException) { passed++; return; }
    throw new Exception(message);
}
string root = Path.Combine(Path.GetTempPath(), "mir3-bundled-" + Guid.NewGuid().ToString("N"));
var assets = new Dictionary<string, byte[]>();
var payload = System.Text.Encoding.UTF8.GetBytes("verified resource content");
var baseZip = Zip("Map/example.map", new byte[] { 1, 2, 3 });
var gzipBytes = Gzip(payload);
assets["LocalUpdate/DataAdd.zip"] = baseZip;
assets["LocalUpdate/Data-example.Zl.gz"] = gzipBytes;
using (var buffer = new MemoryStream())
{
    using (var writer = new BinaryWriter(buffer, System.Text.Encoding.UTF8, true))
        new PatchInformation { FileName = "Data\\example.Zl", CompressedLength = gzipBytes.Length, CheckSum = MD5.HashData(payload) }.Save(writer);
    assets["LocalUpdate/PList.Bin"] = buffer.ToArray();
}
using (var buffer = new MemoryStream())
{
    using (var writer = new BinaryWriter(buffer, System.Text.Encoding.UTF8, true))
    {
        writer.Write("1.0.1"); writer.Write("client.apk"); writer.Write(1L);
        writer.Write(16); writer.Write(new byte[16]); writer.Write("DataAdd.zip");
        writer.Write((long)baseZip.Length); writer.Write(16); writer.Write(MD5.HashData(baseZip));
    }
    assets["LocalUpdate/APKVersion.bin"] = buffer.ToArray();
}
Stream Open(string path) => assets.TryGetValue(path, out var bytes) ? new NonSeekStream(bytes) : throw new FileNotFoundException(path);
try
{
    var progress = new List<double>();
    var statuses = new List<string>();
    Check(BundledResources.Install(Open, root, false, statuses.Add, progress.Add), "first install");
    Check(progress.Any(value => value > 0 && value < 1), "installation reports intermediate progress");
    Check(progress.All(value => value >= 0 && value <= 1), "progress stays within range");
    Check(progress.Zip(progress.Skip(1)).All(pair => pair.First <= pair.Second), "progress is monotonic");
    Check(progress.Last() == 1, "completion reaches 100 percent");
    Check(statuses.Last() == "内置资源安装完成", "completion status reported");
    Check(File.ReadAllBytes(Path.Combine(root, "Data/example.Zl")).SequenceEqual(payload), "patch content");
    Check(File.Exists(Path.Combine(root, "Map/example.map")), "base ZIP content");
    Check(File.Exists(Path.Combine(root, "Version.bin")), "version state");
    var newer = new byte[] { 9, 8, 7 };
    File.WriteAllBytes(Path.Combine(root, "Data/example.Zl"), newer);
    Check(BundledResources.Install(Open, root, false, null), "restart");
    Check(File.ReadAllBytes(Path.Combine(root, "Data/example.Zl")).SequenceEqual(newer), "restart must preserve server update");
    assets["LocalUpdate/Data-example.Zl.gz"] = Gzip(new byte[] { 0 });
    Fails(() => BundledResources.Install(Open, root, true, null), "checksum mismatch must fail");
    Check(File.ReadAllBytes(Path.Combine(root, "Data/example.Zl")).SequenceEqual(newer), "failed patch must preserve old file");
    assets["LocalUpdate/Data-example.Zl.gz"] = gzipBytes;
    Check(BundledResources.Install(Open, root, true, null), "repair after failed patch");
    Check(File.ReadAllBytes(Path.Combine(root, "Data/example.Zl")).SequenceEqual(payload), "repaired bytes");
    File.Delete(Path.Combine(root, "Map/example.map")); Directory.Delete(Path.Combine(root, "Map"));
    Check(BundledResources.Install(Open, root, false, null), "missing base must reinstall");
    Check(File.Exists(Path.Combine(root, "Map/example.map")), "missing map recovered");
    var marker = File.ReadAllBytes(Path.Combine(root, ".bundled-resources.sha256"));
    assets["LocalUpdate/DataAdd.zip"] = new byte[] { 0 };
    Fails(() => BundledResources.Install(Open, root, true, null), "corrupt base must fail");
    Check(File.ReadAllBytes(Path.Combine(root, ".bundled-resources.sha256")).SequenceEqual(marker), "failed installation must not advance marker");
    var hostile = Zip("../outside.txt", payload);
    Fails(() => BundledResources.InstallZip(() => new NonSeekStream(hostile), root), "ZIP traversal must fail");
    Check(!File.Exists(Path.Combine(Path.GetDirectoryName(root)!, "outside.txt")), "no traversal write");
    Check(!BundledResources.Install(_ => throw new FileNotFoundException(), root, false, null), "online-only APK compatibility");
    Check(!Directory.EnumerateFiles(root, "*.tmp", SearchOption.AllDirectories).Any(), "temporary files cleaned");
    Check(!Directory.EnumerateFiles(root, ".resource-*.zip").Any(), "staging archives cleaned");
    Console.WriteLine($"PASS: {passed} bundled resource checks");
}
finally { if (Directory.Exists(root)) Directory.Delete(root, true); }

sealed class NonSeekStream : Stream
{
    readonly MemoryStream inner;
    public NonSeekStream(byte[] bytes) { inner = new MemoryStream(bytes); }
    public override bool CanRead => true;
    public override bool CanSeek => false;
    public override bool CanWrite => false;
    public override long Length => throw new NotSupportedException();
    public override long Position { get => throw new NotSupportedException(); set => throw new NotSupportedException(); }
    public override int Read(byte[] b, int o, int c) => inner.Read(b, o, c);
    public override void Flush() { }
    public override long Seek(long o, SeekOrigin s) => throw new NotSupportedException();
    public override void SetLength(long v) => throw new NotSupportedException();
    public override void Write(byte[] b, int o, int c) => throw new NotSupportedException();
    protected override void Dispose(bool disposing) { if (disposing) inner.Dispose(); base.Dispose(disposing); }
}
