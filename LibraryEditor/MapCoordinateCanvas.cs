using System;
using System.Collections.Generic;
using System.Drawing;
using System.Drawing.Drawing2D;
using System.Linq;
using System.Windows.Forms;

namespace LibraryEditor
{
    internal sealed class MapCoordinateCanvas : Control
    {
        private const int CellWidth = 48;
        private const int CellHeight = 32;

        private MapFileData _map;
        private Image _mapImage;
        private MapCoordinateTileRenderer _tileRenderer;
        private MapCoordinateTileSource _tileSource;
        private bool _realRenderAvailable;
        private Point _selectionStart;
        private Point _selectionEnd;
        private bool _selecting;
        private float _zoom = 1F;
        private int _animation;

        public readonly HashSet<Point> Selection = new HashSet<Point>();
        public readonly List<Tuple<Point, Color, string>> Markers = new List<Tuple<Point, Color, string>>();
        public Size SourceImageSize { get { return _mapImage == null ? Size.Empty : _mapImage.Size; } }
        public Size VirtualExtent
        {
            get
            {
                if (_map == null) return Size.Empty;
                return new Size(ScaledExtent(_map.Width * (double)CellWidth * _zoom), ScaledExtent(_map.Height * (double)CellHeight * _zoom));
            }
        }
        public float Zoom { get { return _zoom; } }
        public bool LastFrameUsedFallback { get; private set; }
        public Point ScrollOffset
        {
            get
            {
                Panel host = Parent as Panel;
                if (host == null) return Point.Empty;
                Point position = host.AutoScrollPosition;
                return new Point(Math.Max(0, -position.X), Math.Max(0, -position.Y));
            }
        }
        public bool ShowBlockedCells { get; set; }
        public event EventHandler CoordinateChanged;
        public event EventHandler SelectionChanged;
        public Point CurrentCoordinate { get; private set; }

        public MapCoordinateCanvas()
        {
            DoubleBuffered = true;
            BackColor = Color.Black;
            Cursor = Cursors.Cross;
            MinimumSize = new Size(1, 1);
            Dock = DockStyle.Fill;
        }

        public void SetMap(MapFileData map, Image mapImage)
        {
            SetMap(map, mapImage, null, null, false);
        }

        public void SetMap(MapFileData map, Image mapImage, MapCoordinateTileRenderer tileRenderer, MapCoordinateTileSource tileSource, bool realRenderAvailable)
        {
            _map = map;
            _mapImage = mapImage;
            _tileRenderer = tileRenderer;
            _tileSource = tileSource;
            _realRenderAvailable = realRenderAvailable;
            _zoom = 1F;
            _animation = 0;
            LastFrameUsedFallback = false;
            Selection.Clear();
            Markers.Clear();
            CurrentCoordinate = Point.Empty;
            UpdateVirtualExtent();
            Invalidate();
        }

        public void SetZoom(float zoom)
        {
            if (zoom <= 0F) return;
            _zoom = zoom;
            UpdateVirtualExtent();
            Invalidate();
        }

        public void SetAnimation(int animation)
        {
            _animation = Math.Max(0, animation);
            Invalidate();
        }

        public bool HasVisibleAnimatedCells
        {
            get
            {
                return _map != null && (_mapImage == null || _zoom >= 0.05F) && _tileRenderer != null &&
                    _tileRenderer.HasVisibleAnimatedCells(_map, ClientRectangle, ScrollOffset, _zoom);
            }
        }

        public void SetSelection(IEnumerable<Point> points)
        {
            Selection.Clear();
            if (points != null)
                foreach (Point point in points)
                    if (_map != null && point.X >= 0 && point.Y >= 0 && point.X < _map.Width && point.Y < _map.Height)
                        Selection.Add(point);
            Invalidate();
        }

        public void ClearSelection()
        {
            Selection.Clear();
            Invalidate();
            SelectionChanged?.Invoke(this, EventArgs.Empty);
        }

        protected override void OnParentChanged(EventArgs e)
        {
            base.OnParentChanged(e);
            UpdateVirtualExtent();
        }

        protected override void OnLocationChanged(EventArgs e)
        {
            base.OnLocationChanged(e);
            if (Parent is Panel && Location != Point.Empty)
                Location = Point.Empty;
        }

        protected override void OnMouseDown(MouseEventArgs e)
        {
            base.OnMouseDown(e);
            if (e.Button != MouseButtons.Left || _map == null) return;
            _selectionStart = ToMapPoint(e.Location);
            _selectionEnd = _selectionStart;
            _selecting = true;
            Capture = true;
            Invalidate();
        }

        protected override void OnMouseMove(MouseEventArgs e)
        {
            base.OnMouseMove(e);
            if (_map == null) return;
            CurrentCoordinate = ToMapPoint(e.Location);
            CoordinateChanged?.Invoke(this, EventArgs.Empty);
            if (!_selecting) return;
            _selectionEnd = CurrentCoordinate;
            Invalidate();
        }

        protected override void OnMouseUp(MouseEventArgs e)
        {
            base.OnMouseUp(e);
            if (!_selecting || _map == null) return;
            _selecting = false;
            Capture = false;
            _selectionEnd = ToMapPoint(e.Location);
            Selection.Clear();
            int left = Math.Min(_selectionStart.X, _selectionEnd.X);
            int right = Math.Max(_selectionStart.X, _selectionEnd.X);
            int top = Math.Min(_selectionStart.Y, _selectionEnd.Y);
            int bottom = Math.Max(_selectionStart.Y, _selectionEnd.Y);
            for (int y = top; y <= bottom; y++)
                for (int x = left; x <= right; x++)
                    if (x >= 0 && y >= 0 && x < _map.Width && y < _map.Height)
                        Selection.Add(new Point(x, y));
            Invalidate();
            SelectionChanged?.Invoke(this, EventArgs.Empty);
        }

        protected override void OnPaint(PaintEventArgs e)
        {
            base.OnPaint(e);
            if (_map == null) return;

            Point scroll = ScrollOffset;
            e.Graphics.Clear(Color.Black);
            bool drewRealMap = false;
            bool overview = _mapImage != null && _zoom < 0.05F;
            if (_realRenderAvailable && _tileRenderer != null && _tileSource != null && !overview)
            {
                _tileRenderer.Draw(e.Graphics, _map, ClientRectangle, scroll, _zoom, _animation, _tileSource.Resolve);
                drewRealMap = _tileRenderer.RenderedTileCount > 0;
            }
            if (!drewRealMap)
                DrawFallbackMap(e.Graphics, scroll);
            LastFrameUsedFallback = !drewRealMap && !overview;

            if (ShowBlockedCells)
                DrawBlockedCells(e.Graphics, scroll);
            DrawMarkers(e.Graphics, scroll);
            DrawSelection(e.Graphics, scroll);
            DrawGrid(e.Graphics, scroll);
        }

        private void DrawFallbackMap(Graphics graphics, Point scroll)
        {
            if (_mapImage == null) return;
            Size extent = VirtualExtent;
            if (extent.Width <= 0 || extent.Height <= 0) return;
            Rectangle visible = Rectangle.Intersect(ClientRectangle,
                new Rectangle(-scroll.X, -scroll.Y, extent.Width, extent.Height));
            if (visible.IsEmpty) return;
            GraphicsState state = graphics.Save();
            try
            {
                RectangleF source = new RectangleF(
                    (visible.X + scroll.X) * _mapImage.Width / (float)extent.Width,
                    (visible.Y + scroll.Y) * _mapImage.Height / (float)extent.Height,
                    visible.Width * _mapImage.Width / (float)extent.Width,
                    visible.Height * _mapImage.Height / (float)extent.Height);
                graphics.InterpolationMode = source.Width < 1F || source.Height < 1F
                    ? InterpolationMode.NearestNeighbor : InterpolationMode.HighQualityBicubic;
                graphics.PixelOffsetMode = PixelOffsetMode.HighQuality;
                graphics.DrawImage(_mapImage, visible, source, GraphicsUnit.Pixel);
            }
            finally
            {
                graphics.Restore(state);
            }
        }

        private void DrawBlockedCells(Graphics graphics, Point scroll)
        {
            float cellWidth = CellWidth * _zoom;
            float cellHeight = CellHeight * _zoom;
            int firstX;
            int lastX;
            int firstY;
            int lastY;
            GetVisibleCells(scroll, cellWidth, cellHeight, out firstX, out lastX, out firstY, out lastY);
            using (SolidBrush brush = new SolidBrush(Color.FromArgb(90, 230, 45, 45)))
            {
                for (int x = firstX; x <= lastX; x++)
                    for (int y = firstY; y <= lastY; y++)
                        if (_map.GetCell(x, y).Blocked)
                            graphics.FillRectangle(brush, x * cellWidth - scroll.X, y * cellHeight - scroll.Y,
                                Math.Max(1F, cellWidth), Math.Max(1F, cellHeight));
            }
        }

        private void DrawMarkers(Graphics graphics, Point scroll)
        {
            float cellWidth = CellWidth * _zoom;
            float cellHeight = CellHeight * _zoom;
            foreach (Tuple<Point, Color, string> marker in Markers)
            {
                if (!IsInside(marker.Item1)) continue;
                float x = (marker.Item1.X + 0.5F) * cellWidth - scroll.X;
                float y = (marker.Item1.Y + 0.5F) * cellHeight - scroll.Y;
                using (SolidBrush brush = new SolidBrush(marker.Item2))
                    graphics.FillEllipse(brush, x - 4, y - 4, 8, 8);
                if (cellWidth >= 5F && !string.IsNullOrEmpty(marker.Item3))
                    using (SolidBrush text = new SolidBrush(Color.White))
                        graphics.DrawString(marker.Item3, Font, text, x + 5, y - Font.Height / 2F);
            }
        }

        private void DrawSelection(Graphics graphics, Point scroll)
        {
            float cellWidth = CellWidth * _zoom;
            float cellHeight = CellHeight * _zoom;
            IEnumerable<Point> points = Selection;
            if (_selecting)
            {
                int left = Math.Min(_selectionStart.X, _selectionEnd.X);
                int right = Math.Max(_selectionStart.X, _selectionEnd.X);
                int top = Math.Min(_selectionStart.Y, _selectionEnd.Y);
                int bottom = Math.Max(_selectionStart.Y, _selectionEnd.Y);
                points = from y in Enumerable.Range(top, bottom - top + 1)
                         from x in Enumerable.Range(left, right - left + 1)
                         select new Point(x, y);
            }
            using (SolidBrush brush = new SolidBrush(Color.FromArgb(135, 0, 180, 255)))
            using (Pen border = new Pen(Color.Cyan, 1F))
            {
                foreach (Point point in points)
                {
                    if (!IsInside(point)) continue;
                    RectangleF cell = new RectangleF(point.X * cellWidth - scroll.X, point.Y * cellHeight - scroll.Y,
                        Math.Max(1F, cellWidth), Math.Max(1F, cellHeight));
                    if (!cell.IntersectsWith(graphics.VisibleClipBounds)) continue;
                    graphics.FillRectangle(brush, cell);
                    if (cellWidth >= 4F && cellHeight >= 4F)
                        graphics.DrawRectangle(border, cell.X, cell.Y, cell.Width, cell.Height);
                }
            }
        }

        private void DrawGrid(Graphics graphics, Point scroll)
        {
            float cellWidth = CellWidth * _zoom;
            float cellHeight = CellHeight * _zoom;
            if (cellWidth < 8F || cellHeight < 8F) return;
            Rectangle clip = ClientRectangle;
            int firstX;
            int lastX;
            int firstY;
            int lastY;
            GetVisibleCells(scroll, cellWidth, cellHeight, out firstX, out lastX, out firstY, out lastY);
            using (Pen pen = new Pen(Color.FromArgb(60, Color.White)))
            {
                for (int x = firstX; x <= lastX + 1; x++)
                    graphics.DrawLine(pen, x * cellWidth - scroll.X, clip.Top, x * cellWidth - scroll.X, clip.Bottom);
                for (int y = firstY; y <= lastY + 1; y++)
                    graphics.DrawLine(pen, clip.Left, y * cellHeight - scroll.Y, clip.Right, y * cellHeight - scroll.Y);
            }
        }

        private Point ToMapPoint(Point location)
        {
            if (_map == null) return Point.Empty;
            Point scroll = ScrollOffset;
            int x = Math.Min(_map.Width - 1, Math.Max(0, (int)Math.Floor((location.X + scroll.X) / (CellWidth * _zoom))));
            int y = Math.Min(_map.Height - 1, Math.Max(0, (int)Math.Floor((location.Y + scroll.Y) / (CellHeight * _zoom))));
            return new Point(x, y);
        }

        private void GetVisibleCells(Point scroll, float cellWidth, float cellHeight,
            out int firstX, out int lastX, out int firstY, out int lastY)
        {
            firstX = Math.Max(0, (int)Math.Floor(scroll.X / cellWidth));
            lastX = Math.Min(_map.Width - 1, (int)Math.Ceiling((scroll.X + ClientSize.Width) / cellWidth));
            firstY = Math.Max(0, (int)Math.Floor(scroll.Y / cellHeight));
            lastY = Math.Min(_map.Height - 1, (int)Math.Ceiling((scroll.Y + ClientSize.Height) / cellHeight));
        }

        private bool IsInside(Point point)
        {
            return _map != null && point.X >= 0 && point.Y >= 0 && point.X < _map.Width && point.Y < _map.Height;
        }

        private void UpdateVirtualExtent()
        {
            Panel host = Parent as Panel;
            if (host == null) return;
            host.AutoScrollMinSize = VirtualExtent;
            if (host.ClientSize.Width > 0 && host.ClientSize.Height > 0)
            {
                Dock = DockStyle.None;
                Location = Point.Empty;
                Size = host.ClientSize;
            }
        }

        private static int ScaledExtent(double value)
        {
            if (value <= 1D) return 1;
            return value >= int.MaxValue ? int.MaxValue : Math.Max(1, (int)Math.Ceiling(value));
        }
    }
}
