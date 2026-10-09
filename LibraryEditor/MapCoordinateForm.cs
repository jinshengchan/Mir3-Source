using Library;
using Library.SystemModels;
using MirDB;
using System;
using System.Collections.Generic;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Windows.Forms;

namespace LibraryEditor
{
    internal sealed class MapCoordinateForm : Form
    {
        private static readonly Font MapButtonFont = new Font("Microsoft YaHei UI", 9F, FontStyle.Regular, GraphicsUnit.Point);

        private sealed class MapEntry
        {
            public string FileName;
            public string Path;
            public MapInfo Info;
            public override string ToString() { return FileName; }
        }

        private sealed class MapObjectEntry
        {
            public MapInfo Map;
            public Point Point;
            public string Kind;
            public string Description;
            public override string ToString() { return Description; }
        }

        private readonly string _initialDataPath;
        private readonly TextBox _databasePath = new TextBox();
        private readonly TextBox _mapPath = new TextBox();
        private readonly TextBox _dataPath = new TextBox();
        private readonly TextBox _password = new TextBox();
        private readonly CheckBox _encrypted = new CheckBox { Text = "数据库已加密", AutoSize = true };
        private readonly Label _status = new Label { AutoSize = false, Dock = DockStyle.Bottom, Height = 22, TextAlign = ContentAlignment.MiddleLeft };
        private readonly ListBox _leftMaps = new ListBox { IntegralHeight = false };
        private readonly ListBox _rightMaps = new ListBox { IntegralHeight = false };
        private readonly MapCoordinateCanvas _leftCanvas = new MapCoordinateCanvas();
        private readonly MapCoordinateCanvas _rightCanvas = new MapCoordinateCanvas();
        private readonly Panel _leftCanvasHost = new Panel { AutoScroll = true, BackColor = Color.Black };
        private readonly Panel _rightCanvasHost = new Panel { AutoScroll = true, BackColor = Color.Black };
        private readonly Label _leftPathLabel = new Label { AutoEllipsis = true, TextAlign = ContentAlignment.MiddleLeft };
        private readonly Label _rightPathLabel = new Label { AutoEllipsis = true, TextAlign = ContentAlignment.MiddleLeft };
        private readonly Label[] _mapNameLabels = { new Label(), new Label() };
        private readonly Label[] _mapFileLabels = { new Label(), new Label() };
        private readonly Label[] _mapSizeLabels = { new Label(), new Label() };
        private readonly Label[] _mouseLabels = { new Label(), new Label() };
        private readonly Label[] _cellLabels = { new Label(), new Label() };
        private readonly ListBox[,] _objectLists = new ListBox[2, 4];
        private readonly MapCoordinateTileRenderer _tileRenderer = new MapCoordinateTileRenderer();
        private readonly Timer _animationTimer = new Timer { Interval = 100 };
        private readonly NumericUpDown[] _jumpX = { NewCoordinateInput(), NewCoordinateInput() };
        private readonly NumericUpDown[] _jumpY = { NewCoordinateInput(), NewCoordinateInput() };
        private readonly TextBox _sourceDescription = new TextBox { Text = "入口" };
        private readonly TextBox _destinationDescription = new TextBox { Text = "出口" };
        private readonly ComboBox _effect = new ComboBox { DropDownStyle = ComboBoxStyle.DropDownList };
        private readonly ComboBox _requiredClass = new ComboBox { DropDownStyle = ComboBoxStyle.DropDownList };
        private readonly TextBox _extraInfo = new TextBox();
        private readonly NumericUpDown _spanTime = new NumericUpDown { Maximum = int.MaxValue };
        private readonly CheckBox _linkTips = new CheckBox { Text = "显示门点提示", AutoSize = true };
        private readonly Button _showBlockedButton = NewToolbarButton("不可移动区域", 98);
        private readonly Button _showEntryBlockedButton = NewToolbarButton("只进不可移动", 98);
        private readonly Button _showObjectsButton = NewToolbarButton("显示地图对象", 98);
        private readonly ToolTip _toolTip = new ToolTip();

        private Session _session;
        private DBCollection<MapInfo> _maps;
        private DBCollection<MapRegion> _regions;
        private DBCollection<MovementInfo> _movements;
        private DBCollection<NPCInfo> _npcs;
        private DBCollection<GuardInfo> _guards;
        private BlackDragonLibrary _miniMapLibrary;
        private MapCoordinateTileSource _tileSource;
        private MapFileData _leftMapData;
        private MapFileData _rightMapData;
        private Point[] _sourcePoints = new Point[0];
        private Point[] _destinationPoints = new Point[0];
        private MovementInfo _currentMovement;
        private bool _showObjects = true;
        private bool _dirty;
        private bool _settingsPrompted;
        private int _sourceMapSide;
        private int _destinationMapSide = 1;
        private float _leftZoom = 1F;
        private float _rightZoom = 1F;
        private int _animation;
        private bool _tileFallbackStatusShown;

        public MapCoordinateForm(string dataPath)
        {
            _initialDataPath = dataPath;
            Text = "地图坐标编辑器";
            StartPosition = FormStartPosition.CenterParent;
            Size = new Size(1600, 850);
            MinimumSize = new Size(1450, 700);
            Font = SystemFonts.MessageBoxFont;
            BuildInterface();
            BindEvents();
            PopulateEnums();
            InitializePaths();
            _animationTimer.Tick += AnimationTimer_Tick;
            VisibleChanged += delegate
            {
                if (Visible) _animationTimer.Start();
                else _animationTimer.Stop();
            };
            Shown += delegate { BeginInvoke((MethodInvoker)PromptForSettingsIfNeeded); };
        }

        private void BuildInterface()
        {
            SuspendLayout();

            TableLayoutPanel root = new TableLayoutPanel { Dock = DockStyle.Fill, RowCount = 3, ColumnCount = 1, Padding = new Padding(6, 6, 6, 0) };
            root.RowStyles.Add(new RowStyle(SizeType.Absolute, 39));
            root.RowStyles.Add(new RowStyle(SizeType.Percent, 100F));
            root.RowStyles.Add(new RowStyle(SizeType.Absolute, 184));
            Controls.Add(root);
            Controls.Add(_status);

            FlowLayoutPanel toolbar = new FlowLayoutPanel { Dock = DockStyle.Fill, WrapContents = false, Padding = new Padding(0, 2, 0, 2), Margin = Padding.Empty };
            toolbar.Controls.Add(NewToolbarButton("保存", 62, delegate { SaveCurrentWork(); }));
            toolbar.Controls.Add(NewToolbarButton("撤销", 62, delegate { LoadData(); }));
            toolbar.Controls.Add(_showBlockedButton);
            toolbar.Controls.Add(_showEntryBlockedButton);
            toolbar.Controls.Add(_showObjectsButton);
            toolbar.Controls.Add(NewToolbarButton("跳转对象", 88, delegate { OpenObjectTable(true); }));
            toolbar.Controls.Add(NewToolbarButton("地图对象表", 88, delegate { OpenObjectTable(false); }));
            toolbar.Controls.Add(NewToolbarButton("地图连接表", 88, delegate { OpenMovementTable(); }));
            toolbar.Controls.Add(NewToolbarButton("设置", 62, delegate { ShowSettings(false); }));
            root.Controls.Add(toolbar, 0, 0);

            _showEntryBlockedButton.Enabled = false;
            _toolTip.SetToolTip(_showEntryBlockedButton, "当前 .map 数据没有可可靠区分的“只进不可移动”标记，因此此过滤项不可用。");

            TableLayoutPanel maps = new TableLayoutPanel { Dock = DockStyle.Fill, ColumnCount = 4, RowCount = 1, Margin = Padding.Empty };
            maps.ColumnStyles.Add(new ColumnStyle(SizeType.Absolute, 158));
            maps.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 50F));
            maps.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 50F));
            maps.ColumnStyles.Add(new ColumnStyle(SizeType.Absolute, 158));
            maps.Controls.Add(BuildMapListPanel("地图一目录", _leftMaps), 0, 0);
            maps.Controls.Add(BuildMapPane(true), 1, 0);
            maps.Controls.Add(BuildMapPane(false), 2, 0);
            maps.Controls.Add(BuildMapListPanel("地图二目录", _rightMaps), 3, 0);
            root.Controls.Add(maps, 0, 1);

            GroupBox properties = new GroupBox { Text = "地图连接属性", Dock = DockStyle.Fill, Margin = new Padding(0, 4, 0, 0) };
            TableLayoutPanel propertyLayout = new TableLayoutPanel { Dock = DockStyle.Fill, ColumnCount = 2, RowCount = 1, Padding = new Padding(3) };
            propertyLayout.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 50F));
            propertyLayout.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 50F));
            propertyLayout.Controls.Add(BuildPropertyPane(true), 0, 0);
            propertyLayout.Controls.Add(BuildPropertyPane(false), 1, 0);
            properties.Controls.Add(propertyLayout);
            root.Controls.Add(properties, 0, 2);
            ResumeLayout();
        }

        private static Control BuildMapListPanel(string caption, ListBox list)
        {
            TableLayoutPanel panel = new TableLayoutPanel { Dock = DockStyle.Fill, RowCount = 2, ColumnCount = 1, Margin = new Padding(0, 0, 5, 0) };
            panel.RowStyles.Add(new RowStyle(SizeType.Absolute, 24));
            panel.RowStyles.Add(new RowStyle(SizeType.Percent, 100F));
            panel.Controls.Add(new Label { Text = caption, Dock = DockStyle.Fill, TextAlign = ContentAlignment.MiddleLeft }, 0, 0);
            list.Dock = DockStyle.Fill;
            list.BorderStyle = BorderStyle.FixedSingle;
            panel.Controls.Add(list, 0, 1);
            return panel;
        }

        private Control BuildMapPane(bool source)
        {
            Panel host = source ? _leftCanvasHost : _rightCanvasHost;
            MapCoordinateCanvas canvas = source ? _leftCanvas : _rightCanvas;
            Label path = source ? _leftPathLabel : _rightPathLabel;
            int side = source ? 0 : 1;

            TableLayoutPanel pane = new TableLayoutPanel { Dock = DockStyle.Fill, RowCount = 3, ColumnCount = 1, Margin = new Padding(source ? 0 : 5, 0, source ? 5 : 0, 0) };
            pane.RowStyles.Add(new RowStyle(SizeType.Absolute, 37));
            pane.RowStyles.Add(new RowStyle(SizeType.Absolute, 24));
            pane.RowStyles.Add(new RowStyle(SizeType.Percent, 100F));

            FlowLayoutPanel controls = new FlowLayoutPanel { Dock = DockStyle.Fill, WrapContents = false, Margin = Padding.Empty, Padding = new Padding(0, 2, 0, 2) };
            controls.Controls.Add(NewSmallButton("放大", delegate { ChangeZoom(source, 2F); }));
            controls.Controls.Add(NewSmallButton("缩小", delegate { ChangeZoom(source, 0.5F); }));
            controls.Controls.Add(NewSmallButton("重置", delegate { ResetZoom(source); }));
            controls.Controls.Add(NewInlineLabel("X:"));
            controls.Controls.Add(_jumpX[side]);
            controls.Controls.Add(NewInlineLabel("Y:"));
            controls.Controls.Add(_jumpY[side]);
            controls.Controls.Add(NewSmallButton("跳转", delegate { SelectCoordinate(source, (int)_jumpX[side].Value, (int)_jumpY[side].Value); }));
            controls.Controls.Add(NewWideButton("保存进入点", delegate { CaptureSelection(source, true); }));
            controls.Controls.Add(NewWideButton("保存出口点", delegate { CaptureSelection(source, false); }));
            pane.Controls.Add(controls, 0, 0);

            path.Dock = DockStyle.Fill;
            path.Text = (source ? "地图一：" : "地图二：") + _mapPath.Text;
            pane.Controls.Add(path, 0, 1);
            host.Dock = DockStyle.Fill;
            host.BorderStyle = BorderStyle.FixedSingle;
            canvas.Location = Point.Empty;
            host.Controls.Add(canvas);
            pane.Controls.Add(host, 0, 2);
            return pane;
        }

        private Control BuildPropertyPane(bool source)
        {
            int side = source ? 0 : 1;
            TableLayoutPanel pane = new TableLayoutPanel { Dock = DockStyle.Fill, RowCount = 2, ColumnCount = 1, Margin = new Padding(source ? 0 : 3, 0, source ? 3 : 0, 0) };
            pane.RowStyles.Add(new RowStyle(SizeType.Absolute, 54));
            pane.RowStyles.Add(new RowStyle(SizeType.Percent, 100F));
            TableLayoutPanel summary = new TableLayoutPanel { Dock = DockStyle.Fill, ColumnCount = 5, RowCount = 2 };
            for (int i = 0; i < 5; i++) summary.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 20F));
            string[] captions = { "地图名称:", "地图文件:", "地图大小:", "鼠标坐标:", "单元格选中:" };
            Label[] values = { _mapNameLabels[side], _mapFileLabels[side], _mapSizeLabels[side], _mouseLabels[side], _cellLabels[side] };
            for (int i = 0; i < captions.Length; i++)
            {
                summary.Controls.Add(new Label { Text = captions[i], Dock = DockStyle.Fill, TextAlign = ContentAlignment.BottomCenter }, i, 0);
                values[i].Dock = DockStyle.Fill;
                values[i].AutoEllipsis = true;
                values[i].TextAlign = ContentAlignment.TopCenter;
                summary.Controls.Add(values[i], i, 1);
            }
            pane.Controls.Add(summary, 0, 0);

            TableLayoutPanel lists = new TableLayoutPanel { Dock = DockStyle.Fill, ColumnCount = 4, RowCount = 2 };
            for (int i = 0; i < 4; i++) lists.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 25F));
            lists.RowStyles.Add(new RowStyle(SizeType.Absolute, 23));
            lists.RowStyles.Add(new RowStyle(SizeType.Percent, 100F));
            string[] names = { "NPC数量:", "卫士数量:", "进口数量:", "出口数量:" };
            for (int i = 0; i < 4; i++)
            {
                Label count = new Label { Text = names[i] + " 0", Dock = DockStyle.Fill, TextAlign = ContentAlignment.MiddleCenter, Tag = names[i] };
                lists.Controls.Add(count, i, 0);
                ListBox list = new ListBox { Dock = DockStyle.Fill, IntegralHeight = false, BorderStyle = BorderStyle.FixedSingle, Tag = side };
                list.DoubleClick += ObjectList_DoubleClick;
                _objectLists[side, i] = list;
                lists.Controls.Add(list, i, 1);
            }
            pane.Controls.Add(lists, 0, 1);
            return pane;
        }

        private static NumericUpDown NewCoordinateInput()
        {
            return new NumericUpDown { Width = 52, Maximum = 10000, Height = 25, Margin = new Padding(2, 2, 4, 0) };
        }

        private static Button NewToolbarButton(string text, int width)
        {
            return new Button { Text = text, Font = MapButtonFont, Width = width, Height = 29, Margin = new Padding(0, 0, 10, 0), UseVisualStyleBackColor = true };
        }

        private static Button NewToolbarButton(string text, int width, EventHandler handler)
        {
            Button button = NewToolbarButton(text, width);
            button.Click += handler;
            return button;
        }

        private static Button NewSmallButton(string text, EventHandler handler)
        {
            Button button = new Button { Text = text, Font = MapButtonFont, Width = 48, Height = 27, Margin = new Padding(0, 0, 5, 0) };
            button.Click += handler;
            return button;
        }

        private static Button NewWideButton(string text, EventHandler handler)
        {
            Button button = new Button { Text = text, Font = MapButtonFont, Width = 82, Height = 27, Margin = new Padding(0, 0, 5, 0) };
            button.Click += handler;
            return button;
        }

        private static Label NewInlineLabel(string text)
        {
            return new Label { Text = text, AutoSize = true, Margin = new Padding(0, 7, 1, 0) };
        }

        private void BindEvents()
        {
            _leftMaps.SelectedIndexChanged += delegate { LoadMap(true); };
            _rightMaps.SelectedIndexChanged += delegate { LoadMap(false); };
            _leftCanvas.CoordinateChanged += delegate { UpdateCoordinateLabel(true); };
            _rightCanvas.CoordinateChanged += delegate { UpdateCoordinateLabel(false); };
            _leftCanvas.SelectionChanged += delegate { UpdateCoordinateLabel(true); };
            _rightCanvas.SelectionChanged += delegate { UpdateCoordinateLabel(false); };
            _leftCanvasHost.Resize += delegate { ResizeCanvas(true); };
            _rightCanvasHost.Resize += delegate { ResizeCanvas(false); };
            _leftCanvasHost.Scroll += delegate { _leftCanvas.Invalidate(); RefreshAnimationTimer(); };
            _rightCanvasHost.Scroll += delegate { _rightCanvas.Invalidate(); RefreshAnimationTimer(); };
            _leftCanvas.Paint += delegate { UpdateTileFallbackStatus(_leftCanvas); };
            _rightCanvas.Paint += delegate { UpdateTileFallbackStatus(_rightCanvas); };
            _showBlockedButton.Click += delegate
            {
                _leftCanvas.ShowBlockedCells = !_leftCanvas.ShowBlockedCells;
                _rightCanvas.ShowBlockedCells = _leftCanvas.ShowBlockedCells;
                _showBlockedButton.BackColor = _leftCanvas.ShowBlockedCells ? Color.LightSkyBlue : SystemColors.Control;
                _leftCanvas.Invalidate();
                _rightCanvas.Invalidate();
            };
            _showObjectsButton.Click += delegate
            {
                _showObjects = !_showObjects;
                _showObjectsButton.BackColor = _showObjects ? Color.LightSkyBlue : SystemColors.Control;
                RefreshMapObjects(true);
                RefreshMapObjects(false);
            };
            _showObjectsButton.BackColor = Color.LightSkyBlue;
            FormClosing += MapCoordinateForm_FormClosing;
        }

        private void PopulateEnums()
        {
            foreach (MovementEffect value in Enum.GetValues(typeof(MovementEffect)))
                _effect.Items.Add(value);
            foreach (RequiredClass value in Enum.GetValues(typeof(RequiredClass)))
                _requiredClass.Items.Add(value);
        }

        private void InitializePaths()
        {
            if (string.IsNullOrWhiteSpace(_initialDataPath) || !Directory.Exists(_initialDataPath)) return;
            _dataPath.Text = Path.GetFullPath(_initialDataPath);
            DirectoryInfo data = new DirectoryInfo(_initialDataPath);
            string siblingMap = Path.Combine(data.Parent == null ? data.FullName : data.Parent.FullName, "Map");
            if (Directory.Exists(siblingMap)) _mapPath.Text = siblingMap;
            UpdatePathLabels();
        }

        private void PromptForSettingsIfNeeded()
        {
            if (_settingsPrompted || IsConfigured()) return;
            _settingsPrompted = true;
            ShowSettings(true);
        }

        private bool IsConfigured()
        {
            return File.Exists(_databasePath.Text.Trim()) && Directory.Exists(_mapPath.Text.Trim()) &&
                !string.IsNullOrEmpty(ResolveDataFolder(_dataPath.Text.Trim(), _mapPath.Text.Trim()));
        }

        private void ShowSettings(bool firstPrompt)
        {
            using (MapSettingsForm dialog = new MapSettingsForm(_databasePath.Text, _mapPath.Text, _dataPath.Text, _encrypted.Checked, _password.Text))
            {
                if (dialog.ShowDialog(this) != DialogResult.OK)
                {
                    if (firstPrompt) SetStatus("尚未配置 System.db、Client\\Map 和 Client\\Data，点击“设置”后加载。", true);
                    return;
                }
                _databasePath.Text = dialog.DatabasePath;
                _mapPath.Text = dialog.MapPath;
                _dataPath.Text = dialog.DataPath;
                _encrypted.Checked = dialog.Encrypted;
                _password.Text = dialog.Password;
                UpdatePathLabels();
                LoadData();
            }
        }

        private void UpdatePathLabels()
        {
            _leftPathLabel.Text = "地图一：" + _mapPath.Text;
            _rightPathLabel.Text = "地图二：" + _mapPath.Text;
        }

        private void LoadData()
        {
            string databaseFile = _databasePath.Text.Trim();
            string mapFolder = _mapPath.Text.Trim();
            string dataFolder = ResolveDataFolder(_dataPath.Text.Trim(), mapFolder);
            if (!File.Exists(databaseFile) || !Directory.Exists(mapFolder) || string.IsNullOrEmpty(dataFolder))
            {
                SetStatus("请在“设置”中选择有效的 System.db、Map，以及包含 MiniMap.Zl 的 Client\\Data。", true);
                return;
            }
            if (!string.Equals(_dataPath.Text.Trim(), dataFolder, StringComparison.OrdinalIgnoreCase))
                _dataPath.Text = dataFolder;
            try
            {
                DisposeData();
                string root = Path.GetDirectoryName(Path.GetFullPath(databaseFile)) + Path.DirectorySeparatorChar;
                string backup = Path.Combine(root, "Backup") + Path.DirectorySeparatorChar;
                _session = new Session(SessionMode.ServerTool, new[] { typeof(MapInfo).Assembly }, _encrypted.Checked, _password.Text, root, backup);
                _session.BackUp = false;
                _session.Init();
                _maps = _session.GetCollection<MapInfo>();
                _regions = _session.GetCollection<MapRegion>();
                _movements = _session.GetCollection<MovementInfo>();
                _npcs = _session.GetCollection<NPCInfo>();
                _guards = _session.GetCollection<GuardInfo>();
                string miniMapFile = Path.Combine(dataFolder, "MiniMap.Zl");
                _miniMapLibrary = new BlackDragonLibrary(miniMapFile);
                _tileSource = new MapCoordinateTileSource(dataFolder);
                _tileFallbackStatusShown = false;
                _animation = 0;
                PopulateMapLists(mapFolder);
                NewMovement();
                _dirty = false;
                SetStatus(string.Format("已加载 {0} 张数据库地图、{1} 条地图连接。", _maps.Binding.Count, _movements.Binding.Count), false);
            }
            catch (Exception ex)
            {
                DisposeData();
                SetStatus("加载失败：" + ex.Message, true);
                MessageBox.Show(this, ex.ToString(), "加载地图数据失败", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private static string ResolveDataFolder(string selectedDataFolder, string mapFolder)
        {
            List<string> candidates = new List<string>();
            if (!string.IsNullOrWhiteSpace(selectedDataFolder)) candidates.Add(selectedDataFolder);
            if (!string.IsNullOrWhiteSpace(mapFolder))
            {
                DirectoryInfo map = new DirectoryInfo(mapFolder);
                if (map.Parent != null)
                {
                    candidates.Add(Path.Combine(map.Parent.FullName, "Data"));
                    candidates.Add(Path.Combine(map.Parent.FullName, "Client", "Data"));
                }
            }
            foreach (string candidate in candidates)
            {
                string fullPath;
                try { fullPath = Path.GetFullPath(candidate); }
                catch { continue; }
                if (File.Exists(Path.Combine(fullPath, "MiniMap.Zl"))) return fullPath;
            }
            return string.Empty;
        }

        private void PopulateMapLists(string mapFolder)
        {
            Dictionary<string, MapInfo> infoByFile = _maps.Binding.Where(map => !string.IsNullOrWhiteSpace(map.FileName))
                .GroupBy(map => map.FileName, StringComparer.OrdinalIgnoreCase)
                .ToDictionary(group => group.Key, group => group.First(), StringComparer.OrdinalIgnoreCase);
            List<MapEntry> entries = Directory.GetFiles(mapFolder, "*.map").Select(path =>
            {
                string name = Path.GetFileNameWithoutExtension(path);
                MapInfo info;
                infoByFile.TryGetValue(name, out info);
                return new MapEntry { FileName = name, Path = path, Info = info };
            }).OrderBy(entry => entry.FileName, StringComparer.OrdinalIgnoreCase).ToList();
            _leftMaps.DataSource = new List<MapEntry>(entries);
            _rightMaps.DataSource = new List<MapEntry>(entries);
            if (_leftMaps.Items.Count > 0) _leftMaps.SelectedIndex = 0;
            if (_rightMaps.Items.Count > 1) _rightMaps.SelectedIndex = 1;
            else if (_rightMaps.Items.Count > 0) _rightMaps.SelectedIndex = 0;
        }

        private void LoadMap(bool source)
        {
            ListBox list = source ? _leftMaps : _rightMaps;
            MapEntry entry = list.SelectedItem as MapEntry;
            if (entry == null) return;
            try
            {
                MapFileData map = MapFileReader.Read(entry.Path);
                Image miniMap = GetMiniMap(entry.Info);
                MapCoordinateCanvas canvas = source ? _leftCanvas : _rightCanvas;
                if (_tileSource != null) _tileSource.ClearCache();
                _tileFallbackStatusShown = false;
                canvas.SetMap(map, miniMap, _tileRenderer, _tileSource, _tileSource != null);
                (source ? _rightCanvas : _leftCanvas).Invalidate();
                if (source) _leftMapData = map; else _rightMapData = map;
                FitMap(source);
                RefreshMapObjects(source);
                UpdateCoordinateLabel(source);
                RefreshAnimationTimer();
            }
            catch (Exception ex)
            {
                SetStatus(entry.FileName + " 加载失败：" + ex.Message, true);
            }
        }

        private Image GetMiniMap(MapInfo info)
        {
            if (info == null || info.MiniMap <= 0 || _miniMapLibrary == null) return null;
            BlackDragonLibrary.MImage image = _miniMapLibrary.CreateImage(info.MiniMap, ImageType.Image);
            return image == null ? null : image.Image;
        }

        private void ResizeCanvas(bool source)
        {
            MapFileData map = source ? _leftMapData : _rightMapData;
            Panel host = source ? _leftCanvasHost : _rightCanvasHost;
            MapCoordinateCanvas canvas = source ? _leftCanvas : _rightCanvas;
            float zoom = source ? _leftZoom : _rightZoom;
            if (map == null || host.ClientSize.Width < 2 || host.ClientSize.Height < 2) return;
            canvas.SetZoom(zoom);
            canvas.Dock = DockStyle.None;
            canvas.Location = Point.Empty;
            canvas.Size = host.ClientSize;
            host.AutoScrollMinSize = canvas.VirtualExtent;
        }

        private void ChangeZoom(bool source, float factor)
        {
            MapCoordinateCanvas canvas = source ? _leftCanvas : _rightCanvas;
            Panel host = source ? _leftCanvasHost : _rightCanvasHost;
            if ((source ? _leftMapData : _rightMapData) == null) return;
            float oldZoom = source ? _leftZoom : _rightZoom;
            float newZoom = Math.Max(0.01F, Math.Min(4F, oldZoom * factor));
            ApplyZoom(source, canvas, host, oldZoom, newZoom);
        }

        private void ResetZoom(bool source)
        {
            MapCoordinateCanvas canvas = source ? _leftCanvas : _rightCanvas;
            Panel host = source ? _leftCanvasHost : _rightCanvasHost;
            float oldZoom = source ? _leftZoom : _rightZoom;
            ApplyZoom(source, canvas, host, oldZoom, 1F);
        }

        private void FitMap(bool source)
        {
            MapFileData map = source ? _leftMapData : _rightMapData;
            Panel host = source ? _leftCanvasHost : _rightCanvasHost;
            MapCoordinateCanvas canvas = source ? _leftCanvas : _rightCanvas;
            if (map == null || host.ClientSize.Width < 2 || host.ClientSize.Height < 2) return;
            host.AutoScrollMinSize = Size.Empty;
            host.AutoScrollPosition = Point.Empty;
            float zoom = Math.Min(1F, Math.Min(
                (host.ClientSize.Width - 1) / (map.Width * 48F),
                (host.ClientSize.Height - 1) / (map.Height * 32F)));
            if (source) _leftZoom = zoom; else _rightZoom = zoom;
            canvas.SetZoom(zoom);
            host.AutoScrollMinSize = canvas.VirtualExtent;
            canvas.Invalidate();
            RefreshAnimationTimer();
        }

        private void ApplyZoom(bool source, MapCoordinateCanvas canvas, Panel host, float oldZoom, float newZoom)
        {
            if (canvas == null || host == null || oldZoom <= 0F) return;
            Point scroll = canvas.ScrollOffset;
            Point center = new Point(host.ClientSize.Width / 2, host.ClientSize.Height / 2);
            PointF mapCenter = new PointF(
                (center.X + scroll.X) / (48F * oldZoom),
                (center.Y + scroll.Y) / (32F * oldZoom));
            if (source) _leftZoom = newZoom; else _rightZoom = newZoom;
            canvas.SetZoom(newZoom);
            host.AutoScrollMinSize = canvas.VirtualExtent;
            host.AutoScrollPosition = new Point(
                Math.Max(0, (int)(mapCenter.X * 48F * newZoom - center.X)),
                Math.Max(0, (int)(mapCenter.Y * 32F * newZoom - center.Y)));
            canvas.Invalidate();
            RefreshAnimationTimer();
        }

        private void SelectCoordinate(bool source, int x, int y)
        {
            MapFileData map = source ? _leftMapData : _rightMapData;
            MapCoordinateCanvas canvas = source ? _leftCanvas : _rightCanvas;
            if (map == null || x < 0 || y < 0 || x >= map.Width || y >= map.Height)
            {
                SetStatus("跳转坐标超出当前地图范围。", true);
                return;
            }
            canvas.SetSelection(new[] { new Point(x, y) });
            UpdateCoordinateLabel(source);
        }

        private void CaptureSelection(bool canvasIsLeft, bool asSource)
        {
            MapCoordinateCanvas canvas = canvasIsLeft ? _leftCanvas : _rightCanvas;
            Point[] points = canvas.Selection.OrderBy(point => point.Y).ThenBy(point => point.X).ToArray();
            if (points.Length == 0)
            {
                SetStatus("请先在地图上用鼠标拖选坐标区域。", true);
                return;
            }
            if (asSource)
            {
                _sourcePoints = points;
                _sourceMapSide = canvasIsLeft ? 0 : 1;
            }
            else
            {
                _destinationPoints = points;
                _destinationMapSide = canvasIsLeft ? 0 : 1;
            }
            SetStatus(string.Format("已记录{0}区域：{1} 个格子。顶部“保存”会写入编辑会话并保存数据库。", asSource ? "入口" : "出口", points.Length), false);
            UpdateCoordinateLabel(canvasIsLeft);
        }

        private void RefreshMapObjects(bool source)
        {
            int side = source ? 0 : 1;
            MapEntry entry = (source ? _leftMaps : _rightMaps).SelectedItem as MapEntry;
            MapFileData map = source ? _leftMapData : _rightMapData;
            MapCoordinateCanvas canvas = source ? _leftCanvas : _rightCanvas;
            for (int i = 0; i < 4; i++) _objectLists[side, i].Items.Clear();
            canvas.Markers.Clear();
            if (entry == null || entry.Info == null || map == null)
            {
                UpdateObjectCounts(side);
                canvas.Invalidate();
                return;
            }

            foreach (NPCInfo npc in _npcs.Binding.Where(item => item.Region != null && item.Region.Map == entry.Info))
            {
                Point point = npc.Region.GetPoints(map.Width).FirstOrDefault();
                AddObject(side, 0, entry.Info, point, "NPC", npc.NPCName, canvas, Color.Lime);
            }
            foreach (GuardInfo guard in _guards.Binding.Where(item => item.Map == entry.Info))
                AddObject(side, 1, entry.Info, new Point(guard.X, guard.Y), "卫士", "#" + guard.Index, canvas, Color.Gold);
            foreach (MovementInfo movement in _movements.Binding)
            {
                if (movement.SourceRegion != null && movement.SourceRegion.Map == entry.Info)
                    AddRegionObject(side, 2, entry.Info, movement.SourceRegion, map.Width, "进口", movement.Index, canvas, Color.DeepSkyBlue);
                if (movement.DestinationRegion != null && movement.DestinationRegion.Map == entry.Info)
                    AddRegionObject(side, 3, entry.Info, movement.DestinationRegion, map.Width, "出口", movement.Index, canvas, Color.OrangeRed);
            }
            UpdateObjectCounts(side);
            if (!_showObjects) canvas.Markers.Clear();
            canvas.Invalidate();
        }

        private void AddObject(int side, int category, MapInfo map, Point point, string kind, string description, MapCoordinateCanvas canvas, Color color)
        {
            MapObjectEntry item = new MapObjectEntry { Map = map, Point = point, Kind = kind, Description = string.Format("{0} ({1},{2})", description, point.X, point.Y) };
            _objectLists[side, category].Items.Add(item);
            if (_showObjects) canvas.Markers.Add(Tuple.Create(point, color, kind));
        }

        private void AddRegionObject(int side, int category, MapInfo map, MapRegion region, int width, string kind, int index, MapCoordinateCanvas canvas, Color color)
        {
            Point point = region.GetPoints(width).FirstOrDefault();
            AddObject(side, category, map, point, kind, string.Format("#{0} {1}", index, region.Description), canvas, color);
        }

        private void UpdateObjectCounts(int side)
        {
            for (int i = 0; i < 4; i++)
            {
                TableLayoutPanel parent = _objectLists[side, i].Parent as TableLayoutPanel;
                if (parent == null) continue;
                Label label = parent.GetControlFromPosition(i, 0) as Label;
                if (label != null) label.Text = (string)label.Tag + " " + _objectLists[side, i].Items.Count;
            }
        }

        private void UpdateCoordinateLabel(bool source)
        {
            int side = source ? 0 : 1;
            MapEntry entry = (source ? _leftMaps : _rightMaps).SelectedItem as MapEntry;
            MapFileData map = source ? _leftMapData : _rightMapData;
            MapCoordinateCanvas canvas = source ? _leftCanvas : _rightCanvas;
            if (entry == null || map == null)
            {
                _mapNameLabels[side].Text = _mapFileLabels[side].Text = _mapSizeLabels[side].Text = _mouseLabels[side].Text = _cellLabels[side].Text = "-";
                return;
            }
            _mapNameLabels[side].Text = entry.Info == null ? "-" : entry.Info.Description;
            _mapFileLabels[side].Text = entry.FileName;
            _mapSizeLabels[side].Text = map.Width + " × " + map.Height;
            _mouseLabels[side].Text = canvas.CurrentCoordinate.X + ", " + canvas.CurrentCoordinate.Y;
            _cellLabels[side].Text = canvas.Selection.Count.ToString();
        }

        private void ObjectList_DoubleClick(object sender, EventArgs e)
        {
            ListBox list = sender as ListBox;
            MapObjectEntry item = list == null ? null : list.SelectedItem as MapObjectEntry;
            if (item == null) return;
            JumpToObject((int)list.Tag == 0, item);
        }

        private IEnumerable<MapObjectEntry> GetVisibleObjects()
        {
            for (int side = 0; side < 2; side++)
                for (int category = 0; category < 4; category++)
                    foreach (MapObjectEntry item in _objectLists[side, category].Items.OfType<MapObjectEntry>())
                        yield return item;
        }

        private void OpenObjectTable(bool jumpMode)
        {
            List<MapObjectEntry> objects = GetVisibleObjects().GroupBy(item => new { item.Map, item.Point, item.Kind, item.Description }).Select(group => group.First()).ToList();
            if (objects.Count == 0)
            {
                SetStatus("当前两张地图没有可显示的地图对象。", true);
                return;
            }
            using (MapObjectSelectionForm form = new MapObjectSelectionForm(objects, jumpMode))
            {
                if (form.ShowDialog(this) == DialogResult.OK && form.SelectedObject != null)
                    JumpToObject(true, form.SelectedObject);
            }
        }

        private void JumpToObject(bool source, MapObjectEntry item)
        {
            ListBox maps = source ? _leftMaps : _rightMaps;
            SelectMap(maps, item.Map);
            SelectCoordinate(source, item.Point.X, item.Point.Y);
            int side = source ? 0 : 1;
            _jumpX[side].Value = Math.Max(_jumpX[side].Minimum, Math.Min(_jumpX[side].Maximum, item.Point.X));
            _jumpY[side].Value = Math.Max(_jumpY[side].Minimum, Math.Min(_jumpY[side].Maximum, item.Point.Y));
        }

        private void NewMovement()
        {
            _currentMovement = null;
            _sourceMapSide = 0;
            _destinationMapSide = 1;
            _sourcePoints = new Point[0];
            _destinationPoints = new Point[0];
            _leftCanvas.ClearSelection();
            _rightCanvas.ClearSelection();
            _sourceDescription.Text = "入口";
            _destinationDescription.Text = "出口";
            _extraInfo.Clear();
            _effect.SelectedIndex = 0;
            _requiredClass.SelectedItem = RequiredClass.All;
            _spanTime.Value = 0;
            _linkTips.Checked = false;
        }

        private void SaveCurrentWork()
        {
            if (_session == null)
            {
                ShowSettings(true);
                return;
            }
            if (_sourcePoints.Length > 0 || _destinationPoints.Length > 0)
            {
                if (!SaveMovement()) return;
            }
            SaveDatabase();
        }

        private bool SaveMovement()
        {
            MapEntry sourceMap = (_sourceMapSide == 0 ? _leftMaps : _rightMaps).SelectedItem as MapEntry;
            MapEntry destinationMap = (_destinationMapSide == 0 ? _leftMaps : _rightMaps).SelectedItem as MapEntry;
            if (sourceMap == null || destinationMap == null || sourceMap.Info == null || destinationMap.Info == null)
            {
                SetStatus("入口和出口都必须选择数据库中存在的地图。", true);
                return false;
            }
            if (_sourcePoints.Length == 0 || _destinationPoints.Length == 0)
            {
                SetStatus("请先保存入口点和出口点。", true);
                return false;
            }
            if (_currentMovement == null)
            {
                _currentMovement = _movements.CreateNewObject();
                _currentMovement.SourceRegion = _regions.CreateNewObject();
                _currentMovement.DestinationRegion = _regions.CreateNewObject();
            }
            ApplyRegion(_currentMovement.SourceRegion, sourceMap.Info, _sourceDescription.Text, _sourcePoints);
            ApplyRegion(_currentMovement.DestinationRegion, destinationMap.Info, _destinationDescription.Text, _destinationPoints);
            _currentMovement.Effect = (MovementEffect)_effect.SelectedItem;
            _currentMovement.RequiredClass = (RequiredClass)_requiredClass.SelectedItem;
            _currentMovement.ExtraInfo = _extraInfo.Text;
            _currentMovement.CanLinkTips = _linkTips.Checked;
            _currentMovement.SpanTime = (int)_spanTime.Value;
            _dirty = true;
            RefreshMapObjects(true);
            RefreshMapObjects(false);
            return true;
        }

        private static void ApplyRegion(MapRegion region, MapInfo map, string description, Point[] points)
        {
            region.Map = map;
            region.Description = description;
            region.BitRegion = null;
            region.PointRegion = points.ToArray();
            region.Size = points.Length;
        }

        private void OpenMovementTable()
        {
            if (_movements == null)
            {
                SetStatus("请先在“设置”中加载数据库。", true);
                return;
            }
            using (MovementSelectionForm form = new MovementSelectionForm(_movements.Binding, _toolTip))
            {
                DialogResult result = form.ShowDialog(this);
                if (result != DialogResult.OK) return;
                if (form.Action == MovementSelectionAction.SaveDatabase)
                {
                    SaveDatabase();
                    return;
                }
                if (form.SelectedMovement == null) return;
                LoadMovement(form.SelectedMovement);
                if (form.Action == MovementSelectionAction.Delete) DeleteMovement();
                else if (form.Action == MovementSelectionAction.Edit) EditMovementProperties();
            }
        }

        private void EditMovementProperties()
        {
            if (_currentMovement == null) return;
            using (MovementPropertyForm dialog = new MovementPropertyForm(_sourceDescription.Text, _destinationDescription.Text,
                (MovementEffect)_effect.SelectedItem, (RequiredClass)_requiredClass.SelectedItem, _extraInfo.Text, _linkTips.Checked, (int)_spanTime.Value))
            {
                if (dialog.ShowDialog(this) != DialogResult.OK) return;
                _sourceDescription.Text = dialog.SourceDescription;
                _destinationDescription.Text = dialog.DestinationDescription;
                _effect.SelectedItem = dialog.Effect;
                _requiredClass.SelectedItem = dialog.RequiredClass;
                _extraInfo.Text = dialog.ExtraInfo;
                _linkTips.Checked = dialog.LinkTips;
                _spanTime.Value = dialog.SpanTime;
                SaveMovement();
                SetStatus("连接属性已写入编辑会话，点击顶部“保存”写入数据库。", false);
            }
        }

        private void LoadMovement(MovementInfo movement)
        {
            _currentMovement = movement;
            _sourceMapSide = 0;
            _destinationMapSide = 1;
            SelectMap(_leftMaps, movement.SourceRegion == null ? null : movement.SourceRegion.Map);
            SelectMap(_rightMaps, movement.DestinationRegion == null ? null : movement.DestinationRegion.Map);
            _sourcePoints = movement.SourceRegion == null || _leftMapData == null ? new Point[0] : movement.SourceRegion.GetPoints(_leftMapData.Width).ToArray();
            _destinationPoints = movement.DestinationRegion == null || _rightMapData == null ? new Point[0] : movement.DestinationRegion.GetPoints(_rightMapData.Width).ToArray();
            _leftCanvas.SetSelection(_sourcePoints);
            _rightCanvas.SetSelection(_destinationPoints);
            _sourceDescription.Text = movement.SourceRegion == null ? string.Empty : movement.SourceRegion.Description;
            _destinationDescription.Text = movement.DestinationRegion == null ? string.Empty : movement.DestinationRegion.Description;
            _effect.SelectedItem = movement.Effect;
            _requiredClass.SelectedItem = movement.RequiredClass;
            _extraInfo.Text = movement.ExtraInfo ?? string.Empty;
            _linkTips.Checked = movement.CanLinkTips;
            _spanTime.Value = Math.Max(_spanTime.Minimum, Math.Min(_spanTime.Maximum, movement.SpanTime));
            SetStatus("已载入地图连接 #" + movement.Index + "。", false);
        }

        private static void SelectMap(ListBox list, MapInfo map)
        {
            if (map == null) return;
            for (int i = 0; i < list.Items.Count; i++)
            {
                MapEntry entry = list.Items[i] as MapEntry;
                if (entry != null && entry.Info == map) { list.SelectedIndex = i; return; }
            }
        }

        private void DeleteMovement()
        {
            if (_currentMovement == null) return;
            if (MessageBox.Show(this, "删除连接 #" + _currentMovement.Index + "？关联区域会保留，避免误删其他对象使用的区域。", "删除地图连接", MessageBoxButtons.YesNo, MessageBoxIcon.Warning) != DialogResult.Yes) return;
            _currentMovement.Delete();
            _currentMovement = null;
            _dirty = true;
            RefreshMapObjects(true);
            RefreshMapObjects(false);
            SetStatus("连接已从编辑会话删除；点击顶部“保存”写入数据库。", false);
        }

        private void SaveDatabase()
        {
            if (_session == null) return;
            if (!_dirty) { SetStatus("当前没有需要写入数据库的地图连接修改。", false); return; }
            if (MessageBox.Show(this, "确认把地图连接修改写入：\r\n" + _databasePath.Text, "保存数据库", MessageBoxButtons.YesNo, MessageBoxIcon.Warning) != DialogResult.Yes) return;
            try
            {
                _session.Save(true, SessionMode.ServerTool);
                _dirty = false;
                NewMovement();
                SetStatus("数据库保存完成，已进入新建连接状态。", false);
            }
            catch (Exception ex)
            {
                SetStatus("保存失败：" + ex.Message, true);
                MessageBox.Show(this, ex.ToString(), "保存数据库失败", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void SetStatus(string text, bool error)
        {
            _status.Text = text;
            _status.ForeColor = error ? Color.Firebrick : Color.DarkGreen;
        }

        private void AnimationTimer_Tick(object sender, EventArgs e)
        {
            if (!Visible)
            {
                _animationTimer.Stop();
                return;
            }
            if (!_leftCanvas.HasVisibleAnimatedCells && !_rightCanvas.HasVisibleAnimatedCells)
            {
                _animationTimer.Stop();
                return;
            }
            _animation++;
            _leftCanvas.SetAnimation(_animation);
            _rightCanvas.SetAnimation(_animation);
        }

        private void RefreshAnimationTimer()
        {
            if (Visible && (_leftCanvas.HasVisibleAnimatedCells || _rightCanvas.HasVisibleAnimatedCells))
                _animationTimer.Start();
        }

        private void UpdateTileFallbackStatus(MapCoordinateCanvas canvas)
        {
            if (_tileFallbackStatusShown || _tileSource == null || canvas == null || !canvas.LastFrameUsedFallback || _tileSource.MissingLibraryCount == 0) return;
            _tileFallbackStatusShown = true;
            SetStatus(string.Format("实际地图素材不可用，已使用 MiniMap 回退（缺失素材库 {0} 个）。", _tileSource.MissingLibraryCount), false);
        }

        private void MapCoordinateForm_FormClosing(object sender, FormClosingEventArgs e)
        {
            if (_dirty && MessageBox.Show(this, "还有未写入数据库的地图连接修改，确定关闭？", "未保存修改", MessageBoxButtons.YesNo, MessageBoxIcon.Warning) != DialogResult.Yes)
            {
                e.Cancel = true;
                return;
            }
            DisposeData();
            _animationTimer.Stop();
            _animationTimer.Dispose();
        }

        private void DisposeData()
        {
            _animationTimer.Stop();
            if (_tileSource != null) _tileSource.Dispose();
            _tileSource = null;
            if (_miniMapLibrary != null) _miniMapLibrary.Dispose();
            _miniMapLibrary = null;
            if (_session != null) _session.Dispose();
            _session = null;
            _maps = null;
            _regions = null;
            _movements = null;
            _npcs = null;
            _guards = null;
        }

        private enum MovementSelectionAction { None, Edit, Delete, SaveDatabase }

        private sealed class MovementSelectionForm : Form
        {
            private readonly DataGridView _grid = new DataGridView();
            public MovementInfo SelectedMovement { get; private set; }
            public MovementSelectionAction Action { get; private set; }

            public MovementSelectionForm(IEnumerable<MovementInfo> movements, ToolTip toolTip)
            {
                Text = "地图连接表";
                StartPosition = FormStartPosition.CenterParent;
                Size = new Size(900, 500);
                MinimumSize = new Size(760, 400);
                _grid.Dock = DockStyle.Fill;
                _grid.ReadOnly = true;
                _grid.AllowUserToAddRows = false;
                _grid.AllowUserToDeleteRows = false;
                _grid.AutoGenerateColumns = false;
                _grid.SelectionMode = DataGridViewSelectionMode.FullRowSelect;
                _grid.MultiSelect = false;
                _grid.BackgroundColor = Color.DarkGray;
                AddColumn("源区域", 105);
                AddColumn("目标区域", 105);
                AddColumn("需要道具", 105);
                AddColumn("需要", 54);
                AddColumn("职业限制", 85);
                AddColumn("特殊", 62);
                AddColumn("Movement", 300);
                foreach (MovementInfo movement in movements.OrderBy(item => item.Index))
                {
                    int row = _grid.Rows.Add(
                        movement.SourceRegion == null ? string.Empty : movement.SourceRegion.ServerDescription,
                        movement.DestinationRegion == null ? string.Empty : movement.DestinationRegion.ServerDescription,
                        movement.NeedItem == null ? "-" : movement.NeedItem.ToString(),
                        movement.NeedSpawn == null ? "否" : "是",
                        movement.RequiredClass,
                        string.IsNullOrEmpty(movement.ExtraInfo) ? "-" : movement.ExtraInfo,
                        movement.GetType().FullName);
                    _grid.Rows[row].Tag = movement;
                }
                _grid.CellDoubleClick += delegate { Complete(MovementSelectionAction.Edit); };
                Controls.Add(_grid);

                FlowLayoutPanel buttons = new FlowLayoutPanel { Dock = DockStyle.Bottom, Height = 45, FlowDirection = FlowDirection.LeftToRight, Padding = new Padding(7, 7, 0, 0), WrapContents = false };
                buttons.Controls.Add(NewActionButton("编辑属性", delegate { Complete(MovementSelectionAction.Edit); }));
                buttons.Controls.Add(NewActionButton("删除", delegate { Complete(MovementSelectionAction.Delete); }));
                buttons.Controls.Add(NewActionButton("数据库写入", delegate { Complete(MovementSelectionAction.SaveDatabase); }));
                Button sync = NewActionButton("同步热更", null);
                Button local = NewActionButton("保存本地", null);
                Button export = NewActionButton("导出", null);
                Button import = NewActionButton("导入", null);
                sync.Enabled = local.Enabled = export.Enabled = import.Enabled = false;
                toolTip.SetToolTip(sync, "当前工程没有可靠的服务端热更新接口，不能伪造同步成功。");
                toolTip.SetToolTip(local, "地图连接由 MirDB System.db 管理，没有独立且可回读的本地格式。");
                toolTip.SetToolTip(export, "当前未定义兼容的地图连接导出格式。");
                toolTip.SetToolTip(import, "当前未定义兼容的地图连接导入格式。");
                buttons.Controls.Add(sync);
                buttons.Controls.Add(local);
                buttons.Controls.Add(export);
                buttons.Controls.Add(import);
                buttons.Controls.Add(NewActionButton("关闭", delegate { DialogResult = DialogResult.Cancel; }));
                Controls.Add(buttons);
            }

            private void AddColumn(string text, int width)
            {
                _grid.Columns.Add(new DataGridViewTextBoxColumn { HeaderText = text, Width = width });
            }

            private static Button NewActionButton(string text, EventHandler handler)
            {
                int width = text == "数据库写入" ? 88 :
                    text == "编辑属性" || text == "同步热更" || text == "保存本地" ? 80 :
                    text == "关闭" ? 68 : 56;
                Button button = new Button { Text = text, Font = MapButtonFont, Width = width, Height = 28, Margin = new Padding(0, 0, 8, 0) };
                if (handler != null) button.Click += handler;
                return button;
            }

            private void Complete(MovementSelectionAction action)
            {
                if (action != MovementSelectionAction.SaveDatabase)
                {
                    if (_grid.SelectedRows.Count == 0) return;
                    SelectedMovement = _grid.SelectedRows[0].Tag as MovementInfo;
                    if (SelectedMovement == null) return;
                }
                Action = action;
                DialogResult = DialogResult.OK;
            }
        }

        private sealed class MapSettingsForm : Form
        {
            private readonly TextBox _database = new TextBox();
            private readonly TextBox _map = new TextBox();
            private readonly TextBox _data = new TextBox();
            private readonly CheckBox _encrypted = new CheckBox { Text = "数据库已加密", AutoSize = true };
            private readonly TextBox _password = new TextBox { UseSystemPasswordChar = true };
            public string DatabasePath { get { return _database.Text.Trim(); } }
            public string MapPath { get { return _map.Text.Trim(); } }
            public string DataPath { get { return _data.Text.Trim(); } }
            public bool Encrypted { get { return _encrypted.Checked; } }
            public string Password { get { return _password.Text; } }

            public MapSettingsForm(string database, string map, string data, bool encrypted, string password)
            {
                Text = "地图坐标设置";
                StartPosition = FormStartPosition.CenterParent;
                FormBorderStyle = FormBorderStyle.FixedDialog;
                MaximizeBox = false;
                MinimizeBox = false;
                ClientSize = new Size(690, 205);
                _database.Text = database;
                _map.Text = map;
                _data.Text = data;
                _encrypted.Checked = encrypted;
                _password.Text = password;
                TableLayoutPanel layout = new TableLayoutPanel { Dock = DockStyle.Fill, ColumnCount = 3, RowCount = 5, Padding = new Padding(10) };
                layout.ColumnStyles.Add(new ColumnStyle(SizeType.Absolute, 100));
                layout.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 100));
                layout.ColumnStyles.Add(new ColumnStyle(SizeType.Absolute, 92));
                AddPath(layout, 0, "System.db", _database, false);
                AddPath(layout, 1, "Client\\Map", _map, true);
                AddPath(layout, 2, "Client\\Data", _data, true);
                layout.Controls.Add(_encrypted, 1, 3);
                layout.Controls.Add(new Label { Text = "临时密码", Dock = DockStyle.Fill, TextAlign = ContentAlignment.MiddleLeft }, 0, 4);
                _password.Dock = DockStyle.Fill;
                layout.Controls.Add(_password, 1, 4);
                FlowLayoutPanel buttons = new FlowLayoutPanel { Dock = DockStyle.Fill, FlowDirection = FlowDirection.RightToLeft, WrapContents = false };
                Button ok = new Button { Text = "加载", Font = MapButtonFont, DialogResult = DialogResult.OK, Width = 78 };
                Button cancel = new Button { Text = "取消", Font = MapButtonFont, DialogResult = DialogResult.Cancel, Width = 78 };
                buttons.Controls.Add(ok);
                buttons.Controls.Add(cancel);
                layout.Controls.Add(buttons, 2, 4);
                Controls.Add(layout);
                AcceptButton = ok;
                CancelButton = cancel;
            }

            private void AddPath(TableLayoutPanel layout, int row, string caption, TextBox box, bool folder)
            {
                layout.Controls.Add(new Label { Text = caption, Dock = DockStyle.Fill, TextAlign = ContentAlignment.MiddleLeft }, 0, row);
                box.Dock = DockStyle.Fill;
                layout.Controls.Add(box, 1, row);
                Button browse = new Button { Text = "选择...", Font = MapButtonFont, Dock = DockStyle.Fill };
                browse.Click += delegate
                {
                    if (folder)
                    {
                        using (FolderBrowserDialog dialog = new FolderBrowserDialog { SelectedPath = Directory.Exists(box.Text) ? box.Text : string.Empty })
                            if (dialog.ShowDialog(this) == DialogResult.OK) box.Text = dialog.SelectedPath;
                    }
                    else
                    {
                        using (OpenFileDialog dialog = new OpenFileDialog { Filter = "System.db|System.db|数据库文件 (*.db)|*.db|所有文件 (*.*)|*.*" })
                            if (dialog.ShowDialog(this) == DialogResult.OK) box.Text = dialog.FileName;
                    }
                };
                layout.Controls.Add(browse, 2, row);
            }
        }

        private sealed class MapObjectSelectionForm : Form
        {
            private readonly DataGridView _grid = new DataGridView();
            public MapObjectEntry SelectedObject { get; private set; }

            public MapObjectSelectionForm(IEnumerable<MapObjectEntry> objects, bool jumpMode)
            {
                Text = jumpMode ? "跳转对象" : "地图对象表";
                StartPosition = FormStartPosition.CenterParent;
                Size = new Size(720, 450);
                _grid.Dock = DockStyle.Fill;
                _grid.ReadOnly = true;
                _grid.AllowUserToAddRows = false;
                _grid.AllowUserToDeleteRows = false;
                _grid.SelectionMode = DataGridViewSelectionMode.FullRowSelect;
                _grid.MultiSelect = false;
                _grid.Columns.Add("Map", "地图");
                _grid.Columns.Add("Kind", "类型");
                _grid.Columns.Add("Description", "对象");
                _grid.Columns.Add("Coordinate", "坐标");
                _grid.Columns[0].Width = 180;
                _grid.Columns[1].Width = 90;
                _grid.Columns[2].AutoSizeMode = DataGridViewAutoSizeColumnMode.Fill;
                foreach (MapObjectEntry item in objects)
                {
                    int row = _grid.Rows.Add(item.Map == null ? "-" : item.Map.Description, item.Kind, item.Description, item.Point.X + ", " + item.Point.Y);
                    _grid.Rows[row].Tag = item;
                }
                _grid.CellDoubleClick += delegate { AcceptSelection(); };
                Controls.Add(_grid);
                FlowLayoutPanel buttons = new FlowLayoutPanel { Dock = DockStyle.Bottom, Height = 40, FlowDirection = FlowDirection.RightToLeft, Padding = new Padding(5) };
                Button close = new Button { Text = "关闭", Font = MapButtonFont, DialogResult = DialogResult.Cancel };
                Button jump = new Button { Text = "跳转", Font = MapButtonFont };
                jump.Click += delegate { AcceptSelection(); };
                buttons.Controls.Add(close);
                buttons.Controls.Add(jump);
                Controls.Add(buttons);
            }

            private void AcceptSelection()
            {
                if (_grid.SelectedRows.Count == 0) return;
                SelectedObject = _grid.SelectedRows[0].Tag as MapObjectEntry;
                if (SelectedObject != null) DialogResult = DialogResult.OK;
            }
        }

        private sealed class MovementPropertyForm : Form
        {
            private readonly TextBox _source = new TextBox();
            private readonly TextBox _destination = new TextBox();
            private readonly ComboBox _effect = new ComboBox { DropDownStyle = ComboBoxStyle.DropDownList };
            private readonly ComboBox _requiredClass = new ComboBox { DropDownStyle = ComboBoxStyle.DropDownList };
            private readonly TextBox _extra = new TextBox();
            private readonly CheckBox _tips = new CheckBox { Text = "显示门点提示", AutoSize = true };
            private readonly NumericUpDown _span = new NumericUpDown { Maximum = int.MaxValue };
            public string SourceDescription { get { return _source.Text; } }
            public string DestinationDescription { get { return _destination.Text; } }
            public MovementEffect Effect { get { return (MovementEffect)_effect.SelectedItem; } }
            public RequiredClass RequiredClass { get { return (RequiredClass)_requiredClass.SelectedItem; } }
            public string ExtraInfo { get { return _extra.Text; } }
            public bool LinkTips { get { return _tips.Checked; } }
            public int SpanTime { get { return (int)_span.Value; } }

            public MovementPropertyForm(string source, string destination, MovementEffect effect, RequiredClass requiredClass, string extra, bool tips, int span)
            {
                Text = "编辑地图连接属性";
                StartPosition = FormStartPosition.CenterParent;
                FormBorderStyle = FormBorderStyle.FixedDialog;
                ClientSize = new Size(470, 285);
                MaximizeBox = false;
                MinimizeBox = false;
                _source.Text = source;
                _destination.Text = destination;
                _effect.DataSource = Enum.GetValues(typeof(MovementEffect));
                _requiredClass.DataSource = Enum.GetValues(typeof(RequiredClass));
                _effect.SelectedItem = effect;
                _requiredClass.SelectedItem = requiredClass;
                _extra.Text = extra;
                _tips.Checked = tips;
                _span.Value = Math.Max(_span.Minimum, Math.Min(_span.Maximum, span));
                TableLayoutPanel layout = new TableLayoutPanel { Dock = DockStyle.Fill, ColumnCount = 2, RowCount = 8, Padding = new Padding(12) };
                layout.ColumnStyles.Add(new ColumnStyle(SizeType.Absolute, 92));
                layout.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 100));
                AddEditorRow(layout, 0, "入口说明", _source);
                AddEditorRow(layout, 1, "出口说明", _destination);
                AddEditorRow(layout, 2, "门点效果", _effect);
                AddEditorRow(layout, 3, "职业限制", _requiredClass);
                AddEditorRow(layout, 4, "特殊信息", _extra);
                AddEditorRow(layout, 5, "关闭延迟", _span);
                layout.Controls.Add(_tips, 1, 6);
                FlowLayoutPanel buttons = new FlowLayoutPanel { Dock = DockStyle.Fill, FlowDirection = FlowDirection.RightToLeft };
                Button ok = new Button { Text = "确定", Font = MapButtonFont, DialogResult = DialogResult.OK };
                Button cancel = new Button { Text = "取消", Font = MapButtonFont, DialogResult = DialogResult.Cancel };
                buttons.Controls.Add(ok);
                buttons.Controls.Add(cancel);
                layout.Controls.Add(buttons, 1, 7);
                Controls.Add(layout);
                AcceptButton = ok;
                CancelButton = cancel;
            }

            private static void AddEditorRow(TableLayoutPanel panel, int row, string caption, Control editor)
            {
                panel.Controls.Add(new Label { Text = caption, Dock = DockStyle.Fill, TextAlign = ContentAlignment.MiddleLeft }, 0, row);
                editor.Dock = DockStyle.Fill;
                panel.Controls.Add(editor, 1, row);
            }
        }
    }
}
