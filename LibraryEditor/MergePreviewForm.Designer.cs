using System.Drawing;
using System.Windows.Forms;

namespace LibraryEditor
{
    partial class MergePreviewForm
    {
        private System.ComponentModel.IContainer components = null;
        private SplitContainer mainSplitContainer;
        private Label layerCountLabel;
        private ListBox layerListBox;
        private FlowLayoutPanel buttonPanel;
        private Label offsetXLabel;
        private NumericUpDown offsetXNumericUpDown;
        private Label offsetYLabel;
        private NumericUpDown offsetYNumericUpDown;
        private Button resetOffsetButton;
        private Button moveBackButton;
        private Button moveFrontButton;
        private Button removeButton;
        private Button clearButton;
        private Panel previewHostPanel;
        private PictureBox previewPictureBox;
        private FlowLayoutPanel playbackPanel;
        private Button previousFrameButton;
        private Button playButton;
        private Button nextFrameButton;
        private Label framePositionLabel;
        private Label speedLabel;
        private NumericUpDown speedNumericUpDown;
        private Label previewInfoLabel;
        private Timer animationTimer;

        protected override void Dispose(bool disposing)
        {
            if (disposing && components != null)
                components.Dispose();
            base.Dispose(disposing);
        }

        private void InitializeComponent()
        {
            this.components = new System.ComponentModel.Container();
            this.mainSplitContainer = new SplitContainer();
            this.layerCountLabel = new Label();
            this.layerListBox = new ListBox();
            this.buttonPanel = new FlowLayoutPanel();
            this.offsetXLabel = new Label();
            this.offsetXNumericUpDown = new NumericUpDown();
            this.offsetYLabel = new Label();
            this.offsetYNumericUpDown = new NumericUpDown();
            this.resetOffsetButton = new Button();
            this.moveBackButton = new Button();
            this.moveFrontButton = new Button();
            this.removeButton = new Button();
            this.clearButton = new Button();
            this.previewHostPanel = new Panel();
            this.previewPictureBox = new PictureBox();
            this.playbackPanel = new FlowLayoutPanel();
            this.previousFrameButton = new Button();
            this.playButton = new Button();
            this.nextFrameButton = new Button();
            this.framePositionLabel = new Label();
            this.speedLabel = new Label();
            this.speedNumericUpDown = new NumericUpDown();
            this.previewInfoLabel = new Label();
            this.animationTimer = new Timer(this.components);
            ((System.ComponentModel.ISupportInitialize)(this.mainSplitContainer)).BeginInit();
            this.mainSplitContainer.Panel1.SuspendLayout();
            this.mainSplitContainer.Panel2.SuspendLayout();
            this.mainSplitContainer.SuspendLayout();
            this.buttonPanel.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.offsetXNumericUpDown)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.offsetYNumericUpDown)).BeginInit();
            this.previewHostPanel.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.previewPictureBox)).BeginInit();
            this.playbackPanel.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.speedNumericUpDown)).BeginInit();
            this.SuspendLayout();
            // 
            // mainSplitContainer
            // 
            this.mainSplitContainer.Dock = DockStyle.Fill;
            this.mainSplitContainer.FixedPanel = FixedPanel.Panel1;
            this.mainSplitContainer.Location = new Point(0, 0);
            this.mainSplitContainer.Name = "mainSplitContainer";
            this.mainSplitContainer.Panel1.BackColor = Color.FromArgb(36, 36, 36);
            this.mainSplitContainer.Panel1.Controls.Add(this.layerListBox);
            this.mainSplitContainer.Panel1.Controls.Add(this.buttonPanel);
            this.mainSplitContainer.Panel1.Controls.Add(this.layerCountLabel);
            this.mainSplitContainer.Panel2.BackColor = Color.Black;
            this.mainSplitContainer.Panel2.Controls.Add(this.previewHostPanel);
            this.mainSplitContainer.Panel2.Controls.Add(this.playbackPanel);
            this.mainSplitContainer.Panel2.Controls.Add(this.previewInfoLabel);
            this.mainSplitContainer.Size = new Size(980, 650);
            this.mainSplitContainer.SplitterDistance = 300;
            this.mainSplitContainer.SplitterWidth = 5;
            this.mainSplitContainer.TabIndex = 0;
            // 
            // layerCountLabel
            // 
            this.layerCountLabel.Dock = DockStyle.Top;
            this.layerCountLabel.ForeColor = Color.Gainsboro;
            this.layerCountLabel.Location = new Point(0, 0);
            this.layerCountLabel.Name = "layerCountLabel";
            this.layerCountLabel.Padding = new Padding(8, 0, 0, 0);
            this.layerCountLabel.Size = new Size(300, 34);
            this.layerCountLabel.TabIndex = 0;
            this.layerCountLabel.Text = "图层（从后到前）：0";
            this.layerCountLabel.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // layerListBox
            // 
            this.layerListBox.BackColor = Color.FromArgb(42, 42, 42);
            this.layerListBox.BorderStyle = BorderStyle.FixedSingle;
            this.layerListBox.Dock = DockStyle.Fill;
            this.layerListBox.ForeColor = Color.WhiteSmoke;
            this.layerListBox.FormattingEnabled = true;
            this.layerListBox.HorizontalScrollbar = true;
            this.layerListBox.ItemHeight = 17;
            this.layerListBox.Location = new Point(0, 34);
            this.layerListBox.Name = "layerListBox";
            this.layerListBox.Size = new Size(300, 524);
            this.layerListBox.TabIndex = 1;
            this.layerListBox.SelectedIndexChanged += new System.EventHandler(this.layerListBox_SelectedIndexChanged);
            // 
            // buttonPanel
            // 
            this.buttonPanel.Controls.Add(this.offsetXLabel);
            this.buttonPanel.Controls.Add(this.offsetXNumericUpDown);
            this.buttonPanel.Controls.Add(this.offsetYLabel);
            this.buttonPanel.Controls.Add(this.offsetYNumericUpDown);
            this.buttonPanel.Controls.Add(this.resetOffsetButton);
            this.buttonPanel.Controls.Add(this.moveBackButton);
            this.buttonPanel.Controls.Add(this.moveFrontButton);
            this.buttonPanel.Controls.Add(this.removeButton);
            this.buttonPanel.Controls.Add(this.clearButton);
            this.buttonPanel.Dock = DockStyle.Bottom;
            this.buttonPanel.Location = new Point(0, 558);
            this.buttonPanel.Name = "buttonPanel";
            this.buttonPanel.Padding = new Padding(5, 6, 0, 0);
            this.buttonPanel.Size = new Size(300, 92);
            this.buttonPanel.TabIndex = 2;
            // 
            // offsetXLabel
            // 
            this.offsetXLabel.ForeColor = Color.Gainsboro;
            this.offsetXLabel.Location = new Point(8, 6);
            this.offsetXLabel.Name = "offsetXLabel";
            this.offsetXLabel.Size = new Size(25, 25);
            this.offsetXLabel.TabIndex = 0;
            this.offsetXLabel.Text = "X";
            this.offsetXLabel.TextAlign = ContentAlignment.MiddleCenter;
            // 
            // offsetXNumericUpDown
            // 
            this.offsetXNumericUpDown.BackColor = Color.FromArgb(58, 58, 58);
            this.offsetXNumericUpDown.Enabled = false;
            this.offsetXNumericUpDown.ForeColor = Color.White;
            this.offsetXNumericUpDown.Location = new Point(39, 9);
            this.offsetXNumericUpDown.Maximum = new decimal(new int[] { 1000, 0, 0, 0 });
            this.offsetXNumericUpDown.Minimum = new decimal(new int[] { 1000, 0, 0, -2147483648 });
            this.offsetXNumericUpDown.Name = "offsetXNumericUpDown";
            this.offsetXNumericUpDown.Size = new Size(62, 21);
            this.offsetXNumericUpDown.TabIndex = 1;
            this.offsetXNumericUpDown.ValueChanged += new System.EventHandler(this.offsetNumericUpDown_ValueChanged);
            // 
            // offsetYLabel
            // 
            this.offsetYLabel.ForeColor = Color.Gainsboro;
            this.offsetYLabel.Location = new Point(107, 6);
            this.offsetYLabel.Name = "offsetYLabel";
            this.offsetYLabel.Size = new Size(25, 25);
            this.offsetYLabel.TabIndex = 2;
            this.offsetYLabel.Text = "Y";
            this.offsetYLabel.TextAlign = ContentAlignment.MiddleCenter;
            // 
            // offsetYNumericUpDown
            // 
            this.offsetYNumericUpDown.BackColor = Color.FromArgb(58, 58, 58);
            this.offsetYNumericUpDown.Enabled = false;
            this.offsetYNumericUpDown.ForeColor = Color.White;
            this.offsetYNumericUpDown.Location = new Point(138, 9);
            this.offsetYNumericUpDown.Maximum = new decimal(new int[] { 1000, 0, 0, 0 });
            this.offsetYNumericUpDown.Minimum = new decimal(new int[] { 1000, 0, 0, -2147483648 });
            this.offsetYNumericUpDown.Name = "offsetYNumericUpDown";
            this.offsetYNumericUpDown.Size = new Size(62, 21);
            this.offsetYNumericUpDown.TabIndex = 3;
            this.offsetYNumericUpDown.ValueChanged += new System.EventHandler(this.offsetNumericUpDown_ValueChanged);
            // 
            // resetOffsetButton
            // 
            this.resetOffsetButton.Enabled = false;
            this.resetOffsetButton.FlatStyle = FlatStyle.Flat;
            this.resetOffsetButton.ForeColor = Color.White;
            this.resetOffsetButton.Location = new Point(206, 9);
            this.resetOffsetButton.Name = "resetOffsetButton";
            this.resetOffsetButton.Size = new Size(62, 25);
            this.resetOffsetButton.TabIndex = 4;
            this.resetOffsetButton.Text = "重置坐标";
            this.resetOffsetButton.UseVisualStyleBackColor = true;
            this.resetOffsetButton.Click += new System.EventHandler(this.resetOffsetButton_Click);
            this.buttonPanel.SetFlowBreak(this.resetOffsetButton, true);
            // 
            // moveBackButton
            // 
            this.moveBackButton.FlatStyle = FlatStyle.Flat;
            this.moveBackButton.ForeColor = Color.White;
            this.moveBackButton.Location = new Point(8, 40);
            this.moveBackButton.Name = "moveBackButton";
            this.moveBackButton.Size = new Size(62, 28);
            this.moveBackButton.TabIndex = 5;
            this.moveBackButton.Text = "后移";
            this.moveBackButton.UseVisualStyleBackColor = true;
            this.moveBackButton.Click += new System.EventHandler(this.moveBackButton_Click);
            // 
            // moveFrontButton
            // 
            this.moveFrontButton.FlatStyle = FlatStyle.Flat;
            this.moveFrontButton.ForeColor = Color.White;
            this.moveFrontButton.Location = new Point(76, 40);
            this.moveFrontButton.Name = "moveFrontButton";
            this.moveFrontButton.Size = new Size(62, 28);
            this.moveFrontButton.TabIndex = 6;
            this.moveFrontButton.Text = "前移";
            this.moveFrontButton.UseVisualStyleBackColor = true;
            this.moveFrontButton.Click += new System.EventHandler(this.moveFrontButton_Click);
            // 
            // removeButton
            // 
            this.removeButton.FlatStyle = FlatStyle.Flat;
            this.removeButton.ForeColor = Color.White;
            this.removeButton.Location = new Point(144, 40);
            this.removeButton.Name = "removeButton";
            this.removeButton.Size = new Size(62, 28);
            this.removeButton.TabIndex = 7;
            this.removeButton.Text = "删除";
            this.removeButton.UseVisualStyleBackColor = true;
            this.removeButton.Click += new System.EventHandler(this.removeButton_Click);
            // 
            // clearButton
            // 
            this.clearButton.FlatStyle = FlatStyle.Flat;
            this.clearButton.ForeColor = Color.White;
            this.clearButton.Location = new Point(212, 40);
            this.clearButton.Name = "clearButton";
            this.clearButton.Size = new Size(62, 28);
            this.clearButton.TabIndex = 8;
            this.clearButton.Text = "清空";
            this.clearButton.UseVisualStyleBackColor = true;
            this.clearButton.Click += new System.EventHandler(this.clearButton_Click);
            // 
            // previewHostPanel
            // 
            this.previewHostPanel.AutoScroll = true;
            this.previewHostPanel.BackColor = Color.Black;
            this.previewHostPanel.Controls.Add(this.previewPictureBox);
            this.previewHostPanel.Dock = DockStyle.Fill;
            this.previewHostPanel.Location = new Point(0, 0);
            this.previewHostPanel.Name = "previewHostPanel";
            this.previewHostPanel.Size = new Size(675, 576);
            this.previewHostPanel.TabIndex = 0;
            this.previewHostPanel.Resize += new System.EventHandler(this.previewHostPanel_Resize);
            // 
            // previewPictureBox
            // 
            this.previewPictureBox.BackColor = Color.Black;
            this.previewPictureBox.Location = new Point(0, 0);
            this.previewPictureBox.Name = "previewPictureBox";
            this.previewPictureBox.Size = new Size(1, 1);
            this.previewPictureBox.SizeMode = PictureBoxSizeMode.Normal;
            this.previewPictureBox.TabIndex = 0;
            this.previewPictureBox.TabStop = false;
            // 
            // playbackPanel
            // 
            this.playbackPanel.BackColor = Color.FromArgb(47, 47, 47);
            this.playbackPanel.Controls.Add(this.previousFrameButton);
            this.playbackPanel.Controls.Add(this.playButton);
            this.playbackPanel.Controls.Add(this.nextFrameButton);
            this.playbackPanel.Controls.Add(this.framePositionLabel);
            this.playbackPanel.Controls.Add(this.speedLabel);
            this.playbackPanel.Controls.Add(this.speedNumericUpDown);
            this.playbackPanel.Dock = DockStyle.Bottom;
            this.playbackPanel.Location = new Point(0, 576);
            this.playbackPanel.Name = "playbackPanel";
            this.playbackPanel.Padding = new Padding(8, 7, 0, 0);
            this.playbackPanel.Size = new Size(675, 44);
            this.playbackPanel.TabIndex = 1;
            // 
            // previousFrameButton
            // 
            this.previousFrameButton.FlatStyle = FlatStyle.Flat;
            this.previousFrameButton.ForeColor = Color.White;
            this.previousFrameButton.Location = new Point(11, 10);
            this.previousFrameButton.Name = "previousFrameButton";
            this.previousFrameButton.Size = new Size(62, 26);
            this.previousFrameButton.TabIndex = 0;
            this.previousFrameButton.Text = "上一帧";
            this.previousFrameButton.UseVisualStyleBackColor = true;
            this.previousFrameButton.Click += new System.EventHandler(this.previousFrameButton_Click);
            // 
            // playButton
            // 
            this.playButton.BackColor = Color.FromArgb(55, 125, 210);
            this.playButton.FlatStyle = FlatStyle.Flat;
            this.playButton.ForeColor = Color.White;
            this.playButton.Location = new Point(79, 10);
            this.playButton.Name = "playButton";
            this.playButton.Size = new Size(62, 26);
            this.playButton.TabIndex = 1;
            this.playButton.Text = "播放";
            this.playButton.UseVisualStyleBackColor = false;
            this.playButton.Click += new System.EventHandler(this.playButton_Click);
            // 
            // nextFrameButton
            // 
            this.nextFrameButton.FlatStyle = FlatStyle.Flat;
            this.nextFrameButton.ForeColor = Color.White;
            this.nextFrameButton.Location = new Point(147, 10);
            this.nextFrameButton.Name = "nextFrameButton";
            this.nextFrameButton.Size = new Size(62, 26);
            this.nextFrameButton.TabIndex = 2;
            this.nextFrameButton.Text = "下一帧";
            this.nextFrameButton.UseVisualStyleBackColor = true;
            this.nextFrameButton.Click += new System.EventHandler(this.nextFrameButton_Click);
            // 
            // framePositionLabel
            // 
            this.framePositionLabel.ForeColor = Color.Gainsboro;
            this.framePositionLabel.Location = new Point(215, 7);
            this.framePositionLabel.Name = "framePositionLabel";
            this.framePositionLabel.Size = new Size(110, 32);
            this.framePositionLabel.TabIndex = 3;
            this.framePositionLabel.Text = "帧：-";
            this.framePositionLabel.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // speedLabel
            // 
            this.speedLabel.ForeColor = Color.Gainsboro;
            this.speedLabel.Location = new Point(331, 7);
            this.speedLabel.Name = "speedLabel";
            this.speedLabel.Size = new Size(62, 32);
            this.speedLabel.TabIndex = 4;
            this.speedLabel.Text = "速度(ms)";
            this.speedLabel.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // speedNumericUpDown
            // 
            this.speedNumericUpDown.BackColor = Color.FromArgb(58, 58, 58);
            this.speedNumericUpDown.ForeColor = Color.White;
            this.speedNumericUpDown.Increment = new decimal(new int[] { 10, 0, 0, 0 });
            this.speedNumericUpDown.Location = new Point(399, 12);
            this.speedNumericUpDown.Maximum = new decimal(new int[] { 1000, 0, 0, 0 });
            this.speedNumericUpDown.Minimum = new decimal(new int[] { 25, 0, 0, 0 });
            this.speedNumericUpDown.Name = "speedNumericUpDown";
            this.speedNumericUpDown.Size = new Size(72, 21);
            this.speedNumericUpDown.TabIndex = 5;
            this.speedNumericUpDown.Value = new decimal(new int[] { 120, 0, 0, 0 });
            this.speedNumericUpDown.ValueChanged += new System.EventHandler(this.speedNumericUpDown_ValueChanged);
            // 
            // previewInfoLabel
            // 
            this.previewInfoLabel.Dock = DockStyle.Bottom;
            this.previewInfoLabel.ForeColor = Color.Silver;
            this.previewInfoLabel.Location = new Point(0, 620);
            this.previewInfoLabel.Name = "previewInfoLabel";
            this.previewInfoLabel.Padding = new Padding(8, 0, 0, 0);
            this.previewInfoLabel.Size = new Size(675, 30);
            this.previewInfoLabel.TabIndex = 2;
            this.previewInfoLabel.Text = "请在外观查询窗口选择帧，然后点击“合并预览”。";
            this.previewInfoLabel.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // animationTimer
            // 
            this.animationTimer.Interval = 120;
            this.animationTimer.Tick += new System.EventHandler(this.animationTimer_Tick);
            // 
            // MergePreviewForm
            // 
            this.AutoScaleDimensions = new SizeF(6F, 12F);
            this.AutoScaleMode = AutoScaleMode.Font;
            this.BackColor = Color.FromArgb(30, 30, 30);
            this.ClientSize = new Size(980, 650);
            this.Controls.Add(this.mainSplitContainer);
            this.MinimumSize = new Size(760, 520);
            this.Name = "MergePreviewForm";
            this.StartPosition = FormStartPosition.CenterParent;
            this.Text = "合并预览（只读）";
            this.FormClosed += new FormClosedEventHandler(this.MergePreviewForm_FormClosed);
            this.mainSplitContainer.Panel1.ResumeLayout(false);
            this.mainSplitContainer.Panel2.ResumeLayout(false);
            ((System.ComponentModel.ISupportInitialize)(this.mainSplitContainer)).EndInit();
            this.mainSplitContainer.ResumeLayout(false);
            this.buttonPanel.ResumeLayout(false);
            ((System.ComponentModel.ISupportInitialize)(this.offsetXNumericUpDown)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.offsetYNumericUpDown)).EndInit();
            this.previewHostPanel.ResumeLayout(false);
            ((System.ComponentModel.ISupportInitialize)(this.previewPictureBox)).EndInit();
            this.playbackPanel.ResumeLayout(false);
            ((System.ComponentModel.ISupportInitialize)(this.speedNumericUpDown)).EndInit();
            this.ResumeLayout(false);
        }
    }
}
