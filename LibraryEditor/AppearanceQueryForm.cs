using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Drawing;
using System.Drawing.Drawing2D;
using System.IO;
using System.Windows.Forms;

namespace LibraryEditor
{
    /// <summary>
    /// Read-only preview for the appearance libraries used by the client.
    /// </summary>
    public sealed partial class AppearanceQueryForm : Form
    {
        private const int ShapeBlockSize = 5000;
        private const int ShapeSlotCount = 10;
        private const int DirectionCount = 8;
        private const int DirectionStride = 10;
        private const int DirectionFrameCapacity = 10;
        private const int MergeFrameLimit = 60;
        private const int InitialThumbnailLimit = 96;
        private const string PlaceholderImageKey = "__placeholder__";

        private static readonly string[] DirectionNames =
        {
            "向上", "右上", "向右", "右下", "向下", "左下", "向左", "左上"
        };

        private static readonly string[] CategoryNames =
        {
            "翅膀特效", "盾牌", "方向特效", "怪物魔法", "盔甲", "魔法特效", "其他",
            "时装", "头发", "头盔", "称号", "武器", "物品特效", "坐骑", "UI特效"
        };

        private readonly string _initialDataPath;
        private readonly List<AppearanceGroup> _groups = new List<AppearanceGroup>();
        private readonly List<LibraryEntry> _libraries = new List<LibraryEntry>();
        private AppearanceGroup _selectedGroup;
        private BlackDragonLibrary _library;
        private string _libraryPath;
        private string _dataPath = string.Empty;
        private bool _binding;
        private bool _playing;
        private MergePreviewForm _mergePreviewForm;

        private sealed class LibraryEntry
        {
            public string Category;
            public string Path;
            public string Name;
            public bool UseWeaponShape;
            public int WeaponNumber;

            public override string ToString()
            {
                return Name;
            }
        }

        private sealed class AppearanceGroup
        {
            public string LibraryPath;
            public string LibraryName;
            public string Category;
            public int LibraryNumber;
            public int ShapeGroup;
            public int ShapeSlot;
            public int Shape;
            public int BaseIndex;
            public int EndIndex;
            public string ImageKey;
            public Bitmap Thumbnail;
            public bool ThumbnailAttempted;
            public readonly List<DirectionFrames> Directions = new List<DirectionFrames>();

            public override string ToString()
            {
                return string.Format("Shape {0} ({1})", Shape, LibraryName);
            }
        }

        private sealed class DirectionFrames
        {
            public int Direction;
            public readonly List<int> Indices = new List<int>();

            public override string ToString()
            {
                string name;
                if (Direction == -1)
                    return string.Format("全部帧 ({0}帧)", Indices.Count);

                name = Direction >= 0 && Direction < DirectionNames.Length
                    ? DirectionNames[Direction]
                    : "已发现帧";
                int rangeStart = Direction * DirectionStride;
                return string.Format("{0} ({1}-{2})", name, rangeStart,
                    rangeStart + DirectionFrameCapacity - 1);
            }
        }

        public AppearanceQueryForm()
            : this(null)
        {
        }

        public AppearanceQueryForm(string dataPath)
        {
            _initialDataPath = dataPath;
            InitializeComponent();

            if (LicenseManager.UsageMode == LicenseUsageMode.Designtime)
                return;

            Shown += AppearanceQueryForm_Shown;
            FormClosing += AppearanceQueryForm_FormClosing;
        }

        private void AppearanceQueryForm_Shown(object sender, EventArgs e)
        {
            if (!string.IsNullOrEmpty(_dataPath))
                return;

            string path = ResolveDataPath(_initialDataPath);
            if (string.IsNullOrEmpty(path))
            {
                SetStatus("未找到客户端 Data 目录，请点击“扫描”选择。", true);
                return;
            }

            ScanData(path);
        }

        private void AppearanceQueryForm_FormClosing(object sender, FormClosingEventArgs e)
        {
            _playing = false;
            playbackTimer.Stop();
            if (_mergePreviewForm != null && !_mergePreviewForm.IsDisposed)
                _mergePreviewForm.Close();
            DisposeCurrentLibrary();
            ClearGroupThumbnails();
        }

        private void scanButton_Click(object sender, EventArgs e)
        {
            using (FolderBrowserDialog dialog = new FolderBrowserDialog())
            {
                dialog.Description = "选择客户端 Data 目录";
                if (Directory.Exists(_dataPath))
                    dialog.SelectedPath = _dataPath;

                if (dialog.ShowDialog(this) == DialogResult.OK)
                    ScanData(dialog.SelectedPath);
            }
        }

        private void exportButton_Click(object sender, EventArgs e)
        {
            MessageBox.Show(this, "尚未选择可导出的目标文件。外观查询仅用于预览，不会修改客户端素材。",
                "导出预览", MessageBoxButtons.OK, MessageBoxIcon.Information);
        }

        private void mergeButton_Click(object sender, EventArgs e)
        {
            DirectionFrames direction = directionComboBox.SelectedItem as DirectionFrames;
            if (_selectedGroup == null || direction == null || direction.Indices.Count == 0 || _library == null)
            {
                MessageBox.Show(this, "请先选择需要加入合并预览的素材帧。",
                    "合并预览", MessageBoxButtons.OK, MessageBoxIcon.Information);
                return;
            }

            int frameIndex = Math.Min(frameTrackBar.Value, direction.Indices.Count - 1);
            int imageIndex = direction.Indices[frameIndex];
            BlackDragonLibrary.MImage image;
            try
            {
                image = _library.GetImage(imageIndex);
            }
            catch (Exception ex)
            {
                SetStatus("加入合并预览失败：" + ex.Message, true);
                return;
            }

            if (image == null || image.Image == null)
            {
                SetStatus("当前帧为空，无法加入合并预览。", true);
                return;
            }

            if (_mergePreviewForm == null || _mergePreviewForm.IsDisposed)
            {
                _mergePreviewForm = new MergePreviewForm();
                _mergePreviewForm.FormClosed += delegate { _mergePreviewForm = null; };
                _mergePreviewForm.Show(this);
            }

            MergePreviewLayer layer = CreateMergePreviewLayer(direction, imageIndex);
            if (layer == null || layer.Frames.Count == 0)
            {
                if (layer != null)
                    layer.Dispose();
                SetStatus("当前帧序列无法解码，未加入合并预览。", true);
                return;
            }

            _mergePreviewForm.AddOrReplaceLayer(layer);
            _mergePreviewForm.BringToFront();
            SetStatus(string.Format("已将 {0} / Image {1} 加入合并预览（{2}帧）。",
                _selectedGroup.LibraryName, imageIndex, layer.Frames.Count), false);
        }

        private MergePreviewLayer CreateMergePreviewLayer(DirectionFrames selectedDirection, int selectedImageIndex)
        {
            DirectionFrames frames = selectedDirection;
            if (selectedDirection.Direction == -1 && _selectedGroup.Shape >= 0)
            {
                frames = null;
                foreach (DirectionFrames candidate in _selectedGroup.Directions)
                {
                    if (candidate.Direction >= 0 && candidate.Indices.Contains(selectedImageIndex))
                    {
                        frames = candidate;
                        break;
                    }
                }
            }

            List<int> indices = frames == null ? selectedDirection.Indices : frames.Indices;
            if (indices.Count == 0)
                return null;

            int selectedPosition = indices.IndexOf(selectedImageIndex);
            if (selectedPosition < 0)
                selectedPosition = Math.Min(frameTrackBar.Value, indices.Count - 1);

            MergePreviewLayer layer = new MergePreviewLayer
            {
                Key = _selectedGroup.LibraryPath,
                Category = _selectedGroup.Category,
                LibraryName = _selectedGroup.LibraryName
            };

            int count = Math.Min(indices.Count, MergeFrameLimit);
            for (int offset = 0; offset < count; offset++)
            {
                int imageIndex = indices[(selectedPosition + offset) % indices.Count];
                try
                {
                    BlackDragonLibrary.MImage image = _library.GetImage(imageIndex);
                    if (image == null || image.Image == null)
                        continue;

                    layer.Frames.Add(new MergePreviewFrame
                    {
                        ImageIndex = imageIndex,
                        OffsetX = image.OffSetX,
                        OffsetY = image.OffSetY,
                        Bitmap = new Bitmap(image.Image)
                    });
                }
                catch
                {
                }
            }
            return layer;
        }

        private void clearCacheButton_Click(object sender, EventArgs e)
        {
            _playing = false;
            UpdatePlayButton();
            DisposeCurrentLibrary();

            if (_selectedGroup != null)
            {
                LoadSelectedLibrary();
                BindSelectedGroup();
            }

            SetStatus("已清理解码缓存，扫描结果和缩略图保留。", false);
        }

        private void playbackTimer_Tick(object sender, EventArgs e)
        {
            if (!_playing || _selectedGroup == null || directionComboBox.SelectedItem == null)
                return;

            MoveFrame(1);
        }

        private void previousButton_Click(object sender, EventArgs e)
        {
            MoveFrame(-1);
        }

        private void playButton_Click(object sender, EventArgs e)
        {
            if (_selectedGroup == null || directionComboBox.SelectedItem == null)
                return;

            _playing = !_playing;
            if (_playing)
                playbackTimer.Start();
            else
                playbackTimer.Stop();
            UpdatePlayButton();
        }

        private void nextButton_Click(object sender, EventArgs e)
        {
            MoveFrame(1);
        }

        private void directionComboBox_SelectedIndexChanged(object sender, EventArgs e)
        {
            if (_binding)
                return;

            BindFrameControls();
        }

        private void frameTrackBar_ValueChanged(object sender, EventArgs e)
        {
            if (_binding)
                return;

            ShowSelectedFrame();
        }

        private void speedNumericUpDown_ValueChanged(object sender, EventArgs e)
        {
            playbackTimer.Interval = Math.Max(25, (int)speedNumericUpDown.Value);
        }

        private void appearanceTreeView_AfterSelect(object sender, TreeViewEventArgs e)
        {
            LibraryEntry entry = e.Node.Tag as LibraryEntry;
            if (entry != null)
            {
                LoadLibraryEntry(entry);
                return;
            }

            AppearanceGroup group = e.Node.Tag as AppearanceGroup;
            if (group != null)
                SelectGroup(group);
        }

        private void shapeListView_ItemSelectionChanged(object sender, ListViewItemSelectionChangedEventArgs e)
        {
            if (_binding || !e.IsSelected)
                return;

            AppearanceGroup group = e.Item.Tag as AppearanceGroup;
            if (group != null)
                SelectGroup(group);
        }

        private void ScanData(string path)
        {
            path = ResolveDataPath(path);
            if (string.IsNullOrEmpty(path))
            {
                ClearScanResult();
                SetStatus("目录无效，未找到客户端 Data 目录。", true);
                return;
            }

            _playing = false;
            playbackTimer.Stop();
            UpdatePlayButton();
            DisposeCurrentLibrary();
            ClearScanResult();
            _dataPath = path;
            dataPathToolStripLabel.Text = "Data: " + _dataPath;
            scanButton.Enabled = false;
            SetStatus("正在扫描素材库目录...", false);

            try
            {
                string[] files = Directory.GetFiles(_dataPath, "*.Zl", SearchOption.TopDirectoryOnly);
                Array.Sort(files, StringComparer.OrdinalIgnoreCase);

                foreach (string file in files)
                {
                    LibraryEntry entry = CreateLibraryEntry(file);
                    if (entry != null)
                        _libraries.Add(entry);
                }

                PopulateTree();

                if (_libraries.Count == 0)
                {
                    SetStatus("扫描完成，但 Data 中没有找到 .Zl 素材库。", true);
                    return;
                }

                SetStatus(string.Format("扫描完成：{0} 个素材库。请选择左侧素材库加载预览。",
                    _libraries.Count), false);
                SelectFirstLibrary("武器");
            }
            catch (Exception ex)
            {
                SetStatus("扫描失败：" + ex.Message, true);
            }
            finally
            {
                scanButton.Enabled = true;
            }
        }

        private void BuildWeaponGroups(LibraryEntry entry)
        {
            if (_library == null || _library.Images == null)
                return;

            for (int slot = 0; slot < ShapeSlotCount; slot++)
            {
                int baseIndex = slot * ShapeBlockSize;
                if (baseIndex >= _library.Images.Count)
                    break;

                AppearanceGroup group = new AppearanceGroup
                {
                    LibraryPath = entry.Path,
                    LibraryName = entry.Name,
                    Category = entry.Category,
                    LibraryNumber = entry.WeaponNumber,
                    ShapeGroup = GetShapeGroup(entry.WeaponNumber),
                    ShapeSlot = slot,
                    Shape = GetShapeGroup(entry.WeaponNumber) * 10 + slot,
                    BaseIndex = baseIndex,
                    EndIndex = Math.Min(_library.Images.Count - 1, baseIndex + ShapeBlockSize - 1),
                    ImageKey = entry.Name + "-" + slot
                };

                DiscoverDirectionFrames(_library, group);
                AddGroupWithThumbnail(group);
            }
        }

        private void BuildGenericGroups(LibraryEntry entry)
        {
            if (_library == null || _library.Images == null)
                return;

            int index = 0;
            int groupNumber = 0;
            while (index < _library.Images.Count)
            {
                while (index < _library.Images.Count && _library.Images[index] == null)
                    index++;
                if (index >= _library.Images.Count)
                    break;

                int start = index;
                DirectionFrames frames = new DirectionFrames { Direction = -1 };
                while (index < _library.Images.Count && _library.Images[index] != null)
                {
                    frames.Indices.Add(index);
                    index++;
                }

                AppearanceGroup group = new AppearanceGroup
                {
                    LibraryPath = entry.Path,
                    LibraryName = entry.Name,
                    Category = entry.Category,
                    LibraryNumber = 0,
                    ShapeGroup = -1,
                    ShapeSlot = groupNumber,
                    Shape = -1,
                    BaseIndex = start,
                    EndIndex = index - 1,
                    ImageKey = entry.Name + "-range-" + groupNumber
                };
                group.Directions.Add(frames);
                AddGroupWithThumbnail(group);
                groupNumber++;
            }
        }

        private void AddGroupWithThumbnail(AppearanceGroup group)
        {
            if (group.Directions.Count == 0 || group.Directions[0].Indices.Count == 0)
                return;

            if (_groups.Count < InitialThumbnailLimit)
            {
                group.ThumbnailAttempted = true;
                group.Thumbnail = CreateThumbnail(_library, group.Directions[0].Indices[0]);
            }
            _groups.Add(group);
        }

        private static void DiscoverDirectionFrames(BlackDragonLibrary library, AppearanceGroup group)
        {
            int blockEnd = Math.Min(library.Images.Count, group.BaseIndex + ShapeBlockSize);
            DirectionFrames allFrames = new DirectionFrames { Direction = -1 };
            for (int index = group.BaseIndex; index < blockEnd; index++)
            {
                if (library.Images[index] != null)
                    allFrames.Indices.Add(index);
            }

            if (allFrames.Indices.Count == 0)
                return;

            group.Directions.Add(allFrames);

            for (int direction = 0; direction < DirectionCount; direction++)
            {
                DirectionFrames frames = new DirectionFrames { Direction = direction };
                int directionStart = group.BaseIndex + direction * DirectionStride;
                int directionEnd = Math.Min(blockEnd, directionStart + DirectionFrameCapacity);
                for (int index = directionStart; index < directionEnd; index++)
                {
                    if (library.Images[index] != null)
                        frames.Indices.Add(index);
                }

                if (frames.Indices.Count > 0)
                    group.Directions.Add(frames);
            }
        }

        private static Bitmap CreateThumbnail(BlackDragonLibrary library, int index)
        {
            try
            {
                BlackDragonLibrary.MImage image = library.GetImage(index);
                if (image == null || image.Image == null)
                    return null;

                Bitmap thumbnail = new Bitmap(96, 96);
                using (Graphics graphics = Graphics.FromImage(thumbnail))
                {
                    graphics.Clear(Color.FromArgb(42, 42, 42));
                    graphics.InterpolationMode = InterpolationMode.NearestNeighbor;
                    graphics.PixelOffsetMode = PixelOffsetMode.Half;
                    int width = image.Width;
                    int height = image.Height;
                    double scale = Math.Min(82.0 / Math.Max(1, width), 82.0 / Math.Max(1, height));
                    int targetWidth = Math.Max(1, (int)Math.Round(width * scale));
                    int targetHeight = Math.Max(1, (int)Math.Round(height * scale));
                    int left = (thumbnail.Width - targetWidth) / 2;
                    int top = (thumbnail.Height - targetHeight) / 2;
                    graphics.DrawImage(image.Image,
                        new Rectangle(left, top, targetWidth, targetHeight),
                        new Rectangle(0, 0, width, height), GraphicsUnit.Pixel);
                }
                return thumbnail;
            }
            catch
            {
                return null;
            }
        }

        private void PopulateGallery()
        {
            _binding = true;
            try
            {
                shapeListView.Items.Clear();
                thumbnailImageList.Images.Clear();
                thumbnailImageList.Images.Add(PlaceholderImageKey, CreatePlaceholderThumbnail());
                foreach (AppearanceGroup group in _groups)
                {
                    if (group.Thumbnail != null)
                        thumbnailImageList.Images.Add(group.ImageKey, group.Thumbnail);
                    string caption = group.Shape >= 0
                        ? string.Format("Shape {0}", group.Shape)
                        : group.BaseIndex == group.EndIndex
                            ? string.Format("Image {0}", group.BaseIndex)
                            : string.Format("Image {0}-{1}", group.BaseIndex, group.EndIndex);
                    ListViewItem item = new ListViewItem(caption)
                    {
                        ImageKey = group.Thumbnail == null ? PlaceholderImageKey : group.ImageKey,
                        Tag = group
                    };
                    shapeListView.Items.Add(item);
                }

                if (shapeListView.Items.Count > 0)
                    shapeListView.Items[0].Selected = true;
            }
            finally
            {
                _binding = false;
            }

            if (_groups.Count > 0)
                SelectGroup(_groups[0]);
        }

        private void PopulateTree()
        {
            _binding = true;
            try
            {
                appearanceTreeView.Nodes.Clear();

                foreach (string categoryName in CategoryNames)
                {
                    TreeNode categoryNode = new TreeNode(categoryName);
                    appearanceTreeView.Nodes.Add(categoryNode);

                    foreach (LibraryEntry entry in _libraries)
                    {
                        if (!string.Equals(entry.Category, categoryName, StringComparison.Ordinal))
                            continue;

                        TreeNode libraryNode = new TreeNode(entry.Name) { Tag = entry };
                        categoryNode.Nodes.Add(libraryNode);
                    }

                    if (categoryNode.Nodes.Count == 0)
                    {
                        TreeNode emptyNode = new TreeNode("(未发现素材库)");
                        emptyNode.ForeColor = Color.Gray;
                        categoryNode.Nodes.Add(emptyNode);
                    }
                }
            }
            finally
            {
                _binding = false;
            }
        }

        private void SelectGroup(AppearanceGroup group)
        {
            if (group == null)
                return;

            _selectedGroup = group;
            groupInfoLabel.Text = group.Shape >= 0
                ? string.Format("{0} | Shape={1} | 起始序号={2}",
                    group.LibraryName, group.Shape, group.BaseIndex)
                : group.BaseIndex == group.EndIndex
                    ? string.Format("{0} | Image={1}", group.LibraryName, group.BaseIndex)
                    : string.Format("{0} | Image={1}-{2}", group.LibraryName,
                        group.BaseIndex, group.EndIndex);
            EnsureGroupThumbnail(group);
            SelectGalleryItem(group);
            LoadSelectedLibrary();
            BindSelectedGroup();
        }

        private void EnsureGroupThumbnail(AppearanceGroup group)
        {
            if (group == null || group.ThumbnailAttempted || _library == null ||
                group.Directions.Count == 0 || group.Directions[0].Indices.Count == 0)
                return;

            group.ThumbnailAttempted = true;
            group.Thumbnail = CreateThumbnail(_library, group.Directions[0].Indices[0]);
            if (group.Thumbnail == null)
                return;

            if (!thumbnailImageList.Images.ContainsKey(group.ImageKey))
                thumbnailImageList.Images.Add(group.ImageKey, group.Thumbnail);

            foreach (ListViewItem item in shapeListView.Items)
            {
                if (item.Tag == group)
                {
                    item.ImageKey = group.ImageKey;
                    break;
                }
            }
        }

        private void SelectFirstLibrary(string category)
        {
            foreach (TreeNode categoryNode in appearanceTreeView.Nodes)
            {
                if (!string.Equals(categoryNode.Text, category, StringComparison.Ordinal))
                    continue;

                foreach (TreeNode libraryNode in categoryNode.Nodes)
                {
                    if (!(libraryNode.Tag is LibraryEntry))
                        continue;

                    categoryNode.Expand();
                    appearanceTreeView.SelectedNode = libraryNode;
                    libraryNode.EnsureVisible();
                    return;
                }
            }
        }

        private void LoadLibraryEntry(LibraryEntry entry)
        {
            if (entry == null)
                return;

            _playing = false;
            playbackTimer.Stop();
            UpdatePlayButton();
            DisposeCurrentLibrary();
            ClearLoadedGroups();
            SetStatus("正在加载 " + entry.Name + "...", false);

            try
            {
                _library = new BlackDragonLibrary(entry.Path);
                _libraryPath = entry.Path;
                if (entry.UseWeaponShape)
                    BuildWeaponGroups(entry);
                else
                    BuildGenericGroups(entry);

                _groups.Sort(CompareGroups);
                PopulateGallery();
                if (_groups.Count == 0)
                {
                    SetStatus(entry.Name + " 中没有可显示的非空帧。", true);
                    return;
                }

                SetStatus(string.Format("已加载 {0}：{1} 个预览组，缩略图按需加载。",
                    entry.Name, _groups.Count), false);
            }
            catch (Exception ex)
            {
                DisposeCurrentLibrary();
                ClearLoadedGroups();
                SetStatus("加载素材库失败：" + ex.Message, true);
            }
        }

        private void SelectGalleryItem(AppearanceGroup group)
        {
            _binding = true;
            try
            {
                foreach (ListViewItem item in shapeListView.Items)
                {
                    if (item.Tag == group)
                    {
                        item.Selected = true;
                        item.Focused = true;
                        item.EnsureVisible();
                        break;
                    }
                }
            }
            finally
            {
                _binding = false;
            }
        }

        private void LoadSelectedLibrary()
        {
            if (_selectedGroup == null)
                return;
            if (_library != null && string.Equals(_libraryPath, _selectedGroup.LibraryPath, StringComparison.OrdinalIgnoreCase))
                return;

            DisposeCurrentLibrary();
            try
            {
                _library = new BlackDragonLibrary(_selectedGroup.LibraryPath);
                _libraryPath = _selectedGroup.LibraryPath;
            }
            catch (Exception ex)
            {
                DisposeCurrentLibrary();
                SetStatus("加载素材库失败：" + ex.Message, true);
            }
        }

        private void BindSelectedGroup()
        {
            _binding = true;
            try
            {
                directionComboBox.Items.Clear();
                foreach (DirectionFrames direction in _selectedGroup.Directions)
                    directionComboBox.Items.Add(direction);

                if (directionComboBox.Items.Count > 0)
                    directionComboBox.SelectedIndex = 0;
                frameTrackBar.Minimum = 0;
                frameTrackBar.Value = 0;
                frameTrackBar.Maximum = 0;
            }
            finally
            {
                _binding = false;
            }

            BindFrameControls();
        }

        private void BindFrameControls()
        {
            DirectionFrames direction = directionComboBox.SelectedItem as DirectionFrames;
            _binding = true;
            try
            {
                int maximum = direction == null ? 0 : Math.Max(0, direction.Indices.Count - 1);
                if (frameTrackBar.Value > maximum)
                    frameTrackBar.Value = maximum;
                frameTrackBar.Maximum = maximum;
            }
            finally
            {
                _binding = false;
            }

            ShowSelectedFrame();
        }

        private void ShowSelectedFrame()
        {
            DirectionFrames direction = directionComboBox.SelectedItem as DirectionFrames;
            if (_selectedGroup == null || direction == null || direction.Indices.Count == 0 || _library == null)
            {
                previewPictureBox.Image = null;
                frameInfoLabel.Text = "帧：-";
                return;
            }

            int frameIndex = Math.Min(frameTrackBar.Value, direction.Indices.Count - 1);
            int imageIndex = direction.Indices[frameIndex];
            Bitmap bitmap = GetFrameBitmap(imageIndex);
            previewPictureBox.Image = bitmap;
            frameInfoLabel.Text = string.Format("帧 {0}/{1}  |  Image={2}",
                frameIndex + 1, direction.Indices.Count, imageIndex);
            if (bitmap == null)
                previewInfoLabel.Text = "该帧无法解码或为空";
            else
                previewInfoLabel.Text = string.Format("Image={0}  {1}×{2}", imageIndex, bitmap.Width, bitmap.Height);
        }

        private Bitmap GetFrameBitmap(int imageIndex)
        {
            try
            {
                BlackDragonLibrary.MImage image = _library.GetImage(imageIndex);
                if (image == null || image.Image == null)
                    return null;
                return image.Image;
            }
            catch
            {
                return null;
            }
        }

        private void MoveFrame(int delta)
        {
            DirectionFrames direction = directionComboBox.SelectedItem as DirectionFrames;
            if (direction == null || direction.Indices.Count == 0)
                return;

            int maximum = Math.Min(frameTrackBar.Maximum, direction.Indices.Count - 1);
            if (maximum < frameTrackBar.Minimum)
                return;

            int value = frameTrackBar.Value + delta;
            if (value < 0)
                value = maximum;
            else if (value > maximum)
                value = frameTrackBar.Minimum;
            frameTrackBar.Value = value;
        }

        private void UpdatePlayButton()
        {
            playButton.Text = _playing ? "暂停" : "播放";
        }

        private void ClearScanResult()
        {
            _selectedGroup = null;
            _libraries.Clear();
            _binding = true;
            try
            {
                appearanceTreeView.Nodes.Clear();
                shapeListView.Items.Clear();
                directionComboBox.Items.Clear();
                frameTrackBar.Value = 0;
                frameTrackBar.Maximum = 0;
            }
            finally
            {
                _binding = false;
            }

            ClearGroupThumbnails();
            previewPictureBox.Image = null;
            previewInfoLabel.Text = "未选择帧";
            frameInfoLabel.Text = "帧：-";
            groupInfoLabel.Text = "未选择 Shape";
        }

        private void ClearLoadedGroups()
        {
            _selectedGroup = null;
            _binding = true;
            try
            {
                shapeListView.Items.Clear();
                directionComboBox.Items.Clear();
                frameTrackBar.Value = 0;
                frameTrackBar.Maximum = 0;
            }
            finally
            {
                _binding = false;
            }

            ClearGroupThumbnails();
            previewPictureBox.Image = null;
            previewInfoLabel.Text = "未选择帧";
            frameInfoLabel.Text = "帧：-";
            groupInfoLabel.Text = "未选择预览组";
        }

        private void ClearGroupThumbnails()
        {
            thumbnailImageList.Images.Clear();
            foreach (AppearanceGroup group in _groups)
            {
                if (group.Thumbnail != null)
                    group.Thumbnail.Dispose();
                group.Thumbnail = null;
            }
            _groups.Clear();
        }

        private void DisposeCurrentLibrary()
        {
            previewPictureBox.Image = null;
            DisposeLibrary(_library);
            _library = null;
            _libraryPath = null;
        }

        private static void DisposeLibrary(BlackDragonLibrary library)
        {
            if (library == null)
                return;

            try
            {
                if (library.Images != null)
                {
                    foreach (BlackDragonLibrary.MImage image in library.Images)
                    {
                        if (image == null)
                            continue;
                        DisposeBitmap(image.Image);
                        DisposeBitmap(image.Preview);
                        DisposeBitmap(image.ShadowImage);
                        DisposeBitmap(image.ShadowPreview);
                        DisposeBitmap(image.OverlayImage);
                        DisposeBitmap(image.OverlayPreview);
                        image.Dispose();
                    }
                }
            }
            finally
            {
                library.Close();
                library.Dispose();
            }
        }

        private static void DisposeBitmap(Bitmap bitmap)
        {
            if (bitmap != null)
                bitmap.Dispose();
        }

        private static string ResolveDataPath(string path)
        {
            if (File.Exists(path))
                path = Path.GetDirectoryName(path);

            if (!string.IsNullOrEmpty(path) && Directory.Exists(path))
            {
                path = Path.GetFullPath(path);
                if (Directory.GetFiles(path, "*.Zl", SearchOption.TopDirectoryOnly).Length > 0)
                    return path;

                string childData = Path.Combine(path, "Data");
                if (Directory.Exists(childData))
                    return Path.GetFullPath(childData);
            }

            string startupData = Path.Combine(Application.StartupPath, "Data");
            if (Directory.Exists(startupData))
                return Path.GetFullPath(startupData);
            return null;
        }

        private static LibraryEntry CreateLibraryEntry(string path)
        {
            string name = Path.GetFileNameWithoutExtension(path) ?? string.Empty;
            string lowerName = name.ToLowerInvariant();
            int weaponNumber;
            bool numericWeapon = TryGetWeaponNumber(name, out weaponNumber);

            string category;
            if (lowerName.Contains("wing"))
                category = "翅膀特效";
            else if (lowerName.StartsWith("m-shield") || lowerName.StartsWith("wm-shield"))
                category = "盾牌";
            else if (lowerName.StartsWith("equipeffect-full"))
                category = "方向特效";
            else if (lowerName.StartsWith("monmagic"))
                category = "怪物魔法";
            else if (lowerName.StartsWith("m-hum") || lowerName.StartsWith("wm-hum") ||
                     lowerName.StartsWith("m-shum") || lowerName.StartsWith("wm-shum"))
                category = "盔甲";
            else if (lowerName.StartsWith("magic"))
                category = "魔法特效";
            else if (lowerName.StartsWith("m-costume") || lowerName.StartsWith("wm-costume"))
                category = "时装";
            else if (lowerName.StartsWith("m-hair") || lowerName.StartsWith("wm-hair"))
                category = "头发";
            else if (lowerName.StartsWith("m-helmet") || lowerName.StartsWith("wm-helmet"))
                category = "头盔";
            else if (lowerName.StartsWith("title"))
                category = "称号";
            else if (lowerName.StartsWith("m-weapon") || lowerName.StartsWith("wm-weapon"))
                category = "武器";
            else if (lowerName.StartsWith("equipeffect-item") ||
                     lowerName.StartsWith("equipeffect-part") ||
                     lowerName.StartsWith("equipeffect-ui") ||
                     lowerName.StartsWith("itemglow") ||
                     lowerName.StartsWith("inventory") ||
                     lowerName.StartsWith("ground") ||
                     lowerName.StartsWith("equip") ||
                     lowerName.StartsWith("storeitems") ||
                     lowerName.StartsWith("saleitem"))
                category = "物品特效";
            else if (lowerName.StartsWith("horse"))
                category = "坐骑";
            else if (lowerName.StartsWith("ui") || lowerName.StartsWith("interface") ||
                     lowerName.StartsWith("gameinter") || lowerName.StartsWith("phoneui") ||
                     lowerName.StartsWith("cbicons") || lowerName.StartsWith("micon") ||
                     lowerName.StartsWith("koreanmicon") || lowerName.StartsWith("145micon") ||
                     lowerName.StartsWith("minimap") || lowerName.StartsWith("worldmap"))
                category = "UI特效";
            else
                category = "其他";

            return new LibraryEntry
            {
                Category = category,
                Path = path,
                Name = Path.GetFileName(path),
                UseWeaponShape = numericWeapon,
                WeaponNumber = weaponNumber
            };
        }

        private static bool TryGetWeaponNumber(string name, out int number)
        {
            number = 0;
            const string malePrefix = "M-Weapon";
            const string femalePrefix = "WM-Weapon";
            string suffix;
            if (name.StartsWith(malePrefix, StringComparison.OrdinalIgnoreCase))
                suffix = name.Substring(malePrefix.Length);
            else if (name.StartsWith(femalePrefix, StringComparison.OrdinalIgnoreCase))
                suffix = name.Substring(femalePrefix.Length);
            else
                return false;

            if (!int.TryParse(suffix, out number))
                return false;
            return number > 0;
        }

        private static int GetShapeGroup(int libraryNumber)
        {
            return libraryNumber <= 7 ? libraryNumber - 1 : libraryNumber;
        }

        private static int CompareGroups(AppearanceGroup left, AppearanceGroup right)
        {
            int result = left.LibraryNumber.CompareTo(right.LibraryNumber);
            if (result != 0)
                return result;
            result = left.ShapeSlot.CompareTo(right.ShapeSlot);
            return result != 0 ? result : left.BaseIndex.CompareTo(right.BaseIndex);
        }

        private void SetStatus(string text, bool error)
        {
            statusLabel.Text = text;
            statusLabel.ForeColor = error ? Color.FromArgb(255, 170, 130) : Color.FromArgb(180, 200, 220);
        }

        private static Bitmap CreatePlaceholderThumbnail()
        {
            Bitmap bitmap = new Bitmap(96, 96);
            using (Graphics graphics = Graphics.FromImage(bitmap))
            using (Brush brush = new SolidBrush(Color.FromArgb(42, 42, 42)))
            using (Pen pen = new Pen(Color.FromArgb(90, 90, 90)))
            using (StringFormat format = new StringFormat
            {
                Alignment = StringAlignment.Center,
                LineAlignment = StringAlignment.Center
            })
            {
                graphics.FillRectangle(brush, 0, 0, bitmap.Width, bitmap.Height);
                graphics.DrawRectangle(pen, 2, 2, bitmap.Width - 5, bitmap.Height - 5);
                graphics.DrawString("无图像", SystemFonts.DefaultFont, Brushes.Gray,
                    new RectangleF(0, 0, bitmap.Width, bitmap.Height), format);
            }
            return bitmap;
        }
    }
}
