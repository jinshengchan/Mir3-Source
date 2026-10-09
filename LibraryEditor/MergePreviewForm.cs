using System;
using System.Collections.Generic;
using System.Drawing;
using System.Drawing.Drawing2D;
using System.Drawing.Imaging;
using System.Windows.Forms;

namespace LibraryEditor
{
    internal sealed class MergePreviewFrame : IDisposable
    {
        public int ImageIndex;
        public int OffsetX;
        public int OffsetY;
        public Bitmap Bitmap;

        public void Dispose()
        {
            if (Bitmap != null)
                Bitmap.Dispose();
            Bitmap = null;
        }
    }

    internal sealed class MergePreviewLayer : IDisposable
    {
        public string Key;
        public string Category;
        public string LibraryName;
        public int AdditionalOffsetX;
        public int AdditionalOffsetY;
        public readonly List<MergePreviewFrame> Frames = new List<MergePreviewFrame>();

        public override string ToString()
        {
            int imageIndex = Frames.Count == 0 ? -1 : Frames[0].ImageIndex;
            return string.Format("{0} | {1} | Image {2} | {3}帧 | 偏移({4},{5})",
                Category, LibraryName, imageIndex, Frames.Count, AdditionalOffsetX, AdditionalOffsetY);
        }

        public void Dispose()
        {
            foreach (MergePreviewFrame frame in Frames)
                frame.Dispose();
            Frames.Clear();
        }
    }

    internal sealed partial class MergePreviewForm : Form
    {
        private const int PreviewPadding = 24;
        private readonly List<MergePreviewLayer> _layers = new List<MergePreviewLayer>();
        private Bitmap _compositeBitmap;
        private int _framePosition;
        private bool _bindingOffsets;

        public MergePreviewForm()
        {
            InitializeComponent();
        }

        internal void AddOrReplaceLayer(MergePreviewLayer layer)
        {
            if (layer == null || layer.Frames.Count == 0)
                return;

            int existingIndex = _layers.FindIndex(item =>
                string.Equals(item.Key, layer.Key, StringComparison.OrdinalIgnoreCase));
            if (existingIndex >= 0)
            {
                _layers[existingIndex].Dispose();
                _layers[existingIndex] = layer;
            }
            else
            {
                int order = GetDefaultOrder(layer.Category);
                int insertIndex = _layers.FindIndex(item => GetDefaultOrder(item.Category) > order);
                if (insertIndex < 0)
                    _layers.Add(layer);
                else
                    _layers.Insert(insertIndex, layer);
                existingIndex = insertIndex < 0 ? _layers.Count - 1 : insertIndex;
            }

            RefreshLayerList(existingIndex);
            _framePosition = 0;
            RebuildComposite();
        }

        private void removeButton_Click(object sender, EventArgs e)
        {
            int index = layerListBox.SelectedIndex;
            if (index < 0 || index >= _layers.Count)
                return;

            _layers[index].Dispose();
            _layers.RemoveAt(index);
            _framePosition = 0;
            RefreshLayerList(Math.Min(index, _layers.Count - 1));
            RebuildComposite();
        }

        private void clearButton_Click(object sender, EventArgs e)
        {
            ClearLayers();
            _framePosition = 0;
            RefreshLayerList(-1);
            RebuildComposite();
        }

        private void moveBackButton_Click(object sender, EventArgs e)
        {
            int index = layerListBox.SelectedIndex;
            if (index <= 0 || index >= _layers.Count)
                return;

            MergePreviewLayer layer = _layers[index];
            _layers.RemoveAt(index);
            _layers.Insert(index - 1, layer);
            RefreshLayerList(index - 1);
            RebuildComposite();
        }

        private void moveFrontButton_Click(object sender, EventArgs e)
        {
            int index = layerListBox.SelectedIndex;
            if (index < 0 || index >= _layers.Count - 1)
                return;

            MergePreviewLayer layer = _layers[index];
            _layers.RemoveAt(index);
            _layers.Insert(index + 1, layer);
            RefreshLayerList(index + 1);
            RebuildComposite();
        }

        private void MergePreviewForm_FormClosed(object sender, FormClosedEventArgs e)
        {
            animationTimer.Stop();
            ClearLayers();
            DisposeComposite();
        }

        private void previousFrameButton_Click(object sender, EventArgs e)
        {
            MoveFrame(-1);
        }

        private void playButton_Click(object sender, EventArgs e)
        {
            if (animationTimer.Enabled)
                animationTimer.Stop();
            else if (GetFrameCount() > 1)
                animationTimer.Start();
            playButton.Text = animationTimer.Enabled ? "暂停" : "播放";
        }

        private void nextFrameButton_Click(object sender, EventArgs e)
        {
            MoveFrame(1);
        }

        private void animationTimer_Tick(object sender, EventArgs e)
        {
            MoveFrame(1);
        }

        private void speedNumericUpDown_ValueChanged(object sender, EventArgs e)
        {
            animationTimer.Interval = Math.Max(25, (int)speedNumericUpDown.Value);
        }

        private void previewHostPanel_Resize(object sender, EventArgs e)
        {
            CenterPreview();
        }

        private void layerListBox_SelectedIndexChanged(object sender, EventArgs e)
        {
            _bindingOffsets = true;
            try
            {
                MergePreviewLayer layer = GetSelectedLayer();
                offsetXNumericUpDown.Value = layer == null ? 0 : layer.AdditionalOffsetX;
                offsetYNumericUpDown.Value = layer == null ? 0 : layer.AdditionalOffsetY;
                offsetXNumericUpDown.Enabled = layer != null;
                offsetYNumericUpDown.Enabled = layer != null;
                resetOffsetButton.Enabled = layer != null;
            }
            finally
            {
                _bindingOffsets = false;
            }
        }

        private void offsetNumericUpDown_ValueChanged(object sender, EventArgs e)
        {
            if (_bindingOffsets)
                return;

            MergePreviewLayer layer = GetSelectedLayer();
            if (layer == null)
                return;

            layer.AdditionalOffsetX = (int)offsetXNumericUpDown.Value;
            layer.AdditionalOffsetY = (int)offsetYNumericUpDown.Value;
            int selectedIndex = layerListBox.SelectedIndex;
            RefreshLayerList(selectedIndex);
            RebuildComposite();
        }

        private void resetOffsetButton_Click(object sender, EventArgs e)
        {
            MergePreviewLayer layer = GetSelectedLayer();
            if (layer == null)
                return;

            layer.AdditionalOffsetX = 0;
            layer.AdditionalOffsetY = 0;
            int selectedIndex = layerListBox.SelectedIndex;
            RefreshLayerList(selectedIndex);
            RebuildComposite();
        }

        private void RefreshLayerList(int selectedIndex)
        {
            layerListBox.BeginUpdate();
            try
            {
                layerListBox.Items.Clear();
                foreach (MergePreviewLayer layer in _layers)
                    layerListBox.Items.Add(layer);
                if (selectedIndex >= 0 && selectedIndex < layerListBox.Items.Count)
                    layerListBox.SelectedIndex = selectedIndex;
            }
            finally
            {
                layerListBox.EndUpdate();
            }

            layerCountLabel.Text = string.Format("图层（从后到前）：{0}", _layers.Count);
            layerListBox_SelectedIndexChanged(this, EventArgs.Empty);
        }

        private void RebuildComposite()
        {
            DisposeComposite();
            if (_layers.Count == 0)
            {
                previewPictureBox.Image = null;
                previewInfoLabel.Text = "请在外观查询窗口选择帧，然后点击“合并预览”。";
                return;
            }

            int minX = int.MaxValue;
            int minY = int.MaxValue;
            int maxX = int.MinValue;
            int maxY = int.MinValue;
            foreach (MergePreviewLayer layer in _layers)
            {
                MergePreviewFrame frame = GetLayerFrame(layer);
                int offsetX = frame.OffsetX + layer.AdditionalOffsetX;
                int offsetY = frame.OffsetY + layer.AdditionalOffsetY;
                minX = Math.Min(minX, offsetX);
                minY = Math.Min(minY, offsetY);
                maxX = Math.Max(maxX, offsetX + frame.Bitmap.Width);
                maxY = Math.Max(maxY, offsetY + frame.Bitmap.Height);
            }

            int width = Math.Max(1, maxX - minX + PreviewPadding * 2);
            int height = Math.Max(1, maxY - minY + PreviewPadding * 2);
            _compositeBitmap = new Bitmap(width, height, PixelFormat.Format32bppArgb);
            using (Graphics graphics = Graphics.FromImage(_compositeBitmap))
            {
                graphics.Clear(Color.Transparent);
                graphics.CompositingMode = CompositingMode.SourceOver;
                graphics.CompositingQuality = CompositingQuality.HighSpeed;
                graphics.InterpolationMode = InterpolationMode.NearestNeighbor;
                graphics.PixelOffsetMode = PixelOffsetMode.Half;
                foreach (MergePreviewLayer layer in _layers)
                {
                    MergePreviewFrame frame = GetLayerFrame(layer);
                    int x = frame.OffsetX + layer.AdditionalOffsetX - minX + PreviewPadding;
                    int y = frame.OffsetY + layer.AdditionalOffsetY - minY + PreviewPadding;
                    graphics.DrawImageUnscaled(frame.Bitmap, x, y);
                }
            }

            previewPictureBox.Image = _compositeBitmap;
            previewPictureBox.Size = _compositeBitmap.Size;
            previewInfoLabel.Text = string.Format("合并尺寸：{0}×{1}  |  坐标范围：({2}, {3}) - ({4}, {5})",
                width, height, minX, minY, maxX, maxY);
            int frameCount = GetFrameCount();
            framePositionLabel.Text = frameCount == 0
                ? "帧：-"
                : string.Format("帧 {0}/{1}", _framePosition + 1, frameCount);
            CenterPreview();
        }

        private void MoveFrame(int delta)
        {
            int frameCount = GetFrameCount();
            if (frameCount <= 1)
                return;

            _framePosition += delta;
            if (_framePosition < 0)
                _framePosition = frameCount - 1;
            else if (_framePosition >= frameCount)
                _framePosition = 0;
            RebuildComposite();
        }

        private int GetFrameCount()
        {
            int count = 0;
            foreach (MergePreviewLayer layer in _layers)
                count = Math.Max(count, layer.Frames.Count);
            return count;
        }

        private MergePreviewFrame GetLayerFrame(MergePreviewLayer layer)
        {
            return layer.Frames[_framePosition % layer.Frames.Count];
        }

        private MergePreviewLayer GetSelectedLayer()
        {
            int index = layerListBox.SelectedIndex;
            return index >= 0 && index < _layers.Count ? _layers[index] : null;
        }

        private void CenterPreview()
        {
            if (_compositeBitmap == null)
                return;

            int x = Math.Max(0, (previewHostPanel.ClientSize.Width - previewPictureBox.Width) / 2);
            int y = Math.Max(0, (previewHostPanel.ClientSize.Height - previewPictureBox.Height) / 2);
            previewPictureBox.Location = new Point(x, y);
        }

        private void ClearLayers()
        {
            foreach (MergePreviewLayer layer in _layers)
                layer.Dispose();
            _layers.Clear();
        }

        private void DisposeComposite()
        {
            previewPictureBox.Image = null;
            if (_compositeBitmap != null)
                _compositeBitmap.Dispose();
            _compositeBitmap = null;
        }

        private static int GetDefaultOrder(string category)
        {
            switch (category)
            {
                case "翅膀特效":
                case "方向特效":
                case "怪物魔法":
                case "魔法特效":
                    return 10;
                case "盔甲":
                case "时装":
                    return 20;
                case "头发":
                case "头盔":
                    return 30;
                case "武器":
                case "盾牌":
                case "物品特效":
                    return 40;
                case "称号":
                    return 50;
                default:
                    return 35;
            }
        }
    }
}
