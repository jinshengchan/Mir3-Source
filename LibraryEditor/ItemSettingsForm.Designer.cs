using System;
using System.Drawing;
using System.Windows.Forms;

namespace LibraryEditor
{
    public sealed partial class ItemSettingsForm
    {
        private TextBox _databasePathTextBox;
        private TextBox _dataPathTextBox;
        private CheckBox _encryptedCheckBox;
        private TextBox _passwordTextBox;
        private Button _saveButton;
        private Button _refreshButton;
        private Label _statusLabel;

        private ListView _itemListView;

        private TextBox _itemNameTextBox;
        private ComboBox _itemTypeComboBox;
        private ComboBox _weaponTypeComboBox;
        private ComboBox _requiredTypeComboBox;
        private ComboBox _requiredClassComboBox;
        private ComboBox _requiredGenderComboBox;
        private ComboBox _effectComboBox;
        private ComboBox _rarityComboBox;
        private NumericUpDown _requiredAmountNumeric;
        private NumericUpDown _shapeNumeric;
        private NumericUpDown _imageNumeric;
        private NumericUpDown _durabilityNumeric;
        private NumericUpDown _priceNumeric;
        private NumericUpDown _weightNumeric;
        private NumericUpDown _stackSizeNumeric;
        private NumericUpDown _sellRateNumeric;
        private NumericUpDown _buffIconNumeric;
        private NumericUpDown _partCountNumeric;
        private NumericUpDown _durationNumeric;
        private TextBox _descriptionTextBox;

        private ComboBox _previewClassComboBox;
        private ComboBox _previewGenderComboBox;
        private RichTextBox _descriptionPreviewTextBox;

        private Panel _inventoryPreviewHostPanel;
        private Panel _equipPreviewHostPanel;
        private Panel _appearancePreviewHostPanel;
        private Panel _smallStorePreviewHostPanel;
        private Panel _mallStorePreviewHostPanel;
        private Panel _groundPreviewHostPanel;
        private Label _imageSizeLabel;
        private Label _basicExternalEffectLabel;
        private Label _basicSetSummaryLabel;
        private Label _basicInventoryWidthLabel;
        private Label _basicInventoryHeightLabel;

        private ListView _itemStatsListView;
        private ComboBox _itemStatComboBox;
        private NumericUpDown _itemStatAmountNumeric;
        private CheckBox _itemStatHiddenCheckBox;

        private ListView _setLinkListView;
        private ComboBox _setGroupComboBox;
        private TextBox _setNameTextBox;
        private TextBox _setDescriptionTextBox;
        private TextBox _setGroupNameTextBox;
        private ComboBox _setRequirementComboBox;
        private NumericUpDown _setRequiredNumberNumeric;
        private ListView _setStatsListView;
        private ComboBox _setStatComboBox;
        private ComboBox _setStatClassComboBox;
        private NumericUpDown _setStatAmountNumeric;
        private NumericUpDown _setStatLevelNumeric;

        private Button addLinkButton;
        private Button addStatButton;
        private Panel appearanceColumn;
        private Label appearanceTitle;
        private Button applySetButton;
        private Button applySetStatButton;
        private GroupBox basicGroup;
        private TableLayoutPanel basicLayout;
        private FlowLayoutPanel categories;
        private Label dataLabel;
        private Label databaseLabel;
        private Button deleteLinkButton;
        private Button deleteSetStatButton;
        private Button deleteStatButton;
        private Label descriptionLabel;
        private TableLayoutPanel descriptionRow;
        private TableLayoutPanel editorColumns;
        private Panel editorHost;
        private TableLayoutPanel editorLayout;
        private Label emptySetLabel;
        private Panel emptySetPanel;
        private Panel equipColumn;
        private Label equipTitle;
        private FlowLayoutPanel flags;
        private Panel groundColumn;
        private Label groundTitle;
        private Panel header;
        private Panel inventoryColumn;
        private Label inventoryTitle;
        private FlowLayoutPanel linkEditor;
        private Panel listPanel;
        private SplitContainer mainSplit;
        private Panel mallStoreColumn;
        private Label mallStoreTitle;
        private Button modifyStatButton;
        private Label passwordLabel;
        private Label previewClassLabel;
        private Label previewGenderLabel;
        private GroupBox previewGroup;
        private GroupBox previewSettingsGroup;
        private TableLayoutPanel previews;
        private Button selectDataButton;
        private Button selectDatabaseButton;
        private Label setDescriptionLabel;
        private TableLayoutPanel setFields;
        private GroupBox setGroup;
        private Label setGroupNameLabel;
        private Label setNameLabel;
        private Label setRequiredNumberLabel;
        private Label setRequirementLabel;
        private FlowLayoutPanel setStatsEditor;
        private TableLayoutPanel setTable;
        private TableLayoutPanel settings;
        private TableLayoutPanel smallPreviews;
        private Panel smallStoreColumn;
        private Label smallStoreTitle;
        private TableLayoutPanel statsEditor;
        private GroupBox statsGroup;
        private TableLayoutPanel statsTable;
        private Button categoryButton0;
        private Button categoryButton1;
        private Button categoryButton2;
        private Button categoryButton3;
        private Button categoryButton4;
        private Button categoryButton5;
        private Button categoryButton6;
        private Button categoryButton7;
        private Button categoryButton8;
        private Button categoryButton9;
        private Button categoryButton10;
        private Button categoryButton11;
        private Button categoryButton12;
        private Button categoryButton13;
        private TableLayoutPanel basicRow0;
        private Label basicLabel0_0;
        private Label basicLabel0_1;
        private Label basicLabel0_2;
        private TableLayoutPanel basicRow1;
        private Label basicLabel1_0;
        private Label basicLabel1_1;
        private Label basicLabel1_2;
        private TableLayoutPanel basicRow2;
        private Label basicLabel2_0;
        private Label basicLabel2_1;
        private Label basicLabel2_2;
        private TableLayoutPanel basicRow3;
        private Label basicLabel3_0;
        private Label basicLabel3_1;
        private Label basicLabel3_2;
        private TableLayoutPanel basicRow4;
        private Label basicLabel4_0;
        private Label basicLabel4_1;
        private Label basicLabel4_2;
        private Label basicLabel4_3;
        private TableLayoutPanel basicRow5;
        private Label basicLabel5_0;
        private Label basicLabel5_1;
        private Label basicLabel5_2;
        private Label basicLabel5_3;
        private TableLayoutPanel basicRow6;
        private Label basicLabel6_0;
        private Label basicLabel6_1;
        private Label basicLabel6_2;
        private CheckBox flagStartItem;
        private CheckBox flagCanRepair;
        private CheckBox flagCanSell;
        private CheckBox flagCanStore;
        private CheckBox flagCanTreasure;
        private CheckBox flagCanTrade;
        private CheckBox flagNoMake;
        private CheckBox flagCanDrop;
        private CheckBox flagCanDeathDrop;
        private CheckBox flagCanAutoPot;
        private Panel basicSpacer;
        private void InitializeComponent()
        {
            this.header = new System.Windows.Forms.Panel();
            this.databaseLabel = new System.Windows.Forms.Label();
            this._databasePathTextBox = new System.Windows.Forms.TextBox();
            this.selectDatabaseButton = new System.Windows.Forms.Button();
            this.dataLabel = new System.Windows.Forms.Label();
            this._dataPathTextBox = new System.Windows.Forms.TextBox();
            this.selectDataButton = new System.Windows.Forms.Button();
            this._encryptedCheckBox = new System.Windows.Forms.CheckBox();
            this.passwordLabel = new System.Windows.Forms.Label();
            this._passwordTextBox = new System.Windows.Forms.TextBox();
            this._refreshButton = new System.Windows.Forms.Button();
            this._saveButton = new System.Windows.Forms.Button();
            this._statusLabel = new System.Windows.Forms.Label();
            this.mainSplit = new System.Windows.Forms.SplitContainer();
            this.listPanel = new System.Windows.Forms.Panel();
            this._itemListView = new System.Windows.Forms.ListView();
            this.categories = new System.Windows.Forms.FlowLayoutPanel();
            this.categoryButton0 = new System.Windows.Forms.Button();
            this.categoryButton1 = new System.Windows.Forms.Button();
            this.categoryButton2 = new System.Windows.Forms.Button();
            this.categoryButton3 = new System.Windows.Forms.Button();
            this.categoryButton4 = new System.Windows.Forms.Button();
            this.categoryButton5 = new System.Windows.Forms.Button();
            this.categoryButton6 = new System.Windows.Forms.Button();
            this.categoryButton7 = new System.Windows.Forms.Button();
            this.categoryButton8 = new System.Windows.Forms.Button();
            this.categoryButton9 = new System.Windows.Forms.Button();
            this.categoryButton10 = new System.Windows.Forms.Button();
            this.categoryButton11 = new System.Windows.Forms.Button();
            this.categoryButton12 = new System.Windows.Forms.Button();
            this.categoryButton13 = new System.Windows.Forms.Button();
            this.editorHost = new System.Windows.Forms.Panel();
            this.editorLayout = new System.Windows.Forms.TableLayoutPanel();
            this.previewGroup = new System.Windows.Forms.GroupBox();
            this.previews = new System.Windows.Forms.TableLayoutPanel();
            this.inventoryColumn = new System.Windows.Forms.Panel();
            this._inventoryPreviewHostPanel = new System.Windows.Forms.Panel();
            this.inventoryTitle = new System.Windows.Forms.Label();
            this.equipColumn = new System.Windows.Forms.Panel();
            this._equipPreviewHostPanel = new System.Windows.Forms.Panel();
            this.equipTitle = new System.Windows.Forms.Label();
            this.appearanceColumn = new System.Windows.Forms.Panel();
            this._appearancePreviewHostPanel = new System.Windows.Forms.Panel();
            this.appearanceTitle = new System.Windows.Forms.Label();
            this.smallPreviews = new System.Windows.Forms.TableLayoutPanel();
            this.smallStoreColumn = new System.Windows.Forms.Panel();
            this._smallStorePreviewHostPanel = new System.Windows.Forms.Panel();
            this.smallStoreTitle = new System.Windows.Forms.Label();
            this.mallStoreColumn = new System.Windows.Forms.Panel();
            this._mallStorePreviewHostPanel = new System.Windows.Forms.Panel();
            this.mallStoreTitle = new System.Windows.Forms.Label();
            this.groundColumn = new System.Windows.Forms.Panel();
            this._groundPreviewHostPanel = new System.Windows.Forms.Panel();
            this.groundTitle = new System.Windows.Forms.Label();
            this._imageSizeLabel = new System.Windows.Forms.Label();
            this.editorColumns = new System.Windows.Forms.TableLayoutPanel();
            this.basicGroup = new System.Windows.Forms.GroupBox();
            this.basicLayout = new System.Windows.Forms.TableLayoutPanel();
            this.basicRow0 = new System.Windows.Forms.TableLayoutPanel();
            this.basicLabel0_0 = new System.Windows.Forms.Label();
            this._itemNameTextBox = new System.Windows.Forms.TextBox();
            this.basicLabel0_1 = new System.Windows.Forms.Label();
            this._itemTypeComboBox = new System.Windows.Forms.ComboBox();
            this.basicLabel0_2 = new System.Windows.Forms.Label();
            this._imageNumeric = new System.Windows.Forms.NumericUpDown();
            this.basicRow1 = new System.Windows.Forms.TableLayoutPanel();
            this.basicLabel1_0 = new System.Windows.Forms.Label();
            this._requiredTypeComboBox = new System.Windows.Forms.ComboBox();
            this.basicLabel1_1 = new System.Windows.Forms.Label();
            this._requiredAmountNumeric = new System.Windows.Forms.NumericUpDown();
            this.basicLabel1_2 = new System.Windows.Forms.Label();
            this._shapeNumeric = new System.Windows.Forms.NumericUpDown();
            this.basicRow2 = new System.Windows.Forms.TableLayoutPanel();
            this.basicLabel2_0 = new System.Windows.Forms.Label();
            this._effectComboBox = new System.Windows.Forms.ComboBox();
            this.basicLabel2_1 = new System.Windows.Forms.Label();
            this._basicExternalEffectLabel = new System.Windows.Forms.Label();
            this.basicLabel2_2 = new System.Windows.Forms.Label();
            this._partCountNumeric = new System.Windows.Forms.NumericUpDown();
            this.basicRow3 = new System.Windows.Forms.TableLayoutPanel();
            this.basicLabel3_0 = new System.Windows.Forms.Label();
            this._requiredClassComboBox = new System.Windows.Forms.ComboBox();
            this.basicLabel3_1 = new System.Windows.Forms.Label();
            this._basicSetSummaryLabel = new System.Windows.Forms.Label();
            this.basicLabel3_2 = new System.Windows.Forms.Label();
            this._buffIconNumeric = new System.Windows.Forms.NumericUpDown();
            this.basicRow4 = new System.Windows.Forms.TableLayoutPanel();
            this.basicLabel4_0 = new System.Windows.Forms.Label();
            this._weightNumeric = new System.Windows.Forms.NumericUpDown();
            this.basicLabel4_1 = new System.Windows.Forms.Label();
            this._durabilityNumeric = new System.Windows.Forms.NumericUpDown();
            this.basicLabel4_2 = new System.Windows.Forms.Label();
            this._priceNumeric = new System.Windows.Forms.NumericUpDown();
            this.basicLabel4_3 = new System.Windows.Forms.Label();
            this._sellRateNumeric = new System.Windows.Forms.NumericUpDown();
            this.basicRow5 = new System.Windows.Forms.TableLayoutPanel();
            this.basicLabel5_0 = new System.Windows.Forms.Label();
            this._rarityComboBox = new System.Windows.Forms.ComboBox();
            this.basicLabel5_1 = new System.Windows.Forms.Label();
            this._stackSizeNumeric = new System.Windows.Forms.NumericUpDown();
            this.basicLabel5_2 = new System.Windows.Forms.Label();
            this._basicInventoryWidthLabel = new System.Windows.Forms.Label();
            this.basicLabel5_3 = new System.Windows.Forms.Label();
            this._basicInventoryHeightLabel = new System.Windows.Forms.Label();
            this.basicRow6 = new System.Windows.Forms.TableLayoutPanel();
            this.basicLabel6_0 = new System.Windows.Forms.Label();
            this._weaponTypeComboBox = new System.Windows.Forms.ComboBox();
            this.basicLabel6_1 = new System.Windows.Forms.Label();
            this._requiredGenderComboBox = new System.Windows.Forms.ComboBox();
            this.basicLabel6_2 = new System.Windows.Forms.Label();
            this._durationNumeric = new System.Windows.Forms.NumericUpDown();
            this.flags = new System.Windows.Forms.FlowLayoutPanel();
            this.flagStartItem = new System.Windows.Forms.CheckBox();
            this.flagCanRepair = new System.Windows.Forms.CheckBox();
            this.flagCanSell = new System.Windows.Forms.CheckBox();
            this.flagCanStore = new System.Windows.Forms.CheckBox();
            this.flagCanTreasure = new System.Windows.Forms.CheckBox();
            this.flagCanTrade = new System.Windows.Forms.CheckBox();
            this.flagNoMake = new System.Windows.Forms.CheckBox();
            this.flagCanDrop = new System.Windows.Forms.CheckBox();
            this.flagCanDeathDrop = new System.Windows.Forms.CheckBox();
            this.flagCanAutoPot = new System.Windows.Forms.CheckBox();
            this.descriptionRow = new System.Windows.Forms.TableLayoutPanel();
            this.descriptionLabel = new System.Windows.Forms.Label();
            this._descriptionTextBox = new System.Windows.Forms.TextBox();
            this.basicSpacer = new System.Windows.Forms.Panel();
            this.statsGroup = new System.Windows.Forms.GroupBox();
            this.statsTable = new System.Windows.Forms.TableLayoutPanel();
            this._itemStatsListView = new System.Windows.Forms.ListView();
            this.statsEditor = new System.Windows.Forms.TableLayoutPanel();
            this._itemStatComboBox = new System.Windows.Forms.ComboBox();
            this._itemStatAmountNumeric = new System.Windows.Forms.NumericUpDown();
            this._itemStatHiddenCheckBox = new System.Windows.Forms.CheckBox();
            this.addStatButton = new System.Windows.Forms.Button();
            this.modifyStatButton = new System.Windows.Forms.Button();
            this.deleteStatButton = new System.Windows.Forms.Button();
            this.previewSettingsGroup = new System.Windows.Forms.GroupBox();
            this.settings = new System.Windows.Forms.TableLayoutPanel();
            this.previewClassLabel = new System.Windows.Forms.Label();
            this._previewClassComboBox = new System.Windows.Forms.ComboBox();
            this.previewGenderLabel = new System.Windows.Forms.Label();
            this._previewGenderComboBox = new System.Windows.Forms.ComboBox();
            this._descriptionPreviewTextBox = new System.Windows.Forms.RichTextBox();
            this.setGroup = new System.Windows.Forms.GroupBox();
            this.setTable = new System.Windows.Forms.TableLayoutPanel();
            this._setLinkListView = new System.Windows.Forms.ListView();
            this.linkEditor = new System.Windows.Forms.FlowLayoutPanel();
            this._setGroupComboBox = new System.Windows.Forms.ComboBox();
            this.addLinkButton = new System.Windows.Forms.Button();
            this.deleteLinkButton = new System.Windows.Forms.Button();
            this.setFields = new System.Windows.Forms.TableLayoutPanel();
            this.setNameLabel = new System.Windows.Forms.Label();
            this._setNameTextBox = new System.Windows.Forms.TextBox();
            this.setGroupNameLabel = new System.Windows.Forms.Label();
            this._setGroupNameTextBox = new System.Windows.Forms.TextBox();
            this.setRequiredNumberLabel = new System.Windows.Forms.Label();
            this._setRequiredNumberNumeric = new System.Windows.Forms.NumericUpDown();
            this.setRequirementLabel = new System.Windows.Forms.Label();
            this._setRequirementComboBox = new System.Windows.Forms.ComboBox();
            this.setDescriptionLabel = new System.Windows.Forms.Label();
            this._setDescriptionTextBox = new System.Windows.Forms.TextBox();
            this.emptySetLabel = new System.Windows.Forms.Label();
            this.emptySetPanel = new System.Windows.Forms.Panel();
            this.applySetButton = new System.Windows.Forms.Button();
            this._setStatsListView = new System.Windows.Forms.ListView();
            this.setStatsEditor = new System.Windows.Forms.FlowLayoutPanel();
            this._setStatComboBox = new System.Windows.Forms.ComboBox();
            this._setStatAmountNumeric = new System.Windows.Forms.NumericUpDown();
            this._setStatClassComboBox = new System.Windows.Forms.ComboBox();
            this._setStatLevelNumeric = new System.Windows.Forms.NumericUpDown();
            this.applySetStatButton = new System.Windows.Forms.Button();
            this.deleteSetStatButton = new System.Windows.Forms.Button();
            this.header.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.mainSplit)).BeginInit();
            this.mainSplit.Panel1.SuspendLayout();
            this.mainSplit.Panel2.SuspendLayout();
            this.mainSplit.SuspendLayout();
            this.listPanel.SuspendLayout();
            this.categories.SuspendLayout();
            this.editorHost.SuspendLayout();
            this.editorLayout.SuspendLayout();
            this.previewGroup.SuspendLayout();
            this.previews.SuspendLayout();
            this.inventoryColumn.SuspendLayout();
            this.equipColumn.SuspendLayout();
            this.appearanceColumn.SuspendLayout();
            this.smallPreviews.SuspendLayout();
            this.smallStoreColumn.SuspendLayout();
            this.mallStoreColumn.SuspendLayout();
            this.groundColumn.SuspendLayout();
            this.editorColumns.SuspendLayout();
            this.basicGroup.SuspendLayout();
            this.basicLayout.SuspendLayout();
            this.basicRow0.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this._imageNumeric)).BeginInit();
            this.basicRow1.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this._requiredAmountNumeric)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this._shapeNumeric)).BeginInit();
            this.basicRow2.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this._partCountNumeric)).BeginInit();
            this.basicRow3.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this._buffIconNumeric)).BeginInit();
            this.basicRow4.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this._weightNumeric)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this._durabilityNumeric)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this._priceNumeric)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this._sellRateNumeric)).BeginInit();
            this.basicRow5.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this._stackSizeNumeric)).BeginInit();
            this.basicRow6.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this._durationNumeric)).BeginInit();
            this.flags.SuspendLayout();
            this.descriptionRow.SuspendLayout();
            this.statsGroup.SuspendLayout();
            this.statsTable.SuspendLayout();
            this.statsEditor.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this._itemStatAmountNumeric)).BeginInit();
            this.previewSettingsGroup.SuspendLayout();
            this.settings.SuspendLayout();
            this.setGroup.SuspendLayout();
            this.setTable.SuspendLayout();
            this.linkEditor.SuspendLayout();
            this.setFields.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this._setRequiredNumberNumeric)).BeginInit();
            this.setStatsEditor.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this._setStatAmountNumeric)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this._setStatLevelNumeric)).BeginInit();
            this.SuspendLayout();
            // 
            // header
            // 
            this.header.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(47)))), ((int)(((byte)(47)))), ((int)(((byte)(47)))));
            this.header.Controls.Add(this.databaseLabel);
            this.header.Controls.Add(this._databasePathTextBox);
            this.header.Controls.Add(this.selectDatabaseButton);
            this.header.Controls.Add(this.dataLabel);
            this.header.Controls.Add(this._dataPathTextBox);
            this.header.Controls.Add(this.selectDataButton);
            this.header.Controls.Add(this._encryptedCheckBox);
            this.header.Controls.Add(this.passwordLabel);
            this.header.Controls.Add(this._passwordTextBox);
            this.header.Controls.Add(this._refreshButton);
            this.header.Controls.Add(this._saveButton);
            this.header.Controls.Add(this._statusLabel);
            this.header.Dock = System.Windows.Forms.DockStyle.Top;
            this.header.Location = new System.Drawing.Point(0, 0);
            this.header.Name = "header";
            this.header.Padding = new System.Windows.Forms.Padding(10);
            this.header.Size = new System.Drawing.Size(1434, 104);
            this.header.TabIndex = 0;
            // 
            // databaseLabel
            // 
            this.databaseLabel.AutoEllipsis = true;
            this.databaseLabel.BackColor = System.Drawing.Color.Transparent;
            this.databaseLabel.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this.databaseLabel.Location = new System.Drawing.Point(0, 3);
            this.databaseLabel.Name = "databaseLabel";
            this.databaseLabel.Size = new System.Drawing.Size(75, 24);
            this.databaseLabel.TabIndex = 0;
            this.databaseLabel.Text = "数据库文件";
            this.databaseLabel.TextAlign = System.Drawing.ContentAlignment.MiddleLeft;
            // 
            // _databasePathTextBox
            // 
            this._databasePathTextBox.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(58)))), ((int)(((byte)(58)))), ((int)(((byte)(58)))));
            this._databasePathTextBox.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this._databasePathTextBox.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this._databasePathTextBox.Location = new System.Drawing.Point(82, 0);
            this._databasePathTextBox.Name = "_databasePathTextBox";
            this._databasePathTextBox.ReadOnly = true;
            this._databasePathTextBox.Size = new System.Drawing.Size(620, 23);
            this._databasePathTextBox.TabIndex = 1;
            // 
            // selectDatabaseButton
            // 
            this.selectDatabaseButton.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(58)))), ((int)(((byte)(58)))), ((int)(((byte)(58)))));
            this.selectDatabaseButton.FlatAppearance.BorderColor = System.Drawing.Color.FromArgb(((int)(((byte)(78)))), ((int)(((byte)(78)))), ((int)(((byte)(78)))));
            this.selectDatabaseButton.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.selectDatabaseButton.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this.selectDatabaseButton.Location = new System.Drawing.Point(710, 0);
            this.selectDatabaseButton.Name = "selectDatabaseButton";
            this.selectDatabaseButton.Size = new System.Drawing.Size(125, 28);
            this.selectDatabaseButton.TabIndex = 2;
            this.selectDatabaseButton.Text = "选择 System.db";
            this.selectDatabaseButton.UseVisualStyleBackColor = false;
            // 
            // dataLabel
            // 
            this.dataLabel.AutoEllipsis = true;
            this.dataLabel.BackColor = System.Drawing.Color.Transparent;
            this.dataLabel.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this.dataLabel.Location = new System.Drawing.Point(0, 37);
            this.dataLabel.Name = "dataLabel";
            this.dataLabel.Size = new System.Drawing.Size(75, 24);
            this.dataLabel.TabIndex = 3;
            this.dataLabel.Text = "客户端 Data";
            this.dataLabel.TextAlign = System.Drawing.ContentAlignment.MiddleLeft;
            // 
            // _dataPathTextBox
            // 
            this._dataPathTextBox.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(58)))), ((int)(((byte)(58)))), ((int)(((byte)(58)))));
            this._dataPathTextBox.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this._dataPathTextBox.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this._dataPathTextBox.Location = new System.Drawing.Point(82, 34);
            this._dataPathTextBox.Name = "_dataPathTextBox";
            this._dataPathTextBox.ReadOnly = true;
            this._dataPathTextBox.Size = new System.Drawing.Size(620, 23);
            this._dataPathTextBox.TabIndex = 4;
            // 
            // selectDataButton
            // 
            this.selectDataButton.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(58)))), ((int)(((byte)(58)))), ((int)(((byte)(58)))));
            this.selectDataButton.FlatAppearance.BorderColor = System.Drawing.Color.FromArgb(((int)(((byte)(78)))), ((int)(((byte)(78)))), ((int)(((byte)(78)))));
            this.selectDataButton.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.selectDataButton.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this.selectDataButton.Location = new System.Drawing.Point(710, 34);
            this.selectDataButton.Name = "selectDataButton";
            this.selectDataButton.Size = new System.Drawing.Size(125, 28);
            this.selectDataButton.TabIndex = 5;
            this.selectDataButton.Text = "选择素材目录";
            this.selectDataButton.UseVisualStyleBackColor = false;
            // 
            // _encryptedCheckBox
            // 
            this._encryptedCheckBox.AutoSize = true;
            this._encryptedCheckBox.BackColor = System.Drawing.Color.Transparent;
            this._encryptedCheckBox.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this._encryptedCheckBox.Location = new System.Drawing.Point(855, 3);
            this._encryptedCheckBox.Name = "_encryptedCheckBox";
            this._encryptedCheckBox.Size = new System.Drawing.Size(99, 21);
            this._encryptedCheckBox.TabIndex = 6;
            this._encryptedCheckBox.Text = "数据库已加密";
            this._encryptedCheckBox.UseVisualStyleBackColor = false;
            // 
            // passwordLabel
            // 
            this.passwordLabel.AutoEllipsis = true;
            this.passwordLabel.BackColor = System.Drawing.Color.Transparent;
            this.passwordLabel.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this.passwordLabel.Location = new System.Drawing.Point(855, 38);
            this.passwordLabel.Name = "passwordLabel";
            this.passwordLabel.Size = new System.Drawing.Size(68, 24);
            this.passwordLabel.TabIndex = 7;
            this.passwordLabel.Text = "临时密码";
            this.passwordLabel.TextAlign = System.Drawing.ContentAlignment.MiddleLeft;
            // 
            // _passwordTextBox
            // 
            this._passwordTextBox.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(58)))), ((int)(((byte)(58)))), ((int)(((byte)(58)))));
            this._passwordTextBox.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this._passwordTextBox.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this._passwordTextBox.Location = new System.Drawing.Point(925, 35);
            this._passwordTextBox.Name = "_passwordTextBox";
            this._passwordTextBox.Size = new System.Drawing.Size(145, 23);
            this._passwordTextBox.TabIndex = 8;
            this._passwordTextBox.UseSystemPasswordChar = true;
            // 
            // _refreshButton
            // 
            this._refreshButton.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(58)))), ((int)(((byte)(58)))), ((int)(((byte)(58)))));
            this._refreshButton.FlatAppearance.BorderColor = System.Drawing.Color.FromArgb(((int)(((byte)(78)))), ((int)(((byte)(78)))), ((int)(((byte)(78)))));
            this._refreshButton.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this._refreshButton.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this._refreshButton.Location = new System.Drawing.Point(1085, 0);
            this._refreshButton.Name = "_refreshButton";
            this._refreshButton.Size = new System.Drawing.Size(105, 28);
            this._refreshButton.TabIndex = 9;
            this._refreshButton.Text = "刷新/加载";
            this._refreshButton.UseVisualStyleBackColor = false;
            // 
            // _saveButton
            // 
            this._saveButton.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(55)))), ((int)(((byte)(125)))), ((int)(((byte)(210)))));
            this._saveButton.FlatAppearance.BorderColor = System.Drawing.Color.FromArgb(((int)(((byte)(78)))), ((int)(((byte)(78)))), ((int)(((byte)(78)))));
            this._saveButton.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this._saveButton.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this._saveButton.Location = new System.Drawing.Point(1085, 34);
            this._saveButton.Name = "_saveButton";
            this._saveButton.Size = new System.Drawing.Size(105, 28);
            this._saveButton.TabIndex = 10;
            this._saveButton.Text = "保存数据库";
            this._saveButton.UseVisualStyleBackColor = false;
            // 
            // _statusLabel
            // 
            this._statusLabel.AutoEllipsis = true;
            this._statusLabel.ForeColor = System.Drawing.Color.LightGray;
            this._statusLabel.Location = new System.Drawing.Point(10, 70);
            this._statusLabel.Name = "_statusLabel";
            this._statusLabel.Size = new System.Drawing.Size(1250, 24);
            this._statusLabel.TabIndex = 12;
            this._statusLabel.Text = "请选择数据库文件和客户端 Data 目录；未选择前不会访问数据库。";
            // 
            // mainSplit
            // 
            this.mainSplit.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(78)))), ((int)(((byte)(78)))), ((int)(((byte)(78)))));
            this.mainSplit.Dock = System.Windows.Forms.DockStyle.Fill;
            this.mainSplit.Location = new System.Drawing.Point(0, 104);
            this.mainSplit.Name = "mainSplit";
            // 
            // mainSplit.Panel1
            // 
            this.mainSplit.Panel1.Controls.Add(this.listPanel);
            // 
            // mainSplit.Panel2
            // 
            this.mainSplit.Panel2.Controls.Add(this.editorHost);
            this.mainSplit.Size = new System.Drawing.Size(1434, 837);
            this.mainSplit.SplitterDistance = 360;
            this.mainSplit.TabIndex = 1;
            // 
            // listPanel
            // 
            this.listPanel.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(36)))), ((int)(((byte)(36)))), ((int)(((byte)(36)))));
            this.listPanel.Controls.Add(this._itemListView);
            this.listPanel.Controls.Add(this.categories);
            this.listPanel.Dock = System.Windows.Forms.DockStyle.Fill;
            this.listPanel.Location = new System.Drawing.Point(0, 0);
            this.listPanel.Name = "listPanel";
            this.listPanel.Padding = new System.Windows.Forms.Padding(8);
            this.listPanel.Size = new System.Drawing.Size(360, 837);
            this.listPanel.TabIndex = 0;
            // 
            // _itemListView
            // 
            this._itemListView.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(58)))), ((int)(((byte)(58)))), ((int)(((byte)(58)))));
            this._itemListView.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this._itemListView.Dock = System.Windows.Forms.DockStyle.Fill;
            this._itemListView.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this._itemListView.FullRowSelect = true;
            this._itemListView.GridLines = true;
            this._itemListView.HideSelection = false;
            this._itemListView.Location = new System.Drawing.Point(8, 100);
            this._itemListView.MultiSelect = false;
            this._itemListView.Name = "_itemListView";
            this._itemListView.Size = new System.Drawing.Size(344, 729);
            this._itemListView.TabIndex = 1;
            this._itemListView.UseCompatibleStateImageBehavior = false;
            this._itemListView.View = System.Windows.Forms.View.Details;
            // 
            // categories
            // 
            this.categories.AutoScroll = true;
            this.categories.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(36)))), ((int)(((byte)(36)))), ((int)(((byte)(36)))));
            this.categories.Controls.Add(this.categoryButton0);
            this.categories.Controls.Add(this.categoryButton1);
            this.categories.Controls.Add(this.categoryButton2);
            this.categories.Controls.Add(this.categoryButton3);
            this.categories.Controls.Add(this.categoryButton4);
            this.categories.Controls.Add(this.categoryButton5);
            this.categories.Controls.Add(this.categoryButton6);
            this.categories.Controls.Add(this.categoryButton7);
            this.categories.Controls.Add(this.categoryButton8);
            this.categories.Controls.Add(this.categoryButton9);
            this.categories.Controls.Add(this.categoryButton10);
            this.categories.Controls.Add(this.categoryButton11);
            this.categories.Controls.Add(this.categoryButton12);
            this.categories.Controls.Add(this.categoryButton13);
            this.categories.Dock = System.Windows.Forms.DockStyle.Top;
            this.categories.Location = new System.Drawing.Point(8, 8);
            this.categories.Name = "categories";
            this.categories.Padding = new System.Windows.Forms.Padding(0, 0, 0, 4);
            this.categories.Size = new System.Drawing.Size(344, 92);
            this.categories.TabIndex = 0;
            // 
            // categoryButton0
            // 
            this.categoryButton0.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(58)))), ((int)(((byte)(58)))), ((int)(((byte)(58)))));
            this.categoryButton0.FlatAppearance.BorderColor = System.Drawing.Color.FromArgb(((int)(((byte)(78)))), ((int)(((byte)(78)))), ((int)(((byte)(78)))));
            this.categoryButton0.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.categoryButton0.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this.categoryButton0.Location = new System.Drawing.Point(2, 2);
            this.categoryButton0.Margin = new System.Windows.Forms.Padding(2);
            this.categoryButton0.Name = "categoryButton0";
            this.categoryButton0.Size = new System.Drawing.Size(67, 27);
            this.categoryButton0.TabIndex = 0;
            this.categoryButton0.Text = "全部";
            this.categoryButton0.UseVisualStyleBackColor = false;
            // 
            // categoryButton1
            // 
            this.categoryButton1.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(58)))), ((int)(((byte)(58)))), ((int)(((byte)(58)))));
            this.categoryButton1.FlatAppearance.BorderColor = System.Drawing.Color.FromArgb(((int)(((byte)(78)))), ((int)(((byte)(78)))), ((int)(((byte)(78)))));
            this.categoryButton1.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.categoryButton1.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this.categoryButton1.Location = new System.Drawing.Point(73, 2);
            this.categoryButton1.Margin = new System.Windows.Forms.Padding(2);
            this.categoryButton1.Name = "categoryButton1";
            this.categoryButton1.Size = new System.Drawing.Size(67, 27);
            this.categoryButton1.TabIndex = 1;
            this.categoryButton1.Text = "武器";
            this.categoryButton1.UseVisualStyleBackColor = false;
            // 
            // categoryButton2
            // 
            this.categoryButton2.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(58)))), ((int)(((byte)(58)))), ((int)(((byte)(58)))));
            this.categoryButton2.FlatAppearance.BorderColor = System.Drawing.Color.FromArgb(((int)(((byte)(78)))), ((int)(((byte)(78)))), ((int)(((byte)(78)))));
            this.categoryButton2.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.categoryButton2.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this.categoryButton2.Location = new System.Drawing.Point(144, 2);
            this.categoryButton2.Margin = new System.Windows.Forms.Padding(2);
            this.categoryButton2.Name = "categoryButton2";
            this.categoryButton2.Size = new System.Drawing.Size(67, 27);
            this.categoryButton2.TabIndex = 2;
            this.categoryButton2.Text = "衣服";
            this.categoryButton2.UseVisualStyleBackColor = false;
            // 
            // categoryButton3
            // 
            this.categoryButton3.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(58)))), ((int)(((byte)(58)))), ((int)(((byte)(58)))));
            this.categoryButton3.FlatAppearance.BorderColor = System.Drawing.Color.FromArgb(((int)(((byte)(78)))), ((int)(((byte)(78)))), ((int)(((byte)(78)))));
            this.categoryButton3.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.categoryButton3.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this.categoryButton3.Location = new System.Drawing.Point(215, 2);
            this.categoryButton3.Margin = new System.Windows.Forms.Padding(2);
            this.categoryButton3.Name = "categoryButton3";
            this.categoryButton3.Size = new System.Drawing.Size(67, 27);
            this.categoryButton3.TabIndex = 3;
            this.categoryButton3.Text = "头盔";
            this.categoryButton3.UseVisualStyleBackColor = false;
            // 
            // categoryButton4
            // 
            this.categoryButton4.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(58)))), ((int)(((byte)(58)))), ((int)(((byte)(58)))));
            this.categoryButton4.FlatAppearance.BorderColor = System.Drawing.Color.FromArgb(((int)(((byte)(78)))), ((int)(((byte)(78)))), ((int)(((byte)(78)))));
            this.categoryButton4.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.categoryButton4.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this.categoryButton4.Location = new System.Drawing.Point(2, 33);
            this.categoryButton4.Margin = new System.Windows.Forms.Padding(2);
            this.categoryButton4.Name = "categoryButton4";
            this.categoryButton4.Size = new System.Drawing.Size(67, 27);
            this.categoryButton4.TabIndex = 4;
            this.categoryButton4.Text = "项链";
            this.categoryButton4.UseVisualStyleBackColor = false;
            // 
            // categoryButton5
            // 
            this.categoryButton5.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(58)))), ((int)(((byte)(58)))), ((int)(((byte)(58)))));
            this.categoryButton5.FlatAppearance.BorderColor = System.Drawing.Color.FromArgb(((int)(((byte)(78)))), ((int)(((byte)(78)))), ((int)(((byte)(78)))));
            this.categoryButton5.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.categoryButton5.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this.categoryButton5.Location = new System.Drawing.Point(73, 33);
            this.categoryButton5.Margin = new System.Windows.Forms.Padding(2);
            this.categoryButton5.Name = "categoryButton5";
            this.categoryButton5.Size = new System.Drawing.Size(67, 27);
            this.categoryButton5.TabIndex = 5;
            this.categoryButton5.Text = "手镯";
            this.categoryButton5.UseVisualStyleBackColor = false;
            // 
            // categoryButton6
            // 
            this.categoryButton6.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(58)))), ((int)(((byte)(58)))), ((int)(((byte)(58)))));
            this.categoryButton6.FlatAppearance.BorderColor = System.Drawing.Color.FromArgb(((int)(((byte)(78)))), ((int)(((byte)(78)))), ((int)(((byte)(78)))));
            this.categoryButton6.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.categoryButton6.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this.categoryButton6.Location = new System.Drawing.Point(144, 33);
            this.categoryButton6.Margin = new System.Windows.Forms.Padding(2);
            this.categoryButton6.Name = "categoryButton6";
            this.categoryButton6.Size = new System.Drawing.Size(67, 27);
            this.categoryButton6.TabIndex = 6;
            this.categoryButton6.Text = "戒指";
            this.categoryButton6.UseVisualStyleBackColor = false;
            // 
            // categoryButton7
            // 
            this.categoryButton7.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(58)))), ((int)(((byte)(58)))), ((int)(((byte)(58)))));
            this.categoryButton7.FlatAppearance.BorderColor = System.Drawing.Color.FromArgb(((int)(((byte)(78)))), ((int)(((byte)(78)))), ((int)(((byte)(78)))));
            this.categoryButton7.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.categoryButton7.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this.categoryButton7.Location = new System.Drawing.Point(215, 33);
            this.categoryButton7.Margin = new System.Windows.Forms.Padding(2);
            this.categoryButton7.Name = "categoryButton7";
            this.categoryButton7.Size = new System.Drawing.Size(67, 27);
            this.categoryButton7.TabIndex = 7;
            this.categoryButton7.Text = "鞋子";
            this.categoryButton7.UseVisualStyleBackColor = false;
            // 
            // categoryButton8
            // 
            this.categoryButton8.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(58)))), ((int)(((byte)(58)))), ((int)(((byte)(58)))));
            this.categoryButton8.FlatAppearance.BorderColor = System.Drawing.Color.FromArgb(((int)(((byte)(78)))), ((int)(((byte)(78)))), ((int)(((byte)(78)))));
            this.categoryButton8.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.categoryButton8.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this.categoryButton8.Location = new System.Drawing.Point(2, 64);
            this.categoryButton8.Margin = new System.Windows.Forms.Padding(2);
            this.categoryButton8.Name = "categoryButton8";
            this.categoryButton8.Size = new System.Drawing.Size(67, 27);
            this.categoryButton8.TabIndex = 8;
            this.categoryButton8.Text = "盾牌";
            this.categoryButton8.UseVisualStyleBackColor = false;
            // 
            // categoryButton9
            // 
            this.categoryButton9.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(58)))), ((int)(((byte)(58)))), ((int)(((byte)(58)))));
            this.categoryButton9.FlatAppearance.BorderColor = System.Drawing.Color.FromArgb(((int)(((byte)(78)))), ((int)(((byte)(78)))), ((int)(((byte)(78)))));
            this.categoryButton9.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.categoryButton9.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this.categoryButton9.Location = new System.Drawing.Point(73, 64);
            this.categoryButton9.Margin = new System.Windows.Forms.Padding(2);
            this.categoryButton9.Name = "categoryButton9";
            this.categoryButton9.Size = new System.Drawing.Size(67, 27);
            this.categoryButton9.TabIndex = 9;
            this.categoryButton9.Text = "时装";
            this.categoryButton9.UseVisualStyleBackColor = false;
            // 
            // categoryButton10
            // 
            this.categoryButton10.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(58)))), ((int)(((byte)(58)))), ((int)(((byte)(58)))));
            this.categoryButton10.FlatAppearance.BorderColor = System.Drawing.Color.FromArgb(((int)(((byte)(78)))), ((int)(((byte)(78)))), ((int)(((byte)(78)))));
            this.categoryButton10.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.categoryButton10.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this.categoryButton10.Location = new System.Drawing.Point(144, 64);
            this.categoryButton10.Margin = new System.Windows.Forms.Padding(2);
            this.categoryButton10.Name = "categoryButton10";
            this.categoryButton10.Size = new System.Drawing.Size(67, 27);
            this.categoryButton10.TabIndex = 10;
            this.categoryButton10.Text = "消耗品";
            this.categoryButton10.UseVisualStyleBackColor = false;
            // 
            // categoryButton11
            // 
            this.categoryButton11.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(58)))), ((int)(((byte)(58)))), ((int)(((byte)(58)))));
            this.categoryButton11.FlatAppearance.BorderColor = System.Drawing.Color.FromArgb(((int)(((byte)(78)))), ((int)(((byte)(78)))), ((int)(((byte)(78)))));
            this.categoryButton11.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.categoryButton11.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this.categoryButton11.Location = new System.Drawing.Point(215, 64);
            this.categoryButton11.Margin = new System.Windows.Forms.Padding(2);
            this.categoryButton11.Name = "categoryButton11";
            this.categoryButton11.Size = new System.Drawing.Size(67, 27);
            this.categoryButton11.TabIndex = 11;
            this.categoryButton11.Text = "书籍";
            this.categoryButton11.UseVisualStyleBackColor = false;
            // 
            // categoryButton12
            // 
            this.categoryButton12.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(58)))), ((int)(((byte)(58)))), ((int)(((byte)(58)))));
            this.categoryButton12.FlatAppearance.BorderColor = System.Drawing.Color.FromArgb(((int)(((byte)(78)))), ((int)(((byte)(78)))), ((int)(((byte)(78)))));
            this.categoryButton12.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.categoryButton12.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this.categoryButton12.Location = new System.Drawing.Point(2, 95);
            this.categoryButton12.Margin = new System.Windows.Forms.Padding(2);
            this.categoryButton12.Name = "categoryButton12";
            this.categoryButton12.Size = new System.Drawing.Size(67, 27);
            this.categoryButton12.TabIndex = 12;
            this.categoryButton12.Text = "卷轴";
            this.categoryButton12.UseVisualStyleBackColor = false;
            // 
            // categoryButton13
            // 
            this.categoryButton13.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(58)))), ((int)(((byte)(58)))), ((int)(((byte)(58)))));
            this.categoryButton13.FlatAppearance.BorderColor = System.Drawing.Color.FromArgb(((int)(((byte)(78)))), ((int)(((byte)(78)))), ((int)(((byte)(78)))));
            this.categoryButton13.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.categoryButton13.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this.categoryButton13.Location = new System.Drawing.Point(73, 95);
            this.categoryButton13.Margin = new System.Windows.Forms.Padding(2);
            this.categoryButton13.Name = "categoryButton13";
            this.categoryButton13.Size = new System.Drawing.Size(67, 27);
            this.categoryButton13.TabIndex = 13;
            this.categoryButton13.Text = "其他";
            this.categoryButton13.UseVisualStyleBackColor = false;
            // 
            // editorHost
            // 
            this.editorHost.AutoScroll = true;
            this.editorHost.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(36)))), ((int)(((byte)(36)))), ((int)(((byte)(36)))));
            this.editorHost.Controls.Add(this.editorLayout);
            this.editorHost.Dock = System.Windows.Forms.DockStyle.Fill;
            this.editorHost.Location = new System.Drawing.Point(0, 0);
            this.editorHost.Name = "editorHost";
            this.editorHost.Padding = new System.Windows.Forms.Padding(8);
            this.editorHost.Size = new System.Drawing.Size(1070, 837);
            this.editorHost.TabIndex = 0;
            // 
            // editorLayout
            // 
            this.editorLayout.AutoSize = true;
            this.editorLayout.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(36)))), ((int)(((byte)(36)))), ((int)(((byte)(36)))));
            this.editorLayout.ColumnCount = 1;
            this.editorLayout.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 100F));
            this.editorLayout.Controls.Add(this.previewGroup, 0, 0);
            this.editorLayout.Controls.Add(this.editorColumns, 0, 1);
            this.editorLayout.Controls.Add(this.setGroup, 0, 2);
            this.editorLayout.Dock = System.Windows.Forms.DockStyle.Top;
            this.editorLayout.Location = new System.Drawing.Point(8, 8);
            this.editorLayout.Name = "editorLayout";
            this.editorLayout.RowCount = 3;
            this.editorLayout.RowStyles.Add(new System.Windows.Forms.RowStyle());
            this.editorLayout.RowStyles.Add(new System.Windows.Forms.RowStyle());
            this.editorLayout.RowStyles.Add(new System.Windows.Forms.RowStyle());
            this.editorLayout.Size = new System.Drawing.Size(1037, 1361);
            this.editorLayout.TabIndex = 0;
            // 
            // previewGroup
            // 
            this.previewGroup.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(47)))), ((int)(((byte)(47)))), ((int)(((byte)(47)))));
            this.previewGroup.Controls.Add(this.previews);
            this.previewGroup.Controls.Add(this._imageSizeLabel);
            this.previewGroup.Dock = System.Windows.Forms.DockStyle.Top;
            this.previewGroup.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this.previewGroup.Location = new System.Drawing.Point(0, 0);
            this.previewGroup.Margin = new System.Windows.Forms.Padding(0, 0, 0, 8);
            this.previewGroup.MinimumSize = new System.Drawing.Size(0, 356);
            this.previewGroup.Name = "previewGroup";
            this.previewGroup.Padding = new System.Windows.Forms.Padding(8, 24, 8, 8);
            this.previewGroup.Size = new System.Drawing.Size(1037, 356);
            this.previewGroup.TabIndex = 0;
            this.previewGroup.TabStop = false;
            this.previewGroup.Text = "素材预览";
            // 
            // previews
            // 
            this.previews.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(47)))), ((int)(((byte)(47)))), ((int)(((byte)(47)))));
            this.previews.ColumnCount = 4;
            this.previews.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 20F));
            this.previews.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 26F));
            this.previews.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 26F));
            this.previews.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 28F));
            this.previews.Controls.Add(this.inventoryColumn, 0, 0);
            this.previews.Controls.Add(this.equipColumn, 1, 0);
            this.previews.Controls.Add(this.appearanceColumn, 2, 0);
            this.previews.Controls.Add(this.smallPreviews, 3, 0);
            this.previews.Dock = System.Windows.Forms.DockStyle.Fill;
            this.previews.GrowStyle = System.Windows.Forms.TableLayoutPanelGrowStyle.FixedSize;
            this.previews.Location = new System.Drawing.Point(8, 40);
            this.previews.Margin = new System.Windows.Forms.Padding(0);
            this.previews.Name = "previews";
            this.previews.RowCount = 1;
            this.previews.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Absolute, 290F));
            this.previews.Size = new System.Drawing.Size(1021, 288);
            this.previews.TabIndex = 0;
            // 
            // inventoryColumn
            // 
            this.inventoryColumn.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(47)))), ((int)(((byte)(47)))), ((int)(((byte)(47)))));
            this.inventoryColumn.Controls.Add(this._inventoryPreviewHostPanel);
            this.inventoryColumn.Controls.Add(this.inventoryTitle);
            this.inventoryColumn.Dock = System.Windows.Forms.DockStyle.Fill;
            this.inventoryColumn.Location = new System.Drawing.Point(0, 0);
            this.inventoryColumn.Margin = new System.Windows.Forms.Padding(0);
            this.inventoryColumn.Name = "inventoryColumn";
            this.inventoryColumn.Padding = new System.Windows.Forms.Padding(2, 0, 2, 0);
            this.inventoryColumn.Size = new System.Drawing.Size(204, 290);
            this.inventoryColumn.TabIndex = 0;
            // 
            // _inventoryPreviewHostPanel
            // 
            this._inventoryPreviewHostPanel.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(47)))), ((int)(((byte)(47)))), ((int)(((byte)(47)))));
            this._inventoryPreviewHostPanel.Dock = System.Windows.Forms.DockStyle.Fill;
            this._inventoryPreviewHostPanel.Location = new System.Drawing.Point(2, 24);
            this._inventoryPreviewHostPanel.Margin = new System.Windows.Forms.Padding(0);
            this._inventoryPreviewHostPanel.Name = "_inventoryPreviewHostPanel";
            this._inventoryPreviewHostPanel.Size = new System.Drawing.Size(200, 266);
            this._inventoryPreviewHostPanel.TabIndex = 0;
            // 
            // inventoryTitle
            // 
            this.inventoryTitle.Dock = System.Windows.Forms.DockStyle.Top;
            this.inventoryTitle.Font = new System.Drawing.Font("Microsoft YaHei UI", 8F);
            this.inventoryTitle.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this.inventoryTitle.Location = new System.Drawing.Point(2, 0);
            this.inventoryTitle.Name = "inventoryTitle";
            this.inventoryTitle.Size = new System.Drawing.Size(200, 24);
            this.inventoryTitle.TabIndex = 1;
            this.inventoryTitle.Text = "大背包 (Inventory.Zl) 6x10";
            this.inventoryTitle.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            // 
            // equipColumn
            // 
            this.equipColumn.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(47)))), ((int)(((byte)(47)))), ((int)(((byte)(47)))));
            this.equipColumn.Controls.Add(this._equipPreviewHostPanel);
            this.equipColumn.Controls.Add(this.equipTitle);
            this.equipColumn.Dock = System.Windows.Forms.DockStyle.Fill;
            this.equipColumn.Location = new System.Drawing.Point(204, 0);
            this.equipColumn.Margin = new System.Windows.Forms.Padding(0);
            this.equipColumn.Name = "equipColumn";
            this.equipColumn.Padding = new System.Windows.Forms.Padding(2, 0, 2, 0);
            this.equipColumn.Size = new System.Drawing.Size(265, 290);
            this.equipColumn.TabIndex = 1;
            // 
            // _equipPreviewHostPanel
            // 
            this._equipPreviewHostPanel.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(47)))), ((int)(((byte)(47)))), ((int)(((byte)(47)))));
            this._equipPreviewHostPanel.Dock = System.Windows.Forms.DockStyle.Fill;
            this._equipPreviewHostPanel.Location = new System.Drawing.Point(2, 24);
            this._equipPreviewHostPanel.Margin = new System.Windows.Forms.Padding(0);
            this._equipPreviewHostPanel.Name = "_equipPreviewHostPanel";
            this._equipPreviewHostPanel.Size = new System.Drawing.Size(261, 266);
            this._equipPreviewHostPanel.TabIndex = 0;
            // 
            // equipTitle
            // 
            this.equipTitle.Dock = System.Windows.Forms.DockStyle.Top;
            this.equipTitle.Font = new System.Drawing.Font("Microsoft YaHei UI", 8F);
            this.equipTitle.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this.equipTitle.Location = new System.Drawing.Point(2, 0);
            this.equipTitle.Name = "equipTitle";
            this.equipTitle.Size = new System.Drawing.Size(261, 24);
            this.equipTitle.TabIndex = 1;
            this.equipTitle.Text = "内观 (Equip.Zl)";
            this.equipTitle.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            // 
            // appearanceColumn
            // 
            this.appearanceColumn.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(47)))), ((int)(((byte)(47)))), ((int)(((byte)(47)))));
            this.appearanceColumn.Controls.Add(this._appearancePreviewHostPanel);
            this.appearanceColumn.Controls.Add(this.appearanceTitle);
            this.appearanceColumn.Dock = System.Windows.Forms.DockStyle.Fill;
            this.appearanceColumn.Location = new System.Drawing.Point(469, 0);
            this.appearanceColumn.Margin = new System.Windows.Forms.Padding(0);
            this.appearanceColumn.Name = "appearanceColumn";
            this.appearanceColumn.Padding = new System.Windows.Forms.Padding(2, 0, 2, 0);
            this.appearanceColumn.Size = new System.Drawing.Size(265, 290);
            this.appearanceColumn.TabIndex = 2;
            // 
            // _appearancePreviewHostPanel
            // 
            this._appearancePreviewHostPanel.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(47)))), ((int)(((byte)(47)))), ((int)(((byte)(47)))));
            this._appearancePreviewHostPanel.Dock = System.Windows.Forms.DockStyle.Fill;
            this._appearancePreviewHostPanel.Location = new System.Drawing.Point(2, 24);
            this._appearancePreviewHostPanel.Margin = new System.Windows.Forms.Padding(0);
            this._appearancePreviewHostPanel.Name = "_appearancePreviewHostPanel";
            this._appearancePreviewHostPanel.Size = new System.Drawing.Size(261, 266);
            this._appearancePreviewHostPanel.TabIndex = 0;
            // 
            // appearanceTitle
            // 
            this.appearanceTitle.Dock = System.Windows.Forms.DockStyle.Top;
            this.appearanceTitle.Font = new System.Drawing.Font("Microsoft YaHei UI", 8F);
            this.appearanceTitle.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this.appearanceTitle.Location = new System.Drawing.Point(2, 0);
            this.appearanceTitle.Name = "appearanceTitle";
            this.appearanceTitle.Size = new System.Drawing.Size(261, 24);
            this.appearanceTitle.TabIndex = 1;
            this.appearanceTitle.Text = "外观 (Shape计算)";
            this.appearanceTitle.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            // 
            // smallPreviews
            // 
            this.smallPreviews.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(47)))), ((int)(((byte)(47)))), ((int)(((byte)(47)))));
            this.smallPreviews.ColumnCount = 1;
            this.smallPreviews.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Absolute, 291F));
            this.smallPreviews.Controls.Add(this.smallStoreColumn, 0, 0);
            this.smallPreviews.Controls.Add(this.mallStoreColumn, 0, 1);
            this.smallPreviews.Controls.Add(this.groundColumn, 0, 2);
            this.smallPreviews.Dock = System.Windows.Forms.DockStyle.Fill;
            this.smallPreviews.GrowStyle = System.Windows.Forms.TableLayoutPanelGrowStyle.FixedSize;
            this.smallPreviews.Location = new System.Drawing.Point(734, 0);
            this.smallPreviews.Margin = new System.Windows.Forms.Padding(0);
            this.smallPreviews.Name = "smallPreviews";
            this.smallPreviews.Padding = new System.Windows.Forms.Padding(2, 0, 0, 0);
            this.smallPreviews.RowCount = 3;
            this.smallPreviews.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 33.3333F));
            this.smallPreviews.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 33.3333F));
            this.smallPreviews.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 33.3334F));
            this.smallPreviews.Size = new System.Drawing.Size(287, 290);
            this.smallPreviews.TabIndex = 3;
            // 
            // smallStoreColumn
            // 
            this.smallStoreColumn.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(47)))), ((int)(((byte)(47)))), ((int)(((byte)(47)))));
            this.smallStoreColumn.Controls.Add(this._smallStorePreviewHostPanel);
            this.smallStoreColumn.Controls.Add(this.smallStoreTitle);
            this.smallStoreColumn.Dock = System.Windows.Forms.DockStyle.Fill;
            this.smallStoreColumn.Location = new System.Drawing.Point(2, 0);
            this.smallStoreColumn.Margin = new System.Windows.Forms.Padding(0);
            this.smallStoreColumn.Name = "smallStoreColumn";
            this.smallStoreColumn.Padding = new System.Windows.Forms.Padding(2, 0, 2, 0);
            this.smallStoreColumn.Size = new System.Drawing.Size(291, 96);
            this.smallStoreColumn.TabIndex = 0;
            // 
            // _smallStorePreviewHostPanel
            // 
            this._smallStorePreviewHostPanel.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(47)))), ((int)(((byte)(47)))), ((int)(((byte)(47)))));
            this._smallStorePreviewHostPanel.Dock = System.Windows.Forms.DockStyle.Fill;
            this._smallStorePreviewHostPanel.Location = new System.Drawing.Point(2, 24);
            this._smallStorePreviewHostPanel.Margin = new System.Windows.Forms.Padding(0);
            this._smallStorePreviewHostPanel.Name = "_smallStorePreviewHostPanel";
            this._smallStorePreviewHostPanel.Size = new System.Drawing.Size(287, 72);
            this._smallStorePreviewHostPanel.TabIndex = 0;
            // 
            // smallStoreTitle
            // 
            this.smallStoreTitle.Dock = System.Windows.Forms.DockStyle.Top;
            this.smallStoreTitle.Font = new System.Drawing.Font("Microsoft YaHei UI", 8F);
            this.smallStoreTitle.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this.smallStoreTitle.Location = new System.Drawing.Point(2, 0);
            this.smallStoreTitle.Name = "smallStoreTitle";
            this.smallStoreTitle.Size = new System.Drawing.Size(287, 24);
            this.smallStoreTitle.TabIndex = 1;
            this.smallStoreTitle.Text = "小背包 (StoreItems)";
            this.smallStoreTitle.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            // 
            // mallStoreColumn
            // 
            this.mallStoreColumn.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(47)))), ((int)(((byte)(47)))), ((int)(((byte)(47)))));
            this.mallStoreColumn.Controls.Add(this._mallStorePreviewHostPanel);
            this.mallStoreColumn.Controls.Add(this.mallStoreTitle);
            this.mallStoreColumn.Dock = System.Windows.Forms.DockStyle.Fill;
            this.mallStoreColumn.Location = new System.Drawing.Point(2, 96);
            this.mallStoreColumn.Margin = new System.Windows.Forms.Padding(0);
            this.mallStoreColumn.Name = "mallStoreColumn";
            this.mallStoreColumn.Padding = new System.Windows.Forms.Padding(2, 0, 2, 0);
            this.mallStoreColumn.Size = new System.Drawing.Size(291, 96);
            this.mallStoreColumn.TabIndex = 1;
            // 
            // _mallStorePreviewHostPanel
            // 
            this._mallStorePreviewHostPanel.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(47)))), ((int)(((byte)(47)))), ((int)(((byte)(47)))));
            this._mallStorePreviewHostPanel.Dock = System.Windows.Forms.DockStyle.Fill;
            this._mallStorePreviewHostPanel.Location = new System.Drawing.Point(2, 24);
            this._mallStorePreviewHostPanel.Margin = new System.Windows.Forms.Padding(0);
            this._mallStorePreviewHostPanel.Name = "_mallStorePreviewHostPanel";
            this._mallStorePreviewHostPanel.Size = new System.Drawing.Size(287, 72);
            this._mallStorePreviewHostPanel.TabIndex = 0;
            // 
            // mallStoreTitle
            // 
            this.mallStoreTitle.Dock = System.Windows.Forms.DockStyle.Top;
            this.mallStoreTitle.Font = new System.Drawing.Font("Microsoft YaHei UI", 8F);
            this.mallStoreTitle.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this.mallStoreTitle.Location = new System.Drawing.Point(2, 0);
            this.mallStoreTitle.Name = "mallStoreTitle";
            this.mallStoreTitle.Size = new System.Drawing.Size(287, 24);
            this.mallStoreTitle.TabIndex = 1;
            this.mallStoreTitle.Text = "商城 (StoreItems)";
            this.mallStoreTitle.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            // 
            // groundColumn
            // 
            this.groundColumn.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(47)))), ((int)(((byte)(47)))), ((int)(((byte)(47)))));
            this.groundColumn.Controls.Add(this._groundPreviewHostPanel);
            this.groundColumn.Controls.Add(this.groundTitle);
            this.groundColumn.Dock = System.Windows.Forms.DockStyle.Fill;
            this.groundColumn.Location = new System.Drawing.Point(2, 192);
            this.groundColumn.Margin = new System.Windows.Forms.Padding(0);
            this.groundColumn.Name = "groundColumn";
            this.groundColumn.Padding = new System.Windows.Forms.Padding(2, 0, 2, 0);
            this.groundColumn.Size = new System.Drawing.Size(291, 98);
            this.groundColumn.TabIndex = 2;
            // 
            // _groundPreviewHostPanel
            // 
            this._groundPreviewHostPanel.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(47)))), ((int)(((byte)(47)))), ((int)(((byte)(47)))));
            this._groundPreviewHostPanel.Dock = System.Windows.Forms.DockStyle.Fill;
            this._groundPreviewHostPanel.Location = new System.Drawing.Point(2, 24);
            this._groundPreviewHostPanel.Margin = new System.Windows.Forms.Padding(0);
            this._groundPreviewHostPanel.Name = "_groundPreviewHostPanel";
            this._groundPreviewHostPanel.Size = new System.Drawing.Size(287, 74);
            this._groundPreviewHostPanel.TabIndex = 0;
            // 
            // groundTitle
            // 
            this.groundTitle.Dock = System.Windows.Forms.DockStyle.Top;
            this.groundTitle.Font = new System.Drawing.Font("Microsoft YaHei UI", 8F);
            this.groundTitle.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this.groundTitle.Location = new System.Drawing.Point(2, 0);
            this.groundTitle.Name = "groundTitle";
            this.groundTitle.Size = new System.Drawing.Size(287, 24);
            this.groundTitle.TabIndex = 1;
            this.groundTitle.Text = "地上 (Ground)";
            this.groundTitle.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            // 
            // _imageSizeLabel
            // 
            this._imageSizeLabel.Dock = System.Windows.Forms.DockStyle.Bottom;
            this._imageSizeLabel.ForeColor = System.Drawing.Color.LightGray;
            this._imageSizeLabel.Location = new System.Drawing.Point(8, 328);
            this._imageSizeLabel.Name = "_imageSizeLabel";
            this._imageSizeLabel.Size = new System.Drawing.Size(1021, 20);
            this._imageSizeLabel.TabIndex = 1;
            this._imageSizeLabel.Text = "尺寸：-";
            this._imageSizeLabel.TextAlign = System.Drawing.ContentAlignment.MiddleLeft;
            // 
            // editorColumns
            // 
            this.editorColumns.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(36)))), ((int)(((byte)(36)))), ((int)(((byte)(36)))));
            this.editorColumns.ColumnCount = 3;
            this.editorColumns.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 55F));
            this.editorColumns.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 22F));
            this.editorColumns.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 23F));
            this.editorColumns.Controls.Add(this.basicGroup, 0, 0);
            this.editorColumns.Controls.Add(this.statsGroup, 1, 0);
            this.editorColumns.Controls.Add(this.previewSettingsGroup, 2, 0);
            this.editorColumns.Dock = System.Windows.Forms.DockStyle.Top;
            this.editorColumns.GrowStyle = System.Windows.Forms.TableLayoutPanelGrowStyle.FixedSize;
            this.editorColumns.Location = new System.Drawing.Point(0, 364);
            this.editorColumns.Margin = new System.Windows.Forms.Padding(0, 0, 0, 8);
            this.editorColumns.MinimumSize = new System.Drawing.Size(0, 420);
            this.editorColumns.Name = "editorColumns";
            this.editorColumns.RowCount = 1;
            this.editorColumns.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Absolute, 420F));
            this.editorColumns.Size = new System.Drawing.Size(1037, 420);
            this.editorColumns.TabIndex = 1;
            // 
            // basicGroup
            // 
            this.basicGroup.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(47)))), ((int)(((byte)(47)))), ((int)(((byte)(47)))));
            this.basicGroup.Controls.Add(this.basicLayout);
            this.basicGroup.Dock = System.Windows.Forms.DockStyle.Fill;
            this.basicGroup.ForeColor = System.Drawing.Color.Yellow;
            this.basicGroup.Location = new System.Drawing.Point(0, 0);
            this.basicGroup.Margin = new System.Windows.Forms.Padding(0, 0, 6, 0);
            this.basicGroup.Name = "basicGroup";
            this.basicGroup.Padding = new System.Windows.Forms.Padding(8, 24, 8, 8);
            this.basicGroup.Size = new System.Drawing.Size(564, 420);
            this.basicGroup.TabIndex = 0;
            this.basicGroup.TabStop = false;
            this.basicGroup.Text = "基础属性";
            // 
            // basicLayout
            // 
            this.basicLayout.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(47)))), ((int)(((byte)(47)))), ((int)(((byte)(47)))));
            this.basicLayout.ColumnCount = 1;
            this.basicLayout.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Absolute, 557F));
            this.basicLayout.Controls.Add(this.basicRow0, 0, 0);
            this.basicLayout.Controls.Add(this.basicRow1, 0, 1);
            this.basicLayout.Controls.Add(this.basicRow2, 0, 2);
            this.basicLayout.Controls.Add(this.basicRow3, 0, 3);
            this.basicLayout.Controls.Add(this.basicRow4, 0, 4);
            this.basicLayout.Controls.Add(this.basicRow5, 0, 5);
            this.basicLayout.Controls.Add(this.basicRow6, 0, 6);
            this.basicLayout.Controls.Add(this.flags, 0, 7);
            this.basicLayout.Controls.Add(this.descriptionRow, 0, 8);
            this.basicLayout.Controls.Add(this.basicSpacer, 0, 9);
            this.basicLayout.Dock = System.Windows.Forms.DockStyle.Fill;
            this.basicLayout.Location = new System.Drawing.Point(8, 40);
            this.basicLayout.Name = "basicLayout";
            this.basicLayout.RowCount = 10;
            this.basicLayout.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Absolute, 28F));
            this.basicLayout.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Absolute, 28F));
            this.basicLayout.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Absolute, 28F));
            this.basicLayout.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Absolute, 28F));
            this.basicLayout.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Absolute, 28F));
            this.basicLayout.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Absolute, 28F));
            this.basicLayout.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Absolute, 28F));
            this.basicLayout.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Absolute, 54F));
            this.basicLayout.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Absolute, 88F));
            this.basicLayout.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 100F));
            this.basicLayout.Size = new System.Drawing.Size(548, 372);
            this.basicLayout.TabIndex = 0;
            // 
            // basicRow0
            // 
            this.basicRow0.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(47)))), ((int)(((byte)(47)))), ((int)(((byte)(47)))));
            this.basicRow0.ColumnCount = 6;
            this.basicRow0.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Absolute, 58F));
            this.basicRow0.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 33.3333F));
            this.basicRow0.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Absolute, 58F));
            this.basicRow0.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 33.3333F));
            this.basicRow0.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Absolute, 58F));
            this.basicRow0.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 33.3333F));
            this.basicRow0.Controls.Add(this.basicLabel0_0, 0, 0);
            this.basicRow0.Controls.Add(this._itemNameTextBox, 1, 0);
            this.basicRow0.Controls.Add(this.basicLabel0_1, 2, 0);
            this.basicRow0.Controls.Add(this._itemTypeComboBox, 3, 0);
            this.basicRow0.Controls.Add(this.basicLabel0_2, 4, 0);
            this.basicRow0.Controls.Add(this._imageNumeric, 5, 0);
            this.basicRow0.Dock = System.Windows.Forms.DockStyle.Fill;
            this.basicRow0.Location = new System.Drawing.Point(0, 0);
            this.basicRow0.Margin = new System.Windows.Forms.Padding(0);
            this.basicRow0.Name = "basicRow0";
            this.basicRow0.RowCount = 1;
            this.basicRow0.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Absolute, 28F));
            this.basicRow0.Size = new System.Drawing.Size(557, 28);
            this.basicRow0.TabIndex = 0;
            // 
            // basicLabel0_0
            // 
            this.basicLabel0_0.BackColor = System.Drawing.Color.Transparent;
            this.basicLabel0_0.Dock = System.Windows.Forms.DockStyle.Fill;
            this.basicLabel0_0.Font = this.Font;
            this.basicLabel0_0.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this.basicLabel0_0.Location = new System.Drawing.Point(2, 2);
            this.basicLabel0_0.Margin = new System.Windows.Forms.Padding(2);
            this.basicLabel0_0.Name = "basicLabel0_0";
            this.basicLabel0_0.Size = new System.Drawing.Size(54, 24);
            this.basicLabel0_0.TabIndex = 0;
            this.basicLabel0_0.Text = "名称";
            this.basicLabel0_0.TextAlign = System.Drawing.ContentAlignment.MiddleLeft;
            // 
            // _itemNameTextBox
            // 
            this._itemNameTextBox.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(58)))), ((int)(((byte)(58)))), ((int)(((byte)(58)))));
            this._itemNameTextBox.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this._itemNameTextBox.Dock = System.Windows.Forms.DockStyle.Fill;
            this._itemNameTextBox.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this._itemNameTextBox.Location = new System.Drawing.Point(60, 2);
            this._itemNameTextBox.Margin = new System.Windows.Forms.Padding(2, 2, 4, 2);
            this._itemNameTextBox.Name = "_itemNameTextBox";
            this._itemNameTextBox.Size = new System.Drawing.Size(121, 23);
            this._itemNameTextBox.TabIndex = 1;
            // 
            // basicLabel0_1
            // 
            this.basicLabel0_1.BackColor = System.Drawing.Color.Transparent;
            this.basicLabel0_1.Dock = System.Windows.Forms.DockStyle.Fill;
            this.basicLabel0_1.Font = this.Font;
            this.basicLabel0_1.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this.basicLabel0_1.Location = new System.Drawing.Point(187, 2);
            this.basicLabel0_1.Margin = new System.Windows.Forms.Padding(2);
            this.basicLabel0_1.Name = "basicLabel0_1";
            this.basicLabel0_1.Size = new System.Drawing.Size(54, 24);
            this.basicLabel0_1.TabIndex = 2;
            this.basicLabel0_1.Text = "类型";
            this.basicLabel0_1.TextAlign = System.Drawing.ContentAlignment.MiddleLeft;
            // 
            // _itemTypeComboBox
            // 
            this._itemTypeComboBox.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(58)))), ((int)(((byte)(58)))), ((int)(((byte)(58)))));
            this._itemTypeComboBox.Dock = System.Windows.Forms.DockStyle.Fill;
            this._itemTypeComboBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this._itemTypeComboBox.DropDownWidth = 100;
            this._itemTypeComboBox.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this._itemTypeComboBox.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this._itemTypeComboBox.Location = new System.Drawing.Point(245, 2);
            this._itemTypeComboBox.Margin = new System.Windows.Forms.Padding(2, 2, 4, 2);
            this._itemTypeComboBox.Name = "_itemTypeComboBox";
            this._itemTypeComboBox.Size = new System.Drawing.Size(121, 25);
            this._itemTypeComboBox.TabIndex = 3;
            this._itemTypeComboBox.SelectedIndexChanged += new System.EventHandler(this._itemTypeComboBox_SelectedIndexChanged);
            // 
            // basicLabel0_2
            // 
            this.basicLabel0_2.BackColor = System.Drawing.Color.Transparent;
            this.basicLabel0_2.Dock = System.Windows.Forms.DockStyle.Fill;
            this.basicLabel0_2.Font = this.Font;
            this.basicLabel0_2.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this.basicLabel0_2.Location = new System.Drawing.Point(372, 2);
            this.basicLabel0_2.Margin = new System.Windows.Forms.Padding(2);
            this.basicLabel0_2.Name = "basicLabel0_2";
            this.basicLabel0_2.Size = new System.Drawing.Size(54, 24);
            this.basicLabel0_2.TabIndex = 4;
            this.basicLabel0_2.Text = "图片序号";
            this.basicLabel0_2.TextAlign = System.Drawing.ContentAlignment.MiddleLeft;
            // 
            // _imageNumeric
            // 
            this._imageNumeric.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(58)))), ((int)(((byte)(58)))), ((int)(((byte)(58)))));
            this._imageNumeric.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this._imageNumeric.Dock = System.Windows.Forms.DockStyle.Fill;
            this._imageNumeric.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this._imageNumeric.Location = new System.Drawing.Point(430, 2);
            this._imageNumeric.Margin = new System.Windows.Forms.Padding(2, 2, 4, 2);
            this._imageNumeric.Maximum = new decimal(new int[] {
            1000000000,
            0,
            0,
            0});
            this._imageNumeric.Minimum = new decimal(new int[] {
            1000000000,
            0,
            0,
            -2147483648});
            this._imageNumeric.Name = "_imageNumeric";
            this._imageNumeric.Size = new System.Drawing.Size(123, 23);
            this._imageNumeric.TabIndex = 10;
            this._imageNumeric.ThousandsSeparator = true;
            // 
            // basicRow1
            // 
            this.basicRow1.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(47)))), ((int)(((byte)(47)))), ((int)(((byte)(47)))));
            this.basicRow1.ColumnCount = 6;
            this.basicRow1.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Absolute, 58F));
            this.basicRow1.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 33.3333F));
            this.basicRow1.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Absolute, 58F));
            this.basicRow1.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 33.3333F));
            this.basicRow1.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Absolute, 58F));
            this.basicRow1.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 33.3333F));
            this.basicRow1.Controls.Add(this.basicLabel1_0, 0, 0);
            this.basicRow1.Controls.Add(this._requiredTypeComboBox, 1, 0);
            this.basicRow1.Controls.Add(this.basicLabel1_1, 2, 0);
            this.basicRow1.Controls.Add(this._requiredAmountNumeric, 3, 0);
            this.basicRow1.Controls.Add(this.basicLabel1_2, 4, 0);
            this.basicRow1.Controls.Add(this._shapeNumeric, 5, 0);
            this.basicRow1.Dock = System.Windows.Forms.DockStyle.Fill;
            this.basicRow1.Location = new System.Drawing.Point(0, 28);
            this.basicRow1.Margin = new System.Windows.Forms.Padding(0);
            this.basicRow1.Name = "basicRow1";
            this.basicRow1.RowCount = 1;
            this.basicRow1.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Absolute, 28F));
            this.basicRow1.Size = new System.Drawing.Size(557, 28);
            this.basicRow1.TabIndex = 1;
            // 
            // basicLabel1_0
            // 
            this.basicLabel1_0.BackColor = System.Drawing.Color.Transparent;
            this.basicLabel1_0.Dock = System.Windows.Forms.DockStyle.Fill;
            this.basicLabel1_0.Font = this.Font;
            this.basicLabel1_0.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this.basicLabel1_0.Location = new System.Drawing.Point(2, 2);
            this.basicLabel1_0.Margin = new System.Windows.Forms.Padding(2);
            this.basicLabel1_0.Name = "basicLabel1_0";
            this.basicLabel1_0.Size = new System.Drawing.Size(54, 24);
            this.basicLabel1_0.TabIndex = 0;
            this.basicLabel1_0.Text = "要求类型";
            this.basicLabel1_0.TextAlign = System.Drawing.ContentAlignment.MiddleLeft;
            // 
            // _requiredTypeComboBox
            // 
            this._requiredTypeComboBox.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(58)))), ((int)(((byte)(58)))), ((int)(((byte)(58)))));
            this._requiredTypeComboBox.Dock = System.Windows.Forms.DockStyle.Fill;
            this._requiredTypeComboBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this._requiredTypeComboBox.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this._requiredTypeComboBox.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this._requiredTypeComboBox.Location = new System.Drawing.Point(60, 2);
            this._requiredTypeComboBox.Margin = new System.Windows.Forms.Padding(2, 2, 4, 2);
            this._requiredTypeComboBox.Name = "_requiredTypeComboBox";
            this._requiredTypeComboBox.Size = new System.Drawing.Size(121, 25);
            this._requiredTypeComboBox.TabIndex = 1;
            // 
            // basicLabel1_1
            // 
            this.basicLabel1_1.BackColor = System.Drawing.Color.Transparent;
            this.basicLabel1_1.Dock = System.Windows.Forms.DockStyle.Fill;
            this.basicLabel1_1.Font = this.Font;
            this.basicLabel1_1.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this.basicLabel1_1.Location = new System.Drawing.Point(187, 2);
            this.basicLabel1_1.Margin = new System.Windows.Forms.Padding(2);
            this.basicLabel1_1.Name = "basicLabel1_1";
            this.basicLabel1_1.Size = new System.Drawing.Size(54, 24);
            this.basicLabel1_1.TabIndex = 2;
            this.basicLabel1_1.Text = "要求参数";
            this.basicLabel1_1.TextAlign = System.Drawing.ContentAlignment.MiddleLeft;
            // 
            // _requiredAmountNumeric
            // 
            this._requiredAmountNumeric.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(58)))), ((int)(((byte)(58)))), ((int)(((byte)(58)))));
            this._requiredAmountNumeric.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this._requiredAmountNumeric.Dock = System.Windows.Forms.DockStyle.Fill;
            this._requiredAmountNumeric.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this._requiredAmountNumeric.Location = new System.Drawing.Point(245, 2);
            this._requiredAmountNumeric.Margin = new System.Windows.Forms.Padding(2, 2, 4, 2);
            this._requiredAmountNumeric.Maximum = new decimal(new int[] {
            1000000000,
            0,
            0,
            0});
            this._requiredAmountNumeric.Minimum = new decimal(new int[] {
            1000000000,
            0,
            0,
            -2147483648});
            this._requiredAmountNumeric.Name = "_requiredAmountNumeric";
            this._requiredAmountNumeric.Size = new System.Drawing.Size(121, 23);
            this._requiredAmountNumeric.TabIndex = 3;
            this._requiredAmountNumeric.ThousandsSeparator = true;
            // 
            // basicLabel1_2
            // 
            this.basicLabel1_2.BackColor = System.Drawing.Color.Transparent;
            this.basicLabel1_2.Dock = System.Windows.Forms.DockStyle.Fill;
            this.basicLabel1_2.Font = this.Font;
            this.basicLabel1_2.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this.basicLabel1_2.Location = new System.Drawing.Point(372, 2);
            this.basicLabel1_2.Margin = new System.Windows.Forms.Padding(2);
            this.basicLabel1_2.Name = "basicLabel1_2";
            this.basicLabel1_2.Size = new System.Drawing.Size(54, 24);
            this.basicLabel1_2.TabIndex = 4;
            this.basicLabel1_2.Text = "外观";
            this.basicLabel1_2.TextAlign = System.Drawing.ContentAlignment.MiddleLeft;
            // 
            // _shapeNumeric
            // 
            this._shapeNumeric.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(58)))), ((int)(((byte)(58)))), ((int)(((byte)(58)))));
            this._shapeNumeric.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this._shapeNumeric.Dock = System.Windows.Forms.DockStyle.Fill;
            this._shapeNumeric.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this._shapeNumeric.Location = new System.Drawing.Point(430, 2);
            this._shapeNumeric.Margin = new System.Windows.Forms.Padding(2, 2, 4, 2);
            this._shapeNumeric.Maximum = new decimal(new int[] {
            1000000000,
            0,
            0,
            0});
            this._shapeNumeric.Minimum = new decimal(new int[] {
            1000000000,
            0,
            0,
            -2147483648});
            this._shapeNumeric.Name = "_shapeNumeric";
            this._shapeNumeric.Size = new System.Drawing.Size(123, 23);
            this._shapeNumeric.TabIndex = 5;
            this._shapeNumeric.ThousandsSeparator = true;
            // 
            // basicRow2
            // 
            this.basicRow2.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(47)))), ((int)(((byte)(47)))), ((int)(((byte)(47)))));
            this.basicRow2.ColumnCount = 6;
            this.basicRow2.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Absolute, 58F));
            this.basicRow2.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 33.3333F));
            this.basicRow2.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Absolute, 58F));
            this.basicRow2.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 33.3333F));
            this.basicRow2.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Absolute, 58F));
            this.basicRow2.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 33.3333F));
            this.basicRow2.Controls.Add(this.basicLabel2_0, 0, 0);
            this.basicRow2.Controls.Add(this._effectComboBox, 1, 0);
            this.basicRow2.Controls.Add(this.basicLabel2_1, 2, 0);
            this.basicRow2.Controls.Add(this._basicExternalEffectLabel, 3, 0);
            this.basicRow2.Controls.Add(this.basicLabel2_2, 4, 0);
            this.basicRow2.Controls.Add(this._partCountNumeric, 5, 0);
            this.basicRow2.Dock = System.Windows.Forms.DockStyle.Fill;
            this.basicRow2.Location = new System.Drawing.Point(0, 56);
            this.basicRow2.Margin = new System.Windows.Forms.Padding(0);
            this.basicRow2.Name = "basicRow2";
            this.basicRow2.RowCount = 1;
            this.basicRow2.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Absolute, 28F));
            this.basicRow2.Size = new System.Drawing.Size(557, 28);
            this.basicRow2.TabIndex = 2;
            // 
            // basicLabel2_0
            // 
            this.basicLabel2_0.BackColor = System.Drawing.Color.Transparent;
            this.basicLabel2_0.Dock = System.Windows.Forms.DockStyle.Fill;
            this.basicLabel2_0.Font = this.Font;
            this.basicLabel2_0.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this.basicLabel2_0.Location = new System.Drawing.Point(2, 2);
            this.basicLabel2_0.Margin = new System.Windows.Forms.Padding(2);
            this.basicLabel2_0.Name = "basicLabel2_0";
            this.basicLabel2_0.Size = new System.Drawing.Size(54, 24);
            this.basicLabel2_0.TabIndex = 0;
            this.basicLabel2_0.Text = "物品特效";
            this.basicLabel2_0.TextAlign = System.Drawing.ContentAlignment.MiddleLeft;
            // 
            // _effectComboBox
            // 
            this._effectComboBox.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(58)))), ((int)(((byte)(58)))), ((int)(((byte)(58)))));
            this._effectComboBox.Dock = System.Windows.Forms.DockStyle.Fill;
            this._effectComboBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this._effectComboBox.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this._effectComboBox.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this._effectComboBox.Location = new System.Drawing.Point(60, 2);
            this._effectComboBox.Margin = new System.Windows.Forms.Padding(2, 2, 4, 2);
            this._effectComboBox.Name = "_effectComboBox";
            this._effectComboBox.Size = new System.Drawing.Size(121, 25);
            this._effectComboBox.TabIndex = 1;
            // 
            // basicLabel2_1
            // 
            this.basicLabel2_1.BackColor = System.Drawing.Color.Transparent;
            this.basicLabel2_1.Dock = System.Windows.Forms.DockStyle.Fill;
            this.basicLabel2_1.Font = this.Font;
            this.basicLabel2_1.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this.basicLabel2_1.Location = new System.Drawing.Point(187, 2);
            this.basicLabel2_1.Margin = new System.Windows.Forms.Padding(2);
            this.basicLabel2_1.Name = "basicLabel2_1";
            this.basicLabel2_1.Size = new System.Drawing.Size(54, 24);
            this.basicLabel2_1.TabIndex = 2;
            this.basicLabel2_1.Text = "外部效果";
            this.basicLabel2_1.TextAlign = System.Drawing.ContentAlignment.MiddleLeft;
            // 
            // _basicExternalEffectLabel
            // 
            this._basicExternalEffectLabel.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(58)))), ((int)(((byte)(58)))), ((int)(((byte)(58)))));
            this._basicExternalEffectLabel.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this._basicExternalEffectLabel.Dock = System.Windows.Forms.DockStyle.Fill;
            this._basicExternalEffectLabel.ForeColor = System.Drawing.Color.LightGray;
            this._basicExternalEffectLabel.Location = new System.Drawing.Point(245, 2);
            this._basicExternalEffectLabel.Margin = new System.Windows.Forms.Padding(2, 2, 4, 2);
            this._basicExternalEffectLabel.Name = "_basicExternalEffectLabel";
            this._basicExternalEffectLabel.Padding = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this._basicExternalEffectLabel.Size = new System.Drawing.Size(121, 24);
            this._basicExternalEffectLabel.TabIndex = 3;
            this._basicExternalEffectLabel.Text = "无";
            this._basicExternalEffectLabel.TextAlign = System.Drawing.ContentAlignment.MiddleLeft;
            // 
            // basicLabel2_2
            // 
            this.basicLabel2_2.BackColor = System.Drawing.Color.Transparent;
            this.basicLabel2_2.Dock = System.Windows.Forms.DockStyle.Fill;
            this.basicLabel2_2.Font = this.Font;
            this.basicLabel2_2.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this.basicLabel2_2.Location = new System.Drawing.Point(372, 2);
            this.basicLabel2_2.Margin = new System.Windows.Forms.Padding(2);
            this.basicLabel2_2.Name = "basicLabel2_2";
            this.basicLabel2_2.Size = new System.Drawing.Size(54, 24);
            this.basicLabel2_2.TabIndex = 4;
            this.basicLabel2_2.Text = "碎片";
            this.basicLabel2_2.TextAlign = System.Drawing.ContentAlignment.MiddleLeft;
            // 
            // _partCountNumeric
            // 
            this._partCountNumeric.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(58)))), ((int)(((byte)(58)))), ((int)(((byte)(58)))));
            this._partCountNumeric.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this._partCountNumeric.Dock = System.Windows.Forms.DockStyle.Fill;
            this._partCountNumeric.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this._partCountNumeric.Location = new System.Drawing.Point(430, 2);
            this._partCountNumeric.Margin = new System.Windows.Forms.Padding(2, 2, 4, 2);
            this._partCountNumeric.Maximum = new decimal(new int[] {
            1000000000,
            0,
            0,
            0});
            this._partCountNumeric.Minimum = new decimal(new int[] {
            1000000000,
            0,
            0,
            -2147483648});
            this._partCountNumeric.Name = "_partCountNumeric";
            this._partCountNumeric.Size = new System.Drawing.Size(123, 23);
            this._partCountNumeric.TabIndex = 5;
            this._partCountNumeric.ThousandsSeparator = true;
            // 
            // basicRow3
            // 
            this.basicRow3.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(47)))), ((int)(((byte)(47)))), ((int)(((byte)(47)))));
            this.basicRow3.ColumnCount = 6;
            this.basicRow3.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Absolute, 58F));
            this.basicRow3.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 33.3333F));
            this.basicRow3.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Absolute, 58F));
            this.basicRow3.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 33.3333F));
            this.basicRow3.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Absolute, 58F));
            this.basicRow3.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 33.3333F));
            this.basicRow3.Controls.Add(this.basicLabel3_0, 0, 0);
            this.basicRow3.Controls.Add(this._requiredClassComboBox, 1, 0);
            this.basicRow3.Controls.Add(this.basicLabel3_1, 2, 0);
            this.basicRow3.Controls.Add(this._basicSetSummaryLabel, 3, 0);
            this.basicRow3.Controls.Add(this.basicLabel3_2, 4, 0);
            this.basicRow3.Controls.Add(this._buffIconNumeric, 5, 0);
            this.basicRow3.Dock = System.Windows.Forms.DockStyle.Fill;
            this.basicRow3.Location = new System.Drawing.Point(0, 84);
            this.basicRow3.Margin = new System.Windows.Forms.Padding(0);
            this.basicRow3.Name = "basicRow3";
            this.basicRow3.RowCount = 1;
            this.basicRow3.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Absolute, 28F));
            this.basicRow3.Size = new System.Drawing.Size(557, 28);
            this.basicRow3.TabIndex = 3;
            // 
            // basicLabel3_0
            // 
            this.basicLabel3_0.BackColor = System.Drawing.Color.Transparent;
            this.basicLabel3_0.Dock = System.Windows.Forms.DockStyle.Fill;
            this.basicLabel3_0.Font = this.Font;
            this.basicLabel3_0.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this.basicLabel3_0.Location = new System.Drawing.Point(2, 2);
            this.basicLabel3_0.Margin = new System.Windows.Forms.Padding(2);
            this.basicLabel3_0.Name = "basicLabel3_0";
            this.basicLabel3_0.Size = new System.Drawing.Size(54, 24);
            this.basicLabel3_0.TabIndex = 0;
            this.basicLabel3_0.Text = "职业要求";
            this.basicLabel3_0.TextAlign = System.Drawing.ContentAlignment.MiddleLeft;
            // 
            // _requiredClassComboBox
            // 
            this._requiredClassComboBox.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(58)))), ((int)(((byte)(58)))), ((int)(((byte)(58)))));
            this._requiredClassComboBox.Dock = System.Windows.Forms.DockStyle.Fill;
            this._requiredClassComboBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this._requiredClassComboBox.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this._requiredClassComboBox.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this._requiredClassComboBox.Location = new System.Drawing.Point(60, 2);
            this._requiredClassComboBox.Margin = new System.Windows.Forms.Padding(2, 2, 4, 2);
            this._requiredClassComboBox.Name = "_requiredClassComboBox";
            this._requiredClassComboBox.Size = new System.Drawing.Size(121, 25);
            this._requiredClassComboBox.TabIndex = 1;
            // 
            // basicLabel3_1
            // 
            this.basicLabel3_1.BackColor = System.Drawing.Color.Transparent;
            this.basicLabel3_1.Dock = System.Windows.Forms.DockStyle.Fill;
            this.basicLabel3_1.Font = this.Font;
            this.basicLabel3_1.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this.basicLabel3_1.Location = new System.Drawing.Point(187, 2);
            this.basicLabel3_1.Margin = new System.Windows.Forms.Padding(2);
            this.basicLabel3_1.Name = "basicLabel3_1";
            this.basicLabel3_1.Size = new System.Drawing.Size(54, 24);
            this.basicLabel3_1.TabIndex = 2;
            this.basicLabel3_1.Text = "套装属性";
            this.basicLabel3_1.TextAlign = System.Drawing.ContentAlignment.MiddleLeft;
            // 
            // _basicSetSummaryLabel
            // 
            this._basicSetSummaryLabel.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(58)))), ((int)(((byte)(58)))), ((int)(((byte)(58)))));
            this._basicSetSummaryLabel.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this._basicSetSummaryLabel.Dock = System.Windows.Forms.DockStyle.Fill;
            this._basicSetSummaryLabel.ForeColor = System.Drawing.Color.LightGray;
            this._basicSetSummaryLabel.Location = new System.Drawing.Point(245, 2);
            this._basicSetSummaryLabel.Margin = new System.Windows.Forms.Padding(2, 2, 4, 2);
            this._basicSetSummaryLabel.Name = "_basicSetSummaryLabel";
            this._basicSetSummaryLabel.Padding = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this._basicSetSummaryLabel.Size = new System.Drawing.Size(121, 24);
            this._basicSetSummaryLabel.TabIndex = 3;
            this._basicSetSummaryLabel.Text = "无";
            this._basicSetSummaryLabel.TextAlign = System.Drawing.ContentAlignment.MiddleLeft;
            // 
            // basicLabel3_2
            // 
            this.basicLabel3_2.BackColor = System.Drawing.Color.Transparent;
            this.basicLabel3_2.Dock = System.Windows.Forms.DockStyle.Fill;
            this.basicLabel3_2.Font = this.Font;
            this.basicLabel3_2.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this.basicLabel3_2.Location = new System.Drawing.Point(372, 2);
            this.basicLabel3_2.Margin = new System.Windows.Forms.Padding(2);
            this.basicLabel3_2.Name = "basicLabel3_2";
            this.basicLabel3_2.Size = new System.Drawing.Size(54, 24);
            this.basicLabel3_2.TabIndex = 4;
            this.basicLabel3_2.Text = "BUFF图";
            this.basicLabel3_2.TextAlign = System.Drawing.ContentAlignment.MiddleLeft;
            // 
            // _buffIconNumeric
            // 
            this._buffIconNumeric.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(58)))), ((int)(((byte)(58)))), ((int)(((byte)(58)))));
            this._buffIconNumeric.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this._buffIconNumeric.Dock = System.Windows.Forms.DockStyle.Fill;
            this._buffIconNumeric.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this._buffIconNumeric.Location = new System.Drawing.Point(430, 2);
            this._buffIconNumeric.Margin = new System.Windows.Forms.Padding(2, 2, 4, 2);
            this._buffIconNumeric.Maximum = new decimal(new int[] {
            1000000000,
            0,
            0,
            0});
            this._buffIconNumeric.Minimum = new decimal(new int[] {
            1000000000,
            0,
            0,
            -2147483648});
            this._buffIconNumeric.Name = "_buffIconNumeric";
            this._buffIconNumeric.Size = new System.Drawing.Size(123, 23);
            this._buffIconNumeric.TabIndex = 5;
            this._buffIconNumeric.ThousandsSeparator = true;
            // 
            // basicRow4
            // 
            this.basicRow4.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(47)))), ((int)(((byte)(47)))), ((int)(((byte)(47)))));
            this.basicRow4.ColumnCount = 8;
            this.basicRow4.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Absolute, 52F));
            this.basicRow4.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 25F));
            this.basicRow4.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Absolute, 52F));
            this.basicRow4.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 25F));
            this.basicRow4.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Absolute, 52F));
            this.basicRow4.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 25F));
            this.basicRow4.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Absolute, 52F));
            this.basicRow4.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 25F));
            this.basicRow4.Controls.Add(this.basicLabel4_0, 0, 0);
            this.basicRow4.Controls.Add(this._weightNumeric, 1, 0);
            this.basicRow4.Controls.Add(this.basicLabel4_1, 2, 0);
            this.basicRow4.Controls.Add(this._durabilityNumeric, 3, 0);
            this.basicRow4.Controls.Add(this.basicLabel4_2, 4, 0);
            this.basicRow4.Controls.Add(this._priceNumeric, 5, 0);
            this.basicRow4.Controls.Add(this.basicLabel4_3, 6, 0);
            this.basicRow4.Controls.Add(this._sellRateNumeric, 7, 0);
            this.basicRow4.Dock = System.Windows.Forms.DockStyle.Fill;
            this.basicRow4.Location = new System.Drawing.Point(0, 112);
            this.basicRow4.Margin = new System.Windows.Forms.Padding(0);
            this.basicRow4.Name = "basicRow4";
            this.basicRow4.RowCount = 1;
            this.basicRow4.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Absolute, 28F));
            this.basicRow4.Size = new System.Drawing.Size(557, 28);
            this.basicRow4.TabIndex = 4;
            // 
            // basicLabel4_0
            // 
            this.basicLabel4_0.BackColor = System.Drawing.Color.Transparent;
            this.basicLabel4_0.Dock = System.Windows.Forms.DockStyle.Fill;
            this.basicLabel4_0.Font = new System.Drawing.Font("宋体", 7F);
            this.basicLabel4_0.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this.basicLabel4_0.Location = new System.Drawing.Point(2, 2);
            this.basicLabel4_0.Margin = new System.Windows.Forms.Padding(2);
            this.basicLabel4_0.Name = "basicLabel4_0";
            this.basicLabel4_0.Size = new System.Drawing.Size(48, 24);
            this.basicLabel4_0.TabIndex = 0;
            this.basicLabel4_0.Text = "重量";
            this.basicLabel4_0.TextAlign = System.Drawing.ContentAlignment.MiddleLeft;
            // 
            // _weightNumeric
            // 
            this._weightNumeric.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(58)))), ((int)(((byte)(58)))), ((int)(((byte)(58)))));
            this._weightNumeric.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this._weightNumeric.Dock = System.Windows.Forms.DockStyle.Fill;
            this._weightNumeric.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this._weightNumeric.Location = new System.Drawing.Point(54, 2);
            this._weightNumeric.Margin = new System.Windows.Forms.Padding(2, 2, 4, 2);
            this._weightNumeric.Maximum = new decimal(new int[] {
            1000000000,
            0,
            0,
            0});
            this._weightNumeric.Minimum = new decimal(new int[] {
            1000000000,
            0,
            0,
            -2147483648});
            this._weightNumeric.Name = "_weightNumeric";
            this._weightNumeric.Size = new System.Drawing.Size(81, 23);
            this._weightNumeric.TabIndex = 1;
            this._weightNumeric.ThousandsSeparator = true;
            // 
            // basicLabel4_1
            // 
            this.basicLabel4_1.BackColor = System.Drawing.Color.Transparent;
            this.basicLabel4_1.Dock = System.Windows.Forms.DockStyle.Fill;
            this.basicLabel4_1.Font = new System.Drawing.Font("宋体", 7F);
            this.basicLabel4_1.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this.basicLabel4_1.Location = new System.Drawing.Point(141, 2);
            this.basicLabel4_1.Margin = new System.Windows.Forms.Padding(2);
            this.basicLabel4_1.Name = "basicLabel4_1";
            this.basicLabel4_1.Size = new System.Drawing.Size(48, 24);
            this.basicLabel4_1.TabIndex = 2;
            this.basicLabel4_1.Text = "持久";
            this.basicLabel4_1.TextAlign = System.Drawing.ContentAlignment.MiddleLeft;
            // 
            // _durabilityNumeric
            // 
            this._durabilityNumeric.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(58)))), ((int)(((byte)(58)))), ((int)(((byte)(58)))));
            this._durabilityNumeric.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this._durabilityNumeric.Dock = System.Windows.Forms.DockStyle.Fill;
            this._durabilityNumeric.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this._durabilityNumeric.Location = new System.Drawing.Point(193, 2);
            this._durabilityNumeric.Margin = new System.Windows.Forms.Padding(2, 2, 4, 2);
            this._durabilityNumeric.Maximum = new decimal(new int[] {
            1000000000,
            0,
            0,
            0});
            this._durabilityNumeric.Minimum = new decimal(new int[] {
            1000000000,
            0,
            0,
            -2147483648});
            this._durabilityNumeric.Name = "_durabilityNumeric";
            this._durabilityNumeric.Size = new System.Drawing.Size(81, 23);
            this._durabilityNumeric.TabIndex = 3;
            this._durabilityNumeric.ThousandsSeparator = true;
            // 
            // basicLabel4_2
            // 
            this.basicLabel4_2.BackColor = System.Drawing.Color.Transparent;
            this.basicLabel4_2.Dock = System.Windows.Forms.DockStyle.Fill;
            this.basicLabel4_2.Font = new System.Drawing.Font("宋体", 7F);
            this.basicLabel4_2.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this.basicLabel4_2.Location = new System.Drawing.Point(280, 2);
            this.basicLabel4_2.Margin = new System.Windows.Forms.Padding(2);
            this.basicLabel4_2.Name = "basicLabel4_2";
            this.basicLabel4_2.Size = new System.Drawing.Size(48, 24);
            this.basicLabel4_2.TabIndex = 4;
            this.basicLabel4_2.Text = "价格";
            this.basicLabel4_2.TextAlign = System.Drawing.ContentAlignment.MiddleLeft;
            // 
            // _priceNumeric
            // 
            this._priceNumeric.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(58)))), ((int)(((byte)(58)))), ((int)(((byte)(58)))));
            this._priceNumeric.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this._priceNumeric.Dock = System.Windows.Forms.DockStyle.Fill;
            this._priceNumeric.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this._priceNumeric.Location = new System.Drawing.Point(332, 2);
            this._priceNumeric.Margin = new System.Windows.Forms.Padding(2, 2, 4, 2);
            this._priceNumeric.Maximum = new decimal(new int[] {
            1000000000,
            0,
            0,
            0});
            this._priceNumeric.Minimum = new decimal(new int[] {
            1000000000,
            0,
            0,
            -2147483648});
            this._priceNumeric.Name = "_priceNumeric";
            this._priceNumeric.Size = new System.Drawing.Size(81, 23);
            this._priceNumeric.TabIndex = 5;
            this._priceNumeric.ThousandsSeparator = true;
            // 
            // basicLabel4_3
            // 
            this.basicLabel4_3.BackColor = System.Drawing.Color.Transparent;
            this.basicLabel4_3.Dock = System.Windows.Forms.DockStyle.Fill;
            this.basicLabel4_3.Font = new System.Drawing.Font("宋体", 7F);
            this.basicLabel4_3.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this.basicLabel4_3.Location = new System.Drawing.Point(419, 2);
            this.basicLabel4_3.Margin = new System.Windows.Forms.Padding(2);
            this.basicLabel4_3.Name = "basicLabel4_3";
            this.basicLabel4_3.Size = new System.Drawing.Size(48, 24);
            this.basicLabel4_3.TabIndex = 6;
            this.basicLabel4_3.Text = "出售率";
            this.basicLabel4_3.TextAlign = System.Drawing.ContentAlignment.MiddleLeft;
            // 
            // _sellRateNumeric
            // 
            this._sellRateNumeric.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(58)))), ((int)(((byte)(58)))), ((int)(((byte)(58)))));
            this._sellRateNumeric.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this._sellRateNumeric.DecimalPlaces = 4;
            this._sellRateNumeric.Dock = System.Windows.Forms.DockStyle.Fill;
            this._sellRateNumeric.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this._sellRateNumeric.Increment = new decimal(new int[] {
            1,
            0,
            0,
            65536});
            this._sellRateNumeric.Location = new System.Drawing.Point(471, 2);
            this._sellRateNumeric.Margin = new System.Windows.Forms.Padding(2, 2, 4, 2);
            this._sellRateNumeric.Maximum = new decimal(new int[] {
            1000000,
            0,
            0,
            0});
            this._sellRateNumeric.Minimum = new decimal(new int[] {
            1000000,
            0,
            0,
            -2147483648});
            this._sellRateNumeric.Name = "_sellRateNumeric";
            this._sellRateNumeric.Size = new System.Drawing.Size(82, 23);
            this._sellRateNumeric.TabIndex = 7;
            this._sellRateNumeric.ThousandsSeparator = true;
            // 
            // basicRow5
            // 
            this.basicRow5.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(47)))), ((int)(((byte)(47)))), ((int)(((byte)(47)))));
            this.basicRow5.ColumnCount = 8;
            this.basicRow5.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Absolute, 52F));
            this.basicRow5.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 25F));
            this.basicRow5.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Absolute, 52F));
            this.basicRow5.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 25F));
            this.basicRow5.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Absolute, 52F));
            this.basicRow5.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 25F));
            this.basicRow5.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Absolute, 52F));
            this.basicRow5.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 25F));
            this.basicRow5.Controls.Add(this.basicLabel5_0, 0, 0);
            this.basicRow5.Controls.Add(this._rarityComboBox, 1, 0);
            this.basicRow5.Controls.Add(this.basicLabel5_1, 2, 0);
            this.basicRow5.Controls.Add(this._stackSizeNumeric, 3, 0);
            this.basicRow5.Controls.Add(this.basicLabel5_2, 4, 0);
            this.basicRow5.Controls.Add(this._basicInventoryWidthLabel, 5, 0);
            this.basicRow5.Controls.Add(this.basicLabel5_3, 6, 0);
            this.basicRow5.Controls.Add(this._basicInventoryHeightLabel, 7, 0);
            this.basicRow5.Dock = System.Windows.Forms.DockStyle.Fill;
            this.basicRow5.Location = new System.Drawing.Point(0, 140);
            this.basicRow5.Margin = new System.Windows.Forms.Padding(0);
            this.basicRow5.Name = "basicRow5";
            this.basicRow5.RowCount = 1;
            this.basicRow5.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Absolute, 28F));
            this.basicRow5.Size = new System.Drawing.Size(557, 28);
            this.basicRow5.TabIndex = 5;
            // 
            // basicLabel5_0
            // 
            this.basicLabel5_0.BackColor = System.Drawing.Color.Transparent;
            this.basicLabel5_0.Dock = System.Windows.Forms.DockStyle.Fill;
            this.basicLabel5_0.Font = new System.Drawing.Font("宋体", 7F);
            this.basicLabel5_0.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this.basicLabel5_0.Location = new System.Drawing.Point(2, 2);
            this.basicLabel5_0.Margin = new System.Windows.Forms.Padding(2);
            this.basicLabel5_0.Name = "basicLabel5_0";
            this.basicLabel5_0.Size = new System.Drawing.Size(48, 24);
            this.basicLabel5_0.TabIndex = 0;
            this.basicLabel5_0.Text = "装备品质";
            this.basicLabel5_0.TextAlign = System.Drawing.ContentAlignment.MiddleLeft;
            // 
            // _rarityComboBox
            // 
            this._rarityComboBox.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(58)))), ((int)(((byte)(58)))), ((int)(((byte)(58)))));
            this._rarityComboBox.Dock = System.Windows.Forms.DockStyle.Fill;
            this._rarityComboBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this._rarityComboBox.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this._rarityComboBox.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this._rarityComboBox.Location = new System.Drawing.Point(54, 2);
            this._rarityComboBox.Margin = new System.Windows.Forms.Padding(2, 2, 4, 2);
            this._rarityComboBox.Name = "_rarityComboBox";
            this._rarityComboBox.Size = new System.Drawing.Size(81, 25);
            this._rarityComboBox.TabIndex = 1;
            // 
            // basicLabel5_1
            // 
            this.basicLabel5_1.BackColor = System.Drawing.Color.Transparent;
            this.basicLabel5_1.Dock = System.Windows.Forms.DockStyle.Fill;
            this.basicLabel5_1.Font = new System.Drawing.Font("宋体", 7F);
            this.basicLabel5_1.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this.basicLabel5_1.Location = new System.Drawing.Point(141, 2);
            this.basicLabel5_1.Margin = new System.Windows.Forms.Padding(2);
            this.basicLabel5_1.Name = "basicLabel5_1";
            this.basicLabel5_1.Size = new System.Drawing.Size(48, 24);
            this.basicLabel5_1.TabIndex = 2;
            this.basicLabel5_1.Text = "堆叠";
            this.basicLabel5_1.TextAlign = System.Drawing.ContentAlignment.MiddleLeft;
            // 
            // _stackSizeNumeric
            // 
            this._stackSizeNumeric.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(58)))), ((int)(((byte)(58)))), ((int)(((byte)(58)))));
            this._stackSizeNumeric.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this._stackSizeNumeric.Dock = System.Windows.Forms.DockStyle.Fill;
            this._stackSizeNumeric.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this._stackSizeNumeric.Location = new System.Drawing.Point(193, 2);
            this._stackSizeNumeric.Margin = new System.Windows.Forms.Padding(2, 2, 4, 2);
            this._stackSizeNumeric.Maximum = new decimal(new int[] {
            1000000000,
            0,
            0,
            0});
            this._stackSizeNumeric.Minimum = new decimal(new int[] {
            1000000000,
            0,
            0,
            -2147483648});
            this._stackSizeNumeric.Name = "_stackSizeNumeric";
            this._stackSizeNumeric.Size = new System.Drawing.Size(81, 23);
            this._stackSizeNumeric.TabIndex = 3;
            this._stackSizeNumeric.ThousandsSeparator = true;
            // 
            // basicLabel5_2
            // 
            this.basicLabel5_2.BackColor = System.Drawing.Color.Transparent;
            this.basicLabel5_2.Dock = System.Windows.Forms.DockStyle.Fill;
            this.basicLabel5_2.Font = new System.Drawing.Font("宋体", 7F);
            this.basicLabel5_2.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this.basicLabel5_2.Location = new System.Drawing.Point(280, 2);
            this.basicLabel5_2.Margin = new System.Windows.Forms.Padding(2);
            this.basicLabel5_2.Name = "basicLabel5_2";
            this.basicLabel5_2.Size = new System.Drawing.Size(48, 24);
            this.basicLabel5_2.TabIndex = 4;
            this.basicLabel5_2.Text = "物品宽度";
            this.basicLabel5_2.TextAlign = System.Drawing.ContentAlignment.MiddleLeft;
            // 
            // _basicInventoryWidthLabel
            // 
            this._basicInventoryWidthLabel.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(58)))), ((int)(((byte)(58)))), ((int)(((byte)(58)))));
            this._basicInventoryWidthLabel.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this._basicInventoryWidthLabel.Dock = System.Windows.Forms.DockStyle.Fill;
            this._basicInventoryWidthLabel.ForeColor = System.Drawing.Color.LightGray;
            this._basicInventoryWidthLabel.Location = new System.Drawing.Point(332, 2);
            this._basicInventoryWidthLabel.Margin = new System.Windows.Forms.Padding(2, 2, 4, 2);
            this._basicInventoryWidthLabel.Name = "_basicInventoryWidthLabel";
            this._basicInventoryWidthLabel.Padding = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this._basicInventoryWidthLabel.Size = new System.Drawing.Size(81, 24);
            this._basicInventoryWidthLabel.TabIndex = 5;
            this._basicInventoryWidthLabel.Text = "-";
            this._basicInventoryWidthLabel.TextAlign = System.Drawing.ContentAlignment.MiddleLeft;
            // 
            // basicLabel5_3
            // 
            this.basicLabel5_3.BackColor = System.Drawing.Color.Transparent;
            this.basicLabel5_3.Dock = System.Windows.Forms.DockStyle.Fill;
            this.basicLabel5_3.Font = new System.Drawing.Font("宋体", 7F);
            this.basicLabel5_3.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this.basicLabel5_3.Location = new System.Drawing.Point(419, 2);
            this.basicLabel5_3.Margin = new System.Windows.Forms.Padding(2);
            this.basicLabel5_3.Name = "basicLabel5_3";
            this.basicLabel5_3.Size = new System.Drawing.Size(48, 24);
            this.basicLabel5_3.TabIndex = 6;
            this.basicLabel5_3.Text = "物品高度";
            this.basicLabel5_3.TextAlign = System.Drawing.ContentAlignment.MiddleLeft;
            // 
            // _basicInventoryHeightLabel
            // 
            this._basicInventoryHeightLabel.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(58)))), ((int)(((byte)(58)))), ((int)(((byte)(58)))));
            this._basicInventoryHeightLabel.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this._basicInventoryHeightLabel.Dock = System.Windows.Forms.DockStyle.Fill;
            this._basicInventoryHeightLabel.ForeColor = System.Drawing.Color.LightGray;
            this._basicInventoryHeightLabel.Location = new System.Drawing.Point(471, 2);
            this._basicInventoryHeightLabel.Margin = new System.Windows.Forms.Padding(2, 2, 4, 2);
            this._basicInventoryHeightLabel.Name = "_basicInventoryHeightLabel";
            this._basicInventoryHeightLabel.Padding = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this._basicInventoryHeightLabel.Size = new System.Drawing.Size(82, 24);
            this._basicInventoryHeightLabel.TabIndex = 7;
            this._basicInventoryHeightLabel.Text = "-";
            this._basicInventoryHeightLabel.TextAlign = System.Drawing.ContentAlignment.MiddleLeft;
            // 
            // basicRow6
            // 
            this.basicRow6.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(47)))), ((int)(((byte)(47)))), ((int)(((byte)(47)))));
            this.basicRow6.ColumnCount = 6;
            this.basicRow6.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Absolute, 58F));
            this.basicRow6.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 33.3333F));
            this.basicRow6.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Absolute, 58F));
            this.basicRow6.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 33.3333F));
            this.basicRow6.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Absolute, 58F));
            this.basicRow6.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 33.3333F));
            this.basicRow6.Controls.Add(this.basicLabel6_0, 0, 0);
            this.basicRow6.Controls.Add(this._weaponTypeComboBox, 1, 0);
            this.basicRow6.Controls.Add(this.basicLabel6_1, 2, 0);
            this.basicRow6.Controls.Add(this._requiredGenderComboBox, 3, 0);
            this.basicRow6.Controls.Add(this.basicLabel6_2, 4, 0);
            this.basicRow6.Controls.Add(this._durationNumeric, 5, 0);
            this.basicRow6.Dock = System.Windows.Forms.DockStyle.Fill;
            this.basicRow6.Location = new System.Drawing.Point(0, 168);
            this.basicRow6.Margin = new System.Windows.Forms.Padding(0);
            this.basicRow6.Name = "basicRow6";
            this.basicRow6.RowCount = 1;
            this.basicRow6.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Absolute, 28F));
            this.basicRow6.Size = new System.Drawing.Size(557, 28);
            this.basicRow6.TabIndex = 6;
            // 
            // basicLabel6_0
            // 
            this.basicLabel6_0.BackColor = System.Drawing.Color.Transparent;
            this.basicLabel6_0.Dock = System.Windows.Forms.DockStyle.Fill;
            this.basicLabel6_0.Font = this.Font;
            this.basicLabel6_0.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this.basicLabel6_0.Location = new System.Drawing.Point(2, 2);
            this.basicLabel6_0.Margin = new System.Windows.Forms.Padding(2);
            this.basicLabel6_0.Name = "basicLabel6_0";
            this.basicLabel6_0.Size = new System.Drawing.Size(54, 24);
            this.basicLabel6_0.TabIndex = 0;
            this.basicLabel6_0.Text = "武器类型";
            this.basicLabel6_0.TextAlign = System.Drawing.ContentAlignment.MiddleLeft;
            // 
            // _weaponTypeComboBox
            // 
            this._weaponTypeComboBox.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(58)))), ((int)(((byte)(58)))), ((int)(((byte)(58)))));
            this._weaponTypeComboBox.Dock = System.Windows.Forms.DockStyle.Fill;
            this._weaponTypeComboBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this._weaponTypeComboBox.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this._weaponTypeComboBox.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this._weaponTypeComboBox.Location = new System.Drawing.Point(60, 2);
            this._weaponTypeComboBox.Margin = new System.Windows.Forms.Padding(2, 2, 4, 2);
            this._weaponTypeComboBox.Name = "_weaponTypeComboBox";
            this._weaponTypeComboBox.Size = new System.Drawing.Size(121, 25);
            this._weaponTypeComboBox.TabIndex = 1;
            // 
            // basicLabel6_1
            // 
            this.basicLabel6_1.BackColor = System.Drawing.Color.Transparent;
            this.basicLabel6_1.Dock = System.Windows.Forms.DockStyle.Fill;
            this.basicLabel6_1.Font = this.Font;
            this.basicLabel6_1.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this.basicLabel6_1.Location = new System.Drawing.Point(187, 2);
            this.basicLabel6_1.Margin = new System.Windows.Forms.Padding(2);
            this.basicLabel6_1.Name = "basicLabel6_1";
            this.basicLabel6_1.Size = new System.Drawing.Size(54, 24);
            this.basicLabel6_1.TabIndex = 2;
            this.basicLabel6_1.Text = "要求性别";
            this.basicLabel6_1.TextAlign = System.Drawing.ContentAlignment.MiddleLeft;
            // 
            // _requiredGenderComboBox
            // 
            this._requiredGenderComboBox.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(58)))), ((int)(((byte)(58)))), ((int)(((byte)(58)))));
            this._requiredGenderComboBox.Dock = System.Windows.Forms.DockStyle.Fill;
            this._requiredGenderComboBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this._requiredGenderComboBox.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this._requiredGenderComboBox.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this._requiredGenderComboBox.Location = new System.Drawing.Point(245, 2);
            this._requiredGenderComboBox.Margin = new System.Windows.Forms.Padding(2, 2, 4, 2);
            this._requiredGenderComboBox.Name = "_requiredGenderComboBox";
            this._requiredGenderComboBox.Size = new System.Drawing.Size(121, 25);
            this._requiredGenderComboBox.TabIndex = 3;
            // 
            // basicLabel6_2
            // 
            this.basicLabel6_2.BackColor = System.Drawing.Color.Transparent;
            this.basicLabel6_2.Dock = System.Windows.Forms.DockStyle.Fill;
            this.basicLabel6_2.Font = this.Font;
            this.basicLabel6_2.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this.basicLabel6_2.Location = new System.Drawing.Point(372, 2);
            this.basicLabel6_2.Margin = new System.Windows.Forms.Padding(2);
            this.basicLabel6_2.Name = "basicLabel6_2";
            this.basicLabel6_2.Size = new System.Drawing.Size(54, 24);
            this.basicLabel6_2.TabIndex = 4;
            this.basicLabel6_2.Text = "使用时长";
            this.basicLabel6_2.TextAlign = System.Drawing.ContentAlignment.MiddleLeft;
            // 
            // _durationNumeric
            // 
            this._durationNumeric.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(58)))), ((int)(((byte)(58)))), ((int)(((byte)(58)))));
            this._durationNumeric.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this._durationNumeric.Dock = System.Windows.Forms.DockStyle.Fill;
            this._durationNumeric.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this._durationNumeric.Location = new System.Drawing.Point(430, 2);
            this._durationNumeric.Margin = new System.Windows.Forms.Padding(2, 2, 4, 2);
            this._durationNumeric.Maximum = new decimal(new int[] {
            1000000000,
            0,
            0,
            0});
            this._durationNumeric.Minimum = new decimal(new int[] {
            1000000000,
            0,
            0,
            -2147483648});
            this._durationNumeric.Name = "_durationNumeric";
            this._durationNumeric.Size = new System.Drawing.Size(123, 23);
            this._durationNumeric.TabIndex = 5;
            this._durationNumeric.ThousandsSeparator = true;
            // 
            // flags
            // 
            this.flags.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(47)))), ((int)(((byte)(47)))), ((int)(((byte)(47)))));
            this.flags.Controls.Add(this.flagStartItem);
            this.flags.Controls.Add(this.flagCanRepair);
            this.flags.Controls.Add(this.flagCanSell);
            this.flags.Controls.Add(this.flagCanStore);
            this.flags.Controls.Add(this.flagCanTreasure);
            this.flags.Controls.Add(this.flagCanTrade);
            this.flags.Controls.Add(this.flagNoMake);
            this.flags.Controls.Add(this.flagCanDrop);
            this.flags.Controls.Add(this.flagCanDeathDrop);
            this.flags.Controls.Add(this.flagCanAutoPot);
            this.flags.Dock = System.Windows.Forms.DockStyle.Fill;
            this.flags.Location = new System.Drawing.Point(0, 196);
            this.flags.Margin = new System.Windows.Forms.Padding(0);
            this.flags.Name = "flags";
            this.flags.Size = new System.Drawing.Size(557, 54);
            this.flags.TabIndex = 7;
            // 
            // flagStartItem
            // 
            this.flagStartItem.AutoSize = true;
            this.flagStartItem.BackColor = System.Drawing.Color.Transparent;
            this.flagStartItem.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this.flagStartItem.Location = new System.Drawing.Point(3, 3);
            this.flagStartItem.Margin = new System.Windows.Forms.Padding(3, 3, 12, 3);
            this.flagStartItem.Name = "flagStartItem";
            this.flagStartItem.Size = new System.Drawing.Size(75, 21);
            this.flagStartItem.TabIndex = 0;
            this.flagStartItem.Tag = "StartItem";
            this.flagStartItem.Text = "新手赠送";
            this.flagStartItem.UseVisualStyleBackColor = false;
            // 
            // flagCanRepair
            // 
            this.flagCanRepair.AutoSize = true;
            this.flagCanRepair.BackColor = System.Drawing.Color.Transparent;
            this.flagCanRepair.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this.flagCanRepair.Location = new System.Drawing.Point(93, 3);
            this.flagCanRepair.Margin = new System.Windows.Forms.Padding(3, 3, 12, 3);
            this.flagCanRepair.Name = "flagCanRepair";
            this.flagCanRepair.Size = new System.Drawing.Size(63, 21);
            this.flagCanRepair.TabIndex = 1;
            this.flagCanRepair.Tag = "CanRepair";
            this.flagCanRepair.Text = "可修理";
            this.flagCanRepair.UseVisualStyleBackColor = false;
            // 
            // flagCanSell
            // 
            this.flagCanSell.AutoSize = true;
            this.flagCanSell.BackColor = System.Drawing.Color.Transparent;
            this.flagCanSell.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this.flagCanSell.Location = new System.Drawing.Point(171, 3);
            this.flagCanSell.Margin = new System.Windows.Forms.Padding(3, 3, 12, 3);
            this.flagCanSell.Name = "flagCanSell";
            this.flagCanSell.Size = new System.Drawing.Size(63, 21);
            this.flagCanSell.TabIndex = 2;
            this.flagCanSell.Tag = "CanSell";
            this.flagCanSell.Text = "可买卖";
            this.flagCanSell.UseVisualStyleBackColor = false;
            // 
            // flagCanStore
            // 
            this.flagCanStore.AutoSize = true;
            this.flagCanStore.BackColor = System.Drawing.Color.Transparent;
            this.flagCanStore.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this.flagCanStore.Location = new System.Drawing.Point(249, 3);
            this.flagCanStore.Margin = new System.Windows.Forms.Padding(3, 3, 12, 3);
            this.flagCanStore.Name = "flagCanStore";
            this.flagCanStore.Size = new System.Drawing.Size(63, 21);
            this.flagCanStore.TabIndex = 3;
            this.flagCanStore.Tag = "CanStore";
            this.flagCanStore.Text = "可存储";
            this.flagCanStore.UseVisualStyleBackColor = false;
            // 
            // flagCanTreasure
            // 
            this.flagCanTreasure.AutoSize = true;
            this.flagCanTreasure.BackColor = System.Drawing.Color.Transparent;
            this.flagCanTreasure.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this.flagCanTreasure.Location = new System.Drawing.Point(327, 3);
            this.flagCanTreasure.Margin = new System.Windows.Forms.Padding(3, 3, 12, 3);
            this.flagCanTreasure.Name = "flagCanTreasure";
            this.flagCanTreasure.Size = new System.Drawing.Size(75, 21);
            this.flagCanTreasure.TabIndex = 4;
            this.flagCanTreasure.Tag = "CanTreasure";
            this.flagCanTreasure.Text = "宝箱获得";
            this.flagCanTreasure.UseVisualStyleBackColor = false;
            // 
            // flagCanTrade
            // 
            this.flagCanTrade.AutoSize = true;
            this.flagCanTrade.BackColor = System.Drawing.Color.Transparent;
            this.flagCanTrade.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this.flagCanTrade.Location = new System.Drawing.Point(417, 3);
            this.flagCanTrade.Margin = new System.Windows.Forms.Padding(3, 3, 12, 3);
            this.flagCanTrade.Name = "flagCanTrade";
            this.flagCanTrade.Size = new System.Drawing.Size(63, 21);
            this.flagCanTrade.TabIndex = 5;
            this.flagCanTrade.Tag = "CanTrade";
            this.flagCanTrade.Text = "可寄售";
            this.flagCanTrade.UseVisualStyleBackColor = false;
            // 
            // flagNoMake
            // 
            this.flagNoMake.AutoSize = true;
            this.flagNoMake.BackColor = System.Drawing.Color.Transparent;
            this.flagNoMake.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this.flagNoMake.Location = new System.Drawing.Point(3, 30);
            this.flagNoMake.Margin = new System.Windows.Forms.Padding(3, 3, 12, 3);
            this.flagNoMake.Name = "flagNoMake";
            this.flagNoMake.Size = new System.Drawing.Size(75, 21);
            this.flagNoMake.TabIndex = 6;
            this.flagNoMake.Tag = "NoMake";
            this.flagNoMake.Text = "不可制造";
            this.flagNoMake.UseVisualStyleBackColor = false;
            // 
            // flagCanDrop
            // 
            this.flagCanDrop.AutoSize = true;
            this.flagCanDrop.BackColor = System.Drawing.Color.Transparent;
            this.flagCanDrop.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this.flagCanDrop.Location = new System.Drawing.Point(93, 30);
            this.flagCanDrop.Margin = new System.Windows.Forms.Padding(3, 3, 12, 3);
            this.flagCanDrop.Name = "flagCanDrop";
            this.flagCanDrop.Size = new System.Drawing.Size(63, 21);
            this.flagCanDrop.TabIndex = 7;
            this.flagCanDrop.Tag = "CanDrop";
            this.flagCanDrop.Text = "可丢弃";
            this.flagCanDrop.UseVisualStyleBackColor = false;
            // 
            // flagCanDeathDrop
            // 
            this.flagCanDeathDrop.AutoSize = true;
            this.flagCanDeathDrop.BackColor = System.Drawing.Color.Transparent;
            this.flagCanDeathDrop.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this.flagCanDeathDrop.Location = new System.Drawing.Point(171, 30);
            this.flagCanDeathDrop.Margin = new System.Windows.Forms.Padding(3, 3, 12, 3);
            this.flagCanDeathDrop.Name = "flagCanDeathDrop";
            this.flagCanDeathDrop.Size = new System.Drawing.Size(75, 21);
            this.flagCanDeathDrop.TabIndex = 8;
            this.flagCanDeathDrop.Tag = "CanDeathDrop";
            this.flagCanDeathDrop.Text = "死亡掉落";
            this.flagCanDeathDrop.UseVisualStyleBackColor = false;
            // 
            // flagCanAutoPot
            // 
            this.flagCanAutoPot.AutoSize = true;
            this.flagCanAutoPot.BackColor = System.Drawing.Color.Transparent;
            this.flagCanAutoPot.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this.flagCanAutoPot.Location = new System.Drawing.Point(261, 30);
            this.flagCanAutoPot.Margin = new System.Windows.Forms.Padding(3, 3, 12, 3);
            this.flagCanAutoPot.Name = "flagCanAutoPot";
            this.flagCanAutoPot.Size = new System.Drawing.Size(75, 21);
            this.flagCanAutoPot.TabIndex = 9;
            this.flagCanAutoPot.Tag = "CanAutoPot";
            this.flagCanAutoPot.Text = "自动物品";
            this.flagCanAutoPot.UseVisualStyleBackColor = false;
            // 
            // descriptionRow
            // 
            this.descriptionRow.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(47)))), ((int)(((byte)(47)))), ((int)(((byte)(47)))));
            this.descriptionRow.ColumnCount = 2;
            this.descriptionRow.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Absolute, 58F));
            this.descriptionRow.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 100F));
            this.descriptionRow.Controls.Add(this.descriptionLabel, 0, 0);
            this.descriptionRow.Controls.Add(this._descriptionTextBox, 1, 0);
            this.descriptionRow.Dock = System.Windows.Forms.DockStyle.Fill;
            this.descriptionRow.Location = new System.Drawing.Point(0, 250);
            this.descriptionRow.Margin = new System.Windows.Forms.Padding(0);
            this.descriptionRow.Name = "descriptionRow";
            this.descriptionRow.RowCount = 1;
            this.descriptionRow.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Absolute, 88F));
            this.descriptionRow.Size = new System.Drawing.Size(557, 88);
            this.descriptionRow.TabIndex = 8;
            // 
            // descriptionLabel
            // 
            this.descriptionLabel.BackColor = System.Drawing.Color.Transparent;
            this.descriptionLabel.Dock = System.Windows.Forms.DockStyle.Fill;
            this.descriptionLabel.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this.descriptionLabel.Location = new System.Drawing.Point(2, 2);
            this.descriptionLabel.Margin = new System.Windows.Forms.Padding(2);
            this.descriptionLabel.Name = "descriptionLabel";
            this.descriptionLabel.Size = new System.Drawing.Size(54, 84);
            this.descriptionLabel.TabIndex = 0;
            this.descriptionLabel.Text = "描述文件";
            this.descriptionLabel.TextAlign = System.Drawing.ContentAlignment.MiddleLeft;
            // 
            // _descriptionTextBox
            // 
            this._descriptionTextBox.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(58)))), ((int)(((byte)(58)))), ((int)(((byte)(58)))));
            this._descriptionTextBox.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this._descriptionTextBox.Dock = System.Windows.Forms.DockStyle.Fill;
            this._descriptionTextBox.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this._descriptionTextBox.Location = new System.Drawing.Point(58, 0);
            this._descriptionTextBox.Margin = new System.Windows.Forms.Padding(0);
            this._descriptionTextBox.Multiline = true;
            this._descriptionTextBox.Name = "_descriptionTextBox";
            this._descriptionTextBox.ScrollBars = System.Windows.Forms.ScrollBars.Vertical;
            this._descriptionTextBox.Size = new System.Drawing.Size(499, 88);
            this._descriptionTextBox.TabIndex = 1;
            // 
            // basicSpacer
            // 
            this.basicSpacer.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(47)))), ((int)(((byte)(47)))), ((int)(((byte)(47)))));
            this.basicSpacer.Dock = System.Windows.Forms.DockStyle.Fill;
            this.basicSpacer.Location = new System.Drawing.Point(0, 338);
            this.basicSpacer.Margin = new System.Windows.Forms.Padding(0);
            this.basicSpacer.Name = "basicSpacer";
            this.basicSpacer.Size = new System.Drawing.Size(557, 34);
            this.basicSpacer.TabIndex = 9;
            // 
            // statsGroup
            // 
            this.statsGroup.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(47)))), ((int)(((byte)(47)))), ((int)(((byte)(47)))));
            this.statsGroup.Controls.Add(this.statsTable);
            this.statsGroup.Dock = System.Windows.Forms.DockStyle.Fill;
            this.statsGroup.ForeColor = System.Drawing.Color.Yellow;
            this.statsGroup.Location = new System.Drawing.Point(570, 0);
            this.statsGroup.Margin = new System.Windows.Forms.Padding(0, 0, 6, 0);
            this.statsGroup.Name = "statsGroup";
            this.statsGroup.Padding = new System.Windows.Forms.Padding(8, 24, 8, 8);
            this.statsGroup.Size = new System.Drawing.Size(222, 420);
            this.statsGroup.TabIndex = 1;
            this.statsGroup.TabStop = false;
            this.statsGroup.Text = "附加属性";
            // 
            // statsTable
            // 
            this.statsTable.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(47)))), ((int)(((byte)(47)))), ((int)(((byte)(47)))));
            this.statsTable.ColumnCount = 1;
            this.statsTable.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Absolute, 209F));
            this.statsTable.Controls.Add(this._itemStatsListView, 0, 0);
            this.statsTable.Controls.Add(this.statsEditor, 0, 1);
            this.statsTable.Dock = System.Windows.Forms.DockStyle.Fill;
            this.statsTable.Location = new System.Drawing.Point(8, 40);
            this.statsTable.Name = "statsTable";
            this.statsTable.RowCount = 2;
            this.statsTable.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 100F));
            this.statsTable.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Absolute, 66F));
            this.statsTable.Size = new System.Drawing.Size(206, 372);
            this.statsTable.TabIndex = 0;
            // 
            // _itemStatsListView
            // 
            this._itemStatsListView.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(58)))), ((int)(((byte)(58)))), ((int)(((byte)(58)))));
            this._itemStatsListView.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this._itemStatsListView.Dock = System.Windows.Forms.DockStyle.Fill;
            this._itemStatsListView.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this._itemStatsListView.FullRowSelect = true;
            this._itemStatsListView.GridLines = true;
            this._itemStatsListView.HideSelection = false;
            this._itemStatsListView.Location = new System.Drawing.Point(3, 3);
            this._itemStatsListView.MultiSelect = false;
            this._itemStatsListView.Name = "_itemStatsListView";
            this._itemStatsListView.Size = new System.Drawing.Size(203, 300);
            this._itemStatsListView.TabIndex = 0;
            this._itemStatsListView.UseCompatibleStateImageBehavior = false;
            this._itemStatsListView.View = System.Windows.Forms.View.Details;
            // 
            // statsEditor
            // 
            this.statsEditor.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(47)))), ((int)(((byte)(47)))), ((int)(((byte)(47)))));
            this.statsEditor.ColumnCount = 3;
            this.statsEditor.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 48F));
            this.statsEditor.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 22F));
            this.statsEditor.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 30F));
            this.statsEditor.Controls.Add(this._itemStatComboBox, 0, 0);
            this.statsEditor.Controls.Add(this._itemStatAmountNumeric, 1, 0);
            this.statsEditor.Controls.Add(this._itemStatHiddenCheckBox, 2, 0);
            this.statsEditor.Controls.Add(this.addStatButton, 0, 1);
            this.statsEditor.Controls.Add(this.modifyStatButton, 1, 1);
            this.statsEditor.Controls.Add(this.deleteStatButton, 2, 1);
            this.statsEditor.Dock = System.Windows.Forms.DockStyle.Fill;
            this.statsEditor.Location = new System.Drawing.Point(0, 306);
            this.statsEditor.Margin = new System.Windows.Forms.Padding(0);
            this.statsEditor.Name = "statsEditor";
            this.statsEditor.RowCount = 2;
            this.statsEditor.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 50F));
            this.statsEditor.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 50F));
            this.statsEditor.Size = new System.Drawing.Size(209, 66);
            this.statsEditor.TabIndex = 1;
            // 
            // _itemStatComboBox
            // 
            this._itemStatComboBox.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(58)))), ((int)(((byte)(58)))), ((int)(((byte)(58)))));
            this._itemStatComboBox.Dock = System.Windows.Forms.DockStyle.Fill;
            this._itemStatComboBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this._itemStatComboBox.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this._itemStatComboBox.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this._itemStatComboBox.Location = new System.Drawing.Point(2, 2);
            this._itemStatComboBox.Margin = new System.Windows.Forms.Padding(2);
            this._itemStatComboBox.Name = "_itemStatComboBox";
            this._itemStatComboBox.Size = new System.Drawing.Size(96, 25);
            this._itemStatComboBox.TabIndex = 0;
            // 
            // _itemStatAmountNumeric
            // 
            this._itemStatAmountNumeric.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(58)))), ((int)(((byte)(58)))), ((int)(((byte)(58)))));
            this._itemStatAmountNumeric.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this._itemStatAmountNumeric.Dock = System.Windows.Forms.DockStyle.Fill;
            this._itemStatAmountNumeric.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this._itemStatAmountNumeric.Location = new System.Drawing.Point(102, 2);
            this._itemStatAmountNumeric.Margin = new System.Windows.Forms.Padding(2);
            this._itemStatAmountNumeric.Maximum = new decimal(new int[] {
            1000000000,
            0,
            0,
            0});
            this._itemStatAmountNumeric.Minimum = new decimal(new int[] {
            1000000000,
            0,
            0,
            -2147483648});
            this._itemStatAmountNumeric.Name = "_itemStatAmountNumeric";
            this._itemStatAmountNumeric.Size = new System.Drawing.Size(41, 23);
            this._itemStatAmountNumeric.TabIndex = 1;
            this._itemStatAmountNumeric.ThousandsSeparator = true;
            // 
            // _itemStatHiddenCheckBox
            // 
            this._itemStatHiddenCheckBox.Dock = System.Windows.Forms.DockStyle.Fill;
            this._itemStatHiddenCheckBox.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this._itemStatHiddenCheckBox.Location = new System.Drawing.Point(149, 5);
            this._itemStatHiddenCheckBox.Margin = new System.Windows.Forms.Padding(4, 5, 2, 2);
            this._itemStatHiddenCheckBox.Name = "_itemStatHiddenCheckBox";
            this._itemStatHiddenCheckBox.Size = new System.Drawing.Size(58, 26);
            this._itemStatHiddenCheckBox.TabIndex = 2;
            this._itemStatHiddenCheckBox.Text = "隐藏";
            // 
            // addStatButton
            // 
            this.addStatButton.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(55)))), ((int)(((byte)(125)))), ((int)(((byte)(210)))));
            this.addStatButton.Dock = System.Windows.Forms.DockStyle.Fill;
            this.addStatButton.FlatAppearance.BorderColor = System.Drawing.Color.FromArgb(((int)(((byte)(55)))), ((int)(((byte)(125)))), ((int)(((byte)(210)))));
            this.addStatButton.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.addStatButton.ForeColor = System.Drawing.Color.White;
            this.addStatButton.Location = new System.Drawing.Point(2, 35);
            this.addStatButton.Margin = new System.Windows.Forms.Padding(2);
            this.addStatButton.Name = "addStatButton";
            this.addStatButton.Size = new System.Drawing.Size(96, 29);
            this.addStatButton.TabIndex = 3;
            this.addStatButton.Text = "增加";
            this.addStatButton.UseVisualStyleBackColor = false;
            // 
            // modifyStatButton
            // 
            this.modifyStatButton.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(55)))), ((int)(((byte)(125)))), ((int)(((byte)(210)))));
            this.modifyStatButton.Dock = System.Windows.Forms.DockStyle.Fill;
            this.modifyStatButton.FlatAppearance.BorderColor = System.Drawing.Color.FromArgb(((int)(((byte)(55)))), ((int)(((byte)(125)))), ((int)(((byte)(210)))));
            this.modifyStatButton.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.modifyStatButton.ForeColor = System.Drawing.Color.White;
            this.modifyStatButton.Location = new System.Drawing.Point(102, 35);
            this.modifyStatButton.Margin = new System.Windows.Forms.Padding(2);
            this.modifyStatButton.Name = "modifyStatButton";
            this.modifyStatButton.Size = new System.Drawing.Size(41, 29);
            this.modifyStatButton.TabIndex = 4;
            this.modifyStatButton.Text = "修改";
            this.modifyStatButton.UseVisualStyleBackColor = false;
            // 
            // deleteStatButton
            // 
            this.deleteStatButton.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(55)))), ((int)(((byte)(125)))), ((int)(((byte)(210)))));
            this.deleteStatButton.Dock = System.Windows.Forms.DockStyle.Fill;
            this.deleteStatButton.FlatAppearance.BorderColor = System.Drawing.Color.FromArgb(((int)(((byte)(55)))), ((int)(((byte)(125)))), ((int)(((byte)(210)))));
            this.deleteStatButton.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.deleteStatButton.ForeColor = System.Drawing.Color.White;
            this.deleteStatButton.Location = new System.Drawing.Point(147, 35);
            this.deleteStatButton.Margin = new System.Windows.Forms.Padding(2);
            this.deleteStatButton.Name = "deleteStatButton";
            this.deleteStatButton.Size = new System.Drawing.Size(60, 29);
            this.deleteStatButton.TabIndex = 5;
            this.deleteStatButton.Text = "删除";
            this.deleteStatButton.UseVisualStyleBackColor = false;
            // 
            // previewSettingsGroup
            // 
            this.previewSettingsGroup.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(47)))), ((int)(((byte)(47)))), ((int)(((byte)(47)))));
            this.previewSettingsGroup.Controls.Add(this.settings);
            this.previewSettingsGroup.Dock = System.Windows.Forms.DockStyle.Fill;
            this.previewSettingsGroup.ForeColor = System.Drawing.Color.Yellow;
            this.previewSettingsGroup.Location = new System.Drawing.Point(798, 0);
            this.previewSettingsGroup.Margin = new System.Windows.Forms.Padding(0, 0, 6, 0);
            this.previewSettingsGroup.Name = "previewSettingsGroup";
            this.previewSettingsGroup.Padding = new System.Windows.Forms.Padding(8, 24, 8, 8);
            this.previewSettingsGroup.Size = new System.Drawing.Size(233, 420);
            this.previewSettingsGroup.TabIndex = 2;
            this.previewSettingsGroup.TabStop = false;
            this.previewSettingsGroup.Text = "预览设置";
            // 
            // settings
            // 
            this.settings.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(47)))), ((int)(((byte)(47)))), ((int)(((byte)(47)))));
            this.settings.ColumnCount = 2;
            this.settings.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Absolute, 72F));
            this.settings.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 100F));
            this.settings.Controls.Add(this.previewClassLabel, 0, 0);
            this.settings.Controls.Add(this._previewClassComboBox, 1, 0);
            this.settings.Controls.Add(this.previewGenderLabel, 0, 1);
            this.settings.Controls.Add(this._previewGenderComboBox, 1, 1);
            this.settings.Controls.Add(this._descriptionPreviewTextBox, 0, 2);
            this.settings.Dock = System.Windows.Forms.DockStyle.Fill;
            this.settings.Location = new System.Drawing.Point(8, 40);
            this.settings.Name = "settings";
            this.settings.RowCount = 3;
            this.settings.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Absolute, 24F));
            this.settings.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Absolute, 24F));
            this.settings.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 100F));
            this.settings.Size = new System.Drawing.Size(217, 372);
            this.settings.TabIndex = 0;
            // 
            // previewClassLabel
            // 
            this.previewClassLabel.Dock = System.Windows.Forms.DockStyle.Fill;
            this.previewClassLabel.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this.previewClassLabel.Location = new System.Drawing.Point(2, 2);
            this.previewClassLabel.Margin = new System.Windows.Forms.Padding(2);
            this.previewClassLabel.Name = "previewClassLabel";
            this.previewClassLabel.Size = new System.Drawing.Size(68, 20);
            this.previewClassLabel.TabIndex = 0;
            this.previewClassLabel.Text = "预览职业";
            this.previewClassLabel.TextAlign = System.Drawing.ContentAlignment.MiddleLeft;
            // 
            // _previewClassComboBox
            // 
            this._previewClassComboBox.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(58)))), ((int)(((byte)(58)))), ((int)(((byte)(58)))));
            this._previewClassComboBox.Dock = System.Windows.Forms.DockStyle.Fill;
            this._previewClassComboBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this._previewClassComboBox.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this._previewClassComboBox.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this._previewClassComboBox.Location = new System.Drawing.Point(74, 2);
            this._previewClassComboBox.Margin = new System.Windows.Forms.Padding(2);
            this._previewClassComboBox.Name = "_previewClassComboBox";
            this._previewClassComboBox.Size = new System.Drawing.Size(141, 25);
            this._previewClassComboBox.TabIndex = 1;
            // 
            // previewGenderLabel
            // 
            this.previewGenderLabel.Dock = System.Windows.Forms.DockStyle.Fill;
            this.previewGenderLabel.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this.previewGenderLabel.Location = new System.Drawing.Point(2, 26);
            this.previewGenderLabel.Margin = new System.Windows.Forms.Padding(2);
            this.previewGenderLabel.Name = "previewGenderLabel";
            this.previewGenderLabel.Size = new System.Drawing.Size(68, 20);
            this.previewGenderLabel.TabIndex = 2;
            this.previewGenderLabel.Text = "预览性别";
            this.previewGenderLabel.TextAlign = System.Drawing.ContentAlignment.MiddleLeft;
            // 
            // _previewGenderComboBox
            // 
            this._previewGenderComboBox.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(58)))), ((int)(((byte)(58)))), ((int)(((byte)(58)))));
            this._previewGenderComboBox.Dock = System.Windows.Forms.DockStyle.Fill;
            this._previewGenderComboBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this._previewGenderComboBox.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this._previewGenderComboBox.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this._previewGenderComboBox.Location = new System.Drawing.Point(74, 26);
            this._previewGenderComboBox.Margin = new System.Windows.Forms.Padding(2);
            this._previewGenderComboBox.Name = "_previewGenderComboBox";
            this._previewGenderComboBox.Size = new System.Drawing.Size(141, 25);
            this._previewGenderComboBox.TabIndex = 3;
            // 
            // _descriptionPreviewTextBox
            // 
            this._descriptionPreviewTextBox.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(4)))), ((int)(((byte)(13)))), ((int)(((byte)(35)))));
            this._descriptionPreviewTextBox.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this.settings.SetColumnSpan(this._descriptionPreviewTextBox, 2);
            this._descriptionPreviewTextBox.DetectUrls = false;
            this._descriptionPreviewTextBox.Dock = System.Windows.Forms.DockStyle.Fill;
            this._descriptionPreviewTextBox.Font = new System.Drawing.Font("Microsoft YaHei UI", 9F);
            this._descriptionPreviewTextBox.ForeColor = System.Drawing.Color.White;
            this._descriptionPreviewTextBox.Location = new System.Drawing.Point(0, 52);
            this._descriptionPreviewTextBox.Margin = new System.Windows.Forms.Padding(0, 4, 0, 0);
            this._descriptionPreviewTextBox.Name = "_descriptionPreviewTextBox";
            this._descriptionPreviewTextBox.ReadOnly = true;
            this._descriptionPreviewTextBox.ScrollBars = System.Windows.Forms.RichTextBoxScrollBars.Vertical;
            this._descriptionPreviewTextBox.ShortcutsEnabled = false;
            this._descriptionPreviewTextBox.Size = new System.Drawing.Size(217, 320);
            this._descriptionPreviewTextBox.TabIndex = 4;
            this._descriptionPreviewTextBox.TabStop = false;
            this._descriptionPreviewTextBox.Text = "";
            this._descriptionPreviewTextBox.WordWrap = false;
            // 
            // setGroup
            // 
            this.setGroup.AutoSize = true;
            this.setGroup.AutoSizeMode = System.Windows.Forms.AutoSizeMode.GrowAndShrink;
            this.setGroup.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(47)))), ((int)(((byte)(47)))), ((int)(((byte)(47)))));
            this.setGroup.Controls.Add(this.setTable);
            this.setGroup.Dock = System.Windows.Forms.DockStyle.Top;
            this.setGroup.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this.setGroup.Location = new System.Drawing.Point(0, 792);
            this.setGroup.Margin = new System.Windows.Forms.Padding(0, 0, 0, 8);
            this.setGroup.Name = "setGroup";
            this.setGroup.Padding = new System.Windows.Forms.Padding(8, 24, 8, 8);
            this.setGroup.Size = new System.Drawing.Size(1037, 561);
            this.setGroup.TabIndex = 2;
            this.setGroup.TabStop = false;
            this.setGroup.Text = "套装属性和成员";
            // 
            // setTable
            // 
            this.setTable.AutoSize = true;
            this.setTable.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(47)))), ((int)(((byte)(47)))), ((int)(((byte)(47)))));
            this.setTable.ColumnCount = 1;
            this.setTable.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Absolute, 1038F));
            this.setTable.Controls.Add(this._setLinkListView, 0, 0);
            this.setTable.Controls.Add(this.linkEditor, 0, 1);
            this.setTable.Controls.Add(this.setFields, 0, 2);
            this.setTable.Controls.Add(this._setStatsListView, 0, 3);
            this.setTable.Controls.Add(this.setStatsEditor, 0, 4);
            this.setTable.Dock = System.Windows.Forms.DockStyle.Top;
            this.setTable.Location = new System.Drawing.Point(8, 40);
            this.setTable.Name = "setTable";
            this.setTable.RowCount = 5;
            this.setTable.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Absolute, 125F));
            this.setTable.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Absolute, 34F));
            this.setTable.RowStyles.Add(new System.Windows.Forms.RowStyle());
            this.setTable.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Absolute, 120F));
            this.setTable.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Absolute, 34F));
            this.setTable.Size = new System.Drawing.Size(1021, 513);
            this.setTable.TabIndex = 0;
            // 
            // _setLinkListView
            // 
            this._setLinkListView.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(58)))), ((int)(((byte)(58)))), ((int)(((byte)(58)))));
            this._setLinkListView.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this._setLinkListView.Dock = System.Windows.Forms.DockStyle.Top;
            this._setLinkListView.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this._setLinkListView.FullRowSelect = true;
            this._setLinkListView.GridLines = true;
            this._setLinkListView.HideSelection = false;
            this._setLinkListView.Location = new System.Drawing.Point(3, 3);
            this._setLinkListView.MultiSelect = false;
            this._setLinkListView.Name = "_setLinkListView";
            this._setLinkListView.Size = new System.Drawing.Size(1032, 14);
            this._setLinkListView.TabIndex = 0;
            this._setLinkListView.UseCompatibleStateImageBehavior = false;
            this._setLinkListView.View = System.Windows.Forms.View.Details;
            // 
            // linkEditor
            // 
            this.linkEditor.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(47)))), ((int)(((byte)(47)))), ((int)(((byte)(47)))));
            this.linkEditor.Controls.Add(this._setGroupComboBox);
            this.linkEditor.Controls.Add(this.addLinkButton);
            this.linkEditor.Controls.Add(this.deleteLinkButton);
            this.linkEditor.Dock = System.Windows.Forms.DockStyle.Top;
            this.linkEditor.Location = new System.Drawing.Point(3, 128);
            this.linkEditor.Name = "linkEditor";
            this.linkEditor.Size = new System.Drawing.Size(1032, 14);
            this.linkEditor.TabIndex = 1;
            this.linkEditor.WrapContents = false;
            // 
            // _setGroupComboBox
            // 
            this._setGroupComboBox.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(58)))), ((int)(((byte)(58)))), ((int)(((byte)(58)))));
            this._setGroupComboBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this._setGroupComboBox.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this._setGroupComboBox.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this._setGroupComboBox.Location = new System.Drawing.Point(2, 2);
            this._setGroupComboBox.Margin = new System.Windows.Forms.Padding(2);
            this._setGroupComboBox.Name = "_setGroupComboBox";
            this._setGroupComboBox.Size = new System.Drawing.Size(330, 25);
            this._setGroupComboBox.TabIndex = 0;
            // 
            // addLinkButton
            // 
            this.addLinkButton.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(58)))), ((int)(((byte)(58)))), ((int)(((byte)(58)))));
            this.addLinkButton.FlatAppearance.BorderColor = System.Drawing.Color.FromArgb(((int)(((byte)(78)))), ((int)(((byte)(78)))), ((int)(((byte)(78)))));
            this.addLinkButton.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.addLinkButton.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this.addLinkButton.Location = new System.Drawing.Point(336, 2);
            this.addLinkButton.Margin = new System.Windows.Forms.Padding(2);
            this.addLinkButton.Name = "addLinkButton";
            this.addLinkButton.Size = new System.Drawing.Size(105, 26);
            this.addLinkButton.TabIndex = 1;
            this.addLinkButton.Text = "关联当前物品";
            this.addLinkButton.UseVisualStyleBackColor = false;
            // 
            // deleteLinkButton
            // 
            this.deleteLinkButton.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(58)))), ((int)(((byte)(58)))), ((int)(((byte)(58)))));
            this.deleteLinkButton.FlatAppearance.BorderColor = System.Drawing.Color.FromArgb(((int)(((byte)(78)))), ((int)(((byte)(78)))), ((int)(((byte)(78)))));
            this.deleteLinkButton.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.deleteLinkButton.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this.deleteLinkButton.Location = new System.Drawing.Point(445, 2);
            this.deleteLinkButton.Margin = new System.Windows.Forms.Padding(2);
            this.deleteLinkButton.Name = "deleteLinkButton";
            this.deleteLinkButton.Size = new System.Drawing.Size(90, 26);
            this.deleteLinkButton.TabIndex = 2;
            this.deleteLinkButton.Text = "移除关联";
            this.deleteLinkButton.UseVisualStyleBackColor = false;
            // 
            // setFields
            // 
            this.setFields.AutoSize = true;
            this.setFields.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(47)))), ((int)(((byte)(47)))), ((int)(((byte)(47)))));
            this.setFields.ColumnCount = 4;
            this.setFields.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Absolute, 90F));
            this.setFields.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 50F));
            this.setFields.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Absolute, 90F));
            this.setFields.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 50F));
            this.setFields.Controls.Add(this.setNameLabel, 0, 0);
            this.setFields.Controls.Add(this._setNameTextBox, 1, 0);
            this.setFields.Controls.Add(this.setGroupNameLabel, 2, 0);
            this.setFields.Controls.Add(this._setGroupNameTextBox, 3, 0);
            this.setFields.Controls.Add(this.setRequiredNumberLabel, 0, 1);
            this.setFields.Controls.Add(this._setRequiredNumberNumeric, 1, 1);
            this.setFields.Controls.Add(this.setRequirementLabel, 2, 1);
            this.setFields.Controls.Add(this._setRequirementComboBox, 3, 1);
            this.setFields.Controls.Add(this.setDescriptionLabel, 0, 2);
            this.setFields.Controls.Add(this._setDescriptionTextBox, 1, 2);
            this.setFields.Controls.Add(this.emptySetLabel, 2, 2);
            this.setFields.Controls.Add(this.emptySetPanel, 3, 2);
            this.setFields.Controls.Add(this.applySetButton, 2, 3);
            this.setFields.Dock = System.Windows.Forms.DockStyle.Top;
            this.setFields.Location = new System.Drawing.Point(3, 162);
            this.setFields.Name = "setFields";
            this.setFields.RowCount = 4;
            this.setFields.RowStyles.Add(new System.Windows.Forms.RowStyle());
            this.setFields.RowStyles.Add(new System.Windows.Forms.RowStyle());
            this.setFields.RowStyles.Add(new System.Windows.Forms.RowStyle());
            this.setFields.RowStyles.Add(new System.Windows.Forms.RowStyle());
            this.setFields.Size = new System.Drawing.Size(1032, 194);
            this.setFields.TabIndex = 2;
            // 
            // setNameLabel
            // 
            this.setNameLabel.AutoSize = true;
            this.setNameLabel.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this.setNameLabel.Location = new System.Drawing.Point(3, 6);
            this.setNameLabel.Margin = new System.Windows.Forms.Padding(3, 6, 3, 3);
            this.setNameLabel.Name = "setNameLabel";
            this.setNameLabel.Size = new System.Drawing.Size(56, 17);
            this.setNameLabel.TabIndex = 0;
            this.setNameLabel.Text = "套装名称";
            // 
            // _setNameTextBox
            // 
            this._setNameTextBox.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(58)))), ((int)(((byte)(58)))), ((int)(((byte)(58)))));
            this._setNameTextBox.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this._setNameTextBox.Dock = System.Windows.Forms.DockStyle.Fill;
            this._setNameTextBox.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this._setNameTextBox.Location = new System.Drawing.Point(93, 3);
            this._setNameTextBox.Name = "_setNameTextBox";
            this._setNameTextBox.Size = new System.Drawing.Size(420, 23);
            this._setNameTextBox.TabIndex = 1;
            // 
            // setGroupNameLabel
            // 
            this.setGroupNameLabel.AutoSize = true;
            this.setGroupNameLabel.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this.setGroupNameLabel.Location = new System.Drawing.Point(519, 6);
            this.setGroupNameLabel.Margin = new System.Windows.Forms.Padding(3, 6, 3, 3);
            this.setGroupNameLabel.Name = "setGroupNameLabel";
            this.setGroupNameLabel.Size = new System.Drawing.Size(56, 17);
            this.setGroupNameLabel.TabIndex = 2;
            this.setGroupNameLabel.Text = "搭配名称";
            // 
            // _setGroupNameTextBox
            // 
            this._setGroupNameTextBox.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(58)))), ((int)(((byte)(58)))), ((int)(((byte)(58)))));
            this._setGroupNameTextBox.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this._setGroupNameTextBox.Dock = System.Windows.Forms.DockStyle.Fill;
            this._setGroupNameTextBox.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this._setGroupNameTextBox.Location = new System.Drawing.Point(609, 3);
            this._setGroupNameTextBox.Name = "_setGroupNameTextBox";
            this._setGroupNameTextBox.Size = new System.Drawing.Size(420, 23);
            this._setGroupNameTextBox.TabIndex = 3;
            // 
            // setRequiredNumberLabel
            // 
            this.setRequiredNumberLabel.AutoSize = true;
            this.setRequiredNumberLabel.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this.setRequiredNumberLabel.Location = new System.Drawing.Point(3, 35);
            this.setRequiredNumberLabel.Margin = new System.Windows.Forms.Padding(3, 6, 3, 3);
            this.setRequiredNumberLabel.Name = "setRequiredNumberLabel";
            this.setRequiredNumberLabel.Size = new System.Drawing.Size(56, 17);
            this.setRequiredNumberLabel.TabIndex = 4;
            this.setRequiredNumberLabel.Text = "触发件数";
            // 
            // _setRequiredNumberNumeric
            // 
            this._setRequiredNumberNumeric.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(58)))), ((int)(((byte)(58)))), ((int)(((byte)(58)))));
            this._setRequiredNumberNumeric.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this._setRequiredNumberNumeric.Dock = System.Windows.Forms.DockStyle.Fill;
            this._setRequiredNumberNumeric.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this._setRequiredNumberNumeric.Location = new System.Drawing.Point(93, 32);
            this._setRequiredNumberNumeric.Maximum = new decimal(new int[] {
            1000000000,
            0,
            0,
            0});
            this._setRequiredNumberNumeric.Minimum = new decimal(new int[] {
            1000000000,
            0,
            0,
            -2147483648});
            this._setRequiredNumberNumeric.Name = "_setRequiredNumberNumeric";
            this._setRequiredNumberNumeric.Size = new System.Drawing.Size(420, 23);
            this._setRequiredNumberNumeric.TabIndex = 5;
            this._setRequiredNumberNumeric.ThousandsSeparator = true;
            // 
            // setRequirementLabel
            // 
            this.setRequirementLabel.AutoSize = true;
            this.setRequirementLabel.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this.setRequirementLabel.Location = new System.Drawing.Point(519, 35);
            this.setRequirementLabel.Margin = new System.Windows.Forms.Padding(3, 6, 3, 3);
            this.setRequirementLabel.Name = "setRequirementLabel";
            this.setRequirementLabel.Size = new System.Drawing.Size(56, 17);
            this.setRequirementLabel.TabIndex = 6;
            this.setRequirementLabel.Text = "触发规则";
            // 
            // _setRequirementComboBox
            // 
            this._setRequirementComboBox.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(58)))), ((int)(((byte)(58)))), ((int)(((byte)(58)))));
            this._setRequirementComboBox.Dock = System.Windows.Forms.DockStyle.Fill;
            this._setRequirementComboBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this._setRequirementComboBox.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this._setRequirementComboBox.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this._setRequirementComboBox.Location = new System.Drawing.Point(609, 32);
            this._setRequirementComboBox.Name = "_setRequirementComboBox";
            this._setRequirementComboBox.Size = new System.Drawing.Size(420, 25);
            this._setRequirementComboBox.TabIndex = 7;
            // 
            // setDescriptionLabel
            // 
            this.setDescriptionLabel.AutoSize = true;
            this.setDescriptionLabel.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this.setDescriptionLabel.Location = new System.Drawing.Point(3, 64);
            this.setDescriptionLabel.Margin = new System.Windows.Forms.Padding(3, 6, 3, 3);
            this.setDescriptionLabel.Name = "setDescriptionLabel";
            this.setDescriptionLabel.Size = new System.Drawing.Size(56, 17);
            this.setDescriptionLabel.TabIndex = 8;
            this.setDescriptionLabel.Text = "套装说明";
            // 
            // _setDescriptionTextBox
            // 
            this._setDescriptionTextBox.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(58)))), ((int)(((byte)(58)))), ((int)(((byte)(58)))));
            this._setDescriptionTextBox.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this._setDescriptionTextBox.Dock = System.Windows.Forms.DockStyle.Fill;
            this._setDescriptionTextBox.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this._setDescriptionTextBox.Location = new System.Drawing.Point(93, 61);
            this._setDescriptionTextBox.Multiline = true;
            this._setDescriptionTextBox.Name = "_setDescriptionTextBox";
            this._setDescriptionTextBox.Size = new System.Drawing.Size(420, 100);
            this._setDescriptionTextBox.TabIndex = 9;
            // 
            // emptySetLabel
            // 
            this.emptySetLabel.AutoSize = true;
            this.emptySetLabel.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this.emptySetLabel.Location = new System.Drawing.Point(519, 64);
            this.emptySetLabel.Margin = new System.Windows.Forms.Padding(3, 6, 3, 3);
            this.emptySetLabel.Name = "emptySetLabel";
            this.emptySetLabel.Size = new System.Drawing.Size(0, 17);
            this.emptySetLabel.TabIndex = 10;
            // 
            // emptySetPanel
            // 
            this.emptySetPanel.Dock = System.Windows.Forms.DockStyle.Fill;
            this.emptySetPanel.Location = new System.Drawing.Point(609, 61);
            this.emptySetPanel.Name = "emptySetPanel";
            this.emptySetPanel.Size = new System.Drawing.Size(420, 100);
            this.emptySetPanel.TabIndex = 11;
            // 
            // applySetButton
            // 
            this.applySetButton.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(58)))), ((int)(((byte)(58)))), ((int)(((byte)(58)))));
            this.applySetButton.FlatAppearance.BorderColor = System.Drawing.Color.FromArgb(((int)(((byte)(78)))), ((int)(((byte)(78)))), ((int)(((byte)(78)))));
            this.applySetButton.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.applySetButton.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this.applySetButton.Location = new System.Drawing.Point(518, 166);
            this.applySetButton.Margin = new System.Windows.Forms.Padding(2);
            this.applySetButton.Name = "applySetButton";
            this.applySetButton.Size = new System.Drawing.Size(86, 26);
            this.applySetButton.TabIndex = 12;
            this.applySetButton.Text = "应用套装字段";
            this.applySetButton.UseVisualStyleBackColor = false;
            // 
            // _setStatsListView
            // 
            this._setStatsListView.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(58)))), ((int)(((byte)(58)))), ((int)(((byte)(58)))));
            this._setStatsListView.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this._setStatsListView.Dock = System.Windows.Forms.DockStyle.Top;
            this._setStatsListView.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this._setStatsListView.FullRowSelect = true;
            this._setStatsListView.GridLines = true;
            this._setStatsListView.HideSelection = false;
            this._setStatsListView.Location = new System.Drawing.Point(3, 362);
            this._setStatsListView.MultiSelect = false;
            this._setStatsListView.Name = "_setStatsListView";
            this._setStatsListView.Size = new System.Drawing.Size(1032, 14);
            this._setStatsListView.TabIndex = 3;
            this._setStatsListView.UseCompatibleStateImageBehavior = false;
            this._setStatsListView.View = System.Windows.Forms.View.Details;
            // 
            // setStatsEditor
            // 
            this.setStatsEditor.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(47)))), ((int)(((byte)(47)))), ((int)(((byte)(47)))));
            this.setStatsEditor.Controls.Add(this._setStatComboBox);
            this.setStatsEditor.Controls.Add(this._setStatAmountNumeric);
            this.setStatsEditor.Controls.Add(this._setStatClassComboBox);
            this.setStatsEditor.Controls.Add(this._setStatLevelNumeric);
            this.setStatsEditor.Controls.Add(this.applySetStatButton);
            this.setStatsEditor.Controls.Add(this.deleteSetStatButton);
            this.setStatsEditor.Dock = System.Windows.Forms.DockStyle.Top;
            this.setStatsEditor.Location = new System.Drawing.Point(3, 482);
            this.setStatsEditor.Name = "setStatsEditor";
            this.setStatsEditor.Size = new System.Drawing.Size(1032, 14);
            this.setStatsEditor.TabIndex = 4;
            this.setStatsEditor.WrapContents = false;
            // 
            // _setStatComboBox
            // 
            this._setStatComboBox.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(58)))), ((int)(((byte)(58)))), ((int)(((byte)(58)))));
            this._setStatComboBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this._setStatComboBox.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this._setStatComboBox.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this._setStatComboBox.Location = new System.Drawing.Point(2, 2);
            this._setStatComboBox.Margin = new System.Windows.Forms.Padding(2);
            this._setStatComboBox.Name = "_setStatComboBox";
            this._setStatComboBox.Size = new System.Drawing.Size(180, 25);
            this._setStatComboBox.TabIndex = 0;
            // 
            // _setStatAmountNumeric
            // 
            this._setStatAmountNumeric.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(58)))), ((int)(((byte)(58)))), ((int)(((byte)(58)))));
            this._setStatAmountNumeric.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this._setStatAmountNumeric.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this._setStatAmountNumeric.Location = new System.Drawing.Point(186, 2);
            this._setStatAmountNumeric.Margin = new System.Windows.Forms.Padding(2);
            this._setStatAmountNumeric.Maximum = new decimal(new int[] {
            1000000000,
            0,
            0,
            0});
            this._setStatAmountNumeric.Minimum = new decimal(new int[] {
            1000000000,
            0,
            0,
            -2147483648});
            this._setStatAmountNumeric.Name = "_setStatAmountNumeric";
            this._setStatAmountNumeric.Size = new System.Drawing.Size(80, 23);
            this._setStatAmountNumeric.TabIndex = 1;
            this._setStatAmountNumeric.ThousandsSeparator = true;
            // 
            // _setStatClassComboBox
            // 
            this._setStatClassComboBox.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(58)))), ((int)(((byte)(58)))), ((int)(((byte)(58)))));
            this._setStatClassComboBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this._setStatClassComboBox.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this._setStatClassComboBox.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this._setStatClassComboBox.Location = new System.Drawing.Point(270, 2);
            this._setStatClassComboBox.Margin = new System.Windows.Forms.Padding(2);
            this._setStatClassComboBox.Name = "_setStatClassComboBox";
            this._setStatClassComboBox.Size = new System.Drawing.Size(160, 25);
            this._setStatClassComboBox.TabIndex = 2;
            // 
            // _setStatLevelNumeric
            // 
            this._setStatLevelNumeric.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(58)))), ((int)(((byte)(58)))), ((int)(((byte)(58)))));
            this._setStatLevelNumeric.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this._setStatLevelNumeric.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this._setStatLevelNumeric.Location = new System.Drawing.Point(434, 2);
            this._setStatLevelNumeric.Margin = new System.Windows.Forms.Padding(2);
            this._setStatLevelNumeric.Maximum = new decimal(new int[] {
            1000000000,
            0,
            0,
            0});
            this._setStatLevelNumeric.Minimum = new decimal(new int[] {
            1000000000,
            0,
            0,
            -2147483648});
            this._setStatLevelNumeric.Name = "_setStatLevelNumeric";
            this._setStatLevelNumeric.Size = new System.Drawing.Size(70, 23);
            this._setStatLevelNumeric.TabIndex = 3;
            this._setStatLevelNumeric.ThousandsSeparator = true;
            // 
            // applySetStatButton
            // 
            this.applySetStatButton.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(58)))), ((int)(((byte)(58)))), ((int)(((byte)(58)))));
            this.applySetStatButton.FlatAppearance.BorderColor = System.Drawing.Color.FromArgb(((int)(((byte)(78)))), ((int)(((byte)(78)))), ((int)(((byte)(78)))));
            this.applySetStatButton.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.applySetStatButton.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this.applySetStatButton.Location = new System.Drawing.Point(508, 2);
            this.applySetStatButton.Margin = new System.Windows.Forms.Padding(2);
            this.applySetStatButton.Name = "applySetStatButton";
            this.applySetStatButton.Size = new System.Drawing.Size(90, 26);
            this.applySetStatButton.TabIndex = 4;
            this.applySetStatButton.Text = "新增/应用";
            this.applySetStatButton.UseVisualStyleBackColor = false;
            // 
            // deleteSetStatButton
            // 
            this.deleteSetStatButton.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(58)))), ((int)(((byte)(58)))), ((int)(((byte)(58)))));
            this.deleteSetStatButton.FlatAppearance.BorderColor = System.Drawing.Color.FromArgb(((int)(((byte)(78)))), ((int)(((byte)(78)))), ((int)(((byte)(78)))));
            this.deleteSetStatButton.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.deleteSetStatButton.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this.deleteSetStatButton.Location = new System.Drawing.Point(602, 2);
            this.deleteSetStatButton.Margin = new System.Windows.Forms.Padding(2);
            this.deleteSetStatButton.Name = "deleteSetStatButton";
            this.deleteSetStatButton.Size = new System.Drawing.Size(70, 26);
            this.deleteSetStatButton.TabIndex = 5;
            this.deleteSetStatButton.Text = "删除";
            this.deleteSetStatButton.UseVisualStyleBackColor = false;
            // 
            // ItemSettingsForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(7F, 17F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(36)))), ((int)(((byte)(36)))), ((int)(((byte)(36)))));
            this.ClientSize = new System.Drawing.Size(1434, 941);
            this.Controls.Add(this.mainSplit);
            this.Controls.Add(this.header);
            this.Font = new System.Drawing.Font("Microsoft YaHei UI", 9F);
            this.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(235)))), ((int)(((byte)(235)))));
            this.KeyPreview = true;
            this.MinimumSize = new System.Drawing.Size(1100, 760);
            this.Name = "ItemSettingsForm";
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterParent;
            this.Text = "物品设置";
            this.header.ResumeLayout(false);
            this.header.PerformLayout();
            this.mainSplit.Panel1.ResumeLayout(false);
            this.mainSplit.Panel2.ResumeLayout(false);
            ((System.ComponentModel.ISupportInitialize)(this.mainSplit)).EndInit();
            this.mainSplit.ResumeLayout(false);
            this.listPanel.ResumeLayout(false);
            this.categories.ResumeLayout(false);
            this.editorHost.ResumeLayout(false);
            this.editorHost.PerformLayout();
            this.editorLayout.ResumeLayout(false);
            this.editorLayout.PerformLayout();
            this.previewGroup.ResumeLayout(false);
            this.previews.ResumeLayout(false);
            this.inventoryColumn.ResumeLayout(false);
            this.equipColumn.ResumeLayout(false);
            this.appearanceColumn.ResumeLayout(false);
            this.smallPreviews.ResumeLayout(false);
            this.smallStoreColumn.ResumeLayout(false);
            this.mallStoreColumn.ResumeLayout(false);
            this.groundColumn.ResumeLayout(false);
            this.editorColumns.ResumeLayout(false);
            this.basicGroup.ResumeLayout(false);
            this.basicLayout.ResumeLayout(false);
            this.basicRow0.ResumeLayout(false);
            this.basicRow0.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)(this._imageNumeric)).EndInit();
            this.basicRow1.ResumeLayout(false);
            ((System.ComponentModel.ISupportInitialize)(this._requiredAmountNumeric)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this._shapeNumeric)).EndInit();
            this.basicRow2.ResumeLayout(false);
            ((System.ComponentModel.ISupportInitialize)(this._partCountNumeric)).EndInit();
            this.basicRow3.ResumeLayout(false);
            ((System.ComponentModel.ISupportInitialize)(this._buffIconNumeric)).EndInit();
            this.basicRow4.ResumeLayout(false);
            ((System.ComponentModel.ISupportInitialize)(this._weightNumeric)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this._durabilityNumeric)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this._priceNumeric)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this._sellRateNumeric)).EndInit();
            this.basicRow5.ResumeLayout(false);
            ((System.ComponentModel.ISupportInitialize)(this._stackSizeNumeric)).EndInit();
            this.basicRow6.ResumeLayout(false);
            ((System.ComponentModel.ISupportInitialize)(this._durationNumeric)).EndInit();
            this.flags.ResumeLayout(false);
            this.flags.PerformLayout();
            this.descriptionRow.ResumeLayout(false);
            this.descriptionRow.PerformLayout();
            this.statsGroup.ResumeLayout(false);
            this.statsTable.ResumeLayout(false);
            this.statsEditor.ResumeLayout(false);
            ((System.ComponentModel.ISupportInitialize)(this._itemStatAmountNumeric)).EndInit();
            this.previewSettingsGroup.ResumeLayout(false);
            this.settings.ResumeLayout(false);
            this.setGroup.ResumeLayout(false);
            this.setGroup.PerformLayout();
            this.setTable.ResumeLayout(false);
            this.setTable.PerformLayout();
            this.linkEditor.ResumeLayout(false);
            this.setFields.ResumeLayout(false);
            this.setFields.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)(this._setRequiredNumberNumeric)).EndInit();
            this.setStatsEditor.ResumeLayout(false);
            ((System.ComponentModel.ISupportInitialize)(this._setStatAmountNumeric)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this._setStatLevelNumeric)).EndInit();
            this.ResumeLayout(false);

        }
    }
}



