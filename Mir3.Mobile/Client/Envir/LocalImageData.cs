using System;
using System.IO;

namespace Client.Envir
{
    internal static class LocalImageData
    {
        // Sparse library slots use a zero first byte, just as the original
        // loader did. Probe that byte without allocating the whole slot.
        public static bool Probe(BinaryReader reader, int position, int imageLength, out byte prefix)
        {
            reader.BaseStream.Seek(position, SeekOrigin.Begin);
            int value = imageLength > 0 ? reader.BaseStream.ReadByte() : -1;
            prefix = value > 0 ? (byte)value : (byte)0;
            return value > 0;
        }

        // Probe has already consumed the first byte. Read all requested planes
        // into one buffer, leaving the reader immediately after their payload.
        public static byte[] Read(BinaryReader reader, byte prefix, int length)
        {
            if (length <= 0) throw new InvalidDataException("Invalid local image length.");
            byte[] bytes = new byte[length];
            bytes[0] = prefix;
            reader.BaseStream.ReadExactly(bytes, 1, length - 1);
            return bytes;
        }
    }
}
