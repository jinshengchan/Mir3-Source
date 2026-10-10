using Client.Envir;
using System.IO.Compression;
using System.Text;

internal static class ActualMapImages
{
    public static int Run(string bundle)
    {
        using var archive = ZipFile.OpenRead(Path.Combine(bundle, "LocalUpdate", "DataAdd.zip"));
        int checkedImages = 0;
        foreach (string name in new[] { "Data/Map Data/Tilesc.Zl", "Data/Map Data/SmTilesc.Zl", "Data/Map Data/Tiles5c.Zl", "Data/Map Data/Wood/Tilesc.Zl" })
        {
            var entry = archive.GetEntry(name) ?? throw new Exception("Missing test library " + name);
            using var stream = entry.Open();
            using var memory = new MemoryStream();
            stream.CopyTo(memory);
            byte[] file = memory.ToArray();
            byte version = (byte)(file[19] & 127);
            int length = BitConverter.ToInt32(file, 20);
            byte[] records = file.AsSpan(24, length).ToArray();
            if ((file[19] & 128) != 0 && version > 1)
                records = Decode(records, Decode(file.AsSpan(24 + length, 8).ToArray(), Encoding.ASCII.GetBytes("BlackDragon Version"), 8), (byte)(length % 255));
            using var reader = new BinaryReader(new MemoryStream(records));
            int count = reader.ReadInt32(), tested = 0;
            for (int index = 0; index < count && tested < 10; index++)
            {
                byte type = reader.ReadByte();
                if (type == 0) continue;
                int position = reader.ReadInt32(), imageLength = reader.ReadInt32();
                short width = reader.ReadInt16(), height = reader.ReadInt16();
                reader.ReadBytes(8); // Image and shadow offsets.
                reader.ReadByte(); // Shadow drawing mode.
                byte shadowType = reader.ReadByte(), overlayType = reader.ReadByte();
                var image = new MapImagePixels.Plane(imageLength, width, height, type);
                var shadow = shadowType == 0 ? default : new MapImagePixels.Plane(reader.ReadInt32(), reader.ReadInt16(), reader.ReadInt16(), shadowType);
                var overlay = overlayType == 0 ? default : new MapImagePixels.Plane(reader.ReadInt32(), version > 1 ? reader.ReadInt16() : width, version > 1 ? reader.ReadInt16() : height, overlayType);
                if (position == 0 || (width == 1 && height == 1) || imageLength == 0 || file[position] == 0) continue;
                int total = checked(image.Length + shadow.Length + overlay.Length);
                var pixels = MapImagePixels.Decode(file.AsSpan(position, total).ToArray(), false, image, shadow, overlay);
                if (pixels.Image == null || (shadow.Length > 0 && pixels.Shadow == null) || (overlay.Length > 0 && pixels.Overlay == null))
                    throw new Exception("Incomplete decoded planes: " + name + "/" + index);
                tested++; checkedImages++;
            }
            if (tested != 10) throw new Exception("Need ten populated images from " + name);
            Console.WriteLine($"PASS {tested} actual old-bundle images from {name}");
        }
        return checkedImages;
    }

    private static byte[] Decode(byte[] bytes, byte[] key, byte salt)
    {
        byte mask = 0;
        foreach (byte value in key) mask ^= value;
        return bytes.Select((value, i) => (byte)(value ^ mask ^ (i == 0 ? salt : bytes[i - 1]))).ToArray();
    }
}
