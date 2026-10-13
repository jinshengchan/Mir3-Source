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
            if (plane.Length < 0 || plane.Width <= 0 || plane.Height <= 0)
                throw new InvalidDataException("Invalid map image plane.");
            int w = checked((plane.Width + 3) / 4 * 4);
            int h = checked((plane.Height + 3) / 4 * 4);
            int pixelLength = checked(w * h * 4);
            // Read only this plane from the existing payload. Streaming DEFLATE
            // into exact-sized buffers avoids a copy, a growing output buffer,
            // and ToArray for every image/shadow/overlay on a first visit.
            using var input = new MemoryStream(data, offset, plane.Length, false);
            offset += plane.Length;
            using var deflate = zircon ? null : new DeflateStream(input, CompressionMode.Decompress);
            Stream source = zircon ? input : deflate;
            byte[] pixels;
            if (plane.Type == 1 || plane.Type == 3 || plane.Type == 5)
            {
                // Keep small DXT block reads in memory instead of making many
                // tiny calls into DEFLATE. Encoded blocks need only 1/8 or 1/4
                // of the final RGBA plane, and are bounded by the dimensions.
                int blockBytes = plane.Type == 1 ? 8 : 16;
                byte[] blocks = new byte[checked(w / 4 * (h / 4) * blockBytes)];
                source.ReadExactly(blocks);
                pixels = plane.Type switch
                {
                    1 => DxtUtil.DecompressDxt1(blocks, w, h),
                    3 => DxtUtil.DecompressDxt3(blocks, w, h),
                    _ => DxtUtil.DecompressDxt5(blocks, w, h)
                };
            }
            else
            {
                pixels = new byte[pixelLength];
                source.ReadExactly(pixels);
            }
            // Reject oversized inflated data without first allocating all of it.
            if (source.ReadByte() != -1)
                throw new InvalidDataException("Decoded map data exceeds the texture dimensions.");
            return pixels;
        }
    }
}
