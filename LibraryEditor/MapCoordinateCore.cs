using System;
using System.Collections.Generic;
using System.Drawing;
using System.IO;

namespace LibraryEditor
{
    internal sealed class MapCellData
    {
        public short BackFile;
        public int BackImage;
        public short MiddleFile;
        public int MiddleImage;
        public short FrontFile;
        public int FrontImage;
        public byte MiddleAnimationFrame;
        public byte MiddleAnimationTick;
        public byte FrontAnimationFrame;
        public byte FrontAnimationTick;
        public bool Blocked;
    }

    internal sealed class MapFileData
    {
        public readonly int Width;
        public readonly int Height;
        public readonly MapCellData[] Cells;

        public MapFileData(int width, int height)
        {
            if (width <= 0 || height <= 0)
                throw new InvalidDataException("地图尺寸无效。");

            Width = width;
            Height = height;
            Cells = new MapCellData[checked(width * height)];
            for (int i = 0; i < Cells.Length; i++)
                Cells[i] = new MapCellData();
        }

        public MapCellData GetCell(int x, int y)
        {
            return Cells[x * Height + y];
        }
    }

    internal static class MapFileReader
    {
        public static MapFileData Read(string fileName)
        {
            byte[] bytes = File.ReadAllBytes(fileName);
            if (bytes.Length < 28)
                throw new InvalidDataException("地图文件过短。文件可能已损坏。");

            if (bytes[0] == 1 && bytes[1] == 0 && bytes[2] == 0x43 && bytes[3] == 0x23)
                return ReadCustom(bytes);

            if (bytes[0] == 0)
                return ReadKoreanMir3(bytes);

            throw new NotSupportedException("当前地图格式不在所选客户端实际使用的两种格式内。");
        }

        private static MapFileData ReadKoreanMir3(byte[] bytes)
        {
            int width = BitConverter.ToInt16(bytes, 22);
            int height = BitConverter.ToInt16(bytes, 24);
            MapFileData map = new MapFileData(width, height);
            int offset = 28;

            for (int x = 0; x < width / 2; x++)
            {
                for (int y = 0; y < height / 2; y++)
                {
                    EnsureAvailable(bytes, offset, 3);
                    short file = (short)(bytes[offset] == 255 ? -1 : bytes[offset] + 200);
                    int image = BitConverter.ToUInt16(bytes, offset + 1) + 1;
                    for (int i = 0; i < 4; i++)
                    {
                        int cellX = x * 2 + i % 2;
                        int cellY = y * 2 + i / 2;
                        if (cellX < width && cellY < height)
                        {
                            MapCellData cell = map.GetCell(cellX, cellY);
                            cell.BackFile = file;
                            cell.BackImage = image;
                        }
                    }
                    offset += 3;
                }
            }

            offset = 28 + 3 * ((width + 1) / 2) * (height / 2);
            for (int x = 0; x < width; x++)
            {
                for (int y = 0; y < height; y++)
                {
                    EnsureAvailable(bytes, offset, 14);
                    MapCellData cell = map.GetCell(x, y);
                    byte flag = bytes[offset];
                    cell.FrontFile = (short)(bytes[offset + 3] == 255 ? -1 : bytes[offset + 3] + 200);
                    cell.MiddleFile = (short)(bytes[offset + 4] == 255 ? -1 : bytes[offset + 4] + 200);
                    cell.MiddleAnimationFrame = bytes[offset + 1];
                    cell.FrontAnimationFrame = (byte)(bytes[offset + 2] == 255 ? 0 : bytes[offset + 2] & 0x8F);
                    cell.MiddleAnimationTick = 0;
                    cell.FrontAnimationTick = 0;
                    cell.MiddleImage = BitConverter.ToUInt16(bytes, offset + 5) + 1;
                    cell.FrontImage = BitConverter.ToUInt16(bytes, offset + 7) + 1;
                    cell.Blocked = (flag & 0x01) != 0x01 || (flag & 0x02) != 0x02;
                    offset += 14;
                }
            }

            return map;
        }

        private static MapFileData ReadCustom(byte[] bytes)
        {
            int width = BitConverter.ToInt16(bytes, 4);
            int height = BitConverter.ToInt16(bytes, 6);
            MapFileData map = new MapFileData(width, height);
            int offset = 8;

            for (int x = 0; x < width; x++)
            {
                for (int y = 0; y < height; y++)
                {
                    EnsureAvailable(bytes, offset, 26);
                    MapCellData cell = map.GetCell(x, y);
                    cell.BackFile = BitConverter.ToInt16(bytes, offset);
                    cell.BackImage = BitConverter.ToInt32(bytes, offset + 2);
                    cell.MiddleFile = BitConverter.ToInt16(bytes, offset + 6);
                    cell.MiddleImage = BitConverter.ToInt16(bytes, offset + 8);
                    cell.FrontFile = BitConverter.ToInt16(bytes, offset + 10);
                    cell.FrontImage = BitConverter.ToInt16(bytes, offset + 12);
                    cell.FrontAnimationFrame = bytes[offset + 16];
                    cell.FrontAnimationTick = bytes[offset + 17];
                    cell.MiddleAnimationFrame = bytes[offset + 18];
                    cell.MiddleAnimationTick = bytes[offset + 19];
                    cell.Blocked = (cell.BackImage & 0x20000000) != 0 || (cell.FrontImage & 0x8000) != 0;
                    offset += 26;
                }
            }

            return map;
        }

        private static void EnsureAvailable(byte[] bytes, int offset, int count)
        {
            if (offset < 0 || count < 0 || offset > bytes.Length - count)
                throw new InvalidDataException("地图数据长度与尺寸不匹配。文件可能已损坏。");
        }
    }

    internal static class MapCoordinateSelection
    {
        public static Point[] CreateSquare(Point center, int size, int mapWidth, int mapHeight)
        {
            if (size <= 0 || mapWidth <= 0 || mapHeight <= 0)
                return new Point[0];

            int before = (size - 1) / 2;
            int after = size / 2;
            List<Point> points = new List<Point>();
            for (int y = center.Y - before; y <= center.Y + after; y++)
            {
                for (int x = center.X - before; x <= center.X + after; x++)
                {
                    if (x >= 0 && y >= 0 && x < mapWidth && y < mapHeight)
                        points.Add(new Point(x, y));
                }
            }
            return points.ToArray();
        }
    }
}
