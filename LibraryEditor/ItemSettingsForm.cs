using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Text;
using System.Windows.Forms;
using Library;
using Library.SystemModels;
using MirDB;

namespace LibraryEditor
{
    /// <summary>
    /// 标准 WinForms 物品设置编辑器。
    /// 数据库和客户端素材路径必须由用户明确选择，窗体不会自动打开部署目录。
    /// </summary>
    public sealed partial class ItemSettingsForm : Form
    {
        private sealed class EnumOption
        {
            public object Value;
            public string Text;

            public override string ToString()
            {
                return Text;
            }
        }

        private sealed class SetGroupOption
        {
            public SetGroup Group;

            public override string ToString()
            {
                if (Group == null)
                    return string.Empty;

                string setName = Group.Set == null ? "未命名套装" : Group.Set.SetName;
                return string.Format("{0} / {1} (#{2})", setName, Group.GroupName, Group.Index);
            }
        }

        private enum ItemCategory
        {
            All,
            Weapon,
            Armour,
            Helmet,
            Necklace,
            Bracelet,
            Ring,
            Shoes,
            Shield,
            Fashion,
            Consumable,
            Book,
            Scroll,
            Other,
        }

        private readonly Color _background = Color.FromArgb(36, 36, 36);
        private readonly Color _panel = Color.FromArgb(47, 47, 47);
        private readonly Color _input = Color.FromArgb(58, 58, 58);
        private readonly Color _line = Color.FromArgb(78, 78, 78);
        private readonly Color _accent = Color.FromArgb(55, 125, 210);
        private readonly Color _foreground = Color.FromArgb(235, 235, 235);
        private readonly Dictionary<ItemCategory, Button> _categoryButtons = new Dictionary<ItemCategory, Button>();
        private readonly Dictionary<string, CheckBox> _flagCheckBoxes = new Dictionary<string, CheckBox>();
        private ItemCategory _category = ItemCategory.All;
        private ItemInfoStat _selectedItemStat;
        private SetGroupItem _selectedSetLink;
        private SetGroup _selectedSetGroup;
        private SetInfoStat _selectedSetStat;

        private Session _session;
        private DBCollection<ItemInfo> _itemCollection;
        private DBCollection<ItemInfoStat> _itemStatCollection;
        private DBCollection<SetInfo> _setInfoCollection;
        private DBCollection<SetGroup> _setGroupCollection;
        private DBCollection<SetGroupItem> _setGroupItemCollection;
        private DBCollection<SetInfoStat> _setInfoStatCollection;
        private ItemInfo _currentItem;
        private bool _binding;
        private bool _dirty;

        private BlackDragonLibrary _inventoryLibrary;
        private BlackDragonLibrary _equipLibrary;
        private BlackDragonLibrary _storeItemsLibrary;
        private BlackDragonLibrary _groundLibrary;
        private BlackDragonLibrary _appearanceLibrary;
        private string _appearanceLibraryPath;

        private PreviewCanvas _inventoryCanvas;
        private PreviewCanvas _equipCanvas;
        private PreviewCanvas _appearanceCanvas;
        private PreviewCanvas _smallStoreItemsCanvas;
        private PreviewCanvas _mallStoreItemsCanvas;
        private PreviewCanvas _groundCanvas;

        public ItemSettingsForm()
        {
            InitializeComponent();
            InitializeEditorRuntimeControls();
            InitializeEditorPreviewCanvases();
            InitializeEditorMappings();
            InitializeEditorChoices();
            Shown += ItemSettingsForm_Shown;
            FormClosing += ItemSettingsForm_FormClosing;
        }

        private void InitializeEditorRuntimeControls()
        {
            _itemListView.Columns.Add("ID", 60);
            _itemListView.Columns.Add("物品名称", 170);
            _itemListView.Columns.Add("类型", 90);
            _itemListView.Columns.Add("Image", 70);
            _itemListView.Columns.Add("Shape", 70);
            _itemStatsListView.Columns.Add("属性", 112);
            _itemStatsListView.Columns.Add("值", 42);
            _itemStatsListView.Columns.Add("隐藏", 42);
            _setLinkListView.Columns.Add("关联ID", 70);
            _setLinkListView.Columns.Add("套装", 180);
            _setLinkListView.Columns.Add("搭配", 180);
            _setLinkListView.Columns.Add("触发件数", 90);
            _setStatsListView.Columns.Add("属性", 180);
            _setStatsListView.Columns.Add("数值", 80);
            _setStatsListView.Columns.Add("职业", 160);
            _setStatsListView.Columns.Add("等级", 70);

            selectDatabaseButton.Click += SelectDatabaseButton_Click;
            selectDataButton.Click += SelectDataButton_Click;
            _encryptedCheckBox.CheckedChanged += EditorChanged;
            _refreshButton.Click += RefreshButton_Click;
            _saveButton.Click += SaveButton_Click;
            _itemListView.SelectedIndexChanged += ItemListView_SelectedIndexChanged;
            _itemListView.DoubleClick += ItemListView_DoubleClick;
            _itemNameTextBox.TextChanged += EditorChanged;
            _itemTypeComboBox.SelectedIndexChanged += EditorChanged;
            _weaponTypeComboBox.SelectedIndexChanged += EditorChanged;
            _rarityComboBox.SelectedIndexChanged += EditorChanged;
            _requiredTypeComboBox.SelectedIndexChanged += EditorChanged;
            _requiredClassComboBox.SelectedIndexChanged += EditorChanged;
            _requiredGenderComboBox.SelectedIndexChanged += EditorChanged;
            _effectComboBox.SelectedIndexChanged += EditorChanged;
            _imageNumeric.ValueChanged += EditorChanged;
            _shapeNumeric.ValueChanged += EditorChanged;
            _requiredAmountNumeric.ValueChanged += EditorChanged;
            _buffIconNumeric.ValueChanged += EditorChanged;
            _partCountNumeric.ValueChanged += EditorChanged;
            _durationNumeric.ValueChanged += EditorChanged;
            _durabilityNumeric.ValueChanged += EditorChanged;
            _priceNumeric.ValueChanged += EditorChanged;
            _weightNumeric.ValueChanged += EditorChanged;
            _stackSizeNumeric.ValueChanged += EditorChanged;
            _sellRateNumeric.ValueChanged += EditorChanged;
            flagStartItem.CheckedChanged += EditorChanged;
            flagCanRepair.CheckedChanged += EditorChanged;
            flagCanSell.CheckedChanged += EditorChanged;
            flagCanStore.CheckedChanged += EditorChanged;
            flagCanTreasure.CheckedChanged += EditorChanged;
            flagCanTrade.CheckedChanged += EditorChanged;
            flagNoMake.CheckedChanged += EditorChanged;
            flagCanDrop.CheckedChanged += EditorChanged;
            flagCanDeathDrop.CheckedChanged += EditorChanged;
            flagCanAutoPot.CheckedChanged += EditorChanged;
            _descriptionTextBox.TextChanged += EditorChanged;
            _itemStatsListView.SelectedIndexChanged += ItemStatsListView_SelectedIndexChanged;
            _itemStatComboBox.SelectedIndexChanged += EditorChanged;
            _itemStatAmountNumeric.ValueChanged += EditorChanged;
            addStatButton.Click += ItemStatAddButton_Click;
            modifyStatButton.Click += ItemStatModifyButton_Click;
            deleteStatButton.Click += ItemStatDeleteButton_Click;
            _previewClassComboBox.SelectedIndexChanged += PreviewSettingsChanged;
            _previewGenderComboBox.SelectedIndexChanged += PreviewSettingsChanged;
            _setLinkListView.SelectedIndexChanged += SetLinkListView_SelectedIndexChanged;
            addLinkButton.Click += AddSetLinkButton_Click;
            deleteLinkButton.Click += DeleteSetLinkButton_Click;
            _setNameTextBox.TextChanged += EditorChanged;
            _setGroupNameTextBox.TextChanged += EditorChanged;
            _setDescriptionTextBox.TextChanged += EditorChanged;
            _setRequirementComboBox.SelectedIndexChanged += EditorChanged;
            _setRequiredNumberNumeric.ValueChanged += EditorChanged;
            applySetButton.Click += ApplySetButton_Click;
            _setStatsListView.SelectedIndexChanged += SetStatsListView_SelectedIndexChanged;
            _setStatComboBox.SelectedIndexChanged += EditorChanged;
            _setStatAmountNumeric.ValueChanged += EditorChanged;
            _setStatClassComboBox.SelectedIndexChanged += EditorChanged;
            _setStatLevelNumeric.ValueChanged += EditorChanged;
            applySetStatButton.Click += ApplySetStatButton_Click;
            deleteSetStatButton.Click += DeleteSetStatButton_Click;
        }

        private void InitializeEditorPreviewCanvases()
        {
            _inventoryCanvas = new PreviewCanvas
            {
                Name = "inventoryCanvas",
                Dock = DockStyle.Fill,
                DrawInventoryGrid = true,
                DrawAtTopLeft = true,
            };
            _equipCanvas = new PreviewCanvas
            {
                Name = "equipCanvas",
                Dock = DockStyle.Fill,
            };
            _appearanceCanvas = new PreviewCanvas
            {
                Name = "appearanceCanvas",
                Dock = DockStyle.Fill,
            };
            _smallStoreItemsCanvas = new PreviewCanvas
            {
                Name = "smallStoreItemsCanvas",
                Dock = DockStyle.Fill,
            };
            _mallStoreItemsCanvas = new PreviewCanvas
            {
                Name = "mallStoreItemsCanvas",
                Dock = DockStyle.Fill,
            };
            _groundCanvas = new PreviewCanvas
            {
                Name = "groundCanvas",
                Dock = DockStyle.Fill,
            };

            _inventoryPreviewHostPanel.Controls.Add(_inventoryCanvas);
            _equipPreviewHostPanel.Controls.Add(_equipCanvas);
            _appearancePreviewHostPanel.Controls.Add(_appearanceCanvas);
            _smallStorePreviewHostPanel.Controls.Add(_smallStoreItemsCanvas);
            _mallStorePreviewHostPanel.Controls.Add(_mallStoreItemsCanvas);
            _groundPreviewHostPanel.Controls.Add(_groundCanvas);
        }

        private void InitializeEditorChoices()
        {
            _binding = true;
            try
            {
                AddEnumOptions(_itemTypeComboBox, typeof(ItemType));
                AddEnumOptions(_weaponTypeComboBox, typeof(WeaponType));
                AddEnumOptions(_rarityComboBox, typeof(Rarity));
                AddEnumOptions(_requiredTypeComboBox, typeof(RequiredType));
                AddEnumOptions(_requiredClassComboBox, typeof(RequiredClass));
                AddEnumOptions(_requiredGenderComboBox, typeof(RequiredGender));
                AddEnumOptions(_effectComboBox, typeof(ItemEffect));
                AddEnumOptions(_itemStatComboBox, typeof(Stat));
                AddEnumOptions(_previewClassComboBox, typeof(RequiredClass));
                AddEnumOptions(_previewGenderComboBox, typeof(RequiredGender));
                AddEnumOptions(_setRequirementComboBox, typeof(ItemSetRequirementType));
                AddEnumOptions(_setStatComboBox, typeof(Stat));
                AddEnumOptions(_setStatClassComboBox, typeof(RequiredClass));
                SelectEnum(_itemStatComboBox, Stat.BaseHealth);
                SelectEnum(_previewClassComboBox, RequiredClass.Warrior);
                SelectEnum(_previewGenderComboBox, RequiredGender.Male);
            }
            finally
            {
                _binding = false;
            }
        }

        private void InitializeEditorMappings()
        {
            RegisterCategoryButton(categoryButton0, ItemCategory.All);
            RegisterCategoryButton(categoryButton1, ItemCategory.Weapon);
            RegisterCategoryButton(categoryButton2, ItemCategory.Armour);
            RegisterCategoryButton(categoryButton3, ItemCategory.Helmet);
            RegisterCategoryButton(categoryButton4, ItemCategory.Necklace);
            RegisterCategoryButton(categoryButton5, ItemCategory.Bracelet);
            RegisterCategoryButton(categoryButton6, ItemCategory.Ring);
            RegisterCategoryButton(categoryButton7, ItemCategory.Shoes);
            RegisterCategoryButton(categoryButton8, ItemCategory.Shield);
            RegisterCategoryButton(categoryButton9, ItemCategory.Fashion);
            RegisterCategoryButton(categoryButton10, ItemCategory.Consumable);
            RegisterCategoryButton(categoryButton11, ItemCategory.Book);
            RegisterCategoryButton(categoryButton12, ItemCategory.Scroll);
            RegisterCategoryButton(categoryButton13, ItemCategory.Other);

            _flagCheckBoxes["StartItem"] = flagStartItem;
            _flagCheckBoxes["CanRepair"] = flagCanRepair;
            _flagCheckBoxes["CanSell"] = flagCanSell;
            _flagCheckBoxes["CanStore"] = flagCanStore;
            _flagCheckBoxes["CanTreasure"] = flagCanTreasure;
            _flagCheckBoxes["CanTrade"] = flagCanTrade;
            _flagCheckBoxes["NoMake"] = flagNoMake;
            _flagCheckBoxes["CanDrop"] = flagCanDrop;
            _flagCheckBoxes["CanDeathDrop"] = flagCanDeathDrop;
            _flagCheckBoxes["CanAutoPot"] = flagCanAutoPot;
        }

        private void RegisterCategoryButton(Button button, ItemCategory category)
        {
            button.Tag = category;
            _categoryButtons[category] = button;
        }

        private static void AddEnumOptions(ComboBox combo, Type enumType)
        {
            foreach (object value in Enum.GetValues(enumType))
                combo.Items.Add(new EnumOption { Value = value, Text = GetEnumDescription(value) });
        }

        private void ItemSettingsForm_Shown(object sender, EventArgs e)
        {
            if (!IsDisposed && mainSplit.Width > 720)
                mainSplit.SplitterDistance = Math.Min(470, Math.Max(320, mainSplit.Width / 4));
        }

        private Label CreateLabel(string text, int left, int top, int width, int height)
        {
            return new Label
            {
                Text = text,
                Location = new Point(left, top),
                Size = new Size(width, height),
                AutoEllipsis = true,
                ForeColor = _foreground,
                BackColor = Color.Transparent,
                TextAlign = ContentAlignment.MiddleLeft,
            };
        }

        private TextBox CreatePathTextBox(int left, int top, int width, int height)
        {
            return new TextBox
            {
                Location = new Point(left, top),
                Size = new Size(width, height),
                ReadOnly = true,
                BackColor = _input,
                ForeColor = _foreground,
                BorderStyle = BorderStyle.FixedSingle,
            };
        }

        private Button CreateButton(string text, int left, int top, int width, int height)
        {
            Button button = new Button
            {
                Text = text,
                Location = new Point(left, top),
                Size = new Size(width, height),
                FlatStyle = FlatStyle.Flat,
                BackColor = _input,
                ForeColor = _foreground,
                UseVisualStyleBackColor = false,
            };
            button.FlatAppearance.BorderColor = _line;
            return button;
        }

        private Button CreateInlineButton(string text, int width)
        {
            Button button = CreateButton(text, 0, 0, width, 26);
            button.Margin = new Padding(2);
            return button;
        }

        private GroupBox CreateGroup(string text)
        {
            return new GroupBox
            {
                Text = text,
                Dock = DockStyle.Top,
                AutoSize = true,
                AutoSizeMode = AutoSizeMode.GrowAndShrink,
                BackColor = _panel,
                ForeColor = _foreground,
                Padding = new Padding(8, 24, 8, 8),
                Margin = new Padding(0, 0, 0, 8),
            };
        }

        private void AddCategoryButton(FlowLayoutPanel panel, ItemCategory category, string text)
        {
            Button button = CreateInlineButton(text, 67);
            button.Tag = category;
            button.Height = 27;
            button.Click += CategoryButton_Click;
            panel.Controls.Add(button);
            _categoryButtons[category] = button;
        }

        private GroupBox CreatePreviewGroup()
        {
            GroupBox group = CreateGroup("素材预览");
            group.AutoSize = false;
            group.Height = 356;
            group.MinimumSize = new Size(0, 356);

            TableLayoutPanel previews = new TableLayoutPanel
            {
                Dock = DockStyle.Fill,
                BackColor = _panel,
                ColumnCount = 4,
                RowCount = 1,
                Padding = new Padding(0),
                Margin = new Padding(0),
                GrowStyle = TableLayoutPanelGrowStyle.FixedSize,
            };

            previews.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 20F));
            previews.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 26F));
            previews.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 26F));
            previews.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 28F));

            _inventoryCanvas = new PreviewCanvas
            {
                DrawInventoryGrid = true,
                DrawAtTopLeft = true,
            };
            _equipCanvas = new PreviewCanvas();
            _appearanceCanvas = new PreviewCanvas();
            _smallStoreItemsCanvas = new PreviewCanvas();
            _mallStoreItemsCanvas = new PreviewCanvas();
            _groundCanvas = new PreviewCanvas();

            previews.Controls.Add(CreatePreviewColumn("大背包 (Inventory.Zl) 6x10", _inventoryCanvas), 0, 0);
            previews.Controls.Add(CreatePreviewColumn("内观 (Equip.Zl)", _equipCanvas), 1, 0);
            previews.Controls.Add(CreatePreviewColumn("外观 (Shape计算)", _appearanceCanvas), 2, 0);

            TableLayoutPanel smallPreviews = new TableLayoutPanel
            {
                Dock = DockStyle.Fill,
                BackColor = _panel,
                ColumnCount = 1,
                RowCount = 3,
                Padding = new Padding(2, 0, 0, 0),
                Margin = new Padding(0),
                GrowStyle = TableLayoutPanelGrowStyle.FixedSize,
            };
            smallPreviews.RowStyles.Add(new RowStyle(SizeType.Percent, 33.3333F));
            smallPreviews.RowStyles.Add(new RowStyle(SizeType.Percent, 33.3333F));
            smallPreviews.RowStyles.Add(new RowStyle(SizeType.Percent, 33.3334F));
            smallPreviews.Controls.Add(CreatePreviewColumn("小背包 (StoreItems)", _smallStoreItemsCanvas), 0, 0);
            smallPreviews.Controls.Add(CreatePreviewColumn("商城 (StoreItems)", _mallStoreItemsCanvas), 0, 1);
            smallPreviews.Controls.Add(CreatePreviewColumn("地上 (Ground)", _groundCanvas), 0, 2);
            previews.Controls.Add(smallPreviews, 3, 0);

            group.Controls.Add(previews);

            _imageSizeLabel = new Label
            {
                Dock = DockStyle.Bottom,
                Height = 20,
                ForeColor = Color.LightGray,
                Text = "尺寸：-",
                TextAlign = ContentAlignment.MiddleLeft,
            };
            group.Controls.Add(_imageSizeLabel);
            return group;
        }

        private Panel CreatePreviewColumn(string title, PreviewCanvas canvas)
        {
            Panel column = new Panel
            {
                Dock = DockStyle.Fill,
                BackColor = _panel,
                Margin = new Padding(0),
                Padding = new Padding(2, 0, 2, 0),
            };
            Label titleLabel = new Label
            {
                Dock = DockStyle.Top,
                Height = 24,
                Text = title,
                ForeColor = _foreground,
                TextAlign = ContentAlignment.MiddleCenter,
                AutoEllipsis = false,
                AutoSize = false,
                Font = new Font("Microsoft YaHei UI", 8F),
            };
            canvas.Dock = DockStyle.Fill;
            column.Controls.Add(canvas);
            titleLabel.BringToFront();
            column.Controls.Add(titleLabel);
            return column;
        }

        private TableLayoutPanel CreateItemEditorGroup()
        {
            TableLayoutPanel columns = new TableLayoutPanel
            {
                Dock = DockStyle.Top,
                AutoSize = false,
                Height = 420,
                MinimumSize = new Size(0, 420),
                ColumnCount = 3,
                RowCount = 1,
                BackColor = _background,
                Margin = new Padding(0, 0, 0, 8),
                Padding = new Padding(0),
                GrowStyle = TableLayoutPanelGrowStyle.FixedSize,
            };
            columns.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 55F));
            columns.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 22F));
            columns.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 23F));
            columns.Controls.Add(CreateBasicColumn(), 0, 0);
            columns.Controls.Add(CreateItemStatsColumn(), 1, 0);
            columns.Controls.Add(CreatePreviewSettingsColumn(), 2, 0);
            return columns;
        }

        private GroupBox CreateEditorColumnGroup(string title)
        {
            return new GroupBox
            {
                Text = title,
                Dock = DockStyle.Fill,
                AutoSize = false,
                BackColor = _panel,
                ForeColor = _foreground,
                Padding = new Padding(8, 24, 8, 8),
                Margin = new Padding(0, 0, 6, 0),
            };
        }

        private GroupBox CreateBasicColumn()
        {
            GroupBox group = CreateEditorColumnGroup("基础属性");
            TableLayoutPanel layout = new TableLayoutPanel
            {
                Dock = DockStyle.Fill,
                ColumnCount = 1,
                RowCount = 10,
                BackColor = _panel,
                Padding = new Padding(0),
            };
            for (int i = 0; i < 7; i++)
                layout.RowStyles.Add(new RowStyle(SizeType.Absolute, 28));
            layout.RowStyles.Add(new RowStyle(SizeType.Absolute, 54));
            layout.RowStyles.Add(new RowStyle(SizeType.Absolute, 88));
            layout.RowStyles.Add(new RowStyle(SizeType.Percent, 100F));
            group.Controls.Add(layout);

            _itemNameTextBox = CreateEditorTextBox();
            _itemTypeComboBox = CreateEnumComboBox(typeof(ItemType));
            _weaponTypeComboBox = CreateEnumComboBox(typeof(WeaponType));
            _rarityComboBox = CreateEnumComboBox(typeof(Rarity));
            _imageNumeric = CreateIntegerNumeric();
            _shapeNumeric = CreateIntegerNumeric();
            _effectComboBox = CreateEnumComboBox(typeof(ItemEffect));
            _requiredTypeComboBox = CreateEnumComboBox(typeof(RequiredType));
            _requiredAmountNumeric = CreateIntegerNumeric();
            _requiredClassComboBox = CreateEnumComboBox(typeof(RequiredClass));
            _requiredGenderComboBox = CreateEnumComboBox(typeof(RequiredGender));
            _buffIconNumeric = CreateIntegerNumeric();
            _partCountNumeric = CreateIntegerNumeric();
            _durationNumeric = CreateIntegerNumeric();
            _durabilityNumeric = CreateIntegerNumeric();
            _priceNumeric = CreateIntegerNumeric();
            _weightNumeric = CreateIntegerNumeric();
            _stackSizeNumeric = CreateIntegerNumeric();
            _sellRateNumeric = CreateDecimalNumeric();

            _basicExternalEffectLabel = CreateBasicReadonlyValue("无");
            _basicSetSummaryLabel = CreateBasicReadonlyValue("无");
            _basicInventoryWidthLabel = CreateBasicReadonlyValue("-");
            _basicInventoryHeightLabel = CreateBasicReadonlyValue("-");

            AddBasicFieldRow(layout, 0,
                "名称", _itemNameTextBox,
                "类型", _itemTypeComboBox,
                "图片序号", _imageNumeric);
            AddBasicFieldRow(layout, 1,
                "要求类型", _requiredTypeComboBox,
                "要求参数", _requiredAmountNumeric,
                "外观", _shapeNumeric);
            AddBasicFieldRow(layout, 2,
                "物品特效", _effectComboBox,
                "外部效果", _basicExternalEffectLabel,
                "碎片", _partCountNumeric);
            AddBasicFieldRow(layout, 3,
                "职业要求", _requiredClassComboBox,
                "套装属性", _basicSetSummaryLabel,
                "BUFF图", _buffIconNumeric);
            AddBasicFieldRow(layout, 4,
                "重量", _weightNumeric,
                "持久", _durabilityNumeric,
                "价格", _priceNumeric,
                "出售率", _sellRateNumeric);
            AddBasicFieldRow(layout, 5,
                "装备品质", _rarityComboBox,
                "堆叠", _stackSizeNumeric,
                "物品宽度", _basicInventoryWidthLabel,
                "物品高度", _basicInventoryHeightLabel);
            AddBasicFieldRow(layout, 6,
                "武器类型", _weaponTypeComboBox,
                "要求性别", _requiredGenderComboBox,
                "使用时长", _durationNumeric);

            FlowLayoutPanel flags = new FlowLayoutPanel
            {
                Dock = DockStyle.Fill,
                AutoSize = false,
                BackColor = _panel,
                WrapContents = true,
                Margin = new Padding(0),
                Padding = new Padding(0),
            };
            AddFlag(flags, "StartItem", "新手赠送");
            AddFlag(flags, "CanRepair", "可修理");
            AddFlag(flags, "CanSell", "可买卖");
            AddFlag(flags, "CanStore", "可存储");
            AddFlag(flags, "CanTreasure", "宝箱获得");
            AddFlag(flags, "CanTrade", "可寄售");
            AddFlag(flags, "NoMake", "不可制造");
            AddFlag(flags, "CanDrop", "可丢弃");
            AddFlag(flags, "CanDeathDrop", "死亡掉落");
            AddFlag(flags, "CanAutoPot", "自动物品");
            layout.Controls.Add(flags, 0, 7);

            _descriptionTextBox = new TextBox
            {
                Dock = DockStyle.Fill,
                Multiline = true,
                ScrollBars = ScrollBars.Vertical,
                BackColor = _input,
                ForeColor = _foreground,
                BorderStyle = BorderStyle.FixedSingle,
                Margin = new Padding(0),
            };
            _descriptionTextBox.TextChanged += EditorChanged;
            AddBasicFieldRow(layout, 8, "描述文件", _descriptionTextBox);
            layout.Controls.Add(new Panel
            {
                Dock = DockStyle.Fill,
                BackColor = _panel,
                Margin = new Padding(0),
            }, 0, 9);
            return group;
        }

        private Label CreateBasicReadonlyValue(string text)
        {
            return new Label
            {
                Text = text,
                Dock = DockStyle.Fill,
                BackColor = _input,
                ForeColor = Color.LightGray,
                BorderStyle = BorderStyle.FixedSingle,
                TextAlign = ContentAlignment.MiddleLeft,
                AutoEllipsis = false,
                Padding = new Padding(4, 0, 4, 0),
                Margin = new Padding(2),
            };
        }

        private void AddBasicFieldRow(TableLayoutPanel layout, int row, params object[] fields)
        {
            int pairCount = fields.Length / 2;
            TableLayoutPanel rowPanel = new TableLayoutPanel
            {
                Dock = DockStyle.Fill,
                ColumnCount = pairCount * 2,
                RowCount = 1,
                BackColor = _panel,
                Margin = new Padding(0),
                Padding = new Padding(0),
            };

            for (int i = 0; i < pairCount; i++)
            {
                rowPanel.ColumnStyles.Add(new ColumnStyle(SizeType.Absolute, pairCount >= 4 ? 52 : 58));
                rowPanel.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 100F / pairCount));

                Label label = new Label
                {
                    Text = (string)fields[i * 2],
                    Dock = DockStyle.Fill,
                    Font = pairCount >= 4 ? new Font(Font.FontFamily, 7F, Font.Style) : Font,
                    ForeColor = _foreground,
                    BackColor = Color.Transparent,
                    TextAlign = ContentAlignment.MiddleLeft,
                    AutoEllipsis = false,
                    Margin = new Padding(2, 2, 2, 2),
                };
                Control control = (Control)fields[i * 2 + 1];
                control.Dock = DockStyle.Fill;
                control.Margin = new Padding(2, 2, 4, 2);
                rowPanel.Controls.Add(label, i * 2, 0);
                rowPanel.Controls.Add(control, i * 2 + 1, 0);
            }
            layout.Controls.Add(rowPanel, 0, row);
        }

        private Label CreateSectionCaption(string text)
        {
            return new Label
            {
                Text = text,
                Dock = DockStyle.Fill,
                ForeColor = Color.LightGray,
                BackColor = Color.Transparent,
                TextAlign = ContentAlignment.MiddleLeft,
                AutoEllipsis = false,
                Margin = new Padding(0),
            };
        }

        private void AddFlag(FlowLayoutPanel panel, string key, string text)
        {
            CheckBox checkBox = new CheckBox
            {
                Text = text,
                Tag = key,
                AutoSize = true,
                Margin = new Padding(3, 3, 12, 3),
                ForeColor = _foreground,
                BackColor = Color.Transparent,
            };
            checkBox.CheckedChanged += EditorChanged;
            panel.Controls.Add(checkBox);
            _flagCheckBoxes[key] = checkBox;
        }

        private GroupBox CreateItemStatsColumn()
        {
            GroupBox group = CreateEditorColumnGroup("附加属性");
            TableLayoutPanel table = new TableLayoutPanel
            {
                Dock = DockStyle.Fill,
                ColumnCount = 1,
                RowCount = 2,
                BackColor = _panel,
                Padding = new Padding(0),
            };
            table.RowStyles.Add(new RowStyle(SizeType.Percent, 100F));
            table.RowStyles.Add(new RowStyle(SizeType.Absolute, 66));
            group.Controls.Add(table);

            _itemStatsListView = CreateListView(3);
            _itemStatsListView.Dock = DockStyle.Fill;
            _itemStatsListView.Columns[0].Text = "属性";
            _itemStatsListView.Columns[0].Width = 112;
            _itemStatsListView.Columns[1].Text = "值";
            _itemStatsListView.Columns[1].Width = 42;
            _itemStatsListView.Columns[2].Text = "隐藏";
            _itemStatsListView.Columns[2].Width = 42;
            _itemStatsListView.SelectedIndexChanged += ItemStatsListView_SelectedIndexChanged;
            table.Controls.Add(_itemStatsListView, 0, 0);

            TableLayoutPanel editor = new TableLayoutPanel
            {
                Dock = DockStyle.Fill,
                ColumnCount = 3,
                RowCount = 2,
                BackColor = _panel,
                Padding = new Padding(0),
                Margin = new Padding(0),
            };
            editor.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 48F));
            editor.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 22F));
            editor.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 30F));
            editor.RowStyles.Add(new RowStyle(SizeType.Percent, 50F));
            editor.RowStyles.Add(new RowStyle(SizeType.Percent, 50F));
            table.Controls.Add(editor, 0, 1);

            _itemStatComboBox = CreateEnumComboBox(typeof(Stat));
            _itemStatComboBox.Dock = DockStyle.Fill;
            _itemStatComboBox.Margin = new Padding(2);
            _itemStatAmountNumeric = CreateIntegerNumeric();
            _itemStatAmountNumeric.Dock = DockStyle.Fill;
            _itemStatAmountNumeric.Margin = new Padding(2);
            _itemStatHiddenCheckBox = new CheckBox
            {
                Text = "隐藏",
                Dock = DockStyle.Fill,
                ForeColor = _foreground,
                Margin = new Padding(4, 5, 2, 2),
            };
            editor.Controls.Add(_itemStatComboBox, 0, 0);
            editor.Controls.Add(_itemStatAmountNumeric, 1, 0);
            editor.Controls.Add(_itemStatHiddenCheckBox, 2, 0);

            Button addButton = CreateAccentButton("增加");
            addButton.Click += ItemStatAddButton_Click;
            Button modifyButton = CreateAccentButton("修改");
            modifyButton.Click += ItemStatModifyButton_Click;
            Button deleteButton = CreateAccentButton("删除");
            deleteButton.Click += ItemStatDeleteButton_Click;
            editor.Controls.Add(addButton, 0, 1);
            editor.Controls.Add(modifyButton, 1, 1);
            editor.Controls.Add(deleteButton, 2, 1);
            if (_itemStatComboBox.Items.Count > 0)
            {
                _binding = true;
                _itemStatComboBox.SelectedIndex = 0;
                _binding = false;
            }
            return group;
        }

        private Button CreateAccentButton(string text)
        {
            Button button = CreateInlineButton(text, 54);
            button.Dock = DockStyle.Fill;
            button.BackColor = _accent;
            button.ForeColor = Color.White;
            button.FlatAppearance.BorderColor = _accent;
            button.Margin = new Padding(2);
            return button;
        }

        private GroupBox CreatePreviewSettingsColumn()
        {
            GroupBox group = CreateEditorColumnGroup("预览设置");
            TableLayoutPanel settings = new TableLayoutPanel
            {
                Dock = DockStyle.Fill,
                ColumnCount = 2,
                RowCount = 3,
                BackColor = _panel,
                Padding = new Padding(0),
            };
            settings.ColumnStyles.Add(new ColumnStyle(SizeType.Absolute, 72));
            settings.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 100F));
            for (int i = 0; i < 2; i++)
                settings.RowStyles.Add(new RowStyle(SizeType.Absolute, 24));
            settings.RowStyles.Add(new RowStyle(SizeType.Percent, 100F));
            group.Controls.Add(settings);

            settings.Controls.Add(CreatePreviewLabel("预览职业"), 0, 0);
            _previewClassComboBox = CreatePreviewEnumComboBox(typeof(RequiredClass), RequiredClass.Warrior);
            settings.Controls.Add(_previewClassComboBox, 1, 0);
            settings.Controls.Add(CreatePreviewLabel("预览性别"), 0, 1);
            _previewGenderComboBox = CreatePreviewEnumComboBox(typeof(RequiredGender), RequiredGender.Male);
            settings.Controls.Add(_previewGenderComboBox, 1, 1);

            _descriptionPreviewTextBox = new RichTextBox
            {
                Dock = DockStyle.Fill,
                ReadOnly = true,
                DetectUrls = false,
                ShortcutsEnabled = false,
                TabStop = false,
                BorderStyle = BorderStyle.FixedSingle,
                BackColor = Color.FromArgb(4, 13, 35),
                ForeColor = Color.White,
                Font = new Font("Microsoft YaHei UI", 9F),
                WordWrap = false,
                ScrollBars = RichTextBoxScrollBars.Vertical,
                Margin = new Padding(0, 4, 0, 0),
            };
            settings.Controls.Add(_descriptionPreviewTextBox, 0, 2);
            settings.SetColumnSpan(_descriptionPreviewTextBox, 2);
            return group;
        }

        private Label CreatePreviewLabel(string text)
        {
            return new Label
            {
                Text = text,
                Dock = DockStyle.Fill,
                ForeColor = _foreground,
                TextAlign = ContentAlignment.MiddleLeft,
                AutoEllipsis = false,
                Margin = new Padding(2, 2, 2, 2),
            };
        }

        private ComboBox CreatePreviewEnumComboBox(Type enumType, object defaultValue)
        {
            ComboBox combo = new ComboBox
            {
                Dock = DockStyle.Fill,
                DropDownStyle = ComboBoxStyle.DropDownList,
                BackColor = _input,
                ForeColor = _foreground,
                FlatStyle = FlatStyle.Flat,
                Margin = new Padding(2),
            };
            foreach (object value in Enum.GetValues(enumType))
            {
                combo.Items.Add(new EnumOption
                {
                    Value = value,
                    Text = GetEnumDescription(value),
                });
            }
            SelectEnum(combo, defaultValue);
            combo.SelectedIndexChanged += PreviewSettingsChanged;
            return combo;
        }

        private GroupBox CreateSetGroup()
        {
            GroupBox group = CreateGroup("套装属性和成员");
            TableLayoutPanel table = new TableLayoutPanel
            {
                Dock = DockStyle.Top,
                AutoSize = true,
                ColumnCount = 1,
                RowCount = 5,
                BackColor = _panel,
            };
            group.Controls.Add(table);

            _setLinkListView = CreateListView(4);
            _setLinkListView.Height = 125;
            _setLinkListView.Columns[0].Text = "关联ID";
            _setLinkListView.Columns[0].Width = 70;
            _setLinkListView.Columns[1].Text = "套装";
            _setLinkListView.Columns[1].Width = 180;
            _setLinkListView.Columns[2].Text = "搭配";
            _setLinkListView.Columns[2].Width = 180;
            _setLinkListView.Columns[3].Text = "触发件数";
            _setLinkListView.Columns[3].Width = 90;
            _setLinkListView.SelectedIndexChanged += SetLinkListView_SelectedIndexChanged;
            table.Controls.Add(_setLinkListView, 0, 0);

            FlowLayoutPanel linkEditor = new FlowLayoutPanel
            {
                Dock = DockStyle.Top,
                Height = 34,
                BackColor = _panel,
                WrapContents = false,
            };
            table.Controls.Add(linkEditor, 0, 1);
            _setGroupComboBox = new ComboBox
            {
                Width = 330,
                DropDownStyle = ComboBoxStyle.DropDownList,
                BackColor = _input,
                ForeColor = _foreground,
                FlatStyle = FlatStyle.Flat,
                Margin = new Padding(2),
            };
            Button addLinkButton = CreateInlineButton("关联当前物品", 105);
            addLinkButton.Click += AddSetLinkButton_Click;
            Button deleteLinkButton = CreateInlineButton("移除关联", 90);
            deleteLinkButton.Click += DeleteSetLinkButton_Click;
            linkEditor.Controls.Add(_setGroupComboBox);
            linkEditor.Controls.Add(addLinkButton);
            linkEditor.Controls.Add(deleteLinkButton);

            TableLayoutPanel setFields = CreateFieldTable();
            table.Controls.Add(setFields, 0, 2);
            _setNameTextBox = CreateEditorTextBox();
            _setGroupNameTextBox = CreateEditorTextBox();
            _setDescriptionTextBox = CreateEditorTextBox();
            _setDescriptionTextBox.Multiline = true;
            _setDescriptionTextBox.Height = 50;
            _setRequirementComboBox = CreateEnumComboBox(typeof(ItemSetRequirementType));
            _setRequiredNumberNumeric = CreateIntegerNumeric();
            AddFieldPair(setFields, "套装名称", _setNameTextBox, "搭配名称", _setGroupNameTextBox);
            AddFieldPair(setFields, "触发件数", _setRequiredNumberNumeric, "触发规则", _setRequirementComboBox);
            AddFieldPair(setFields, "套装说明", _setDescriptionTextBox, "", new Panel { Dock = DockStyle.Fill });
            Button applySetButton = CreateInlineButton("应用套装字段", 110);
            applySetButton.Click += ApplySetButton_Click;
            setFields.Controls.Add(applySetButton, 2, setFields.RowCount++);

            _setStatsListView = CreateListView(4);
            _setStatsListView.Height = 120;
            _setStatsListView.Columns[0].Text = "属性";
            _setStatsListView.Columns[0].Width = 180;
            _setStatsListView.Columns[1].Text = "数值";
            _setStatsListView.Columns[1].Width = 80;
            _setStatsListView.Columns[2].Text = "职业";
            _setStatsListView.Columns[2].Width = 160;
            _setStatsListView.Columns[3].Text = "等级";
            _setStatsListView.Columns[3].Width = 70;
            _setStatsListView.SelectedIndexChanged += SetStatsListView_SelectedIndexChanged;
            table.Controls.Add(_setStatsListView, 0, 3);

            FlowLayoutPanel setStatsEditor = new FlowLayoutPanel
            {
                Dock = DockStyle.Top,
                Height = 34,
                BackColor = _panel,
                WrapContents = false,
            };
            table.Controls.Add(setStatsEditor, 0, 4);
            _setStatComboBox = CreateEnumComboBox(typeof(Stat));
            _setStatComboBox.Width = 180;
            _setStatAmountNumeric = CreateIntegerNumeric();
            _setStatAmountNumeric.Width = 80;
            _setStatClassComboBox = CreateEnumComboBox(typeof(RequiredClass));
            _setStatClassComboBox.Width = 160;
            _setStatLevelNumeric = CreateIntegerNumeric();
            _setStatLevelNumeric.Width = 70;
            Button applySetStatButton = CreateInlineButton("新增/应用", 90);
            applySetStatButton.Click += ApplySetStatButton_Click;
            Button deleteSetStatButton = CreateInlineButton("删除", 70);
            deleteSetStatButton.Click += DeleteSetStatButton_Click;
            setStatsEditor.Controls.Add(_setStatComboBox);
            setStatsEditor.Controls.Add(_setStatAmountNumeric);
            setStatsEditor.Controls.Add(_setStatClassComboBox);
            setStatsEditor.Controls.Add(_setStatLevelNumeric);
            setStatsEditor.Controls.Add(applySetStatButton);
            setStatsEditor.Controls.Add(deleteSetStatButton);
            return group;
        }

        private TableLayoutPanel CreateFieldTable()
        {
            TableLayoutPanel table = new TableLayoutPanel
            {
                Dock = DockStyle.Top,
                AutoSize = true,
                ColumnCount = 4,
                RowCount = 0,
                BackColor = _panel,
                Padding = new Padding(0),
            };
            table.ColumnStyles.Add(new ColumnStyle(SizeType.Absolute, 90));
            table.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 50));
            table.ColumnStyles.Add(new ColumnStyle(SizeType.Absolute, 90));
            table.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 50));
            return table;
        }

        private void AddFieldPair(TableLayoutPanel table, string leftLabel, Control leftControl, string rightLabel, Control rightControl)
        {
            int row = table.RowCount++;
            table.RowStyles.Add(new RowStyle(SizeType.AutoSize));
            table.Controls.Add(new Label
            {
                Text = leftLabel,
                AutoSize = true,
                ForeColor = _foreground,
                Margin = new Padding(3, 6, 3, 3),
            }, 0, row);
            leftControl.Dock = DockStyle.Fill;
            leftControl.Margin = new Padding(3);
            table.Controls.Add(leftControl, 1, row);
            table.Controls.Add(new Label
            {
                Text = rightLabel,
                AutoSize = true,
                ForeColor = _foreground,
                Margin = new Padding(3, 6, 3, 3),
            }, 2, row);
            rightControl.Dock = DockStyle.Fill;
            rightControl.Margin = new Padding(3);
            table.Controls.Add(rightControl, 3, row);
        }

        private TextBox CreateEditorTextBox()
        {
            TextBox textBox = new TextBox
            {
                BackColor = _input,
                ForeColor = _foreground,
                BorderStyle = BorderStyle.FixedSingle,
            };
            textBox.TextChanged += EditorChanged;
            return textBox;
        }

        private NumericUpDown CreateIntegerNumeric()
        {
            NumericUpDown numeric = new NumericUpDown
            {
                Minimum = -1000000000,
                Maximum = 1000000000,
                DecimalPlaces = 0,
                BackColor = _input,
                ForeColor = _foreground,
                BorderStyle = BorderStyle.FixedSingle,
                ThousandsSeparator = true,
            };
            numeric.ValueChanged += EditorChanged;
            return numeric;
        }

        private NumericUpDown CreateDecimalNumeric()
        {
            NumericUpDown numeric = new NumericUpDown
            {
                Minimum = -1000000,
                Maximum = 1000000,
                DecimalPlaces = 4,
                Increment = 0.1M,
                BackColor = _input,
                ForeColor = _foreground,
                BorderStyle = BorderStyle.FixedSingle,
                ThousandsSeparator = true,
            };
            numeric.ValueChanged += EditorChanged;
            return numeric;
        }

        private ComboBox CreateEnumComboBox(Type enumType)
        {
            ComboBox combo = new ComboBox
            {
                DropDownStyle = ComboBoxStyle.DropDownList,
                BackColor = _input,
                ForeColor = _foreground,
                FlatStyle = FlatStyle.Flat,
            };
            foreach (object value in Enum.GetValues(enumType))
            {
                combo.Items.Add(new EnumOption
                {
                    Value = value,
                    Text = GetEnumDescription(value),
                });
            }
            combo.SelectedIndexChanged += EditorChanged;
            return combo;
        }

        private ListView CreateListView(int columns)
        {
            ListView list = new ListView
            {
                View = View.Details,
                FullRowSelect = true,
                GridLines = true,
                HideSelection = false,
                MultiSelect = false,
                BackColor = _input,
                ForeColor = _foreground,
                BorderStyle = BorderStyle.FixedSingle,
                Dock = DockStyle.Top,
            };
            for (int i = 0; i < columns; i++)
                list.Columns.Add(string.Empty, 120);
            return list;
        }

        private static string GetEnumDescription(object value)
        {
            FieldInfo field = value.GetType().GetField(value.ToString());
            DescriptionAttribute attribute = field == null ? null : field.GetCustomAttribute<DescriptionAttribute>();
            return attribute == null ? value.ToString() : attribute.Description;
        }

        private void SelectDatabaseButton_Click(object sender, EventArgs e)
        {
            using (OpenFileDialog dialog = new OpenFileDialog())
            {
                dialog.Filter = "System.db|System.db|数据库文件 (*.db)|*.db|所有文件 (*.*)|*.*";
                dialog.Title = "选择要编辑的 System.db（建议选择临时副本）";
                if (File.Exists(_databasePathTextBox.Text))
                    dialog.InitialDirectory = Path.GetDirectoryName(_databasePathTextBox.Text);
                if (dialog.ShowDialog(this) != DialogResult.OK)
                    return;

                _databasePathTextBox.Text = Path.GetFullPath(dialog.FileName);
                SetStatus("已选择数据库；请确认这是临时副本后点击“刷新/加载”。");
            }
        }

        private void SelectDataButton_Click(object sender, EventArgs e)
        {
            using (FolderBrowserDialog dialog = new FolderBrowserDialog())
            {
                dialog.Description = "选择包含 Inventory.Zl、Equip.Zl、StoreItems.Zl、Ground.Zl 的客户端 Data 目录";
                if (Directory.Exists(_dataPathTextBox.Text))
                    dialog.SelectedPath = _dataPathTextBox.Text;
                if (dialog.ShowDialog(this) != DialogResult.OK)
                    return;

                _dataPathTextBox.Text = Path.GetFullPath(dialog.SelectedPath);
                SetStatus("已选择客户端素材目录；点击“刷新/加载”读取数据库和预览资源。");
            }
        }

        private void RefreshButton_Click(object sender, EventArgs e)
        {
            LoadSelectedData();
        }

        private void LoadSelectedData()
        {
            string databaseFile = _databasePathTextBox.Text.Trim();
            if (!File.Exists(databaseFile))
            {
                SetStatus("数据库文件不存在，请先选择 System.db。", true);
                return;
            }

            string root = Path.GetDirectoryName(Path.GetFullPath(databaseFile));
            if (string.IsNullOrEmpty(root) || !Directory.Exists(root))
            {
                SetStatus("数据库目录无效。", true);
                return;
            }

            try
            {
                DisposeSession();
                string backup = Path.Combine(root, "Backup");
                if (!backup.EndsWith(Path.DirectorySeparatorChar.ToString(), StringComparison.Ordinal))
                    backup += Path.DirectorySeparatorChar;
                if (!root.EndsWith(Path.DirectorySeparatorChar.ToString(), StringComparison.Ordinal))
                    root += Path.DirectorySeparatorChar;

                _session = new Session(
                    SessionMode.ServerTool,
                    new[] { typeof(ItemInfo).Assembly },
                    _encryptedCheckBox.Checked,
                    _passwordTextBox.Text,
                    root,
                    backup);
                _session.BackUp = false;
                _session.Output += Session_Output;
                _session.Init();

                _itemCollection = _session.GetCollection<ItemInfo>();
                _itemStatCollection = _session.GetCollection<ItemInfoStat>();
                _setInfoCollection = _session.GetCollection<SetInfo>();
                _setGroupCollection = _session.GetCollection<SetGroup>();
                _setGroupItemCollection = _session.GetCollection<SetGroupItem>();
                _setInfoStatCollection = _session.GetCollection<SetInfoStat>();

                RefreshSetGroupChoices();
                RefreshItemList();
                LoadAssetLibraries();
                _dirty = false;
                SetStatus(string.Format("已加载 {0} 个物品；保存按钮会再次确认目标路径。", _itemCollection.Binding.Count));
            }
            catch (Exception ex)
            {
                DisposeSession();
                SetStatus("加载失败：" + ex.Message, true);
                MessageBox.Show(this, FormatExceptionDetails(ex), "加载数据库失败", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        internal void LoadTestData(string databasePath, string dataPath)
        {
            _databasePathTextBox.Text = databasePath;
            _dataPathTextBox.Text = dataPath;
            LoadSelectedData();

            foreach (ListViewItem row in _itemListView.Items)
            {
                if (row.SubItems.Count < 5 || row.SubItems[3].Text != "1120" || row.SubItems[4].Text != "30")
                    continue;

                row.Selected = true;
                row.Focused = true;
                row.EnsureVisible();
                _itemListView.Select();
                break;
            }
        }

        private static string FormatExceptionDetails(Exception exception)
        {
            StringBuilder details = new StringBuilder(exception.ToString());
            ReflectionTypeLoadException typeLoad = exception as ReflectionTypeLoadException;
            while (typeLoad == null && exception.InnerException != null)
            {
                exception = exception.InnerException;
                typeLoad = exception as ReflectionTypeLoadException;
            }

            if (typeLoad != null && typeLoad.LoaderExceptions != null)
            {
                details.AppendLine();
                details.AppendLine("LoaderExceptions:");
                foreach (Exception loaderException in typeLoad.LoaderExceptions)
                {
                    if (loaderException == null)
                        continue;
                    details.AppendLine("- " + loaderException);
                }
            }
            return details.ToString();
        }

        private void Session_Output(object sender, string message)
        {
            if (IsDisposed)
                return;

            if (InvokeRequired)
            {
                BeginInvoke(new Action<string>(text => SetStatus(text)), message);
                return;
            }
            SetStatus(message);
        }

        private void LoadAssetLibraries()
        {
            ClearPreviewImages();
            DisposeLibraries();

            string dataPath = _dataPathTextBox.Text.Trim();
            if (!Directory.Exists(dataPath))
            {
                SetStatus("数据库已加载，但客户端 Data 目录未选择，预览不可用。", true);
                return;
            }

            try
            {
                _inventoryLibrary = LoadLibrary(dataPath, "Inventory.Zl");
                _equipLibrary = LoadLibrary(dataPath, "Equip.Zl");
                _storeItemsLibrary = LoadLibrary(dataPath, "StoreItems.Zl");
                _groundLibrary = LoadLibrary(dataPath, "Ground.Zl");
                SetStatus("客户端素材已加载；选择物品查看素材和 Shape 静态帧预览。", false);
                BindItem(_currentItem);
            }
            catch (Exception ex)
            {
                DisposeLibraries();
                SetStatus("素材加载失败：" + ex.Message, true);
            }
        }

        private BlackDragonLibrary LoadLibrary(string dataPath, string fileName)
        {
            string path = Path.Combine(dataPath, fileName);
            if (!File.Exists(path))
                return null;
            return new BlackDragonLibrary(path);
        }

        private void DisposeSession()
        {
            ClearPreviewImages();
            DisposeLibraries();
            if (_session != null)
            {
                _session.Output -= Session_Output;
                _session.Dispose();
                _session = null;
            }
            _itemCollection = null;
            _itemStatCollection = null;
            _setInfoCollection = null;
            _setGroupCollection = null;
            _setGroupItemCollection = null;
            _setInfoStatCollection = null;
            _currentItem = null;
        }

        private void DisposeLibraries()
        {
            if (_inventoryLibrary != null) _inventoryLibrary.Dispose();
            if (_equipLibrary != null) _equipLibrary.Dispose();
            if (_storeItemsLibrary != null) _storeItemsLibrary.Dispose();
            if (_groundLibrary != null) _groundLibrary.Dispose();
            DisposeAppearanceLibrary();
            _inventoryLibrary = null;
            _equipLibrary = null;
            _storeItemsLibrary = null;
            _groundLibrary = null;
        }

        private void DisposeAppearanceLibrary()
        {
            if (_appearanceLibrary != null)
                _appearanceLibrary.Dispose();
            _appearanceLibrary = null;
            _appearanceLibraryPath = null;
        }

        private void ClearPreviewImages()
        {
            if (_inventoryCanvas != null) _inventoryCanvas.SetImage(null, "未加载");
            if (_equipCanvas != null) _equipCanvas.SetImage(null, "未加载");
            if (_appearanceCanvas != null) _appearanceCanvas.SetImage(null, "未加载");
            if (_smallStoreItemsCanvas != null) _smallStoreItemsCanvas.SetImage(null, "未加载");
            if (_mallStoreItemsCanvas != null) _mallStoreItemsCanvas.SetImage(null, "未加载");
            if (_groundCanvas != null) _groundCanvas.SetImage(null, "未加载");
            if (_imageSizeLabel != null) _imageSizeLabel.Text = "尺寸：-";
            if (!IsDisposed && !Disposing)
                RefreshItemDescriptionPreview();
        }

        private void RefreshItemList()
        {
            int selectedIndex = _currentItem == null ? -1 : _currentItem.Index;
            _itemListView.BeginUpdate();
            try
            {
                _itemListView.Items.Clear();
                if (_itemCollection == null)
                    return;

                IEnumerable<ItemInfo> items = _itemCollection.Binding;
                items = items.Where(IsInCurrentCategory).OrderBy(x => x.Index);
                foreach (ItemInfo item in items)
                {
                    ListViewItem row = new ListViewItem(item.Index.ToString());
                    row.SubItems.Add(item.ItemName ?? string.Empty);
                    row.SubItems.Add(GetEnumDescription(item.ItemType));
                    row.SubItems.Add(item.Image.ToString());
                    row.SubItems.Add(item.Shape.ToString());
                    row.Tag = item;
                    _itemListView.Items.Add(row);
                    if (item.Index == selectedIndex)
                        row.Selected = true;
                }
            }
            finally
            {
                _itemListView.EndUpdate();
            }

            if (_itemListView.SelectedItems.Count == 0)
                BindItem(null);
        }

        private bool IsInCurrentCategory(ItemInfo item)
        {
            if (_category == ItemCategory.All)
                return true;

            switch (_category)
            {
                case ItemCategory.Weapon: return item.ItemType == ItemType.Weapon;
                case ItemCategory.Armour: return item.ItemType == ItemType.Armour;
                case ItemCategory.Helmet: return item.ItemType == ItemType.Helmet;
                case ItemCategory.Necklace: return item.ItemType == ItemType.Necklace;
                case ItemCategory.Bracelet: return item.ItemType == ItemType.Bracelet;
                case ItemCategory.Ring: return item.ItemType == ItemType.Ring;
                case ItemCategory.Shoes: return item.ItemType == ItemType.Shoes;
                case ItemCategory.Shield: return item.ItemType == ItemType.Shield;
                case ItemCategory.Fashion: return item.ItemType == ItemType.Fashion;
                case ItemCategory.Consumable: return item.ItemType == ItemType.Consumable;
                case ItemCategory.Book: return item.ItemType == ItemType.Book;
                case ItemCategory.Scroll: return item.ItemType == ItemType.Scroll;
                default:
                    return item.ItemType != ItemType.Weapon && item.ItemType != ItemType.Armour &&
                        item.ItemType != ItemType.Helmet && item.ItemType != ItemType.Necklace &&
                        item.ItemType != ItemType.Bracelet && item.ItemType != ItemType.Ring &&
                        item.ItemType != ItemType.Shoes && item.ItemType != ItemType.Shield &&
                        item.ItemType != ItemType.Fashion && item.ItemType != ItemType.Consumable &&
                        item.ItemType != ItemType.Book && item.ItemType != ItemType.Scroll;
            }
        }

        private void CategoryButton_Click(object sender, EventArgs e)
        {
            Button button = sender as Button;
            if (button == null || button.Tag == null)
                return;
            _category = (ItemCategory)button.Tag;
            RefreshCategoryButtonState();
            RefreshItemList();
        }

        private void RefreshCategoryButtonState()
        {
            foreach (KeyValuePair<ItemCategory, Button> pair in _categoryButtons)
                pair.Value.BackColor = pair.Key == _category ? _accent : _input;
        }

        private void ItemListView_SelectedIndexChanged(object sender, EventArgs e)
        {
            ItemInfo item = null;
            if (_itemListView.SelectedItems.Count > 0)
                item = _itemListView.SelectedItems[0].Tag as ItemInfo;
            BindItem(item);
        }

        private void ItemListView_DoubleClick(object sender, EventArgs e)
        {
            if (_itemListView.SelectedItems.Count > 0)
                _itemNameTextBox.Focus();
        }

        private void BindItem(ItemInfo item)
        {
            if (_currentItem != null && _currentItem != item && !_binding)
                ApplyFieldsToItem();
            _currentItem = item;
            _binding = true;
            try
            {
                SetEditorEnabled(item != null);
                if (item == null)
                {
                    ClearEditor();
                    ClearPreviewImages();
                    RefreshItemStatsList();
                    RefreshSetLinkList();
                    return;
                }

                _itemNameTextBox.Text = item.ItemName ?? string.Empty;
                SelectEnum(_itemTypeComboBox, item.ItemType);
                SelectEnum(_weaponTypeComboBox, item.WeaponType);
                SelectEnum(_rarityComboBox, item.Rarity);
                _imageNumeric.Value = Clamp(_imageNumeric, item.Image);
                _shapeNumeric.Value = Clamp(_shapeNumeric, item.Shape);
                SelectEnum(_effectComboBox, item.Effect);
                SelectEnum(_requiredTypeComboBox, item.RequiredType);
                _requiredAmountNumeric.Value = Clamp(_requiredAmountNumeric, item.RequiredAmount);
                SelectEnum(_requiredClassComboBox, item.RequiredClass);
                SelectEnum(_requiredGenderComboBox, item.RequiredGender);
                _buffIconNumeric.Value = Clamp(_buffIconNumeric, item.BuffIcon);
                _partCountNumeric.Value = Clamp(_partCountNumeric, item.PartCount);
                _durationNumeric.Value = Clamp(_durationNumeric, item.Duration);
                _durabilityNumeric.Value = Clamp(_durabilityNumeric, item.Durability);
                _priceNumeric.Value = Clamp(_priceNumeric, item.Price);
                _weightNumeric.Value = Clamp(_weightNumeric, item.Weight);
                _stackSizeNumeric.Value = Clamp(_stackSizeNumeric, item.StackSize);
                _sellRateNumeric.Value = Clamp(_sellRateNumeric, item.SellRate);
                _descriptionTextBox.Text = item.Description ?? string.Empty;
                _flagCheckBoxes["StartItem"].Checked = item.StartItem;
                _flagCheckBoxes["CanRepair"].Checked = item.CanRepair;
                _flagCheckBoxes["CanSell"].Checked = item.CanSell;
                _flagCheckBoxes["CanStore"].Checked = item.CanStore;
                _flagCheckBoxes["CanTreasure"].Checked = item.CanTreasure;
                _flagCheckBoxes["CanTrade"].Checked = item.CanTrade;
                _flagCheckBoxes["NoMake"].Checked = item.NoMake;
                _flagCheckBoxes["CanDrop"].Checked = item.CanDrop;
                _flagCheckBoxes["CanDeathDrop"].Checked = item.CanDeathDrop;
                _flagCheckBoxes["CanAutoPot"].Checked = item.CanAutoPot;
                RefreshItemStatsList();
                RefreshSetLinkList();
                BindPreviews();
            }
            finally
            {
                _binding = false;
            }
        }

        private void ClearEditor()
        {
            _itemNameTextBox.Text = string.Empty;
            _descriptionTextBox.Text = string.Empty;
            _imageSizeLabel.Text = "尺寸：-";
            RefreshItemDescriptionPreview();
        }

        private void SetEditorEnabled(bool enabled)
        {
            _itemNameTextBox.Enabled = enabled;
            _itemTypeComboBox.Enabled = enabled;
            _weaponTypeComboBox.Enabled = enabled;
            _rarityComboBox.Enabled = enabled;
            _imageNumeric.Enabled = enabled;
            _shapeNumeric.Enabled = enabled;
            _effectComboBox.Enabled = enabled;
            _requiredTypeComboBox.Enabled = enabled;
            _requiredAmountNumeric.Enabled = enabled;
            _requiredClassComboBox.Enabled = enabled;
            _requiredGenderComboBox.Enabled = enabled;
            _buffIconNumeric.Enabled = enabled;
            _partCountNumeric.Enabled = enabled;
            _durationNumeric.Enabled = enabled;
            _durabilityNumeric.Enabled = enabled;
            _priceNumeric.Enabled = enabled;
            _weightNumeric.Enabled = enabled;
            _stackSizeNumeric.Enabled = enabled;
            _sellRateNumeric.Enabled = enabled;
            _descriptionTextBox.Enabled = enabled;
            foreach (CheckBox checkBox in _flagCheckBoxes.Values)
                checkBox.Enabled = enabled;
            _itemStatsListView.Enabled = enabled;
            _setLinkListView.Enabled = enabled;
            _setGroupComboBox.Enabled = enabled;
            _setStatsListView.Enabled = enabled;
        }

        private void ApplyFieldsToItem()
        {
            if (_currentItem == null || _binding)
                return;

            _currentItem.ItemName = _itemNameTextBox.Text;
            _currentItem.ItemType = GetEnum<ItemType>(_itemTypeComboBox);
            _currentItem.WeaponType = GetEnum<WeaponType>(_weaponTypeComboBox);
            _currentItem.Rarity = GetEnum<Rarity>(_rarityComboBox);
            _currentItem.Image = (int)_imageNumeric.Value;
            _currentItem.Shape = (int)_shapeNumeric.Value;
            _currentItem.Effect = GetEnum<ItemEffect>(_effectComboBox);
            _currentItem.RequiredType = GetEnum<RequiredType>(_requiredTypeComboBox);
            _currentItem.RequiredAmount = (int)_requiredAmountNumeric.Value;
            _currentItem.RequiredClass = GetEnum<RequiredClass>(_requiredClassComboBox);
            _currentItem.RequiredGender = GetEnum<RequiredGender>(_requiredGenderComboBox);
            _currentItem.BuffIcon = (int)_buffIconNumeric.Value;
            _currentItem.PartCount = (int)_partCountNumeric.Value;
            _currentItem.Duration = (int)_durationNumeric.Value;
            _currentItem.Durability = (int)_durabilityNumeric.Value;
            _currentItem.Price = (int)_priceNumeric.Value;
            _currentItem.Weight = (int)_weightNumeric.Value;
            _currentItem.StackSize = (int)_stackSizeNumeric.Value;
            _currentItem.SellRate = _sellRateNumeric.Value;
            _currentItem.Description = _descriptionTextBox.Text;
            _currentItem.StartItem = _flagCheckBoxes["StartItem"].Checked;
            _currentItem.CanRepair = _flagCheckBoxes["CanRepair"].Checked;
            _currentItem.CanSell = _flagCheckBoxes["CanSell"].Checked;
            _currentItem.CanStore = _flagCheckBoxes["CanStore"].Checked;
            _currentItem.CanTreasure = _flagCheckBoxes["CanTreasure"].Checked;
            _currentItem.CanTrade = _flagCheckBoxes["CanTrade"].Checked;
            _currentItem.NoMake = _flagCheckBoxes["NoMake"].Checked;
            _currentItem.CanDrop = _flagCheckBoxes["CanDrop"].Checked;
            _currentItem.CanDeathDrop = _flagCheckBoxes["CanDeathDrop"].Checked;
            _currentItem.CanAutoPot = _flagCheckBoxes["CanAutoPot"].Checked;
            _currentItem.StatsChanged();
            BindPreviews();
            RefreshItemListRow(_currentItem);
            _dirty = true;
        }

        private void RefreshItemListRow(ItemInfo item)
        {
            foreach (ListViewItem row in _itemListView.Items)
            {
                if (row.Tag != item)
                    continue;
                row.SubItems[1].Text = item.ItemName ?? string.Empty;
                row.SubItems[2].Text = GetEnumDescription(item.ItemType);
                row.SubItems[3].Text = item.Image.ToString();
                row.SubItems[4].Text = item.Shape.ToString();
                break;
            }
        }

        private void BindPreviews()
        {
            if (_currentItem == null)
            {
                ClearPreviewImages();
                return;
            }

            int imageIndex = _currentItem.Image;
            _imageSizeLabel.Text = string.Format("Image={0} | Shape={1}", imageIndex, _currentItem.Shape);
            SetPreview(_inventoryCanvas, _inventoryLibrary, imageIndex, "Inventory.Zl");
            SetPreview(_equipCanvas, _equipLibrary, imageIndex, "Equip.Zl");
            SetPreview(_smallStoreItemsCanvas, _storeItemsLibrary, imageIndex, "StoreItems");
            SetPreview(_mallStoreItemsCanvas, _storeItemsLibrary, imageIndex, "StoreItems");
            SetPreview(_groundCanvas, _groundLibrary, imageIndex, "Ground");
            BindAppearancePreview(_currentItem);
            RefreshItemDescriptionPreview();
        }

        private void PreviewSettingsChanged(object sender, EventArgs e)
        {
            if (!_binding)
                RefreshItemDescriptionPreview();
        }

        private void RefreshItemDescriptionPreview()
        {
            if (_descriptionPreviewTextBox == null || _descriptionPreviewTextBox.IsDisposed)
                return;

            if (_currentItem == null)
            {
                _basicExternalEffectLabel.Text = "无";
                _basicSetSummaryLabel.Text = "无";
                _basicInventoryWidthLabel.Text = "-";
                _basicInventoryHeightLabel.Text = "-";
                _descriptionPreviewTextBox.Clear();
                AppendPreviewLine("未选择物品", Color.DarkGray);
                return;
            }

            ItemType itemType = GetEnum<ItemType>(_itemTypeComboBox);
            RequiredType requiredType = GetEnum<RequiredType>(_requiredTypeComboBox);
            RequiredClass requiredClass = GetEnum<RequiredClass>(_requiredClassComboBox);
            RequiredGender requiredGender = GetEnum<RequiredGender>(_requiredGenderComboBox);
            Rarity rarity = GetEnum<Rarity>(_rarityComboBox);
            RequiredClass previewClass = GetEnum<RequiredClass>(_previewClassComboBox);
            RequiredGender previewGender = GetEnum<RequiredGender>(_previewGenderComboBox);
            int imageWidth = _inventoryCanvas == null ? 0 : _inventoryCanvas.ImageWidth;
            int imageHeight = _inventoryCanvas == null ? 0 : _inventoryCanvas.ImageHeight;

            _basicExternalEffectLabel.Text = "无";
            _basicSetSummaryLabel.Text = GetSetSummary();
            _basicInventoryWidthLabel.Text = imageWidth > 0 ? imageWidth.ToString() : "-";
            _basicInventoryHeightLabel.Text = imageHeight > 0 ? imageHeight.ToString() : "-";

            _descriptionPreviewTextBox.SuspendLayout();
            try
            {
                _descriptionPreviewTextBox.Clear();
                int displayDurability = Math.Max(0, (int)Math.Round(_durabilityNumeric.Value / 1000M));
                AppendPreviewText(_itemNameTextBox.Text, Color.Gold);
                AppendPreviewText(string.Format("    持久: {0}/{0}", displayDurability), Color.White);
                AppendPreviewText(Environment.NewLine, Color.White);
                AppendPreviewLine(GetEnumDescription(itemType), Color.LightSkyBlue);
                AppendPreviewLine(string.Format("重量: {0}", _weightNumeric.Value), Color.LightGray);

                AppendVisibleStatLines(GetVisiblePreviewStats());

                AppendPreviewLine(string.Format("职业限制: {0}",
                    GetRequiredClassPreviewText(requiredClass)),
                    IsPreviewClassAllowed(requiredClass, previewClass) ? Color.LightSkyBlue : Color.Red);
                if (requiredGender != RequiredGender.None)
                {
                    AppendPreviewLine(string.Format("性别限制: {0}", GetEnumDescription(requiredGender)),
                        IsPreviewGenderAllowed(requiredGender, previewGender) ? Color.LightSkyBlue : Color.Red);
                }

                if (_requiredAmountNumeric.Value > 0)
                {
                    string requirement = string.Format("{0}: {1}",
                        GetRequiredTypePreviewText(requiredType), _requiredAmountNumeric.Value);
                    if (rarity > Rarity.Common)
                        requirement += " (" + GetEnumDescription(rarity) + ")";
                    AppendPreviewLine(requirement,
                        rarity > Rarity.Common ? Color.FromArgb(255, 165, 0) : Color.White);
                }

                AppendPreviewLine(string.Format("售价: {0}", _priceNumeric.Value), Color.LightGoldenrodYellow);
                if (_durabilityNumeric.Value > 0 && _stackSizeNumeric.Value == 1 && itemType != ItemType.Book)
                {
                    AppendPreviewLine(_flagCheckBoxes["CanRepair"].Checked ? "可以特殊修理" : "无法修理",
                        _flagCheckBoxes["CanRepair"].Checked ? Color.LightGreen : Color.Red);
                }
            }
            finally
            {
                _descriptionPreviewTextBox.ResumeLayout(true);
                _descriptionPreviewTextBox.SelectionStart = 0;
                _descriptionPreviewTextBox.SelectionLength = 0;
                _descriptionPreviewTextBox.ScrollToCaret();
                _descriptionPreviewTextBox.Refresh();
            }
        }

        private void AppendPreviewLine(string text, Color color)
        {
            AppendPreviewText(text, color);
            AppendPreviewText(Environment.NewLine, Color.White);
        }

        private void AppendPreviewText(string text, Color color)
        {
            if (_descriptionPreviewTextBox == null)
                return;
            text = text ?? string.Empty;
            int start = _descriptionPreviewTextBox.TextLength;
            _descriptionPreviewTextBox.AppendText(text);
            if (text.Length > 0)
            {
                _descriptionPreviewTextBox.Select(start, text.Length);
                _descriptionPreviewTextBox.SelectionColor = color;
            }
        }

        private void AppendVisibleStatLines(Stats stats)
        {
            if (stats == null)
                return;

            foreach (KeyValuePair<Stat, int> pair in stats.Values)
            {
                string text = GetStatPreviewText(stats, pair.Key);
                if (!string.IsNullOrEmpty(text))
                    AppendPreviewLine(text, Color.LightGreen);
            }
        }

        private Stats GetVisiblePreviewStats()
        {
            Stats stats = new Stats();
            if (_currentItem == null || _currentItem.Stats == null || _currentItem.ItemStats == null)
                return stats;

            HashSet<Stat> visibleStats = new HashSet<Stat>();
            foreach (ItemInfoStat itemStat in _currentItem.ItemStats)
            {
                if (!itemStat.ShowHidden)
                    visibleStats.Add(itemStat.Stat);
            }

            foreach (KeyValuePair<Stat, int> pair in _currentItem.Stats.Values)
            {
                if (visibleStats.Contains(pair.Key))
                    stats[pair.Key] = pair.Value;
            }
            return stats;
        }

        private static string GetStatPreviewText(Stats stats, Stat stat)
        {
            FieldInfo field = typeof(Stat).GetField(stat.ToString());
            StatDescription description = field == null ? null : field.GetCustomAttribute<StatDescription>();
            if (description == null)
                return null;

            string title = string.IsNullOrEmpty(description.Title) ? stat.ToString() : description.Title;
            switch (description.Mode)
            {
                case StatType.None:
                case StatType.Shape:
                    return null;
                case StatType.Default:
                    return title + ": " + FormatStatValue(description, stats[stat]);
                case StatType.Min:
                    if (stats[description.MaxStat] != 0)
                        return null;
                    return title + ": " + FormatStatValue(description, stats[stat]);
                case StatType.Max:
                    return title + ": " + FormatStatValue(description,
                        stats[description.MinStat], stats[stat]);
                case StatType.Percent:
                    return title + ": " + FormatStatValue(description, stats[stat] / 100D);
                case StatType.Text:
                    return title;
                case StatType.AttackSpeed:
                    return title + ": " + FormatAttackSpeed(description, stats[stat] / 10D);
                case StatType.Comfort:
                    return title + ": " + FormatStatValue(description, stats[stat] / 10D);
                case StatType.Luck:
                    return (stats[stat] < 0 ? "诅咒" : "幸运") + ": " +
                        FormatStatValue(description, stats[stat]);
                case StatType.Time:
                    return title + ": " + (stats[stat] < 0
                        ? "永久"
                        : TimeSpan.FromSeconds(stats[stat]).ToString());
                case StatType.SpellPower:
                    return GetSpellPowerPreviewText(stats, stat, description);
                case StatType.AttackElement:
                case StatType.ElementResistance:
                    return GetElementPreviewText(stats, stat, description.Mode);
                default:
                    return null;
            }
        }

        private static string GetSpellPowerPreviewText(Stats stats, Stat stat, StatDescription description)
        {
            if (description.MinStat == stat && stats[description.MaxStat] != 0)
                return null;

            bool sameRange = stats[Stat.MinMC] == stats[Stat.MinSC] &&
                stats[Stat.MaxMC] == stats[Stat.MaxSC];
            if (!sameRange)
            {
                return description.Title + ": " + FormatStatValue(description,
                    stats[description.MinStat], stats[stat]);
            }

            if (stat == Stat.MaxSC || (stat == Stat.MinSC && stats[Stat.MinSC] != 0))
            {
                return "全系列魔法: " + FormatStatValue(description,
                    stats[description.MinStat], stats[description.MaxStat]);
            }
            return null;
        }

        private static string GetElementPreviewText(Stats stats, Stat stat, StatType mode)
        {
            List<Stat> elements = new List<Stat>();
            foreach (KeyValuePair<Stat, int> pair in stats.Values)
            {
                StatDescription description = GetStatDescription(pair.Key);
                if (description != null && description.Mode == mode)
                    elements.Add(pair.Key);
            }

            if (elements.Count == 0 || elements[0] != stat)
            {
                if (mode == StatType.AttackElement || elements.Count == 0)
                    return null;
            }

            if (mode == StatType.AttackElement)
            {
                StringBuilder attackResult = new StringBuilder("攻击元素: ");
                for (int i = 0; i < elements.Count; i++)
                {
                    if (i > 0)
                        attackResult.Append(", ");
                    StatDescription description = GetStatDescription(elements[i]);
                    attackResult.Append(description == null ? elements[i].ToString() : description.Title);
                    attackResult.Append("+").Append(stats[elements[i]]);
                }
                return attackResult.ToString();
            }

            bool hasPositive = elements.Any(element => stats[element] > 0);
            bool hasNegative = elements.Any(element => stats[element] < 0);
            bool showPositive;
            if (!hasPositive)
            {
                showPositive = false;
                if (elements[0] != stat)
                    return null;
            }
            else
            {
                if (!hasNegative && elements[0] != stat)
                    return null;
                showPositive = elements[0] == stat;
                if (!showPositive && (elements.Count < 2 || elements[1] != stat))
                    return null;
            }

            StringBuilder result = new StringBuilder(showPositive ? "强元素: " : "弱元素: ");
            bool needComma = false;
            foreach (Stat element in elements)
            {
                if ((stats[element] > 0) != showPositive)
                    continue;
                if (needComma)
                    result.Append(", ");
                StatDescription description = GetStatDescription(element);
                result.Append(description == null ? element.ToString() : description.Title);
                result.Append("x").Append(Math.Abs(stats[element]));
                needComma = true;
            }
            return result.ToString();
        }

        private static StatDescription GetStatDescription(Stat stat)
        {
            FieldInfo field = typeof(Stat).GetField(stat.ToString());
            return field == null ? null : field.GetCustomAttribute<StatDescription>();
        }

        private static string FormatStatValue(StatDescription description, params object[] values)
        {
            if (!string.IsNullOrEmpty(description.Format))
                return string.Format(description.Format, values);
            return string.Join("-", values.Select(value => value == null ? string.Empty : value.ToString()).ToArray());
        }

        private static string FormatAttackSpeed(StatDescription description, double value)
        {
            string result = FormatStatValue(description, value);
            if (value > 0 && !result.StartsWith("+", StringComparison.Ordinal))
                result = "+" + result;
            return result;
        }

        private static string GetRequiredClassPreviewText(RequiredClass requiredClass)
        {
            if (requiredClass == RequiredClass.None)
                return GetEnumDescription(requiredClass);

            RequiredClass[] classes =
            {
                RequiredClass.Warrior,
                RequiredClass.Wizard,
                RequiredClass.Taoist,
                RequiredClass.Assassin,
            };
            StringBuilder result = new StringBuilder();
            foreach (RequiredClass value in classes)
            {
                if (requiredClass != RequiredClass.All &&
                    (requiredClass & value) != value)
                    continue;
                if (result.Length > 0)
                    result.Append("/");
                result.Append(GetEnumDescription(value));
            }
            return result.Length == 0 ? GetEnumDescription(requiredClass) : result.ToString();
        }

        private static bool IsPreviewClassAllowed(RequiredClass requiredClass, RequiredClass previewClass)
        {
            return requiredClass == RequiredClass.None || requiredClass == RequiredClass.All ||
                (requiredClass & previewClass) != 0;
        }

        private static bool IsPreviewGenderAllowed(RequiredGender requiredGender, RequiredGender previewGender)
        {
            return requiredGender == RequiredGender.None || (requiredGender & previewGender) != 0;
        }

        private static string GetRequiredTypePreviewText(RequiredType requiredType)
        {
            switch (requiredType)
            {
                case RequiredType.Level: return "等级要求";
                case RequiredType.MaxLevel: return "最高等级";
                case RequiredType.AC: return "物理防御要求";
                case RequiredType.MR: return "魔法防御要求";
                case RequiredType.DC: return "破坏要求";
                case RequiredType.MC: return "自然系魔法要求";
                case RequiredType.SC: return "灵魂系魔法要求";
                case RequiredType.Health: return "生命值要求";
                case RequiredType.Mana: return "魔法值要求";
                case RequiredType.Accuracy: return "准确要求";
                case RequiredType.Agility: return "敏捷要求";
                case RequiredType.CompanionLevel: return "宠物等级";
                case RequiredType.MaxCompanionLevel: return "宠物最大等级";
                case RequiredType.RebirthLevel: return "转生等级";
                case RequiredType.MaxRebirthLevel: return "转生最大等级";
                case RequiredType.InternalSkill: return "内功等级";
                default: return "未知类型需求";
            }
        }

        private string GetSetSummary()
        {
            if (_setLinkListView == null || _setLinkListView.Items.Count == 0)
                return "无";

            StringBuilder summary = new StringBuilder();
            int count = Math.Min(2, _setLinkListView.Items.Count);
            for (int i = 0; i < count; i++)
            {
                ListViewItem row = _setLinkListView.Items[i];
                string setName = row.SubItems.Count > 1 ? row.SubItems[1].Text : string.Empty;
                string groupName = row.SubItems.Count > 2 ? row.SubItems[2].Text : string.Empty;
                if (summary.Length > 0)
                    summary.Append("；");
                summary.Append(setName);
                if (!string.IsNullOrEmpty(groupName))
                    summary.Append("/").Append(groupName);
            }
            if (_setLinkListView.Items.Count > count)
                summary.Append(" 等").Append(_setLinkListView.Items.Count).Append("项");
            return summary.ToString();
        }

        private void SetPreview(PreviewCanvas canvas, BlackDragonLibrary library, int index, string libraryName)
        {
            if (canvas == null)
                return;
            if (library == null)
            {
                canvas.SetImage(null, libraryName + " 未加载");
                return;
            }

            BlackDragonLibrary.MImage image;
            try
            {
                image = library.GetImage(index);
            }
            catch
            {
                canvas.SetImage(null, string.Format("索引 {0} 无图像", index));
                return;
            }
            if (image == null || image.Image == null)
            {
                canvas.SetImage(null, string.Format("索引 {0} 无图像", index));
                return;
            }

            canvas.SetImage(image.Image, string.Empty);
            if (library == _inventoryLibrary)
                _imageSizeLabel.Text = string.Format("Image={0} | Inventory.Zl：{1}×{2} | Shape={3}",
                    index, image.Width, image.Height, _currentItem == null ? 0 : _currentItem.Shape);
        }

        private void BindAppearancePreview(ItemInfo item)
        {
            string fileName = GetAppearanceLibraryFile(item);
            if (string.IsNullOrEmpty(fileName))
            {
                DisposeAppearanceLibrary();
                _appearanceCanvas.SetImage(null, "暂不支持该 Shape");
                return;
            }

            string dataPath = _dataPathTextBox.Text.Trim();
            string path;
            try
            {
                path = Path.GetFullPath(Path.Combine(dataPath, fileName));
            }
            catch
            {
                DisposeAppearanceLibrary();
                _appearanceCanvas.SetImage(null, "暂不支持该 Shape");
                return;
            }

            if (_appearanceLibrary == null ||
                !string.Equals(_appearanceLibraryPath, path, StringComparison.OrdinalIgnoreCase))
            {
                DisposeAppearanceLibrary();
                if (!File.Exists(path))
                {
                    _appearanceCanvas.SetImage(null, "缺少 " + fileName);
                    return;
                }

                try
                {
                    _appearanceLibrary = new BlackDragonLibrary(path);
                    _appearanceLibraryPath = path;
                }
                catch
                {
                    DisposeAppearanceLibrary();
                    _appearanceCanvas.SetImage(null, "加载失败 " + fileName);
                    return;
                }
            }

            int imageIndex = GetAppearanceImageIndex(item);
            BlackDragonLibrary.MImage image;
            try
            {
                image = _appearanceLibrary.GetImage(imageIndex);
            }
            catch
            {
                image = null;
            }
            if (image == null || image.Image == null)
            {
                _appearanceCanvas.SetImage(null, string.Format("Shape帧 {0} 无图像", imageIndex));
                return;
            }

            _appearanceCanvas.SetImage(image.Image, string.Empty);
        }

        private static string GetAppearanceLibraryFile(ItemInfo item)
        {
            if (item == null || item.ItemType != ItemType.Weapon || item.Shape < 0 || item.Shape >= 1000)
                return null;

            int shapeGroup = item.Shape / 10;
            if (shapeGroup >= 0 && shapeGroup <= 6)
                return "M-Weapon" + (shapeGroup + 1) + ".Zl";
            if (shapeGroup >= 10 && shapeGroup <= 16)
                return "M-Weapon" + shapeGroup + ".Zl";
            return null;
        }

        private static int GetAppearanceImageIndex(ItemInfo item)
        {
            return (item.Shape % 10) * 5000;
        }

        private void RefreshItemStatsList()
        {
            _itemStatsListView.BeginUpdate();
            try
            {
                _itemStatsListView.Items.Clear();
                _selectedItemStat = null;
                if (_currentItem == null || _currentItem.ItemStats == null)
                    return;
                foreach (ItemInfoStat stat in _currentItem.ItemStats)
                {
                    ListViewItem row = new ListViewItem(GetStatDisplayName(stat.Stat));
                    row.SubItems.Add(stat.Amount.ToString());
                    row.SubItems.Add(stat.ShowHidden ? "是" : "否");
                    row.Tag = stat;
                    _itemStatsListView.Items.Add(row);
                }
            }
            finally
            {
                _itemStatsListView.EndUpdate();
            }
        }

        private void SelectItemStat(ItemInfoStat stat)
        {
            if (stat == null)
                return;
            foreach (ListViewItem row in _itemStatsListView.Items)
            {
                if (row.Tag != stat)
                    continue;
                row.Selected = true;
                row.Focused = true;
                row.EnsureVisible();
                break;
            }
        }

        private static string GetStatDisplayName(Stat stat)
        {
            FieldInfo field = typeof(Stat).GetField(stat.ToString());
            StatDescription description = field == null
                ? null
                : (StatDescription)field.GetCustomAttributes(typeof(StatDescription), false).FirstOrDefault();
            if (description == null || string.IsNullOrEmpty(description.Title))
                return GetEnumDescription(stat);
            if (stat.ToString().StartsWith("Min", StringComparison.Ordinal))
                return description.Title + "下限";
            if (stat.ToString().StartsWith("Max", StringComparison.Ordinal))
                return description.Title + "上限";
            return description.Title;
        }

        private void ItemStatsListView_SelectedIndexChanged(object sender, EventArgs e)
        {
            _selectedItemStat = _itemStatsListView.SelectedItems.Count == 0
                ? null
                : _itemStatsListView.SelectedItems[0].Tag as ItemInfoStat;
            if (_selectedItemStat == null)
                return;
            _binding = true;
            try
            {
                SelectEnum(_itemStatComboBox, _selectedItemStat.Stat);
                _itemStatAmountNumeric.Value = Clamp(_itemStatAmountNumeric, _selectedItemStat.Amount);
                _itemStatHiddenCheckBox.Checked = _selectedItemStat.ShowHidden;
            }
            finally
            {
                _binding = false;
            }
        }

        private void ItemStatAddButton_Click(object sender, EventArgs e)
        {
            if (_currentItem == null || _currentItem.ItemStats == null)
                return;

            ItemInfoStat stat = _currentItem.ItemStats.AddNew();
            stat.Stat = GetEnum<Stat>(_itemStatComboBox);
            stat.Amount = (int)_itemStatAmountNumeric.Value;
            stat.ShowHidden = _itemStatHiddenCheckBox.Checked;
            stat.Item = _currentItem;
            _currentItem.StatsChanged();
            _dirty = true;
            RefreshItemStatsList();
            SelectItemStat(stat);
            BindPreviews();
            SetStatus("物品统计属性已增加，尚未写入数据库。", false);
        }

        private void ItemStatModifyButton_Click(object sender, EventArgs e)
        {
            if (_currentItem == null || _currentItem.ItemStats == null)
                return;
            if (_selectedItemStat == null)
            {
                SetStatus("请先选择要修改的物品属性。", true);
                return;
            }

            _selectedItemStat.Stat = GetEnum<Stat>(_itemStatComboBox);
            _selectedItemStat.Amount = (int)_itemStatAmountNumeric.Value;
            _selectedItemStat.ShowHidden = _itemStatHiddenCheckBox.Checked;
            _selectedItemStat.Item = _currentItem;
            _currentItem.StatsChanged();
            _dirty = true;
            ItemInfoStat stat = _selectedItemStat;
            RefreshItemStatsList();
            SelectItemStat(stat);
            BindPreviews();
            SetStatus("物品统计属性已修改，尚未写入数据库。", false);
        }

        private void ItemStatDeleteButton_Click(object sender, EventArgs e)
        {
            if (_selectedItemStat == null || _currentItem == null)
                return;
            if (MessageBox.Show(this, "删除当前物品统计属性？保存按钮确认后才会写入数据库。", "确认删除", MessageBoxButtons.YesNo, MessageBoxIcon.Warning) != DialogResult.Yes)
                return;
            _currentItem.ItemStats.Remove(_selectedItemStat);
            if (_itemStatCollection != null)
                _itemStatCollection.DeleteFriends(_selectedItemStat);
            _selectedItemStat = null;
            _currentItem.StatsChanged();
            _dirty = true;
            RefreshItemStatsList();
            BindPreviews();
            SetStatus("物品统计属性已删除，尚未写入数据库。", false);
        }

        private void RefreshSetGroupChoices()
        {
            _setGroupComboBox.Items.Clear();
            if (_setGroupCollection == null)
                return;
            foreach (SetGroup group in _setGroupCollection.Binding.OrderBy(x => x.Index))
                _setGroupComboBox.Items.Add(new SetGroupOption { Group = group });
            if (_setGroupComboBox.Items.Count > 0)
                _setGroupComboBox.SelectedIndex = 0;
        }

        private void RefreshSetLinkList()
        {
            _setLinkListView.BeginUpdate();
            try
            {
                _setLinkListView.Items.Clear();
                _selectedSetLink = null;
                _selectedSetGroup = null;
                if (_currentItem == null || _setGroupItemCollection == null)
                {
                    ClearSetFields();
                    return;
                }

                foreach (SetGroupItem link in _setGroupItemCollection.Binding
                    .Where(x => x.SetGroupItemInfo != null && x.SetGroupItemInfo.Index == _currentItem.Index)
                    .OrderBy(x => x.Index))
                {
                    ListViewItem row = new ListViewItem(link.Index.ToString());
                    row.SubItems.Add(link.SetGroupInfo == null || link.SetGroupInfo.Set == null ? "未命名套装" : link.SetGroupInfo.Set.SetName);
                    row.SubItems.Add(link.SetGroupInfo == null ? string.Empty : link.SetGroupInfo.GroupName);
                    row.SubItems.Add(link.SetGroupInfo == null ? string.Empty : link.SetGroupInfo.RequiredNumItems.ToString());
                    row.Tag = link;
                    _setLinkListView.Items.Add(row);
                }
            }
            finally
            {
                _setLinkListView.EndUpdate();
            }
            if (_setLinkListView.SelectedItems.Count == 0)
                ClearSetFields();
        }

        private void SetLinkListView_SelectedIndexChanged(object sender, EventArgs e)
        {
            _selectedSetLink = _setLinkListView.SelectedItems.Count == 0
                ? null
                : _setLinkListView.SelectedItems[0].Tag as SetGroupItem;
            _selectedSetGroup = _selectedSetLink == null ? null : _selectedSetLink.SetGroupInfo;
            BindSetGroupFields();
        }

        private void AddSetLinkButton_Click(object sender, EventArgs e)
        {
            if (_currentItem == null || _setGroupItemCollection == null || _setGroupComboBox.SelectedItem == null)
                return;
            SetGroup group = ((SetGroupOption)_setGroupComboBox.SelectedItem).Group;
            bool exists = _setGroupItemCollection.Binding.Any(x => x.SetGroupItemInfo != null &&
                x.SetGroupItemInfo.Index == _currentItem.Index && x.SetGroupInfo == group);
            if (exists)
            {
                SetStatus("当前物品已经关联此套装搭配。", true);
                return;
            }

            SetGroupItem link = _setGroupItemCollection.CreateNewObject();
            link.SetGroupInfo = group;
            link.SetGroupItemInfo = _currentItem;
            _dirty = true;
            RefreshSetLinkList();
            SelectSetLink(link);
            RefreshItemDescriptionPreview();
        }

        private void DeleteSetLinkButton_Click(object sender, EventArgs e)
        {
            if (_selectedSetLink == null || _setGroupItemCollection == null)
                return;
            if (MessageBox.Show(this, "移除当前物品和套装搭配的关联？保存按钮确认后才会写入数据库。", "确认移除", MessageBoxButtons.YesNo, MessageBoxIcon.Warning) != DialogResult.Yes)
                return;
            if (_selectedSetLink.SetGroupInfo != null && _selectedSetLink.SetGroupInfo.SetGroupItems != null)
                _selectedSetLink.SetGroupInfo.SetGroupItems.Remove(_selectedSetLink);
            _setGroupItemCollection.DeleteFriends(_selectedSetLink);
            _selectedSetLink = null;
            _selectedSetGroup = null;
            _dirty = true;
            RefreshSetLinkList();
            RefreshItemDescriptionPreview();
        }

        private void SelectSetLink(SetGroupItem link)
        {
            foreach (ListViewItem row in _setLinkListView.Items)
            {
                if (row.Tag != link)
                    continue;
                row.Selected = true;
                row.Focused = true;
                row.EnsureVisible();
                break;
            }
        }

        private void ClearSetFields()
        {
            _binding = true;
            try
            {
                _setNameTextBox.Text = string.Empty;
                _setGroupNameTextBox.Text = string.Empty;
                _setDescriptionTextBox.Text = string.Empty;
                _setStatsListView.Items.Clear();
                _selectedSetStat = null;
            }
            finally
            {
                _binding = false;
            }
        }

        private void BindSetGroupFields()
        {
            _binding = true;
            try
            {
                if (_selectedSetGroup == null)
                {
                    ClearSetFields();
                    return;
                }
                SetInfo set = _selectedSetGroup.Set;
                _setNameTextBox.Text = set == null ? string.Empty : set.SetName ?? string.Empty;
                _setDescriptionTextBox.Text = set == null ? string.Empty : set.SetDescription ?? string.Empty;
                _setGroupNameTextBox.Text = _selectedSetGroup.GroupName ?? string.Empty;
                SelectEnum(_setRequirementComboBox, _selectedSetGroup.SetRequirement);
                _setRequiredNumberNumeric.Value = Clamp(_setRequiredNumberNumeric, _selectedSetGroup.RequiredNumItems);
                RefreshSetStatsList();
            }
            finally
            {
                _binding = false;
            }
        }

        private void ApplySetButton_Click(object sender, EventArgs e)
        {
            if (_selectedSetGroup == null)
                return;
            if (_selectedSetGroup.Set == null && _setInfoCollection != null)
                _selectedSetGroup.Set = _setInfoCollection.CreateNewObject();
            if (_selectedSetGroup.Set != null)
            {
                _selectedSetGroup.Set.SetName = _setNameTextBox.Text;
                _selectedSetGroup.Set.SetDescription = _setDescriptionTextBox.Text;
            }
            _selectedSetGroup.GroupName = _setGroupNameTextBox.Text;
            _selectedSetGroup.SetRequirement = GetEnum<ItemSetRequirementType>(_setRequirementComboBox);
            _selectedSetGroup.RequiredNumItems = (int)_setRequiredNumberNumeric.Value;
            _dirty = true;
            RefreshSetGroupChoices();
            RefreshSetLinkList();
            RefreshItemDescriptionPreview();
            SetStatus("套装字段已修改，尚未写入数据库。", false);
        }

        private void RefreshSetStatsList()
        {
            _setStatsListView.BeginUpdate();
            try
            {
                _setStatsListView.Items.Clear();
                _selectedSetStat = null;
                if (_selectedSetGroup == null || _selectedSetGroup.GroupStats == null)
                    return;
                foreach (SetInfoStat stat in _selectedSetGroup.GroupStats)
                {
                    ListViewItem row = new ListViewItem(GetEnumDescription(stat.Stat));
                    row.SubItems.Add(stat.Amount.ToString());
                    row.SubItems.Add(GetEnumDescription(stat.Class));
                    row.SubItems.Add(stat.Level.ToString());
                    row.Tag = stat;
                    _setStatsListView.Items.Add(row);
                }
            }
            finally
            {
                _setStatsListView.EndUpdate();
            }
        }

        private void SetStatsListView_SelectedIndexChanged(object sender, EventArgs e)
        {
            _selectedSetStat = _setStatsListView.SelectedItems.Count == 0
                ? null
                : _setStatsListView.SelectedItems[0].Tag as SetInfoStat;
            if (_selectedSetStat == null)
                return;
            _binding = true;
            try
            {
                SelectEnum(_setStatComboBox, _selectedSetStat.Stat);
                _setStatAmountNumeric.Value = Clamp(_setStatAmountNumeric, _selectedSetStat.Amount);
                SelectEnum(_setStatClassComboBox, _selectedSetStat.Class);
                _setStatLevelNumeric.Value = Clamp(_setStatLevelNumeric, _selectedSetStat.Level);
            }
            finally
            {
                _binding = false;
            }
        }

        private void ApplySetStatButton_Click(object sender, EventArgs e)
        {
            if (_selectedSetGroup == null || _selectedSetGroup.GroupStats == null)
                return;
            SetInfoStat stat = _selectedSetStat;
            if (stat == null)
                stat = _selectedSetGroup.GroupStats.AddNew();
            stat.Stat = GetEnum<Stat>(_setStatComboBox);
            stat.Amount = (int)_setStatAmountNumeric.Value;
            stat.Class = GetEnum<RequiredClass>(_setStatClassComboBox);
            stat.Level = (int)_setStatLevelNumeric.Value;
            stat.Group = _selectedSetGroup;
            _dirty = true;
            RefreshSetStatsList();
        }

        private void DeleteSetStatButton_Click(object sender, EventArgs e)
        {
            if (_selectedSetStat == null || _selectedSetGroup == null)
                return;
            if (MessageBox.Show(this, "删除当前套装属性？保存按钮确认后才会写入数据库。", "确认删除", MessageBoxButtons.YesNo, MessageBoxIcon.Warning) != DialogResult.Yes)
                return;
            if (_selectedSetStat.Group != null && _selectedSetStat.Group.GroupStats != null)
                _selectedSetStat.Group.GroupStats.Remove(_selectedSetStat);
            else
                _selectedSetGroup.GroupStats.Remove(_selectedSetStat);
            if (_setInfoStatCollection != null)
                _setInfoStatCollection.DeleteFriends(_selectedSetStat);
            _selectedSetStat = null;
            _dirty = true;
            RefreshSetStatsList();
        }

        private void SaveButton_Click(object sender, EventArgs e)
        {
            if (_session == null || _itemCollection == null)
            {
                SetStatus("尚未加载数据库，不能保存。", true);
                return;
            }

            ApplyFieldsToItem();
            ApplySetGroupFields();
            if (!_dirty)
            {
                SetStatus("没有待保存的修改。", false);
                return;
            }

            string target = _session.SystemPath;
            DialogResult result = MessageBox.Show(
                this,
                string.Format("确定保存当前修改？\n\n目标数据库：{0}\n\n只保存此数据库，不会自动保存客户端素材。", target),
                "确认保存",
                MessageBoxButtons.YesNo,
                MessageBoxIcon.Warning,
                MessageBoxDefaultButton.Button2);
            if (result != DialogResult.Yes)
                return;

            try
            {
                _session.Save(true, SessionMode.ServerTool);
                _dirty = false;
                SetStatus("数据库保存完成：" + target, false);
            }
            catch (Exception ex)
            {
                SetStatus("保存失败：" + ex.Message, true);
                MessageBox.Show(this, ex.ToString(), "保存数据库失败", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void ApplySetGroupFields()
        {
            if (_selectedSetGroup == null || _binding)
                return;
            if (_selectedSetGroup.Set == null &&
                (string.IsNullOrEmpty(_setNameTextBox.Text) && string.IsNullOrEmpty(_setDescriptionTextBox.Text)))
                return;
            if (_selectedSetGroup.Set == null && _setInfoCollection != null)
                _selectedSetGroup.Set = _setInfoCollection.CreateNewObject();
            if (_selectedSetGroup.Set != null)
            {
                _selectedSetGroup.Set.SetName = _setNameTextBox.Text;
                _selectedSetGroup.Set.SetDescription = _setDescriptionTextBox.Text;
            }
            _selectedSetGroup.GroupName = _setGroupNameTextBox.Text;
            _selectedSetGroup.SetRequirement = GetEnum<ItemSetRequirementType>(_setRequirementComboBox);
            _selectedSetGroup.RequiredNumItems = (int)_setRequiredNumberNumeric.Value;
        }

        private void EditorChanged(object sender, EventArgs e)
        {
            if (!_binding)
            {
                _dirty = true;
                RefreshItemDescriptionPreview();
            }
        }

        private void SetStatus(string text, bool error = false)
        {
            _statusLabel.Text = text ?? string.Empty;
            _statusLabel.ForeColor = error ? Color.Orange : Color.LightGray;
        }

        private void ItemSettingsForm_FormClosing(object sender, FormClosingEventArgs e)
        {
            if (_dirty)
            {
                DialogResult result = MessageBox.Show(
                    this,
                    "存在尚未保存的修改。关闭将丢弃这些修改，是否继续？",
                    "未保存修改",
                    MessageBoxButtons.YesNo,
                    MessageBoxIcon.Warning,
                    MessageBoxDefaultButton.Button2);
                if (result != DialogResult.Yes)
                {
                    e.Cancel = true;
                    return;
                }
            }
            DisposeSession();
        }

        private static decimal Clamp(NumericUpDown numeric, decimal value)
        {
            if (value < numeric.Minimum) return numeric.Minimum;
            if (value > numeric.Maximum) return numeric.Maximum;
            return value;
        }

        private static void SelectEnum<T>(ComboBox combo, T value)
        {
            for (int i = 0; i < combo.Items.Count; i++)
            {
                EnumOption option = combo.Items[i] as EnumOption;
                if (option != null && option.Value.Equals(value))
                {
                    combo.SelectedIndex = i;
                    return;
                }
            }
            if (combo.Items.Count > 0)
                combo.SelectedIndex = 0;
        }

        private static T GetEnum<T>(ComboBox combo)
        {
            EnumOption option = combo.SelectedItem as EnumOption;
            return option == null ? default(T) : (T)option.Value;
        }

        protected override void Dispose(bool disposing)
        {
            if (disposing)
            {
                DisposeSession();
            }
            base.Dispose(disposing);
        }

        private void _itemTypeComboBox_SelectedIndexChanged(object sender, EventArgs e)
        {

        }
    }
}
