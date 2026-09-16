using Library;
using Library.Network;
using Library.SystemModels;
using MirDB;
using Server.DBModels;
using Server.Models;
using Server.Scripts.Npc;
using System;
using System.Collections.Generic;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using C = Library.Network.ClientPackets;
using S = Library.Network.ServerPackets;

namespace Server.Envir
{
    /// <summary>
    /// 假人管理系统
    /// </summary>
    public static partial class BotManager
    {
        private static List<BotAccountInfo> botAccounts = new List<BotAccountInfo>();

        // ──────────────────────────────────────────────────────────────────────
        // 线程安全改造：botPlayers 改用 ReaderWriterLockSlim 保护，
        // 所有 ToList() 快照由 SnapshotBotPlayers() 统一替代。
        // 读操作（Tick）持读锁；写操作（Add/Remove）持写锁。
        // ──────────────────────────────────────────────────────────────────────
        private static List<PlayerObject> botPlayers = new List<PlayerObject>();
        private static readonly System.Threading.ReaderWriterLockSlim _botPlayersLock
            = new System.Threading.ReaderWriterLockSlim();

        // ──────────────────────────────────────────────────────────────────────
        // 中央状态字典：每个在线假人持有一个 BotState 实例。
        // 替代原先散落各处的 40+ 个 Dictionary<uint,T>，实现内聚封装。
        // 旧字典保留不删，逐步迁移；新代码通过 GetBotState() 访问状态。
        // ──────────────────────────────────────────────────────────────────────
        private static readonly System.Collections.Concurrent.ConcurrentDictionary<uint, BotState> _botStates
            = new System.Collections.Concurrent.ConcurrentDictionary<uint, BotState>();

        /// <summary>
        /// 获取假人的状态对象。若不存在则自动创建（首次访问时懒初始化）。
        /// </summary>
        internal static BotState GetBotState(uint objectId)
        {
            return _botStates.GetOrAdd(objectId, _ => new BotState());
        }

        /// <summary>
        /// 获取假人的状态对象（PlayerObject 重载）。
        /// </summary>
        internal static BotState GetBotState(PlayerObject player)
        {
            return player == null ? null : GetBotState(player.ObjectID);
        }

        /// <summary>
        /// 线程安全地获取 botPlayers 的只读快照，替代所有 botPlayers.ToList() 调用。
        /// 持读锁期间执行 ToArray()，快照后立即释放锁，后续遍历不再持锁。
        /// </summary>
        private static PlayerObject[] SnapshotBotPlayers()
        {
            _botPlayersLock.EnterReadLock();
            try
            {
                return botPlayers.ToArray();
            }
            finally
            {
                _botPlayersLock.ExitReadLock();
            }
        }

        /// <summary>
        /// 线程安全地向 botPlayers 添加假人。
        /// </summary>
        private static void AddBotPlayer(PlayerObject player)
        {
            if (player == null) return;
            _botPlayersLock.EnterWriteLock();
            try { botPlayers.Add(player); }
            finally { _botPlayersLock.ExitWriteLock(); }
        }

        /// <summary>
        /// 线程安全地从 botPlayers 移除假人。
        /// </summary>
        private static void RemoveBotPlayer(PlayerObject player)
        {
            if (player == null) return;
            _botPlayersLock.EnterWriteLock();
            try { botPlayers.Remove(player); }
            finally { _botPlayersLock.ExitWriteLock(); }
        }

        private static Timer botTimer;
        private static Timer botPotionTimer;
        private static bool isRunning = false;
        private static string botFilePath = "";
        private static string botGuildNameFilePath = "";
        private static int botCount = 0;

        // ──────────────────────────────────────────────────────────────────────
        // ItemType → EquipmentSlot 映射表（只映射可穿戴装备类型）
        // 注：Ring / Bracelet 为双槽，不在此表中，由 ProcessBotAutoEquip 单独处理
        // ──────────────────────────────────────────────────────────────────────
        private static readonly Dictionary<ItemType, EquipmentSlot> ItemTypeToSlot
            = new Dictionary<ItemType, EquipmentSlot>
        {
            { ItemType.Weapon,     EquipmentSlot.Weapon     },
            { ItemType.Armour,     EquipmentSlot.Armour     },
            { ItemType.Helmet,     EquipmentSlot.Helmet     },
            { ItemType.Torch,      EquipmentSlot.Torch      },
            { ItemType.Necklace,   EquipmentSlot.Necklace   },
            { ItemType.Shoes,      EquipmentSlot.Shoes      },
            { ItemType.Amulet,     EquipmentSlot.Amulet     },
            { ItemType.HorseArmour,EquipmentSlot.HorseArmour},
            { ItemType.Flower,     EquipmentSlot.Flower     },
        };

        // MirClass → RequiredClass 的位掩码，用于职业匹配校验
        private static readonly Dictionary<MirClass, RequiredClass> ClassToRequired
            = new Dictionary<MirClass, RequiredClass>
        {
            { MirClass.Warrior,  RequiredClass.Warrior  },
            { MirClass.Wizard,   RequiredClass.Wizard   },
            { MirClass.Taoist,   RequiredClass.Taoist   },
            { MirClass.Assassin, RequiredClass.Assassin },
        };

        // MirGender → RequiredGender 的位掩码，用于性别匹配校验
        private static readonly Dictionary<MirGender, RequiredGender> GenderToRequired
            = new Dictionary<MirGender, RequiredGender>
        {
            { MirGender.Male,   RequiredGender.Male   },
            { MirGender.Female, RequiredGender.Female },
        };

        private sealed class BotSkillBookRecipe
        {
            public int PageCount;
            public int ComposeGold;
            public int AppraiseGold;
        }

        private sealed class BotMapRuntimeMetrics
        {
            public double ActiveSeconds;
            public int Visits;
            public int Kills;
            public int Pickups;
            public int BlockedMoves;
            public int MagicSuccessCount;
            public int MagicFailCount;
            public int BossMechanicEvents;
            public DateTime LastVisitTime;
        }

        private sealed class BotTelemetryWindow
        {
            public DateTime WindowStart = DateTime.MinValue;
            public int Kills;
            public int PotionsUsed;
            public int MagicSuccessCount;
            public int MagicFailCount;
            public int BlockedMoves;
            public int MapSwitches;
            public int Pickups;
            public int BossRetreats;
            public int BossAddSwitches;
            public int SocialMessages;
            public int GroupResets;
            public int CurrentMapIndex = -1;
            public DateTime CurrentMapEnterTime = DateTime.MinValue;
            public Dictionary<int, BotMapRuntimeMetrics> MapMetrics = new Dictionary<int, BotMapRuntimeMetrics>();
        }

        private sealed class BotBehaviorProfile
        {
            public int AggressionBias;
            public int CautionBias;
            public int FollowSlack;
            public int RoamRandomnessPct;
            public int SocialDelayBiasMs;
        }

        private enum BotProgressionStage
        {

            SafeNursery = 0,
            TownOutskirts = 1,
            MixedLevelAndBooks = 2,
            LevelRush = 3,
            HighBookFarm = 4,
            LateLevelRush = 5,
        }

        private static readonly string[] BotSafeNurseryMonsterKeywords =
        {
            "鸡", "羊", "猪", "牛",
        };

        private static readonly string[] BotTownOutskirtsMonsterKeywords =
        {
            "稻草人", "钉耙猫", "半兽人", "多钩猫", "森林雪人", "蛤蟆",
        };

        // ══════════════════════════════════════════════════════════════════════
        //  高级技能书地图白名单（打书模式下可进入的 BOSS 图）
        // ══════════════════════════════════════════════════════════════════════
        /// <summary>
        /// 高级技能书掉落地图白名单（文件名关键词匹配）。
        /// 这些地图可能包含 BOSS，但会掉落高级技能书，假人在打书模式下可以进入。
        /// </summary>
        private static readonly string[] BotHighSkillBookMapKeywords =
        {
            "尸王", "僵尸", "Zuma", "祖玛", "ZumaKing", "祖玛教主", "Boss", "Worm", "尸魔",
            "石墓阵", "猪洞", "牛洞", "祖玛寺庙", "将军墓", "猪", "牛",
        };

        private static readonly ItemType[] BotEquipmentPurchasePriority =
        {
            ItemType.Weapon,
            ItemType.Armour,
            ItemType.Helmet,
            ItemType.Shoes,
            ItemType.Necklace,
            ItemType.Bracelet,
            ItemType.Ring,
        };

        // ══════════════════════════════════════════════════════════════════════
        //  装备升级决策配置
        // ══════════════════════════════════════════════════════════════════════
        /// <summary>装备显著提升的最小阈值（分数差值，绝对值）</summary>
        private const int BotEquipmentSignificantUpgradeThreshold = 20;

        /// <summary>装备升级最小百分比提升（1 = 100%）</summary>
        private const decimal BotEquipmentMinUpgradePercent = 0.15m;

        /// <summary>装备升级检查间隔（秒）</summary>
        private const int BotEquipmentUpgradeCheckInterval = 30;

        /// <summary>装备升级状态字典：记录每个假人上次检查时间</summary>
        private static readonly Dictionary<uint, DateTime> _botLastEquipmentUpgradeCheckTime
            = new Dictionary<uint, DateTime>();

        // ══════════════════════════════════════════════════════════════════════
        //  特修系统智能化配置
        // ══════════════════════════════════════════════════════════════════════
        /// <summary>装备特修检查间隔（秒）</summary>
        private const int BotEquipmentRepairCheckInterval = 10;

        /// <summary>特修触发耐久阈值（百分比，低于此值时触发特修）</summary>
        private const double BotEquipmentRepairDurabilityThreshold = 0.5;

        /// <summary>特修状态字典：记录每个假人上次特修检查时间</summary>
        private static readonly Dictionary<uint, DateTime> _botLastEquipmentRepairCheckTime
            = new Dictionary<uint, DateTime>();

        private const int BotEquipmentMaintenanceIntervalSeconds = 30;
        private const int BotConsumableMaintenanceIntervalSeconds = 20;
        private const int BotInventoryMaintenanceIntervalSeconds = 60;
        private const int BotClassSupportIntervalSeconds = 10;
        private const int BotHighBossMaintenanceIntervalSeconds = 180;

        private static readonly Dictionary<uint, DateTime> _botEquipmentMaintenanceTime
            = new Dictionary<uint, DateTime>();
        private static readonly Dictionary<uint, DateTime> _botConsumableMaintenanceTime
            = new Dictionary<uint, DateTime>();
        private static readonly Dictionary<uint, DateTime> _botInventoryMaintenanceTime
            = new Dictionary<uint, DateTime>();
        private static readonly Dictionary<uint, DateTime> _botClassSupportTime
            = new Dictionary<uint, DateTime>();
        private static readonly Dictionary<uint, DateTime> _botHighBossMaintenanceTime
            = new Dictionary<uint, DateTime>();

        private static bool ShouldRunBotMaintenance(Dictionary<uint, DateTime> schedule, uint objectId, int intervalSeconds)
        {
            DateTime now = SEnvir.Now;
            if (schedule.TryGetValue(objectId, out DateTime next) && now < next)
                return false;

            schedule[objectId] = now.AddSeconds(intervalSeconds);
            return true;
        }

        // ══════════════════════════════════════════════════════════════════════
        //  交易系统智能化配置
        // ══════════════════════════════════════════════════════════════════════
        /// <summary>bot之间互相交易检查间隔（秒）</summary>
        private const int BotTradeWithBotCheckInterval = 120;

        /// <summary>bot主动向真人交易极品装备检查间隔（秒）</summary>
        private const int BotTradeWithHumanCheckInterval = 180;

        /// <summary>极品装备评分阈值（超过此值视为极品）</summary>
        private const int BotPremiumEquipmentScoreThreshold = 80;

        /// <summary>bot之间交易的最大距离（格）</summary>
        private const int BotTradeWithBotMaxDistance = 6;

        /// <summary>bot向真人交易的最大距离（格）</summary>
        private const int BotTradeWithHumanMaxDistance = 12;

        /// <summary>bot交易冷却时间（秒）</summary>
        private const int BotTradeCooldownSeconds = 30;

        /// <summary>bot向真人交易的最大物品数量</summary>
        private const int BotTradeWithHumanMaxItems = 5;

        /// <summary>bot之间互相交易状态字典：记录每个假人上次交易检查时间</summary>
        private static readonly Dictionary<uint, DateTime> _botLastTradeWithBotCheckTime
            = new Dictionary<uint, DateTime>();

        // 上一帧交易伙伴（用于检测交易完成）
        private static readonly Dictionary<uint, PlayerObject> _botLastTradePartner
            = new Dictionary<uint, PlayerObject>();

        /// <summary>bot向真人交易状态字典：记录每个假人上次真人交易检查时间</summary>
        private static readonly Dictionary<uint, DateTime> _botLastTradeWithHumanCheckTime
            = new Dictionary<uint, DateTime>();

        /// <summary>bot交易冷却字典：记录每个假人上次交易时间</summary>
        private static readonly Dictionary<uint, DateTime> _botTradeCooldownUntil
            = new Dictionary<uint, DateTime>();

        private static readonly string[] BotDefaultGuildNamesChinese =
        {
            "苍狼",
            "赤霄",
            "玄武",
            "青龙",
            "白虎",
            "朱雀",
            "天命",
            "烈焰",
            "龙魂",
            "战神",
            "无双",
            "铁血",
            "逐鹿",
            "天涯",
            "沧海",
            "破晓",
        };


        private static readonly string[] BotDefaultGuildNamesEnglish =
        {
            "Atlas",
            "Blaze",
            "Drake",
            "Frost",
            "Vex",
            "Ares",
            "Nyx",
            "Orion",
        };

        private static readonly List<string> _botGuildNames = new List<string>();

        private static readonly Dictionary<uint, BotTelemetryWindow> _botTelemetry
            = new Dictionary<uint, BotTelemetryWindow>();

        private static readonly Dictionary<uint, BotBehaviorProfile> _botBehaviorProfiles
            = new Dictionary<uint, BotBehaviorProfile>();

        private static readonly Dictionary<uint, DateTime> _botLoginWarmupUntil
            = new Dictionary<uint, DateTime>();

        private static readonly Dictionary<uint, DateTime> _botConquestApplyTime
            = new Dictionary<uint, DateTime>();

        private static readonly Dictionary<uint, DateTime> _botForcedGroupLockUntil
            = new Dictionary<uint, DateTime>();

        private static bool _botGroupRebuildPending;

        private static DateTime _botNextGroupRebuildTime = DateTime.MinValue;
        private static DateTime _botAutoGroupRebuildLockUntil = DateTime.MinValue;

        private const int BotTelemetrySummaryWindowSeconds = 60;
        private const int BotTelemetryBlockedMoveWarnThreshold = 16;
        private const int BotTelemetryMagicFailWarnThreshold = 14;
        private const int BotTelemetryBossWarnThreshold = 4;
        private const int BotRuntimeMapMetricsMinSeconds = 45;

        private static readonly Dictionary<string, BotSkillBookRecipe> BotSkillBookRecipes
            = new Dictionary<string, BotSkillBookRecipe>
        {

            { "铁布衫",     new BotSkillBookRecipe { PageCount = 400, ComposeGold = 800000,  AppraiseGold = 12880000 } },
            { "十方斩",     new BotSkillBookRecipe { PageCount = 300, ComposeGold = 500000,  AppraiseGold = 9980000  } },
            { "破血狂杀",   new BotSkillBookRecipe { PageCount = 500, ComposeGold = 1000000, AppraiseGold = 16880000 } },
            { "乾坤大挪移", new BotSkillBookRecipe { PageCount = 300, ComposeGold = 500000,  AppraiseGold = 9980000  } },
            { "斗转星移",   new BotSkillBookRecipe { PageCount = 300, ComposeGold = 500000,  AppraiseGold = 9980000  } },
            { "魄冰刺",     new BotSkillBookRecipe { PageCount = 300, ComposeGold = 500000,  AppraiseGold = 9980000  } },
            { "怒神霹雳",   new BotSkillBookRecipe { PageCount = 400, ComposeGold = 800000,  AppraiseGold = 12880000 } },
            { "凝血离魂",   new BotSkillBookRecipe { PageCount = 500, ComposeGold = 1000000, AppraiseGold = 16880000 } },
            { "焰天火雨",   new BotSkillBookRecipe { PageCount = 400, ComposeGold = 800000,  AppraiseGold = 12880000 } },
            { "云寂术",     new BotSkillBookRecipe { PageCount = 300, ComposeGold = 500000,  AppraiseGold = 9980000  } },
            { "妙影无踪",   new BotSkillBookRecipe { PageCount = 500, ComposeGold = 1000000, AppraiseGold = 16880000 } },
            { "阴阳法环",   new BotSkillBookRecipe { PageCount = 500, ComposeGold = 1000000, AppraiseGold = 16880000 } },
            { "移花接玉",   new BotSkillBookRecipe { PageCount = 300, ComposeGold = 500000,  AppraiseGold = 9980000  } },
        };

        private const int BotSkillActionRetrySeconds = 1;
        private const int BotGoldFarmPreferredLevelGap = 3;
        private const int BotEmergencyGoldFarmPreferredLevelGap = 8;
        private const int BotEmergencyGoldFarmPickupRadius = 6;
        private const int BotLoginBatchSize = 3;
        private const int BotLoginWarmupSeconds = 5;
        private const int BotMainSliceCount = 4;
        private static int _botMainSliceCursor = -1;

        /// <summary>
        /// 自动组队重建防抖时间（秒）：延长到 10 秒，避免多个事件触发重复组队重建。
        /// </summary>
        private const int BotAutoGroupDebounceSeconds = 10;
        private const int BotForcedGroupLockSeconds = 90;
        private const int BotAutoGroupRebuildLockSeconds = 90;

        /// <summary>
        /// 初始化假人系统
        /// </summary>
        public static void Initialize()
        {
            PlayerObject.BotPvPDamaged -= OnBotPvPDamaged;
            PlayerObject.BotPvPDamaged += OnBotPvPDamaged;
            botTimer = new Timer(BotTick, null, Timeout.Infinite, Timeout.Infinite);
            botPotionTimer = new Timer(BotPotionTick, null, Timeout.Infinite, Timeout.Infinite);
            SEnvir.Log("假人管理系统已初始化");
        }

        /// <summary>
        /// 启动假人系统
        /// </summary>
        public static void Start(string filePath, int count)
        {
            if (isRunning)
            {
                SEnvir.Log("假人系统已在运行中");
                return;
            }

            if (string.IsNullOrEmpty(filePath) || !File.Exists(filePath))
            {
                SEnvir.Log($"假人文件不存在: {filePath}");
                return;
            }

            if (!SEnvir.Started
                || SEnvir.AccountInfoList?.Binding == null
                || SEnvir.CharacterInfoList?.Binding == null
                || SEnvir.BotAccountInfoList?.Binding == null)
            {
                SEnvir.Log("假人系统启动延后：服务器数据库尚未就绪");
                return;
            }

            botFilePath = filePath;
            botCount = Math.Max(0, count);
            ResetManagementCounters();
            _botRecoverySeconds.Clear();
            _botDeathRecorded.Clear();
            _botNextAttackAttemptTime.Clear();
            _botNextPickupAttemptTime.Clear();
            _botLoginWarmupUntil.Clear();
            _botForcedGroupLockUntil.Clear();
            _botGroupRebuildPending = false;
            _botNextGroupRebuildTime = DateTime.MinValue;
            _botAutoGroupRebuildLockUntil = DateTime.MinValue;
            _botNextPeriodicGroupTime = DateTime.MinValue;
            _botMainSliceCursor = -1;
            _pendingRecallAll = false;
            _pendingRecallResult = null;
            _botRecallBatchOffset = 0;
            _botNextRecallBatchTime = DateTime.MinValue;
            _recallActionQueued = false;

            //加载假人配置
            LoadBotAccounts();
            LoadBotChatConfig();
            LoadBotGuildNameConfig();
            if (botAccounts.Count == 0)
            {
                SEnvir.Log("假人配置为空或格式不匹配；当前支持两种格式：角色名,职业,性别 或 账号,密码,角色名,职业,性别");
            }

            // 加载跨会话持久化记忆（地图经验 + 社交关系）
            BotMemory.Load();
            BotSocialMemory.Load();

            // 主 AI 分四个稳定槽执行，每个假人仍约四个主循环周期驱动一次。
            botTimer.Change(0, Math.Max(1, Config.BotMainLoopIntervalMs));
            // 启动独立药水监控（只负责血蓝检查与喝药，不阻塞战斗逻辑）
            botPotionTimer.Change(0, Math.Max(1, Config.BotPotionMonitorIntervalMs));
            isRunning = true;

            SEnvir.Log($"假人系统已启动,加载文件: {filePath}, 目标数量: {count}");
        }

        /// <summary>
        /// 停止假人系统，将所有假人踢下线
        /// </summary>
        public static void Stop()
        {
            if (!isRunning) return;

            // 先停止定时器，防止后续 Tick 继续投递
            botTimer.Change(Timeout.Infinite, Timeout.Infinite);
            botPotionTimer.Change(Timeout.Infinite, Timeout.Infinite);
            isRunning = false;
            ResetRuntimeQuickTuning("停止假人");

            // 将踢下线操作投递到主线程执行（Stop 可能从 UI 线程调用）
            // ★ Disconnect() → CleanUp(Player.StopGame()) → OnBotDisconnected
            //   → RemoveBotConnection()：从 botPlayers / SEnvir.Players /
            //     SEnvir.Connections 移除，重置 BotState = Idle
            // 因此 lambda 里不需要手动 Remove，只做兜底 Clear 即可。
            var playersToKick = SnapshotBotPlayers();

            SEnvir.BotActionQueue.Enqueue(() =>
            {
                try
                {
                    foreach (var player in playersToKick)
                    {
                        if (player?.Connection == null) continue;
                        if (!player.Connection.Connected) continue; // 已断开，跳过

                        try
                        {
                            player.Connection.Disconnect();
                        }
                        catch (Exception ex)
                        {
                            // 单个假人踢下线失败（如 Despawn Node=null），不影响后续清理
                            SEnvir.Log($"踢假人下线异常 [{player.Name}]: {ex.Message}\n{ex.StackTrace}");
                        }
                    }
                }
                finally
                {
                    // ★ 无论 Disconnect 是否抛出，都必须执行兜底清理
                    // 避免残留 player 继续被 BotTick / BotPotionTick 驱动导致后续异常
                    _botPlayersLock.EnterWriteLock();
                    try { botPlayers.Clear(); }
                    finally { _botPlayersLock.ExitWriteLock(); }
                    _botStates.Clear();
                    botAccounts.Clear();
                    ClearBotQueuedMarkers();
                    _botMapStayMapIndex.Clear();
                    _botMapStayStartTime.Clear();
                    _botPotionCooldownTime.Clear();
                    _botUrgentPotionBuyTime.Clear();
                    _botAssassinSupportTime.Clear();
                    _botLastAutoEquipCheckTime.Clear();
                    _botNextSocialTime.Clear();
                    _botPendingChatReplies.Clear();
                    _botHighBossGroupPrepareTime.Clear();
                    _botUpcomingHighBossGroupTargets.Clear();
                    _botTelemetry.Clear();
                    _botBehaviorProfiles.Clear();
                    _botLoginWarmupUntil.Clear();
                    _botConquestApplyTime.Clear();
                    _botForcedGroupLockUntil.Clear();
                    _botLastEquipmentUpgradeCheckTime.Clear();
                    _botLastEquipmentRepairCheckTime.Clear();
                    _botEquipmentMaintenanceTime.Clear();
                    _botConsumableMaintenanceTime.Clear();
                    _botInventoryMaintenanceTime.Clear();
                    _botClassSupportTime.Clear();
                    _botHighBossMaintenanceTime.Clear();
                    _botLastTradeWithBotCheckTime.Clear();
                    _botLastTradeWithHumanCheckTime.Clear();
                    _botTradeCooldownUntil.Clear();
                    _botGroupRebuildPending = false;

                    _botNextGroupRebuildTime = DateTime.MinValue;
                    _botAutoGroupRebuildLockUntil = DateTime.MinValue;
                    _botNextPeriodicGroupTime = DateTime.MinValue;
                    _pendingRecallAll = false;
                    _pendingRecallResult = null;
                    _botRecallBatchOffset = 0;
                    _botNextRecallBatchTime = DateTime.MinValue;
                    _recallActionQueued = false;
                    _botTaoistLastPoisonCast.Clear();
                    _botTaoistPoisonUseCount.Clear();
                    _botDeathRecorded.Clear();
                    _botNextAttackAttemptTime.Clear();
                    _botNextPickupAttemptTime.Clear();
                    BotPvPStrategy.ClearAllPvPStates();
                    BotMemory.ClearAll();
                    BotSocialMemory.ClearAll();
                    SEnvir.Log("假人系统已停止，所有假人已踢下线");

                }
            });
        }

        /// <summary>
        /// 加载假人账号配置
        /// </summary>
        private static void LoadBotAccounts()
        {
            try
            {
                botAccounts.Clear();

                if (botCount <= 0)
                {
                    SEnvir.Log("假人目标数量小于等于 0，本次不加载任何假人账号");
                    return;
                }

                var lines = File.ReadAllLines(botFilePath, Encoding.UTF8);
                int loadedCount = 0;
                int skippedCount = 0;

                for (int lineIndex = 0; lineIndex < lines.Length; lineIndex++)
                {
                    if (loadedCount >= botCount)
                        break;

                    string rawLine = lines[lineIndex];
                    if (string.IsNullOrWhiteSpace(rawLine))
                        continue;

                    string line = rawLine.Trim();
                    if (line.StartsWith("#"))
                        continue;

                    try
                    {
                        string account;
                        string password;
                        string charName;
                        MirClass jobClass;
                        MirGender gender;

                        if (!TryParseBotConfigLine(line, out account, out password, out charName, out jobClass, out gender))
                        {
                            skippedCount++;
                            SEnvir.Log($"假人配置第 {lineIndex + 1} 行格式无效: {line}");
                            continue;
                        }

                        var existingChar = SEnvir.CharacterInfoList.Binding
                            .FirstOrDefault(x => x != null && !x.Deleted && x.CharacterName == charName);

                        var existingAccount = existingChar?.Account
                            ?? SEnvir.AccountInfoList.Binding.FirstOrDefault(x => x.EMailAddress == account);

                        if (existingAccount == null)
                        {
                            existingAccount = RegisterBotAccount(account, password);
                        }

                        if (existingAccount == null)
                        {
                            skippedCount++;
                            SEnvir.Log($"假人配置第 {lineIndex + 1} 行账号创建失败: {line}");
                            continue;
                        }

                        account = existingAccount.EMailAddress;
                        existingChar = existingAccount.Characters.FirstOrDefault(x => !x.Deleted && x.CharacterName == charName)
                            ?? existingChar;

                        if (existingChar == null)
                        {
                            existingChar = CreateBotCharacter(existingAccount, charName, jobClass, gender);
                        }

                        if (existingChar == null)
                        {
                            skippedCount++;
                            SEnvir.Log($"假人配置第 {lineIndex + 1} 行角色创建失败: {charName}");
                            continue;
                        }

                        if (botAccounts.Any(x => x.Account == existingAccount))
                        {
                            SEnvir.Log($"假人配置第 {lineIndex + 1} 行账号已加载，跳过重复项: {account}");
                            continue;
                        }

                        var botInfo = SEnvir.BotAccountInfoList.CreateNewObject();
                        botInfo.Account = existingAccount;
                        botInfo.BotId = account;
                        botInfo.CharacterCreated = true;
                        botInfo.BotState = DBModels.BotState.Idle;
                        botInfo.LastActionTime = Time.Now;

                        botAccounts.Add(botInfo);
                        loadedCount++;
                    }
                    catch (Exception ex)
                    {
                        skippedCount++;
                        SEnvir.Log($"加载假人配置第 {lineIndex + 1} 行失败: {ex.Message}");
                    }
                }

                SEnvir.Log($"已按目标数量加载 {loadedCount}/{botCount} 个假人账号，跳过 {skippedCount} 行");
            }
            catch (Exception ex)
            {
                SEnvir.Log($"加载假人配置失败: {ex.Message}");
            }
        }







        private static IEnumerable<string> GetDefaultBotGuildNames()
        {
            return Config.CanUseChineseGuildName ? BotDefaultGuildNamesChinese : BotDefaultGuildNamesEnglish;
        }

        private static IEnumerable<string> GetConfiguredBotGuildNames()
        {
            return _botGuildNames.Count > 0 ? _botGuildNames : GetDefaultBotGuildNames();
        }

        private static void LoadBotGuildNameConfig()
        {
            try
            {
                _botGuildNames.Clear();

                botGuildNameFilePath = ResolveBotGuildNameFilePath();
                EnsureBotGuildNameFileExists(botGuildNameFilePath);

                if (!File.Exists(botGuildNameFilePath))
                {
                    _botGuildNames.AddRange(GetDefaultBotGuildNames());
                    SEnvir.Log($"假人行会名字配置不存在，当前回退到内置默认名字池: {botGuildNameFilePath}");
                    return;
                }

                foreach (string rawLine in File.ReadAllLines(botGuildNameFilePath, Encoding.UTF8))
                {
                    if (string.IsNullOrWhiteSpace(rawLine))
                        continue;

                    string line = rawLine.Trim();
                    if (line.Length == 0 || line.StartsWith("#") || line.StartsWith("//") || line.StartsWith(";"))
                        continue;

                    if (!IsValidBotGuildNameConfigEntry(line))
                    {
                        SEnvir.Log($"假人行会名字配置忽略无效名称: {line}");
                        continue;
                    }

                    if (_botGuildNames.Any(x => string.Equals(x, line, StringComparison.OrdinalIgnoreCase)))
                        continue;

                    _botGuildNames.Add(line);
                }

                if (_botGuildNames.Count == 0)
                {
                    _botGuildNames.AddRange(GetDefaultBotGuildNames());
                    SEnvir.Log($"假人行会名字配置为空，当前回退到内置默认名字池: {botGuildNameFilePath}");
                    return;
                }

                SEnvir.Log($"假人行会名字配置已加载: {botGuildNameFilePath}, 名称 {_botGuildNames.Count} 个");
            }
            catch (Exception ex)
            {
                _botGuildNames.Clear();
                _botGuildNames.AddRange(GetDefaultBotGuildNames());
                SEnvir.Log($"加载假人行会名字配置失败: {ex.Message}");
            }
        }

        private static string ResolveBotGuildNameFilePath()
        {
            var candidates = new List<string>();

            try
            {
                if (!string.IsNullOrWhiteSpace(botFilePath))
                {
                    string fullBotPath = Path.IsPathRooted(botFilePath) ? botFilePath : Path.GetFullPath(botFilePath);
                    string botDir = Path.GetDirectoryName(fullBotPath);

                    if (!string.IsNullOrWhiteSpace(botDir))
                        candidates.Add(Path.Combine(botDir, "假人行会名字.txt"));
                }
            }
            catch
            {
            }

            string baseDir = AppDomain.CurrentDomain.BaseDirectory;
            if (!string.IsNullOrWhiteSpace(baseDir))
                candidates.Add(Path.Combine(baseDir, "假人行会名字.txt"));

            string currentDir = Environment.CurrentDirectory;
            if (!string.IsNullOrWhiteSpace(currentDir))
                candidates.Add(Path.Combine(currentDir, "假人行会名字.txt"));

            string existingPath = candidates.FirstOrDefault(File.Exists);
            return existingPath ?? candidates.FirstOrDefault() ?? "假人行会名字.txt";
        }

        private static void EnsureBotGuildNameFileExists(string path)
        {
            if (string.IsNullOrWhiteSpace(path) || File.Exists(path))
                return;

            try
            {
                string directory = Path.GetDirectoryName(path);
                if (!string.IsNullOrWhiteSpace(directory) && !Directory.Exists(directory))
                    Directory.CreateDirectory(directory);

                File.WriteAllLines(path, BuildDefaultBotGuildNameFileLines(), new UTF8Encoding(true));
                SEnvir.Log($"已自动创建假人行会名字配置: {path}");
            }
            catch (Exception ex)
            {
                SEnvir.Log($"创建假人行会名字配置失败: {ex.Message}");
            }
        }

        private static string[] BuildDefaultBotGuildNameFileLines()
        {
            var lines = new List<string>
            {
                "# 假人行会名字配置",
                "# 一行一个名字；空行、#、;、// 开头的行会被忽略。",
                "# 当配置里的名字都已被占用时，系统会基于这些名字自动追加数字后缀继续建会。",
                "# 当前版本修改后需要重启假人系统才会重新加载。",
                string.Empty,
            };

            lines.AddRange(GetDefaultBotGuildNames());
            return lines.ToArray();
        }

        private static bool IsValidBotGuildNameConfigEntry(string name)
        {
            if (string.IsNullOrWhiteSpace(name))
                return false;

            return Config.CanUseChineseGuildName
                ? Globals.GuildNameRegex.IsMatch(name)
                : Globals.EnGuildNameRegex.IsMatch(name);
        }


        private static List<BotAccountInfo> GetTargetBotAccountsSnapshot()
        {
            if (botCount <= 0 || botAccounts.Count == 0)
                return new List<BotAccountInfo>();

            return botAccounts.Take(Math.Min(botCount, botAccounts.Count)).ToList();
        }

        private static bool IsBotWithinTargetCount(BotAccountInfo bot)
        {
            if (bot == null || botCount <= 0)
                return false;

            int maxCount = Math.Min(botCount, botAccounts.Count);
            for (int i = 0; i < maxCount; i++)
            {
                if (ReferenceEquals(botAccounts[i], bot))
                    return true;
            }

            return false;
        }

        public static void UpdateTargetCount(int count)
        {
            int newCount = Math.Max(0, count);
            int oldCount = botCount;
            botCount = newCount;
            Config.BotCount = newCount;

            if (!isRunning)
            {
                SEnvir.Log($"假人目标数量已更新为 {newCount}，将在下次启动时生效");
                return;
            }

            if (newCount >= oldCount)
            {
                SEnvir.Log($"假人目标数量已更新为 {newCount}，当前在线 {botPlayers.Count}；后续登录将按新数量限制执行");
                return;
            }

            var removedAccounts = botAccounts
                .Skip(newCount)
                .Select(x => x?.Account)
                .Where(x => x != null)
                .Distinct()
                .ToHashSet();

            var playersToKick = botPlayers
                .Where(x => x?.Connection?.Account != null && removedAccounts.Contains(x.Connection.Account))
                .ToList();

            SEnvir.Log($"假人目标数量从 {oldCount} 下调到 {newCount}，准备踢下线 {playersToKick.Count} 个超额假人");

            if (playersToKick.Count == 0)
                return;

            SEnvir.BotActionQueue.Enqueue(() =>
            {
                foreach (var player in playersToKick)
                {
                    if (player?.Connection == null || !player.Connection.Connected) continue;

                    try
                    {
                        player.Connection.Disconnect();
                    }
                    catch (Exception ex)
                    {
                        SEnvir.Log($"自动踢下线超额假人异常 [{player.Name}]: {ex.Message}\n{ex.StackTrace}");
                    }
                }
            });
        }

        private static bool TryParseBotConfigLine(string line, out string account, out string password,
            out string charName, out MirClass jobClass, out MirGender gender)
        {
            account = string.Empty;
            password = string.Empty;
            charName = string.Empty;
            jobClass = MirClass.Warrior;
            gender = MirGender.Male;

            if (string.IsNullOrWhiteSpace(line)) return false;

            var parts = line.Split(',');

            if (parts.Length >= 5)
            {
                account = parts[0].Trim();
                password = parts[1].Trim();
                charName = parts[2].Trim();

                int classValue;
                int genderValue;
                if (!int.TryParse(parts[3].Trim(), out classValue)) return false;
                if (!int.TryParse(parts[4].Trim(), out genderValue)) return false;

                jobClass = (MirClass)classValue;
                gender = (MirGender)genderValue;
                return !string.IsNullOrWhiteSpace(account)
                    && !string.IsNullOrWhiteSpace(password)
                    && !string.IsNullOrWhiteSpace(charName);
            }

            if (parts.Length >= 3)
            {
                charName = parts[0].Trim();

                int classValue;
                int genderValue;
                if (!int.TryParse(parts[1].Trim(), out classValue)) return false;
                if (!int.TryParse(parts[2].Trim(), out genderValue)) return false;

                jobClass = (MirClass)classValue;
                gender = (MirGender)genderValue;
                account = BuildAutoBotAccount(charName);
                password = BuildAutoBotPassword(charName);
                return !string.IsNullOrWhiteSpace(charName);
            }

            return false;
        }

        private static string BuildAutoBotAccount(string charName)
        {
            return $"bot_auto_{charName}";
        }

        private static string BuildAutoBotPassword(string charName)
        {
            return $"bot_pwd_{charName}";
        }

        /// <summary>
        /// 注册假人账号
        /// </summary>
        private static AccountInfo RegisterBotAccount(string account, string password)
        {
            try
            {
                var existing = SEnvir.AccountInfoList.Binding.FirstOrDefault(x => x.EMailAddress == account);
                if (existing != null) return existing;

                var newAccount = SEnvir.AccountInfoList.CreateNewObject();
                newAccount.EMailAddress = account;
                newAccount.Password = Encoding.UTF8.GetBytes(password);
                newAccount.RealName = "Bot";
                newAccount.BirthDate = DateTime.Now.AddYears(-18);
                newAccount.Question = "bot";
                newAccount.Answer = "bot";
                newAccount.CreationIP = "127.0.0.1";
                newAccount.CreationDate = Time.Now;
                newAccount.Activated = true;
                newAccount.Admin = false;

                SEnvir.Log($"假人账号注册成功: {account}");
                return newAccount;
            }
            catch (Exception ex)
            {
                SEnvir.Log($"注册假人账号失败: {ex.Message}");
                return null;
            }
        }

        /// <summary>
        /// 创建假人角色
        /// </summary>
        private static CharacterInfo CreateBotCharacter(AccountInfo account, string charName, MirClass jobClass, MirGender gender)
        {
            try
            {
                if (account.Characters.Count >= Globals.MaxCharacterCount)
                    return null;

                var character = SEnvir.CharacterInfoList.CreateNewObject();
                character.Account = account;
                character.CharacterName = charName;
                character.Class = jobClass;
                character.Gender = gender;
                character.Level = 1;
                character.HairType = 0;
                character.HairColour = Color.Black;
                character.ArmourColour = Color.Black;
                character.CurrentHP = 100;
                character.CurrentMP = 50;

                long initialGold = Math.Max(0L, Config.BotInitialGoldFloor)
                                  + (jobClass == MirClass.Taoist ? BotTaoistStarterExtraGold : 0L);
                if (account.Gold < initialGold)
                    account.Gold = initialGold;

                // 必须初始化排行榜节点，否则升级时 RankingSort 会空引用崩溃
                character.RankingNode = SEnvir.Rankings.AddLast(character);
                SEnvir.RankingSort(character, false);

                SEnvir.Log($"假人角色创建成功: {charName}, 职业: {jobClass}, 性别: {gender}");
                return character;
            }
            catch (Exception ex)
            {
                SEnvir.Log($"创建假人角色失败: {ex.Message}");
                return null;
            }
        }

        /// <summary>
        /// 假人主 AI 分片处理（每 200ms 触发一个稳定槽，每个假人约 800ms 驱动一次）。
        /// ★ 只做轻量的"快照"和"投递"，不直接调用任何游戏逻辑。
        ///   所有游戏操作（Attack/Move/GainItem 等）都通过 SEnvir.BotActionQueue
        ///   投递到主循环中执行，确保线程安全。
        /// </summary>
        private static void BotTick(object state)
        {
            if (!isRunning) return;

            try
            {
                int currentSlice = (Interlocked.Increment(ref _botMainSliceCursor) & int.MaxValue) % BotMainSliceCount;
                int dispatchBudget = Math.Max(1, Math.Min(10000, Config.BotTickDispatchLimit));

                // 0. 全体回城指令（UI 线程通过 RecallAllBots() 设置标志位，此处在主线程中执行传送）
                if (currentSlice == 0 && _pendingRecallAll && !_recallActionQueued
                    && SEnvir.Now >= _botNextRecallBatchTime)
                {
                    _recallActionQueued = true;
                    SEnvir.BotActionQueue.Enqueue(ExecuteRecallAllBots);
                }

                // 社交记忆定期维护（衰减亲密度、清理过期记忆、自动保存）
                if (currentSlice == 0)
                    BotSocialMemory.Tick();

                // 地图/技能记忆自动保存（每 5 分钟保存一次跨会话经验）
                if (currentSlice == 0)
                    BotMemory.Tick();

                if (currentSlice == 0 && ShouldRunPeriodicBotGrouping())
                    ApplyGroupSwitchToAllBots(true);

                // 每3秒检查是否有待处理的自动组队重建
                if (currentSlice == 0 && _botGroupRebuildPending)
                    // SEnvir.Log($"[BotTick] 检测到待处理的自动组队重建, 下次执行时间={_botNextGroupRebuildTime}");
                    TryFlushPendingBotAutoGroupRebuild();

                // 1. 登录：分批将 Idle 账号的登录操作投递到主线程，避免首拍登录风暴。
                if (currentSlice == 0)
                {
                    int pendingLoginCount = botAccounts.Count(x => x?.BotState == DBModels.BotState.LoggingIn);
                    int onlineLimit = Math.Min(Math.Max(0, botCount), Math.Max(0, Config.BotMaxOnline));
                    int remainingLoginSlots = Math.Max(0, onlineLimit - botPlayers.Count - pendingLoginCount);
                    int loginDispatchBudget = Math.Min(Math.Min(BotLoginBatchSize, remainingLoginSlots), dispatchBudget);

                    foreach (var bot in botAccounts.ToList())
                    {
                        if (loginDispatchBudget <= 0) break;
                        if (bot.BotState != DBModels.BotState.Idle) continue;
                        if (!bot.CharacterCreated) continue;
                        if (GetBotPlayer(bot) != null) continue;

                        bot.BotState = DBModels.BotState.LoggingIn;
                        bot.LastActionTime = Time.Now;
                        loginDispatchBudget--;
                        dispatchBudget--;

                        var capturedBot = bot;
                        SEnvir.BotActionQueue.Enqueue(() => LoginBot(capturedBot));
                    }
                }

                // 2. 驱动在线假人 AI
                // ★ 每个假人独立投递一个 Lambda，彻底避免"大Lambda积压叠加"问题：
                //   - 假人多时，大Lambda执行时间>800ms → 下一轮已入队 → 主循环连续消费两轮
                //     → 同一假人在同一帧被驱动两次 → Move(东)后立刻Move(西) → 来回跑
                //   - 独立Lambda后，每个假人最多同时在队列里有1个待处理Lambda（由 _botQueued 标志保护）
                //   - 某个假人的AI很慢，也不会阻塞其他假人
                var snapshot = SnapshotBotPlayers();
                if (snapshot.Length == 0) return;

                foreach (var snapPlayer in snapshot)
                {
                    if (dispatchBudget <= 0) break;
                    if (snapPlayer == null) continue;
                    if (IsBotInWarmup(snapPlayer)) continue;

                    // ★ 防积压：若该假人上一轮的 Lambda 还没被消费，本轮跳过
                    // 避免队列里堆多个相同假人的 Lambda，导致同一帧连续驱动两次
                    uint snapId = snapPlayer.ObjectID;
                    if (snapId % BotMainSliceCount != (uint)currentSlice) continue;
                    if (!TryMarkBotQueued(_botQueued, snapId)) continue;

                    var capturedPlayer = snapPlayer; // 闭包捕获
                    SEnvir.BotActionQueue.Enqueue(() =>
                    {
                        // Lambda 进入消费，立即释放"占位"，允许下一个 800ms 周期重新投递
                        UnmarkBotQueued(_botQueued, capturedPlayer.ObjectID);

                        if (capturedPlayer == null) return;

                        // ── 死亡处理 ──────────────────────────────────────────
                        if (capturedPlayer.Dead)
                        {
                            if (capturedPlayer.Node == null)
                            {
                                _botDeathRecorded.TryRemove(capturedPlayer.ObjectID, out _);
                                // 角色已移出地图，清理并重置为 Idle 等待重新登录
                                RemoveBotPlayer(capturedPlayer);
                                _botStates.TryRemove(capturedPlayer.ObjectID, out _);
                                _botTargets.Remove(capturedPlayer.ObjectID);
                                _botTargetSwitchTime.Remove(capturedPlayer.ObjectID);
                                _botRoamDir.Remove(capturedPlayer.ObjectID);
                                _botRoamTime.Remove(capturedPlayer.ObjectID);
                                _botTargetItems.Remove(capturedPlayer.ObjectID);
                                _botWaitingPickup.Remove(capturedPlayer.ObjectID);
                                _botKiteMode.Remove(capturedPlayer.ObjectID);
                                _botLastAttackTime.Remove(capturedPlayer.ObjectID);
                                _botLastSnapPos.Remove(capturedPlayer.ObjectID);
                                _botLastSnapTime.Remove(capturedPlayer.ObjectID);
                                _botDriftAnchorPos.Remove(capturedPlayer.ObjectID);
                                _botDriftAnchorTime.Remove(capturedPlayer.ObjectID);
                                _botMapEvalTime.Remove(capturedPlayer.ObjectID);
                                _botMapStayMapIndex.Remove(capturedPlayer.ObjectID);
                                _botMapStayStartTime.Remove(capturedPlayer.ObjectID);
                                _botRecallUntil.Remove(capturedPlayer.ObjectID);
                                _botNextAttackAttemptTime.Remove(capturedPlayer.ObjectID);
                                _botNextPickupAttemptTime.Remove(capturedPlayer.ObjectID);
                                _botSkillLearnTime.Remove(capturedPlayer.ObjectID);
                                _botSellTime.Remove(capturedPlayer.ObjectID);
                                _botRestockTime.Remove(capturedPlayer.ObjectID);
                                _botPotionCooldownTime.Remove(capturedPlayer.ObjectID);
                                _botUrgentPotionBuyTime.Remove(capturedPlayer.ObjectID);
                                _botAssassinSupportTime.Remove(capturedPlayer.ObjectID);
                                _botNextSocialTime.Remove(capturedPlayer.ObjectID);
                                _botPendingChatReplies.Remove(capturedPlayer.ObjectID);
                                _botHighBossGroupPrepareTime.Remove(capturedPlayer.ObjectID);
                                _botUpcomingHighBossGroupTargets.Remove(capturedPlayer.ObjectID);
                                _botHumanInviteCooldown.Remove(capturedPlayer.ObjectID);
                                _botTelemetry.Remove(capturedPlayer.ObjectID);
                                _botBehaviorProfiles.Remove(capturedPlayer.ObjectID);
                                _botLoginWarmupUntil.Remove(capturedPlayer.ObjectID);
                                _botConquestApplyTime.Remove(capturedPlayer.ObjectID);
                                UnmarkBotQueued(_botPotionQueued, capturedPlayer.ObjectID);
                                _botTaoistLastPoisonCast.Remove(capturedPlayer.ObjectID);
                                _botTaoistPoisonUseCount.Remove(capturedPlayer.ObjectID);
                                _botLastTradePartner.Remove(capturedPlayer.ObjectID);
                                _botEquipmentMaintenanceTime.Remove(capturedPlayer.ObjectID);
                                _botConsumableMaintenanceTime.Remove(capturedPlayer.ObjectID);
                                _botInventoryMaintenanceTime.Remove(capturedPlayer.ObjectID);
                                _botClassSupportTime.Remove(capturedPlayer.ObjectID);
                                _botHighBossMaintenanceTime.Remove(capturedPlayer.ObjectID);
                                BotSocialMemory.ClearBot(capturedPlayer.ObjectID);

                                // 离开队伍，通知其他队员刷新状态

                                if (capturedPlayer.GroupMembers != null)
                                    try { capturedPlayer.GroupLeave(); } catch { }
                                SEnvir.Players.Remove(capturedPlayer);

                                var deadBot = botAccounts.FirstOrDefault(b =>
                                    b.Account == capturedPlayer.Connection?.Account);
                                if (deadBot != null)
                                    deadBot.BotState = DBModels.BotState.Idle;
                            }
                            else
                            {
                                if (_botDeathRecorded.TryAdd(capturedPlayer.ObjectID, 0))
                                {
                                    IncrementBotDeathCount();
                                    RecordManagementLog(BotLogKind.Activity,
                                        "假人死亡 [" + (capturedPlayer.Name ?? string.Empty) + "]");
                                }

                                // 仍在地图中，城镇复活
                                try
                                {
                                    capturedPlayer.TownRevive();
                                }
                                catch (Exception)
                                {
                                }
                            }
                            return;
                        }

                        if (capturedPlayer.Node == null) return;

                        _botDeathRecorded.TryRemove(capturedPlayer.ObjectID, out _);

                        ApplyBotLevelRewards(capturedPlayer);

                        if (capturedPlayer.InSafeZone)
                        {
                            if (capturedPlayer.CurrentHP < capturedPlayer.Stats[Stat.Health])
                                capturedPlayer.SetHP(capturedPlayer.Stats[Stat.Health]);

                            if (capturedPlayer.CurrentMP < capturedPlayer.Stats[Stat.Mana])
                                capturedPlayer.SetMP(capturedPlayer.Stats[Stat.Mana]);
                        }

                        ProcessConfiguredRecovery(capturedPlayer);
                        if (IsPaused) return;

                        // ── 正常 AI 驱动 ──────────────────────────────────────
                        try
                        {
                            ProcessBotBehaviorPipeline(capturedPlayer); // 通用模块 → 组队模块 → 职业模块

                        }
                        catch (Exception)
                        {
                            // SEnvir.Log($"假人AI处理异常 [{capturedPlayer.Name}]: {ex.Message}");
                        }
                    });
                    dispatchBudget--;
                }
            }
            catch (Exception)
            {
                // SEnvir.Log($"假人Tick处理异常: {ex.Message}");
            }
        }

        /// <summary>
        /// 独立药水监控。
        /// 只做血蓝检查与喝药投递，不参与选怪/移动/攻击，避免和主战斗逻辑互相阻塞。
        /// 投递到独立药水队列主线程执行，保证角色对象线程安全。
        /// </summary>
        private static void BotPotionTick(object state)
        {
            if (!isRunning) return;

            try
            {
                var snapshot = SnapshotBotPlayers();
                if (snapshot.Length == 0) return;

                foreach (var snapPlayer in snapshot)
                {
                    if (snapPlayer == null) continue;
                    if (IsBotInWarmup(snapPlayer)) continue;

                    uint snapId = snapPlayer.ObjectID;
                    if (!TryMarkBotQueued(_botPotionQueued, snapId)) continue;

                    var capturedPlayer = snapPlayer;
                    SEnvir.BotPotionActionQueue.Enqueue(() =>
                    {
                        UnmarkBotQueued(_botPotionQueued, capturedPlayer.ObjectID);

                        if (capturedPlayer == null || capturedPlayer.Node == null || capturedPlayer.Dead) return;


                        try
                        {
                            ProcessBotPotionModule(capturedPlayer);
                        }
                        catch (Exception)
                        {
                            // SEnvir.Log($"假人药水监控异常 [{capturedPlayer.Name}]: {ex.Message}");
                        }
                    });
                }
            }
            catch (Exception)
            {
                // SEnvir.Log($"假人药水Tick处理异常: {ex.Message}");
            }
        }

        /// <summary>
        /// 独立喝药模块：优先级最高，由 200ms 定时器驱动。
        /// </summary>
        private static void ProcessBotPotionModule(PlayerObject player)
        {
            if (Config.BotAutoPotionSupply)
                ProcessBotPotionMonitor(player);
        }

        private static bool IsBotInWarmup(PlayerObject player)
        {
            if (player == null) return false;

            return _botLoginWarmupUntil.TryGetValue(player.ObjectID, out DateTime until)
                   && SEnvir.Now < until;
        }

        private static void BeginBotLoginWarmup(PlayerObject player)
        {
            if (player == null) return;

            _botLoginWarmupUntil[player.ObjectID] = SEnvir.Now.AddSeconds(BotLoginWarmupSeconds);
        }

        private static void SetBotForcedGroupLock(PlayerObject player, DateTime until)
        {
            if (player == null) return;

            if (until <= SEnvir.Now)
            {
                _botForcedGroupLockUntil.Remove(player.ObjectID);
                return;
            }

            _botForcedGroupLockUntil[player.ObjectID] = until;
        }

        private static bool IsBotForcedGroupLockActive(PlayerObject player)
        {
            if (player == null) return false;
            return IsBotForcedGroupLockActive(player.ObjectID);
        }

        private static bool IsBotForcedGroupLockActive(uint objectID)
        {
            if (!_botForcedGroupLockUntil.TryGetValue(objectID, out DateTime until))
                return false;

            if (SEnvir.Now >= until)
            {
                _botForcedGroupLockUntil.Remove(objectID);
                return false;
            }

            return true;
        }

        private static void SetBotAutoGroupRebuildLock(DateTime until)
        {
            _botAutoGroupRebuildLockUntil = until > SEnvir.Now ? until : DateTime.MinValue;
        }

        private static void ScheduleBotAutoGroupRebuild()
        {
            if (!Config.BotAllowGroup || !Config.BotAutoGroup) return;

            DateTime scheduledAt = SEnvir.Now.AddSeconds(BotAutoGroupDebounceSeconds);
            if (_botAutoGroupRebuildLockUntil > scheduledAt)
                scheduledAt = _botAutoGroupRebuildLockUntil;

            _botGroupRebuildPending = true;
            _botNextGroupRebuildTime = scheduledAt;
        }

        private static void TryFlushPendingBotAutoGroupRebuild()
        {
            if (!_botGroupRebuildPending)
                return;

            if (!Config.BotAllowGroup || !Config.BotAutoGroup)
            {
                _botGroupRebuildPending = false;
                _botNextGroupRebuildTime = DateTime.MinValue;
                return;
            }

            if (_botAutoGroupRebuildLockUntil > SEnvir.Now)
            {
                if (_botNextGroupRebuildTime < _botAutoGroupRebuildLockUntil)
                    _botNextGroupRebuildTime = _botAutoGroupRebuildLockUntil;
                return;
            }

            if (SEnvir.Now < _botNextGroupRebuildTime)
                return;

            _botGroupRebuildPending = false;
            _botNextGroupRebuildTime = DateTime.MinValue;
            // SEnvir.Log($"[TryFlushPendingBotAutoGroupRebuild] 触发 ApplyGroupSwitchToAllBots, 当前在线假人数={BotManager.botPlayers.Count}");
            ApplyGroupSwitchToAllBots(true);
        }

        /// <summary>
        /// 假人总行为管线：常规喝药由独立 200ms 定时器处理，
        /// 职业战斗仍可在危险血线触发紧急喝药。
        /// </summary>
        private static void ProcessBotBehaviorPipeline(PlayerObject player)
        {
            if (player == null || player.Dead || player.Node == null) return;

            // 行会邀请：自动接受（AllowGuild 在 LoginBot 里已打开）
            if (Config.BotGuildSystem && player.GuildInvitation != null)
                player.GuildJoin();

            if (TryProcessBotRecallRecovery(player))
                return;

            if (player.TradePartner != null || player.TradePartnerRequest != null)
            {
                ClearBotPendingCombatActions(player);
                _botTargets.Remove(player.ObjectID);
                _botTargetItems.Remove(player.ObjectID);
                _botWaitingPickup.Remove(player.ObjectID);
                _botKiteMode.Remove(player.ObjectID);
                player.PacketWaiting = false;

                // 记录上一次交易伙伴，用于检测交易完成
                if (player.TradePartner != null)
                    _botLastTradePartner[player.ObjectID] = player.TradePartner;
                return;
            }

            // 检测交易完成：上一帧有交易伙伴，这一帧没了 → 交易结束
            PlayerObject lastPartner;
            if (_botLastTradePartner.TryGetValue(player.ObjectID, out lastPartner) && lastPartner != null)
            {
                // 如果双方都不在交易中了，记录社交记忆
                if (lastPartner.TradePartner == null)
                {
                    BotSocialMemory.RecordTradeSuccess(player, lastPartner);
                }
                _botLastTradePartner.Remove(player.ObjectID);
            }

            ApplyBotLevelRewards(player);

            if (TryProcessBotAutoRebirth(player))
                return;

            ProcessBotConquestApply(player);

            if (ProcessBotConquestWarfare(player))
                return;

            ProcessBotCommonModules(player);
            ProcessBotTeamModule(player);
            ProcessBotClassModules(player);
            ProcessBotSocialModule(player);
            ProcessBotTradeModule(player);
        }

        /// <summary>
        /// 全职业共享模块：装备、Buff 消耗品、技能学习、背包清理与货币兑换。
        /// Bot 自动经济操作统一在模块末尾同步一次金币，避免客户端先看到“卖东西得到金币”，
        /// 下一拍又因为前面静默补货/购书的延迟同步而弹出一条“减少金币”的错乱提示。
        /// </summary>
        private static void ProcessBotCommonModules(PlayerObject player)
        {
            long goldBefore = player?.Gold ?? 0;

            ProcessBotEquipmentModule(player);
            ProcessBotSupplyModule(player);
            ProcessBotConsumableModule(player);
            ProcessBotSkillModule(player);
            ProcessBotInventoryModule(player);

            FlushBotGoldState(player, goldBefore);
        }

        private static void ChangeBotGoldSilently(PlayerObject player, long amount)
        {
            if (player == null || amount == 0) return;
            player.Gold += amount;
        }

        private static void FlushBotGoldState(PlayerObject player, long goldBefore)
        {
            if (player == null) return;
            if (player.Gold == goldBefore) return;
            player.GoldChanged();
        }

        /// <summary>
        /// 全职业共享的装备模块。
        /// </summary>
        private static void ProcessBotEquipmentModule(PlayerObject player)
        {
            EquipStarterWeapon(player);
            if (ShouldRunBotMaintenance(_botEquipmentMaintenanceTime, player.ObjectID, BotEquipmentMaintenanceIntervalSeconds))
            {
                if (Config.BotAutoEquip)
                    ProcessBotAutoEquip(player);
                ProcessBotBuyEquip(player);
                if (Config.BotAutoSpecialRepair)
                    ProcessBotEquipmentRepair(player); // 检查并修复耐久低于配置阈值的装备
            }
        }

        /// <summary>
        /// 全职业共享的补给模块：定期检查并补充 HP/MP/双效药库存。
        /// </summary>
        private static void ProcessBotSupplyModule(PlayerObject player)
        {
            if (Config.BotAutoPotionSupply)
                ProcessBotPotionSupply(player, false);
        }

        /// <summary>
        /// 全职业共享的非药水消耗品模块。
        /// </summary>
        private static void ProcessBotConsumableModule(PlayerObject player)

        {
            if (ShouldRunBotMaintenance(_botConsumableMaintenanceTime, player.ObjectID, BotConsumableMaintenanceIntervalSeconds))
            {
                ProcessBotUseConsumable(player);
            }
        }

        /// <summary>
        /// 全职业共享的自动学技能模块。
        /// </summary>
        private static void ProcessBotSkillModule(PlayerObject player)
        {
            if (Config.BotAutoLearnSkill)
                ProcessBotLearnSkill(player);
        }

        /// <summary>
        /// 全职业共享的背包/货币整理模块。
        /// </summary>
        private static void ProcessBotInventoryModule(PlayerObject player)
        {
            if (ShouldRunBotMaintenance(_botInventoryMaintenanceTime, player.ObjectID, BotInventoryMaintenanceIntervalSeconds))
            {
                if (Config.BotAutoSellTrash)
                    ProcessBotSellInventory(player);
                ProcessBotUseGameGoldItems(player);
            }
        }

        /// <summary>
        /// 组队模块：处理组队邀请与队长跟随；站位纠偏后仍允许继续执行拾取/协战。
        /// </summary>
        private static void ProcessBotTeamModule(PlayerObject player)
        {
            if (ProcessBotSoloGoldFarmTeamIsolation(player)) return;

            ProcessBotGroupAccept(player);
            ProcessBotGroupFollow(player);
            if (Config.BotAutoGroup)
                ProcessBotHighBossGroupMaintenance(player);
        }

        /// <summary>
        /// 按职业分发行为模块，避免所有职业共用同一套行为组合。
        /// </summary>
        private static void ProcessBotClassModules(PlayerObject player)
        {
            switch (player.Class)
            {
                case MirClass.Warrior:
                    ProcessBotWarriorModules(player);
                    return;
                case MirClass.Wizard:
                    ProcessBotWizardModules(player);
                    return;
                case MirClass.Taoist:
                    ProcessBotTaoistModules(player);
                    return;
                default:
                    ProcessBotAssassinModules(player);
                    return;
            }
        }

        /// <summary>
        /// 假人社交模块：按当前战斗/拾取/组队/打金场景，从 假人聊天.txt 里抽台词主动说话，
        /// 并给附近假人安排延迟回复，形成简单互聊。
        /// </summary>

        /// <summary>
        /// 交易行为模块：bot之间互相交易多余装备，bot主动向真人交易极品装备。
        /// </summary>
        private static void ProcessBotTradeModule(PlayerObject player)
        {
            if (player == null || player.Dead || player.Node == null || !Config.BotAutoTrade) return;
            if (player.CurrentMap == null || !player.InSafeZone) return;

            uint pid = player.ObjectID;
            DateTime now = SEnvir.Now;

            // 检查交易冷却
            if (_botTradeCooldownUntil.TryGetValue(pid, out DateTime cooldownUntil) && now < cooldownUntil)
                return;

            // 优先处理bot之间互相交易多余装备
            DateTime lastBotTradeCheck;
            if (!_botLastTradeWithBotCheckTime.TryGetValue(pid, out lastBotTradeCheck))
                _botLastTradeWithBotCheckTime[pid] = now.AddSeconds(-BotTradeWithBotCheckInterval);

            if (now >= _botLastTradeWithBotCheckTime[pid].AddSeconds(BotTradeWithBotCheckInterval))
            {
                _botLastTradeWithBotCheckTime[pid] = now;
                if (TryProcessBotTradeWithOtherBot(player))
                    return;
            }

            // 检查bot向真人交易极品装备
            DateTime lastHumanTradeCheck;
            if (!_botLastTradeWithHumanCheckTime.TryGetValue(pid, out lastHumanTradeCheck))
                _botLastTradeWithHumanCheckTime[pid] = now.AddSeconds(-BotTradeWithHumanCheckInterval);

            if (now >= _botLastTradeWithHumanCheckTime[pid].AddSeconds(BotTradeWithHumanCheckInterval))
            {
                _botLastTradeWithHumanCheckTime[pid] = now;
                TryProcessBotTradeWithHuman(player);
            }
        }

        /// <summary>
        /// 尝试让bot与其他bot交易多余装备
        /// </summary>
        private static bool TryProcessBotTradeWithOtherBot(PlayerObject player)
        {
            if (player == null || player.Dead || player.Node == null) return false;
            if (player.CurrentMap == null) return false;

            uint pid = player.ObjectID;

            // 检查是否有可交易的装备
            List<UserItem> tradeableItems = GetBotTradeableItems(player, true);
            if (tradeableItems.Count == 0)
                return false;

            // 寻找附近的bot交易伙伴
            PlayerObject tradePartner = FindNearbyBotTradePartner(player);
            if (tradePartner == null)
                return false;

            // 检查对方是否有需要的装备
            List<UserItem> desiredItems = GetItemsDesiredByOtherBot(tradePartner, tradeableItems);
            if (desiredItems.Count == 0)
                return false;

            // 开始交易流程
            return TryInitiateBotTrade(player, tradePartner, desiredItems);
        }

        /// <summary>
        /// 尝试让bot向真人交易极品装备
        /// </summary>
        private static bool TryProcessBotTradeWithHuman(PlayerObject player)
        {
            if (player == null || player.Dead || player.Node == null) return false;
            if (player.CurrentMap == null) return false;

            uint pid = player.ObjectID;

            // 检查是否有极品装备
            List<UserItem> premiumItems = GetBotPremiumItems(player);
            if (premiumItems.Count == 0)
                return false;

            // 限制交易数量
            if (premiumItems.Count > BotTradeWithHumanMaxItems)
                premiumItems = premiumItems.Take(BotTradeWithHumanMaxItems).ToList();

            // 寻找附近的真人
            PlayerObject humanTarget = FindNearbyHumanForTrade(player);
            if (humanTarget == null)
                return false;

            // 开始交易流程
            return TryInitiateBotTrade(player, humanTarget, premiumItems);
        }

        /// <summary>
        /// 获取bot可交易的装备
        /// </summary>
        private static List<UserItem> GetBotTradeableItems(PlayerObject player, bool onlySurplus)
        {
            List<UserItem> tradeableItems = new List<UserItem>();

            if (player == null || player.Inventory == null)
                return tradeableItems;

            foreach (UserItem item in player.Inventory)
            {
                if (item == null || item.Info == null)
                    continue;

                // 检查物品是否可交易
                if (!IsItemTradable(player, item))
                    continue;

                // 只检查装备
                if (!IsEquipmentItem(item.Info.ItemType))
                    continue;

                // 如果只需要多余装备，检查是否已经装备了同类更好的装备
                if (onlySurplus && IsItemBetterThanEquipped(player, item))
                    continue;

                tradeableItems.Add(item);
            }

            return tradeableItems;
        }

        /// <summary>
        /// 获取bot的极品装备
        /// </summary>
        private static List<UserItem> GetBotPremiumItems(PlayerObject player)
        {
            List<UserItem> premiumItems = new List<UserItem>();

            if (player == null || player.Inventory == null)
                return premiumItems;

            foreach (UserItem item in player.Inventory)
            {
                if (item == null || item.Info == null)
                    continue;

                // 检查物品是否可交易
                if (!IsItemTradable(player, item))
                    continue;

                // 只检查装备
                if (!IsEquipmentItem(item.Info.ItemType))
                    continue;

                // 计算装备评分
                int score = (int)CalculateWeightedItemScore(item, player.Character.Class);
                if (score >= BotPremiumEquipmentScoreThreshold)
                    premiumItems.Add(item);
            }

            // 按评分降序排序
            premiumItems.Sort((a, b) => CalculateWeightedItemScore(b, player.Character.Class)
                .CompareTo(CalculateWeightedItemScore(a, player.Character.Class)));

            return premiumItems;
        }

        /// <summary>
        /// 检查物品是否可交易
        /// </summary>
        private static bool IsItemTradable(PlayerObject player, UserItem item)
        {
            if (item == null || item.Info == null)
                return false;

            // 检查绑定状态
            if (item.Flags.HasFlag(UserItemFlags.Bound))
                return false;

            // 检查婚姻物品
            if (item.Flags.HasFlag(UserItemFlags.Marriage))
                return false;

            // 检查物品是否允许交易
            if (!item.Info.CanTrade)
                return false;

            // 管理员物品不可交易
            if (!player.Character.Account.Admin && (item.Flags & UserItemFlags.Bound) == UserItemFlags.Bound)
                return false;

            return true;
        }

        /// <summary>
        /// 检查物品是否为装备
        /// </summary>
        private static bool IsEquipmentItem(ItemType itemType)
        {
            return itemType == ItemType.Weapon
                || itemType == ItemType.Armour
                || itemType == ItemType.Helmet
                || itemType == ItemType.Necklace
                || itemType == ItemType.Shoes
                || itemType == ItemType.Ring
                || itemType == ItemType.Bracelet
                || itemType == ItemType.Torch
                || itemType == ItemType.Amulet
                || itemType == ItemType.HorseArmour
                || itemType == ItemType.Flower;
        }

        /// <summary>
        /// 检查物品是否比当前装备更好
        /// </summary>
        private static bool IsItemBetterThanEquipped(PlayerObject player, UserItem item)
        {
            if (player == null || item == null || item.Info == null)
                return false;

            long itemScore = CalculateWeightedItemScore(item, player.Character.Class);

            // 查找对应装备槽的当前装备
            EquipmentSlot? slot = GetEquipmentSlotForItemType(item.Info.ItemType);
            if (!slot.HasValue)
                return false;

            int slotIndex = (int)slot.Value;
            if (slotIndex < 0 || slotIndex >= player.Equipment.Length)
                return false;

            UserItem equippedItem = player.Equipment[slotIndex];
            if (equippedItem == null || equippedItem.Info == null)
                return true;

            long equippedScore = CalculateWeightedItemScore(equippedItem, player.Character.Class);
            return itemScore > equippedScore;
        }

        /// <summary>
        /// 根据物品类型获取装备槽
        /// </summary>
        private static EquipmentSlot? GetEquipmentSlotForItemType(ItemType itemType)
        {
            if (ItemTypeToSlot.ContainsKey(itemType))
                return ItemTypeToSlot[itemType];

            return null;
        }

        /// <summary>
        /// 查找附近的bot交易伙伴
        /// </summary>
        private static PlayerObject FindNearbyBotTradePartner(PlayerObject player)
        {
            if (player == null || player.CurrentMap == null)
                return null;

            PlayerObject nearestBot = null;
            int nearestDistance = int.MaxValue;

            foreach (PlayerObject otherBot in botPlayers)
            {
                if (otherBot == null || otherBot == player)
                    continue;

                if (otherBot.Dead || otherBot.Node == null)
                    continue;

                if (otherBot.CurrentMap != player.CurrentMap)
                    continue;

                if (otherBot.TradePartner != null || otherBot.TradePartnerRequest != null)
                    continue;

                if (otherBot.PacketWaiting || (otherBot.ActionList?.Count ?? 0) > 0)
                    continue;

                int distance = Functions.Distance(player.CurrentLocation, otherBot.CurrentLocation);
                if (distance > BotTradeWithBotMaxDistance)
                    continue;

                if (distance < nearestDistance)
                {
                    nearestDistance = distance;
                    nearestBot = otherBot;
                }
            }

            return nearestBot;
        }

        /// <summary>
        /// 查找附近的真人进行交易
        /// </summary>
        private static PlayerObject FindNearbyHumanForTrade(PlayerObject player)
        {
            if (player == null || player.CurrentMap == null)
                return null;

            PlayerObject nearestHuman = null;
            int nearestDistance = int.MaxValue;

            foreach (PlayerObject otherPlayer in SEnvir.Players)
            {
                if (otherPlayer == null || otherPlayer == player)
                    continue;

                if (otherPlayer.IsBot)
                    continue;

                if (otherPlayer.Dead || otherPlayer.Node == null)
                    continue;

                if (otherPlayer.CurrentMap != player.CurrentMap)
                    continue;

                if (otherPlayer.TradePartner != null || otherPlayer.TradePartnerRequest != null)
                    continue;

                int distance = Functions.Distance(player.CurrentLocation, otherPlayer.CurrentLocation);
                if (distance > BotTradeWithHumanMaxDistance)
                    continue;

                if (distance < nearestDistance)
                {
                    nearestDistance = distance;
                    nearestHuman = otherPlayer;
                }
            }

            return nearestHuman;
        }

        /// <summary>
        /// 获取另一个bot需要的物品
        /// </summary>
        private static List<UserItem> GetItemsDesiredByOtherBot(PlayerObject otherBot, List<UserItem> availableItems)
        {
            List<UserItem> desiredItems = new List<UserItem>();

            if (otherBot == null || availableItems == null || availableItems.Count == 0)
                return desiredItems;

            foreach (UserItem item in availableItems)
            {
                if (item == null || item.Info == null)
                    continue;

                // 检查职业是否匹配
                if (item.Info.RequiredClass != RequiredClass.None && item.Info.RequiredClass != RequiredClass.All)
                {
                    RequiredClass classMask = ClassToRequired.ContainsKey(otherBot.Character.Class)
                        ? ClassToRequired[otherBot.Character.Class]
                        : RequiredClass.None;

                    if ((item.Info.RequiredClass & classMask) == 0)
                        continue;
                }

                // 检查性别是否匹配
                if (item.Info.RequiredGender != RequiredGender.None)
                {
                    RequiredGender genderMask = GenderToRequired.ContainsKey(otherBot.Character.Gender)
                        ? GenderToRequired[otherBot.Character.Gender]
                        : RequiredGender.None;

                    if ((item.Info.RequiredGender & genderMask) == 0)
                        continue;
                }

                // 检查等级要求 (暂时注释掉,ItemInfo可能没有直接的等级属性)
                // if (otherBot.Level < item.Info.RequiredLevel)
                //     continue;

                // 检查装备是否比对方当前装备好
                if (IsItemBetterThanEquipped(otherBot, item))
                    desiredItems.Add(item);
            }

            return desiredItems;
        }

        /// <summary>
        /// 尝试发起bot交易
        /// </summary>
        private static bool TryInitiateBotTrade(PlayerObject requester, PlayerObject target, List<UserItem> itemsToTrade)
        {
            if (requester == null || target == null || itemsToTrade == null || itemsToTrade.Count == 0)
                return false;

            if (requester.TradePartner != null || requester.TradePartnerRequest != null)
                return false;

            if (target.TradePartner != null || target.TradePartnerRequest != null)
                return false;

            uint pid = requester.ObjectID;

            // 设置交易冷却
            _botTradeCooldownUntil[pid] = SEnvir.Now.AddSeconds(BotTradeCooldownSeconds);

            // 清理当前动作
            ClearBotPendingCombatActions(requester);
            _botTargets.Remove(pid);
            _botTargetItems.Remove(pid);
            _botWaitingPickup.Remove(pid);
            _botKiteMode.Remove(pid);
            requester.PacketWaiting = false;

            // 如果目标是真人，移动到真人附近
            if (!target.IsBot)
            {
                int distance = Functions.Distance(requester.CurrentLocation, target.CurrentLocation);
                if (distance > 3)
                {
                    Point nearbyLocation = FindNearbyWalkableLocation(target.CurrentMap, target.CurrentLocation, 2);
                    if (nearbyLocation != Point.Empty)
                    {
                        requester.Teleport(target.CurrentMap, nearbyLocation, false);
                    }
                }
            }

            // 发起交易请求
            requester.TradeRequest(target.Character.Index);

            return true;
        }

        /// <summary>
        /// 查找附近可走的格子
        /// </summary>
        private static Point FindNearbyWalkableLocation(Map map, Point center, int maxDistance)
        {
            if (map == null)
                return Point.Empty;

            for (int distance = 1; distance <= maxDistance; distance++)
            {
                for (int dx = -distance; dx <= distance; dx++)
                {
                    for (int dy = -distance; dy <= distance; dy++)
                    {
                        if (Math.Abs(dx) != distance && Math.Abs(dy) != distance)
                            continue;

                        Point location = new Point(center.X + dx, center.Y + dy);
                        Cell cell = map.GetCell(location);

                        if (cell != null && !cell.IsBlocking(null, false))
                            return location;
                    }
                }
            }

            return Point.Empty;
        }









        /// <summary>
        /// 战士行为模块：PK → 拾取 → 打怪升级。
        /// </summary>
        private static void ProcessBotWarriorModules(PlayerObject player)
        {
            if (ProcessBotPK(player)) return;
            if (Config.BotAutoPickup)
                ProcessBotPickUp(player);
            ProcessBotCombat(player);
        }

        /// <summary>
        /// 法师行为模块：防御Buff → PK → 拾取 → 打怪升级。
        /// 具体技能与站位在职业战斗模块里单独处理。
        /// </summary>
        private static void ProcessBotWizardModules(PlayerObject player)
        {
            if (ShouldRunBotMaintenance(_botClassSupportTime, player.ObjectID, BotClassSupportIntervalSeconds))
            {
                ProcessBotWizardAttackBuff(player);
                ProcessBotWizardDefenceBuff(player);
            }

            if (ProcessBotPK(player)) return;
            if (Config.BotAutoPickup)
                ProcessBotPickUp(player);
            ProcessBotCombat(player);
        }

        /// <summary>
        /// 道士行为模块：补给/召唤/Buff → PK → 拾取 → 打怪升级。
        /// </summary>
        private static void ProcessBotTaoistModules(PlayerObject player)
        {
            if (ShouldRunBotMaintenance(_botClassSupportTime, player.ObjectID, BotClassSupportIntervalSeconds))
            {
                ProcessBotTaoistSupply(player);
                ProcessBotTaoistEquipSupply(player);
                ProcessBotTaoistSummon(player);
                ProcessBotTaoistDefenceBuff(player);
                ProcessBotTaoistSupportBuff(player);
            }

            if (ProcessBotPK(player)) return;
            if (Config.BotAutoPickup)
                ProcessBotPickUp(player);
            ProcessBotCombat(player);
        }

        /// <summary>
        /// 刺客行为模块：先补傀儡/维持防御增益，再处理 PK、拾取与战斗。
        /// </summary>
        private static void ProcessBotAssassinModules(PlayerObject player)
        {
            if (ShouldRunBotMaintenance(_botClassSupportTime, player.ObjectID, BotClassSupportIntervalSeconds))
            {
                ProcessBotAssassinSupport(player);
                ProcessBotAssassinDefenceBuff(player);
            }

            if (ProcessBotPK(player)) return;
            if (Config.BotAutoPickup)
                ProcessBotPickUp(player);
            ProcessBotCombat(player);
        }

        // 刺客支援模块冷却：ObjectID → 下次允许尝试补傀儡/补增益的时间
        private static readonly Dictionary<uint, DateTime> _botAssassinSupportTime
            = new Dictionary<uint, DateTime>();

        /// <summary>
        /// 刺客支援模块冷却时间（秒）：避免每 Tick 重复召唤/补 Buff。
        /// </summary>
        private const int BotAssassinSupportCooldown = 5;

        /// <summary>
        /// 刺客支援模块：优先补亡灵替身，其次补风之守护/闪避/增伤/集中等自保增益。
        /// </summary>
        private static void ProcessBotAssassinSupport(PlayerObject player)
        {
            if (player == null || player.Dead) return;
            if (player.Class != MirClass.Assassin) return;

            uint pid = player.ObjectID;
            if (_botAssassinSupportTime.TryGetValue(pid, out DateTime nextSupport) && SEnvir.Now < nextSupport) return;
            if (!player.CanCast || player.PacketWaiting || player.ActionList.Count > 0) return;

            MagicType summonMagic = BotSkillSelector.GetAssassinSummonMagic(player);
            if (summonMagic != MagicType.None)
            {
                if (TryCastBotMagic(player, player.Direction, summonMagic, player, player.CurrentLocation))
                    _botAssassinSupportTime[pid] = SEnvir.Now.AddSeconds(BotAssassinSupportCooldown);
                return;
            }

            MagicType buffMagic = BotSkillSelector.GetAssassinBuffMagic(player);
            if (buffMagic == MagicType.None) return;

            if (TryCastBotMagic(player, player.Direction, buffMagic, player, player.CurrentLocation))
                _botAssassinSupportTime[pid] = SEnvir.Now.AddSeconds(BotAssassinSupportCooldown);
        }

        private static BotBehaviorProfile GetBotBehaviorProfile(PlayerObject player)
        {
            if (player == null) return null;

            if (!_botBehaviorProfiles.TryGetValue(player.ObjectID, out BotBehaviorProfile profile))
            {
                int seed = unchecked((int)player.ObjectID * 397) ^ ((int)player.Class * 131);
                Random profileRandom = new Random(seed);

                profile = new BotBehaviorProfile
                {
                    AggressionBias = profileRandom.Next(-2, 3),
                    CautionBias = profileRandom.Next(-2, 3),
                    FollowSlack = profileRandom.Next(-2, 3),
                    RoamRandomnessPct = profileRandom.Next(18, 42),
                    SocialDelayBiasMs = profileRandom.Next(-400, 601),
                };

                switch (player.Class)
                {
                    case MirClass.Warrior:
                        profile.AggressionBias += 1;
                        break;
                    case MirClass.Wizard:
                    case MirClass.Taoist:
                        profile.CautionBias += 1;
                        break;
                    case MirClass.Assassin:
                        profile.AggressionBias += 1;
                        profile.RoamRandomnessPct += 4;
                        break;
                }

                _botBehaviorProfiles[player.ObjectID] = profile;
            }

            return profile;
        }

        private static BotTelemetryWindow GetBotTelemetry(PlayerObject player)
        {
            if (player == null) return null;

            if (!_botTelemetry.TryGetValue(player.ObjectID, out BotTelemetryWindow telemetry))
            {
                telemetry = new BotTelemetryWindow
                {
                    WindowStart = SEnvir.Now,
                    CurrentMapIndex = player.CurrentMap?.Info?.Index ?? -1,
                    CurrentMapEnterTime = SEnvir.Now,
                };

                _botTelemetry[player.ObjectID] = telemetry;
            }
            else if (telemetry.WindowStart == DateTime.MinValue)
            {
                telemetry.WindowStart = SEnvir.Now;
            }

            EnsureBotTelemetryMapContext(player, telemetry);
            return telemetry;
        }

        private static BotMapRuntimeMetrics GetBotMapRuntimeMetrics(BotTelemetryWindow telemetry, int mapIndex)
        {
            if (telemetry == null || mapIndex < 0) return null;

            if (!telemetry.MapMetrics.TryGetValue(mapIndex, out BotMapRuntimeMetrics metrics))
            {
                metrics = new BotMapRuntimeMetrics();
                telemetry.MapMetrics[mapIndex] = metrics;
            }

            return metrics;
        }

        private static void FlushBotTelemetryMapStay(BotTelemetryWindow telemetry)
        {
            if (telemetry == null || telemetry.CurrentMapIndex < 0 || telemetry.CurrentMapEnterTime == DateTime.MinValue)
                return;

            double staySeconds = Math.Max(0, (SEnvir.Now - telemetry.CurrentMapEnterTime).TotalSeconds);
            if (staySeconds > 0)
            {
                BotMapRuntimeMetrics metrics = GetBotMapRuntimeMetrics(telemetry, telemetry.CurrentMapIndex);
                if (metrics != null)
                    metrics.ActiveSeconds += staySeconds;

                // 学习记忆：记录地图驻留时间
                BotMemory.RecordMapStay(telemetry.CurrentMapIndex, staySeconds);
            }

            telemetry.CurrentMapEnterTime = SEnvir.Now;
        }

        private static void EnsureBotTelemetryMapContext(PlayerObject player, BotTelemetryWindow telemetry = null)
        {
            if (player?.CurrentMap?.Info == null) return;

            telemetry = telemetry ?? GetBotTelemetry(player);
            if (telemetry == null) return;

            int mapIndex = player.CurrentMap.Info.Index;
            if (telemetry.CurrentMapIndex != mapIndex)
            {
                FlushBotTelemetryMapStay(telemetry);
                telemetry.CurrentMapIndex = mapIndex;
                telemetry.CurrentMapEnterTime = SEnvir.Now;
            }

            BotMapRuntimeMetrics metrics = GetBotMapRuntimeMetrics(telemetry, mapIndex);
            if (metrics == null) return;

            metrics.LastVisitTime = SEnvir.Now;
            if (metrics.Visits <= 0)
                metrics.Visits = 1;
        }

        private static BotMapRuntimeMetrics GetCurrentBotMapRuntimeMetrics(PlayerObject player, BotTelemetryWindow telemetry = null)
        {
            telemetry = telemetry ?? GetBotTelemetry(player);
            if (telemetry == null) return null;

            EnsureBotTelemetryMapContext(player, telemetry);
            return GetBotMapRuntimeMetrics(telemetry, telemetry.CurrentMapIndex);
        }

        private static void RecordBotPotionUsage(PlayerObject player)
        {
            BotTelemetryWindow telemetry = GetBotTelemetry(player);
            if (telemetry == null) return;

            telemetry.PotionsUsed++;
        }

        private static void RecordBotMagicCastResult(PlayerObject player, bool success)
        {
            BotTelemetryWindow telemetry = GetBotTelemetry(player);
            if (telemetry == null) return;

            BotMapRuntimeMetrics metrics = GetCurrentBotMapRuntimeMetrics(player, telemetry);
            if (success)
            {
                telemetry.MagicSuccessCount++;
                if (metrics != null)
                    metrics.MagicSuccessCount++;
            }
            else
            {
                telemetry.MagicFailCount++;
                if (metrics != null)
                    metrics.MagicFailCount++;
            }
        }

        private static void RecordBotMoveResult(PlayerObject player, bool success)
        {
            if (player == null) return;

            if (success)
            {
                EnsureBotTelemetryMapContext(player);
                return;
            }

            BotTelemetryWindow telemetry = GetBotTelemetry(player);
            if (telemetry == null) return;

            telemetry.BlockedMoves++;

            BotMapRuntimeMetrics metrics = GetCurrentBotMapRuntimeMetrics(player, telemetry);
            if (metrics != null)
                metrics.BlockedMoves++;
        }

        private static void RecordBotMapSwitch(PlayerObject player, Map destination)
        {
            BotTelemetryWindow telemetry = GetBotTelemetry(player);
            if (telemetry == null) return;

            FlushBotTelemetryMapStay(telemetry);
            telemetry.MapSwitches++;

            if (destination?.Info == null) return;

            telemetry.CurrentMapIndex = destination.Info.Index;
            telemetry.CurrentMapEnterTime = SEnvir.Now;

            BotMapRuntimeMetrics metrics = GetBotMapRuntimeMetrics(telemetry, telemetry.CurrentMapIndex);
            if (metrics != null)
            {
                metrics.Visits++;
                metrics.LastVisitTime = SEnvir.Now;
            }

            // 切图时清除技能选择缓存，让假人在新地图重新评估最优技能
            BotSkillSelector.ClearBotSkillCache(player.ObjectID);
        }

        private static void RecordBotKill(PlayerObject player, MapObject target)
        {
            if (player == null || target?.CurrentMap?.Info == null) return;

            IncrementBotKillCount();

            BotTelemetryWindow telemetry = GetBotTelemetry(player);
            if (telemetry == null) return;

            telemetry.Kills++;

            BotMapRuntimeMetrics metrics = GetBotMapRuntimeMetrics(telemetry, target.CurrentMap.Info.Index);
            if (metrics != null)
            {
                metrics.Kills++;
                metrics.LastVisitTime = SEnvir.Now;
            }

            // 学习记忆：记录击杀
            BotMemory.RecordKill(target.CurrentMap.Info.Index);

            // 社交记忆：同队成员一起战斗
            RecordSocialFightTogether(player);
        }

        private static void RecordBotPickup(PlayerObject player, ItemObject item)
        {
            BotTelemetryWindow telemetry = GetBotTelemetry(player);
            if (telemetry == null) return;

            telemetry.Pickups++;

            BotMapRuntimeMetrics metrics = GetCurrentBotMapRuntimeMetrics(player, telemetry);
            if (metrics != null)
                metrics.Pickups++;

            // 学习记忆：记录拾取
            if (player?.CurrentMap?.Info != null)
                BotMemory.RecordPickup(player.CurrentMap.Info.Index);
        }

        /// <summary>
        /// 记录同队成员一起战斗（社交记忆辅助方法）
        /// 在 RecordBotKill 中调用，避免每次击杀都遍历全队。
        /// </summary>
        private static void RecordSocialFightTogether(PlayerObject player)
        {
            if (player?.GroupMembers == null || player.GroupMembers.Count <= 1)
                return;

            foreach (PlayerObject member in player.GroupMembers)
            {
                if (member == null || member == player || member.Dead || member.Node == null)
                    continue;
                if (member.CurrentMap != player.CurrentMap)
                    continue;

                BotSocialMemory.RecordFightTogether(player, member);
            }
        }

        private static void RecordBotBossEvent(PlayerObject player, bool retreat, bool switchedAdd)
        {
            BotTelemetryWindow telemetry = GetBotTelemetry(player);
            if (telemetry == null) return;

            if (retreat) telemetry.BossRetreats++;
            if (switchedAdd) telemetry.BossAddSwitches++;

            BotMapRuntimeMetrics metrics = GetCurrentBotMapRuntimeMetrics(player, telemetry);
            if (metrics != null)
                metrics.BossMechanicEvents++;
        }

        private static void RecordBotGroupReset(PlayerObject player)
        {
            BotTelemetryWindow telemetry = GetBotTelemetry(player);
            if (telemetry == null) return;

            telemetry.GroupResets++;
        }


        /// <summary>
        /// 采样目标血量：定期记录当前目标的血量，用于预测血量是否快速下降
        /// </summary>
        private static void SampleBotTargetHealth(uint playerObjectId, MapObject target)
        {
            if (target == null || target.Dead || target.Race != ObjectType.Monster) return;

            // 检查是否到了采样时间
            if (_botTargetHealthSampleTime.TryGetValue(playerObjectId, out DateTime lastSampleTime))
            {
                if ((SEnvir.Now - lastSampleTime).TotalSeconds < BotTargetHealthSampleInterval)
                    return;
            }

            // 获取当前血量
            MonsterObject monster = target as MonsterObject;
            if (monster == null) return;

            int currentHP = monster.CurrentHP;
            int maxHP = Math.Max(1, monster.Stats[Stat.Health]);
            int hpPct = currentHP * 100 / maxHP;

            // 初始化血量历史记录
            if (!_botTargetHealthHistory.TryGetValue(playerObjectId, out List<int> healthHistory))
            {
                healthHistory = new List<int>();
                _botTargetHealthHistory[playerObjectId] = healthHistory;
            }

            // 添加当前血量百分比
            healthHistory.Add(hpPct);

            // 保持历史记录在合理范围内
            if (healthHistory.Count > BotTargetHealthHistoryMaxSize)
            {
                healthHistory.RemoveAt(0);
            }

            _botTargetHealthSampleTime[playerObjectId] = SEnvir.Now;
        }

        /// <summary>
        /// 判断目标血量是否快速下降：基于最近几次采样的血量趋势
        /// </summary>
        /// <returns>true 表示血量快速下降，应该继续黏住当前目标</returns>
        private static bool IsTargetHealthDroppingFast(uint playerObjectId, MapObject target)
        {
            if (target == null || target.Dead || target.Race != ObjectType.Monster) return false;

            if (!_botTargetHealthHistory.TryGetValue(playerObjectId, out List<int> healthHistory))
                return false;

            // 历史记录太少无法判断
            if (healthHistory.Count < 3)
                return false;

            // 计算平均下降速度（每秒血量百分比下降）
            int oldestHP = healthHistory[0];
            int newestHP = healthHistory[healthHistory.Count - 1];
            int hpDrop = oldestHP - newestHP;

            if (hpDrop <= 0)
                return false;

            // 时间跨度 = (记录数 - 1) * 采样间隔
            double timeSpanSeconds = (healthHistory.Count - 1) * BotTargetHealthSampleInterval;
            if (timeSpanSeconds <= 0)
                return false;

            // 计算每秒下降百分比
            double dropPerSecond = hpDrop / timeSpanSeconds;

            // 判断是否快速下降
            return dropPerSecond >= BotTargetHealthDropFastThreshold;
        }

        private static void ObserveBotTelemetry(PlayerObject player)
        {
            BotTelemetryWindow telemetry = GetBotTelemetry(player);
            if (telemetry == null) return;

            if ((SEnvir.Now - telemetry.WindowStart).TotalSeconds < BotTelemetrySummaryWindowSeconds)
                return;

            FlushBotTelemetryMapStay(telemetry);

            bool blockedWarn = telemetry.BlockedMoves >= BotTelemetryBlockedMoveWarnThreshold;
            bool magicWarn = telemetry.MagicFailCount >= BotTelemetryMagicFailWarnThreshold
                             && telemetry.MagicFailCount >= telemetry.MagicSuccessCount;
            bool bossWarn = telemetry.BossRetreats + telemetry.BossAddSwitches >= BotTelemetryBossWarnThreshold;

            if (blockedWarn || magicWarn || bossWarn)
            {
                // SEnvir.Log($"Bot观测[{player.Name}] 近{BotTelemetrySummaryWindowSeconds}秒: 击杀={telemetry.Kills}, 喝药={telemetry.PotionsUsed}, 施法成功={telemetry.MagicSuccessCount}, 施法失败={telemetry.MagicFailCount}, 移动受阻={telemetry.BlockedMoves}, 切图={telemetry.MapSwitches}, 拾取={telemetry.Pickups}, Boss规避={telemetry.BossRetreats}, 转火小怪={telemetry.BossAddSwitches}");
            }

            telemetry.WindowStart = SEnvir.Now;
            telemetry.Kills = 0;
            telemetry.PotionsUsed = 0;
            telemetry.MagicSuccessCount = 0;
            telemetry.MagicFailCount = 0;
            telemetry.BlockedMoves = 0;
            telemetry.MapSwitches = 0;
            telemetry.Pickups = 0;
            telemetry.BossRetreats = 0;
            telemetry.BossAddSwitches = 0;
            telemetry.SocialMessages = 0;
            telemetry.GroupResets = 0;
        }

        private static int GetBotRuntimeMapScoreAdjustment(PlayerObject player, Map map)
        {
            if (player == null || map?.Info == null) return 0;

            int adjustment = Math.Max(0, Config.BotMapPoolBonus);
            int otherPlayers = Math.Max(0, map.PlayerCount - ((player.CurrentMap == map && player.Node != null) ? 1 : 0));
            int botCount = map.Players.Count(x => x != null && x.BotPlayer);

            adjustment -= Math.Max(0, otherPlayers - 4) * 6;
            adjustment -= Math.Max(0, botCount - 3) * 8;

            if (!_botTelemetry.TryGetValue(player.ObjectID, out BotTelemetryWindow telemetry) || telemetry == null)
                return adjustment;

            if (telemetry.CurrentMapIndex == map.Info.Index)
                FlushBotTelemetryMapStay(telemetry);

            if (!telemetry.MapMetrics.TryGetValue(map.Info.Index, out BotMapRuntimeMetrics metrics) || metrics == null)
                return adjustment;

            if (metrics.ActiveSeconds < BotRuntimeMapMetricsMinSeconds)
                return adjustment;

            double minutes = Math.Max(0.5, metrics.ActiveSeconds / 60.0);
            double killsPerMinute = metrics.Kills / minutes;
            double pickupsPerMinute = metrics.Pickups / minutes;
            double blockedPerMinute = metrics.BlockedMoves / minutes;
            double magicFailPerMinute = metrics.MagicFailCount / minutes;

            adjustment += (int)Math.Round(Math.Min(120, killsPerMinute * 12 + pickupsPerMinute * 8));
            adjustment -= (int)Math.Round(Math.Min(140, blockedPerMinute * 6 + magicFailPerMinute * 5));
            adjustment -= Math.Min(60, metrics.BossMechanicEvents * 4);

            // 学习记忆：参考历史地图刷怪效率
            adjustment += BotMemory.GetMapMemoryScoreBonus(map.Info.Index);

            return adjustment;
        }

        private static long GetBotEconomyReserveTarget(PlayerObject player)
        {
            if (player == null) return Config.BotGoldFarmThreshold;

            switch (GetBotProgressionStage(player))
            {
                case BotProgressionStage.SafeNursery:
                    return 120000;
                case BotProgressionStage.TownOutskirts:
                    return 220000;
                case BotProgressionStage.MixedLevelAndBooks:
                    return 500000;
                case BotProgressionStage.LevelRush:
                    return 900000;
                case BotProgressionStage.HighBookFarm:
                    return 1500000;
                case BotProgressionStage.LateLevelRush:
                    return 2200000;
                default:
                    return Config.BotGoldFarmThreshold;
            }
        }

        private static int GetBotEquipmentEconomyPriority(ItemType itemType)
        {
            switch (itemType)
            {
                case ItemType.Weapon:
                    return 0;
                case ItemType.Armour:
                    return 1;
                case ItemType.Helmet:
                case ItemType.Shoes:
                    return 2;
                case ItemType.Necklace:
                    return 3;
                case ItemType.Bracelet:
                case ItemType.Ring:
                    return 4;
                default:
                    return 5;
            }
        }

        private static bool ShouldBotDeferEquipmentPurchase(PlayerObject player, ItemType itemType)
        {
            if (player == null) return false;
            if (player.Gold >= GetBotEconomyReserveTarget(player)) return false;

            int priority = GetBotEquipmentEconomyPriority(itemType);
            switch (GetBotProgressionStage(player))
            {
                case BotProgressionStage.SafeNursery:
                case BotProgressionStage.TownOutskirts:
                    return priority > 1;
                case BotProgressionStage.MixedLevelAndBooks:
                case BotProgressionStage.LevelRush:
                    return priority > 2;
                case BotProgressionStage.HighBookFarm:
                case BotProgressionStage.LateLevelRush:
                    return priority > 3;
                default:
                    return priority > 2;
            }
        }

    }
}

