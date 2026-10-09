using System;
using System.Drawing;
using System.Windows.Forms;

namespace LibraryEditor
{
    public sealed class PreviewCanvas : Panel
    {
        private Bitmap _image;
        private string _emptyText = "未加载";

        public bool DrawInventoryGrid { get; set; }
        public bool DrawAtTopLeft { get; set; }
        public bool HasImage { get { return _image != null; } }
        public int ImageWidth { get { return _image == null ? 0 : _image.Width; } }
        public int ImageHeight { get { return _image == null ? 0 : _image.Height; } }

        public PreviewCanvas()
        {
            BackColor = Color.Black;
            BorderStyle = BorderStyle.FixedSingle;
            SetStyle(ControlStyles.UserPaint | ControlStyles.AllPaintingInWmPaint |
                ControlStyles.OptimizedDoubleBuffer | ControlStyles.ResizeRedraw, true);
        }

        public void SetImage(Bitmap image, string emptyText)
        {
            _image = image;
            _emptyText = string.IsNullOrEmpty(emptyText) ? "未加载" : emptyText;
            Invalidate();
        }

        protected override void OnPaint(PaintEventArgs e)
        {
            base.OnPaint(e);
            e.Graphics.Clear(Color.Black);

            if (DrawInventoryGrid)
            {
                using (Pen gridPen = new Pen(Color.FromArgb(58, 58, 58)))
                {
                    for (int column = 1; column < 6; column++)
                    {
                        int x = ClientSize.Width * column / 6;
                        e.Graphics.DrawLine(gridPen, x, 0, x, ClientSize.Height);
                    }
                    for (int row = 1; row < 10; row++)
                    {
                        int y = ClientSize.Height * row / 10;
                        e.Graphics.DrawLine(gridPen, 0, y, ClientSize.Width, y);
                    }
                }
            }

            if (_image == null)
            {
                using (Brush textBrush = new SolidBrush(Color.DarkGray))
                using (StringFormat format = new StringFormat
                {
                    Alignment = StringAlignment.Center,
                    LineAlignment = StringAlignment.Center,
                })
                {
                    e.Graphics.DrawString(_emptyText, Font, textBrush, ClientRectangle, format);
                }
                return;
            }

            int targetWidth = _image.Width;
            int targetHeight = _image.Height;
            if (!DrawAtTopLeft &&
                (targetWidth > ClientSize.Width || targetHeight > ClientSize.Height))
            {
                double scale = Math.Min(
                    (double)ClientSize.Width / Math.Max(1, targetWidth),
                    (double)ClientSize.Height / Math.Max(1, targetHeight));
                targetWidth = Math.Max(1, (int)Math.Round(targetWidth * scale));
                targetHeight = Math.Max(1, (int)Math.Round(targetHeight * scale));
            }

            int left = DrawAtTopLeft ? 0 : (ClientSize.Width - targetWidth) / 2;
            int top = DrawAtTopLeft ? 0 : (ClientSize.Height - targetHeight) / 2;
            e.Graphics.InterpolationMode = System.Drawing.Drawing2D.InterpolationMode.NearestNeighbor;
            e.Graphics.PixelOffsetMode = System.Drawing.Drawing2D.PixelOffsetMode.Half;
            e.Graphics.DrawImage(
                _image,
                new Rectangle(left, top, targetWidth, targetHeight),
                0,
                0,
                _image.Width,
                _image.Height,
                GraphicsUnit.Pixel);
        }
    }
}
