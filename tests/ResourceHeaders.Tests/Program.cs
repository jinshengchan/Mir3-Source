using Mir3.Mobile;
using System.Text;
using System.IO.Compression;

int passed = 0;
byte[] Header(int version, bool reserved, int position, int size)
{
    using var records = new MemoryStream();
    using (var w = new BinaryWriter(records, Encoding.UTF8, true))
    {
        w.Write(1); w.Write((byte)1); w.Write(position); w.Write(size);
        for (int i = 0; i < 6; i++) w.Write((short)4);
        w.Write((byte)0); w.Write((byte)0); w.Write((byte)0);
    }
    using var output = new MemoryStream();
    using var writer = new BinaryWriter(output);
    writer.Write(Encoding.ASCII.GetBytes("BlackDragon Version"));
    writer.Write((byte)version); writer.Write((int)records.Length); writer.Write(records.ToArray());
    if (reserved) writer.Write(new byte[8]);
    return output.ToArray();
}
void Reject(byte[] header, long total)
{
    try { LibraryHeaderValidator.Validate(header, total); }
    catch (Exception ex) when (ex is IOException || ex is InvalidDataException) { passed++; return; }
    throw new Exception("Invalid header was accepted.");
}
LibraryHeaderValidator.Validate(Header(3, false, 52, 8), 60); passed++;
LibraryHeaderValidator.Validate(Header(3, true, 60, 8), 68); passed++;
LibraryHeaderValidator.Validate(Header(1, false, 52, 8), 60); passed++;
Reject(Header(4, false, 52, 8), 60);
Reject(Header(3, false, 10, 8), 60);
Reject(Header(3, false, 52, 9), 60);
Reject(Header(3, false, 52, -1), 60);
Reject(Header(3, false, 52, 8)[..^1], 60);
Reject(Header(3, false, 52, 8).Concat(new byte[1]).ToArray(), 60);
Reject(new byte[3], 60);
Reject(Header(3, false, 52, 8), uint.MaxValue + 1L);

if (args.Length == 1)
{
    // Validate actual encrypted bundled metadata independently of the fixtures.
    using var archive = ZipFile.OpenRead(Path.Combine(args[0], "LocalUpdate", "DataAdd.zip"));
    foreach (var name in new[] { "Data/Map Data/Tilesc.Zl", "Data/Map Data/SmTilesc.Zl", "Data/Map Data/Tiles5c.Zl", "Data/Map Data/Wood/Tilesc.Zl" })
    {
        var entry = archive.GetEntry(name)!;
        using var input = new BinaryReader(entry.Open());
        byte[] prefix = input.ReadBytes(24);
        int length = BitConverter.ToInt32(prefix, 20);
        byte[] header = prefix.Concat(input.ReadBytes(length + 8)).ToArray();
        LibraryHeaderValidator.Validate(header, entry.Length); passed++;
    }
    using var stream = new GZipStream(File.OpenRead(Path.Combine(args[0], "LocalUpdate", "Data-M-Shield1.Zl.gz")), CompressionMode.Decompress);
    using var memory = new MemoryStream(); stream.CopyTo(memory);
    byte[] data = memory.ToArray();
    int shieldLength = BitConverter.ToInt32(data, 20) + 32;
    LibraryHeaderValidator.Validate(data[..shieldLength], data.Length); passed++;
}
passed += await RecoveryChecks.Run();
Console.WriteLine($"PASS: {passed} resource header integrity and recovery checks");
