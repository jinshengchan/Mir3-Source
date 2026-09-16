using Library;
using Library.Network;
using Library.SystemModels;
using MirDB;
using Server.DBModels;
using Server.Models;
using Server.Models.Monsters;
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
    public static partial class BotManager
    {
        // ══════════════════════════════════════════════════════════════════════
        //  AI – 自动打怪升级（参考真人自动打怪逻辑）
        // ══════════════════════════════════════════════════════════════════════

        // 跨 Tick 目标锁定表：假人 ObjectID → 当前锁定目标（怪物 / 真人 / 宠物主人）
        private static readonly Dictionary<uint, MapObject> _botTargets
            = new Dictionary<uint, MapObject>();

        // 假人最近被攻击者记录：假人 ObjectID → 攻击者列表（ObjectID列表，用于判断被几个真人攻击）
        private static readonly Dictionary<uint, List<uint>> _botLastAttackers
            = new Dictionary<uint, List<uint>>();

        // 假人最近攻击者记录时间：假人 ObjectID → 最后被攻击时间（用于清理过期的攻击者记录）
        private static readonly Dictionary<uint, DateTime> _botLastAttackedTime
            = new Dictionary<uint, DateTime>();

        // 切怪超时表：假人 ObjectID → 下次允许换怪的时间（仿真人 TargetSwitchTime，默认10s未打死则换怪）
        private static readonly Dictionary<uint, DateTime> _botTargetSwitchTime
            = new Dictionary<uint, DateTime>();

        // 目标血量历史记录：假人 ObjectID → 目标血量历史（用于判断血量是否快速下降）
        private static readonly Dictionary<uint, List<int>> _botTargetHealthHistory
            = new Dictionary<uint, List<int>>();

        // 目标血量历史记录时间：假人 ObjectID → 上次记录血量的时间
        private static readonly Dictionary<uint, DateTime> _botTargetHealthSampleTime
            = new Dictionary<uint, DateTime>();

        // 漫游方向表：假人 ObjectID → 当前漫游方向（视野无怪时持续沿此方向跑）
        private static readonly Dictionary<uint, MirDirection> _botRoamDir
            = new Dictionary<uint, MirDirection>();

        // 漫游换向时间表：假人 ObjectID → 下次允许换方向的时间（仿真人 pathfindertime，避免每Tick随机抖动）
        private static readonly Dictionary<uint, DateTime> _botRoamTime
            = new Dictionary<uint, DateTime>();

        // 拾取目标表：假人 ObjectID → 当前锁定的地面物品（仿宠物 TargetItem 跨Tick持久化）
        private static readonly Dictionary<uint, ItemObject> _botTargetItems
            = new Dictionary<uint, ItemObject>();

        // PVP 风筝模式标记：假人 ObjectID → 是否处于风筝模式（战士风筝时跳过突进贴脸）
        private static readonly Dictionary<uint, bool> _botKiteMode
            = new Dictionary<uint, bool>();

        // 等待拾取标志：假人 ObjectID 在此集合中时，表示"锁定的怪已死，优先捡物品后再打怪"
        // 记录的值是进入等待拾取状态的时间，用于超时兜底（防止无掉落物时永久阻塞攻击）
        private static readonly Dictionary<uint, DateTime> _botWaitingPickup
            = new Dictionary<uint, DateTime>();

        // 出售冷却：假人 ObjectID → 下次允许常规出售的时间（避免每Tick扫描全背包）
        private static readonly Dictionary<uint, DateTime> _botSellTime
            = new Dictionary<uint, DateTime>();

        // 补药冷却：假人 ObjectID → 下次允许检查药水库存并补货的时间
        private static readonly Dictionary<uint, DateTime> _botRestockTime
            = new Dictionary<uint, DateTime>();

        // 假人药水冷却：ObjectID → 下次允许再次主动喝药的时间
        // 只约束独立药水监控，不影响攻击/施法节奏。
        private static readonly Dictionary<uint, DateTime> _botPotionCooldownTime
            = new Dictionary<uint, DateTime>();

        // 紧急缺药补货节奏：ObjectID → 下次允许因“当前要喝但背包没药”而立刻补货的时间
        private static readonly Dictionary<uint, DateTime> _botUrgentPotionBuyTime
            = new Dictionary<uint, DateTime>();

        /// <summary>
        /// 药水库存检查冷却（秒）：避免每 Tick 扫描物品表和背包。
        /// </summary>
        private const int BotPotionRestockCooldownSeconds = 30;

        /// <summary>
        /// 紧急缺药时的即时补货冷却（秒）：避免 200ms 药水监控持续触发重复买药。
        /// </summary>
        private const int BotPotionShortageBuyCooldownSeconds = 5;

        /// <summary>
        /// HP 药库存低于此值时触发补货。
        /// </summary>
        private const int BotMinHealthPotionCount = 80;

        /// <summary>
        /// MP 药库存低于此值时触发补货。
        /// </summary>
        private const int BotMinManaPotionCount = 80;

        /// <summary>
        /// 双效药库存低于此值时触发补货。
        /// </summary>
        private const int BotMinDualPotionCount = 20;

        /// <summary>
        /// HP 药补货目标数量。
        /// </summary>
        private const int BotTargetHealthPotionCount = 200;

        /// <summary>
        /// MP 药补货目标数量。
        /// </summary>
        private const int BotTargetManaPotionCount = 200;

        /// <summary>
        /// 双效药补货目标数量。
        /// </summary>
        private const int BotTargetDualPotionCount = 60;


        private const int BotPotionRetryIntervalMs = 800;


        /// <summary>
        /// 兼容大补贴“HP保持值”：假人默认至少把血线保到这个绝对值以上。
        /// </summary>
        private const int BotPotionKeepHpValue = 180;

        /// <summary>
        /// 兼容大补贴“智能调整最大血量%”：按最大血量百分比动态抬高喝红线。
        /// </summary>
        private const int BotPotionKeepHpMaxPct = 92;

        /// <summary>
        /// HP 低于该百分比时，直接进入优先补血区，哪怕本次缺口还没吃满一整瓶也会立刻喝药。
        /// </summary>
        private const int BotPotionHpCriticalPct = 50;

        /// <summary>
        /// HP 低于该百分比时无视喝药冷却强制追喝，防止死于冷却空档期。
        /// </summary>
        private const int BotPotionEmergencyHpPct = 15;

        /// <summary>
        /// 兼容大补贴“MP保持值”：假人默认至少把蓝线保到这个绝对值以上。
        /// </summary>
        private const int BotPotionKeepMpValue = 120;

        /// <summary>
        /// 兼容大补贴“智能调整最大蓝量%”：按最大蓝量百分比动态抬高喝蓝线。
        /// </summary>
        private const int BotPotionKeepMpMaxPct = 82;

        /// <summary>
        /// MP 低于该百分比时，直接进入优先补蓝区，避免战斗中空蓝发呆。
        /// </summary>
        private const int BotPotionMpCriticalPct = 50;

        /// <summary>
        /// HP、MP 同时低于该百分比时，优先使用双效药。
        /// </summary>
        private const int BotPotionDualPriorityPct = 75;

        /// <summary>
        /// 非危急状态下，缺口至少达到药水恢复量的该百分比时才喝，避免只掉一点点就浪费整瓶药。
        /// </summary>
        private const int BotPotionEffectiveUsePct = 35;

        // 防积压标志：正在 BotActionQueue 中等待消费的假人 ObjectID 集合
        // BotTick 投递 Lambda 前加入，Lambda 开始执行时移除
        // 避免同一假人在队列里堆多个 Lambda，导致同一帧被连续驱动两次（来回跑）
        private static readonly HashSet<uint> _botQueued = new HashSet<uint>();

        // 药水监控的独立防积压标志，避免 200ms Tick 持续堆叠同一假人的喝药任务
        private static readonly HashSet<uint> _botPotionQueued = new HashSet<uint>();

        private static readonly object _botQueueSync = new object();

        private static bool TryMarkBotQueued(HashSet<uint> queue, uint objectId)
        {
            lock (_botQueueSync)
            {
                if (queue.Contains(objectId)) return false;
                queue.Add(objectId);
                return true;
            }
        }

        private static void UnmarkBotQueued(HashSet<uint> queue, uint objectId)
        {
            lock (_botQueueSync)
                queue.Remove(objectId);
        }

        private static void ClearBotQueuedMarkers()
        {
            lock (_botQueueSync)
            {
                _botQueued.Clear();
                _botPotionQueued.Clear();
            }
        }

        /// <summary>
        /// 清除假人的全部战斗追踪状态（目标/漫游/卡死检测/血量历史）。
        /// 用于切图、卡死解救、漂移逃脱等场景。
        /// </summary>
        private static void ClearBotCombatTrackingState(uint pid)
        {
            _botTargets.Remove(pid);
            _botTargetSwitchTime.Remove(pid);
            _botRoamDir.Remove(pid);
            _botRoamTime.Remove(pid);
            _botLastSnapPos.Remove(pid);
            _botLastSnapTime.Remove(pid);
            _botDriftAnchorPos.Remove(pid);
            _botDriftAnchorTime.Remove(pid);
            _botTargetHealthHistory.Remove(pid);
            _botTargetHealthSampleTime.Remove(pid);
            BotPathFinder.ClearPath(pid); // 切图/卡死时清 A* 路径缓存
        }

        /// <summary>
        /// 清除假人的目标锁定状态（目标+切怪超时+血量历史）。
        /// 用于紧急逃跑、目标失效、PVP逃跑等场景。
        /// </summary>
        private static void ClearBotTargetLockState(uint pid)
        {
            _botTargets.Remove(pid);
            _botTargetSwitchTime.Remove(pid);
            _botTargetHealthHistory.Remove(pid);
            _botTargetHealthSampleTime.Remove(pid);
            BotPathFinder.ClearPath(pid); // 换目标/失效时清 A* 路径缓存
        }

        /// <summary>
        /// 怪物死亡后等待拾取的最长时间（秒）。
        /// 若超过此时间还没有可捡物品（无掉落 / 物品保护时间内），自动解除等待状态，继续攻击。
        /// </summary>
        private const int BotPickupWaitTimeout = 6;

        /// <summary>
        /// 常规背包出售/清理的冷却时间（秒）。
        /// 触发紧急条件（背包格不足 / 负重超限）时无视此冷却立即执行。
        /// </summary>
        private const int BotSellCooldownSeconds = 10;

        /// <summary>
        /// 背包空格紧急阈值：剩余空格数 ≤ 此值时，立即绕过出售冷却强制清理。
        /// </summary>
        private const int BotSellUrgentFreeSlots = 5;

        /// <summary>
        /// 负重紧急阈值（百分比）：BagWeight ≥ MaxBagWeight × 此值 / 100 时，立即绕过冷却强制清理。
        /// </summary>
        private const int BotSellUrgentWeightPct = 90;

        /// <summary>
        /// 因负重卖药时，尽量把背包压回到这个安全百分比以下，避免下一拍又立刻触发超重清理。
        /// </summary>
        private const int BotSellPotionTargetWeightPct = 85;

        /// <summary>
        /// 目标切换超时（秒）：锁定怪物后超过此时间且近期没有有效输出时，才允许切换新目标。
        /// </summary>
        private const int BotTargetSwitchTimeout = 10;

        /// <summary>
        /// 切怪保护时间（秒）：只要最近还在持续出手，就继续黏住当前目标，别打一半又换怪乱跑。
        /// </summary>
        private const int BotTargetSwitchAttackGraceSeconds = 5;

        /// <summary>
        /// 目标血量历史采样间隔（秒）：每隔多久采样一次目标血量
        /// </summary>
        private const int BotTargetHealthSampleInterval = 1;

        /// <summary>
        /// 目标血量快速下降阈值（%/秒）：每秒血量下降超过此百分比则认为目标血量快速下降
        /// </summary>
        private const double BotTargetHealthDropFastThreshold = 5.0;

        /// <summary>
        /// 目标血量历史最大记录数：保留最近N次血量采样
        /// </summary>
        private const int BotTargetHealthHistoryMaxSize = 6;

        /// <summary>
        /// 附近清怪半径（切比雪夫距离，格）。
        /// 无论是否组队，都先把这个范围内的怪物逐个清掉，再考虑协战/漫游。
        /// </summary>
        private const int BotNearbyMonsterSweepRange = 6;

        /// <summary>
        /// 组队跟随：队员假人距队长超过此格数（切比雪夫距离）时，传送到队长旁边。
        /// 不在同一张地图时无视此阈值，直接传送。
        /// </summary>
        private const int BotFollowLeaderMaxDist = 15;

        /// <summary>
        /// 组队成员自主选怪时允许偏离队长的最大距离（切比雪夫距离）。
        /// 超出后不再自己接新怪，避免整队越打越散、一路串图跑偏。
        /// </summary>
        private const int BotGroupTargetLeashRange = 10;

        // ── 卡死检测 ────────────────────────────────────────────────────────
        // 最后一次成功攻击时间（用于检测是否长时间未打到怪）
        private static readonly Dictionary<uint, DateTime> _botLastAttackTime
            = new Dictionary<uint, DateTime>();

        // 上一次记录的坐标快照（用于检测是否在小范围循环移动）
        private static readonly Dictionary<uint, Point>    _botLastSnapPos
            = new Dictionary<uint, Point>();

        // 坐标快照时刻（每 BotStuckCheckInterval 秒检查一次位置变化）
        private static readonly Dictionary<uint, DateTime> _botLastSnapTime
            = new Dictionary<uint, DateTime>();

        // ── 小范围漂移卡死检测（新） ─────────────────────────────────────
        // 锚点：上次确认"有效漂移"或刚进入检测时的位置（用于判断2分钟内是否离开5格范围）
        private static readonly Dictionary<uint, Point>    _botDriftAnchorPos
            = new Dictionary<uint, Point>();

        // 锚点记录时刻：上次刷新锚点的时间，超过 BotDriftStuckTimeout 且仍在5格内即触发解卡
        private static readonly Dictionary<uint, DateTime> _botDriftAnchorTime
            = new Dictionary<uint, DateTime>();

        // 地图评估时刻：假人 ObjectID → 下次允许重新评估当前地图是否适合的时间
        private static readonly Dictionary<uint, DateTime> _botMapEvalTime
            = new Dictionary<uint, DateTime>();

        // 当前驻留地图索引：假人 ObjectID → 本轮驻图统计对应的地图 Index
        private static readonly Dictionary<uint, int> _botMapStayMapIndex
            = new Dictionary<uint, int>();

        // 当前地图驻留起始时间：假人 ObjectID → 进入当前统计地图的时间
        private static readonly Dictionary<uint, DateTime> _botMapStayStartTime
            = new Dictionary<uint, DateTime>();

        // 回城冻结时刻：假人 ObjectID → 允许恢复打怪升级的时间（回城后延时1分钟）
        private static readonly Dictionary<uint, DateTime> _botRecallUntil
            = new Dictionary<uint, DateTime>();
        private static readonly System.Collections.Concurrent.ConcurrentDictionary<uint, byte> _botDeathRecorded
            = new System.Collections.Concurrent.ConcurrentDictionary<uint, byte>();
        private static readonly Dictionary<uint, DateTime> _botNextAttackAttemptTime
            = new Dictionary<uint, DateTime>();
        private static readonly Dictionary<uint, DateTime> _botNextPickupAttemptTime
            = new Dictionary<uint, DateTime>();

        /// <summary>
        /// 假人回城目标地图索引（道馆，MapInfo.Index = 7）。
        /// </summary>
        private const int BotHomeMapIndex = 7;

        /// <summary>
        /// 假人回城目标坐标（道馆 400, 123）。
        /// </summary>
        private static readonly Point BotHomePoint = new Point(400, 123);

        /// <summary>
        /// 回城后恢复打怪升级的延迟时间（秒）。
        /// </summary>
        private const int BotRecallRestSeconds = 60;
        private const int BotCriticalRecallHpPct = 5;

        /// <summary>
        /// 标志位：是否有待执行的全体回城请求（由 UI 线程写，BotTick 主循环消费）。
        /// 使用 volatile 保证跨线程可见性。
        /// </summary>
        private static volatile bool _pendingRecallAll = false;
        private static BotBatchResult _pendingRecallResult;
        private static int _botRecallBatchOffset;
        private static DateTime _botNextRecallBatchTime = DateTime.MinValue;
        private static volatile bool _recallActionQueued;

        /// <summary>
        /// 无攻击超时阈值（秒）：超过此时间既未攻击又未有效移动，则视为卡死。
        /// </summary>
        private const int BotStuckAttackTimeout = 15;

        /// <summary>
        /// 坐标快照间隔（秒）：每隔此时间记录一次位置，用于判断是否原地/小范围循环。
        /// </summary>
        private const int BotStuckCheckInterval = 5;

        /// <summary>
        /// 判定"有效移动"的最小曼哈顿距离：在 BotStuckCheckInterval 内移动距离 ≤ 此值
        /// 视为没有有效位移（在两点间来回算无效）。
        /// </summary>
        private const int BotStuckMinMoveRange = 3;

        /// <summary>
        /// 小范围漂移卡死超时（秒）：在此时间内始终未离开 BotDriftStuckRange 格范围
        /// 且没有攻击动作、不在安全区，则视为漂移卡死，传送到当前地图内 BotDriftEscapeMinDist 格以外。
        /// </summary>
        private const int BotDriftStuckTimeout = 120;

        /// <summary>
        /// 漂移卡死判定范围（曼哈顿距离）：2分钟内位移不超过此值即触发解卡。
        /// </summary>
        private const int BotDriftStuckRange = 5;

        /// <summary>
        /// 漂移解卡传送最小距离：要求落点与当前位置的曼哈顿距离 ≥ 此值。
        /// </summary>
        private const int BotDriftEscapeMinDist = 10;

        /// <summary>
        /// 地图适合性评估间隔（秒）：常规练级时每隔此时间检查一次当前地图是否仍适合假人停留。
        /// </summary>
        private const int BotMapEvalInterval = 120;

        /// <summary>
        /// 打金模式地图评估间隔（秒）：缺钱时延长驻图时间，避免为了追分频繁切图。
        /// </summary>
        private const int BotGoldFarmMapEvalInterval = 180;

        /// <summary>
        /// 普通打金模式切图分差：只有新地图明显更赚钱，才值得换图。
        /// </summary>
        private const int BotGoldFarmSwitchMargin = 60;

        /// <summary>
        /// 应急打金模式切图分差：金币=0且背包无药时允许更积极找更安全的图，但仍避免来回抖动。
        /// </summary>
        private const int BotEmergencyGoldFarmSwitchMargin = 15;

        /// <summary>
        /// 低阶刷图地图的强制轮换间隔（秒）：超过此时间还停留在无 60 级以上 Boss 的图里，就主动换图继续刷金币/装备/技能书。
        /// </summary>
        private const int BotLowTierFarmMapStaySeconds = 1800;

        /// <summary>
        /// 高阶 Boss 判定等级阈值：地图存在高于此等级的 Boss 刷新点时，不纳入低阶轮换池。
        /// </summary>
        private const int BotHighLevelBossThreshold = 60;

        /// <summary>
        /// 怪物等级容差：目标地图怪物平均等级比假人等级高超过此值时，拒绝进入。
        /// </summary>
        private const int BotMapLevelTolerance = 3;

        /// <summary>
        /// 地图平均伤害至少要让假人能扛住这么多下，否则视为危险地图。
        /// </summary>
        private const int BotMapSafeAverageHits = 6;

        /// <summary>
        /// 地图峰值伤害至少要让假人能扛住这么多下，否则视为容易暴毙。
        /// </summary>
        private const int BotMapSafePeakHits = 4;

        /// <summary>
        /// 怪物最高准确比假人敏捷高出太多时，命中过高，拒绝进入。
        /// </summary>
        private const int BotMapMaxAccuracyGap = 12;

        /// <summary>
        /// 法师 / 道士远程技能最小保持距离（切比雪夫距离，格）。
        /// 与怪物距离 &lt; 此值时，假人主动后退拉开距离。
        /// </summary>
        private const int BotRangedMinDist = 2;

        /// <summary>
        /// 法师 / 道士远程技能最大攻击距离（切比雪夫距离，格）。
        /// 与怪物距离 &gt; 此值时，假人向前追击进入射程。
        /// </summary>
        private const int BotRangedMaxDist = 5;

        /// <summary>
        /// 低血量逃跑阈值（当前HP占最大HP的百分比）。
        /// 所有职业的假人血量低于此值时，停止攻击并向远离怪物方向移动。
        /// </summary>
        private const int BotFleeHpPct = 30;

        private static readonly Random _botRandom = new Random();

        private static bool ShouldBotFarmGold(PlayerObject player)
        {
            return player != null && player.Gold < Math.Max(Config.BotGoldFarmThreshold, GetBotEconomyReserveTarget(player));
        }


        private static bool ShouldBotEmergencyGoldFarm(PlayerObject player)
        {
            if (player == null || player.Gold > 0) return false;

            CountBotPotionStock(player, out int healthCount, out int manaCount, out int dualCount);
            return healthCount <= 0 && manaCount <= 0 && dualCount <= 0;
        }

        private static void GetBotGoldFarmContext(PlayerObject player, out bool goldFarmMode, out bool emergencyGoldFarmMode)
        {
            goldFarmMode = ShouldBotFarmGold(player);
            emergencyGoldFarmMode = ShouldBotEmergencyGoldFarm(player);

            if (emergencyGoldFarmMode)
                goldFarmMode = true;
        }

        private static bool IsBotSoloRun(PlayerObject player)
        {
            return player?.GroupMembers == null || player.GroupMembers.Count <= 1;
        }

        private static bool ShouldBotAvoidTownBigMap(PlayerObject player, bool goldFarmMode)
        {
            if (player == null || player.Level < 30) return false;

            return !(goldFarmMode && IsBotSoloRun(player));
        }

        private static bool IsBotTownBigMap(Map map)
        {
            return map?.HasSafeZone == true;
        }

        // ══════════════════════════════════════════════════════════════════════
        //  高级技能书地图判断
        // ══════════════════════════════════════════════════════════════════════
        /// <summary>
        /// 判断地图是否为高级技能书掉落地图（BOSS 图白名单）。
        /// </summary>
        private static bool IsBotHighSkillBookMap(Map map)
        {
            if (map?.Info == null) return false;

            string mapName = map.Info.FileName ?? string.Empty;
            string mapDesc = map.Info.Description ?? string.Empty;

            // 检查是否命中白名单关键词
            foreach (string keyword in BotHighSkillBookMapKeywords)
            {
                if (string.IsNullOrEmpty(keyword)) continue;

                // 不区分大小写匹配
                if (mapName.IndexOf(keyword, StringComparison.OrdinalIgnoreCase) >= 0)
                {
                    return true;
                }
                if (mapDesc.IndexOf(keyword, StringComparison.OrdinalIgnoreCase) >= 0)
                {
                    return true;
                }
            }

            return false;
        }

        private static bool ProcessBotSoloGoldFarmTeamIsolation(PlayerObject player)
        {
            if (!ShouldBotEmergencyGoldFarm(player)) return false;
            if (player == null) return false;

            PlayerObject inviter = player.GroupInvitation;
            bool humanInvitePending = inviter != null && inviter.Node != null && !botPlayers.Contains(inviter);
            if (humanInvitePending)
                return false;

            if (player.GroupMembers != null && player.GroupMembers.Count > 0)
            {
                PlayerObject leader = player.GroupMembers[0];
                bool hasHumanLeader = leader != null && leader.Node != null && !botPlayers.Contains(leader);
                if (hasHumanLeader)
                    return false;
            }

            if (player.GroupInvitation != null)
                player.GroupInvitation = null;

            if (player.GroupMembers != null)
            {
                try
                {
                    player.GroupLeave();
                }
                catch (Exception)
                {
                }
            }

            return true;
        }

        private static void GetBotGroupLeaderContext(PlayerObject player, out PlayerObject groupLeader, out bool hasHumanLeader)
        {
            groupLeader = null;
            hasHumanLeader = false;

            if (!Config.BotAllowGroup || player?.GroupMembers == null || player.GroupMembers.Count <= 1)
                return;

            groupLeader = player.GroupMembers[0];
            if (groupLeader == null || groupLeader == player || groupLeader.Node == null || groupLeader.Dead)
                return;

            // ★ 性能优化：用 IsBotConnection 快速判断是否为假人，避免 botPlayers.Contains() O(n) 扫描
            hasHumanLeader = !groupLeader.IsBot;
        }

        private static bool IsBotGroupSharedTarget(PlayerObject player, MapObject target)
        {
            if (player?.GroupMembers == null || target == null) return false;

            foreach (PlayerObject member in player.GroupMembers)
            {
                if (member == null || member.Node == null || member.Dead) continue;
                if (ReferenceEquals(member, target)) return true;
            }

            return false;
        }

        private static bool IsValidBotAssistTarget(PlayerObject player, MapObject target)
        {
            if (player == null || target == null || target.Node == null || target.Dead) return false;
            if (IsBotGroupSharedTarget(player, target)) return false;

            return player.CanAttackTarget(target);
        }

        private static bool IsValidUmaKingHornForConquest(UserItem item)
        {
            if (item?.Info?.Effect != ItemEffect.UmaKingHorn) return false;
            if (item.SourceRace != ObjectType.Monster) return false;
            if (string.IsNullOrWhiteSpace(item.SourceName)) return false;

            return item.SourceName.IndexOf("祖玛教主", StringComparison.OrdinalIgnoreCase) >= 0
                   || item.SourceName.IndexOf("ZumaKing", StringComparison.OrdinalIgnoreCase) >= 0;
        }

        private static bool CanBotScanDrop(PlayerObject player, ItemObject item)
        {
            if (player == null || item?.Item == null) return false;
            if (item.Item.Info?.Effect == ItemEffect.UmaKingHorn && !IsValidUmaKingHornForConquest(item.Item))
                return false;

            bool canScan;
            if (item.Account == null)
            {
                canScan = true;
            }
            else if (item.Account == player.Character?.Account)
            {
                canScan = true;
            }
            else if (player.GroupMembers != null)
            {
                canScan = false;
                foreach (PlayerObject member in player.GroupMembers)
                {
                    if (member?.Character?.Account != item.Account) continue;

                    canScan = true;
                    break;
                }
            }
            else
            {
                canScan = false;
            }

            if (!canScan) return false;

            return IsPreferredBotGroupSkillBookPicker(player, item);
        }

        private static bool IsPreferredBotGroupSkillBookPicker(PlayerObject player, ItemObject item)
        {
            if (player == null || !player.IsBot || item?.Item?.Info == null)
                return true;
            if (!item.MonsterDrop || player.GroupMembers == null || player.GroupMembers.Count <= 1)
                return true;
            if (item.Item.Info.ItemType != ItemType.Book)
                return true;

            MagicInfo magic = SEnvir.MagicInfoList.Binding.FirstOrDefault(x => x?.Index == item.Item.Info.Shape);
            if (magic == null)
                return true;

            PlayerObject bestPicker = null;
            int bestDistance = int.MaxValue;

            foreach (PlayerObject member in player.GroupMembers)
            {
                if (member == null || !member.IsBot || member.Node == null || member.Dead) continue;
                if (member.CurrentMap != item.CurrentMap) continue;
                if (!Functions.InRange(member.CurrentLocation, item.CurrentLocation, Config.MaxViewRange)) continue;
                if (member.Class != magic.Class) continue;
                if (member.Magics.ContainsKey(magic.Magic)) continue;

                int distance = Functions.Distance(member.CurrentLocation, item.CurrentLocation);
                if (bestPicker != null)
                {
                    if (distance > bestDistance) continue;
                    if (distance == bestDistance && member.ObjectID >= bestPicker.ObjectID) continue;
                }

                bestPicker = member;
                bestDistance = distance;
            }

            return bestPicker == null || ReferenceEquals(bestPicker, player);
        }


        private static bool HasBotImmediateCombatTarget(PlayerObject player, int maxDistance = 1)
        {
            if (player == null) return false;
            if (!_botTargets.TryGetValue(player.ObjectID, out MapObject target)) return false;
            if (target == null || target.Node == null || target.Dead) return false;
            if (!player.CanAttackTarget(target)) return false;

            return MaxChebyshevDistance(player.CurrentLocation, target.CurrentLocation) <= Math.Max(1, maxDistance);
        }

        private static bool IsValidBotSweepMonster(PlayerObject player, MonsterObject monster, int maxDistance)
        {
            if (player == null || monster == null || monster.Node == null || monster.Dead) return false;
            if (monster.CurrentMap != player.CurrentMap) return false;
            if (monster.PetOwner != null) return false;
            if (monster.MonsterInfo?.AI < 0) return false;
            if (monster.MonsterInfo?.AI == 4) return false;
            if (!player.CanAttackTarget(monster)) return false;

            return MaxChebyshevDistance(player.CurrentLocation, monster.CurrentLocation) <= Math.Max(1, maxDistance);
        }

        private static bool IsBotGroupFocusedMonster(PlayerObject player, MonsterObject monster)
        {
            if (player?.GroupMembers == null || monster == null) return false;

            foreach (PlayerObject member in player.GroupMembers)
            {
                if (member == null || member.Node == null || member.Dead) continue;

                if (_botTargets.TryGetValue(member.ObjectID, out MapObject trackedTarget)
                    && ReferenceEquals(trackedTarget, monster))
                    return true;

                if (member.GroupAssistTargetTime > SEnvir.Now.AddSeconds(-5)
                    && ReferenceEquals(member.GroupAssistTarget, monster))
                    return true;
            }

            return false;
        }

        private static bool IsBotTargetWithinGroupLeaderLeash(PlayerObject player, PlayerObject groupLeader, MapObject target)
        {
            if (player == null || groupLeader == null || target == null)
                return true;

            if (groupLeader.CurrentMap == null || target.CurrentMap != groupLeader.CurrentMap)
                return false;

            if (target.Race != ObjectType.Monster)
                return true;

            MonsterObject monster = target as MonsterObject;
            if (monster == null)
                return true;

            if (IsBotGroupFocusedMonster(player, monster))
                return true;

            return MaxChebyshevDistance(groupLeader.CurrentLocation, monster.CurrentLocation) <= BotGroupTargetLeashRange;
        }

        private static BotProgressionStage GetBotProgressionStage(PlayerObject player)
        {
            int level = player?.Level ?? 0;
            if (level < 10) return BotProgressionStage.SafeNursery;
            if (level < 20) return BotProgressionStage.TownOutskirts;
            if (level < 40) return BotProgressionStage.MixedLevelAndBooks;
            if (level < 50) return BotProgressionStage.LevelRush;
            if (level < 60) return BotProgressionStage.HighBookFarm;
            return BotProgressionStage.LateLevelRush;
        }

        private static string[] GetBotPreferredMonsterKeywords(PlayerObject player)
        {
            switch (GetBotProgressionStage(player))
            {
                case BotProgressionStage.SafeNursery:
                    return BotSafeNurseryMonsterKeywords;
                case BotProgressionStage.TownOutskirts:
                    return BotTownOutskirtsMonsterKeywords;
                default:
                    return null;
            }
        }

        private static bool IsBotMonsterNameMatch(string monsterName, string[] keywords)
        {
            if (string.IsNullOrWhiteSpace(monsterName) || keywords == null) return false;

            foreach (string keyword in keywords)
            {
                if (!string.IsNullOrWhiteSpace(keyword)
                    && monsterName.IndexOf(keyword, StringComparison.OrdinalIgnoreCase) >= 0)
                    return true;
            }

            return false;
        }

        private static int GetBotProgressionMonsterScore(PlayerObject player, MonsterObject monster)
        {
            if (player == null || monster?.MonsterInfo == null) return 0;

            if (TryGetBotPriorityMissingSkills(player, out List<MagicInfo> missingSkills))
            {
                int missingSkillScore = GetBotMissingSkillMonsterDropScore(player, monster.MonsterInfo, missingSkills);
                if (missingSkillScore > 0)
                    return 2_000_000 + missingSkillScore * 2;
            }

            switch (GetBotProgressionStage(player))
            {
                case BotProgressionStage.SafeNursery:
                {
                    bool preferred = IsBotMonsterNameMatch(monster.MonsterInfo.MonsterName, BotSafeNurseryMonsterKeywords);
                    int bonus = preferred ? 1_200_000 : 0;
                    if (!preferred && monster.Level <= 8) bonus += 120_000;
                    if (player.CurrentMap?.HasSafeZone == true) bonus += 180_000;
                    bonus -= Math.Max(0, monster.Level - Math.Max(4, player.Level + 1)) * 150_000;
                    return bonus;
                }
                case BotProgressionStage.TownOutskirts:
                {
                    bool preferred = IsBotMonsterNameMatch(monster.MonsterInfo.MonsterName, BotTownOutskirtsMonsterKeywords);
                    int bonus = preferred ? 900_000 : 0;
                    if (!preferred && player.CurrentMap?.HasSafeZone == true && monster.Level <= 20) bonus += 160_000;
                    if (IsBotMonsterNameMatch(monster.MonsterInfo.MonsterName, BotSafeNurseryMonsterKeywords)) bonus += 80_000;
                    bonus -= Math.Max(0, monster.Level - Math.Max(12, player.Level + 2)) * 90_000;
                    return bonus;
                }
                default:
                    return 0;
            }
        }

        private static MonsterObject FindBestBotVisibleMonsterTarget(PlayerObject player, int maxDistance, bool preferGroupFocus)
        {
            if (player?.VisibleObjects == null) return null;

            GetBotGroupLeaderContext(player, out PlayerObject groupLeader, out bool _);
            bool restrictToLeader = groupLeader != null && groupLeader.CurrentMap == player.CurrentMap;

            MonsterObject bestTarget = null;
            long bestScore = long.MinValue;

            foreach (MapObject ob in player.VisibleObjects)
            {
                MonsterObject monster = ob as MonsterObject;
                if (!IsValidBotSweepMonster(player, monster, maxDistance)) continue;
                if (restrictToLeader && !IsBotTargetWithinGroupLeaderLeash(player, groupLeader, monster)) continue;

                int distance = MaxChebyshevDistance(player.CurrentLocation, monster.CurrentLocation);
                int maxHP = Math.Max(1, monster.Stats[Stat.Health]);
                int hpPct = monster.CurrentHP * 100 / maxHP;

                long score = GetBotProgressionMonsterScore(player, monster);
                if (preferGroupFocus && IsBotGroupFocusedMonster(player, monster))
                    score += 2_000_000L;

                score += GetBotProfileTargetScoreAdjustment(player, monster, distance);
                score -= distance * 10_000L;

                // ★ 优化：血量越少，优先级越高
                // 使用平方函数让血量少的目标优先级更高
                score -= hpPct * 200L;  // 从 100 提升到 200
                score -= monster.CurrentHP;

                // ★ 新增：威胁评估
                // 距离越近 + 血量越少 = 威胁越高，优先消灭
                double threatScore = CalculateBotTargetThreatScore(player, monster, distance, hpPct);
                score += (long)(threatScore * 500_000L);

                if (score > bestScore)
                {
                    bestScore = score;
                    bestTarget = monster;
                }
            }

            return bestTarget;
        }

        private static bool IsValidBotProactiveHumanTarget(PlayerObject player, PlayerObject target)
        {
            if (player == null || target == null || player.Node == null
                || target == player || target.Node == null || target.Dead || !target.Visible
                || target.Observer || player.CurrentMap == null || target.CurrentMap != player.CurrentMap
                || !Functions.InRange(player.CurrentLocation, target.CurrentLocation, Config.MaxViewRange))
                return false;

            if (player.InSafeZone || target.InSafeZone)
                return false;

            if (player.CurrentMap.Info?.Fight == FightSetting.Safe
                || target.CurrentMap.Info?.Fight == FightSetting.Safe)
                return false;

            return !target.IsBot && !player.InGroup(target) && !player.InGuild(target)
                && player.CanAttackTarget(target);
        }

        private static PlayerObject FindNearestBotProactiveHumanTarget(PlayerObject player)
        {
            if (player == null)
                return null;
            if (Config.BotProactivePvpMinLevel > 0 && player.Level < Config.BotProactivePvpMinLevel)
                return null;

            PlayerObject bestTarget = null;
            int bestDistance = int.MaxValue;

            foreach (PlayerObject target in SEnvir.Players)
            {
                if (!IsValidBotProactiveHumanTarget(player, target))
                    continue;

                int distance = MaxChebyshevDistance(player.CurrentLocation, target.CurrentLocation);
                if (bestTarget != null
                    && (distance > bestDistance
                        || (distance == bestDistance && target.ObjectID >= bestTarget.ObjectID)))
                    continue;

                bestTarget = target;
                bestDistance = distance;
            }

            return bestTarget;
        }

        private static bool HasBotNearbySweepMonster(PlayerObject player, int maxDistance = BotNearbyMonsterSweepRange)
        {
            return FindBestBotVisibleMonsterTarget(player, maxDistance, false) != null;
        }

        private static bool IsValidBotPickupTarget(PlayerObject player, ItemObject item)
        {
            return player != null
                   && item != null
                   && item.Node != null
                   && item.CurrentMap == player.CurrentMap
                   && Functions.InRange(player.CurrentLocation, item.CurrentLocation, Config.MaxViewRange)
                   && CanBotScanDrop(player, item);
        }

        private static bool IsBotPickupLocationBlocked(PlayerObject player, ItemObject item)
        {
            if (player == null || item?.Node == null || item.CurrentMap == null)
                return true;

            if (item.CurrentLocation == player.CurrentLocation)
                return false;

            Cell cell = item.CurrentMap.GetCell(item.CurrentLocation);
            if (cell?.Objects == null) return false;

            foreach (MapObject ob in cell.Objects)
            {
                if (ob == null || ob == item || ob == player || ob.Dead) continue;
                if (!ob.Blocking) continue;

                if (ob.Race == ObjectType.Monster)
                {
                    MonsterObject monster = (MonsterObject)ob;
                    if (monster.PetOwner == player) continue;
                }

                return true;
            }

            return false;
        }

        private static bool TryTeleportBotToPickupTarget(PlayerObject player, ItemObject item)
        {
            if (!IsValidBotPickupTarget(player, item) || IsBotPickupLocationBlocked(player, item))
                return false;

            if (item.CurrentLocation == player.CurrentLocation)
                return true;

            if (!player.Teleport(player.CurrentMap, item.CurrentLocation))
                return false;

            uint pid = player.ObjectID;
            DateTime now = SEnvir.Now;
            _botLastAttackTime[pid] = now;
            _botLastSnapPos[pid] = player.CurrentLocation;
            _botLastSnapTime[pid] = now;
            return true;
        }

        private static bool TryGetNearestBotPickableDrop(PlayerObject player, out ItemObject targetItem, int maxDistance)
        {
            targetItem = null;
            if (player?.VisibleObjects == null) return false;

            int bestDist = int.MaxValue;
            bool bestIsValidHorn = false;
            foreach (MapObject ob in player.VisibleObjects)
            {
                if (ob?.Node == null || ob.Race != ObjectType.Item) continue;

                ItemObject item = (ItemObject)ob;
                if (!IsValidBotPickupTarget(player, item)) continue;
                if (IsBotPickupLocationBlocked(player, item)) continue;

                int distance = Functions.Distance(ob.CurrentLocation, player.CurrentLocation);
                if (distance > maxDistance) continue;

                bool isValidHorn = IsValidUmaKingHornForConquest(item.Item);
                if (targetItem != null)
                {
                    if (!isValidHorn && bestIsValidHorn)
                        continue;

                    if (isValidHorn == bestIsValidHorn && distance >= bestDist)
                        continue;
                }


                bestDist = distance;
                bestIsValidHorn = isValidHorn;
                targetItem = item;
            }

            return targetItem != null;
        }


        private static bool ShouldBotPrioritizeEmergencyPickup(PlayerObject player, out ItemObject targetItem)
        {
            targetItem = null;
            if (!ShouldBotEmergencyGoldFarm(player)) return false;

            if (_botTargetItems.TryGetValue(player.ObjectID, out ItemObject lockedItem)
                && IsValidBotPickupTarget(player, lockedItem)
                && Functions.Distance(player.CurrentLocation, lockedItem.CurrentLocation) <= BotEmergencyGoldFarmPickupRadius)
            {
                targetItem = lockedItem;
                return true;
            }

            if (!TryGetNearestBotPickableDrop(player, out targetItem, BotEmergencyGoldFarmPickupRadius))
                return false;

            _botTargetItems[player.ObjectID] = targetItem;
            return true;
        }

        private static bool IsBotCombatAction(Server.Models.ActionType actionType)
        {
            switch (actionType)
            {
                case Server.Models.ActionType.Attack:
                case Server.Models.ActionType.Magic:
                case Server.Models.ActionType.RangeAttack:
                case Server.Models.ActionType.DelayAttack:
                case Server.Models.ActionType.DelayMagic:
                case Server.Models.ActionType.AttackDelay:
                case Server.Models.ActionType.DelayedAttackDamage:
                case Server.Models.ActionType.DelayedMagicDamage:
                    return true;
                default:
                    return false;
            }
        }

        private static void ClearBotPendingCombatActions(PlayerObject player)
        {
            if (player?.ActionList == null || player.ActionList.Count == 0) return;

            bool removedAny = false;
            for (int i = player.ActionList.Count - 1; i >= 0; i--)
            {
                DelayedAction action = player.ActionList[i];
                if (action == null || !IsBotCombatAction(action.Type)) continue;

                player.ActionList.RemoveAt(i);
                removedAny = true;
            }

            if (removedAny)
                player.PacketWaiting = false;
        }

        /// <summary>
        /// 根据当前场景动态更新假人的攻击模式
        /// </summary>
        private static void UpdateBotAttackMode(PlayerObject player, bool allowImmediateEscape = true)
        {
            if (player == null) return;

            uint pid = player.ObjectID;

            // 1. 检查是否在攻城战中
            var war = SEnvir.ConquestWars.FirstOrDefault(w => w.Map == player.CurrentMap && w.IsWaring);
            if (war != null)
            {
                player.AttackMode = AttackMode.Guild;
                return;
            }

            if (Config.BotAttackPlayers
                && _botTargets.TryGetValue(pid, out MapObject trackedTarget)
                && trackedTarget != null
                && trackedTarget.Race == ObjectType.Player
                && trackedTarget is PlayerObject proactiveTarget
                && IsValidBotProactiveHumanTarget(player, proactiveTarget))
            {
                player.AttackMode = AttackMode.All;
                return;
            }

            // 2. 检查被攻击情况（最近10秒内）
            if (_botLastAttackedTime.TryGetValue(pid, out DateTime lastAttackedTime)
                && (SEnvir.Now - lastAttackedTime).TotalSeconds <= 10)
            {
                if (_botLastAttackers.TryGetValue(pid, out List<uint> attackers) && attackers != null && attackers.Count > 0)
                {
                    // 过滤掉已死亡或不存在的攻击者
                    attackers.RemoveAll(attackerId =>
                    {
                        var obj = GetBotObject(attackerId);
                        return obj == null || obj.Dead;
                    });

                // 3. 检查是否在安全区
                if (!IsSafeZone(player))
                {
                    // 4. 被单个真人攻击：全体模式
                    if (attackers.Count == 1)
                    {
                        player.AttackMode = AttackMode.All;
                        return;
                    }

                    // 5. 被多个真人攻击：行会模式，检查附近是否有同行会的人
                    if (attackers.Count > 1)
                    {
                        player.AttackMode = AttackMode.Guild;

                        // 检查附近是否有同行会的真人或假人
                        if (allowImmediateEscape && !HasNearbyGuildMember(player))
                        {
                            // 没有同行会的人，逃跑
                            TriggerBotEmergencyEscape(player);
                        }
                        return;
                    }
                }
            }
            }

            // 6. 检查是否有队伍
            if (player.GroupMembers != null && player.GroupMembers.Count > 1)
            {
                player.AttackMode = AttackMode.Group;
                return;
            }

            // 7. 默认：无组队自己打怪，和平模式
            player.AttackMode = AttackMode.Peace;
        }

        /// <summary>
        /// 检查玩家是否在安全区
        /// </summary>
        private static bool IsSafeZone(PlayerObject player)
        {
            if (player == null) return false;

            Cell cell = player.CurrentMap?.GetCell(player.CurrentLocation);
            return cell?.SafeZone != null;
        }

        /// <summary>
        /// 根据ObjectID获取地图对象
        /// </summary>
    private static MapObject GetBotObject(uint objectId)
    {
        // 通过 SEnvir.Players 集合查找对应的对象
        return SEnvir.Players.FirstOrDefault(p => p?.ObjectID == objectId);
    }

        /// <summary>
        /// 检查假人附近是否有同行会的成员
        /// </summary>
        private static bool HasNearbyGuildMember(PlayerObject player)
        {
            if (player == null) return false;

            GuildInfo guild = player.Character?.Account?.GuildMember?.Guild;
            if (guild == null) return false;

            int range = 15; // 搜索范围

            foreach (MapObject obj in player.CurrentMap.Objects)
            {
                if (obj == null || obj.Dead || obj.Race != ObjectType.Player) continue;

                PlayerObject otherPlayer = (PlayerObject)obj;
                if (ReferenceEquals(otherPlayer, player)) continue;
                GuildInfo otherGuild = otherPlayer.Character?.Account?.GuildMember?.Guild;
                if (otherGuild != guild) continue;

                int dx = player.CurrentLocation.X - otherPlayer.CurrentLocation.X;
                int dy = player.CurrentLocation.Y - otherPlayer.CurrentLocation.Y;
                if (dx * dx + dy * dy <= range * range)
                {
                    return true;
                }
            }

            return false;
        }

        /// <summary>
        /// 触发假人紧急逃跑（被多人攻击且无同行会人时）。
        /// 通过 BotPvPStrategy 强制切换为逃跑策略，并立即执行一步逃跑移动。
        /// </summary>
        private static void TriggerBotEmergencyEscape(PlayerObject player)
        {
            if (player == null) return;

            uint pid = player.ObjectID;

            // 清除当前目标，避免继续黏住敌人
            ClearBotTargetLockState(pid);
            ClearBotPendingCombatActions(player);

            // 强制切换为逃跑策略
            BotPvPStrategy.ForceFlee(pid);

            // 立即执行一次逃跑决策（计算最优逃跑方向并移动）
            BotPvPStrategy.PvPStrategyDecision decision = BotPvPStrategy.EvaluateAndDecide(player);
            if (decision.Action == BotPvPStrategy.PvPAction.Flee)
            {
                TryMoveBotAlongDirection(player, decision.FleeDir, 2, out _, out _);
            }
            else
            {
                // 没有威胁记录时，向随机方向逃跑
                MirDirection randomDir = (MirDirection)SEnvir.Random.Next(8);
                TryMoveBotAlongDirection(player, randomDir, 2, out _, out _);
            }
        }

        /// <summary>
        /// 记录假人被攻击的攻击者，同时上报给 PVP 策略系统。
        /// </summary>
        private static void OnBotPvPDamaged(PlayerObject player, PlayerObject attacker, int damage)
        {
            if (!isRunning || player == null || attacker == null || !player.IsBot) return;
            if (player.Node == null || player.Dead || attacker.Node == null || attacker.Dead) return;
            if (player.CurrentMap != attacker.CurrentMap) return;
            if (!Functions.InRange(player.CurrentLocation, attacker.CurrentLocation, Config.MaxViewRange)) return;

            try
            {
                RecordBotAttacker(player, attacker, damage, false);
            }
            catch (Exception ex)
            {
                SEnvir.Log($"假人受击记录异常 [{player.Name}]: {ex.Message}");
            }
        }

        private static void RecordBotAttacker(PlayerObject player, PlayerObject attacker, int damage = 1,
            bool allowImmediateEscape = true)
        {
            if (player == null || attacker == null) return;

            uint pid = player.ObjectID;
            uint attackerId = attacker.ObjectID;

            // 上报给 PVP 策略系统
            BotPvPStrategy.RecordPvPDamage(pid, attackerId, Math.Max(1, damage));

            // 社交记忆：记录被攻击
            BotSocialMemory.RecordAttacked(player, attacker, damage);

            // 记录最后被攻击时间
            _botLastAttackedTime[pid] = SEnvir.Now;

            // 添加到攻击者列表
            if (!_botLastAttackers.TryGetValue(pid, out List<uint> attackers))
            {
                attackers = new List<uint>();
                _botLastAttackers[pid] = attackers;
            }

            // 避免重复记录同一个攻击者
            if (!attackers.Contains(attackerId))
            {
                attackers.Add(attackerId);
            }

            // 更新攻击模式
            UpdateBotAttackMode(player, allowImmediateEscape);
        }

        /// <summary>
        /// 清理过期的攻击者记录（超过30秒的记录）
        /// </summary>
        private static void CleanupBotAttackerRecords()
        {
            DateTime expireTime = SEnvir.Now.AddSeconds(-30);

            List<uint> toRemove = new List<uint>();
            foreach (var kvp in _botLastAttackedTime)
            {
                if (kvp.Value < expireTime)
                {
                    toRemove.Add(kvp.Key);
                }
            }

            foreach (uint pid in toRemove)
            {
                _botLastAttackedTime.Remove(pid);
                _botLastAttackers.Remove(pid);
            }
        }

        private static MapObject ResolveBotGroupHostileTarget(PlayerObject player, MapObject target)
        {
            if (player == null || target == null || target.Node == null || target.Dead) return null;

            switch (target.Race)
            {
                case ObjectType.Player:
                    return player.CanAttackTarget(target) ? target : null;
                case ObjectType.Monster:
                    MonsterObject monster = (MonsterObject)target;
                    if (monster.PetOwner != null
                        && monster.PetOwner != player
                        && monster.PetOwner.Node != null
                        && !monster.PetOwner.Dead
                        && player.CanAttackTarget(monster.PetOwner))
                        return monster.PetOwner;

                    return player.CanAttackTarget(monster) ? monster : null;
                default:
                    return null;
            }
        }

        private static MapObject SelectHumanLeaderAssistTarget(PlayerObject player, PlayerObject leader)
        {
            if (player == null || leader?.Node == null || leader.Dead) return null;

            MapObject directTarget = null;
            if (leader.GroupAssistTargetTime > SEnvir.Now.AddSeconds(-5))
                directTarget = ResolveBotGroupHostileTarget(player, leader.GroupAssistTarget);

            if (IsValidBotAssistTarget(player, directTarget))
                return directTarget;

            MonsterObject bestTarget = null;
            long bestScore = long.MinValue;

            foreach (MonsterObject tagged in leader.TaggedMonsters)
            {
                if (!IsValidBotAssistTarget(player, tagged)) continue;

                int leaderDist = MaxChebyshevDistance(leader.CurrentLocation, tagged.CurrentLocation);
                int playerDist = MaxChebyshevDistance(player.CurrentLocation, tagged.CurrentLocation);
                int maxMobHP = Math.Max(1, tagged.Stats[Stat.Health]);
                int mobHpPct = tagged.CurrentHP * 100 / maxMobHP;

                long score = 0;
                if (IsBotGroupSharedTarget(player, tagged.Target)) score += 2000000L;
                score += (100 - mobHpPct) * 1000L;
                score -= leaderDist * 100L;
                score -= playerDist * 10L;

                if (score > bestScore)
                {
                    bestScore = score;
                    bestTarget = tagged;
                }
            }

            return bestTarget;
        }

        private static MapObject GetBotGroupAssistTarget(PlayerObject player, PlayerObject groupLeader, bool hasHumanLeader)
        {
            if (!Config.BotAllowGroup || player == null || groupLeader?.Node == null || groupLeader.Dead)
                return null;

            if (player.GroupMembers == null)
                return null;

            foreach (PlayerObject member in player.GroupMembers)
            {
                if (member == null || member == player || member.Node == null || member.Dead) continue;

                MapObject memberTarget = null;
                if (_botTargets.TryGetValue(member.ObjectID, out MapObject trackedTarget))
                    memberTarget = ResolveBotGroupHostileTarget(player, trackedTarget);

                if (memberTarget == null && !botPlayers.Contains(member))
                    memberTarget = SelectHumanLeaderAssistTarget(player, member);

                if (IsValidBotAssistTarget(player, memberTarget))
                    return memberTarget;
            }

            if (hasHumanLeader)
                return SelectHumanLeaderAssistTarget(player, groupLeader);

            return null;
        }

        private static bool HasBotRecoveryPotionStock(PlayerObject player, int missingHP, int missingMP)
        {
            if (player?.Inventory == null) return false;

            foreach (UserItem item in player.Inventory)
            {
                if (item?.Info == null) continue;
                if (IsBotPotionBlockedByMap(player, item.Info)) continue;

                BotPotionKind kind = GetBotPotionKind(item, out int hpRestore, out int mpRestore);
                if (kind == BotPotionKind.None) continue;
                if (missingHP > 0 && hpRestore > 0) return true;
                if (missingMP > 0 && mpRestore > 0) return true;
            }

            return false;
        }

        private static bool TryProcessBotRoundRecovery(PlayerObject player)
        {
            if (player == null || player.Dead || player.Node == null) return false;
            if (HasBotNearbySweepMonster(player)) return false;

            int maxHP = player.Stats[Stat.Health];
            int maxMP = player.Stats[Stat.Mana];
            int missingHP = maxHP > 0 ? Math.Max(0, maxHP - player.CurrentHP) : 0;
            int missingMP = maxMP > 0 ? Math.Max(0, maxMP - player.CurrentMP) : 0;
            if (missingHP <= 0 && missingMP <= 0)
                return false;

            ProcessBotPotionMonitor(player, true);

            int fullThreshold = Math.Max(0, Math.Min(100, Config.BotFullHealthThresholdPercent));
            bool fullHP = maxHP <= 0 || player.CurrentHP * 100L >= maxHP * (long)fullThreshold;
            bool fullMP = maxMP <= 0 || player.CurrentMP * 100L >= maxMP * (long)fullThreshold;
            if (fullHP && fullMP)
                return false;

            bool hasRecoveryPotion = HasBotRecoveryPotionStock(player, missingHP, missingMP);
            bool waitingPotionCooldown = _botPotionCooldownTime.TryGetValue(player.ObjectID, out DateTime cooldownUntil)
                                       && SEnvir.Now < cooldownUntil;

            return hasRecoveryPotion || waitingPotionCooldown;
        }

        private static bool TryStabilizeBotLowHpWithPotion(PlayerObject player, long hpPct)
        {
            if (player == null || player.Dead || player.Node == null) return false;
            if (hpPct <= BotPotionEmergencyHpPct) return false;

            int maxHP = player.Stats[Stat.Health];
            int maxMP = player.Stats[Stat.Mana];
            int missingHP = maxHP > 0 ? Math.Max(0, maxHP - player.CurrentHP) : 0;
            int missingMP = maxMP > 0 ? Math.Max(0, maxMP - player.CurrentMP) : 0;
            if (missingHP <= 0 && missingMP <= 0) return false;

            if (ProcessBotPotionMonitor(player, true))
                return true;

            bool hasRecoveryPotion = HasBotRecoveryPotionStock(player, missingHP, missingMP);
            bool waitingPotionCooldown = _botPotionCooldownTime.TryGetValue(player.ObjectID, out DateTime cooldownUntil)
                                       && SEnvir.Now < cooldownUntil;

            return hasRecoveryPotion && waitingPotionCooldown;
        }

        /// <summary>
        /// AI 战斗主循环，参考真人客户端自动打怪逻辑：
        ///
        ///   Step 1. 安全区检测 → BFS找最近出口 → Teleport传送出去（不战斗）
        ///   Step 2. 刷新视野（RemoveAllObjects / AddAllObjects）
        ///   Step 3. 维持锁定目标（失效：死亡 / Node=null / 超视野 / 切怪超时）
        ///   Step 4. 无目标时从视野内重新选最近野怪（欧氏距离²排序，仿真人 SelectMonster）
        ///   Step 5. dist==1 且 CanAttack → 攻击；dist>1 → 绕障追击（仿真人 DirectionBest）
        ///   Step 6. 无目标 → 漫游（仿真人 pathfindertime，定时换向而非每Tick随机）
        ///
        /// ★ 攻击必须用 Attack(MirDirection, MagicType) 而非 Attack(MapObject,...)：
        ///   前者走完整流程：Direction → ActionTime/AttackTime → AttackLocation（真正伤害）
        ///   → Broadcast(S.ObjectAttack)（真人客户端看到动画）
        /// </summary>
        private static bool ShouldRecallBotForCriticalHealth(PlayerObject player)
        {
            int maxHP = player?.Stats?[Stat.Health] ?? 0;
            return maxHP > 0 && player.CurrentHP * 100L / maxHP < BotCriticalRecallHpPct;
        }

        private static bool TryRecallBotForCriticalHealth(PlayerObject player)
        {
            if (player?.Node == null || player.Dead) return false;

            Map homeMap = SEnvir.GetMap(BotHomeMapIndex);
            if (homeMap == null) return false;

            Point dest = homeMap.GetRandomLocation(BotHomePoint, 15, 50);
            if (dest == Point.Empty) dest = BotHomePoint;

            try
            {
                if (!player.Teleport(homeMap, dest))
                    return false;
            }
            catch (Exception)
            {
                return false;
            }

            uint pid = player.ObjectID;
            DateTime now = SEnvir.Now;
            DateTime restUntil = now.AddSeconds(BotRecallRestSeconds);
            _botRecallUntil[pid] = restUntil;
            ClearBotPendingCombatActions(player);
            ClearBotCombatTrackingState(pid);
            _botTargetItems.Remove(pid);
            _botWaitingPickup.Remove(pid);
            _botKiteMode.Remove(pid);
            ClearBotUpcomingHighBossGroupTarget(player);
            ClearBotSiegeState(pid);
            _botLastAttackTime[pid] = now;
            _botMapEvalTime[pid] = restUntil;
            ResetBotMapStayState(player, homeMap, now);
            RecordBotMapSwitch(player, homeMap);
            return true;
        }

        private static bool TryProcessBotRecallRecovery(PlayerObject player)
        {
            if (player == null || player.Dead || player.Node == null) return false;

            uint pid = player.ObjectID;
            if (_botRecallUntil.TryGetValue(pid, out DateTime recallUntil))
            {
                if (SEnvir.Now < recallUntil)
                {
                    ProcessBotReplenishSupplies(player);

                    int maxHP = player.Stats[Stat.Health];
                    if (maxHP > 0 && player.CurrentHP < maxHP)
                        return true;

                    _botRecallUntil.Remove(pid);
                    return true;
                }

                _botRecallUntil.Remove(pid);
            }

            if (ShouldRecallBotForCriticalHealth(player) && TryRecallBotForCriticalHealth(player))
                return true;

            return false;
        }

        private static void ProcessBotCombat(PlayerObject player)
        {
            if (player == null || player.Dead || player.Node == null)
                return;
            if (!Config.BotAutoLevel && !Config.BotAttackPlayers && !Config.BotPvpRetaliation)
                return;

            if (!Config.BotAutoPickup)
            {
                _botWaitingPickup.Remove(player.ObjectID);
                _botTargetItems.Remove(player.ObjectID);
            }

            // ── Step 0：定期清理过期的攻击者记录（每3秒）──────
            if (_botRandom.Next(100) < 10) // 10% 的概率清理，约每30秒清理一次
            {
                CleanupBotAttackerRecords();
            }

            EnsureBotTelemetryMapContext(player);
            ObserveBotTelemetry(player);

            GetBotGroupLeaderContext(player, out PlayerObject groupLeader, out bool hasHumanLeader);

            bool isGroupedFollower = groupLeader != null;
            bool isBotLeaderWithFollowers = !isGroupedFollower && player.GroupMembers != null && player.GroupMembers.Count > 1;

            // ── Step 0：定期评估当前地图是否适合（每 BotMapEvalInterval 秒一次）──────
            // 除了危险地图过滤外，金币不足时也会切去更稳、更容易卖杂物的打金图。
            {
                uint pid = player.ObjectID;
                DateTime now = SEnvir.Now;
                GetBotGoldFarmContext(player, out bool goldFarmMode, out bool emergencyGoldFarmMode);
                DateTime staySince = now;
                bool forceRotateLowTierFarm = !isGroupedFollower && ShouldForceRotateBotFarmMap(player, now, out staySince);
                bool forceLeaveTownBigMap = !isGroupedFollower
                                            && ShouldBotAvoidTownBigMap(player, goldFarmMode)
                                            && IsBotTownBigMap(player.CurrentMap);
                int mapEvalInterval = goldFarmMode ? BotGoldFarmMapEvalInterval : BotMapEvalInterval;
                bool needEval = Config.BotAutoLevel
                                && Config.BotAutoMapSwitch
                                && ShouldTriggerScaledBehavior(Config.BotActivityPercent, pid,
                                    now.Ticks / TimeSpan.TicksPerSecond)
                                && (forceRotateLowTierFarm
                                || forceLeaveTownBigMap
                                || !_botMapEvalTime.TryGetValue(pid, out DateTime nextEval)
                                || now >= nextEval);
                if (needEval)
                {
                    _botMapEvalTime[pid] = now.AddSeconds(mapEvalInterval);

                    // 队员跟队时不再自己评估切图，统一由队长带图，避免刚贴队又被单独地图评分拉走。
                    if (!isGroupedFollower)
                    {
                        int currentAvgLv;
                        int currentDanger;
                        int currentScore = GetBotMapScore(player.CurrentMap, player, goldFarmMode, emergencyGoldFarmMode, out currentAvgLv, out currentDanger);

                        var (newMap, dest) = FindSuitableMapForBot(player, goldFarmMode, emergencyGoldFarmMode, forceRotateLowTierFarm);
                        if (newMap != null)
                        {
                            int bestAvgLv;
                            int bestDanger;
                            int bestScore = GetBotMapScore(newMap, player, goldFarmMode, emergencyGoldFarmMode, out bestAvgLv, out bestDanger);

                            bool shouldSwitchMap = currentScore == int.MinValue || forceRotateLowTierFarm;
                            int switchMargin = emergencyGoldFarmMode
                                ? BotEmergencyGoldFarmSwitchMargin
                                : goldFarmMode
                                    ? BotGoldFarmSwitchMargin
                                    : 25;
                            if (!shouldSwitchMap && goldFarmMode && bestScore > currentScore + switchMargin)
                                shouldSwitchMap = true;

                            if (!shouldSwitchMap && !goldFarmMode && player.Level >= 40 && bestScore > currentScore + switchMargin)
                                shouldSwitchMap = true;

                            if (!shouldSwitchMap && emergencyGoldFarmMode && currentAvgLv >= 0 && bestAvgLv >= 0 && bestAvgLv < currentAvgLv)
                                shouldSwitchMap = true;

                            bool shouldPreheatHighBoss = ShouldBotPreheatUpcomingHighBossMap(player, newMap, currentScore, bestScore, switchMargin, shouldSwitchMap || forceRotateLowTierFarm);
                            if (shouldPreheatHighBoss)
                            {
                                SetBotUpcomingHighBossGroupTarget(player, newMap);

                                if (!shouldSwitchMap)
                                    TryPrepareBotFullGroupForUpcomingHighBossMap(player, newMap);
                            }
                            else
                            {
                                ClearBotUpcomingHighBossGroupTarget(player);
                            }

                            if (shouldSwitchMap && IsBotHighLevelBossMap(newMap)
                                && !TryPrepareBotFullGroupForUpcomingHighBossMap(player, newMap))
                            {
                                _botMapEvalTime[pid] = now.AddSeconds(5);
                                shouldSwitchMap = false;
                            }

                            if (shouldSwitchMap)
                            {
                                string reason = currentScore == int.MinValue
                                    ? $"当前地图 [{player.CurrentMap?.Info?.Description}]（怪物均级={currentAvgLv}）不适合"
                                    : forceRotateLowTierFarm
                                        ? $"当前地图 [{player.CurrentMap?.Info?.Description}] 已连续驻留 {(int)(now - staySince).TotalMinutes} 分钟，切去其它低阶收益图轮刷"
                                        : emergencyGoldFarmMode
                                            ? "金币=0且背包无药，切去更安全的单刷打金图"
                                            : $"金币偏低（{player.Gold}），切去掉落卖店收益更好的打金图";

                                if (!player.Teleport(newMap, dest))
                                    return;

                                RecordBotMapSwitch(player, newMap);
                                ClearBotUpcomingHighBossGroupTarget(player);
                                ResetBotMapStayState(player, newMap, now);

                                ClearBotCombatTrackingState(pid);
                            _botLastAttackTime[pid] = now;
                            _botMapEvalTime[pid] = now.AddSeconds(mapEvalInterval);
                            return;
                            }
                        }
                        else
                        {
                            ClearBotUpcomingHighBossGroupTarget(player);
                        }
                    }
                }
            }

            // ── Step 1：安全区 → BFS找出口 → Teleport ──────────────────────
            if (player.InSafeZone && Config.BotAutoLevel && Config.BotAutoMapSwitch)
            {
                Point exit = FindNearestNonSafeCell(player.CurrentMap, player.CurrentLocation, 50);
                if (exit != Point.Empty)
                    player.Teleport(player.CurrentMap, exit);
                return;
            }

            // ── Step 1b：卡死检测 → 随机传送 ────────────────────────────────
            // 条件：距上次攻击超过 BotStuckAttackTimeout 秒，同时在 BotStuckCheckInterval
            //       内的位移 ≤ BotStuckMinMoveRange（不动 或 在小区间循环）
            {
                DateTime now = SEnvir.Now;
                uint pid = player.ObjectID;

                // 队员跟队时不再用“长时间没打到怪”判定自己卡死换图，
                // 否则真人/队长一停手，队员很容易误判后自己乱飞乱串图。
                if (isGroupedFollower)
                {
                    _botLastAttackTime[pid] = now;
                    _botLastSnapPos[pid] = player.CurrentLocation;
                    _botLastSnapTime[pid] = now;
                }
                else
                {
                    // 初始化攻击时间（首次进来先记录当前时间，避免一上线就传送）
                    if (!_botLastAttackTime.ContainsKey(pid))
                        _botLastAttackTime[pid] = now;

                    // 坐标快照：每隔 BotStuckCheckInterval 秒记录一次
                    if (!_botLastSnapTime.TryGetValue(pid, out DateTime snapTime)
                        || (now - snapTime).TotalSeconds >= BotStuckCheckInterval)
                    {
                        // 判断本轮快照与上次快照之间的位移是否"有效"
                        bool effectivelyMoved = false;
                        if (_botLastSnapPos.TryGetValue(pid, out Point prevPos))
                        {
                            int moved = Math.Abs(player.CurrentLocation.X - prevPos.X)
                                      + Math.Abs(player.CurrentLocation.Y - prevPos.Y);
                            effectivelyMoved = moved > BotStuckMinMoveRange;
                        }

                        // 如果有效移动了，刷新攻击超时起点（说明假人没卡住，只是没怪可打）
                        if (effectivelyMoved)
                            _botLastAttackTime[pid] = now;

                        _botLastSnapPos[pid]  = player.CurrentLocation;
                        _botLastSnapTime[pid] = now;
                    }

                    // 超时判断：长时间无攻击 且 没有有效移动
                    bool stuckTooLong = (now - _botLastAttackTime[pid]).TotalSeconds >= BotStuckAttackTimeout;
                    if (stuckTooLong)
                    {
                        // ★ 卡死时：优先换一张合适的地图（等级匹配 + 无BOSS），
                        //   如果实在找不到合适地图，再退回到当前地图随机传送
                        var (newMap, dest) = FindSuitableMapForBot(player);
                        if (newMap != null && IsBotHighLevelBossMap(newMap))
                        {
                            SetBotUpcomingHighBossGroupTarget(player, newMap);

                            if (!TryPrepareBotFullGroupForUpcomingHighBossMap(player, newMap))
                            {
                                _botMapEvalTime[pid] = now.AddSeconds(5);
                                newMap = null;
                            }
                        }
                        else
                        {
                            ClearBotUpcomingHighBossGroupTarget(player);
                        }

                        if (newMap != null)
                        {
                            if (player.Teleport(newMap, dest))
                            {
                                RecordBotMapSwitch(player, newMap);
                                ClearBotUpcomingHighBossGroupTarget(player);
                            }
                        }

                        else
                        {
                            Point fallback = GetRandomWalkablePoint(player.CurrentMap);
                            if (fallback != Point.Empty)
                                player.Teleport(player.CurrentMap, fallback);
                        }
                        // 重置所有状态，让 AI 从头开始
                        _botLastAttackTime[pid] = now;
                        ClearBotCombatTrackingState(pid);
                        // 重置地图评估时间，新地图刚进去先等一个评估周期再评估。
                        GetBotGoldFarmContext(player, out bool stuckGoldFarmMode, out bool _);
                        _botMapEvalTime[pid] = now.AddSeconds(stuckGoldFarmMode ? BotGoldFarmMapEvalInterval : BotMapEvalInterval);
                        return; // 本 Tick 不做其他操作，等下一 Tick 重新扫怪
                    }

                    // ── 漂移卡死检测：2分钟内始终在5格以内且无攻击动作 → 原地图内飞远 ──
                    // 补充场景：假人有移动、不触发 stuckTooLong，但一直在小圈里打转（路被堵死、
                    // 被围住转圈等），此时按锚点检测是否长时间未离开指定范围。
                    if (!player.InSafeZone)
                    {
                        Point curPos = player.CurrentLocation;
                        bool hasAnchor = _botDriftAnchorPos.TryGetValue(pid, out Point anchor)
                            & _botDriftAnchorTime.TryGetValue(pid, out DateTime anchorTime);

                        int distFromAnchor = hasAnchor
                            ? Math.Abs(curPos.X - anchor.X) + Math.Abs(curPos.Y - anchor.Y)
                            : int.MaxValue;

                        if (!hasAnchor || distFromAnchor > BotDriftStuckRange)
                        {
                            // 离开了5格范围 → 刷新锚点，重新计时
                            _botDriftAnchorPos[pid]  = curPos;
                            _botDriftAnchorTime[pid] = now;
                        }
                        else if ((now - anchorTime).TotalSeconds >= BotDriftStuckTimeout)
                        {
                            // 2分钟内一直在锚点5格内 → 漂移卡死，在当前地图找一个10格以外的点飞过去
                            Point escape = GetWalkablePointFarFrom(player.CurrentMap, curPos, BotDriftEscapeMinDist);
                            if (escape == Point.Empty)
                                escape = GetRandomWalkablePoint(player.CurrentMap);
                            if (escape != Point.Empty)
                                player.Teleport(player.CurrentMap, escape);

                            // 重置漂移锚点和战斗状态
                            _botDriftAnchorPos[pid]  = player.CurrentLocation;
                            _botDriftAnchorTime[pid] = now;
                            _botLastAttackTime[pid]  = now;
                            ClearBotCombatTrackingState(pid);
                            return;
                        }
                    }
                }
            }

            // ── Step 1c：组队跟随已前置到 ProcessBotTeamModule ─────────────────
            // 这里不再重复处理，避免组队/战斗逻辑互相耦合。

            // ── Step 2：不再每 Tick 强制刷新视野 ────────────────────────────────
            // Move() / Teleport() 内部会自动调用 RemoveAllObjects/AddAllObjects
            // 每 Tick 强制刷会导致旁观者客户端看到假人每秒消失再出现（视觉闪烁）

            // ── Step 2b：等待拾取中 → 暂停攻击，交由 ProcessBotPickUp 处理 ────
            // 怪物死亡后进入等待拾取状态；超时兜底（BotPickupWaitTimeout秒）防止永久阻塞
            if (_botWaitingPickup.TryGetValue(player.ObjectID, out DateTime waitSince))
            {
                // ★ 智能：先主动检查视野内是否有“当前可到达”的可捡物品。
                //   若掉落点被活怪或其他阻挡物占住，就不继续傻等这一件，交给拾取模块改捡别的。
                bool hasReachablePickableItem = false;
                if ((SEnvir.Now - waitSince).TotalSeconds >= 0.8) // 至少等0.8s让物品落地
                {
                    hasReachablePickableItem = TryGetNearestBotPickableDrop(player, out _, Config.MaxViewRange);

                    if (!hasReachablePickableItem)
                    {
                        // 视野内没有当前可到达的可捡物品，立即解除等待
                        _botWaitingPickup.Remove(player.ObjectID);
                        // 继续向下执行攻击逻辑
                    }
                    else
                    {
                        return; // 有物品要捡，继续等待
                    }
                }
                else
                {
                    return; // 刚进入等待状态，稍等物品落地
                }

                // 超时兜底（通常走不到这里，但保留兜底逻辑）
                if (_botWaitingPickup.ContainsKey(player.ObjectID)
                    && (SEnvir.Now - waitSince).TotalSeconds >= BotPickupWaitTimeout)
                {
                    _botWaitingPickup.Remove(player.ObjectID);
                }
                else if (_botWaitingPickup.ContainsKey(player.ObjectID))
                {
                    return; // 还在超时等待期内
                }
            }

            if (ShouldBotPrioritizeEmergencyPickup(player, out _) && !HasBotImmediateCombatTarget(player))
            {
                ClearBotPendingCombatActions(player);
                player.PacketWaiting = false;
                return;
            }

            // ── Step 3：仇恨回转 + 维持/验证锁定目标 ────────────────────────────
            // ★ 既支持怪物仇恨回转，也支持真人 / 敌方宠物主人的 PK 回转。
            {
                MapObject hostileTarget = ResolveBotGroupHostileTarget(player, player.LastHitter);
                if (IsValidBotAssistTarget(player, hostileTarget))
                {
                    // 若仇恨来源是真人，上报给 PVP 策略系统
                    if (hostileTarget.Race == ObjectType.Player)
                        RecordBotAttacker(player, (PlayerObject)hostileTarget);

                    // 只在当前无目标、当前目标失效，或新仇恨目标更近 / 更优先为真人时切换
                    _botTargets.TryGetValue(player.ObjectID, out MapObject curTarget);
                    if (!IsValidBotAssistTarget(player, curTarget))
                    {
                        _botTargets[player.ObjectID] = hostileTarget;
                        _botTargetSwitchTime[player.ObjectID] = SEnvir.Now.AddSeconds(BotTargetSwitchTimeout);
                        _botRoamTime.Remove(player.ObjectID);
                    }
                    else
                    {
                        int hostileDist = MaxChebyshevDistance(player.CurrentLocation, hostileTarget.CurrentLocation);
                        int curDist = MaxChebyshevDistance(player.CurrentLocation, curTarget.CurrentLocation);
                        bool preferHostileTarget = hostileTarget.Race == ObjectType.Player && curTarget.Race != ObjectType.Player;

                        if (preferHostileTarget || hostileDist < curDist)
                        {
                            _botTargets[player.ObjectID] = hostileTarget;
                            _botTargetSwitchTime[player.ObjectID] = SEnvir.Now.AddSeconds(BotTargetSwitchTimeout);
                            _botRoamTime.Remove(player.ObjectID);
                        }
                    }
                }

                player.LastHitter = null; // 清除，避免重复处理
            }

            // ── Step 3b：PVP 策略执行（仇恨回转之后，目标验证之前）─────────────
            // 如果假人处于 PVP 威胁状态，优先执行 PVP 策略决策。
            if (!Config.BotPvpRetaliation)
                BotPvPStrategy.ClearPvPState(player.ObjectID);

            if (Config.BotPvpRetaliation && BotPvPStrategy.IsInPvPStrategy(player.ObjectID))
            {
                BotPvPStrategy.PvPStrategyDecision pvpDecision = BotPvPStrategy.EvaluateAndDecide(player);

                if (pvpDecision.Action == BotPvPStrategy.PvPAction.Flee)
                {
                    // 逃跑：持续向计算出的最优方向移动
                    ClearBotPendingCombatActions(player);
                    ClearBotTargetLockState(player.ObjectID);
                    _botKiteMode.Remove(player.ObjectID);
                    TryMoveBotAlongDirection(player, pvpDecision.FleeDir, 2, out _, out _);
                    return;
                }

                if (pvpDecision.Action == BotPvPStrategy.PvPAction.Retreat)
                {
                    // 后退（风筝模式）：先移动拉距离，下一帧再攻击
                    TryMoveBotAlongDirection(player, pvpDecision.FleeDir, 2, out _, out _);
                    // 标记风筝模式：战士不突进贴脸
                    _botKiteMode[player.ObjectID] = pvpDecision.NeedKiteSkill;
                    // 不 return，让后续逻辑继续（本帧移完如果还有 lockedTarget 会尝试攻击）
                }

                if (pvpDecision.Action == BotPvPStrategy.PvPAction.Attack && pvpDecision.Target != null
                    && pvpDecision.Target.Node != null && !pvpDecision.Target.Dead)
                {
                    // 覆盖锁定目标为 PVP 最优目标
                    _botTargets[player.ObjectID] = pvpDecision.Target;
                    _botTargetSwitchTime[player.ObjectID] = SEnvir.Now.AddSeconds(BotTargetSwitchTimeout);
                    _botRoamTime.Remove(player.ObjectID);
                    // 攻击模式下更新风筝标记
                    if (pvpDecision.Strategy == BotPvPStrategy.PvPStrategy.Kite)
                        _botKiteMode[player.ObjectID] = pvpDecision.NeedKiteSkill;
                    else
                        _botKiteMode.Remove(player.ObjectID);
                }

                // 无动作/无目标时清除风筝标记
                if (pvpDecision.Action == BotPvPStrategy.PvPAction.None)
                {
                    _botKiteMode.Remove(player.ObjectID);
                }
            }
            else
            {
                // 不在 PVP 策略中时清除风筝标记
                _botKiteMode.Remove(player.ObjectID);
            }

            // ── Step 3（原）：维持/验证锁定目标 ────────────────────────────────
            _botTargets.TryGetValue(player.ObjectID, out MapObject lockedTarget);
            if (lockedTarget?.Race == ObjectType.Player && (Config.BotAttackPlayers || Config.BotPvpRetaliation))
            {
                MonsterObject monster = FindBestBotVisibleMonsterTarget(player, Config.MaxViewRange, true);
                if (monster != null)
                {
                    lockedTarget = monster;
                    _botTargets[player.ObjectID] = monster;
                    _botTargetSwitchTime[player.ObjectID] = SEnvir.Now.AddSeconds(BotTargetSwitchTimeout);
                }
            }

            if (lockedTarget != null)
            {
                if (lockedTarget.Race == ObjectType.Player && Config.BotAttackPlayers)
                    UpdateBotAttackMode(player);

                bool switchTimeout = _botTargetSwitchTime.TryGetValue(player.ObjectID, out DateTime switchTime)
                                     && SEnvir.Now > switchTime;
                bool noRecentAttack = !_botLastAttackTime.TryGetValue(player.ObjectID, out DateTime lastAttackTime)
                                      || (SEnvir.Now - lastAttackTime).TotalSeconds >= BotTargetSwitchAttackGraceSeconds;
                bool targetEnded = lockedTarget.Dead || lockedTarget.Node == null;

                // ★ 新增：目标血量快速下降检测
                bool targetHealthDroppingFast = false;
                if (!switchTimeout && !targetEnded && lockedTarget.Race == ObjectType.Monster)
                {
                    targetHealthDroppingFast = IsTargetHealthDroppingFast(player.ObjectID, lockedTarget);
                }

                // 综合判断：目标血量快速下降时，即使超时也继续黏住
                bool shouldSwitch = switchTimeout && noRecentAttack && !targetHealthDroppingFast;
                bool proactiveHumanDisabled = lockedTarget.Race == ObjectType.Player
                                               && !Config.BotAttackPlayers
                                               && !BotPvPStrategy.IsInPvPStrategy(player.ObjectID);

                bool invalid = targetEnded
                              || IsBotGroupSharedTarget(player, lockedTarget)
                              || (lockedTarget.Race == ObjectType.Monster && !Config.BotAutoLevel)
                              || proactiveHumanDisabled
                              || !player.CanAttackTarget(lockedTarget)
                              || !Functions.InRange(player.CurrentLocation, lockedTarget.CurrentLocation, Config.MaxViewRange)
                              || (groupLeader != null && !IsBotTargetWithinGroupLeaderLeash(player, groupLeader, lockedTarget))
                              || shouldSwitch;

                if (invalid)
                {

                    // ★ 修复：目标死亡 / 消失时，顺手清掉残留的攻击/施法延迟动作。
                    //   否则上一拍已经排进 ActionList 的近战挥刀、延迟技能仍会继续执行，
                    //   看起来就像"怪死了还在空打"，同时也会拖慢重新选怪。
                    if (targetEnded)
                        ClearBotPendingCombatActions(player);

                    // 只有怪物目标真正死亡 / 消失时才进入等待拾取；真人 PK 目标不进拾取流程。
                    if (targetEnded && lockedTarget.Race == ObjectType.Monster)
                    {
                        if (_botLastAttackTime.TryGetValue(player.ObjectID, out DateTime recentAttack)
                            && (SEnvir.Now - recentAttack).TotalSeconds <= 6)
                        {
                            RecordBotKill(player, lockedTarget);
                        }

                        _botWaitingPickup[player.ObjectID] = SEnvir.Now;
                    }


                    lockedTarget = null;
                    ClearBotTargetLockState(player.ObjectID);
                }
                else if (!targetEnded)
                {
                    // 目标有效时，定期采样血量用于预测
                    SampleBotTargetHealth(player.ObjectID, lockedTarget);
                }
            }

            // ── Step 4：无目标时，组队协战优先；没人带节奏时再清附近怪、补满、自己找怪 ──
            MapObject assistTarget = null;
            if (lockedTarget == null)
            {
                assistTarget = GetBotGroupAssistTarget(player, groupLeader, hasHumanLeader);
                if (Config.BotAutoLevel && IsValidBotAssistTarget(player, assistTarget)
                    && assistTarget.Race != ObjectType.Player)
                {
                    lockedTarget = assistTarget;
                    _botTargets[player.ObjectID] = lockedTarget;
                    _botTargetSwitchTime[player.ObjectID] = SEnvir.Now.AddSeconds(BotTargetSwitchTimeout);
                    _botRoamTime.Remove(player.ObjectID);
                }
            }

            if (lockedTarget == null && Config.BotAutoLevel)
            {
                MonsterObject nearbyTarget = FindBestBotVisibleMonsterTarget(player, BotNearbyMonsterSweepRange, true);
                if (nearbyTarget != null)
                {
                    lockedTarget = nearbyTarget;
                    _botTargets[player.ObjectID] = lockedTarget;
                    _botTargetSwitchTime[player.ObjectID] = SEnvir.Now.AddSeconds(BotTargetSwitchTimeout);
                    _botRoamTime.Remove(player.ObjectID);
                }
            }

            if (lockedTarget == null)
            {
                // ★ 有真人队长时：只有队长最近确实在打架，才优先待命等协战。
                //   否则先按自己的视野继续找怪，避免队长一停手，全队一起发呆。
                bool leaderIsActuallyFighting = hasHumanLeader
                    && groupLeader != null
                    && groupLeader.GroupAssistTargetTime > SEnvir.Now.AddSeconds(-5)
                    && groupLeader.GroupAssistTarget?.Node != null
                    && !groupLeader.GroupAssistTarget.Dead;

                // 队员只负责协战和清理队长身边的近怪，不再自己拉全视野的新目标乱跑；
                // 但假人队长自己要负责继续带队推进，附近清光后应主动在视野内续怪。
                bool canSelfPickTarget = Config.BotAutoLevel
                                         && !leaderIsActuallyFighting && !isGroupedFollower;

                if (canSelfPickTarget)
                {
                    lockedTarget = FindBestBotVisibleMonsterTarget(player, Config.MaxViewRange, true);
                    if (lockedTarget != null)
                    {
                        _botTargets[player.ObjectID] = lockedTarget;
                        _botTargetSwitchTime[player.ObjectID] = SEnvir.Now.AddSeconds(BotTargetSwitchTimeout);
                        _botRoamTime.Remove(player.ObjectID);
                    }
                }
            }

            if (lockedTarget == null
                && assistTarget?.Race == ObjectType.Player
                && IsValidBotAssistTarget(player, assistTarget))
            {
                lockedTarget = assistTarget;
                _botTargets[player.ObjectID] = assistTarget;
                _botTargetSwitchTime[player.ObjectID] = SEnvir.Now.AddSeconds(BotTargetSwitchTimeout);
                _botRoamTime.Remove(player.ObjectID);
                if (Config.BotAttackPlayers)
                    UpdateBotAttackMode(player);
            }

            if (lockedTarget == null && Config.BotAttackPlayers
                && ShouldTriggerScaledBehavior(Config.BotAggressionPercent, player.ObjectID,
                    SEnvir.Now.Ticks / TimeSpan.TicksPerSecond))
            {
                PlayerObject human = FindNearestBotProactiveHumanTarget(player);
                if (human != null)
                {
                    lockedTarget = human;
                    _botTargets[player.ObjectID] = human;
                    _botTargetSwitchTime[player.ObjectID] = SEnvir.Now.AddSeconds(BotTargetSwitchTimeout);
                    _botRoamTime.Remove(player.ObjectID);
                    UpdateBotAttackMode(player);
                }
            }

            // 假人队长要继续带队推进，附近清光后允许先续怪/漫游，不要因为补满逻辑把整队卡在原地。
            if (lockedTarget == null && Config.BotAutoLevel
                && !isBotLeaderWithFollowers && TryProcessBotRoundRecovery(player))
                return;

            // ── Step 5（无目标）：智能换向漫游（优先往怪多的方向走）──
            // ★ 修复：有真人队长时，只在队长"最近5秒内有实际战斗输出"时才原地待命；
            //   队长 AFK/未战斗时允许漫游找怪，不乱跑引怪但也不傻站。
            if (lockedTarget == null && Config.BotAutoLevel)
            {
                bool leaderIsFightingNow = hasHumanLeader
                    && groupLeader != null
                    && groupLeader.GroupAssistTargetTime > SEnvir.Now.AddSeconds(-5)
                    && groupLeader.GroupAssistTarget?.Node != null
                    && !groupLeader.GroupAssistTarget.Dead;

                if (leaderIsFightingNow) return; // 队长正在战斗，静止等待协战目标同步

                // ★ 有积压动作时跳过，避免"双重移动"
                if (player.CanMove && !player.PacketWaiting && player.ActionList.Count == 0)
                {
                    bool needNewDir = !_botRoamDir.TryGetValue(player.ObjectID, out MirDirection roamDir);

                    // 仿真人 pathfindertime：漫游超时后换方向（2~4秒随机）
                    if (!needNewDir
                        && _botRoamTime.TryGetValue(player.ObjectID, out DateTime roamExpiry)
                        && SEnvir.Now > roamExpiry)
                    {
                        needNewDir = true;
                    }

                    if (needNewDir)
                    {
                        // ★ 优先用 A* 找最近可攻击怪物格子，直接导航过去。
                        //   找不到（视野清空）再退回智能方向漫游。
                        Point astarRoamTarget = BotPathFinder.FindNearestMonsterCellByAStar(player);
                        if (astarRoamTarget != Point.Empty
                            && BotPathFinder.TryUpdateRoamPath(player, astarRoamTarget))
                        {
                            // 有路径：直接走 A*，不更新漫游方向（下一帧继续消费路径）
                            BotPathFinder.TryMoveBotAlongPath(player);
                            return;
                        }

                        // ★ 智能选向：统计视野内8个方向各象限的怪物数量，
                        //   优先朝怪最多的半区移动（有三成概率随机，避免太机械）
                        roamDir = GetSmartRoamDirection(player);
                        _botRoamDir[player.ObjectID] = roamDir;
                        _botRoamTime[player.ObjectID] = SEnvir.Now.AddSeconds(2 + _botRandom.Next(3));
                    }

                    // 有缓存路径时优先消费（漫游 A* 路径未走完时继续跟着走）
                    if (BotPathFinder.HasValidPath(player.ObjectID))
                    {
                        if (BotPathFinder.TryMoveBotAlongPath(player))
                            return;
                        // 路径消耗完或被阻断，下一帧重算
                    }

                    // 遇障换方向 + 整段路径校验：漫游也走统一移动链，避免第二格被队友/怪挡住时原地空转。
                    if (TryMoveBotAlongDirection(player, roamDir, 2, out MirDirection actualRoamDir, out _))
                        _botRoamDir[player.ObjectID] = actualRoamDir;
                    else
                        _botRoamDir[player.ObjectID] = roamDir;
                }
                return;
            }

            // ── Step 5.5 / 6：进入职业战斗模块（含低血逃跑、远程站位、近战兜底）──
            ProcessBotCombatEngagement(player, lockedTarget);
        }

        /// <summary>
        /// PK 模块：仅对主动攻击自己的真人/宠物主人进行反击，避免无差别乱杀。
        /// 返回 true 表示本 Tick 已切入 PK 处理，不再继续普通刷怪逻辑。
        /// </summary>
        private static bool ProcessBotPK(PlayerObject player)
        {
            if (!Config.BotPvpRetaliation)
                return false;

            PlayerObject target = GetBotPriorityPKTarget(player);
            if (target == null) return false;

            // 记录攻击者
            RecordBotAttacker(player, target);

            ProcessBotCombatEngagement(player, target);
            return true;
        }

        /// <summary>
        /// 获取当前应优先反击的 PK 目标：真人攻击者，或敌方宠物对应的主人。
        /// </summary>
        private static PlayerObject GetBotPriorityPKTarget(PlayerObject player)
        {
            if (player == null || player.Dead) return null;

            MapObject attacker = player.LastHitter;
            if (attacker == null)
                return null;

            if (attacker.Node == null || attacker.Dead)
            {
                player.LastHitter = null;
                return null;
            }

            PlayerObject hostilePlayer = null;
            switch (attacker.Race)
            {
                case ObjectType.Player:
                    hostilePlayer = (PlayerObject)attacker;
                    break;
                case ObjectType.Monster:
                    hostilePlayer = ((MonsterObject)attacker).PetOwner;
                    break;
            }

            if (hostilePlayer == null || hostilePlayer == player || hostilePlayer.Node == null || hostilePlayer.Dead)
            {
                player.LastHitter = null;
                return null;
            }

            if (!Functions.InRange(player.CurrentLocation, hostilePlayer.CurrentLocation, Config.MaxViewRange))
            {
                player.LastHitter = null;
                return null;
            }

            if (!player.CanAttackTarget(hostilePlayer))
                return null;

            return hostilePlayer;
        }

        private static void SetBotRuntimeState(PlayerObject player, DBModels.BotState state)
        {
            AccountInfo account = player?.Connection?.Account;
            if (account == null) return;

            BotAccountInfo bot = botAccounts.FirstOrDefault(x => x.Account == account);
            if (bot == null) return;

            bot.BotState = state;
            bot.LastActionTime = Time.Now;
        }

        private static ConquestWar GetBotActiveConquestWar(PlayerObject player)
        {
            GuildInfo guild = player?.Character?.Account?.GuildMember?.Guild;
            if (guild == null) return null;

            return SEnvir.ConquestWars.FirstOrDefault(war => war != null
                && war.IsWaring
                && war.Participants != null
                && war.Participants.Contains(guild));
        }

        private static long GetBotConquestTargetScore(PlayerObject player, ConquestWar war, MapObject target)
        {
            if (player == null || war == null || target == null || target.Node == null || target.Dead)
                return long.MinValue;
            if (player.CurrentMap != war.Map || target.CurrentMap != war.Map)
                return long.MinValue;
            if (!Functions.InRange(player.CurrentLocation, target.CurrentLocation, Config.MaxViewRange))
                return long.MinValue;

            bool attacker = player.IsWarAttacker();
            int distance = MaxChebyshevDistance(player.CurrentLocation, target.CurrentLocation);

            switch (target)
            {
                case PlayerObject hostilePlayer:
                    if (!player.CanAttackTarget(hostilePlayer))
                        return long.MinValue;

                    long playerScore = 280_000L - distance * 2_000L - hostilePlayer.CurrentHP;
                    if (ReferenceEquals(player.LastHitter, hostilePlayer))
                        playerScore += 260_000L;
                    if (distance <= 2)
                        playerScore += 120_000L;
                    return playerScore;


                case MonsterObject monster:
                    if (!player.CanAttackTarget(monster))
                        return long.MinValue;

                    if (monster.PetOwner != null)
                    {
                        long petScore = 220_000L - distance * 2_000L - monster.CurrentHP;
                        if (ReferenceEquals(player.LastHitter, monster.PetOwner))
                            petScore += 60_000L;
                        return petScore;
                    }

                    if (!attacker)
                        return long.MinValue;

                    if (monster is SabukPrimeGate)
                        return 1_000_000L - distance * 5_000L - monster.CurrentHP;

                    if (monster is SabakGuard || monster is SabakGuardian)
                        return 720_000L - distance * 3_000L - monster.CurrentHP;

                    if (monster is CastleLord)
                        return 560_000L - distance * 2_500L - monster.CurrentHP;

                    return long.MinValue;

                default:
                    return long.MinValue;
            }
        }

        private static MapObject FindBotConquestPriorityTarget(PlayerObject player, ConquestWar war)
        {
            if (player?.VisibleObjects == null || war == null) return null;

            MapObject bestTarget = null;
            long bestScore = long.MinValue;

            foreach (MapObject visible in player.VisibleObjects)
            {
                long score = GetBotConquestTargetScore(player, war, visible);
                if (score <= bestScore) continue;

                bestScore = score;
                bestTarget = visible;
            }

            return bestTarget;
        }

        private static Point GetNearestBotConquestRegionPoint(MapRegion region, Point from)
        {
            if (region?.PointList == null || region.PointList.Count == 0)
                return Point.Empty;

            Point bestPoint = Point.Empty;
            int bestDistance = int.MaxValue;
            foreach (Point point in region.PointList)
            {
                int distance = Functions.Distance(from, point);
                if (distance >= bestDistance) continue;

                bestDistance = distance;
                bestPoint = point;
            }

            return bestPoint;
        }

        private static bool TryAdvanceBotInConquestMap(PlayerObject player, ConquestWar war)
        {
            if (player == null || war?.info == null || player.CurrentMap != war.Map)
                return false;

            Point advancePoint = player.IsWarAttacker()
                ? GetNearestBotConquestRegionPoint(war.info.CastleRegion, player.CurrentLocation)
                : GetNearestBotConquestRegionPoint(war.info.DefenderSpawnRegion ?? war.info.CastleRegion, player.CurrentLocation);

            if (advancePoint == Point.Empty)
                advancePoint = war.info.FlagPoint;
            if (advancePoint == Point.Empty || advancePoint == player.CurrentLocation)
                return false;

            MirDirection dir = Functions.DirectionFromPoint(player.CurrentLocation, advancePoint);
            return TryMoveBotAlongDirection(player, dir, 2, out _, out _);
        }

        /// <summary>
        /// 攻城战主入口：委托给策略化攻城逻辑（BotManager.Siege.cs）。
        /// </summary>
        private static bool ProcessBotConquestWarfare(PlayerObject player)
        {
            if (!Config.BotParticipateConquest || player == null || player.Dead || player.Node == null)
                return false;

            ConquestWar war = GetBotActiveConquestWar(player);
            if (war == null)
            {
                // 攻城结束，清理策略状态
                ClearBotSiegeState(player.ObjectID);
                SetBotRuntimeState(player, DBModels.BotState.Playing);
                return false;
            }

            SetBotRuntimeState(player, DBModels.BotState.GuildWar);

            return ProcessBotSiegeWarfare(player, war);
        }

        /// <summary>
        /// 职业战斗分发：统一处理低血逃跑、远程技能、近战物理与职业差异。
        /// </summary>

        private static void ProcessBotCombatEngagement(PlayerObject player, MapObject target)
        {
            if (player == null || target == null || target.Node == null || target.Dead)
                return;

            // 常规药水由 BotPotionTick（200ms 独立定时器）处理，
            // 战斗帧仅在危险血线下触发紧急喝药。
            // 仅在低血紧急模式（<15%）时尝试一次强制追喝。

            int dist = MaxChebyshevDistance(player.CurrentLocation, target.CurrentLocation);
            MirDirection dir = Functions.DirectionFromPoint(player.CurrentLocation, target.CurrentLocation);
            bool forcePhysicalFallback = target.Race == ObjectType.Monster;

            if (TryProcessBotBossMechanicAwareness(player, ref target, dist, dir))
                return;

            dist = MaxChebyshevDistance(player.CurrentLocation, target.CurrentLocation);
            dir = Functions.DirectionFromPoint(player.CurrentLocation, target.CurrentLocation);

            if (TryProcessBotRetreat(player, target, dir))
                return;


            switch (player.Class)
            {
                case MirClass.Warrior:
                    ProcessBotWarriorCombatAction(player, target, dist, dir);
                    return;
                case MirClass.Wizard:
                    ProcessBotWizardCombatAction(player, target, dist, dir, forcePhysicalFallback);
                    return;
                case MirClass.Taoist:
                    ProcessBotTaoistCombatAction(player, target, dist, dir, forcePhysicalFallback);
                    return;
                case MirClass.Assassin:
                    ProcessBotAssassinCombatAction(player, target, dist, dir);
                    return;
                default:
                    ProcessBotMeleeCombatAction(player, dist, dir, MagicType.None);
                    return;
            }
        }

        /// <summary>
        /// 低血逃跑模块：所有职业共用，HP 低于阈值时先保命。
        /// </summary>
        private static bool TryProcessBotRetreat(PlayerObject player, MapObject target, MirDirection targetDir)
        {
            if (player.Stats[Stat.Health] <= 0)
                return false;

            long hpPct = player.CurrentHP * 100L / player.Stats[Stat.Health];
            if (hpPct >= BotFleeHpPct)
                return false;

            // 30% 以下先站住把药顶出来，不再因为“轻伤”就整拍满场风筝。
            if (hpPct > BotPotionEmergencyHpPct)
            {
                TryStabilizeBotLowHpWithPotion(player, hpPct);
                return false;
            }

            // 真正跌进危险区时，再补一次紧急药；能拉回血就继续留在原目标上输出。
            if (ProcessBotPotionMonitor(player, true))
                return false;

            MirDirection fleeDir = Functions.ShiftDirection(targetDir, 4);
            if (player.CanMove && !player.PacketWaiting && player.ActionList.Count == 0)
                TryMoveBotAlongDirection(player, fleeDir, 2, out _, out _);
            return true;
        }

        /// <summary>
        /// 战士战斗模块：低级阶段也会按距离/怪堆切换攻杀、刺杀和半月，避免全程只会平砍一招。
        /// </summary>
        private static void ProcessBotWarriorCombatAction(PlayerObject player, MapObject target, int dist, MirDirection dir)
        {
            if (TryPrepareBotWarriorChargedAttack(player, target, dir))
                return;

            // PVP 风筝模式下保持距离
            if (_botKiteMode.TryGetValue(player.ObjectID, out bool kiteMode) && kiteMode)
            {
                // 战士在风筝模式下：距离近（≤1格）才挥刀打一下，否则不追不贴脸
                if (dist <= 1)
                {
                    int mobCount = BotSkillSelector.CountNearbyAttackableMonsters(player, player.CurrentLocation, 1);
                    MagicType magic = BotSkillSelector.GetWarriorMeleeAttackMagic(player, target, mobCount);
                    ProcessBotMeleeCombatAction(player, dist, dir, magic);
                }
                // 距离远时不追 → return 等下一帧 PVP 策略计算后退方向
                return;
            }

            int nearbyMobCount = BotSkillSelector.CountNearbyAttackableMonsters(player, player.CurrentLocation, 1);
            MagicType meleeMagic = BotSkillSelector.GetWarriorMeleeAttackMagic(player, target, nearbyMobCount);
            ProcessBotMeleeCombatAction(player, dist, dir, meleeMagic);
        }

        private static bool TryPrepareBotWarriorChargedAttack(PlayerObject player, MapObject target, MirDirection dir)
        {
            if (player == null || target == null)
                return false;
            if (player.CanFlamingSword || player.CanBladeStorm || player.CanMaelstromBlade)
                return false;

            MagicType chargeMagic = BotSkillSelector.GetWarriorChargeMagic(player);
            if (chargeMagic == MagicType.None)
                return false;

            return TryCastBotMagic(player, dir, chargeMagic, player, player.CurrentLocation);
        }

        /// <summary>
        /// 法师战斗模块：先远程输出；十级以上没有可用技能时保持远程距离。
        /// </summary>
        private static void ProcessBotWizardCombatAction(PlayerObject player, MapObject target, int dist, MirDirection dir, bool forcePhysicalFallback)
        {
            if (TryRepositionBotFromImmediateRangedThreat(player, target))
                return;

            int nearbyMobCount = BotSkillSelector.CountNearbyAttackableMonsters(player, player.CurrentLocation, 2);
            if (TryProcessBotRangedCombatAction(player, target, dist, dir, BotSkillSelector.GetWizardRangedMagic(player, target, nearbyMobCount)))
                return;

            ProcessBotRangedNoMagicFallback(player, target, dist, dir);
        }

        /// <summary>
        /// 道士战斗模块：先依次尝试远程攻击技能，均不可用时再施毒；十级以上没有可用技能时保持远程距离。
        /// </summary>
        private static void ProcessBotTaoistCombatAction(PlayerObject player, MapObject target, int dist, MirDirection dir, bool forcePhysicalFallback)
        {
            if (TryRepositionBotFromImmediateRangedThreat(player, target))
                return;

            // ── 计算周围可攻击怪物数量（用于判断是否使用群体技能）──────────────────
            int nearbyMobCount = BotSkillSelector.CountNearbyAttackableMonsters(player, player.CurrentLocation, 2);

            foreach (MagicType directMagic in BotSkillSelector.GetTaoistReadyDirectAttacks(player))
            {
                if (TryProcessBotRangedCombatAction(player, target, dist, dir, directMagic))
                    return;
            }

            // ── 道士战斗中毒药切换：确保装备槽里是当前需要的毒药 ──────────────────────
            // 按视觉颜色判断：正常→红毒（Shape=1），粉紫→绿毒（Shape=0），绿色→不切换
            if (player.Class == MirClass.Taoist && target != null && !target.Dead)
            {
                // 用视觉颜色判断怪物状态（与 BotSkillSelector 保持一致）
                bool hasGreenPoison = (target.Poison & PoisonType.Green) != PoisonType.None;
                bool hasRedPoison   = (target.Poison & PoisonType.Red)   != PoisonType.None;

                // 确定当前需要装备的毒药类型
                int targetShape = -1;
                if (!hasRedPoison)
                    targetShape = 1; // 需要施红毒 → 装黄色药粉 Shape=1
                else if (!hasGreenPoison)
                    targetShape = 0; // 需要施绿毒 → 装灰色药粉 Shape=0
                // 双毒齐全：targetShape=-1，无需切换

                if (targetShape >= 0)
                    TryEquipBotTaoistPoisonForShape(player, targetShape);
            }

            MagicType optionalPoison = BotSkillSelector.GetTaoistOptionalPoisonMagic(player, target, nearbyMobCount);
            if (TryProcessBotRangedCombatAction(player, target, dist, dir, optionalPoison))
                return;

            ProcessBotRangedNoMagicFallback(player, target, dist, dir);
        }

        private static void ProcessBotRangedNoMagicFallback(PlayerObject player, MapObject target, int dist, MirDirection dir)
        {
            if (player.Level <= 10)
            {
                ProcessBotMeleeCombatAction(player, dist, dir, MagicType.None);
                return;
            }

            int preferredDistance = GetBotPreferredRangedDistance(player, target);
            if (dist < preferredDistance)
                TryRepositionBotForPreferredRange(player, dir, preferredDistance - dist);
        }

        /// <summary>
        /// 刺客战斗模块：依次尝试范围、单体、突进和近战技能，均不可用时再执行普通攻击。
        /// </summary>
        private static void ProcessBotAssassinCombatAction(PlayerObject player, MapObject target, int dist, MirDirection dir)
        {
            int nearbyMobCount = BotSkillSelector.CountNearbyAttackableMonsters(player, player.CurrentLocation, 2);

            if (TryProcessBotAssassinAreaCombatAction(player, target, dist, dir, nearbyMobCount))
                return;

            if (TryProcessBotRangedCombatAction(player, target, dist, dir, BotSkillSelector.GetAssassinTargetMagic(player, target)))
                return;

            if (TryProcessBotAssassinGapClose(player, target, dist, dir))
                return;

            MagicType meleeMagic = BotSkillSelector.GetAssassinMeleeAttackMagic(player, target, nearbyMobCount);
            ProcessBotMeleeCombatAction(player, dist, dir, meleeMagic);
        }

        /// <summary>
        /// 刺客近身 AOE：怪物扎堆时优先铺毒云，其次放血之盟约。
        /// </summary>
        private static bool TryProcessBotAssassinAreaCombatAction(PlayerObject player, MapObject target, int dist, MirDirection dir, int nearbyMobCount)
        {
            MagicType areaMagic = BotSkillSelector.GetAssassinAreaMagic(player, target, nearbyMobCount);
            if (areaMagic == MagicType.None)
                return false;

            switch (areaMagic)
            {
                case MagicType.PoisonousCloud:
                    if (dist > 2)
                        return false;

                    return TryCastBotMagic(player, dir, areaMagic, player, player.CurrentLocation);
                case MagicType.Rake:
                    if (target == null || dist > 1)
                        return false;

                    return TryCastBotMagic(player, dir, areaMagic, target, target.CurrentLocation);
                default:
                    return false;
            }
        }

        /// <summary>
        /// 刺客突进模块：中距离优先鹰击贴脸，避免一直傻跑。
        /// </summary>
        private static bool TryProcessBotAssassinGapClose(PlayerObject player, MapObject target, int dist, MirDirection dir)
        {
            MagicType gapMagic = BotSkillSelector.GetAssassinGapCloserMagic(player, dist);
            if (gapMagic == MagicType.None || target == null)
                return false;

            return TryCastBotMagic(player, dir, gapMagic, target, target.CurrentLocation);
        }

        /// <summary>
        /// 通用施法帮助：统一处理方向、目标、坐标与最近一次攻击时间更新。
        /// </summary>
        private static bool TryCastBotMagic(PlayerObject player, MirDirection dir, MagicType magicType, MapObject target = null, Point? location = null)
        {
            if (player == null || magicType == MagicType.None)
                return false;
            if (!player.CanCast || player.PacketWaiting || player.ActionList.Count > 0)
                return false;
            if (!player.Magics.TryGetValue(magicType, out UserMagic magic) || magic?.Info == null)
                return false;
            if (player.Level < magic.Info.NeedLevel1 || magic.Cooldown > SEnvir.Now)
                return false;
            if (magic.Cost > player.CurrentMP)
                return false;

            if (!TryStartBotAttackAttempt(player))
                return false;

            if (TryGetBotTaoistAmuletRequirement(
                    magicType,
                    out int requiredAmuletCount,
                    out bool requiresSoulAmulet))
            {
                if (!TryEquipBotTaoistAmuletForMagic(player, magicType))
                    return false;

                UserItem equippedAmulet = player.Equipment[(int)EquipmentSlot.Amulet];
                int requiredShapeMin = requiresSoulAmulet ? 0 : 1;
                int requiredShapeMax = requiresSoulAmulet ? 0 : 8;
                if (equippedAmulet?.Info?.ItemType != ItemType.Amulet
                    || equippedAmulet.Count < requiredAmuletCount
                    || equippedAmulet.Info.Shape < requiredShapeMin
                    || equippedAmulet.Info.Shape > requiredShapeMax)
                    return false;
            }

            // ── 施毒技能：递增毒药使用计数 ────────────────────────────────────
            bool isPoisonSkill = magicType == MagicType.PoisonDust || magicType == MagicType.GreaterPoisonDust;

            DateTime previousCooldown = magic.Cooldown;

            // 动态更新攻击模式（根据当前场景选择合适的模式）
            UpdateBotAttackMode(player);

            player.Direction = dir;
            player.Magic(new C.Magic
            {
                Direction = dir,
                Type = magicType,
                Target = target?.ObjectID ?? player.ObjectID,
                Location = location ?? target?.CurrentLocation ?? player.CurrentLocation,
            });

            bool castSucceeded = magic.Cooldown > previousCooldown && magic.Cooldown > SEnvir.Now;
            RecordBotMagicCastResult(player, castSucceeded);
            if (!castSucceeded)
                return false;

            // ── 施毒技能：递增毒药使用计数 ────────────────────────────────────
            if (isPoisonSkill)
            {
                uint pid = player.ObjectID;
                if (!_botTaoistPoisonUseCount.TryGetValue(pid, out int useCount))
                    useCount = 0;
                _botTaoistPoisonUseCount[pid] = useCount + 1;

                // 记录施毒信息（目标ID + 时间 + 毒药Shape），用于确认 500ms 延迟
                if (target != null)
                {
                    UserItem equippedPoison = player.Equipment[(int)EquipmentSlot.Poison];
                    int poisonShape = equippedPoison?.Info.Shape ?? -1;
                    _botTaoistLastPoisonCast[pid] = (target.ObjectID, SEnvir.Now, poisonShape);
                }
            }

            _botLastAttackTime[player.ObjectID] = SEnvir.Now;
            return true;

        }

        private static bool TryStartBotAttackAttempt(PlayerObject player)
        {
            if (player == null) return false;

            uint objectId = player.ObjectID;
            DateTime now = SEnvir.Now;
            if (_botNextAttackAttemptTime.TryGetValue(objectId, out DateTime next)
                && now < next)
                return false;

            _botNextAttackAttemptTime[objectId] = now.AddMilliseconds(
                Math.Max(1, Math.Min(60000, Config.BotAttackAttemptIntervalMs)));
            return true;
        }

        private static bool TryStartBotPickupAttempt(PlayerObject player)
        {
            if (player == null) return false;

            uint objectId = player.ObjectID;
            DateTime now = SEnvir.Now;
            if (_botNextPickupAttemptTime.TryGetValue(objectId, out DateTime next)
                && now < next)
                return false;

            _botNextPickupAttemptTime[objectId] = now.AddMilliseconds(
                Math.Max(1, Math.Min(60000, Config.BotPickupAttemptIntervalMs)));
            return true;
        }

        private static IEnumerable<MirDirection> EnumerateBotDirectionCandidates(MirDirection preferredDir)
        {
            yield return preferredDir;

            for (int offset = 1; offset <= 4; offset++)
            {
                MirDirection left = Functions.ShiftDirection(preferredDir, -offset);
                MirDirection right = Functions.ShiftDirection(preferredDir, offset);

                yield return left;
                if (right != left)
                    yield return right;
            }
        }

        private static bool CanBotTraverseDirection(PlayerObject player, MirDirection dir, int distance, out Point destination)
        {
            destination = player?.CurrentLocation ?? Point.Empty;
            if (player?.CurrentMap == null || distance <= 0)
                return false;

            distance = Math.Max(1, Math.Min(3, distance));
            for (int step = 1; step <= distance; step++)
            {
                Point stepLocation = Functions.Move(player.CurrentLocation, dir, step);
                Cell stepCell = player.CurrentMap.GetCell(stepLocation);
                if (stepCell == null || stepCell.IsBlocking(player, false))
                    return false;
                // 安全区格子不可进入（漫游/追击/逃跑时均不得踏入安全区边界）
                // 避免假人在道馆等安全区/非安全区边界反复进出导致卡住
                if (stepCell.SafeZone != null)
                    return false;
            }

            destination = Functions.Move(player.CurrentLocation, dir, distance);
            return true;
        }

        private static MapObject GetBotTrackedCombatTarget(PlayerObject player)
        {
            if (player == null) return null;

            if (_botTargets.TryGetValue(player.ObjectID, out MapObject trackedTarget)
                && trackedTarget != null
                && trackedTarget.Node != null
                && !trackedTarget.Dead)
                return trackedTarget;

            if (player.GroupAssistTargetTime > SEnvir.Now.AddSeconds(-5)
                && player.GroupAssistTarget != null
                && player.GroupAssistTarget.Node != null
                && !player.GroupAssistTarget.Dead)
                return player.GroupAssistTarget;

            return null;
        }

        private static bool TryMoveBotGroupBlockerAside(PlayerObject blocker, PlayerObject leader, MirDirection leaderDir)
        {
            if (blocker == null || leader == null || blocker == leader)
                return false;
            if (blocker.Node == null || blocker.Dead || blocker.CurrentMap != leader.CurrentMap)
                return false;
            if (!botPlayers.Contains(blocker))
                return false;
            if (!blocker.CanMove || blocker.PacketWaiting || blocker.ActionList.Count > 0)
                return false;

            MirDirection awayDir = blocker.CurrentLocation == leader.CurrentLocation
                ? Functions.ShiftDirection(leaderDir, 4)
                : Functions.DirectionFromPoint(leader.CurrentLocation, blocker.CurrentLocation);

            MirDirection[] preferredDirs =
            {
                awayDir,
                Functions.ShiftDirection(awayDir, -1),
                Functions.ShiftDirection(awayDir, 1),
                Functions.ShiftDirection(leaderDir, -2),
                Functions.ShiftDirection(leaderDir, 2),
                Functions.ShiftDirection(leaderDir, -3),
                Functions.ShiftDirection(leaderDir, 3),
                Functions.ShiftDirection(leaderDir, 4),
            };

            foreach (MirDirection dir in preferredDirs.Distinct())
            {
                for (int distance = 2; distance >= 1; distance--)
                {
                    if (!CanBotTraverseDirection(blocker, dir, distance, out _)) continue;

                    blocker.Move(dir, distance);
                    return true;
                }
            }

            return false;
        }

        private static void TryClearBotGroupMoveLane(PlayerObject leader, MirDirection preferredDir)
        {
            if (leader?.GroupMembers == null || leader.GroupMembers.Count <= 1)
                return;
            if (leader.GroupMembers[0] != leader || leader.CurrentMap == null)
                return;

            Point firstStep = Functions.Move(leader.CurrentLocation, preferredDir, 1);
            Cell cell = leader.CurrentMap.GetCell(firstStep);
            if (cell?.Objects == null) return;

            foreach (PlayerObject blocker in cell.Objects.OfType<PlayerObject>().ToList())
            {
                if (blocker == null || blocker == leader || blocker.Node == null || blocker.Dead) continue;
                if (!leader.GroupMembers.Contains(blocker)) continue;

                TryMoveBotGroupBlockerAside(blocker, leader, preferredDir);
            }
        }

        private static bool TryMoveBotAlongDirection(PlayerObject player, MirDirection preferredDir, int maxDistance, out MirDirection actualDir, out int actualDistance)
        {
            actualDir = preferredDir;
            actualDistance = 0;

            if (player == null || player.Dead || player.Node == null || player.CurrentMap == null)
                return false;
            if (!player.CanMove || player.PacketWaiting || player.ActionList.Count > 0)
                return false;

            maxDistance = Math.Max(1, Math.Min(3, maxDistance));
            TryClearBotGroupMoveLane(player, preferredDir);

            foreach (MirDirection dir in EnumerateBotDirectionCandidates(preferredDir))
            {
                for (int distance = maxDistance; distance >= 1; distance--)
                {
                    if (!CanBotTraverseDirection(player, dir, distance, out _)) continue;

                    actualDir = dir;
                    actualDistance = distance;
                    player.Move(dir, distance);
                    RecordBotMoveResult(player, true);
                    return true;
                }
            }

            RecordBotMoveResult(player, false);
            return false;

        }

        private static bool IsBotBossTarget(MapObject target)
        {
            MonsterObject monster = target as MonsterObject;
            return monster?.MonsterInfo?.IsBoss == true;
        }

        private static int GetBotPreferredRangedDistance(PlayerObject player, MapObject target)
        {
            if (player == null) return BotRangedMinDist;

            BotBehaviorProfile profile = GetBotBehaviorProfile(player);
            bool grouped = player.GroupMembers != null && player.GroupMembers.Count > 1;
            bool leader = grouped && player.GroupMembers[0] == player;

            int preferredDistance;
            switch (player.Class)
            {
                case MirClass.Wizard:
                    preferredDistance = 4;
                    break;
                case MirClass.Taoist:
                    preferredDistance = 3;
                    break;
                case MirClass.Assassin:
                    preferredDistance = 2;
                    break;
                default:
                    preferredDistance = BotRangedMinDist;
                    break;
            }

            if (grouped && !leader)
                preferredDistance += 1;
            if (leader)
                preferredDistance = Math.Max(BotRangedMinDist, preferredDistance - 1);
            if (IsBotBossTarget(target) && (player.Class == MirClass.Wizard || player.Class == MirClass.Taoist))
                preferredDistance += 1;

            preferredDistance += Math.Max(-1, Math.Min(1, (profile?.CautionBias ?? 0) - (profile?.AggressionBias ?? 0)));
            return Math.Max(BotRangedMinDist, Math.Min(BotRangedMaxDist + 1, preferredDistance));
        }

        private static bool TryRepositionBotForPreferredRange(PlayerObject player, MirDirection targetDir, int extraDistance)
        {
            if (player == null || extraDistance <= 0)
                return false;

            int step = Math.Max(1, Math.Min(2, extraDistance));
            MirDirection backDir = Functions.ShiftDirection(targetDir, 4);
            if (TryMoveBotAlongDirection(player, backDir, step, out _, out _))
                return true;

            MirDirection leftDir = Functions.ShiftDirection(backDir, -1);
            if (TryMoveBotAlongDirection(player, leftDir, 2, out _, out _))
                return true;

            MirDirection rightDir = Functions.ShiftDirection(backDir, 1);
            return TryMoveBotAlongDirection(player, rightDir, 2, out _, out _);
        }

        private static bool TryRepositionBotFromImmediateRangedThreat(PlayerObject player, MapObject target)
        {
            if (player == null)
                return false;

            MonsterObject immediateThreat = target as MonsterObject;
            if (immediateThreat == null
                || immediateThreat.Node == null
                || immediateThreat.Dead
                || MaxChebyshevDistance(player.CurrentLocation, immediateThreat.CurrentLocation) > 1)
            {
                immediateThreat = FindBestBotVisibleMonsterTarget(player, 1, true);
            }

            if (immediateThreat == null)
                return false;

            MirDirection threatDir = Functions.DirectionFromPoint(player.CurrentLocation, immediateThreat.CurrentLocation);
            return TryRepositionBotForPreferredRange(player, threatDir, 2);
        }

        /// <summary>
        /// 计算目标威胁评分：距离越近 + 血量越少 = 威胁越高
        /// </summary>
        /// <returns>威胁评分（0-1），1 表示最高威胁</returns>
        private static double CalculateBotTargetThreatScore(PlayerObject player, MonsterObject monster, int distance, int hpPct)
        {
            if (player == null || monster == null) return 0;

            // 距离威胁：越近威胁越大（距离 1-15 映射到 0.4-0）
            double distanceThreat = Math.Max(0, 1.0 - (distance - 1.0) / 14.0) * 0.4;

            // 血量威胁：血量越少威胁越大（血量百分比 0-100 映射到 0.6-0）
            double healthThreat = (100.0 - hpPct) / 100.0 * 0.6;

            // 怪物等级加成：等级比玩家高的怪威胁更高
            int levelDiff = monster.Level - player.Level;
            double levelThreat = levelDiff > 0 ? Math.Min(0.2, levelDiff * 0.02) : 0;

            // 综合威胁评分
            double totalThreat = distanceThreat + healthThreat + levelThreat;

            return Math.Max(0, Math.Min(1, totalThreat));
        }

        /// <summary>
        /// 预判怪物移动轨迹：分析怪物的当前移动方向，预测未来位置
        /// </summary>
        /// <returns>预测的怪物未来位置，如果无法预测则返回当前位置</returns>
        private static Point PredictMonsterMovement(PlayerObject player, MonsterObject monster, int currentDistance)
        {
            if (player == null || monster == null || monster.CurrentMap == null)
                return Point.Empty;

            // 只对距离较远的怪物进行预判（3格以上）
            if (currentDistance <= 3)
                return monster.CurrentLocation;

            // 检查怪物是否正在向玩家靠近
            Point playerPos = player.CurrentLocation;
            Point monsterPos = monster.CurrentLocation;

            // 如果怪物已经贴脸，不需要预判
            if (Functions.Distance(playerPos, monsterPos) <= 2)
                return monster.CurrentLocation;

            // 计算怪物到玩家的方向
            int dx = playerPos.X - monsterPos.X;
            int dy = playerPos.Y - monsterPos.Y;

            // 判断怪物是否正在靠近玩家
            bool monsterApproaching = Math.Abs(dx) <= currentDistance && Math.Abs(dy) <= currentDistance;

            if (!monsterApproaching)
                return monster.CurrentLocation;

            // 预测怪物未来位置（简单预测：假设怪物会继续沿直线移动）
            // 预测距离为当前距离的 30%
            int predictSteps = Math.Max(1, currentDistance / 3);

            int predictedX = monsterPos.X + (dx > 0 ? Math.Min(predictSteps, dx) : (dx < 0 ? Math.Min(predictSteps, -dx) : 0));
            int predictedY = monsterPos.Y + (dy > 0 ? Math.Min(predictSteps, dy) : (dy < 0 ? Math.Min(predictSteps, -dy) : 0));

            Point predictedPos = new Point(predictedX, predictedY);

            // 确保预测位置在地图范围内且可走
            if (monster.CurrentMap.Width > 0 && monster.CurrentMap.Height > 0)
            {
                if (predictedX < 0 || predictedX >= monster.CurrentMap.Width ||
                    predictedY < 0 || predictedY >= monster.CurrentMap.Height)
                    return monster.CurrentLocation;

                Cell cell = monster.CurrentMap.GetCell(predictedPos);
                if (cell == null)
                    return monster.CurrentLocation;
            }

            return predictedPos;
        }

        /// <summary>
        /// 使用预判位置进行施法
        /// </summary>
        private static bool TryCastBotMagicWithPredicton(PlayerObject player, MirDirection dir, MagicType magicType, MapObject target, Point predictedLocation)
        {
            if (player == null || magicType == MagicType.None || target == null)
                return false;
            if (!player.CanCast || player.PacketWaiting || player.ActionList.Count > 0)
                return false;
            if (!player.Magics.TryGetValue(magicType, out UserMagic magic) || magic?.Info == null)
                return false;
            if (player.Level < magic.Info.NeedLevel1 || magic.Cooldown > SEnvir.Now)
                return false;
            if (magic.Cost > player.CurrentMP)
                return false;

            if (TryGetBotTaoistAmuletRequirement(
                    magicType,
                    out int requiredAmuletCount,
                    out bool requiresSoulAmulet))
            {
                if (!TryEquipBotTaoistAmuletForMagic(player, magicType))
                    return false;

                UserItem equippedAmulet = player.Equipment[(int)EquipmentSlot.Amulet];
                int requiredShapeMin = requiresSoulAmulet ? 0 : 1;
                int requiredShapeMax = requiresSoulAmulet ? 0 : 8;
                if (equippedAmulet?.Info?.ItemType != ItemType.Amulet
                    || equippedAmulet.Count < requiredAmuletCount
                    || equippedAmulet.Info.Shape < requiredShapeMin
                    || equippedAmulet.Info.Shape > requiredShapeMax)
                    return false;
            }

            DateTime previousCooldown = magic.Cooldown;

            // 动态更新攻击模式（根据当前场景选择合适的模式）
            UpdateBotAttackMode(player);

            player.Direction = dir;
            player.Magic(new C.Magic
            {
                Direction = dir,
                Type = magicType,
                Target = target.ObjectID,
                Location = predictedLocation,  // 使用预测位置
            });

            bool castSucceeded = magic.Cooldown > previousCooldown && magic.Cooldown > SEnvir.Now;
            RecordBotMagicCastResult(player, castSucceeded);
            if (!castSucceeded)
                return false;

            _botLastAttackTime[player.ObjectID] = SEnvir.Now;
            return true;
        }

        private static long GetBotProfileTargetScoreAdjustment(PlayerObject player, MonsterObject monster, int distance)
        {
            if (player == null || monster?.MonsterInfo == null) return 0;

            BotBehaviorProfile profile = GetBotBehaviorProfile(player);
            long score = 0;

            switch (player.Class)
            {
                case MirClass.Warrior:
                    score -= distance * 4000L;
                    score += Math.Max(0, monster.Level - player.Level + 1) * 5000L;
                    break;
                case MirClass.Wizard:
                    score -= Math.Max(0, 2 - distance) * 18000L;
                    score += Math.Max(0, 5 - distance) * 2500L;
                    break;
                case MirClass.Taoist:
                    score -= Math.Max(0, 2 - distance) * 12000L;
                    score += Math.Max(0, 4 - distance) * 1800L;
                    break;
                case MirClass.Assassin:
                    score += Math.Max(0, 3 - distance) * 4500L;
                    break;
            }

            score += (profile?.AggressionBias ?? 0) * Math.Max(0, monster.Level - player.Level + 2) * 2500L;
            score -= (profile?.CautionBias ?? 0) * Math.Max(0, monster.Level - player.Level) * 3200L;
            score -= (profile?.CautionBias ?? 0) * monster.CurrentHP / 3;
            return score;
        }

        private static MonsterObject FindBotBossPressureAdd(PlayerObject player, MonsterObject boss)
        {
            if (player?.VisibleObjects == null || boss == null) return null;

            MonsterObject bestTarget = null;
            int bestDistance = int.MaxValue;

            foreach (MonsterObject monster in player.VisibleObjects.OfType<MonsterObject>())
            {
                if (monster == null || monster == boss || monster.Node == null || monster.Dead) continue;
                if (monster.PetOwner != null || monster.MonsterInfo?.IsBoss == true) continue;
                if (!player.CanAttackTarget(monster)) continue;

                bool pressuringGroup = ReferenceEquals(monster.Target, player)
                                      || (player.GroupMembers != null && player.GroupMembers.Contains(monster.Target as PlayerObject));
                bool nearBoss = boss.CurrentMap == monster.CurrentMap && MaxChebyshevDistance(boss.CurrentLocation, monster.CurrentLocation) <= 4;
                if (!pressuringGroup && !nearBoss) continue;

                int distance = MaxChebyshevDistance(player.CurrentLocation, monster.CurrentLocation);
                if (distance >= bestDistance) continue;

                bestDistance = distance;
                bestTarget = monster;
            }

            return bestTarget;
        }

        private static bool TryProcessBotBossMechanicAwareness(PlayerObject player, ref MapObject target, int dist, MirDirection dir)
        {
            MonsterObject boss = target as MonsterObject;
            if (player == null || boss?.MonsterInfo?.IsBoss != true)
                return false;

            BotBehaviorProfile profile = GetBotBehaviorProfile(player);
            int nearbyMobCount = BotSkillSelector.CountNearbyAttackableMonsters(player, player.CurrentLocation, 3);
            int hpMax = Math.Max(1, player.Stats[Stat.Health]);
            long hpPct = player.CurrentHP * 100L / hpMax;
            int retreatThreshold = Math.Max(BotPotionEmergencyHpPct, 18 + Math.Max(0, profile?.CautionBias ?? 0) * 3);

            if (hpPct <= retreatThreshold && nearbyMobCount >= 2)
            {
                ProcessBotPotionMonitor(player, true);
                if (TryMoveBotAlongDirection(player, Functions.ShiftDirection(dir, 4), 2, out _, out _))
                {
                    RecordBotBossEvent(player, true, false);
                    return true;
                }
            }

            if (player.Class != MirClass.Warrior)
            {
                MonsterObject addTarget = FindBotBossPressureAdd(player, boss);
                if (addTarget != null)
                {
                    target = addTarget;
                    _botTargets[player.ObjectID] = addTarget;
                    _botTargetSwitchTime[player.ObjectID] = SEnvir.Now.AddSeconds(BotTargetSwitchTimeout);
                    RecordBotBossEvent(player, false, true);
                    return false;
                }
            }

            if ((player.Class == MirClass.Wizard || player.Class == MirClass.Taoist) && dist <= 1)
            {
                if (TryRepositionBotForPreferredRange(player, dir, GetBotPreferredRangedDistance(player, boss) - dist))
                {
                    RecordBotBossEvent(player, true, false);
                    return true;
                }
            }

            return false;
        }

        /// <summary>
        /// 远程战斗模块：适用于法师、道士与刺客的点名技能。2~5 格内施法，过远追击，贴脸则返回 false 交给近战模块兜底。
        /// 修复：不再依赖 Config.CanFlyTargetCheck 全局开关（该开关决定玩家端直线魔法，与假人无关）；
        ///       改为只要目标存活且在视野内即可施法。
        /// </summary>
        private static bool TryProcessBotRangedCombatAction(PlayerObject player, MapObject target, int dist, MirDirection dir, MagicType rangedMagic)

        {
            // 假人远程判断：技能有效 + 目标存活可达（不依赖 CanFlyTarget 全局开关）
            if (rangedMagic == MagicType.None || target == null || target.Node == null || target.Dead)
                return false;

            int preferredDistance = GetBotPreferredRangedDistance(player, target);
            int maxDistance = Math.Max(BotRangedMaxDist, preferredDistance + 1);

            if (player.Class != MirClass.Assassin && dist < preferredDistance)
            {
                if (TryRepositionBotForPreferredRange(player, dir, preferredDistance - dist))
                    return true;
            }

            if (dist <= maxDistance)
            {
                // ★ 法师远程战斗时，预判怪物移动轨迹，选择最优走位
                if (player.Class == MirClass.Wizard && target.Race == ObjectType.Monster)
                {
                    Point predictedPosition = PredictMonsterMovement(player, target as MonsterObject, dist);
                    if (predictedPosition != Point.Empty && predictedPosition != target.CurrentLocation)
                    {
                        // 预判到怪物会移动，调整施法位置
                        return TryCastBotMagicWithPredicton(player, dir, rangedMagic, target, predictedPosition);
                    }
                }

                return TryCastBotMagic(player, dir, rangedMagic, target, target.CurrentLocation);
            }

            // 超出射程追击：距离足够远时先走 A* 路径，绕过复杂地形
            if (dist >= BotPathFinder.MinPathfindDistance
                && player.CanMove && !player.PacketWaiting && player.ActionList.Count == 0)
            {
                MapObject chaseTarget2 = null;
                _botTargets.TryGetValue(player.ObjectID, out chaseTarget2);
                if (chaseTarget2 != null && chaseTarget2.Node != null && !chaseTarget2.Dead
                    && BotPathFinder.TryUpdateChasePath(player, chaseTarget2)
                    && BotPathFinder.TryMoveBotAlongPath(player))
                    return true;
            }

            TryMoveBotAlongDirection(player, dir, 2, out _, out _);
            return true;
        }


        /// <summary>
        /// 近战兜底模块：无论职业是否有技能，只要贴脸就允许攻击；否则继续追击。
        /// 修复：不再要求 ActionList.Count==0，只要 CanAttack 就可以直接攻击。
        /// 原先因为 ActionList 里残留上一帧排队的 DelayedAttack 而被完全跳过的问题已消除。
        /// </summary>
        private static void ProcessBotMeleeCombatAction(PlayerObject player, int dist, MirDirection dir, MagicType attackMagic)
        {
            if (dist <= 1)
            {
                // ★ 只检查 CanAttack（已内含 ActionTime/AttackTime 判断），不再额外限制 PacketWaiting/ActionList
                //   避免上一帧 Attack() 加入 ActionList 后本帧被全部跳过的节奏断档
                if (player.CanAttack && TryStartBotAttackAttempt(player))
                {
                    // 动态更新攻击模式（根据当前场景选择合适的模式）
                    UpdateBotAttackMode(player);

                    player.Direction = dir;
                    player.Attack(dir, attackMagic);

                    _botLastAttackTime[player.ObjectID] = SEnvir.Now;
                }
                return;
            }

            // 追击：距离足够远（≥ A* 启用阈值）时先走路径寻路绕过障碍，否则用方向试探。
            // 这样遇到墙角、走廊等复杂地形时，假人能绕道抵达目标而不是撞墙原地空转。
            if (dist >= BotPathFinder.MinPathfindDistance
                && player.CanMove && !player.PacketWaiting && player.ActionList.Count == 0)
            {
                MapObject chaseTarget = null;
                _botTargets.TryGetValue(player.ObjectID, out chaseTarget);
                if (chaseTarget != null && chaseTarget.Node != null && !chaseTarget.Dead
                    && BotPathFinder.TryUpdateChasePath(player, chaseTarget)
                    && BotPathFinder.TryMoveBotAlongPath(player))
                    return;
            }

            // 近距离或 A* 失败时：按完整路径长度校验 2 格 / 1 格，而不是只看第一格就盲目 Move(2)。
            // 这样目标刚好在 2 格、第二格被怪物/队友占住，或队长第一步前方被队友卡位时，
            // 假人会自动退化成 1 步或侧移，不再原地空转。
            TryMoveBotAlongDirection(player, dir, 2, out _, out _);
        }

        /// <summary>
        /// 在地图上随机取一个可走且不在安全区的坐标。
        /// 先尝试全图随机采样（100次），若全部失败则返回 Point.Empty。
        /// </summary>
        private static Point GetRandomWalkablePoint(Map map, int attempts = 100)
        {
            if (map == null || map.Width <= 0 || map.Height <= 0)
                return Point.Empty;

            for (int i = 0; i < attempts; i++)
            {
                int x = _botRandom.Next(0, map.Width);
                int y = _botRandom.Next(0, map.Height);
                Cell cell = map.GetCell(x, y);
                if (cell == null) continue;
                if (cell.SafeZone != null) continue;  // 排除安全区
                // cell != null 即表示该格子存在于地图（不是障碍墙），可以传送落点
                return new Point(x, y);
            }
            return Point.Empty;
        }

        /// <summary>
        /// 在地图上随机取一个可走、不在安全区、且与 <paramref name="from"/> 点
        /// 曼哈顿距离 ≥ <paramref name="minDist"/> 的坐标。
        /// 先尝试 <paramref name="attempts"/> 次随机采样；若全部失败则返回 Point.Empty。
        /// </summary>
        private static Point GetWalkablePointFarFrom(Map map, Point from, int minDist, int attempts = 150)
        {
            if (map == null || map.Width <= 0 || map.Height <= 0)
                return Point.Empty;

            for (int i = 0; i < attempts; i++)
            {
                int x = _botRandom.Next(0, map.Width);
                int y = _botRandom.Next(0, map.Height);
                if (Math.Abs(x - from.X) + Math.Abs(y - from.Y) < minDist) continue;
                Cell cell = map.GetCell(x, y);
                if (cell == null) continue;
                if (cell.SafeZone != null) continue;
                return new Point(x, y);
            }
            return Point.Empty;
        }



        /// <summary>
        /// 智能漫游方向选择：视野内无目标时，统计8个方向各自象限的怪物密度，
        /// 优先朝怪最多的方向走（提高效率）。
        /// 三成概率引入随机性，避免多个假人都挤到同一个怪堆。
        /// </summary>
        private static MirDirection GetSmartRoamDirection(PlayerObject player)
        {
            BotBehaviorProfile profile = GetBotBehaviorProfile(player);
            int randomPct = Math.Max(12, Math.Min(50, profile?.RoamRandomnessPct ?? 30));

            // 带一点稳定个体差异的随机漫游，避免所有 bot 永远同节奏扎向同一个怪堆。
            if (_botRandom.Next(100) < randomPct)
                return (MirDirection)_botRandom.Next(8);


            // 统计8个方向（每格45°）各自方向上的怪物数量
            int[] dirCount = new int[8];

            foreach (MapObject ob in player.VisibleObjects)
            {
                if (ob == null || ob.Node == null || ob.Dead) continue;
                if (ob.Race != ObjectType.Monster) continue;
                MonsterObject mob = (MonsterObject)ob;
                if (mob.PetOwner != null) continue;
                if (mob.MonsterInfo?.AI < 0) continue;
                if (!player.CanAttackTarget(mob)) continue;

                // 计算该怪在哪个方向扇区
                MirDirection d = Functions.DirectionFromPoint(player.CurrentLocation, mob.CurrentLocation);
                dirCount[(int)d]++;
            }

            // 找怪最多的方向
            int best = 0;
            for (int d = 1; d < 8; d++)
                if (dirCount[d] > dirCount[best]) best = d;

            // 如果视野内没怪，完全随机
            if (dirCount[best] == 0)
                return (MirDirection)_botRandom.Next(8);

            return (MirDirection)best;
        }

        /// <summary>
        /// 绕障最佳方向（仿真人客户端 DirectionBest）：
        /// 当前方向可走就直接用；否则依次尝试左偏1~4、右偏1~4，找第一个可走的方向。
        /// 这里只负责单步方向判断；真正移动时再由 TryMoveBotAlongDirection 校验整段路径长度。
        /// </summary>
        private static MirDirection BotDirectionBest(PlayerObject player, MirDirection dir)
        {
            foreach (MirDirection candidate in EnumerateBotDirectionCandidates(dir))
            {
                if (CanBotTraverseDirection(player, candidate, 1, out _))
                    return candidate;
            }

            return dir; // 全部被阻，保持原方向
        }

        /// <summary>
        /// BFS 向外扩展，找到距离 origin 最近的非安全区格子。
        /// maxRadius 限制搜索半径，防止在超大安全区里无限扩展。
        /// 返回 Point.Empty 表示搜索半径内找不到出口。
        /// 要求落点与安全区边界至少间隔 SafeExitBorderClearance 格，
        /// 避免传送落点紧贴边界后下一帧再次滑入安全区卡住。
        /// </summary>
        private static Point FindNearestNonSafeCell(Map map, Point origin, int maxRadius)
        {
            if (map == null) return Point.Empty;

            var visited = new HashSet<Point>();
            var queue = new Queue<Point>();
            queue.Enqueue(origin);
            visited.Add(origin);

            // 预先获取可走格子的索引，加速判定
            var validCellSet = new HashSet<Point>(map.ValidCells.Select(c => c.Location));

            // ★ 记录找到的第一个非安全区点（边界点），然后继续 BFS 找一个远离边界的点
            Point firstNonSafeCell = Point.Empty;

            // 安全出口与安全区边界的最小间距（格）：≥2格才算"真正离开边界"
            const int SafeExitBorderClearance = 2;

            while (queue.Count > 0)
            {
                Point cur = queue.Dequeue();
                Cell cell = map.GetCell(cur);

                // 格子存在、可走且不在安全区
                if (cell != null && cell.SafeZone == null && validCellSet.Contains(cur))
                {
                    // 第一次找到非安全区点，记录下来（兜底用）
                    if (firstNonSafeCell == Point.Empty)
                        firstNonSafeCell = cur;

                    // 检查这个点是否远离安全区边界（周围 SafeExitBorderClearance 格内都没有安全区格子）
                    bool isFarFromSafeZone = true;
                    for (int dx = -SafeExitBorderClearance; dx <= SafeExitBorderClearance && isFarFromSafeZone; dx++)
                    {
                        for (int dy = -SafeExitBorderClearance; dy <= SafeExitBorderClearance && isFarFromSafeZone; dy++)
                        {
                            if (dx == 0 && dy == 0) continue;
                            Point neighbor = new Point(cur.X + dx, cur.Y + dy);
                            Cell neighborCell = map.GetCell(neighbor);
                            if (neighborCell?.SafeZone != null)
                                isFarFromSafeZone = false;
                        }
                    }

                    // 找到远离边界的非安全区点，直接返回
                    if (isFarFromSafeZone)
                        return cur;
                }

                // 超出搜索半径
                if (Math.Max(Math.Abs(cur.X - origin.X), Math.Abs(cur.Y - origin.Y)) >= maxRadius)
                    continue;

                // 向8个方向扩展
                for (int d = 0; d < 8; d++)
                {
                    Point next = Functions.Move(cur, (MirDirection)d);
                    if (visited.Contains(next)) continue;
                    if (next.X < 0 || next.Y < 0 || next.X >= map.Width || next.Y >= map.Height) continue;
                    visited.Add(next);
                    queue.Enqueue(next);
                }
            }

            // 兜底：如果找不到远离边界的点，返回第一个非安全区点
            return firstNonSafeCell;
        }

        // ══════════════════════════════════════════════════════════════════════
        //  AI – 地图选择辅助（打怪升级地图策略）
        // ══════════════════════════════════════════════════════════════════════

        /// <summary>
        /// 检测地图上是否存在存活的 BOSS 怪物（含普通活跃的 IsBoss=true 的怪）。
        /// 有 BOSS 的地图禁止假人进入，避免被秒。
        /// </summary>
        private static bool MapHasBoss(Map map)
        {
            if (map == null) return false;
            foreach (MapObject ob in map.Objects)
            {
                if (ob == null || ob.Node == null || ob.Dead) continue;
                if (ob.Race != ObjectType.Monster) continue;
                MonsterObject mob = (MonsterObject)ob;
                if (mob.MonsterInfo != null && mob.MonsterInfo.IsBoss)
                    return true;
            }
            return false;
        }

        private static bool MapHasBossAboveLevel(Map map, int levelThreshold)
        {
            if (map?.Info == null) return false;

            int count = 0;

            // 检查刷新配置中的 BOSS
            foreach (RespawnInfo respawn in SEnvir.RespawnInfoList.Binding)
            {
                if (respawn?.Region?.Map != map.Info) continue;

                MonsterInfo monster = respawn.Monster;
                if (monster == null || !monster.IsBoss) continue;
                if (monster.Level > levelThreshold)
                {
                    count++;
                    if (count >= 3) return true;
                }
            }

            // 检查地图上已生成的 BOSS
            foreach (MapObject ob in map.Objects)
            {
                if (ob == null || ob.Node == null || ob.Dead) continue;
                if (ob.Race != ObjectType.Monster) continue;

                MonsterObject mob = (MonsterObject)ob;
                MonsterInfo info = mob.MonsterInfo;
                if (info == null || !info.IsBoss) continue;
                if (Math.Max(mob.Level, info.Level) > levelThreshold)
                {
                    count++;
                    if (count >= 3) return true;
                }
            }

            return false;
        }

        private static bool ShouldBotPreheatUpcomingHighBossMap(PlayerObject player, Map targetMap, int currentScore, int bestScore, int switchMargin, bool forceSwitch)
        {
            if (!Config.BotAllowGroup) return false;
            if (player?.Node == null || player.Dead) return false;
            if (!IsBotHighLevelBossMap(targetMap)) return false;
            if (ShouldBotEmergencyGoldFarm(player)) return false;

            if (player.GroupMembers != null && player.GroupMembers.Count > 0 && player.GroupMembers[0] != player)
                return false;

            if (forceSwitch || currentScore == int.MinValue)
                return true;

            return bestScore != int.MinValue
                   && bestScore + BotHighBossGroupPreheatScoreBuffer >= currentScore + switchMargin;
        }

        private static void ResetBotMapStayState(PlayerObject player, Map map, DateTime now)
        {
            if (player == null) return;

            uint pid = player.ObjectID;
            if (map?.Info == null)
            {
                _botMapStayMapIndex.Remove(pid);
                _botMapStayStartTime.Remove(pid);
                return;
            }

            _botMapStayMapIndex[pid] = map.Info.Index;
            _botMapStayStartTime[pid] = now;
        }

        private static bool ShouldForceRotateBotFarmMap(PlayerObject player, DateTime now, out DateTime staySince)
        {
            staySince = now;
            if (player?.CurrentMap?.Info == null)
                return false;

            uint pid = player.ObjectID;
            int currentMapIndex = player.CurrentMap.Info.Index;
            if (!_botMapStayMapIndex.TryGetValue(pid, out int trackedMapIndex) || trackedMapIndex != currentMapIndex)
            {
                ResetBotMapStayState(player, player.CurrentMap, now);
                return false;
            }

            if (!_botMapStayStartTime.TryGetValue(pid, out staySince))
            {
                ResetBotMapStayState(player, player.CurrentMap, now);
                staySince = now;
                return false;
            }

            if (MapHasBossAboveLevel(player.CurrentMap, BotHighLevelBossThreshold))
                return false;

            return (now - staySince).TotalSeconds >= BotLowTierFarmMapStaySeconds;
        }

        private struct BotMapMonsterProfile
        {
            public int Count;
            public int AverageLevel;
            public int AverageAttack;
            public int MaxAttack;
            public int AverageAccuracy;
            public int MaxAccuracy;
        }

        /// <summary>
        /// 统计地图普通怪画像：优先取当前存活野怪；若地图暂时刷空，则回退到刷新配置，
        /// 避免手动/强制切图时因为某张图瞬间没活怪而误判成“无地图可去”。
        /// </summary>
        private static bool TryGetMapMonsterProfile(Map map, out BotMapMonsterProfile profile)
        {
            profile = default(BotMapMonsterProfile);
            if (map == null) return false;

            long totalLevel = 0;
            long totalAttack = 0;
            long totalAccuracy = 0;
            int maxAttack = 0;
            int maxAccuracy = 0;
            int count = 0;

            foreach (MapObject ob in map.Objects)
            {
                if (ob == null || ob.Node == null || ob.Dead) continue;
                if (ob.Race != ObjectType.Monster) continue;

                MonsterObject mob = (MonsterObject)ob;
                MonsterInfo info = mob.MonsterInfo;
                if (info == null) continue;
                if (info.IsBoss) continue;
                if (mob.PetOwner != null) continue;
                if (info.AI < 0) continue;

                int attack = Math.Max(0, Math.Max(info.Stats[Stat.MaxDC], info.Stats[Stat.MinDC]));
                int accuracy = Math.Max(0, info.Stats[Stat.Accuracy]);

                totalLevel += mob.Level;
                totalAttack += attack;
                totalAccuracy += accuracy;
                if (attack > maxAttack) maxAttack = attack;
                if (accuracy > maxAccuracy) maxAccuracy = accuracy;
                count++;
            }

            if (count == 0)
            {
                foreach (RespawnInfo respawn in SEnvir.RespawnInfoList.Binding)
                {
                    if (respawn?.Region?.Map != map.Info) continue;

                    MonsterInfo info = respawn.Monster;
                    if (info == null || info.IsBoss || info.AI < 0) continue;

                    int spawnCount = Math.Max(1, respawn.Count);
                    int attack = Math.Max(0, Math.Max(info.Stats[Stat.MaxDC], info.Stats[Stat.MinDC]));
                    int accuracy = Math.Max(0, info.Stats[Stat.Accuracy]);

                    totalLevel += (long)Math.Max(1, info.Level) * spawnCount;
                    totalAttack += (long)attack * spawnCount;
                    totalAccuracy += (long)accuracy * spawnCount;
                    if (attack > maxAttack) maxAttack = attack;
                    if (accuracy > maxAccuracy) maxAccuracy = accuracy;
                    count += spawnCount;
                }
            }

            if (count == 0) return false;

            profile = new BotMapMonsterProfile
            {
                Count = count,
                AverageLevel = (int)(totalLevel / count),
                AverageAttack = (int)(totalAttack / count),
                MaxAttack = maxAttack,
                AverageAccuracy = (int)(totalAccuracy / count),
                MaxAccuracy = maxAccuracy,
            };
            return true;
        }


        /// <summary>
        /// 计算地图上所有存活普通野怪的平均等级。
        /// 返回 -1 表示地图上没有符合条件的怪物（空旷地图）。
        /// </summary>
        private static int GetMapAverageMonsterLevel(Map map)
        {
            BotMapMonsterProfile profile;
            return TryGetMapMonsterProfile(map, out profile) ? profile.AverageLevel : -1;
        }

        private static Point GetBotPreferredProgressionPoint(Map map, PlayerObject player)
        {
            if (map?.Info == null || player == null) return Point.Empty;

            if (TryGetBotPriorityMissingSkills(player, out List<MagicInfo> missingSkills))
            {
                Point bestSkillPoint = Point.Empty;
                int bestSkillScore = 0;

                foreach (RespawnInfo respawn in SEnvir.RespawnInfoList.Binding)
                {
                    if (respawn?.Region?.Map != map.Info) continue;

                    MonsterInfo monster = respawn.Monster;
                    if (monster == null || monster.AI < 0) continue;

                    // 打书模式下，BOSS 也参与技能书掉落评估
                    int skillScore = GetBotMissingSkillMonsterDropScore(player, monster, missingSkills);
                    if (skillScore <= 0) continue;

                    Point center = new Point(respawn.MapX, respawn.MapY);
                    Point dest = FindNearestNonSafeCell(map, center, Math.Max(8, respawn.Range + 4));
                    if (dest == Point.Empty) continue;

                    skillScore *= Math.Max(1, respawn.Count);
                    if (skillScore > bestSkillScore)
                    {
                        bestSkillScore = skillScore;
                        bestSkillPoint = dest;
                    }
                }

                if (bestSkillPoint != Point.Empty)
                    return bestSkillPoint;
            }

            string[] keywords = GetBotPreferredMonsterKeywords(player);
            if (keywords == null || keywords.Length == 0) return Point.Empty;

            foreach (RespawnInfo respawn in SEnvir.RespawnInfoList.Binding)
            {
                if (respawn?.Region?.Map != map.Info) continue;

                MonsterInfo monster = respawn.Monster;
                if (monster == null || monster.IsBoss || monster.AI < 0) continue;
                if (!IsBotMonsterNameMatch(monster.MonsterName, keywords)) continue;

                Point center = new Point(respawn.MapX, respawn.MapY);
                Point dest = FindNearestNonSafeCell(map, center, Math.Max(8, respawn.Range + 4));
                if (dest != Point.Empty)
                    return dest;
            }

            return Point.Empty;
        }

        /// <summary>
        /// 综合玩家等级、血量、防御、敏捷与地图怪物画像，给地图打分。
        /// 返回 int.MinValue 表示该地图对当前假人不安全或不合规。
        /// </summary>
        private static int GetBotMapScore(Map map, PlayerObject player, out int avgMonsterLevel, out int dangerScore)
        {
            GetBotGoldFarmContext(player, out bool goldFarmMode, out bool emergencyGoldFarmMode);
            return GetBotMapScore(map, player, goldFarmMode, emergencyGoldFarmMode, out avgMonsterLevel, out dangerScore);
        }

        private static int GetBotMapScore(Map map, PlayerObject player, bool goldFarmMode, bool emergencyGoldFarmMode, out int avgMonsterLevel, out int dangerScore)
        {
            avgMonsterLevel = -1;
            dangerScore = int.MaxValue;

            if (map == null || map.Info == null || player == null) return int.MinValue;
            if (map.Info.IsDynamic) return int.MinValue;
            if (map.Info.BanAndroidPlayer) return int.MinValue;
            if (map.Info.MinimumLevel > 0 && map.Info.MinimumLevel > player.Level) return int.MinValue;

            // ══════════════════════════════════════════════════════════════════════
            //  打书模式：允许进入特定 BOSS 图打高级技能书
            // ══════════════════════════════════════════════════════════════════════
            bool prioritySkillFarm = TryGetBotPriorityMissingSkills(player, out List<MagicInfo> missingSkills);
            bool allowBossMapForSkillFarm = prioritySkillFarm && IsBotHighSkillBookMap(map);

            // 非 BOSS 模式：过滤掉有 BOSS 的地图（避免被秒）
            // 打书模式：只允许进入指定的高级技能书 BOSS 图
            if (MapHasBoss(map) && !allowBossMapForSkillFarm)
            {
                return int.MinValue;
            }

            if (ShouldBotAvoidTownBigMap(player, goldFarmMode) && IsBotTownBigMap(map)) return int.MinValue;

            BotMapMonsterProfile profile;
            if (!TryGetMapMonsterProfile(map, out profile))
                return int.MinValue;

            avgMonsterLevel = profile.AverageLevel;
            if (profile.AverageLevel > player.Level + BotMapLevelTolerance)
                return int.MinValue;

            if (emergencyGoldFarmMode && player.Level >= 8 && profile.AverageLevel >= player.Level)
                return int.MinValue;

            int maxHP = Math.Max(1, player.Stats[Stat.Health]);
            int avgAC = Math.Max(0, (player.Stats[Stat.MinAC] + player.Stats[Stat.MaxAC]) / 2);
            int avgMR = Math.Max(0, (player.Stats[Stat.MinMR] + player.Stats[Stat.MaxMR]) / 2);
            int playerDefense = Math.Max(0, (avgAC * 2 + avgMR) / 3);
            int conservativeDefense = Math.Max(0, Math.Min(avgAC, avgMR));
            int playerAgility = Math.Max(0, player.Stats[Stat.Agility]);
            int mapDamageBonus = Math.Max(0, Math.Max(map.Info.MonsterDamage, map.Info.MaxMonsterDamage));

            int scaledAvgAttack = profile.AverageAttack * (100 + mapDamageBonus) / 100;
            int scaledMaxAttack = profile.MaxAttack * (100 + mapDamageBonus) / 100;
            int effectiveAvgDamage = Math.Max(1, scaledAvgAttack - playerDefense);
            int effectivePeakDamage = Math.Max(1, scaledMaxAttack - conservativeDefense);
            int avgAccuracyGap = Math.Max(0, profile.AverageAccuracy - playerAgility);
            int peakAccuracyGap = Math.Max(0, profile.MaxAccuracy - playerAgility);

            if (effectiveAvgDamage * BotMapSafeAverageHits > maxHP) return int.MinValue;
            if (effectivePeakDamage * BotMapSafePeakHits > maxHP) return int.MinValue;
            if (peakAccuracyGap > BotMapMaxAccuracyGap) return int.MinValue;

            dangerScore = effectiveAvgDamage * 100 / maxHP
                        + effectivePeakDamage * 100 / maxHP
                        + avgAccuracyGap * 2
                        + peakAccuracyGap * 3
                        + Math.Max(0, profile.AverageLevel - player.Level) * 15
                        + mapDamageBonus / 5;

            int experienceRate = Math.Max(1, Math.Max(map.Info.ExperienceRate, map.Info.MaxExperienceRate));
            int dropRate = Math.Max(1, Math.Max(map.Info.DropRate, map.Info.MaxDropRate));
            int goldRate = Math.Max(1, Math.Max(map.Info.GoldRate, map.Info.MaxGoldRate));

            double dropValueScore = 0;
            int respawnMonsterCount = 0;
            double respawnArea = 0;
            int nurseryMonsterCount = 0;
            int outskirtsMonsterCount = 0;
            int missingSkillRespawnScore = 0;
            bool hasMissingSkillRespawn = false;

            foreach (RespawnInfo respawn in SEnvir.RespawnInfoList.Binding)
            {
                if (respawn?.Region?.Map != map.Info) continue;

                MonsterInfo monster = respawn.Monster;
                if (monster == null || monster.AI < 0) continue;

                // 统计 BOSS 的技能书掉落（打书模式需要）
                // 注意：怪物计数和密度统计仍然跳过 BOSS，以避免影响地图评估
                bool isBoss = monster.IsBoss;
                int spawnCount = Math.Max(1, respawn.Count);

                if (!isBoss)
                {
                    int spawnRange = Math.Max(1, respawn.Range);
                    respawnMonsterCount += spawnCount;
                    respawnArea += Math.Max(1, spawnRange * spawnRange);

                    if (IsBotMonsterNameMatch(monster.MonsterName, BotSafeNurseryMonsterKeywords))
                        nurseryMonsterCount += spawnCount;
                    if (IsBotMonsterNameMatch(monster.MonsterName, BotTownOutskirtsMonsterKeywords))
                        outskirtsMonsterCount += spawnCount;
                }

                if (prioritySkillFarm)
                {
                    int skillScore = GetBotMissingSkillMonsterDropScore(player, monster, missingSkills);
                    if (skillScore > 0)
                    {
                        hasMissingSkillRespawn = true;
                        missingSkillRespawnScore += skillScore * spawnCount;
                    }
                }

                double monsterDropScore = Math.Log10(Math.Max(10, monster.Level + 10));
                foreach (DropInfo drop in monster.Drops)
                {
                    if (drop?.Item == null) continue;

                    long itemValue = Math.Max(1, drop.Item.Price) * Math.Max(1, drop.Amount);
                    double chanceFactor = Math.Log10(Math.Max(10, drop.Chance));
                    double valueFactor = Math.Log10(itemValue + 10);
                    double partFactor = drop.PartOnly ? 0.65 : 1.0;

                    monsterDropScore += chanceFactor * valueFactor * partFactor;
                }

                dropValueScore += monsterDropScore * spawnCount;
            }

            double density = respawnArea > 0 ? respawnMonsterCount / respawnArea : Math.Max(1, profile.Count);
            int lootScore = (int)Math.Max(0, Math.Min(120, Math.Round(dropValueScore * dropRate / 100.0)));
            int distributionScore = respawnMonsterCount > 0
                ? Math.Max(-15, Math.Min(25, (int)Math.Round(20 - density * 30)))
                : 0;

            BotProgressionStage stage = GetBotProgressionStage(player);
            int farmingScore = 80
                             - Math.Abs(profile.AverageLevel - player.Level) * 12
                             + experienceRate / 10
                             + Math.Min(20, profile.Count / 4)
                             + lootScore / 2
                             + distributionScore;

            switch (stage)
            {
                case BotProgressionStage.SafeNursery:
                    if (!map.HasSafeZone || nurseryMonsterCount <= 0)
                        return int.MinValue;

                    farmingScore += 220 + Math.Min(80, nurseryMonsterCount * 4) + Math.Min(40, experienceRate / 5);
                    dangerScore += Math.Max(0, profile.AverageLevel - 8) * 35;
                    break;
                case BotProgressionStage.TownOutskirts:
                    if (!map.HasSafeZone || outskirtsMonsterCount <= 0)
                        return int.MinValue;

                    farmingScore += 180 + Math.Min(70, outskirtsMonsterCount * 3) + Math.Min(35, nurseryMonsterCount * 2);
                    dangerScore += Math.Max(0, profile.AverageLevel - 18) * 22;
                    break;
                case BotProgressionStage.MixedLevelAndBooks:
                    farmingScore += experienceRate / 8 + lootScore / 2 + dropRate / 16;
                    break;
                case BotProgressionStage.LevelRush:
                    farmingScore += experienceRate / 3 + Math.Min(60, profile.Count / 2) + Math.Max(0, profile.AverageLevel - 25) * 4;
                    farmingScore += lootScore / 6;
                    break;
                case BotProgressionStage.HighBookFarm:
                    farmingScore += lootScore * 2 + dropRate / 4 + Math.Max(0, profile.AverageLevel - 40) * 6;
                    farmingScore -= Math.Max(0, 45 - profile.AverageLevel) * 12;
                    break;
                case BotProgressionStage.LateLevelRush:
                    farmingScore += experienceRate / 3 + Math.Min(80, profile.Count / 2) + Math.Max(0, profile.AverageLevel - 50) * 5;
                    farmingScore += lootScore / 8;
                    break;
            }

            if (emergencyGoldFarmMode)
            {
                int desiredLevelGap = Math.Max(2, Math.Min(BotEmergencyGoldFarmPreferredLevelGap, Math.Max(2, player.Level / 3)));
                int actualLevelGap = Math.Max(0, player.Level - profile.AverageLevel);
                int levelGapBonus = Math.Min(160, actualLevelGap * 16);
                int levelGapPenalty = Math.Max(0, desiredLevelGap - actualLevelGap) * 28;

                farmingScore += lootScore + goldRate / 6 + distributionScore * 2 + levelGapBonus - levelGapPenalty;
                dangerScore = dangerScore * 2
                            + effectiveAvgDamage * 100 / maxHP
                            + effectivePeakDamage * 100 / maxHP
                            + avgAccuracyGap * 4
                            + peakAccuracyGap * 6;
            }
            else if (goldFarmMode)
            {
                int desiredLevelGap = Math.Max(1, Math.Min(BotGoldFarmPreferredLevelGap, Math.Max(1, player.Level / 15)));
                int desiredFarmLevel = Math.Max(1, player.Level - desiredLevelGap);
                int levelFitBonus = Math.Max(-90, 120 - Math.Abs(profile.AverageLevel - desiredFarmLevel) * 18);
                int vendorValueBonus = lootScore * 2 + dropRate / 6 + goldRate / 10;
                int higherValueLootBonus = Math.Min(80, Math.Max(0, profile.AverageLevel - Math.Max(8, player.Level / 3)) * 4);

                farmingScore += vendorValueBonus + distributionScore * 2 + levelFitBonus + higherValueLootBonus;
            }
            else
            {
                farmingScore += lootScore / 3 + goldRate / 20;
            }

            if (prioritySkillFarm)
            {
                if (hasMissingSkillRespawn)
                {
                    // 基础打书评分
                    int skillFarmScore = 4000 + Math.Min(8000, missingSkillRespawnScore / 2);

                    // 高级技能书地图（BOSS 图）额外加分
                    if (IsBotHighSkillBookMap(map))
                    {
                        skillFarmScore += 2000;  // BOSS 图额外加分
                        dangerScore = Math.Max(0, dangerScore - 40);  // 进一步降低危险感知
                    }
                    else
                    {
                        dangerScore = Math.Max(0, dangerScore - 25);
                    }

                    farmingScore += skillFarmScore;

                farmingScore = skillFarmScore;
            }
            else
            {
                farmingScore -= 1500;  // 没有技能书掉落的地图惩罚加重
            }
            }

            farmingScore += GetBotRuntimeMapScoreAdjustment(player, map);
            return farmingScore * 2 - dangerScore;

        }

        /// <summary>
        /// 判断某地图是否适合当前假人打怪：除了等级和 BOSS 过滤，还会结合假人的扛伤与闪避能力评估风险。
        /// </summary>
        private static bool IsMapSuitableForBot(Map map, PlayerObject player)
        {
            int avgMonsterLevel;
            int dangerScore;
            return GetBotMapScore(map, player, out avgMonsterLevel, out dangerScore) != int.MinValue;
        }

        /// <summary>
        /// 从所有已加载的地图中，为 <paramref name="player"/> 选一张更适合当前等级与身板的打怪地图，
        /// 并返回该地图中一个随机可行走、非安全区的坐标。
        /// 如果找不到合适地图，返回 (null, Point.Empty)。
        /// </summary>
        private static (Map map, Point point) FindSuitableMapForBot(PlayerObject player)
        {
            GetBotGoldFarmContext(player, out bool goldFarmMode, out bool emergencyGoldFarmMode);
            return FindSuitableMapForBot(player, goldFarmMode, emergencyGoldFarmMode, false);
        }

        private static (Map map, Point point) FindSuitableMapForBot(PlayerObject player, bool goldFarmMode, bool emergencyGoldFarmMode, bool lowTierRotationOnly = false)
        {
            List<BotManualMapSwitchCandidate> candidates = new List<BotManualMapSwitchCandidate>();

            foreach (KeyValuePair<MapInfo, Map> kv in SEnvir.Maps)
            {
                Map m = kv.Value;
                if (m == player.CurrentMap) continue;
                if (lowTierRotationOnly && MapHasBossAboveLevel(m, BotHighLevelBossThreshold)) continue;

                int avgMonsterLevel;
                int dangerScore;
                int score = GetBotMapScore(m, player, goldFarmMode, emergencyGoldFarmMode, out avgMonsterLevel, out dangerScore);
                if (score == int.MinValue) continue;

                Point dest = GetBotPreferredProgressionPoint(m, player);
                if (dest == Point.Empty)
                    dest = GetRandomWalkablePoint(m);
                if (dest == Point.Empty) continue;

                candidates.Add(new BotManualMapSwitchCandidate
                {
                    Map = m,
                    Point = dest,
                    Score = score,
                    Danger = dangerScore,
                });
            }

            if (candidates.Count == 0)
                return (null, Point.Empty);

            int bestScore = candidates.Max(x => x.Score);
            int gap = Math.Max(0, Config.BotMapSwitchScoreGapMax);
            List<BotManualMapSwitchCandidate> pool = candidates
                .Where(x => x.Score >= bestScore - gap)
                .ToList();

            BotManualMapSwitchCandidate selected = gap > 0
                ? pool[_botRandom.Next(pool.Count)]
                : pool.OrderByDescending(x => x.Score).ThenBy(x => x.Danger).First();

            return (selected.Map, selected.Point);
        }

        // ══════════════════════════════════════════════════════════════════════
        //  AI – 自动拾取地面物品（仿宠物 Companion 逻辑）
        // ══════════════════════════════════════════════════════════════════════

        /// <summary>
        /// 自动拾取逻辑（参考宠物 Companion.ProcessSearch / ProcessTarget）：
        ///
        ///   ★ 战斗优先（正常情况）：有锁定怪物目标时跳过拾取（仿真人挂机：打怪 > 捡装）
        ///   ★ 怪死后拾取优先：目标死亡后进入"等待拾取"状态，优先捡光掉落物再继续攻击
        ///   1. 维持 / 验证跨Tick锁定的目标物品（失效：已消失 / 换地图 / 超出视野）
        ///   2. 无目标时扫描 VisibleObjects，选距离最近的、属于自己账号的怪物掉落物品
        ///   3. 有目标 → BotDirectionBest 移动到物品格；到达后调用 item.PickUpItem(player)
        ///   4. 等待拾取状态且视野内无可捡物品 → 解除等待状态（本Tick通知战斗可继续）
        /// </summary>
        private static void ProcessBotPickUp(PlayerObject player)
        {
            if (player == null || player.Dead || !Config.BotAutoPickup) return;

            GetBotGroupLeaderContext(player, out PlayerObject _, out bool hasHumanLeader);
            if (Config.BotSkipPickupWhenGroupedWithHuman && hasHumanLeader)
                return;
            if (!TryStartBotPickupAttempt(player))
                return;

            bool waitingPickup = _botWaitingPickup.ContainsKey(player.ObjectID);
            bool emergencyPickupMode = ShouldBotPrioritizeEmergencyPickup(player, out ItemObject emergencyPickupTarget);
            if (emergencyPickupMode && HasBotImmediateCombatTarget(player))
            {
                emergencyPickupMode = false;
                emergencyPickupTarget = null;
            }

            // ★ 常规战斗优先：有锁定怪物目标时跳过拾取（仿真人挂机：打怪 > 捡装）
            // 例外 1：怪物刚死进入等待拾取状态时，忽略此限制，优先把掉落物捡完
            // 例外 2：金币=0 且背包无药时，只要脚边/附近有可捡掉落，就先捡再打
            if (!waitingPickup && _botTargets.ContainsKey(player.ObjectID) && !emergencyPickupMode) return;

            if (emergencyPickupMode)
            {
                ClearBotPendingCombatActions(player);
                player.PacketWaiting = false;
            }

            // ── Step 1：验证当前锁定物品是否仍有效；被怪占位就立刻换目标 ────────
            _botTargetItems.TryGetValue(player.ObjectID, out ItemObject targetItem);
            if (!IsValidBotPickupTarget(player, targetItem)
                || IsBotPickupLocationBlocked(player, targetItem))
            {
                targetItem = null;
                _botTargetItems.Remove(player.ObjectID);
            }

            if (targetItem == null && emergencyPickupTarget != null)
            {
                targetItem = emergencyPickupTarget;
                _botTargetItems[player.ObjectID] = targetItem;
            }

            // ── Step 2：无目标时扫描最近可捡物品（仿 Companion.ProcessSearch）──
            if (targetItem == null)
            {
                if (TryGetNearestBotPickableDrop(player, out targetItem,
                    Math.Max(0, Config.BotPickupRadius)))
                    _botTargetItems[player.ObjectID] = targetItem;
            }

            // ── Step 2b：等待拾取中但视野内无可捡物品 → 解除等待，让战斗继续 ──
            if (targetItem == null && waitingPickup)
            {
                _botWaitingPickup.Remove(player.ObjectID);
                return;
            }

            // ── Step 3：有目标 → 移动过去 / 到达后捡取（仿 Companion.ProcessTarget）──
            if (targetItem == null) return;

            if (targetItem.CurrentLocation == player.CurrentLocation)
            {
                // 已到达物品格 → 直接调用服务端拾取
                targetItem.PickUpItem(player);
                RecordBotPickup(player, targetItem);
                _botTargetItems.Remove(player.ObjectID);
                // 捡完后继续扫描（下一 Tick 会重新查找剩余物品，若无则自动解除等待状态）
            }

            else if (player.CanMove)
            {
                // 优先跑向掉落物；只剩一格时精确落点。如果第一步都走不出去，直接飞到掉落格。
                MirDirection dir = Functions.DirectionFromPoint(player.CurrentLocation, targetItem.CurrentLocation);
                int pickupDistance = Math.Min(2, MaxChebyshevDistance(player.CurrentLocation, targetItem.CurrentLocation));
                if (!TryMoveBotAlongDirection(player, dir, pickupDistance, out _, out _)
                    && TryTeleportBotToPickupTarget(player, targetItem)
                    && IsValidBotPickupTarget(player, targetItem)
                    && targetItem.CurrentLocation == player.CurrentLocation)
                {
                    targetItem.PickUpItem(player);
                    RecordBotPickup(player, targetItem);
                    _botTargetItems.Remove(player.ObjectID);
                }

            }
        }

        
    }
}
