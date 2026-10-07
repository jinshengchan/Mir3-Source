using System;
using System.IO;
using System.Text;

namespace Mir3.Mobile
{
    public static class LibraryHeaderValidator
    {
        public static void Validate(byte[] header, long totalLength)
        {
            if (header == null || header.Length < 4 || header.Length > 16 * 1024 * 1024 ||
                totalLength < header.Length || totalLength > uint.MaxValue)
                throw new InvalidDataException("Invalid resource header size.");
            using var input = new BinaryReader(new MemoryStream(header));
            bool zircon = header.Length < 20 || Encoding.ASCII.GetString(header, 0, 19) != "BlackDragon Version";
            int version = 0;
            byte[] records;
            if (zircon)
                records = ReadExact(input, input.ReadInt32());
            else
            {
                input.BaseStream.Position = 19;
                byte flags = input.ReadByte();
                version = flags & 127;
                if (version < 1 || version > 3) throw new InvalidDataException("Unsupported resource version.");
                int length = input.ReadInt32();
                records = ReadExact(input, length);
                if ((flags & 128) != 0 && version > 1)
                {
                    byte[] key = Decode(ReadExact(input, 8), Encoding.ASCII.GetBytes("BlackDragon Version"), 8);
                    records = Decode(records, key, (byte)(length % 255));
                }
            }
            using var reader = new BinaryReader(new MemoryStream(records));
            int count = reader.ReadInt32();
            if (count < 1 || count > 1000000) throw new InvalidDataException("Invalid resource image count.");
            for (int i = 0; i < count; i++)
            {
                if (reader.ReadByte() == 0) continue;
                int position = reader.ReadInt32();
                long bytes;
                if (zircon)
                {
                    int width = reader.ReadInt16(), height = reader.ReadInt16();
                    reader.ReadInt16(); reader.ReadInt16(); reader.ReadByte();
                    int sw = reader.ReadInt16(), sh = reader.ReadInt16();
                    reader.ReadInt16(); reader.ReadInt16();
                    int ow = reader.ReadInt16(), oh = reader.ReadInt16();
                    bytes = DxtBytes(width, height) + DxtBytes(sw, sh) + DxtBytes(ow, oh);
                }
                else
                {
                    bytes = Positive(reader.ReadInt32());
                    for (int j = 0; j < 6; j++) reader.ReadInt16();
                    reader.ReadByte();
                    byte shadow = reader.ReadByte(), overlay = reader.ReadByte();
                    if (shadow != 0) { bytes += Positive(reader.ReadInt32()); reader.ReadInt16(); reader.ReadInt16(); }
                    if (overlay != 0) { bytes += Positive(reader.ReadInt32()); if (version > 1) { reader.ReadInt16(); reader.ReadInt16(); } }
                }
                if (bytes < 0 || position < 0 || (position != 0 &&
                    (position < header.Length || position + bytes > totalLength)))
                    throw new InvalidDataException("Resource image lies outside its file.");
            }
            long trailing = header.Length - input.BaseStream.Position;
            if (reader.BaseStream.Position != records.Length ||
                (trailing != 0 && !(!zircon && version > 1 && trailing == 8)))
                throw new InvalidDataException("Unexpected trailing resource header data.");
        }

        private static long Positive(int value) => value >= 0 ? value : throw new InvalidDataException("Negative image size.");
        private static long DxtBytes(int width, int height) => width >= 0 && height >= 0
            ? ((long)(width + 3) / 4 * 4) * ((long)(height + 3) / 4 * 4) / 2
            : throw new InvalidDataException("Negative image dimensions.");
        private static byte[] ReadExact(BinaryReader reader, int size)
        {
            if (size < 0 || size > reader.BaseStream.Length - reader.BaseStream.Position)
                throw new InvalidDataException("Truncated resource header.");
            return reader.ReadBytes(size);
        }
        private static byte[] Decode(byte[] data, byte[] key, byte salt)
        {
            byte mask = 0;
            foreach (byte value in key) mask ^= value;
            var result = new byte[data.Length];
            for (int i = 0; i < data.Length; i++) result[i] = (byte)(data[i] ^ mask ^ (i == 0 ? salt : data[i - 1]));
            return result;
        }
    }
}
