using Library;
using Server.Models;
using System;
using System.Collections.Generic;
using System.Drawing;

namespace Server.Envir
{
    /// <summary>
    /// 假人每实例状态对象。
    /// 将原先散落在 BotManager 各 partial 文件中 55 个 Dictionary&lt;uint,T&gt; 按功能域整合，
    /// 每个在线假人持有一个 BotState 实例，通过 BotManager._botStates[ObjectID] 访问。
    ///
    /// 设计原则：
    ///   - 仅存放"每假人独立"的状态，全局唯一的配置/常量保留在 BotManager 中。
    ///   - 各功能模块通过 BotManager.GetBotState(player.ObjectID) 获取状态。
    ///   - Stop/RemoveBotConnection 只需从 _botStates 删除对应 ObjectID，一次性清理所有状态。
    ///   - 现有旧字典保留不删，通过 BotStateExtensions 提供兼容桥接，逐步迁移。
    /// </summary>
    internal sealed class BotState
    {
        // ══════════════════════════════════════════════════════════════════════
        //  战斗域 (Combat)
        // ══════════════════════════════════════════════════════════════════════

        /// <summary>当前锁定目标（怪物 / 真人 / 宠物主人）</summary>
        public MapObject Target = null;

        /// <summary>最近被攻击者 ObjectID 列表</summary>
        public List<uint> LastAttackers = new List<uint>();

        /// <summary>最后被攻击时间</summary>
        public DateTime LastAttackedTime = DateTime.MinValue;

        /// <summary>下次允许换怪的时间（切怪超时保护）</summary>
        public DateTime TargetSwitchTime = DateTime.MinValue;

        /// <summary>目标血量历史（用于判断血量是否快速下降）</summary>
        public List<int> TargetHealthHistory = new List<int>();

        /// <summary>上次记录目标血量的时间</summary>
        public DateTime TargetHealthSampleTime = DateTime.MinValue;

        /// <summary>当前漫游方向</summary>
        public MirDirection RoamDir = MirDirection.Up;

        /// <summary>下次允许换漫游方向的时间</summary>
        public DateTime RoamTime = DateTime.MinValue;

        /// <summary>当前锁定的地面物品（跨 Tick 拾取状态）</summary>
        public ItemObject TargetItem = null;

        /// <summary>是否处于 PVP 风筝模式</summary>
        public bool KiteMode = false;

        /// <summary>进入等待拾取状态的时间（超时兜底）</summary>
        public DateTime WaitingPickupSince = DateTime.MinValue;

        // ──── 卡死检测 ────

        /// <summary>最后一次成功攻击时间（检测是否长时间未打到怪）</summary>
        public DateTime LastAttackTime = DateTime.MinValue;

        /// <summary>坐标快照位置（检测循环移动）</summary>
        public Point LastSnapPos = new Point();

        /// <summary>坐标快照时刻</summary>
        public DateTime LastSnapTime = DateTime.MinValue;

        /// <summary>漂移锚点位置（2分钟内判断是否离开5格范围）</summary>
        public Point DriftAnchorPos = new Point();

        /// <summary>漂移锚点记录时刻</summary>
        public DateTime DriftAnchorTime = DateTime.MinValue;

        // ──── 地图评估 / 驻留统计 ────

        /// <summary>下次允许重新评估地图的时间</summary>
        public DateTime MapEvalTime = DateTime.MinValue;

        /// <summary>当前驻留地图索引（驻图统计）</summary>
        public int MapStayMapIndex = -1;

        /// <summary>进入当前统计地图的时间</summary>
        public DateTime MapStayStartTime = DateTime.MinValue;

        /// <summary>回城冻结结束时间（回城后延时打怪）</summary>
        public DateTime RecallUntil = DateTime.MinValue;

        // ══════════════════════════════════════════════════════════════════════
        //  经济域 (Economy) — 出售 / 补货 / 药水
        // ══════════════════════════════════════════════════════════════════════

        /// <summary>下次允许常规出售的时间</summary>
        public DateTime SellTime = DateTime.MinValue;

        /// <summary>下次允许检查并补购药水的时间</summary>
        public DateTime RestockTime = DateTime.MinValue;

        /// <summary>下次允许主动喝药的时间（药水监控冷却）</summary>
        public DateTime PotionCooldownTime = DateTime.MinValue;

        /// <summary>下次允许因缺药而即时补货的时间（紧急补货节奏）</summary>
        public DateTime UrgentPotionBuyTime = DateTime.MinValue;

        // ══════════════════════════════════════════════════════════════════════
        //  装备域 (Equipment)
        // ══════════════════════════════════════════════════════════════════════

        /// <summary>下次允许自动穿装检查的时间</summary>
        public DateTime LastAutoEquipCheckTime = DateTime.MinValue;

        /// <summary>下次允许装备升级检查的时间</summary>
        public DateTime LastEquipmentUpgradeCheckTime = DateTime.MinValue;

        /// <summary>下次允许装备特修检查的时间</summary>
        public DateTime LastEquipmentRepairCheckTime = DateTime.MinValue;

        // ══════════════════════════════════════════════════════════════════════
        //  交易域 (Trade)
        // ══════════════════════════════════════════════════════════════════════

        /// <summary>下次允许 bot 间互相交易检查的时间</summary>
        public DateTime LastTradeWithBotCheckTime = DateTime.MinValue;

        /// <summary>下次允许主动向真人交易的时间</summary>
        public DateTime LastTradeWithHumanCheckTime = DateTime.MinValue;

        /// <summary>交易冷却结束时间</summary>
        public DateTime TradeCooldownUntil = DateTime.MinValue;

        /// <summary>上一帧的交易伙伴（跨帧检测交易完成）</summary>
        public PlayerObject LastTradePartner = null;

        // ══════════════════════════════════════════════════════════════════════
        //  社交域 (Social / Chat)
        // ══════════════════════════════════════════════════════════════════════

        /// <summary>下次允许触发社交的时间</summary>
        public DateTime NextSocialTime = DateTime.MinValue;

        /// <summary>待发送的聊天回复（延迟回复队列）</summary>
        public BotPendingChatReplyState PendingChatReply = null;

        /// <summary>最近与特定玩家聊过的话题（目标ObjectID → 话题key）</summary>
        public Dictionary<uint, string> LastChatTopicWith = new Dictionary<uint, string>();

        /// <summary>最近聊天目标 ObjectID</summary>
        public uint LastChatTargetId = 0;

        // ══════════════════════════════════════════════════════════════════════
        //  攻城域 (Siege)
        // ══════════════════════════════════════════════════════════════════════

        /// <summary>已分配的攻城策略（每场攻城只分配一次，null表示未分配）</summary>
        public BotSiegeStrategyValue? SiegeStrategy = null;

        // ══════════════════════════════════════════════════════════════════════
        //  遥测 / 行为档案域 (Telemetry / Profile)
        // ══════════════════════════════════════════════════════════════════════

        /// <summary>遥测窗口（运行时统计）</summary>
        public BotTelemetryWindowState Telemetry = new BotTelemetryWindowState();

        /// <summary>行为档案（随机个性参数）</summary>
        public BotBehaviorProfileState Profile = new BotBehaviorProfileState();

        // ══════════════════════════════════════════════════════════════════════
        //  登录 / 组队域 (Login / Group)
        // ══════════════════════════════════════════════════════════════════════

        /// <summary>登录热身结束时间（避免刚上线立刻触发复杂行为）</summary>
        public DateTime LoginWarmupUntil = DateTime.MinValue;

        /// <summary>上次申请攻城的时间</summary>
        public DateTime ConquestApplyTime = DateTime.MinValue;

        /// <summary>强制组队锁结束时间（切图后组队保护期）</summary>
        public DateTime ForcedGroupLockUntil = DateTime.MinValue;

        /// <summary>技能学习冷却（避免每 Tick 重复触发学技能）</summary>
        public DateTime SkillLearnTime = DateTime.MinValue;

        /// <summary>高阶 BOSS 图扩编冷却</summary>
        public DateTime HighBossGroupPrepareTime = DateTime.MinValue;

        /// <summary>最近判定可能切去的高阶 BOSS 地图</summary>
        public Map UpcomingHighBossGroupTarget = null;

        /// <summary>真人邀请冷却（保证真人有足够时间邀请假人入队）</summary>
        public DateTime HumanInviteCooldown = DateTime.MinValue;

        // ══════════════════════════════════════════════════════════════════════
        //  职业专属域 — 道士 (Taoist)
        // ══════════════════════════════════════════════════════════════════════

        /// <summary>购买符/毒的冷却时间</summary>
        public DateTime TaoistBuyTime = DateTime.MinValue;

        /// <summary>召唤宝宝的冷却时间</summary>
        public DateTime TaoistSummonTime = DateTime.MinValue;

        /// <summary>道士施毒次数（每 20 次切换药粉颜色）</summary>
        public int TaoistPoisonUseCount = 0;

        /// <summary>上次施毒记录（目标ID, 施毒时间, 毒药Shape）</summary>
        public (uint targetId, DateTime time, int poisonShape) TaoistLastPoisonCast = (0, DateTime.MinValue, 0);

        /// <summary>道士防御BUFF冷却</summary>
        public DateTime TaoistBuffTime = DateTime.MinValue;

        // ══════════════════════════════════════════════════════════════════════
        //  职业专属域 — 法师 (Wizard)
        // ══════════════════════════════════════════════════════════════════════

        /// <summary>法师防御技能冷却</summary>
        public DateTime WizardBuffTime = DateTime.MinValue;

        // ══════════════════════════════════════════════════════════════════════
        //  职业专属域 — 刺客 (Assassin)
        // ══════════════════════════════════════════════════════════════════════

        /// <summary>刺客支援技能冷却（召唤木偶/Buff）</summary>
        public DateTime AssassinSupportTime = DateTime.MinValue;

        /// <summary>刺客防御BUFF冷却</summary>
        public DateTime AssassinBuffTime = DateTime.MinValue;
    }

    // ══════════════════════════════════════════════════════════════════════
    //  BotState 内嵌辅助类型
    // ══════════════════════════════════════════════════════════════════════

    /// <summary>待发送聊天回复状态（原 BotPendingChatReply 的独立版本）</summary>
    internal sealed class BotPendingChatReplyState
    {
        public uint ReplyToObjectID = 0;
        public string Text = null;
        public DateTime ReplyTime = DateTime.MinValue;
        public DateTime ExpireTime = DateTime.MinValue;
        public string SpeakerName = null;
    }

    /// <summary>攻城策略枚举值（对应 BotManager 内部 BotSiegeStrategy，可空包装用于 BotState）</summary>
    internal enum BotSiegeStrategyValue
    {
        FrontalAssault,
        FlankingAssault,
        DefensiveCounterAttack,
        SplitAssault
    }

    /// <summary>单张地图运行指标（原 BotManager.BotMapRuntimeMetrics 的独立版本）</summary>
    internal sealed class BotMapRuntimeMetricsState
    {
        public double ActiveSeconds = 0;
        public int Visits = 0;
        public int Kills = 0;
        public int Pickups = 0;
        public int BlockedMoves = 0;
        public int MagicSuccessCount = 0;
        public int MagicFailCount = 0;
        public int BossMechanicEvents = 0;
        public DateTime LastVisitTime = DateTime.MinValue;
    }

    /// <summary>遥测统计窗口（原 BotManager.BotTelemetryWindow 的独立版本）</summary>
    internal sealed class BotTelemetryWindowState
    {
        public DateTime WindowStart = DateTime.MinValue;
        public int Kills = 0;
        public int PotionsUsed = 0;
        public int MagicSuccessCount = 0;
        public int MagicFailCount = 0;
        public int BlockedMoves = 0;
        public int MapSwitches = 0;
        public int Pickups = 0;
        public int BossRetreats = 0;
        public int BossAddSwitches = 0;
        public int SocialMessages = 0;
        public int GroupResets = 0;
        public int CurrentMapIndex = -1;
        public DateTime CurrentMapEnterTime = DateTime.MinValue;
        public Dictionary<int, BotMapRuntimeMetricsState> MapMetrics = new Dictionary<int, BotMapRuntimeMetricsState>();
    }

    /// <summary>行为档案（原 BotManager.BotBehaviorProfile 的独立版本）</summary>
    internal sealed class BotBehaviorProfileState
    {
        public int AggressionBias = 0;
        public int CautionBias = 0;
        public int FollowSlack = 0;
        public int RoamRandomnessPct = 0;
        public int SocialDelayBiasMs = 0;
    }
}
