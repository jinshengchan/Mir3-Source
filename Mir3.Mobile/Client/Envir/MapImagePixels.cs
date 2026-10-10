using Client.Extentions;
using System;
using System.IO;
using System.IO.Compression;

namespace Client.Envir
{
    // CPU-only decoding: this class must never create or access GPU textures.
    internal sealed class MapImagePixels
    {
        internal readonly struct Plane
        {
            public readonly int Length, Width, Height;
            public readonly byte Type;
            public Plane(int length, int width, int height, byte type)
            {
                Length = length; Width = width; Height = height; Type = type;
            }
        }

        public byte[] Image, Shadow, Overlay;

        public static MapImagePixels Decode(byte[] data, bool zircon, Plane image, Plane shadow, Plane overlay)
        {
            if (data.Length != checked(image.Length + shadow.Length + overlay.Length))
                throw new InvalidDataException("Map image payload length differs from its header.");

            int offset = 0;
            return new MapImagePixels
            {
                Image = DecodePlane(data, ref offset, image, zircon),
                Shadow = DecodePlane(data, ref offset, shadow, zircon),
                Overlay = DecodePlane(data, ref offset, overlay, zircon)
            };
        }

        private static byte[] DecodePlane(byte[] data, ref int offset, Plane plane, bool zircon)
        {
            if (plane.Length == 0) return null;
            byte[] compressed = new byte[plane.Length];
            Buffer.BlockCopy(data, offset, compressed, 0, plane.Length);
            offset += plane.Length;
            int w = plane.Width + (4 - plane.Width % 4) % 4;
            int h = plane.Height + (4 - plane.Height % 4) % 4;
            if (w <= 0 || h <= 0) throw new InvalidDataException("Invalid map image dimensions.");
            if (!zircon)
            {
                using (var input = new MemoryStream(compressed))
                using (var deflate = new DeflateStream(input, CompressionMode.Decompress))
                using (var output = new MemoryStream())
                {
                    deflate.CopyTo(output);
                    compressed = output.ToArray();
                }
            }

            byte[] pixels;
            switch (plane.Type)
            {
                case 1: pixels = DxtUtil.DecompressDxt1(compressed, w, h); break;
                case 3: pixels = DxtUtil.DecompressDxt3(compressed, w, h); break;
                case 5: pixels = DxtUtil.DecompressDxt5(compressed, w, h); break;
                default: pixels = compressed; break;
            }
            if (pixels.Length != checked(w * h * 4))
                throw new InvalidDataException("Decoded map pixels differ from the texture dimensions.");
            return pixels;
        }
    }
}
