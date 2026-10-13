namespace Client.Envir
{
    // Test the actual sprite bounds before reading, requesting or decoding pixels.
    // Keep a pixel of padding so filtering/rounding at screen edges is conservative.
    internal static class MapImageVisibility
    {
        public static bool IsNearViewport(float x, float y, int width, int height,
            int targetWidth, int targetHeight, int marginX, int marginY)
        {
            return !Intersects(x, y, width, height, 0, 0, 1, 0, targetWidth, targetHeight) &&
                Intersects(x + marginX, y + marginY, width, height, 0, 0, 1, 0,
                    targetWidth + marginX * 2, targetHeight + marginY * 2);
        }

        public static bool Intersects(float x, float y, int width, int height,
            int offsetX, int offsetY, float zoom, int uiOffsetX, int targetWidth, int targetHeight)
        {
            if (width <= 0 || height <= 0 || targetWidth <= 0 || targetHeight <= 0 ||
                zoom <= 0 || float.IsNaN(zoom) || float.IsInfinity(zoom)) return true;
            // MirImage uploads textures rounded to complete four-pixel blocks.
            width += (4 - width % 4) % 4;
            height += (4 - height % 4) % 4;
            float left = (x + offsetX) * zoom + (zoom == 1F ? 0 : uiOffsetX);
            float top = (y + offsetY) * zoom;
            return !(left > targetWidth + 1 || top > targetHeight + 1 ||
                left + width * zoom < -1 || top + height * zoom < -1);
        }
    }
}
