using Library;
using System;
using System.Collections.Generic;
using System.Drawing;
using System.Drawing.Drawing2D;
using System.IO;

namespace LibraryEditor
{
    internal sealed class MapCoordinateTileSource : IDisposable
    {
        private readonly string _clientRoot;
        private readonly Dictionary<string, BlackDragonLibrary> _libraries = new Dictionary<string, BlackDragonLibrary>(StringComparer.OrdinalIgnoreCase);
        private readonly Dictionary<string, Image> _images = new Dictionary<string, Image>(StringComparer.OrdinalIgnoreCase);
        private readonly HashSet<string> _missingLibraries = new HashSet<string>(StringComparer.OrdinalIgnoreCase);
        private readonly HashSet<string> _missingImages = new HashSet<string>(StringComparer.OrdinalIgnoreCase);
        private bool _disposed;

        public MapCoordinateTileSource(string dataDirectory)
        {
            string dataPath = Path.GetFullPath(dataDirectory ?? string.Empty);
            DirectoryInfo data = new DirectoryInfo(dataPath);
            _clientRoot = data.Parent == null ? data.FullName : data.Parent.FullName;
        }

        public bool HasRenderableLibraries { get { return _libraries.Count > 0; } }
        public int MissingLibraryCount { get { return _missingLibraries.Count; } }
        public int MissingImageCount { get { return _missingImages.Count; } }

        public Image Resolve(short file, int imageIndex)
        {
            if (_disposed || file < 0 || imageIndex < 0) return null;

            LibraryFile libraryFile;
            if (!Libraries.KROrder.TryGetValue(file, out libraryFile))
            {
                _missingLibraries.Add("#" + file);
                return null;
            }

            string relativePath;
            if (!Libraries.LibraryList.TryGetValue(libraryFile, out relativePath))
            {
                _missingLibraries.Add(libraryFile.ToString());
                return null;
            }

            string path = Path.GetFullPath(Path.Combine(_clientRoot, relativePath.Replace('/', Path.DirectorySeparatorChar)));
            BlackDragonLibrary library;
            if (!_libraries.TryGetValue(path, out library))
            {
                if (!File.Exists(path))
                {
                    _missingLibraries.Add(path);
                    return null;
                }

                try
                {
                    library = new BlackDragonLibrary(path);
                }
                catch
                {
                    _missingLibraries.Add(path);
                    return null;
                }

                if (library.Images == null || library.Images.Count == 0)
                {
                    library.Dispose();
                    _missingLibraries.Add(path);
                    return null;
                }
                _libraries[path] = library;
            }

            string cacheKey = path + "|" + imageIndex + "|Image";
            Image cached;
            if (_images.TryGetValue(cacheKey, out cached)) return cached;

            if (imageIndex >= library.Images.Count || library.Images[imageIndex] == null)
            {
                _missingImages.Add(cacheKey);
                return null;
            }

            BlackDragonLibrary.MImage image;
            try
            {
                image = library.CreateImage(imageIndex, ImageType.Image);
            }
            catch
            {
                _missingImages.Add(cacheKey);
                return null;
            }
            if (image == null || image.Image == null)
            {
                _missingImages.Add(cacheKey);
                return null;
            }

            _images[cacheKey] = image.Image;
            return image.Image;
        }

        public void Dispose()
        {
            if (_disposed) return;
            _disposed = true;
            ClearCache();
        }

        public void ClearCache()
        {
            if (_disposed && _libraries.Count == 0) return;
            foreach (BlackDragonLibrary library in _libraries.Values)
            {
                if (library.Images != null)
                {
                    foreach (BlackDragonLibrary.MImage image in library.Images)
                    {
                        if (image == null) continue;
                        DisposeImage(image.Image);
                        DisposeImage(image.Preview);
                        DisposeImage(image.ShadowImage);
                        DisposeImage(image.ShadowPreview);
                        DisposeImage(image.OverlayImage);
                        DisposeImage(image.OverlayPreview);
                        image.Dispose();
                    }
                }
                library.Dispose();
            }
            _images.Clear();
            _libraries.Clear();
            _missingLibraries.Clear();
            _missingImages.Clear();
        }

        private static void DisposeImage(Image image)
        {
            if (image != null) image.Dispose();
        }
    }

    internal sealed class MapCoordinateTileRenderer
    {
        private const int CellWidth = 48;
        private const int CellHeight = 32;

        public int RenderedTileCount { get; private set; }

        public void Draw(Graphics graphics, MapFileData map, Rectangle viewport, Point scrollOffset, float zoom, int animation, Func<short, int, Image> resolveImage)
        {
            RenderedTileCount = 0;
            if (graphics == null || map == null || resolveImage == null || zoom <= 0F) return;

            float cellWidth = CellWidth * zoom;
            float cellHeight = CellHeight * zoom;
            int firstX;
            int lastX;
            int firstY;
            int lastY;
            GetVisibleCells(map, viewport, scrollOffset, cellWidth, cellHeight, out firstX, out lastX, out firstY, out lastY);

            GraphicsState state = graphics.Save();
            graphics.InterpolationMode = InterpolationMode.NearestNeighbor;
            graphics.PixelOffsetMode = PixelOffsetMode.Half;
            graphics.CompositingMode = System.Drawing.Drawing2D.CompositingMode.SourceOver;
            graphics.SetClip(viewport);
            try
            {
                for (int y = firstY; y <= lastY; y++)
                {
                    if ((y & 1) != 0) continue;
                    for (int x = firstX; x <= lastX; x++)
                    {
                        if ((x & 1) != 0) continue;
                        MapCellData cell = map.GetCell(x, y);
                        Image image = cell.BackImage == -1 ? null : Resolve(resolveImage, cell.BackFile, (cell.BackImage & 0x1FFFF) - 1);
                        DrawImage(graphics, image, x * cellWidth - scrollOffset.X, y * cellHeight - scrollOffset.Y, zoom);
                    }
                }

                for (int y = firstY; y <= lastY; y++)
                    for (int x = firstX; x <= lastX; x++)
                    {
                        MapCellData cell = map.GetCell(x, y);
                        int index = cell.MiddleImage - 1;
                        Image image = Resolve(resolveImage, cell.MiddleFile, index);
                        if (IsStandardTile(image))
                            DrawImage(graphics, image, x * cellWidth - scrollOffset.X, y * cellHeight - scrollOffset.Y, zoom);
                    }

                for (int y = firstY; y <= lastY; y++)
                    for (int x = firstX; x <= lastX; x++)
                    {
                        MapCellData cell = map.GetCell(x, y);
                        int index = (cell.FrontImage & 0x7FFF) - 1;
                        if (cell.FrontAnimationFrame > 1 && cell.FrontAnimationFrame < 255) continue;
                        Image image = Resolve(resolveImage, cell.FrontFile, index);
                        if (IsStandardTile(image))
                            DrawImage(graphics, image, x * cellWidth - scrollOffset.X, y * cellHeight - scrollOffset.Y, zoom);
                    }

                int objectLastY = Math.Min(map.Height - 1, lastY + 20);
                for (int y = firstY; y <= objectLastY; y++)
                    for (int x = firstX; x <= lastX; x++)
                    {
                        MapCellData cell = map.GetCell(x, y);
                        int middleIndex = GetMiddleAnimationIndex(cell, animation);
                        Image middle = Resolve(resolveImage, cell.MiddleFile, middleIndex);
                        if (middle != null && !IsStandardTile(middle))
                            DrawImage(graphics, middle, x * cellWidth - scrollOffset.X,
                                (y + 1) * cellHeight - scrollOffset.Y - middle.Height * zoom, zoom);

                        int frontIndex = GetFrontAnimationIndex(cell, animation);
                        Image front = Resolve(resolveImage, cell.FrontFile, frontIndex);
                        if (front != null && !IsStandardTile(front))
                            DrawImage(graphics, front, x * cellWidth - scrollOffset.X,
                                (y + 1) * cellHeight - scrollOffset.Y - front.Height * zoom, zoom);
                    }
            }
            finally
            {
                graphics.Restore(state);
            }
        }

        public bool HasVisibleAnimatedCells(MapFileData map, Rectangle viewport, Point scrollOffset, float zoom)
        {
            if (map == null || zoom <= 0F) return false;
            float cellWidth = CellWidth * zoom;
            float cellHeight = CellHeight * zoom;
            int firstX;
            int lastX;
            int firstY;
            int lastY;
            GetVisibleCells(map, viewport, scrollOffset, cellWidth, cellHeight, out firstX, out lastX, out firstY, out lastY);
            int objectLastY = Math.Min(map.Height - 1, lastY + 20);
            for (int y = firstY; y <= objectLastY; y++)
                for (int x = firstX; x <= lastX; x++)
                {
                    MapCellData cell = map.GetCell(x, y);
                    if (IsAnimated(cell.MiddleAnimationFrame) || IsAnimated(cell.FrontAnimationFrame)) return true;
                }
            return false;
        }

        private static bool IsAnimated(byte animation)
        {
            return animation > 1 && animation < 255;
        }

        private static int GetMiddleAnimationIndex(MapCellData cell, int animation)
        {
            int index = cell.MiddleImage - 1;
            if (IsAnimated(cell.MiddleAnimationFrame))
            {
                int frames = cell.MiddleAnimationFrame & 0x0F;
                if (frames > 0) index += animation % frames;
            }
            return index;
        }

        private static int GetFrontAnimationIndex(MapCellData cell, int animation)
        {
            int index = (cell.FrontImage & 0x7FFF) - 1;
            if (IsAnimated(cell.FrontAnimationFrame))
            {
                int frames = cell.FrontAnimationFrame & 0x7F;
                int total = frames + frames * cell.FrontAnimationTick;
                if (total > 0) index += (animation % total) / (1 + cell.FrontAnimationTick);
            }
            return index;
        }

        private static bool IsStandardTile(Image image)
        {
            return image != null && ((image.Width == CellWidth && image.Height == CellHeight) ||
                (image.Width == CellWidth * 2 && image.Height == CellHeight * 2));
        }

        private Image Resolve(Func<short, int, Image> resolver, short file, int index)
        {
            if (file == -1 || index < 0) return null;
            return resolver(file, index);
        }

        private void DrawImage(Graphics graphics, Image image, float x, float y, float zoom)
        {
            if (image == null) return;
            RectangleF destination = new RectangleF(x, y, image.Width * zoom, image.Height * zoom);
            if (!destination.IntersectsWith(graphics.VisibleClipBounds)) return;
            graphics.DrawImage(image, destination, new RectangleF(0, 0, image.Width, image.Height), GraphicsUnit.Pixel);
            RenderedTileCount++;
        }

        private static void GetVisibleCells(MapFileData map, Rectangle viewport, Point scrollOffset, float cellWidth, float cellHeight,
            out int firstX, out int lastX, out int firstY, out int lastY)
        {
            firstX = Math.Max(0, (int)Math.Floor(scrollOffset.X / cellWidth) - 1);
            lastX = Math.Min(map.Width - 1, (int)Math.Ceiling((scrollOffset.X + viewport.Width) / cellWidth));
            firstY = Math.Max(0, (int)Math.Floor(scrollOffset.Y / cellHeight) - 1);
            lastY = Math.Min(map.Height - 1, (int)Math.Ceiling((scrollOffset.Y + viewport.Height) / cellHeight));
        }
    }
}
