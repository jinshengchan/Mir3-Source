using System;

namespace Mir3.UnityPrototype
{
    // The Korean Mir3 format (version 5 in Mir3.Mobile/MapControl.cs).
    // Pure C#: this class can also be used by an offline resource conversion tool.
    public sealed class Mir3KoreanMap
    {
        private const int HeaderLength = 28;
        private const int CellLength = 14;
        private readonly byte[] data;
        private readonly int floorRows;
        private readonly int cellStart;

        public int Width { get; private set; }
        public int Height { get; private set; }

        public Mir3KoreanMap(byte[] bytes)
        {
            if (bytes == null) throw new ArgumentNullException(nameof(bytes));
            if (bytes.Length < HeaderLength || bytes[0] != 0)
                throw new NotSupportedException("Expected a Korean Mir3 (type 5) map.");

            // The game reads these as signed 16-bit little-endian integers.
            Width = ReadInt16(bytes, 22);
            Height = ReadInt16(bytes, 24);
            if (Width <= 0 || Height <= 0 || Height % 2 != 0 || Width > 8192 || Height > 8192)
                throw new FormatException("Invalid map dimensions.");

            floorRows = Height / 2;
            long floorBytes = 3L * ((Width + 1) / 2) * floorRows;
            long end = HeaderLength + floorBytes + (long)Width * Height * CellLength;
            if (floorRows == 0 || end > bytes.Length || end > int.MaxValue)
                throw new FormatException("Map data is truncated or too large.");

            cellStart = (int)(HeaderLength + floorBytes);
            data = bytes;
        }

        public Cell GetCell(int x, int y)
        {
            if (x < 0 || x >= Width || y < 0 || y >= Height)
                throw new ArgumentOutOfRangeException("Map cell coordinates are outside the map.");

            // The original map stores one floor record for each 2x2 cell block.
            int floorOffset = HeaderLength + ((x / 2) * floorRows + y / 2) * 3;
            int offset = cellStart + (x * Height + y) * CellLength;
            byte flags = data[offset];
            int backFile = data[floorOffset] == 255 ? -1 : data[floorOffset] + 200;
            int middleFile = data[offset + 4] == 255 ? -1 : data[offset + 4] + 200;
            int frontFile = data[offset + 3] == 255 ? -1 : data[offset + 3] + 200;

            return new Cell(
                backFile, ReadUInt16(data, floorOffset + 1),
                middleFile, ReadUInt16(data, offset + 5),
                frontFile, ReadUInt16(data, offset + 7),
                (flags & 3) != 3);
        }

        private static short ReadInt16(byte[] bytes, int offset)
        {
            return unchecked((short)ReadUInt16(bytes, offset));
        }

        private static ushort ReadUInt16(byte[] bytes, int offset)
        {
            return (ushort)(bytes[offset] | bytes[offset + 1] << 8);
        }

        public struct Cell
        {
            public readonly int BackFile, BackIndex;
            public readonly int MiddleFile, MiddleIndex;
            public readonly int FrontFile, FrontIndex;
            public readonly bool Blocked;

            public Cell(int backFile, int backIndex, int middleFile, int middleIndex,
                int frontFile, int frontIndex, bool blocked)
            {
                BackFile = backFile;
                BackIndex = backIndex;
                MiddleFile = middleFile;
                MiddleIndex = middleIndex;
                FrontFile = frontFile;
                FrontIndex = frontIndex;
                Blocked = blocked;
            }
        }
    }
}
