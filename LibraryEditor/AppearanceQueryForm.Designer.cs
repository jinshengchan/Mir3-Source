using System;
using System.ComponentModel;
using System.Drawing;
using System.Windows.Forms;

namespace LibraryEditor
{
    public sealed partial class AppearanceQueryForm
    {
        private IContainer components;
        private ToolStrip toolStrip;
        private ToolStripButton scanButton;
        private ToolStripButton exportButton;
        private ToolStripButton clearCacheButton;
        private ToolStripButton mergeButton;
        private ToolStripLabel dataPathToolStripLabel;
        private SplitContainer mainSplitContainer;
        private TreeView appearanceTreeView;
        private Label treeHeaderLabel;
        private SplitContainer previewSplitContainer;
        private Panel galleryPanel;
        private Label galleryHeaderLabel;
        private ListView shapeListView;
        private ImageList thumbnailImageList;
        private Panel previewPanel;
        private PictureBox previewPictureBox;
        private Label previewInfoLabel;
        private Label groupInfoLabel;
        private Panel playbackPanel;
        private Button previousButton;
        private Button playButton;
        private Button nextButton;
        private Label directionLabel;
        private ComboBox directionComboBox;
        private Label frameLabel;
        private TrackBar frameTrackBar;
        private Label frameInfoLabel;
        private Label speedLabel;
        private NumericUpDown speedNumericUpDown;
        private Label statusLabel;
        private Timer playbackTimer;

        protected override void Dispose(bool disposing)
        {
            if (disposing && components != null)
                components.Dispose();
            base.Dispose(disposing);
        }

        private void InitializeComponent()
        {
            this.components = new Container();
            this.toolStrip = new ToolStrip();
            this.scanButton = new ToolStripButton();
            this.exportButton = new ToolStripButton();
            this.clearCacheButton = new ToolStripButton();
            this.mergeButton = new ToolStripButton();
            this.dataPathToolStripLabel = new ToolStripLabel();
            this.mainSplitContainer = new SplitContainer();
            this.appearanceTreeView = new TreeView();
            this.treeHeaderLabel = new Label();
            this.previewSplitContainer = new SplitContainer();
            this.galleryPanel = new Panel();
            this.galleryHeaderLabel = new Label();
            this.shapeListView = new ListView();
            this.thumbnailImageList = new ImageList(this.components);
            this.previewPanel = new Panel();
            this.previewPictureBox = new PictureBox();
            this.previewInfoLabel = new Label();
            this.groupInfoLabel = new Label();
            this.playbackPanel = new Panel();
            this.previousButton = new Button();
            this.playButton = new Button();
            this.nextButton = new Button();
            this.directionLabel = new Label();
            this.directionComboBox = new ComboBox();
            this.frameLabel = new Label();
            this.frameTrackBar = new TrackBar();
            this.frameInfoLabel = new Label();
            this.speedLabel = new Label();
            this.speedNumericUpDown = new NumericUpDown();
            this.statusLabel = new Label();
            this.playbackTimer = new Timer(this.components);
            this.toolStrip.SuspendLayout();
            ((ISupportInitialize)(this.mainSplitContainer)).BeginInit();
            this.mainSplitContainer.Panel1.SuspendLayout();
            this.mainSplitContainer.Panel2.SuspendLayout();
            this.mainSplitContainer.SuspendLayout();
            ((ISupportInitialize)(this.previewSplitContainer)).BeginInit();
            this.previewSplitContainer.Panel1.SuspendLayout();
            this.previewSplitContainer.Panel2.SuspendLayout();
            this.previewSplitContainer.SuspendLayout();
            this.galleryPanel.SuspendLayout();
            this.previewPanel.SuspendLayout();
            ((ISupportInitialize)(this.previewPictureBox)).BeginInit();
            this.playbackPanel.SuspendLayout();
            ((ISupportInitialize)(this.frameTrackBar)).BeginInit();
            ((ISupportInitialize)(this.speedNumericUpDown)).BeginInit();
            this.SuspendLayout();
            // 
            // toolStrip
            // 
            this.toolStrip.BackColor = Color.FromArgb(45, 45, 48);
            this.toolStrip.ForeColor = Color.Gainsboro;
            this.toolStrip.GripStyle = ToolStripGripStyle.Hidden;
            this.toolStrip.Items.AddRange(new ToolStripItem[] {
            this.scanButton,
            this.exportButton,
            this.clearCacheButton,
            this.mergeButton,
            this.dataPathToolStripLabel});
            this.toolStrip.Location = new Point(0, 0);
            this.toolStrip.Name = "toolStrip";
            this.toolStrip.Padding = new Padding(6, 3, 6, 3);
            this.toolStrip.Size = new Size(1280, 31);
            this.toolStrip.TabIndex = 0;
            // 
            // scanButton
            // 
            this.scanButton.DisplayStyle = ToolStripItemDisplayStyle.Text;
            this.scanButton.ForeColor = Color.White;
            this.scanButton.Name = "scanButton";
            this.scanButton.Size = new Size(44, 22);
            this.scanButton.Text = "扫描";
            this.scanButton.Click += new EventHandler(this.scanButton_Click);
            // 
            // exportButton
            // 
            this.exportButton.DisplayStyle = ToolStripItemDisplayStyle.Text;
            this.exportButton.ForeColor = Color.White;
            this.exportButton.Name = "exportButton";
            this.exportButton.Size = new Size(44, 22);
            this.exportButton.Text = "导出";
            this.exportButton.Click += new EventHandler(this.exportButton_Click);
            // 
            // clearCacheButton
            // 
            this.clearCacheButton.DisplayStyle = ToolStripItemDisplayStyle.Text;
            this.clearCacheButton.ForeColor = Color.White;
            this.clearCacheButton.Name = "clearCacheButton";
            this.clearCacheButton.Size = new Size(68, 22);
            this.clearCacheButton.Text = "清理缓存";
            this.clearCacheButton.Click += new EventHandler(this.clearCacheButton_Click);
            // 
            // mergeButton
            // 
            this.mergeButton.DisplayStyle = ToolStripItemDisplayStyle.Text;
            this.mergeButton.ForeColor = Color.White;
            this.mergeButton.Name = "mergeButton";
            this.mergeButton.Size = new Size(68, 22);
            this.mergeButton.Text = "合并预览";
            this.mergeButton.Click += new EventHandler(this.mergeButton_Click);
            // 
            // dataPathToolStripLabel
            // 
            this.dataPathToolStripLabel.Alignment = ToolStripItemAlignment.Right;
            this.dataPathToolStripLabel.AutoSize = false;
            this.dataPathToolStripLabel.ForeColor = Color.Silver;
            this.dataPathToolStripLabel.Name = "dataPathToolStripLabel";
            this.dataPathToolStripLabel.Size = new Size(820, 22);
            this.dataPathToolStripLabel.Text = "Data: 未选择";
            this.dataPathToolStripLabel.TextAlign = ContentAlignment.MiddleRight;
            // 
            // mainSplitContainer
            // 
            this.mainSplitContainer.BackColor = Color.FromArgb(78, 78, 80);
            this.mainSplitContainer.Dock = DockStyle.Fill;
            this.mainSplitContainer.FixedPanel = FixedPanel.Panel1;
            this.mainSplitContainer.Location = new Point(0, 31);
            this.mainSplitContainer.Name = "mainSplitContainer";
            // 
            // mainSplitContainer.Panel1
            // 
            this.mainSplitContainer.Panel1.BackColor = Color.FromArgb(36, 36, 36);
            this.mainSplitContainer.Panel1.Controls.Add(this.appearanceTreeView);
            this.mainSplitContainer.Panel1.Controls.Add(this.treeHeaderLabel);
            // 
            // mainSplitContainer.Panel2
            // 
            this.mainSplitContainer.Panel2.Controls.Add(this.previewSplitContainer);
            this.mainSplitContainer.Size = new Size(1280, 695);
            this.mainSplitContainer.SplitterDistance = 270;
            this.mainSplitContainer.SplitterWidth = 5;
            this.mainSplitContainer.TabIndex = 1;
            // 
            // appearanceTreeView
            // 
            this.appearanceTreeView.BackColor = Color.FromArgb(36, 36, 36);
            this.appearanceTreeView.BorderStyle = BorderStyle.None;
            this.appearanceTreeView.Dock = DockStyle.Fill;
            this.appearanceTreeView.ForeColor = Color.FromArgb(230, 230, 230);
            this.appearanceTreeView.HideSelection = false;
            this.appearanceTreeView.Location = new Point(0, 30);
            this.appearanceTreeView.Name = "appearanceTreeView";
            this.appearanceTreeView.Size = new Size(270, 665);
            this.appearanceTreeView.TabIndex = 0;
            this.appearanceTreeView.AfterSelect += new TreeViewEventHandler(this.appearanceTreeView_AfterSelect);
            // 
            // treeHeaderLabel
            // 
            this.treeHeaderLabel.BackColor = Color.FromArgb(47, 47, 47);
            this.treeHeaderLabel.Dock = DockStyle.Top;
            this.treeHeaderLabel.ForeColor = Color.FromArgb(235, 235, 235);
            this.treeHeaderLabel.Location = new Point(0, 0);
            this.treeHeaderLabel.Name = "treeHeaderLabel";
            this.treeHeaderLabel.Padding = new Padding(8, 0, 0, 0);
            this.treeHeaderLabel.Size = new Size(270, 30);
            this.treeHeaderLabel.TabIndex = 1;
            this.treeHeaderLabel.Text = "分类 / 素材库 / Shape";
            this.treeHeaderLabel.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // previewSplitContainer
            // 
            this.previewSplitContainer.Dock = DockStyle.Fill;
            this.previewSplitContainer.Location = new Point(0, 0);
            this.previewSplitContainer.Name = "previewSplitContainer";
            this.previewSplitContainer.Orientation = Orientation.Horizontal;
            // 
            // previewSplitContainer.Panel1
            // 
            this.previewSplitContainer.Panel1.Controls.Add(this.galleryPanel);
            // 
            // previewSplitContainer.Panel2
            // 
            this.previewSplitContainer.Panel2.Controls.Add(this.previewPanel);
            this.previewSplitContainer.Size = new Size(1005, 695);
            this.previewSplitContainer.SplitterDistance = 285;
            this.previewSplitContainer.SplitterWidth = 5;
            this.previewSplitContainer.TabIndex = 0;
            // 
            // galleryPanel
            // 
            this.galleryPanel.BackColor = Color.FromArgb(36, 36, 36);
            this.galleryPanel.Controls.Add(this.shapeListView);
            this.galleryPanel.Controls.Add(this.galleryHeaderLabel);
            this.galleryPanel.Dock = DockStyle.Fill;
            this.galleryPanel.Location = new Point(0, 0);
            this.galleryPanel.Name = "galleryPanel";
            this.galleryPanel.Padding = new Padding(8);
            this.galleryPanel.Size = new Size(1005, 285);
            this.galleryPanel.TabIndex = 0;
            // 
            // galleryHeaderLabel
            // 
            this.galleryHeaderLabel.Dock = DockStyle.Top;
            this.galleryHeaderLabel.ForeColor = Color.FromArgb(235, 235, 235);
            this.galleryHeaderLabel.Location = new Point(8, 8);
            this.galleryHeaderLabel.Name = "galleryHeaderLabel";
            this.galleryHeaderLabel.Size = new Size(989, 30);
            this.galleryHeaderLabel.TabIndex = 0;
            this.galleryHeaderLabel.Text = "Shape 缩略图";
            this.galleryHeaderLabel.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // shapeListView
            // 
            this.shapeListView.BackColor = Color.FromArgb(42, 42, 42);
            this.shapeListView.BorderStyle = BorderStyle.FixedSingle;
            this.shapeListView.Dock = DockStyle.Fill;
            this.shapeListView.ForeColor = Color.FromArgb(235, 235, 235);
            this.shapeListView.HideSelection = false;
            this.shapeListView.LargeImageList = this.thumbnailImageList;
            this.shapeListView.Location = new Point(8, 38);
            this.shapeListView.MultiSelect = false;
            this.shapeListView.Name = "shapeListView";
            this.shapeListView.Size = new Size(989, 239);
            this.shapeListView.TabIndex = 1;
            this.shapeListView.UseCompatibleStateImageBehavior = false;
            this.shapeListView.View = View.LargeIcon;
            this.shapeListView.ItemSelectionChanged += new ListViewItemSelectionChangedEventHandler(this.shapeListView_ItemSelectionChanged);
            // 
            // thumbnailImageList
            // 
            this.thumbnailImageList.ColorDepth = ColorDepth.Depth32Bit;
            this.thumbnailImageList.ImageSize = new Size(96, 96);
            this.thumbnailImageList.TransparentColor = Color.Transparent;
            // 
            // previewPanel
            // 
            this.previewPanel.BackColor = Color.FromArgb(30, 30, 30);
            this.previewPanel.Controls.Add(this.previewPictureBox);
            this.previewPanel.Controls.Add(this.previewInfoLabel);
            this.previewPanel.Controls.Add(this.groupInfoLabel);
            this.previewPanel.Dock = DockStyle.Fill;
            this.previewPanel.Location = new Point(0, 0);
            this.previewPanel.Name = "previewPanel";
            this.previewPanel.Padding = new Padding(8);
            this.previewPanel.Size = new Size(1005, 405);
            this.previewPanel.TabIndex = 0;
            // 
            // previewPictureBox
            // 
            this.previewPictureBox.BackColor = Color.Black;
            this.previewPictureBox.BorderStyle = BorderStyle.FixedSingle;
            this.previewPictureBox.Dock = DockStyle.Fill;
            this.previewPictureBox.Location = new Point(8, 62);
            this.previewPictureBox.Name = "previewPictureBox";
            this.previewPictureBox.Size = new Size(989, 309);
            this.previewPictureBox.SizeMode = PictureBoxSizeMode.CenterImage;
            this.previewPictureBox.TabIndex = 0;
            this.previewPictureBox.TabStop = false;
            // 
            // previewInfoLabel
            // 
            this.previewInfoLabel.Dock = DockStyle.Bottom;
            this.previewInfoLabel.ForeColor = Color.Silver;
            this.previewInfoLabel.Location = new Point(8, 371);
            this.previewInfoLabel.Name = "previewInfoLabel";
            this.previewInfoLabel.Size = new Size(989, 26);
            this.previewInfoLabel.TabIndex = 1;
            this.previewInfoLabel.Text = "未选择帧";
            this.previewInfoLabel.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // groupInfoLabel
            // 
            this.groupInfoLabel.Dock = DockStyle.Top;
            this.groupInfoLabel.ForeColor = Color.FromArgb(230, 230, 230);
            this.groupInfoLabel.Location = new Point(8, 8);
            this.groupInfoLabel.Name = "groupInfoLabel";
            this.groupInfoLabel.Size = new Size(989, 26);
            this.groupInfoLabel.TabIndex = 2;
            this.groupInfoLabel.Text = "未选择 Shape";
            this.groupInfoLabel.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // playbackPanel
            // 
            this.playbackPanel.BackColor = Color.FromArgb(47, 47, 47);
            this.playbackPanel.Controls.Add(this.previousButton);
            this.playbackPanel.Controls.Add(this.playButton);
            this.playbackPanel.Controls.Add(this.nextButton);
            this.playbackPanel.Controls.Add(this.directionLabel);
            this.playbackPanel.Controls.Add(this.directionComboBox);
            this.playbackPanel.Controls.Add(this.frameLabel);
            this.playbackPanel.Controls.Add(this.frameTrackBar);
            this.playbackPanel.Controls.Add(this.frameInfoLabel);
            this.playbackPanel.Controls.Add(this.speedLabel);
            this.playbackPanel.Controls.Add(this.speedNumericUpDown);
            this.playbackPanel.Dock = DockStyle.Bottom;
            this.playbackPanel.Location = new Point(0, 726);
            this.playbackPanel.Name = "playbackPanel";
            this.playbackPanel.Size = new Size(1280, 70);
            this.playbackPanel.TabIndex = 2;
            // 
            // previousButton
            // 
            this.previousButton.BackColor = Color.FromArgb(65, 65, 68);
            this.previousButton.FlatStyle = FlatStyle.Flat;
            this.previousButton.ForeColor = Color.White;
            this.previousButton.Location = new Point(10, 20);
            this.previousButton.Name = "previousButton";
            this.previousButton.Size = new Size(62, 28);
            this.previousButton.TabIndex = 0;
            this.previousButton.Text = "上一帧";
            this.previousButton.UseVisualStyleBackColor = false;
            this.previousButton.Click += new EventHandler(this.previousButton_Click);
            // 
            // playButton
            // 
            this.playButton.BackColor = Color.FromArgb(55, 125, 210);
            this.playButton.FlatStyle = FlatStyle.Flat;
            this.playButton.ForeColor = Color.White;
            this.playButton.Location = new Point(78, 20);
            this.playButton.Name = "playButton";
            this.playButton.Size = new Size(62, 28);
            this.playButton.TabIndex = 1;
            this.playButton.Text = "播放";
            this.playButton.UseVisualStyleBackColor = false;
            this.playButton.Click += new EventHandler(this.playButton_Click);
            // 
            // nextButton
            // 
            this.nextButton.BackColor = Color.FromArgb(65, 65, 68);
            this.nextButton.FlatStyle = FlatStyle.Flat;
            this.nextButton.ForeColor = Color.White;
            this.nextButton.Location = new Point(146, 20);
            this.nextButton.Name = "nextButton";
            this.nextButton.Size = new Size(62, 28);
            this.nextButton.TabIndex = 2;
            this.nextButton.Text = "下一帧";
            this.nextButton.UseVisualStyleBackColor = false;
            this.nextButton.Click += new EventHandler(this.nextButton_Click);
            // 
            // directionLabel
            // 
            this.directionLabel.AutoSize = true;
            this.directionLabel.ForeColor = Color.Gainsboro;
            this.directionLabel.Location = new Point(228, 27);
            this.directionLabel.Name = "directionLabel";
            this.directionLabel.Size = new Size(41, 12);
            this.directionLabel.TabIndex = 3;
            this.directionLabel.Text = "方向：";
            // 
            // directionComboBox
            // 
            this.directionComboBox.BackColor = Color.FromArgb(58, 58, 58);
            this.directionComboBox.DropDownStyle = ComboBoxStyle.DropDownList;
            this.directionComboBox.ForeColor = Color.White;
            this.directionComboBox.FormattingEnabled = true;
            this.directionComboBox.Location = new Point(274, 22);
            this.directionComboBox.Name = "directionComboBox";
            this.directionComboBox.Size = new Size(135, 20);
            this.directionComboBox.TabIndex = 4;
            this.directionComboBox.SelectedIndexChanged += new EventHandler(this.directionComboBox_SelectedIndexChanged);
            // 
            // frameLabel
            // 
            this.frameLabel.AutoSize = true;
            this.frameLabel.ForeColor = Color.Gainsboro;
            this.frameLabel.Location = new Point(428, 27);
            this.frameLabel.Name = "frameLabel";
            this.frameLabel.Size = new Size(41, 12);
            this.frameLabel.TabIndex = 5;
            this.frameLabel.Text = "帧：";
            // 
            // frameTrackBar
            // 
            this.frameTrackBar.Anchor = AnchorStyles.Left | AnchorStyles.Right | AnchorStyles.Top;
            this.frameTrackBar.Location = new Point(462, 13);
            this.frameTrackBar.Maximum = 1;
            this.frameTrackBar.Name = "frameTrackBar";
            this.frameTrackBar.Size = new Size(615, 45);
            this.frameTrackBar.TabIndex = 6;
            this.frameTrackBar.ValueChanged += new EventHandler(this.frameTrackBar_ValueChanged);
            // 
            // frameInfoLabel
            // 
            this.frameInfoLabel.Anchor = AnchorStyles.Top | AnchorStyles.Right;
            this.frameInfoLabel.ForeColor = Color.Silver;
            this.frameInfoLabel.Location = new Point(1084, 15);
            this.frameInfoLabel.Name = "frameInfoLabel";
            this.frameInfoLabel.Size = new Size(112, 20);
            this.frameInfoLabel.TabIndex = 7;
            this.frameInfoLabel.Text = "帧：-";
            this.frameInfoLabel.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // speedLabel
            // 
            this.speedLabel.Anchor = AnchorStyles.Top | AnchorStyles.Right;
            this.speedLabel.AutoSize = true;
            this.speedLabel.ForeColor = Color.Gainsboro;
            this.speedLabel.Location = new Point(1084, 40);
            this.speedLabel.Name = "speedLabel";
            this.speedLabel.Size = new Size(53, 12);
            this.speedLabel.TabIndex = 8;
            this.speedLabel.Text = "速度(ms)";
            // 
            // speedNumericUpDown
            // 
            this.speedNumericUpDown.Anchor = AnchorStyles.Top | AnchorStyles.Right;
            this.speedNumericUpDown.BackColor = Color.FromArgb(58, 58, 58);
            this.speedNumericUpDown.ForeColor = Color.White;
            this.speedNumericUpDown.Location = new Point(1142, 36);
            this.speedNumericUpDown.Maximum = new decimal(new int[] {
            1000,
            0,
            0,
            0});
            this.speedNumericUpDown.Minimum = new decimal(new int[] {
            25,
            0,
            0,
            0});
            this.speedNumericUpDown.Name = "speedNumericUpDown";
            this.speedNumericUpDown.Size = new Size(62, 21);
            this.speedNumericUpDown.TabIndex = 9;
            this.speedNumericUpDown.Value = new decimal(new int[] {
            120,
            0,
            0,
            0});
            this.speedNumericUpDown.ValueChanged += new EventHandler(this.speedNumericUpDown_ValueChanged);
            // 
            // statusLabel
            // 
            this.statusLabel.BackColor = Color.FromArgb(36, 36, 36);
            this.statusLabel.Dock = DockStyle.Bottom;
            this.statusLabel.ForeColor = Color.FromArgb(180, 200, 220);
            this.statusLabel.Location = new Point(0, 796);
            this.statusLabel.Name = "statusLabel";
            this.statusLabel.Padding = new Padding(8, 0, 0, 0);
            this.statusLabel.Size = new Size(1280, 22);
            this.statusLabel.TabIndex = 3;
            this.statusLabel.Text = "等待扫描";
            this.statusLabel.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // playbackTimer
            // 
            this.playbackTimer.Interval = 120;
            this.playbackTimer.Tick += new EventHandler(this.playbackTimer_Tick);
            // 
            // AppearanceQueryForm
            // 
            this.AutoScaleDimensions = new SizeF(6F, 12F);
            this.AutoScaleMode = AutoScaleMode.Font;
            this.BackColor = Color.FromArgb(36, 36, 36);
            this.ClientSize = new Size(1280, 818);
            this.Controls.Add(this.mainSplitContainer);
            this.Controls.Add(this.playbackPanel);
            this.Controls.Add(this.statusLabel);
            this.Controls.Add(this.toolStrip);
            this.ForeColor = Color.FromArgb(235, 235, 235);
            this.MinimumSize = new Size(1050, 650);
            this.Name = "AppearanceQueryForm";
            this.StartPosition = FormStartPosition.CenterParent;
            this.Text = "外观预览计算器";
            this.toolStrip.ResumeLayout(false);
            this.toolStrip.PerformLayout();
            this.mainSplitContainer.Panel1.ResumeLayout(false);
            this.mainSplitContainer.Panel2.ResumeLayout(false);
            ((ISupportInitialize)(this.mainSplitContainer)).EndInit();
            this.mainSplitContainer.ResumeLayout(false);
            this.previewSplitContainer.Panel1.ResumeLayout(false);
            this.previewSplitContainer.Panel2.ResumeLayout(false);
            ((ISupportInitialize)(this.previewSplitContainer)).EndInit();
            this.previewSplitContainer.ResumeLayout(false);
            this.galleryPanel.ResumeLayout(false);
            this.previewPanel.ResumeLayout(false);
            ((ISupportInitialize)(this.previewPictureBox)).EndInit();
            this.playbackPanel.ResumeLayout(false);
            this.playbackPanel.PerformLayout();
            ((ISupportInitialize)(this.frameTrackBar)).EndInit();
            ((ISupportInitialize)(this.speedNumericUpDown)).EndInit();
            this.ResumeLayout(false);
            this.PerformLayout();
        }
    }
}
