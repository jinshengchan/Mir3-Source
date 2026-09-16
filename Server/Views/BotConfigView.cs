using Server;
using Server.Envir;
using System;
using System.Collections.Generic;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Windows.Forms;

namespace Server.Views
{
    /// <summary>
    /// 假人管理完整面板。配置先读入 detached model，校验成功后才交给 BotManager 应用。
    /// </summary>
    public class BotConfigView : Form
    {
        private sealed class BotLevelRangeOption
        {
            public string Text { get; set; }
            public int MinLevel { get; set; }
            public int MaxLevel { get; set; }

            public override string ToString()
            {
                return Text;
            }
        }

        private readonly List<BotLevelRangeOption> _botMapRanges = new List<BotLevelRangeOption>();
        private const int LeftPanelWidth = 800;
        private const int LeftGroupWidth = 775;
        private const int RightPanelMinWidth = 520;
        private const int HalfRowWidth = 365;
        private const int FullRowWidth = 745;
        private const int LeftOperationButtonMaxWidth = 180;
        private const int RightQuickButtonMaxWidth = 220;
        private const int MapButtonMaxWidth = 150;
        private BotManagementSettings _loadedSettings;
        private Timer _refreshTimer;
        private bool _loading;
        private bool _cleanedUp;
        private bool _runtimeQuickTuningWasActive;
        private string _runtimeQuickTuningStatusMessage = string.Empty;

        private TextBox BotFilePathEdit;
        private NumericUpDown BotCountEdit;
        private CheckBox BotEnableCheckEdit;
        private CheckBox BotCreateGuildCheckEdit;
        private CheckBox BotAllowGroupCheckEdit;
        private CheckBox BotEnableChatCheckEdit;
        private CheckBox BotAutoLevelCheckEdit;
        private CheckBox BotAutoPickupCheckEdit;
        private CheckBox BotAutoSellTrashCheckEdit;
        private CheckBox BotAutoPotionSupplyCheckEdit;
        private CheckBox BotAutoEquipCheckEdit;
        private CheckBox BotAutoLearnSkillCheckEdit;
        private CheckBox BotAutoGroupCheckEdit;
        private CheckBox BotAutoTradeCheckEdit;
        private CheckBox BotGuildSystemCheckEdit;
        private CheckBox BotParticipateConquestCheckEdit;
        private CheckBox BotPvpRetaliationCheckEdit;
        private CheckBox BotAutoMapSwitchCheckEdit;
        private CheckBox BotSkipPickupWhenGroupedWithHumanCheckEdit;
        private CheckBox BotAttackPlayersCheckEdit;
        private CheckBox BotAutoRebirthCheckEdit;
        private CheckBox BotPercentRecoveryCheckEdit;
        private CheckBox BotFixedRecoveryCheckEdit;
        private CheckBox BotAutoSpecialRepairCheckEdit;

        private NumericUpDown BotProactivePvpMinLevelEdit;
        private NumericUpDown BotAutoRebirthLevelEdit;
        private NumericUpDown BotAutoRebirthMaxCountEdit;
        private NumericUpDown BotDefenseLevelIntervalEdit;
        private NumericUpDown BotDefenseBonusPerTierEdit;
        private NumericUpDown BotStrongElementStartLevelEdit;
        private NumericUpDown BotStrongElementLevelIntervalEdit;
        private NumericUpDown BotStrongElementTypeCountEdit;
        private NumericUpDown BotPercentRecoveryPerSecondEdit;
        private NumericUpDown BotFixedRecoveryPerSecondEdit;
        private NumericUpDown BotGlobalChatIntervalSecondsEdit;
        private NumericUpDown BotSpecialRepairThresholdPercentEdit;
        private NumericUpDown BotRecallBatchIntervalMsEdit;
        private NumericUpDown BotRecallBatchSizeEdit;

        private TrackBar BotAggressionSlider;
        private TrackBar BotActivitySlider;
        private TrackBar BotGroupTendencySlider;
        private TrackBar BotChatFrequencySlider;
        private Label BotAggressionValueLabel;
        private Label BotActivityValueLabel;
        private Label BotGroupTendencyValueLabel;
        private Label BotChatFrequencyValueLabel;

        private NumericUpDown BotInitialGoldFloorEdit;
        private NumericUpDown BotGoldFarmThresholdEdit;
        private NumericUpDown BotMinHealthPotionCountEdit;
        private NumericUpDown BotMinManaPotionCountEdit;
        private NumericUpDown BotTickDispatchLimitEdit;
        private NumericUpDown BotMainLoopIntervalMsEdit;
        private NumericUpDown BotMaxOnlineEdit;
        private NumericUpDown BotPotionMonitorIntervalMsEdit;
        private NumericUpDown BotFullHealthThresholdPercentEdit;
        private NumericUpDown BotAttackAttemptIntervalMsEdit;
        private NumericUpDown BotPickupAttemptIntervalMsEdit;
        private NumericUpDown BotPickupRadiusEdit;
        private NumericUpDown BotMapPoolBonusEdit;
        private NumericUpDown BotMapSwitchScoreGapMaxEdit;
        private NumericUpDown BotPeriodicGroupSecondsEdit;
        private NumericUpDown BotMainActionsPerFrameEdit;
        private NumericUpDown BotPotionActionsPerFrameEdit;
        private TextBox BotLogDirectoryEdit;

        private Button BotStartButton;
        private Button BotStopButton;
        private Button BotRecallButton;
        private Button BotPauseButton;
        private Button BotSyncButton;
        private Button BotSaveButton;
        private Button BotRefreshButton;
        private Button BotQuickRecallButton;
        private Button BotQuickPauseButton;
        private Button BotQuickSyncButton;
        private Button BotBackfillRewardsButton;
        private Button BotRewardReportButton;
        private Button BotMapProbButton;
        private Button BotSwitchMapButton;
        private Button BotForceSwitchAllButton;
        private ComboBox BotMapRangeComboBox;
        private Label BotStatusLabel;
        private Label BotStatisticsLabel;
        private Label BotActivityStateLabel;
        private Label BotQuickActionStatusLabel;
        private ListView BotListView;
        private TextBox BotActivityLogBox;
        private TextBox BotOperationLogBox;

        public BotConfigView()
        {
            InitializeBotMapRanges();
            InitializeComponent();
            LoadBotSettings();

            _refreshTimer = new Timer
            {
                Interval = 1000,
            };
            _refreshTimer.Tick += RefreshTimer_Tick;
            _refreshTimer.Start();
            RefreshSnapshot(BotManager.GetManagementSnapshot());
        }

        private void InitializeComponent()
        {
            SuspendLayout();

            BotFilePathEdit = new TextBox { Name = "BotFilePathEdit", Width = 320 };
            BotCountEdit = CreateNumeric("BotCountEdit", 0, 10000, 0);
            BotEnableCheckEdit = CreateCheck("BotEnableCheckEdit", "启动时自动运行");
            BotCreateGuildCheckEdit = CreateCheck("BotCreateGuildCheckEdit", "自动创建行会");
            BotAllowGroupCheckEdit = CreateCheck("BotAllowGroupCheckEdit", "允许假人组队");
            BotEnableChatCheckEdit = CreateCheck("BotEnableChatCheckEdit", "启用假人聊天");

            BotAutoLevelCheckEdit = CreateCheck("BotAutoLevelCheckEdit", "自动打怪升级");
            BotAutoPickupCheckEdit = CreateCheck("BotAutoPickupCheckEdit", "自动拾取物品");
            BotAutoSellTrashCheckEdit = CreateCheck("BotAutoSellTrashCheckEdit", "自动出售垃圾");
            BotAutoPotionSupplyCheckEdit = CreateCheck("BotAutoPotionSupplyCheckEdit", "自动补给药水");
            BotAutoEquipCheckEdit = CreateCheck("BotAutoEquipCheckEdit", "自动穿戴装备");
            BotAutoLearnSkillCheckEdit = CreateCheck("BotAutoLearnSkillCheckEdit", "自动学习技能");
            BotAutoGroupCheckEdit = CreateCheck("BotAutoGroupCheckEdit", "自动组队");
            BotAutoTradeCheckEdit = CreateCheck("BotAutoTradeCheckEdit", "自动交易");
            BotGuildSystemCheckEdit = CreateCheck("BotGuildSystemCheckEdit", "行会系统");
            BotParticipateConquestCheckEdit = CreateCheck("BotParticipateConquestCheckEdit", "参与攻城");
            BotPvpRetaliationCheckEdit = CreateCheck("BotPvpRetaliationCheckEdit", "PVP反击");
            BotAutoMapSwitchCheckEdit = CreateCheck("BotAutoMapSwitchCheckEdit", "自动切图");
            BotSkipPickupWhenGroupedWithHumanCheckEdit = CreateCheck(
                "BotSkipPickupWhenGroupedWithHumanCheckEdit", "与玩家组队不捡物品");
            BotAttackPlayersCheckEdit = CreateCheck("BotAttackPlayersCheckEdit", "达到等级后主动PK");
            BotAutoRebirthCheckEdit = CreateCheck("BotAutoRebirthCheckEdit", "自动转生");
            BotPercentRecoveryCheckEdit = CreateCheck("BotPercentRecoveryCheckEdit", "按比例每秒给假人回血蓝");
            BotFixedRecoveryCheckEdit = CreateCheck("BotFixedRecoveryCheckEdit", "按数值每秒给假人回血蓝");
            BotAutoSpecialRepairCheckEdit = CreateCheck("BotAutoSpecialRepairCheckEdit", "自动特修装备");

            BotProactivePvpMinLevelEdit = CreateNumeric("BotProactivePvpMinLevelEdit", 0, 255, 45);
            BotAutoRebirthLevelEdit = CreateNumeric("BotAutoRebirthLevelEdit", 0, 255, 1);
            BotAutoRebirthMaxCountEdit = CreateNumeric("BotAutoRebirthMaxCountEdit", 0, 255, 5);
            BotDefenseLevelIntervalEdit = CreateNumeric("BotDefenseLevelIntervalEdit", 0, 10000, 0);
            BotDefenseBonusPerTierEdit = CreateNumeric("BotDefenseBonusPerTierEdit", 0, 10000, 0);
            BotStrongElementStartLevelEdit = CreateNumeric("BotStrongElementStartLevelEdit", 0, 255, 0);
            BotStrongElementLevelIntervalEdit = CreateNumeric("BotStrongElementLevelIntervalEdit", 0, 10000, 0);
            BotStrongElementTypeCountEdit = CreateNumeric("BotStrongElementTypeCountEdit", 0, 7, 0);
            BotPercentRecoveryPerSecondEdit = CreateNumeric("BotPercentRecoveryPerSecondEdit", 0, 10000, 0);
            BotFixedRecoveryPerSecondEdit = CreateNumeric("BotFixedRecoveryPerSecondEdit", 0, 10000, 0);
            BotGlobalChatIntervalSecondsEdit = CreateNumeric("BotGlobalChatIntervalSecondsEdit", 0, 60000, 30);
            BotSpecialRepairThresholdPercentEdit = CreateNumeric("BotSpecialRepairThresholdPercentEdit", 0, 100, 50);
            BotRecallBatchIntervalMsEdit = CreateNumeric("BotRecallBatchIntervalMsEdit", 1, 60000, 200);
            BotRecallBatchSizeEdit = CreateNumeric("BotRecallBatchSizeEdit", 0, 10000, 10000);

            BotAggressionSlider = CreateSlider("BotAggressionSlider");
            BotActivitySlider = CreateSlider("BotActivitySlider");
            BotGroupTendencySlider = CreateSlider("BotGroupTendencySlider");
            BotChatFrequencySlider = CreateSlider("BotChatFrequencySlider");
            BotAggressionValueLabel = new Label { AutoSize = true };
            BotActivityValueLabel = new Label { AutoSize = true };
            BotGroupTendencyValueLabel = new Label { AutoSize = true };
            BotChatFrequencyValueLabel = new Label { AutoSize = true };
            BotAggressionSlider.Scroll += delegate { UpdateSliderLabel(BotAggressionSlider, BotAggressionValueLabel); };
            BotActivitySlider.Scroll += delegate { UpdateSliderLabel(BotActivitySlider, BotActivityValueLabel); };
            BotGroupTendencySlider.Scroll += delegate { UpdateSliderLabel(BotGroupTendencySlider, BotGroupTendencyValueLabel); };
            BotChatFrequencySlider.Scroll += delegate { UpdateSliderLabel(BotChatFrequencySlider, BotChatFrequencyValueLabel); };

            BotInitialGoldFloorEdit = CreateNumeric("BotInitialGoldFloorEdit", 0, 9999999999999999m, 100000);
            BotGoldFarmThresholdEdit = CreateNumeric("BotGoldFarmThresholdEdit", 0, 9999999999999999m, 500000);
            BotMinHealthPotionCountEdit = CreateNumeric("BotMinHealthPotionCountEdit", 0, 10000, 80);
            BotMinManaPotionCountEdit = CreateNumeric("BotMinManaPotionCountEdit", 0, 10000, 80);
            BotTickDispatchLimitEdit = CreateNumeric("BotTickDispatchLimitEdit", 0, 10000, 10000);
            BotMainLoopIntervalMsEdit = CreateNumeric("BotMainLoopIntervalMsEdit", 1, 60000, 200);
            BotMaxOnlineEdit = CreateNumeric("BotMaxOnlineEdit", 0, 10000, 10000);
            BotPotionMonitorIntervalMsEdit = CreateNumeric("BotPotionMonitorIntervalMsEdit", 1, 60000, 200);
            BotFullHealthThresholdPercentEdit = CreateNumeric("BotFullHealthThresholdPercentEdit", 0, 100, 100);
            BotAttackAttemptIntervalMsEdit = CreateNumeric("BotAttackAttemptIntervalMsEdit", 1, 60000, 200);
            BotPickupAttemptIntervalMsEdit = CreateNumeric("BotPickupAttemptIntervalMsEdit", 1, 60000, 200);
            BotPickupRadiusEdit = CreateNumeric("BotPickupRadiusEdit", 0, 20, 6);
            BotMapPoolBonusEdit = CreateNumeric("BotMapPoolBonusEdit", 0, 10000, 0);
            BotMapSwitchScoreGapMaxEdit = CreateNumeric("BotMapSwitchScoreGapMaxEdit", 0, 536870911, 0);
            BotPeriodicGroupSecondsEdit = CreateNumeric("BotPeriodicGroupSecondsEdit", 0, 60000, 0);
            BotMainActionsPerFrameEdit = CreateNumeric("BotMainActionsPerFrameEdit", 1, 10000, 200);
            BotPotionActionsPerFrameEdit = CreateNumeric("BotPotionActionsPerFrameEdit", 1, 10000, 200);
            BotLogDirectoryEdit = new TextBox { Name = "BotLogDirectoryEdit", Width = 320 };

            BotStartButton = CreateButton("启动假人", Color.FromArgb(160, 225, 160), BotStartButton_Click);
            BotStopButton = CreateButton("停止假人", Color.FromArgb(245, 160, 160), BotStopButton_Click);
            BotRecallButton = CreateButton("所有假人回城", Color.FromArgb(255, 205, 120), BotRecallButton_Click);
            BotPauseButton = CreateButton("暂停", Color.FromArgb(245, 220, 140), BotPauseButton_Click);
            BotSyncButton = CreateButton("同步到左侧", Color.FromArgb(170, 215, 255), BotSyncButton_Click);
            BotSaveButton = CreateButton("保存配置", Color.FromArgb(170, 215, 255), BotSaveButton_Click);
            BotRefreshButton = CreateButton("刷新", Color.FromArgb(210, 210, 210), BotRefreshButton_Click);
            BotQuickRecallButton = CreateButton("全员回城", Color.FromArgb(255, 205, 120), BotRecallButton_Click);
            BotQuickPauseButton = CreateButton("暂停", Color.FromArgb(245, 220, 140), BotPauseButton_Click);
            BotQuickSyncButton = CreateButton("同步到左侧", Color.FromArgb(170, 215, 255), BotSyncButton_Click);
            BotBackfillRewardsButton = CreateButton("补充防御强元素", Color.FromArgb(230, 205, 150), BotBackfillRewardsButton_Click);
            BotRewardReportButton = CreateButton("查看奖励漏发", Color.FromArgb(210, 225, 170), BotRewardReportButton_Click);
            BotMapProbButton = CreateButton("地图概率分布统计", Color.FromArgb(180, 220, 180), BotMapProbButton_Click);
            BotSwitchMapButton = CreateButton("按档随机切换地图", Color.FromArgb(120, 200, 255), BotSwitchMapButton_Click);
            BotForceSwitchAllButton = CreateButton("强制一键按档切图", Color.FromArgb(255, 160, 120), BotForceSwitchAllButton_Click);

            BotMapRangeComboBox = new ComboBox
            {
                Name = "BotMapRangeComboBox",
                DropDownStyle = ComboBoxStyle.DropDownList,
                Width = 155,
            };
            BotMapRangeComboBox.Items.AddRange(_botMapRanges.Cast<object>().ToArray());
            if (BotMapRangeComboBox.Items.Count > 0) BotMapRangeComboBox.SelectedIndex = 0;

            BotStatusLabel = new Label { Name = "BotStatusLabel", AutoSize = true, Text = "状态: 已停止" };
            BotStatisticsLabel = new Label { Name = "BotStatisticsLabel", AutoSize = false, Width = FullRowWidth, Height = 48, Dock = DockStyle.Top, AutoEllipsis = false };
            BotActivityStateLabel = new Label { Name = "BotActivityStateLabel", AutoSize = false, Width = FullRowWidth, Height = 36, Dock = DockStyle.Top, AutoEllipsis = false };
            BotQuickActionStatusLabel = new Label
            {
                Name = "BotQuickActionStatusLabel",
                AutoSize = false,
                Width = FullRowWidth,
                Height = 24,
                Text = "快捷调整：未启用",
                AutoEllipsis = false,
            };

            BotListView = new ListView
            {
                Name = "BotListView",
                View = View.Details,
                FullRowSelect = true,
                GridLines = true,
                Height = 165,
                Width = FullRowWidth,
            };
            BotListView.Columns.Add("名称", 110);
            BotListView.Columns.Add("等级", 55);
            BotListView.Columns.Add("地图", 70);
            BotListView.Columns.Add("金币", 100);
            BotListView.Columns.Add("状态", 100);

            BotActivityLogBox = CreateLogBox("BotActivityLogBox");
            BotOperationLogBox = CreateLogBox("BotOperationLogBox");

            SplitContainer split = new SplitContainer
            {
                Dock = DockStyle.Fill,
                Orientation = Orientation.Vertical,
                IsSplitterFixed = false,
            };
            split.ClientSize = new Size(1380, 820);
            split.Panel1MinSize = LeftPanelWidth;
            split.Panel2MinSize = RightPanelMinWidth;
            split.Panel1.Controls.Add(BuildLeftColumn());
            Control rightColumn = BuildRightColumn();
            split.Panel2.Controls.Add(rightColumn);

            ClientSize = new Size(1380, 820);
            MinimumSize = new Size(1340, 650);
            Controls.Add(split);
            split.ClientSizeChanged += delegate
            {
                if (split.ClientSize.Width >= split.Panel1MinSize + split.Panel2MinSize + split.SplitterWidth)
                    split.SplitterDistance = Math.Min(LeftPanelWidth,
                        Math.Max(split.Panel1MinSize, split.ClientSize.Width - split.Panel2MinSize - split.SplitterWidth));
            };
            FormBorderStyle = FormBorderStyle.Sizable;
            MaximizeBox = true;
            MinimizeBox = true;
            Name = "BotConfigView";
            StartPosition = FormStartPosition.CenterScreen;
            Text = "假人系统配置";
            FormClosed += BotConfigView_FormClosed;
            Shown += delegate { ResizeRightColumnGroups(rightColumn as FlowLayoutPanel); };

            ResumeLayout(false);
            PerformLayout();
            if (split.ClientSize.Width >= split.Panel1MinSize + split.Panel2MinSize + split.SplitterWidth)
                split.SplitterDistance = Math.Min(LeftPanelWidth,
                    Math.Max(split.Panel1MinSize, split.ClientSize.Width - split.Panel2MinSize - split.SplitterWidth));
        }

        private Control BuildLeftColumn()
        {
            FlowLayoutPanel column = CreateColumn();

            GroupBox basic = CreateGroup("假人基础配置", LeftGroupWidth);
            FlowLayoutPanel basicFlow = GetGroupFlow(basic, true, FullRowWidth);
            AddPathRow(basicFlow, "假人配置文件", FullRowWidth);
            AddField(basicFlow, "假人数量", BotCountEdit, HalfRowWidth);
            AddCheck(basicFlow, BotEnableCheckEdit, HalfRowWidth);
            AddCheck(basicFlow, BotCreateGuildCheckEdit, HalfRowWidth);
            AddCheck(basicFlow, BotAllowGroupCheckEdit, HalfRowWidth);
            AddCheck(basicFlow, BotEnableChatCheckEdit, HalfRowWidth);
            column.Controls.Add(basic);

            GroupBox behavior = CreateGroup("自动行为开关", LeftGroupWidth);
            FlowLayoutPanel behaviorFlow = GetGroupFlow(behavior, true, FullRowWidth);
            AddCheck(behaviorFlow, BotAutoLevelCheckEdit, HalfRowWidth);
            AddCheck(behaviorFlow, BotAutoPickupCheckEdit, HalfRowWidth);
            AddCheck(behaviorFlow, BotAutoSellTrashCheckEdit, HalfRowWidth);
            AddCheck(behaviorFlow, BotAutoPotionSupplyCheckEdit, HalfRowWidth);
            AddCheck(behaviorFlow, BotAutoEquipCheckEdit, HalfRowWidth);
            AddCheck(behaviorFlow, BotAutoLearnSkillCheckEdit, HalfRowWidth);
            AddCheck(behaviorFlow, BotAutoGroupCheckEdit, HalfRowWidth);
            AddCheck(behaviorFlow, BotAutoTradeCheckEdit, HalfRowWidth);
            AddCheck(behaviorFlow, BotGuildSystemCheckEdit, HalfRowWidth);
            AddCheck(behaviorFlow, BotParticipateConquestCheckEdit, HalfRowWidth);
            AddCheck(behaviorFlow, BotPvpRetaliationCheckEdit, HalfRowWidth);
            AddCheck(behaviorFlow, BotAutoMapSwitchCheckEdit, HalfRowWidth);
            AddCheck(behaviorFlow, BotSkipPickupWhenGroupedWithHumanCheckEdit, HalfRowWidth);
            column.Controls.Add(behavior);

            GroupBox pvp = CreateGroup("主动 PK 与自动转生", LeftGroupWidth);
            FlowLayoutPanel pvpFlow = GetGroupFlow(pvp, true, FullRowWidth);
            AddInline(pvpFlow, "达到", BotProactivePvpMinLevelEdit, "级以上与玩家PK", HalfRowWidth);
            AddCheck(pvpFlow, BotAttackPlayersCheckEdit, HalfRowWidth);
            AddInline(pvpFlow, "达到", BotAutoRebirthLevelEdit, "级自动转生，最高", HalfRowWidth);
            AddInline(pvpFlow, "", BotAutoRebirthMaxCountEdit, "转", HalfRowWidth);
            AddCheck(pvpFlow, BotAutoRebirthCheckEdit, HalfRowWidth);
            column.Controls.Add(pvp);

            GroupBox rewards = CreateGroup("等级奖励", LeftGroupWidth);
            FlowLayoutPanel rewardsFlow = GetGroupFlow(rewards, true, FullRowWidth);
            AddField(rewardsFlow, "双防奖励每多少级", BotDefenseLevelIntervalEdit, HalfRowWidth);
            AddField(rewardsFlow, "增加双防", BotDefenseBonusPerTierEdit, HalfRowWidth);
            AddField(rewardsFlow, "强元素起始等级", BotStrongElementStartLevelEdit, HalfRowWidth);
            AddField(rewardsFlow, "强元素等级间隔", BotStrongElementLevelIntervalEdit, HalfRowWidth);
            AddField(rewardsFlow, "随机增加几种强元素", BotStrongElementTypeCountEdit, HalfRowWidth);
            AddButtonRow(rewardsFlow, FullRowWidth, BotBackfillRewardsButton, BotRewardReportButton);
            column.Controls.Add(rewards);

            GroupBox recovery = CreateGroup("每秒恢复", LeftGroupWidth);
            FlowLayoutPanel recoveryFlow = GetGroupFlow(recovery, true, FullRowWidth);
            AddCheck(recoveryFlow, BotPercentRecoveryCheckEdit, HalfRowWidth);
            AddField(recoveryFlow, "比例恢复百分比/秒", BotPercentRecoveryPerSecondEdit, HalfRowWidth);
            AddCheck(recoveryFlow, BotFixedRecoveryCheckEdit, HalfRowWidth);
            AddField(recoveryFlow, "数值恢复点数/秒", BotFixedRecoveryPerSecondEdit, HalfRowWidth);
            column.Controls.Add(recovery);

            GroupBox maintenance = CreateGroup("聊天、特修与回城", LeftGroupWidth);
            FlowLayoutPanel maintenanceFlow = GetGroupFlow(maintenance, true, FullRowWidth);
            AddField(maintenanceFlow, "假人全服聊天间隔秒数", BotGlobalChatIntervalSecondsEdit, HalfRowWidth);
            AddCheck(maintenanceFlow, BotAutoSpecialRepairCheckEdit, HalfRowWidth);
            AddField(maintenanceFlow, "特修耐久百分比阈值", BotSpecialRepairThresholdPercentEdit, HalfRowWidth);
            AddField(maintenanceFlow, "分批回城数量", BotRecallBatchSizeEdit, HalfRowWidth);
            AddField(maintenanceFlow, "分批回城间隔毫秒", BotRecallBatchIntervalMsEdit, HalfRowWidth);
            column.Controls.Add(maintenance);

            GroupBox operations = CreateGroup("假人操作", LeftGroupWidth);
            FlowLayoutPanel operationsFlow = GetGroupFlow(operations, false, FullRowWidth);
            AddButtonRow(operationsFlow, FullRowWidth, LeftOperationButtonMaxWidth, BotStartButton, BotStopButton, BotRecallButton);
            AddButtonRow(operationsFlow, FullRowWidth, LeftOperationButtonMaxWidth, BotPauseButton, BotSaveButton);
            AddButtonRow(operationsFlow, FullRowWidth, LeftOperationButtonMaxWidth, BotRefreshButton);
            AddFullWidthControl(operationsFlow, BotStatusLabel, FullRowWidth);
            column.Controls.Add(operations);

            GroupBox maps = CreateGroup("覆盖地图与切图", LeftGroupWidth);
            FlowLayoutPanel mapsFlow = GetGroupFlow(maps, false, FullRowWidth);
            AddField(mapsFlow, "切图档位", BotMapRangeComboBox, FullRowWidth);
            AddButtonRow(mapsFlow, FullRowWidth, BotSwitchMapButton, BotForceSwitchAllButton, BotMapProbButton);
            AddFullWidthControl(mapsFlow, new Label { Text = "覆盖地图 / 地图概率分布", AutoSize = false }, FullRowWidth);
            AddFullWidthControl(mapsFlow, new Label { Name = "BotLeftActivityStateLabel", Text = "假人打怪状态", AutoSize = false }, FullRowWidth);
            column.Controls.Add(maps);

            GroupBox logs = CreateGroup("日志目录、假人列表与日志", LeftGroupWidth);
            FlowLayoutPanel logsFlow = GetGroupFlow(logs, false, FullRowWidth);
            AddField(logsFlow, "日志目录", BotLogDirectoryEdit, FullRowWidth);
            AddFullWidthControl(logsFlow, new Label { Text = "假人列表", AutoSize = false }, FullRowWidth);
            AddFullWidthControl(logsFlow, BotListView, FullRowWidth);
            AddFullWidthControl(logsFlow, new Label { Text = "实时活动日志", AutoSize = false }, FullRowWidth);
            AddFullWidthControl(logsFlow, BotActivityLogBox, FullRowWidth);
            AddFullWidthControl(logsFlow, new Label { Text = "操作日志", AutoSize = false }, FullRowWidth);
            AddFullWidthControl(logsFlow, BotOperationLogBox, FullRowWidth);
            column.Controls.Add(logs);

            ResizeColumnGroups(column);
            return column;
        }

        private Control BuildRightColumn()
        {
            FlowLayoutPanel column = CreateColumn();
            int rightContentWidth = RightPanelMinWidth - 36;
            int rightHalfWidth = (rightContentWidth - 5) / 2;

            GroupBox statistics = CreateGroup("运行状态统计", RightPanelMinWidth - 20);
            FlowLayoutPanel statisticsFlow = GetGroupFlow(statistics, false, rightContentWidth);
            AddFullWidthControl(statisticsFlow, BotStatisticsLabel, rightContentWidth);
            AddFullWidthControl(statisticsFlow, new Label { Text = "假人打怪状态", AutoSize = false }, rightContentWidth);
            AddFullWidthControl(statisticsFlow, BotActivityStateLabel, rightContentWidth);
            column.Controls.Add(statistics);

            GroupBox strengths = CreateGroup("行为强度", RightPanelMinWidth - 20);
            FlowLayoutPanel strengthsFlow = GetGroupFlow(strengths, false, rightContentWidth);
            AddSliderRow(strengthsFlow, "攻击性", BotAggressionSlider, BotAggressionValueLabel, rightContentWidth);
            AddSliderRow(strengthsFlow, "活跃度", BotActivitySlider, BotActivityValueLabel, rightContentWidth);
            AddSliderRow(strengthsFlow, "组队倾向", BotGroupTendencySlider, BotGroupTendencyValueLabel, rightContentWidth);
            AddSliderRow(strengthsFlow, "聊天频率", BotChatFrequencySlider, BotChatFrequencyValueLabel, rightContentWidth);
            column.Controls.Add(strengths);

            GroupBox economy = CreateGroup("经济控制", RightPanelMinWidth - 20);
            FlowLayoutPanel economyFlow = GetGroupFlow(economy, true, rightContentWidth);
            AddField(economyFlow, "初始金币", BotInitialGoldFloorEdit, rightHalfWidth);
            AddField(economyFlow, "打金阈值", BotGoldFarmThresholdEdit, rightHalfWidth);
            AddField(economyFlow, "最低 HP 药水", BotMinHealthPotionCountEdit, rightHalfWidth);
            AddField(economyFlow, "最低 MP 药水", BotMinManaPotionCountEdit, rightHalfWidth);
            column.Controls.Add(economy);

            GroupBox performance = CreateGroup("性能调优", RightPanelMinWidth - 20);
            FlowLayoutPanel performanceFlow = GetGroupFlow(performance, true, rightContentWidth);
            AddField(performanceFlow, "每 Tick 处理", BotTickDispatchLimitEdit, rightHalfWidth);
            AddField(performanceFlow, "主循环毫秒", BotMainLoopIntervalMsEdit, rightHalfWidth);
            AddField(performanceFlow, "最大在线", BotMaxOnlineEdit, rightHalfWidth);
            AddField(performanceFlow, "药水监控毫秒", BotPotionMonitorIntervalMsEdit, rightHalfWidth);
            AddField(performanceFlow, "满血阈值百分比", BotFullHealthThresholdPercentEdit, rightHalfWidth);
            column.Controls.Add(performance);

            GroupBox quick = CreateGroup("快捷操作", RightPanelMinWidth - 20);
            FlowLayoutPanel quickFlow = GetGroupFlow(quick, false, rightContentWidth);
            AddButtonRow(quickFlow, rightContentWidth, RightQuickButtonMaxWidth,
                CreateButton("攻击性 +10", Color.FromArgb(205, 230, 205), delegate { ApplyRuntimeQuickTuning(BotRuntimeQuickTuningTarget.Aggression, 10); }),
                CreateButton("攻击性 -10", Color.FromArgb(230, 205, 205), delegate { ApplyRuntimeQuickTuning(BotRuntimeQuickTuningTarget.Aggression, -10); }));
            AddButtonRow(quickFlow, rightContentWidth, RightQuickButtonMaxWidth,
                CreateButton("活跃度 +10", Color.FromArgb(205, 230, 205), delegate { ApplyRuntimeQuickTuning(BotRuntimeQuickTuningTarget.Activity, 10); }),
                CreateButton("活跃度 -10", Color.FromArgb(230, 205, 205), delegate { ApplyRuntimeQuickTuning(BotRuntimeQuickTuningTarget.Activity, -10); }));
            AddButtonRow(quickFlow, rightContentWidth, RightQuickButtonMaxWidth,
                CreateButton("药水补给 +5", Color.FromArgb(205, 230, 205), delegate { ApplyRuntimeQuickTuning(BotRuntimeQuickTuningTarget.PotionMinimums, 5); }),
                CreateButton("药水补给 -5", Color.FromArgb(230, 205, 205), delegate { ApplyRuntimeQuickTuning(BotRuntimeQuickTuningTarget.PotionMinimums, -5); }));
            AddButtonRow(quickFlow, rightContentWidth, RightQuickButtonMaxWidth, BotQuickRecallButton, BotQuickPauseButton, BotQuickSyncButton);
            AddFullWidthControl(quickFlow, BotQuickActionStatusLabel, rightContentWidth);
            column.Controls.Add(quick);

            GroupBox quickMaps = CreateGroup("按档快速切图", RightPanelMinWidth - 20);
            FlowLayoutPanel quickMapsFlow = GetGroupFlow(quickMaps, false, rightContentWidth);
            List<Button> mapButtons = new List<Button>();
            foreach (BotLevelRangeOption option in _botMapRanges)
            {
                BotLevelRangeOption capturedOption = option;
                mapButtons.Add(CreateButton(option.Text, Color.FromArgb(190, 220, 250),
                    delegate { SwitchBotMapRange(capturedOption); }));
            }
            for (int index = 0; index < mapButtons.Count; index += 4)
                AddButtonRow(quickMapsFlow, rightContentWidth, MapButtonMaxWidth, mapButtons.Skip(index).Take(4).ToArray());
            column.Controls.Add(quickMaps);

            GroupBox features = CreateGroup("新增功能配置", RightPanelMinWidth - 20);
            FlowLayoutPanel featuresFlow = GetGroupFlow(features, true, rightContentWidth);
            AddField(featuresFlow, "快速攻击毫秒", BotAttackAttemptIntervalMsEdit, rightHalfWidth);
            AddField(featuresFlow, "快速捡取毫秒", BotPickupAttemptIntervalMsEdit, rightHalfWidth);
            AddField(featuresFlow, "拾取半径格数", BotPickupRadiusEdit, rightHalfWidth);
            AddField(featuresFlow, "地图池加成", BotMapPoolBonusEdit, rightHalfWidth);
            AddField(featuresFlow, "切图分差上限", BotMapSwitchScoreGapMaxEdit, rightHalfWidth);
            AddField(featuresFlow, "周期组队（秒）", BotPeriodicGroupSecondsEdit, rightHalfWidth);
            AddField(featuresFlow, "主AI每帧上限", BotMainActionsPerFrameEdit, rightHalfWidth);
            AddField(featuresFlow, "药水每帧上限", BotPotionActionsPerFrameEdit, rightHalfWidth);
            column.Controls.Add(features);

            column.ClientSizeChanged += delegate { ResizeRightColumnGroups(column); };
            ResizeRightColumnGroups(column);
            return column;
        }

        private void InitializeBotMapRanges()
        {
            _botMapRanges.Clear();
            _botMapRanges.Add(new BotLevelRangeOption { Text = "1-9级", MinLevel = 1, MaxLevel = 9 });
            _botMapRanges.Add(new BotLevelRangeOption { Text = "10-19级", MinLevel = 10, MaxLevel = 19 });
            _botMapRanges.Add(new BotLevelRangeOption { Text = "20-29级", MinLevel = 20, MaxLevel = 29 });
            _botMapRanges.Add(new BotLevelRangeOption { Text = "30-39级", MinLevel = 30, MaxLevel = 39 });
            _botMapRanges.Add(new BotLevelRangeOption { Text = "40-49级", MinLevel = 40, MaxLevel = 49 });
            _botMapRanges.Add(new BotLevelRangeOption { Text = "50-59级", MinLevel = 50, MaxLevel = 59 });
            _botMapRanges.Add(new BotLevelRangeOption { Text = "60-69级", MinLevel = 60, MaxLevel = 69 });
            _botMapRanges.Add(new BotLevelRangeOption { Text = "70级以上", MinLevel = 70, MaxLevel = int.MaxValue });
        }

        private void LoadBotSettings()
        {
            _loading = true;
            try
            {
                _loadedSettings = BotManagementSettings.FromConfig();
                ApplySettingsToControls(_loadedSettings);
                UpdateRecoveryChecks();
            }
            finally
            {
                _loading = false;
            }

            UpdateBotStatus();
        }

        private bool TryReadFormSettings(out BotManagementSettings settings, out string error)
        {
            settings = BotManagementSettings.FromConfig();
            settings.BotFilePath = BotFilePathEdit.Text.Trim();
            settings.BotCount = DecimalToInt(BotCountEdit.Value);
            settings.EnableBotSystem = BotEnableCheckEdit.Checked;
            settings.BotCreateGuild = BotCreateGuildCheckEdit.Checked;
            settings.BotAllowGroup = BotAllowGroupCheckEdit.Checked;
            settings.BotAttackPlayers = BotAttackPlayersCheckEdit.Checked;
            settings.BotEnableChat = BotEnableChatCheckEdit.Checked;
            settings.BotAutoLevel = BotAutoLevelCheckEdit.Checked;
            settings.BotAutoPickup = BotAutoPickupCheckEdit.Checked;
            settings.BotAutoSellTrash = BotAutoSellTrashCheckEdit.Checked;
            settings.BotAutoPotionSupply = BotAutoPotionSupplyCheckEdit.Checked;
            settings.BotAutoEquip = BotAutoEquipCheckEdit.Checked;
            settings.BotAutoLearnSkill = BotAutoLearnSkillCheckEdit.Checked;
            settings.BotAutoGroup = BotAutoGroupCheckEdit.Checked;
            settings.BotAutoTrade = BotAutoTradeCheckEdit.Checked;
            settings.BotGuildSystem = BotGuildSystemCheckEdit.Checked;
            settings.BotParticipateConquest = BotParticipateConquestCheckEdit.Checked;
            settings.BotPvpRetaliation = BotPvpRetaliationCheckEdit.Checked;
            settings.BotAutoMapSwitch = BotAutoMapSwitchCheckEdit.Checked;
            settings.BotSkipPickupWhenGroupedWithHuman = BotSkipPickupWhenGroupedWithHumanCheckEdit.Checked;
            settings.BotAutoRebirth = BotAutoRebirthCheckEdit.Checked;
            settings.PercentRecoveryEnabled = BotPercentRecoveryCheckEdit.Checked;
            settings.FixedRecoveryEnabled = BotFixedRecoveryCheckEdit.Checked;
            settings.BotAutoSpecialRepair = BotAutoSpecialRepairCheckEdit.Checked;

            settings.AggressionPercent = BotAggressionSlider.Value;
            settings.BotAggressionPercent = BotAggressionSlider.Value;
            settings.ActivityPercent = BotActivitySlider.Value;
            settings.BotActivityPercent = BotActivitySlider.Value;
            settings.GroupTendencyPercent = BotGroupTendencySlider.Value;
            settings.BotGroupTendencyPercent = BotGroupTendencySlider.Value;
            settings.ChatFrequencyPercent = BotChatFrequencySlider.Value;
            settings.BotChatFrequencyPercent = BotChatFrequencySlider.Value;

            settings.ProactivePvpMinLevel = DecimalToInt(BotProactivePvpMinLevelEdit.Value);
            settings.BotProactivePvpMinLevel = settings.ProactivePvpMinLevel;
            settings.AutoRebirthLevel = DecimalToInt(BotAutoRebirthLevelEdit.Value);
            settings.BotAutoRebirthLevel = settings.AutoRebirthLevel;
            settings.AutoRebirthMaxCount = DecimalToInt(BotAutoRebirthMaxCountEdit.Value);
            settings.BotAutoRebirthMaxCount = settings.AutoRebirthMaxCount;
            settings.BotDefenseLevelInterval = DecimalToInt(BotDefenseLevelIntervalEdit.Value);
            settings.BotDefenseBonusPerTier = DecimalToInt(BotDefenseBonusPerTierEdit.Value);
            settings.BotStrongElementStartLevel = DecimalToInt(BotStrongElementStartLevelEdit.Value);
            settings.BotStrongElementLevelInterval = DecimalToInt(BotStrongElementLevelIntervalEdit.Value);
            settings.BotStrongElementTypeCount = DecimalToInt(BotStrongElementTypeCountEdit.Value);
            settings.PercentRecoveryPerSecond = DecimalToInt(BotPercentRecoveryPerSecondEdit.Value);
            settings.BotPercentRecoveryPerSecond = settings.PercentRecoveryPerSecond;
            settings.FixedRecoveryPerSecond = DecimalToInt(BotFixedRecoveryPerSecondEdit.Value);
            settings.BotFixedRecoveryPerSecond = settings.FixedRecoveryPerSecond;
            settings.BotGlobalChatIntervalSeconds = DecimalToInt(BotGlobalChatIntervalSecondsEdit.Value);
            settings.BotSpecialRepairThresholdPercent = DecimalToInt(BotSpecialRepairThresholdPercentEdit.Value);
            settings.BotRecallBatchIntervalMs = DecimalToInt(BotRecallBatchIntervalMsEdit.Value);
            settings.BotRecallBatchSize = DecimalToInt(BotRecallBatchSizeEdit.Value);

            settings.BotInitialGoldFloor = DecimalToLong(BotInitialGoldFloorEdit.Value);
            settings.BotGoldFarmThreshold = DecimalToLong(BotGoldFarmThresholdEdit.Value);
            settings.BotMinHealthPotionCount = DecimalToInt(BotMinHealthPotionCountEdit.Value);
            settings.BotMinManaPotionCount = DecimalToInt(BotMinManaPotionCountEdit.Value);
            settings.BotTickDispatchLimit = DecimalToInt(BotTickDispatchLimitEdit.Value);
            settings.BotMainLoopIntervalMs = DecimalToInt(BotMainLoopIntervalMsEdit.Value);
            settings.BotMaxOnline = DecimalToInt(BotMaxOnlineEdit.Value);
            settings.BotPotionMonitorIntervalMs = DecimalToInt(BotPotionMonitorIntervalMsEdit.Value);
            settings.BotFullHealthThresholdPercent = DecimalToInt(BotFullHealthThresholdPercentEdit.Value);
            settings.BotAttackAttemptIntervalMs = DecimalToInt(BotAttackAttemptIntervalMsEdit.Value);
            settings.BotPickupAttemptIntervalMs = DecimalToInt(BotPickupAttemptIntervalMsEdit.Value);
            settings.BotPickupRadius = DecimalToInt(BotPickupRadiusEdit.Value);
            settings.BotMapPoolBonus = DecimalToInt(BotMapPoolBonusEdit.Value);
            settings.BotMapSwitchScoreGapMax = DecimalToInt(BotMapSwitchScoreGapMaxEdit.Value);
            settings.BotPeriodicGroupSeconds = DecimalToInt(BotPeriodicGroupSecondsEdit.Value);
            settings.MainActionsPerFrame = DecimalToInt(BotMainActionsPerFrameEdit.Value);
            settings.BotMainActionsPerFrame = settings.MainActionsPerFrame;
            settings.PotionActionsPerFrame = DecimalToInt(BotPotionActionsPerFrameEdit.Value);
            settings.BotPotionActionsPerFrame = settings.PotionActionsPerFrame;
            settings.BotLogDirectory = BotLogDirectoryEdit.Text.Trim();

            if (!settings.TryValidate(out error))
                return false;

            return true;
        }

        private bool ApplyFormSettings(bool persist)
        {
            if (!TryReadFormSettings(out BotManagementSettings settings, out string error))
            {
                ShowError(error);
                return false;
            }

            if (!BotManager.TryApplyManagementSettings(settings, persist, out error))
            {
                ShowError(error);
                return false;
            }

            _loadedSettings = settings;
            if (persist)
            {
                _runtimeQuickTuningStatusMessage = string.Empty;
                _runtimeQuickTuningWasActive = false;
                RefreshRuntimeQuickTuningControls(BotManager.GetRuntimeQuickTuningSnapshot(), false);
            }
            UpdateBotStatus();
            return true;
        }

        private void ApplySettingsToControls(BotManagementSettings settings)
        {
            BotFilePathEdit.Text = settings.BotFilePath ?? string.Empty;
            SetValue(BotCountEdit, settings.BotCount);
            BotEnableCheckEdit.Checked = settings.EnableBotSystem;
            BotCreateGuildCheckEdit.Checked = settings.BotCreateGuild;
            BotAllowGroupCheckEdit.Checked = settings.BotAllowGroup;
            BotAttackPlayersCheckEdit.Checked = settings.BotAttackPlayers;
            BotEnableChatCheckEdit.Checked = settings.BotEnableChat;
            BotAutoLevelCheckEdit.Checked = settings.BotAutoLevel;
            BotAutoPickupCheckEdit.Checked = settings.BotAutoPickup;
            BotAutoSellTrashCheckEdit.Checked = settings.BotAutoSellTrash;
            BotAutoPotionSupplyCheckEdit.Checked = settings.BotAutoPotionSupply;
            BotAutoEquipCheckEdit.Checked = settings.BotAutoEquip;
            BotAutoLearnSkillCheckEdit.Checked = settings.BotAutoLearnSkill;
            BotAutoGroupCheckEdit.Checked = settings.BotAutoGroup;
            BotAutoTradeCheckEdit.Checked = settings.BotAutoTrade;
            BotGuildSystemCheckEdit.Checked = settings.BotGuildSystem;
            BotParticipateConquestCheckEdit.Checked = settings.BotParticipateConquest;
            BotPvpRetaliationCheckEdit.Checked = settings.BotPvpRetaliation;
            BotAutoMapSwitchCheckEdit.Checked = settings.BotAutoMapSwitch;
            BotSkipPickupWhenGroupedWithHumanCheckEdit.Checked = settings.BotSkipPickupWhenGroupedWithHuman;
            BotAutoRebirthCheckEdit.Checked = settings.BotAutoRebirth;
            BotPercentRecoveryCheckEdit.Checked = settings.PercentRecoveryEnabled;
            BotFixedRecoveryCheckEdit.Checked = settings.FixedRecoveryEnabled;
            BotAutoSpecialRepairCheckEdit.Checked = settings.BotAutoSpecialRepair;

            BotAggressionSlider.Value = ClampPercent(settings.BotAggressionPercent);
            BotActivitySlider.Value = ClampPercent(settings.BotActivityPercent);
            BotGroupTendencySlider.Value = ClampPercent(settings.BotGroupTendencyPercent);
            BotChatFrequencySlider.Value = ClampPercent(settings.BotChatFrequencyPercent);
            UpdateSliderLabel(BotAggressionSlider, BotAggressionValueLabel);
            UpdateSliderLabel(BotActivitySlider, BotActivityValueLabel);
            UpdateSliderLabel(BotGroupTendencySlider, BotGroupTendencyValueLabel);
            UpdateSliderLabel(BotChatFrequencySlider, BotChatFrequencyValueLabel);

            SetValue(BotProactivePvpMinLevelEdit, settings.BotProactivePvpMinLevel);
            SetValue(BotAutoRebirthLevelEdit, settings.BotAutoRebirthLevel);
            SetValue(BotAutoRebirthMaxCountEdit, settings.BotAutoRebirthMaxCount);
            SetValue(BotDefenseLevelIntervalEdit, settings.BotDefenseLevelInterval);
            SetValue(BotDefenseBonusPerTierEdit, settings.BotDefenseBonusPerTier);
            SetValue(BotStrongElementStartLevelEdit, settings.BotStrongElementStartLevel);
            SetValue(BotStrongElementLevelIntervalEdit, settings.BotStrongElementLevelInterval);
            SetValue(BotStrongElementTypeCountEdit, settings.BotStrongElementTypeCount);
            SetValue(BotPercentRecoveryPerSecondEdit, settings.PercentRecoveryPerSecond);
            SetValue(BotFixedRecoveryPerSecondEdit, settings.FixedRecoveryPerSecond);
            SetValue(BotGlobalChatIntervalSecondsEdit, settings.BotGlobalChatIntervalSeconds);
            SetValue(BotSpecialRepairThresholdPercentEdit, settings.BotSpecialRepairThresholdPercent);
            SetValue(BotRecallBatchIntervalMsEdit, settings.BotRecallBatchIntervalMs);
            SetValue(BotRecallBatchSizeEdit, settings.BotRecallBatchSize);
            SetValue(BotInitialGoldFloorEdit, settings.BotInitialGoldFloor);
            SetValue(BotGoldFarmThresholdEdit, settings.BotGoldFarmThreshold);
            SetValue(BotMinHealthPotionCountEdit, settings.BotMinHealthPotionCount);
            SetValue(BotMinManaPotionCountEdit, settings.BotMinManaPotionCount);
            SetValue(BotTickDispatchLimitEdit, settings.BotTickDispatchLimit);
            SetValue(BotMainLoopIntervalMsEdit, settings.BotMainLoopIntervalMs);
            SetValue(BotMaxOnlineEdit, settings.BotMaxOnline);
            SetValue(BotPotionMonitorIntervalMsEdit, settings.BotPotionMonitorIntervalMs);
            SetValue(BotFullHealthThresholdPercentEdit, settings.BotFullHealthThresholdPercent);
            SetValue(BotAttackAttemptIntervalMsEdit, settings.BotAttackAttemptIntervalMs);
            SetValue(BotPickupAttemptIntervalMsEdit, settings.BotPickupAttemptIntervalMs);
            SetValue(BotPickupRadiusEdit, settings.BotPickupRadius);
            SetValue(BotMapPoolBonusEdit, settings.BotMapPoolBonus);
            SetValue(BotMapSwitchScoreGapMaxEdit, settings.BotMapSwitchScoreGapMax);
            SetValue(BotPeriodicGroupSecondsEdit, settings.BotPeriodicGroupSeconds);
            SetValue(BotMainActionsPerFrameEdit, settings.BotMainActionsPerFrame);
            SetValue(BotPotionActionsPerFrameEdit, settings.BotPotionActionsPerFrame);
            BotLogDirectoryEdit.Text = settings.BotLogDirectory ?? string.Empty;
        }

        private void RefreshTimer_Tick(object sender, EventArgs e)
        {
            if (IsDisposed) return;
            RefreshSnapshot(BotManager.GetManagementSnapshot());
        }

        private void RefreshSnapshot(BotManagementSnapshot snapshot)
        {
            if (snapshot == null) return;

            BotStatusLabel.Text = snapshot.IsRunning
                ? string.Format("状态: {0}，在线假人: {1}，目标: {2}", snapshot.IsPaused ? "已暂停" : "运行中",
                    snapshot.OnlineBotCount, BotManager.BotCount)
                : "状态: 已停止";
            BotPauseButton.Text = snapshot.IsPaused ? "继续" : "暂停";
            BotQuickPauseButton.Text = snapshot.IsPaused ? "继续" : "暂停";
            BotStatisticsLabel.Text = string.Format(
                "在线假人: {0}    总击杀: {1}    死亡数: {2}\r\n覆盖地图: {3}    总金币: {4}    平均等级: {5:0.00}",
                snapshot.OnlineBotCount, snapshot.TotalKills, snapshot.TotalDeaths, snapshot.CoveredMapCount,
                snapshot.TotalGold, snapshot.AverageLevel);
            BotActivityStateLabel.Text = snapshot.IsPaused ? "普通 AI 状态: 已暂停（保命与连接维护继续）" : "普通 AI 状态: 运行中";
            RefreshRuntimeQuickTuningControls(BotManager.GetRuntimeQuickTuningSnapshot(), false);

            BotListView.BeginUpdate();
            try
            {
                BotListView.Items.Clear();
                foreach (BotManagementRow row in snapshot.Bots)
                {
                    ListViewItem item = new ListViewItem(row.Name ?? string.Empty);
                    item.SubItems.Add(row.Level.ToString());
                    item.SubItems.Add(row.MapIndex.ToString());
                    item.SubItems.Add(row.Gold.ToString());
                    item.SubItems.Add(row.State ?? string.Empty);
                    BotListView.Items.Add(item);
                }
            }
            finally
            {
                BotListView.EndUpdate();
            }

            BotActivityLogBox.Text = string.Join(Environment.NewLine, snapshot.ActivityLogs);
            BotOperationLogBox.Text = string.Join(Environment.NewLine, snapshot.OperationLogs);
            if (BotActivityLogBox.TextLength > 0) BotActivityLogBox.SelectionStart = BotActivityLogBox.TextLength;
            if (BotOperationLogBox.TextLength > 0) BotOperationLogBox.SelectionStart = BotOperationLogBox.TextLength;
        }

        private void ApplyRuntimeQuickTuning(BotRuntimeQuickTuningTarget target, int delta)
        {
            BotRuntimeQuickTuningSnapshot snapshot = BotManager.AdjustRuntimeQuickTuning(target, delta);
            if (snapshot != null && !string.IsNullOrWhiteSpace(snapshot.Message))
                _runtimeQuickTuningStatusMessage = snapshot.Message;
            RefreshRuntimeQuickTuningControls(snapshot, true);
        }

        private void RefreshRuntimeQuickTuningControls(BotRuntimeQuickTuningSnapshot snapshot, bool showMessage)
        {
            if (snapshot == null) return;

            BotAggressionSlider.Value = ClampPercent(snapshot.AggressionPercent);
            BotActivitySlider.Value = ClampPercent(snapshot.ActivityPercent);
            SetValue(BotMinHealthPotionCountEdit, snapshot.MinHealthPotionCount);
            SetValue(BotMinManaPotionCountEdit, snapshot.MinManaPotionCount);
            UpdateSliderLabel(BotAggressionSlider, BotAggressionValueLabel);
            UpdateSliderLabel(BotActivitySlider, BotActivityValueLabel);

            if (showMessage && !string.IsNullOrWhiteSpace(snapshot.Message))
                _runtimeQuickTuningStatusMessage = snapshot.Message;
            else if (!showMessage && !snapshot.Active && _runtimeQuickTuningWasActive)
                _runtimeQuickTuningStatusMessage = "快捷调整：已恢复保存基线";

            if (!string.IsNullOrWhiteSpace(_runtimeQuickTuningStatusMessage))
                BotQuickActionStatusLabel.Text = _runtimeQuickTuningStatusMessage;
            else if (!snapshot.Active)
                BotQuickActionStatusLabel.Text = "快捷调整：未启用";
            else
                BotQuickActionStatusLabel.Text = snapshot.Changed ? "快捷调整：临时值已生效" : "快捷调整：当前为保存基线";
            _runtimeQuickTuningWasActive = snapshot.Active;
        }

        private void UpdateBotStatus()
        {
            bool running = BotManager.IsRunning;
            BotStartButton.Enabled = !running;
            BotStopButton.Enabled = running;
            BotRecallButton.Enabled = running;
            BotPauseButton.Enabled = running;
            BotQuickRecallButton.Enabled = running;
            BotQuickPauseButton.Enabled = running;
            BotQuickSyncButton.Enabled = true;
            BotSwitchMapButton.Enabled = running;
            BotForceSwitchAllButton.Enabled = running;
        }

        private void BotStartButton_Click(object sender, EventArgs e)
        {
            string filePath = BotFilePathEdit.Text.Trim();
            if (string.IsNullOrWhiteSpace(filePath) || !File.Exists(filePath))
            {
                ShowError("假人配置文件不存在，请先选择有效文件。");
                return;
            }

            if (BotManager.IsRunning)
            {
                ShowError("假人系统已经运行。");
                return;
            }

            if (!ApplyFormSettings(true)) return;

            BotManager.Start(filePath, DecimalToInt(BotCountEdit.Value));
            UpdateBotStatus();
            if (BotManager.IsRunning)
                MessageBox.Show("假人系统已启动。", "提示", MessageBoxButtons.OK, MessageBoxIcon.Information);
            else
                MessageBox.Show("服务器数据库尚未就绪，启动已延后，请先启动服务器。", "提示", MessageBoxButtons.OK, MessageBoxIcon.Information);
        }

        private void BotStopButton_Click(object sender, EventArgs e)
        {
            BotManagementSnapshot snapshot = BotManager.GetManagementSnapshot();
            if (!BotManager.IsRunning) return;

            DialogResult confirm = MessageBox.Show(
                string.Format("确定停止假人系统并让当前在线的 {0} 名假人下线吗？", snapshot.OnlineBotCount),
                "停止假人", MessageBoxButtons.YesNo, MessageBoxIcon.Warning);
            if (confirm != DialogResult.Yes) return;

            BotManager.Stop();
            UpdateBotStatus();
        }

        private void BotRecallButton_Click(object sender, EventArgs e)
        {
            BotManagementSnapshot snapshot = BotManager.GetManagementSnapshot();
            if (!BotManager.IsRunning || snapshot.OnlineBotCount == 0)
            {
                MessageBox.Show("当前没有可回城的在线假人。", "提示", MessageBoxButtons.OK, MessageBoxIcon.Information);
                return;
            }

            DialogResult confirm = MessageBox.Show(
                string.Format("确定将当前在线的 {0} 名假人分批传送回城吗？", snapshot.OnlineBotCount),
                "所有假人回城", MessageBoxButtons.YesNo, MessageBoxIcon.Question);
            if (confirm != DialogResult.Yes) return;

            BotBatchResult result = BotManager.RecallAllBots();
            MessageBox.Show(FormatBatchResult("回城指令已发送", result), "回城", MessageBoxButtons.OK, MessageBoxIcon.Information);
        }

        private void BotPauseButton_Click(object sender, EventArgs e)
        {
            BotManager.SetPaused(!BotManager.IsPaused);
            RefreshSnapshot(BotManager.GetManagementSnapshot());
        }

        private void BotSaveButton_Click(object sender, EventArgs e)
        {
            if (ApplyFormSettings(true))
                MessageBox.Show("配置已校验、保存并应用。", "保存配置", MessageBoxButtons.OK, MessageBoxIcon.Information);
        }

        private void BotRefreshButton_Click(object sender, EventArgs e)
        {
            RefreshSnapshot(BotManager.GetManagementSnapshot());
        }

        private void BotSyncButton_Click(object sender, EventArgs e)
        {
            if (!ApplyFormSettings(true)) return;

            BotBatchResult syncResult = BotManager.SyncOnlineBots();
            BotManagementSnapshot snapshot = BotManager.GetManagementSnapshot();
            BotBatchResult trimResult = null;
            int excess = Math.Max(0, snapshot.OnlineBotCount - Config.BotMaxOnline);
            if (excess > 0)
            {
                DialogResult confirm = MessageBox.Show(
                    string.Format("最大在线已低于当前在线数量，将有 {0} 名假人超出上限。是否按当前批量规则下线超额假人？", excess),
                    "确认超额在线处理", MessageBoxButtons.YesNo, MessageBoxIcon.Warning);
                if (confirm == DialogResult.Yes)
                    trimResult = BotManager.TrimOnlineBotsToMaxOnline();
            }

            string message = FormatBatchResult("在线同步已投递", syncResult);
            if (trimResult != null)
                message += Environment.NewLine + FormatBatchResult("超额在线处理", trimResult);
            MessageBox.Show(message, "同步在线假人", MessageBoxButtons.OK, MessageBoxIcon.Information);
        }

        private void BotBackfillRewardsButton_Click(object sender, EventArgs e)
        {
            BotBatchResult result = BotManager.BackfillMissingBotRewards();
            MessageBox.Show(FormatBatchResult("奖励补发", result), "补充防御强元素", MessageBoxButtons.OK, MessageBoxIcon.Information);
        }

        private void BotRewardReportButton_Click(object sender, EventArgs e)
        {
            IReadOnlyList<BotRewardGap> gaps = BotManager.GetMissingBotRewardReport();
            List<string> lines = gaps.Select(gap => string.Format("{0} / {1} / 等级 {2}: 双防缺 {3} 段，强元素缺 {4} 段",
                gap.BotId, gap.CharacterName, gap.Level, gap.MissingDefenseTiers, gap.MissingStrongElementTiers)).ToList();
            ShowReport("奖励漏发清单", lines.Count == 0 ? "没有发现奖励漏发。" : string.Join(Environment.NewLine, lines));
        }

        private void BotMapProbButton_Click(object sender, EventArgs e)
        {
            ShowReport("假人地图概率分布统计", BotManager.GetBotMapProbabilityReport());
        }

        private void BotSwitchMapButton_Click(object sender, EventArgs e)
        {
            BotLevelRangeOption option = BotMapRangeComboBox.SelectedItem as BotLevelRangeOption;
            if (option != null) SwitchBotMapRange(option);
        }

        private void SwitchBotMapRange(BotLevelRangeOption option)
        {
            if (option == null || !BotManager.IsRunning) return;

            BotManagementSnapshot snapshot = BotManager.GetManagementSnapshot();
            DialogResult confirm = MessageBox.Show(
                string.Format("确定为 {0} 在线假人执行按档随机切图吗？当前在线共 {1} 名。", option.Text, snapshot.OnlineBotCount),
                "按档随机切图", MessageBoxButtons.YesNo, MessageBoxIcon.Question);
            if (confirm != DialogResult.Yes) return;

            BotBatchResult result = BotManager.SwitchOnlineBotsMapByLevelRange(option.MinLevel, option.MaxLevel);
            MessageBox.Show(FormatBatchResult("按档切图", result), "按档切图", MessageBoxButtons.OK, MessageBoxIcon.Information);
        }

        private void BotForceSwitchAllButton_Click(object sender, EventArgs e)
        {
            if (!BotManager.IsRunning) return;

            BotManagementSnapshot snapshot = BotManager.GetManagementSnapshot();
            DialogResult confirm = MessageBox.Show(
                string.Format("确定对当前 {0} 名在线假人执行强制一键按档切图吗？现有真人带队和城战保护仍会跳过。", snapshot.OnlineBotCount),
                "强制一键按档切图", MessageBoxButtons.YesNo, MessageBoxIcon.Warning);
            if (confirm != DialogResult.Yes) return;

            BotManager.BotForceSwitchAllRangesResult result =
                BotManager.ForceSwitchOnlineBotsByLevelRangesAndRebuild(BuildBotLevelRangeRequests());
            if (result == null)
            {
                ShowError("强制切图没有返回结果。");
                return;
            }

            List<string> lines = result.Summaries.Select(summary => string.Format("{0}: 成功 {1} 名，目标 {2}",
                summary.RangeText, summary.SwitchedCount,
                string.IsNullOrWhiteSpace(summary.TargetMapName) ? "无合适地图" : summary.TargetMapName)).ToList();
            string report = string.IsNullOrWhiteSpace(result.ErrorMessage)
                ? string.Join(Environment.NewLine, lines)
                : result.ErrorMessage;
            if (result.TimedOut) report += Environment.NewLine + "操作已超时，请查看操作日志。";
            ShowReport("强制一键按档切图", report);
        }

        private List<BotManager.BotManualLevelRangeRequest> BuildBotLevelRangeRequests()
        {
            return _botMapRanges.Select(option => new BotManager.BotManualLevelRangeRequest
            {
                Text = option.Text,
                MinLevel = option.MinLevel,
                MaxLevel = option.MaxLevel,
            }).ToList();
        }

        private void BotPercentRecoveryCheckEdit_CheckedChanged(object sender, EventArgs e)
        {
            if (!_loading && BotPercentRecoveryCheckEdit.Checked)
                BotFixedRecoveryCheckEdit.Checked = false;
            UpdateRecoveryChecks();
        }

        private void BotFixedRecoveryCheckEdit_CheckedChanged(object sender, EventArgs e)
        {
            if (!_loading && BotFixedRecoveryCheckEdit.Checked)
                BotPercentRecoveryCheckEdit.Checked = false;
            UpdateRecoveryChecks();
        }

        private void UpdateRecoveryChecks()
        {
            if (BotPercentRecoveryCheckEdit == null || BotFixedRecoveryCheckEdit == null) return;
            BotPercentRecoveryCheckEdit.CheckedChanged -= BotPercentRecoveryCheckEdit_CheckedChanged;
            BotFixedRecoveryCheckEdit.CheckedChanged -= BotFixedRecoveryCheckEdit_CheckedChanged;
            BotPercentRecoveryCheckEdit.CheckedChanged += BotPercentRecoveryCheckEdit_CheckedChanged;
            BotFixedRecoveryCheckEdit.CheckedChanged += BotFixedRecoveryCheckEdit_CheckedChanged;
        }

        private void BtnBrowse_Click(object sender, EventArgs e)
        {
            using (OpenFileDialog dialog = new OpenFileDialog())
            {
                dialog.Filter = "文本文件 (*.txt)|*.txt|所有文件 (*.*)|*.*";
                if (dialog.ShowDialog(this) == DialogResult.OK)
                    BotFilePathEdit.Text = dialog.FileName;
            }
        }

        private void BotConfigView_FormClosed(object sender, FormClosedEventArgs e)
        {
            CleanupRefreshTimer();
        }

        protected override void Dispose(bool disposing)
        {
            if (disposing)
                CleanupRefreshTimer();
            base.Dispose(disposing);
        }

        private void CleanupRefreshTimer()
        {
            if (_cleanedUp) return;
            _cleanedUp = true;
            if (_refreshTimer == null) return;
            _refreshTimer.Stop();
            _refreshTimer.Tick -= RefreshTimer_Tick;
            _refreshTimer.Dispose();
            _refreshTimer = null;
        }

        private static FlowLayoutPanel CreateColumn()
        {
            FlowLayoutPanel column = new FlowLayoutPanel
            {
                Dock = DockStyle.Fill,
                AutoScroll = true,
                FlowDirection = FlowDirection.TopDown,
                WrapContents = false,
                Padding = new Padding(6),
            };
            column.HorizontalScroll.Enabled = false;
            return column;
        }

        private static GroupBox CreateGroup(string title, int width)
        {
            return new GroupBox
            {
                Text = title,
                Width = width,
                MinimumSize = new Size(width, 0),
                AutoSize = false,
                AutoSizeMode = AutoSizeMode.GrowAndShrink,
                Padding = new Padding(8, 18, 8, 8),
            };
        }

        private static FlowLayoutPanel GetGroupFlow(GroupBox group, bool twoColumn, int contentWidth)
        {
            FlowLayoutPanel flow = new FlowLayoutPanel
            {
                Dock = DockStyle.Top,
                Width = contentWidth,
                AutoSize = true,
                AutoSizeMode = AutoSizeMode.GrowAndShrink,
                FlowDirection = twoColumn ? FlowDirection.LeftToRight : FlowDirection.TopDown,
                WrapContents = twoColumn,
                Tag = twoColumn,
            };
            flow.HorizontalScroll.Enabled = false;
            flow.ClientSizeChanged += delegate
            {
                ResizeGroupFlowRows(flow);
                ResizeGroupHeight(flow);
            };
            group.Controls.Add(flow);
            return flow;
        }

        private void AddPathRow(FlowLayoutPanel flow, string labelText, int rowWidth)
        {
            Panel row = CreateRow(rowWidth, 35);
            row.Tag = "path";
            Label label = CreateRowLabel(labelText);
            Button browse = CreateButton("...", Color.LightGray, BtnBrowse_Click);
            row.Controls.Add(label);
            row.Controls.Add(BotFilePathEdit);
            row.Controls.Add(browse);
            row.Resize += delegate { ResizePathRow(row, label, BotFilePathEdit, browse); };
            ResizePathRow(row, label, BotFilePathEdit, browse);
            flow.Controls.Add(row);
        }

        private static void AddField(FlowLayoutPanel flow, string labelText, Control control, int rowWidth)
        {
            Panel row = CreateRow(rowWidth, Math.Max(31, control.Height + 7));
            row.Tag = "field";
            Label label = CreateRowLabel(labelText);
            row.Controls.Add(label);
            row.Controls.Add(control);
            ResizeFieldRow(row);
            flow.Controls.Add(row);
        }

        private static void AddInline(FlowLayoutPanel flow, string prefix, Control control, string suffix, int rowWidth)
        {
            Panel row = CreateRow(rowWidth, Math.Max(31, control.Height + 7));
            row.Tag = "inline";
            Label prefixLabel = new Label { Text = prefix, Location = new Point(0, 7), AutoSize = true };
            control.Location = new Point(55, (row.Height - control.Height) / 2);
            Label suffixLabel = new Label { Text = suffix, Location = new Point(150, 7), AutoSize = true };
            row.Controls.Add(prefixLabel);
            row.Controls.Add(control);
            row.Controls.Add(suffixLabel);
            flow.Controls.Add(row);
        }

        private static void AddCheck(FlowLayoutPanel flow, CheckBox check, int rowWidth)
        {
            check.AutoSize = false;
            check.Width = rowWidth;
            check.Height = 24;
            check.Margin = new Padding(0);
            check.Tag = "half";
            flow.Controls.Add(check);
        }

        private static void AddFullWidthControl(FlowLayoutPanel flow, Control control, int rowWidth)
        {
            control.Tag = "full";
            if (control is Label)
            {
                Label label = (Label)control;
                label.AutoSize = false;
                label.AutoEllipsis = false;
                label.Height = Math.Max(24, label.Height);
            }
            control.Margin = new Padding(0);
            control.Width = rowWidth;
            flow.Controls.Add(control);
        }

        private static void AddButtonRow(FlowLayoutPanel flow, int rowWidth, params Button[] buttons)
        {
            AddButtonRow(flow, rowWidth, 0, buttons);
        }

        private static void AddButtonRow(FlowLayoutPanel flow, int rowWidth, int maxButtonWidth, params Button[] buttons)
        {
            Panel row = CreateRow(rowWidth, 35);
            row.Tag = "button";
            foreach (Button button in buttons)
            {
                if (maxButtonWidth > 0)
                    button.MaximumSize = new Size(maxButtonWidth, button.Height);
                row.Controls.Add(button);
            }
            row.Resize += delegate { ResizeButtonRow(row); };
            ResizeButtonRow(row);
            flow.Controls.Add(row);
        }

        private static void AddSliderRow(FlowLayoutPanel flow, string labelText, TrackBar slider, Label valueLabel, int rowWidth)
        {
            Panel row = CreateRow(rowWidth, 48);
            row.Tag = "slider";
            Label label = CreateRowLabel(labelText);
            row.Controls.Add(label);
            row.Controls.Add(slider);
            row.Controls.Add(valueLabel);
            row.Resize += delegate { ResizeSliderRow(row); };
            ResizeSliderRow(row);
            flow.Controls.Add(row);
        }

        private static Panel CreateRow(int width, int height)
        {
            return new Panel { Width = width, Height = height, Margin = new Padding(0) };
        }

        private static Label CreateRowLabel(string text)
        {
            return new Label
            {
                Text = text,
                Location = new Point(0, 8),
                Width = 175,
                Height = 20,
                AutoEllipsis = false,
            };
        }

        private static void ResizeRightColumnGroups(FlowLayoutPanel column)
        {
            if (column == null) return;

            int availableWidth = column.DisplayRectangle.Width;
            int groupWidth = Math.Max(RightPanelMinWidth - 20, availableWidth - 2);
            foreach (GroupBox group in column.Controls.OfType<GroupBox>())
            {
                group.Width = groupWidth;
                foreach (FlowLayoutPanel flow in group.Controls.OfType<FlowLayoutPanel>())
                {
                    flow.Width = Math.Max(1, group.ClientSize.Width - group.Padding.Horizontal);
                    ResizeGroupFlowRows(flow);
                    ResizeGroupHeight(flow);
                }
            }
        }

        private static void ResizeColumnGroups(FlowLayoutPanel column)
        {
            if (column == null) return;

            foreach (GroupBox group in column.Controls.OfType<GroupBox>())
            {
                foreach (FlowLayoutPanel flow in group.Controls.OfType<FlowLayoutPanel>())
                {
                    ResizeGroupFlowRows(flow);
                    ResizeGroupHeight(flow);
                }
            }
        }

        private static void ResizeGroupHeight(FlowLayoutPanel flow)
        {
            if (flow == null) return;

            GroupBox group = flow.Parent as GroupBox;
            if (group == null) return;

            int chromeHeight = group.Height - group.ClientSize.Height;
            int flowBottom = Math.Max(flow.Bottom, flow.Top + flow.PreferredSize.Height);
            int requiredClientHeight = flowBottom + group.Padding.Bottom;
            group.Height = Math.Max(group.MinimumSize.Height, requiredClientHeight + chromeHeight);
        }

        private static void ResizeGroupFlowRows(FlowLayoutPanel flow)
        {
            if (flow == null) return;

            bool twoColumn = flow.Tag is bool && (bool)flow.Tag;
            int availableWidth = Math.Max(1, flow.ClientSize.Width);
            int halfWidth = Math.Max(1, (availableWidth - 5) / 2);
            foreach (Control control in flow.Controls)
            {
                string tag = control.Tag as string;
                bool half = twoColumn && (tag == "half" || tag == "field" || tag == "inline");
                int width = half ? halfWidth : availableWidth;
                control.Width = width;
                Panel row = control as Panel;
                if (row == null) continue;

                switch (row.Tag as string)
                {
                    case "field":
                        ResizeFieldRow(row);
                        break;
                    case "path":
                        ResizePathRow(row, row.Controls[0] as Label, row.Controls[1], row.Controls[2] as Button);
                        break;
                    case "button":
                        ResizeButtonRow(row);
                        break;
                    case "slider":
                        ResizeSliderRow(row);
                        break;
                }
            }
        }

        private static void ResizeFieldRow(Panel row)
        {
            if (row == null || row.Controls.Count < 2) return;
            Label label = row.Controls[0] as Label;
            Control control = row.Controls[1];
            if (label == null) return;
            label.Width = Math.Max(1, row.ClientSize.Width - control.Width - 5);
            label.Location = new Point(0, Math.Max(0, (row.Height - label.Height) / 2));
            control.Location = new Point(row.ClientSize.Width - control.Width, Math.Max(0, (row.Height - control.Height) / 2));
        }

        private static void ResizePathRow(Panel row, Label label, Control edit, Button browse)
        {
            if (row == null || label == null || edit == null || browse == null) return;
            label.Width = Math.Min(175, Math.Max(90, row.ClientSize.Width - 230));
            label.Location = new Point(0, 8);
            browse.Width = 38;
            browse.Location = new Point(row.ClientSize.Width - browse.Width, 2);
            edit.Location = new Point(label.Width + 5, 4);
            edit.Width = Math.Max(80, row.ClientSize.Width - edit.Left - browse.Width - 5);
        }

        private static void ResizeButtonRow(Panel row)
        {
            if (row == null || row.Controls.Count == 0) return;
            Button[] buttons = row.Controls.OfType<Button>().ToArray();
            if (buttons.Length == 0) return;

            int gaps = 5 * (buttons.Length - 1);
            int availableButtonWidth = Math.Max(1, row.ClientSize.Width - gaps);
            int width = Math.Max(1, availableButtonWidth / buttons.Length);
            int configuredMaximum = buttons
                .Where(button => button.MaximumSize.Width > 0)
                .Select(button => button.MaximumSize.Width)
                .DefaultIfEmpty(width)
                .Min();
            width = Math.Min(width, configuredMaximum);

            int totalWidth = width * buttons.Length + gaps;
            int x = Math.Max(0, (row.ClientSize.Width - totalWidth) / 2);
            foreach (Button button in buttons)
            {
                button.Location = new Point(x, 2);
                button.Width = width;
                x += width + 5;
            }
        }

        private static void ResizeSliderRow(Panel row)
        {
            if (row == null || row.Controls.Count < 3) return;
            Label label = row.Controls[0] as Label;
            TrackBar slider = row.Controls[1] as TrackBar;
            Label valueLabel = row.Controls[2] as Label;
            if (label == null || slider == null || valueLabel == null) return;
            int valueWidth = Math.Max(35, valueLabel.PreferredWidth);
            int labelWidth = Math.Min(175, Math.Max(70, row.ClientSize.Width / 3));
            label.Width = labelWidth;
            label.Location = new Point(0, 14);
            slider.Location = new Point(labelWidth + 5, 0);
            slider.Width = Math.Max(50, row.ClientSize.Width - labelWidth - valueWidth - 10);
            valueLabel.Location = new Point(row.ClientSize.Width - valueWidth, 14);
        }

        private static Button CreateButton(string text, Color color, EventHandler handler)
        {
            Button button = new Button
            {
                Text = text,
                Width = 135,
                Height = 30,
                BackColor = color,
                FlatStyle = FlatStyle.Flat,
                UseVisualStyleBackColor = false,
            };
            if (handler != null) button.Click += handler;
            return button;
        }

        private static CheckBox CreateCheck(string name, string text)
        {
            return new CheckBox { Name = name, Text = text, AutoSize = true };
        }

        private static NumericUpDown CreateNumeric(string name, decimal minimum, decimal maximum, decimal value)
        {
            NumericUpDown editor = new NumericUpDown
            {
                Name = name,
                Minimum = minimum,
                Maximum = maximum,
                Increment = 1,
                Width = 95,
                ThousandsSeparator = true,
            };
            SetValue(editor, value);
            return editor;
        }

        private static TrackBar CreateSlider(string name)
        {
            return new TrackBar
            {
                Name = name,
                Minimum = 0,
                Maximum = 100,
                Value = 50,
                TickFrequency = 10,
                SmallChange = 1,
                LargeChange = 10,
            };
        }

        private static TextBox CreateLogBox(string name)
        {
            return new TextBox
            {
                Name = name,
                Multiline = true,
                ReadOnly = true,
                ScrollBars = ScrollBars.Vertical,
                Height = 125,
                Width = 475,
                Font = new Font("Consolas", 9),
            };
        }

        private static void SetValue(NumericUpDown editor, long value)
        {
            SetValue(editor, (decimal)value);
        }

        private static void SetValue(NumericUpDown editor, decimal value)
        {
            if (editor == null) return;
            editor.Value = Math.Max(editor.Minimum, Math.Min(editor.Maximum, value));
        }

        private static int DecimalToInt(decimal value)
        {
            return decimal.ToInt32(value);
        }

        private static long DecimalToLong(decimal value)
        {
            return decimal.ToInt64(value);
        }

        private static int ClampPercent(int value)
        {
            return Math.Max(0, Math.Min(100, value));
        }

        private static void UpdateSliderLabel(TrackBar slider, Label label)
        {
            if (slider != null && label != null)
                label.Text = slider.Value + "%";
        }

        private static string FormatBatchResult(string title, BotBatchResult result)
        {
            if (result == null) return title + "：没有返回结果。";
            string error = string.IsNullOrWhiteSpace(result.ErrorMessage) ? string.Empty : "，说明: " + result.ErrorMessage;
            return string.Format("{0}：成功 {1}，失败 {2}，保护 {3}，跳过 {4}，排队 {5}，超时 {6}{7}",
                title, result.Succeeded, result.Failed, result.Protected, result.Skipped, result.Queued, result.Timeout, error);
        }

        private static void ShowReport(string title, string report)
        {
            using (Form reportForm = new Form
            {
                Text = title,
                Size = new Size(720, 560),
                StartPosition = FormStartPosition.CenterParent,
                MaximizeBox = false,
            })
            {
                TextBox reportBox = new TextBox
                {
                    Multiline = true,
                    ReadOnly = true,
                    ScrollBars = ScrollBars.Vertical,
                    Dock = DockStyle.Fill,
                    Font = new Font("Consolas", 9),
                    Text = report ?? string.Empty,
                };
                reportForm.Controls.Add(reportBox);
                reportForm.ShowDialog();
            }
        }

        private static void ShowError(string message)
        {
            MessageBox.Show(message ?? "操作失败。", "错误", MessageBoxButtons.OK, MessageBoxIcon.Warning);
        }
    }
}
