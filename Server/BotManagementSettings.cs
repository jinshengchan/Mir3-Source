using Server.Envir;
using System;

namespace Server
{
    /// <summary>
    /// 假人管理面板的 detached 配置快照。UI 只修改此对象，校验成功后一次性写入 Config。
    /// </summary>
    public sealed class BotManagementSettings
    {
        public bool EnableBotSystem { get; set; }
        public string BotFilePath { get; set; }
        public int BotCount { get; set; }
        public bool BotCreateGuild { get; set; }
        public bool BotAllowGroup { get; set; }
        public bool BotAttackPlayers { get; set; }

        public int AggressionPercent { get; set; }
        public int ActivityPercent { get; set; }
        public int GroupTendencyPercent { get; set; }
        public int ChatFrequencyPercent { get; set; }
        public bool PercentRecoveryEnabled { get; set; }
        public bool FixedRecoveryEnabled { get; set; }
        public int PercentRecoveryPerSecond { get; set; }
        public int FixedRecoveryPerSecond { get; set; }
        public int ProactivePvpMinLevel { get; set; }
        public int AutoRebirthLevel { get; set; }
        public int AutoRebirthMaxCount { get; set; }
        public int MainActionsPerFrame { get; set; }
        public int PotionActionsPerFrame { get; set; }

        public bool BotEnableChat { get; set; }
        public bool BotAutoLevel { get; set; }
        public bool BotAutoPickup { get; set; }
        public bool BotAutoSellTrash { get; set; }
        public bool BotAutoPotionSupply { get; set; }
        public bool BotAutoEquip { get; set; }
        public bool BotAutoLearnSkill { get; set; }
        public bool BotAutoGroup { get; set; }
        public bool BotAutoTrade { get; set; }
        public bool BotGuildSystem { get; set; }
        public bool BotParticipateConquest { get; set; }
        public bool BotPvpRetaliation { get; set; }
        public bool BotAutoMapSwitch { get; set; }
        public bool BotSkipPickupWhenGroupedWithHuman { get; set; }
        public bool BotAutoRebirth { get; set; }
        public bool BotPercentRecoveryEnabled { get; set; }
        public bool BotFixedRecoveryEnabled { get; set; }
        public bool BotAutoSpecialRepair { get; set; }
        public int BotProactivePvpMinLevel { get; set; }
        public int BotAutoRebirthLevel { get; set; }
        public int BotAutoRebirthMaxCount { get; set; }
        public int BotDefenseLevelInterval { get; set; }
        public int BotDefenseBonusPerTier { get; set; }
        public int BotStrongElementStartLevel { get; set; }
        public int BotStrongElementLevelInterval { get; set; }
        public int BotStrongElementTypeCount { get; set; }
        public int BotPercentRecoveryPerSecond { get; set; }
        public int BotFixedRecoveryPerSecond { get; set; }
        public int BotGlobalChatIntervalSeconds { get; set; }
        public int BotSpecialRepairThresholdPercent { get; set; }
        public int BotRecallBatchIntervalMs { get; set; }
        public int BotRecallBatchSize { get; set; }
        public int BotAggressionPercent { get; set; }
        public int BotActivityPercent { get; set; }
        public int BotGroupTendencyPercent { get; set; }
        public int BotChatFrequencyPercent { get; set; }
        public long BotInitialGoldFloor { get; set; }
        public long BotGoldFarmThreshold { get; set; }
        public int BotMinHealthPotionCount { get; set; }
        public int BotMinManaPotionCount { get; set; }
        public int BotTickDispatchLimit { get; set; }
        public int BotMainLoopIntervalMs { get; set; }
        public int BotMaxOnline { get; set; }
        public int BotPotionMonitorIntervalMs { get; set; }
        public int BotFullHealthThresholdPercent { get; set; }
        public int BotAttackAttemptIntervalMs { get; set; }
        public int BotPickupAttemptIntervalMs { get; set; }
        public int BotPickupRadius { get; set; }
        public int BotMapPoolBonus { get; set; }
        public int BotMapSwitchScoreGapMax { get; set; }
        public int BotPeriodicGroupSeconds { get; set; }
        public int BotMainActionsPerFrame { get; set; }
        public int BotPotionActionsPerFrame { get; set; }
        public string BotLogDirectory { get; set; }

        public static BotManagementSettings FromConfig()
        {
            return new BotManagementSettings
            {
                EnableBotSystem = Config.EnableBotSystem,
                BotFilePath = Config.BotFilePath,
                BotCount = Config.BotCount,
                BotCreateGuild = Config.BotCreateGuild,
                BotAllowGroup = Config.BotAllowGroup,
                BotAttackPlayers = Config.BotAttackPlayers,
                AggressionPercent = Config.BotAggressionPercent,
                ActivityPercent = Config.BotActivityPercent,
                GroupTendencyPercent = Config.BotGroupTendencyPercent,
                ChatFrequencyPercent = Config.BotChatFrequencyPercent,
                PercentRecoveryEnabled = Config.BotPercentRecoveryEnabled,
                FixedRecoveryEnabled = Config.BotFixedRecoveryEnabled,
                PercentRecoveryPerSecond = Config.BotPercentRecoveryPerSecond,
                FixedRecoveryPerSecond = Config.BotFixedRecoveryPerSecond,
                ProactivePvpMinLevel = Config.BotProactivePvpMinLevel,
                AutoRebirthLevel = Config.BotAutoRebirthLevel,
                AutoRebirthMaxCount = Config.BotAutoRebirthMaxCount,
                MainActionsPerFrame = Config.BotMainActionsPerFrame,
                PotionActionsPerFrame = Config.BotPotionActionsPerFrame,
                BotEnableChat = Config.BotEnableChat,
                BotAutoLevel = Config.BotAutoLevel,
                BotAutoPickup = Config.BotAutoPickup,
                BotAutoSellTrash = Config.BotAutoSellTrash,
                BotAutoPotionSupply = Config.BotAutoPotionSupply,
                BotAutoEquip = Config.BotAutoEquip,
                BotAutoLearnSkill = Config.BotAutoLearnSkill,
                BotAutoGroup = Config.BotAutoGroup,
                BotAutoTrade = Config.BotAutoTrade,
                BotGuildSystem = Config.BotGuildSystem,
                BotParticipateConquest = Config.BotParticipateConquest,
                BotPvpRetaliation = Config.BotPvpRetaliation,
                BotAutoMapSwitch = Config.BotAutoMapSwitch,
                BotSkipPickupWhenGroupedWithHuman = Config.BotSkipPickupWhenGroupedWithHuman,
                BotAutoRebirth = Config.BotAutoRebirth,
                BotPercentRecoveryEnabled = Config.BotPercentRecoveryEnabled,
                BotFixedRecoveryEnabled = Config.BotFixedRecoveryEnabled,
                BotAutoSpecialRepair = Config.BotAutoSpecialRepair,
                BotProactivePvpMinLevel = Config.BotProactivePvpMinLevel,
                BotAutoRebirthLevel = Config.BotAutoRebirthLevel,
                BotAutoRebirthMaxCount = Config.BotAutoRebirthMaxCount,
                BotDefenseLevelInterval = Config.BotDefenseLevelInterval,
                BotDefenseBonusPerTier = Config.BotDefenseBonusPerTier,
                BotStrongElementStartLevel = Config.BotStrongElementStartLevel,
                BotStrongElementLevelInterval = Config.BotStrongElementLevelInterval,
                BotStrongElementTypeCount = Config.BotStrongElementTypeCount,
                BotPercentRecoveryPerSecond = Config.BotPercentRecoveryPerSecond,
                BotFixedRecoveryPerSecond = Config.BotFixedRecoveryPerSecond,
                BotGlobalChatIntervalSeconds = Config.BotGlobalChatIntervalSeconds,
                BotSpecialRepairThresholdPercent = Config.BotSpecialRepairThresholdPercent,
                BotRecallBatchIntervalMs = Config.BotRecallBatchIntervalMs,
                BotRecallBatchSize = Config.BotRecallBatchSize,
                BotAggressionPercent = Config.BotAggressionPercent,
                BotActivityPercent = Config.BotActivityPercent,
                BotGroupTendencyPercent = Config.BotGroupTendencyPercent,
                BotChatFrequencyPercent = Config.BotChatFrequencyPercent,
                BotInitialGoldFloor = Config.BotInitialGoldFloor,
                BotGoldFarmThreshold = Config.BotGoldFarmThreshold,
                BotMinHealthPotionCount = Config.BotMinHealthPotionCount,
                BotMinManaPotionCount = Config.BotMinManaPotionCount,
                BotTickDispatchLimit = Config.BotTickDispatchLimit,
                BotMainLoopIntervalMs = Config.BotMainLoopIntervalMs,
                BotMaxOnline = Config.BotMaxOnline,
                BotPotionMonitorIntervalMs = Config.BotPotionMonitorIntervalMs,
                BotFullHealthThresholdPercent = Config.BotFullHealthThresholdPercent,
                BotAttackAttemptIntervalMs = Config.BotAttackAttemptIntervalMs,
                BotPickupAttemptIntervalMs = Config.BotPickupAttemptIntervalMs,
                BotPickupRadius = Config.BotPickupRadius,
                BotMapPoolBonus = Config.BotMapPoolBonus,
                BotMapSwitchScoreGapMax = Config.BotMapSwitchScoreGapMax,
                BotPeriodicGroupSeconds = Config.BotPeriodicGroupSeconds,
                BotMainActionsPerFrame = Config.BotMainActionsPerFrame,
                BotPotionActionsPerFrame = Config.BotPotionActionsPerFrame,
                BotLogDirectory = Config.BotLogDirectory,
            };
        }

        public bool TryValidate(out string error)
        {
            error = null;
            if (PercentRecoveryEnabled && FixedRecoveryEnabled)
                error = "按比例恢复和按数值恢复不能同时启用";
            else if (BotCount < 0 || BotCount > 10000)
                error = "假人数量必须在 0 到 10000 之间";
            else if (!IsPercent(AggressionPercent) || !IsPercent(ActivityPercent)
                     || !IsPercent(GroupTendencyPercent) || !IsPercent(ChatFrequencyPercent)
                     || !IsPercent(BotAggressionPercent) || !IsPercent(BotActivityPercent)
                     || !IsPercent(BotGroupTendencyPercent) || !IsPercent(BotChatFrequencyPercent)
                     || !IsPercent(BotSpecialRepairThresholdPercent)
                     || !IsPercent(BotFullHealthThresholdPercent))
                error = "百分比配置必须在 0 到 100 之间";
            else if (!IsNonNegative(PercentRecoveryPerSecond, 10000)
                     || !IsNonNegative(FixedRecoveryPerSecond, 10000)
                     || !IsNonNegative(BotPercentRecoveryPerSecond, 10000)
                     || !IsNonNegative(BotFixedRecoveryPerSecond, 10000))
                error = "恢复数值必须在 0 到 10000 之间";
            else if (!IsInterval(BotRecallBatchIntervalMs)
                     || !IsInterval(BotMainLoopIntervalMs)
                     || !IsInterval(BotPotionMonitorIntervalMs)
                     || !IsInterval(BotAttackAttemptIntervalMs)
                     || !IsInterval(BotPickupAttemptIntervalMs))
                error = "毫秒间隔必须在 1 到 60000 之间";
            else if (!IsSeconds(BotGlobalChatIntervalSeconds) || !IsSeconds(BotPeriodicGroupSeconds))
                error = "秒数配置必须在 0 到 60000 之间";
            else if (!IsNonNegative(BotRecallBatchSize, 10000)
                     || !IsNonNegative(BotMinHealthPotionCount, 10000)
                     || !IsNonNegative(BotMinManaPotionCount, 10000)
                     || !IsNonNegative(BotTickDispatchLimit, 10000)
                     || !IsNonNegative(BotMaxOnline, 10000)
                     || !IsNonNegative(BotMapPoolBonus, 10000))
                error = "数量配置必须在 0 到 10000 之间";
            else if (BotMainActionsPerFrame < 1 || BotMainActionsPerFrame > 10000
                     || MainActionsPerFrame < 1 || MainActionsPerFrame > 10000
                     || BotPotionActionsPerFrame < 1 || BotPotionActionsPerFrame > 10000
                     || PotionActionsPerFrame < 1 || PotionActionsPerFrame > 10000)
                error = "每帧动作预算必须在 1 到 10000 之间";
            else if (BotPickupRadius < 0 || BotPickupRadius > 20)
                error = "拾取半径必须在 0 到 20 格之间";
            else if (BotAutoRebirthMaxCount < 0 || BotAutoRebirthMaxCount > 255
                     || AutoRebirthMaxCount < 0 || AutoRebirthMaxCount > 255)
                error = "转生次数必须在 0 到 255 之间";
            else if ((BotAutoRebirthMaxCount > 0 && BotAutoRebirthLevel == 0)
                     || (AutoRebirthMaxCount > 0 && AutoRebirthLevel == 0))
                error = "设置转生次数上限时必须设置自动转生等级";
            else if (BotDefenseLevelInterval < 0 || BotDefenseLevelInterval > 10000
                     || BotStrongElementStartLevel < 0 || BotStrongElementStartLevel > int.MaxValue
                     || BotStrongElementLevelInterval < 0 || BotStrongElementLevelInterval > 10000
                     || BotStrongElementTypeCount < 0 || BotStrongElementTypeCount > 7
                     || BotDefenseBonusPerTier < 0 || BotDefenseBonusPerTier > 10000
                     || BotProactivePvpMinLevel < 0 || BotAutoRebirthLevel < 0
                     || ProactivePvpMinLevel < 0 || AutoRebirthLevel < 0)
                error = "等级、奖励和元素配置超出合法范围";
            else if (BotMapSwitchScoreGapMax < 0 || BotMapSwitchScoreGapMax > int.MaxValue / 4)
                error = "切图分差上限超出合法范围";
            else if (BotInitialGoldFloor < 0 || BotGoldFarmThreshold < 0
                     || BotInitialGoldFloor > long.MaxValue / 2 || BotGoldFarmThreshold > long.MaxValue / 2)
                error = "金币配置超出合法范围";
            else if (EnableBotSystem && string.IsNullOrWhiteSpace(BotFilePath))
                error = "启用假人系统时必须填写假人配置文件";

            return error == null;
        }

        public void WriteToConfig()
        {
            Config.EnableBotSystem = EnableBotSystem;
            Config.BotFilePath = BotFilePath ?? string.Empty;
            Config.BotCount = BotCount;
            Config.BotCreateGuild = BotCreateGuild;
            Config.BotAllowGroup = BotAllowGroup;
            Config.BotAttackPlayers = BotAttackPlayers;
            Config.BotEnableChat = BotEnableChat;
            Config.BotAutoLevel = BotAutoLevel;
            Config.BotAutoPickup = BotAutoPickup;
            Config.BotAutoSellTrash = BotAutoSellTrash;
            Config.BotAutoPotionSupply = BotAutoPotionSupply;
            Config.BotAutoEquip = BotAutoEquip;
            Config.BotAutoLearnSkill = BotAutoLearnSkill;
            Config.BotAutoGroup = BotAutoGroup;
            Config.BotAutoTrade = BotAutoTrade;
            Config.BotGuildSystem = BotGuildSystem;
            Config.BotParticipateConquest = BotParticipateConquest;
            Config.BotPvpRetaliation = BotPvpRetaliation;
            Config.BotAutoMapSwitch = BotAutoMapSwitch;
            Config.BotSkipPickupWhenGroupedWithHuman = BotSkipPickupWhenGroupedWithHuman;
            Config.BotAutoRebirth = BotAutoRebirth;
            Config.BotPercentRecoveryEnabled = PercentRecoveryEnabled;
            Config.BotFixedRecoveryEnabled = FixedRecoveryEnabled;
            Config.BotAutoSpecialRepair = BotAutoSpecialRepair;
            Config.BotProactivePvpMinLevel = ProactivePvpMinLevel;
            Config.BotAutoRebirthLevel = AutoRebirthLevel;
            Config.BotAutoRebirthMaxCount = AutoRebirthMaxCount;
            Config.BotDefenseLevelInterval = BotDefenseLevelInterval;
            Config.BotDefenseBonusPerTier = BotDefenseBonusPerTier;
            Config.BotStrongElementStartLevel = BotStrongElementStartLevel;
            Config.BotStrongElementLevelInterval = BotStrongElementLevelInterval;
            Config.BotStrongElementTypeCount = BotStrongElementTypeCount;
            Config.BotPercentRecoveryPerSecond = PercentRecoveryPerSecond;
            Config.BotFixedRecoveryPerSecond = FixedRecoveryPerSecond;
            Config.BotGlobalChatIntervalSeconds = BotGlobalChatIntervalSeconds;
            Config.BotSpecialRepairThresholdPercent = BotSpecialRepairThresholdPercent;
            Config.BotRecallBatchIntervalMs = BotRecallBatchIntervalMs;
            Config.BotRecallBatchSize = BotRecallBatchSize;
            Config.BotAggressionPercent = AggressionPercent;
            Config.BotActivityPercent = ActivityPercent;
            Config.BotGroupTendencyPercent = GroupTendencyPercent;
            Config.BotChatFrequencyPercent = ChatFrequencyPercent;
            Config.BotInitialGoldFloor = BotInitialGoldFloor;
            Config.BotGoldFarmThreshold = BotGoldFarmThreshold;
            Config.BotMinHealthPotionCount = BotMinHealthPotionCount;
            Config.BotMinManaPotionCount = BotMinManaPotionCount;
            Config.BotTickDispatchLimit = BotTickDispatchLimit;
            Config.BotMainLoopIntervalMs = BotMainLoopIntervalMs;
            Config.BotMaxOnline = BotMaxOnline;
            Config.BotPotionMonitorIntervalMs = BotPotionMonitorIntervalMs;
            Config.BotFullHealthThresholdPercent = BotFullHealthThresholdPercent;
            Config.BotAttackAttemptIntervalMs = BotAttackAttemptIntervalMs;
            Config.BotPickupAttemptIntervalMs = BotPickupAttemptIntervalMs;
            Config.BotPickupRadius = BotPickupRadius;
            Config.BotMapPoolBonus = BotMapPoolBonus;
            Config.BotMapSwitchScoreGapMax = BotMapSwitchScoreGapMax;
            Config.BotPeriodicGroupSeconds = BotPeriodicGroupSeconds;
            Config.BotMainActionsPerFrame = MainActionsPerFrame;
            Config.BotPotionActionsPerFrame = PotionActionsPerFrame;
            Config.BotLogDirectory = BotLogDirectory ?? string.Empty;
        }

        private static bool IsPercent(int value)
        {
            return value >= 0 && value <= 100;
        }

        private static bool IsInterval(int value)
        {
            return value >= 1 && value <= 60000;
        }

        private static bool IsSeconds(int value)
        {
            return value >= 0 && value <= 60000;
        }

        private static bool IsNonNegative(int value, int max)
        {
            return value >= 0 && value <= max;
        }
    }
}
