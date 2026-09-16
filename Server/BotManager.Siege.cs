using Library;
using Library.SystemModels;
using Server.DBModels;
using Server.Models;
using Server.Models.Monsters;

using System;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;
using S = Library.Network.ServerPackets;

namespace Server.Envir
{
    public static partial class BotManager
    {
        // ══════════════════════════════════════════════════════════════════════
        //  攻城战智能策略系统
        // ══════════════════════════════════════════════════════════════════════

        /// <summary>
        /// 攻城战术类型
        /// </summary>
        private enum BotSiegeStrategy
        {
            /// <summary>正面强攻：优先破城门，逐个清理守卫，最后打城主</summary>
            FrontalAssault,

            /// <summary>侧翼偷袭：复活后直插城主/旗帜点，不纠结城门</summary>
            FlankingAssault,

            /// <summary>防守反击：己方占领城堡时优先守城门</summary>
            DefensiveCounterAttack,

            /// <summary>分兵突击：70%正面 + 30%侧翼（已用 SplitAssault 分配标记）</summary>
            SplitAssault
        }

        /// <summary>
        /// 攻城会话类型
        /// </summary>
        private enum BotSiegeChatType
        {
            StrategyAnnounce,      // 战术宣布（攻城开始前）
            DefenseReminder,       // 防守提醒（防守方）
            GateBroken,            // 城门被破
            IntruderAlert,         // 发现偷袭者
            VictoryAnnounce,       // 占领成功
            RetryAttack            // 重新组织进攻
        }

        // ── 状态字典 ──

        /// <summary>假人攻城策略（按 ObjectID 存储，每场攻城分配一次）</summary>
        private static readonly Dictionary<uint, BotSiegeStrategy> _botSiegeStrategies
            = new Dictionary<uint, BotSiegeStrategy>();

        /// <summary>假人攻城会话冷却时间（按行会名称存储，避免刷屏）</summary>
        private static readonly Dictionary<string, DateTime> _guildSiegeChatCooldown
            = new Dictionary<string, DateTime>();

        /// <summary>城门上一次状态（用于检测城门被破事件）：MapIndex → Direction</summary>
        private static readonly Dictionary<int, MirDirection> _lastGateDirection
            = new Dictionary<int, MirDirection>();

        // ── 配置常量 ──

        /// <summary>攻城会话冷却时间（秒）</summary>
        private const int BotSiegeChatCooldownSeconds = 45;

        /// <summary>分兵突击时突击小队比例（30%）</summary>
        private const double BotSplitAssaultRatio = 0.3;

        /// <summary>分兵突击所需最低在线行会成员数</summary>
        private const int BotSiegeMemberCountForSplit = 15;

        /// <summary>城门低血量阈值（HP%）：低于此值视为"城门防御弱"</summary>
        private const double BotGateWeakHpPercent = 40;

        // ══════════════════════════════════════════════════════════════════════
        //  策略决策
        // ══════════════════════════════════════════════════════════════════════

        /// <summary>
        /// 为假人决定攻城策略。每场攻城只分配一次，后续直接读缓存。
        /// </summary>
        private static BotSiegeStrategy DetermineBotSiegeStrategy(PlayerObject player, ConquestWar war)
        {
            if (player == null || war == null)
                return BotSiegeStrategy.FrontalAssault;

            uint pid = player.ObjectID;
            if (_botSiegeStrategies.TryGetValue(pid, out BotSiegeStrategy cached))
                return cached;

            // 防守方：己方行会占领此城堡 → 防守反击
            GuildInfo guild = player.Character?.Account?.GuildMember?.Guild;
            if (guild != null && guild.Castle == war.info)
            {
                _botSiegeStrategies[pid] = BotSiegeStrategy.DefensiveCounterAttack;
                return BotSiegeStrategy.DefensiveCounterAttack;
            }

            // 攻城方：根据行会在线人数和城门状态选择
            int onlineCount = GetGuildOnlineMemberCount(guild);

            if (onlineCount >= BotSiegeMemberCountForSplit && SEnvir.Random.Next(100) < 25)
            {
                // 人数充足时，按比例分配正面/侧翼（用 SplitAssault 标记，实际分配在下面）
                bool isFlanker = SEnvir.Random.NextDouble() < BotSplitAssaultRatio;
                BotSiegeStrategy strategy = isFlanker
                    ? BotSiegeStrategy.FlankingAssault
                    : BotSiegeStrategy.FrontalAssault;

                _botSiegeStrategies[pid] = strategy;
                return strategy;
            }

            // 城门血量低 → 侧翼偷袭概率高
            if (IsGateWeakOnMap(war.Map) && SEnvir.Random.Next(100) < 35)
            {
                _botSiegeStrategies[pid] = BotSiegeStrategy.FlankingAssault;
                return BotSiegeStrategy.FlankingAssault;
            }

            // 默认：正面强攻
            _botSiegeStrategies[pid] = BotSiegeStrategy.FrontalAssault;
            return BotSiegeStrategy.FrontalAssault;
        }

        /// <summary>
        /// 获取行会在线成员数（在攻城地图上的不算，只算总在线）
        /// </summary>
        private static int GetGuildOnlineMemberCount(GuildInfo guild)
        {
            if (guild?.Members == null) return 0;
            return guild.Members.Count(m => m.Account?.Connection?.Player != null);
        }

        /// <summary>
        /// 判断攻城地图上城门是否处于低血量状态（HP% &lt; 40%）
        /// </summary>
        private static bool IsGateWeakOnMap(Map map)
        {
            if (map == null) return false;

            foreach (MapObject obj in map.Objects)
            {
                if (obj is SabukPrimeGate gate && !gate.Dead && gate.Stats != null && gate.Stats[Stat.Health] > 0)
                {
                    double hpPercent = (1d * gate.CurrentHP) / gate.Stats[Stat.Health] * 100d;
                    return hpPercent < BotGateWeakHpPercent;
                }
            }
            return false;
        }

        /// <summary>
        /// 判断攻城地图上城门是否已破（Direction == UpLeft 或 Dead）
        /// </summary>
        private static bool IsGateDestroyed(Map map)
        {
            if (map == null) return false;

            foreach (MapObject obj in map.Objects)
            {
                if (obj is SabukPrimeGate gate)
                {
                    return gate.Dead || gate.Direction == MirDirection.UpLeft;
                }
            }
            return true; // 没有城门 = 城门不存在，视为已破
        }

        // ══════════════════════════════════════════════════════════════════════
        //  基于策略的目标选择
        // ══════════════════════════════════════════════════════════════════════

        /// <summary>
        /// 基于当前攻城策略选择优先目标（替代原有 FindBotConquestPriorityTarget 的固定逻辑）。
        /// 策略不同则目标优先级不同。
        /// </summary>
        private static MapObject FindBotSiegeStrategyTarget(PlayerObject player, ConquestWar war, BotSiegeStrategy strategy)
        {
            if (player?.VisibleObjects == null || war == null) return null;

            MapObject bestTarget = null;
            long bestScore = long.MinValue;

            foreach (MapObject visible in player.VisibleObjects)
            {
                long score = GetSiegeStrategyTargetScore(player, war, visible, strategy);
                if (score <= bestScore) continue;

                bestScore = score;
                bestTarget = visible;
            }

            return bestTarget;
        }

        /// <summary>
        /// 根据攻城策略计算目标的优先级分数
        /// </summary>
        private static long GetSiegeStrategyTargetScore(PlayerObject player, ConquestWar war, MapObject target, BotSiegeStrategy strategy)
        {
            if (player == null || war == null || target == null || target.Node == null || target.Dead)
                return long.MinValue;
            if (player.CurrentMap != war.Map || target.CurrentMap != war.Map)
                return long.MinValue;
            if (!Functions.InRange(player.CurrentLocation, target.CurrentLocation, Config.MaxViewRange))
                return long.MinValue;

            int distance = MaxChebyshevDistance(player.CurrentLocation, target.CurrentLocation);

            switch (target)
            {
                case PlayerObject hostilePlayer:
                    if (!player.CanAttackTarget(hostilePlayer))
                        return long.MinValue;

                    return GetSiegePlayerScore(player, hostilePlayer, distance, strategy);

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

                    return GetSiegeMonsterScore(player, monster, distance, strategy);

                default:
                    return long.MinValue;
            }
        }

        /// <summary>
        /// 根据策略计算敌方玩家的分数
        /// </summary>
        private static long GetSiegePlayerScore(PlayerObject player, PlayerObject hostile, int distance, BotSiegeStrategy strategy)
        {
            bool attacker = player.IsWarAttacker();
            long score = 280_000L - distance * 2_000L - hostile.CurrentHP;

            if (ReferenceEquals(player.LastHitter, hostile))
                score += 260_000L;
            if (distance <= 2)
                score += 120_000L;

            // 防守方：城门附近的进攻方玩家优先级提高
            if (strategy == BotSiegeStrategy.DefensiveCounterAttack)
            {
                // 防守方优先清理靠近城门的敌人
                if (IsNearGate(player.CurrentMap, hostile.CurrentLocation, 10))
                    score += 150_000L;
            }

            // 侧翼偷袭：忽略远处敌人，专注核心目标
            if (strategy == BotSiegeStrategy.FlankingAssault)
            {
                score -= 80_000L; // 降低敌对玩家优先级，让城主/旗帜得分更高
            }

            return score;
        }

        /// <summary>
        /// 根据策略计算怪物的分数
        /// </summary>
        private static long GetSiegeMonsterScore(PlayerObject player, MonsterObject monster, int distance, BotSiegeStrategy strategy)
        {
            bool attacker = player.IsWarAttacker();

            // 防守方不攻击守卫和城门
            if (!attacker)
            {
                // 防守方只攻击敌方宠物（已在 PetOwner 分支处理）
                // 不主动攻击 SabukPrimeGate / SabakGuard / CastleLord
                if (monster is SabukPrimeGate || monster is SabakGuard || monster is SabakGuardian || monster is CastleLord)
                    return long.MinValue;
            }

            switch (strategy)
            {
                case BotSiegeStrategy.FrontalAssault:
                    return GetFrontalAssaultMonsterScore(monster, distance, attacker);

                case BotSiegeStrategy.FlankingAssault:
                    return GetFlankingAssaultMonsterScore(monster, distance, attacker);

                case BotSiegeStrategy.DefensiveCounterAttack:
                    return GetDefensiveCounterAttackMonsterScore(monster, distance, attacker);

                case BotSiegeStrategy.SplitAssault:
                    // SplitAssault 实际被分配为 FrontalAssault 或 FlankingAssault，此处兜底
                    return GetFrontalAssaultMonsterScore(monster, distance, attacker);

                default:
                    return long.MinValue;
            }
        }

        /// <summary>
        /// 正面强攻目标优先级：城门 > 守卫 > 城主
        /// </summary>
        private static long GetFrontalAssaultMonsterScore(MonsterObject monster, int distance, bool attacker)
        {
            if (monster is SabukPrimeGate gate)
            {
                // 城门已破则忽略
                if (gate.Dead || gate.Direction == MirDirection.UpLeft)
                    return long.MinValue;
                return 1_200_000L - distance * 5_000L - monster.CurrentHP;
            }

            if (monster is SabakGuard || monster is SabakGuardian)
                return 720_000L - distance * 3_000L - monster.CurrentHP;

            if (monster is CastleLord)
            {
                // 城门未破时，城主优先级较低（先破城门）
                if (!IsGateDestroyed(monster.CurrentMap))
                    return 400_000L - distance * 2_000L - monster.CurrentHP;
                // 城门已破，全力打城主
                return 1_000_000L - distance * 2_500L - monster.CurrentHP;
            }

            return long.MinValue;
        }

        /// <summary>
        /// 侧翼偷袭目标优先级：城主 > 守卫（忽略城门）
        /// </summary>
        private static long GetFlankingAssaultMonsterScore(MonsterObject monster, int distance, bool attacker)
        {
            // 侧翼偷袭完全忽略城门
            if (monster is SabukPrimeGate)
                return long.MinValue;

            // 城主最高优先级（直接打核心目标）
            if (monster is CastleLord)
                return 1_200_000L - distance * 2_000L - monster.CurrentHP;

            // 守卫次之（清理干扰）
            if (monster is SabakGuard || monster is SabakGuardian)
                return 500_000L - distance * 3_000L - monster.CurrentHP;

            return long.MinValue;
        }

        /// <summary>
        /// 防守反击目标优先级：城门 > 城门附近守卫 > 城主（保护己方城主）
        /// </summary>
        private static long GetDefensiveCounterAttackMonsterScore(MonsterObject monster, int distance, bool attacker)
        {
            if (monster is SabukPrimeGate gate)
            {
                // 防守方保护城门，优先修复/守卫城门区域
                if (gate.Dead || gate.Direction == MirDirection.UpLeft)
                    return long.MinValue; // 城门已破，无力回天
                return 1_000_000L - distance * 5_000L - monster.CurrentHP;
            }

            // 守卫协助防守
            if (monster is SabakGuard || monster is SabakGuardian)
                return 600_000L - distance * 3_000L - monster.CurrentHP;

            // 防守方一般不打城主
            if (monster is CastleLord)
                return long.MinValue;

            return long.MinValue;
        }

        /// <summary>
        /// 检查目标点是否在城门附近
        /// </summary>
        private static bool IsNearGate(Map map, Point location, int range)
        {
            if (map == null) return false;

            foreach (MapObject obj in map.Objects)
            {
                if (obj is SabukPrimeGate gate && !gate.Dead)
                {
                    return Functions.InRange(location, gate.CurrentLocation, range);
                }
            }
            return false;
        }

        // ══════════════════════════════════════════════════════════════════════
        //  基于策略的移动方向
        // ══════════════════════════════════════════════════════════════════════

        /// <summary>
        /// 根据攻城策略决定假人在攻城地图中的前进方向
        /// </summary>
        private static bool TryAdvanceBotSiegeStrategy(PlayerObject player, ConquestWar war, BotSiegeStrategy strategy)
        {
            if (player == null || war?.info == null || player.CurrentMap != war.Map)
                return false;

            Point advancePoint = Point.Empty;

            switch (strategy)
            {
                case BotSiegeStrategy.FrontalAssault:
                case BotSiegeStrategy.SplitAssault:
                    // 正面强攻：朝城堡区域推进
                    if (player.IsWarAttacker())
                        advancePoint = GetNearestBotConquestRegionPoint(war.info.CastleRegion, player.CurrentLocation);
                    else
                        advancePoint = GetNearestBotConquestRegionPoint(war.info.DefenderSpawnRegion ?? war.info.CastleRegion, player.CurrentLocation);
                    break;

                case BotSiegeStrategy.FlankingAssault:
                    // 侧翼偷袭：朝城主/Boss刷新区域或旗点推进（绕过城门）
                    if (war.info.FlagPoint != Point.Empty)
                        advancePoint = war.info.FlagPoint;
                    else
                        advancePoint = GetNearestBotConquestRegionPoint(war.info.CastleRegion, player.CurrentLocation);
                    break;

                case BotSiegeStrategy.DefensiveCounterAttack:
                    // 防守反击：守在城门附近或城堡区域
                    advancePoint = GetNearestBotConquestRegionPoint(war.info.CastleRegion, player.CurrentLocation);
                    // 如果离城门更近，优先靠近城门
                    Point gatePoint = GetNearestGatePoint(war.Map, player.CurrentLocation);
                    if (gatePoint != Point.Empty)
                    {
                        int gateDist = Functions.Distance(player.CurrentLocation, gatePoint);
                        int regionDist = advancePoint != Point.Empty ? Functions.Distance(player.CurrentLocation, advancePoint) : int.MaxValue;
                        if (gateDist < regionDist)
                            advancePoint = gatePoint;
                    }
                    break;
            }

            if (advancePoint == Point.Empty)
                advancePoint = war.info.FlagPoint;
            if (advancePoint == Point.Empty || advancePoint == player.CurrentLocation)
                return false;

            MirDirection dir = Functions.DirectionFromPoint(player.CurrentLocation, advancePoint);
            return TryMoveBotAlongDirection(player, dir, 2, out _, out _);
        }

        /// <summary>
        /// 找到地图上最近的城门位置
        /// </summary>
        private static Point GetNearestGatePoint(Map map, Point from)
        {
            if (map == null) return Point.Empty;

            Point bestPoint = Point.Empty;
            int bestDistance = int.MaxValue;

            foreach (MapObject obj in map.Objects)
            {
                if (obj is SabukPrimeGate gate && !gate.Dead)
                {
                    int dist = Functions.Distance(from, gate.CurrentLocation);
                    if (dist < bestDistance)
                    {
                        bestDistance = dist;
                        bestPoint = gate.CurrentLocation;
                    }
                }
            }

            return bestPoint;
        }

        // ══════════════════════════════════════════════════════════════════════
        //  攻城会话协调
        // ══════════════════════════════════════════════════════════════════════

        /// <summary>
        /// 攻城会话消息模板
        /// </summary>
        private static readonly Dictionary<BotSiegeChatType, Func<BotSiegeStrategy, string>> SiegeChatMessages =
            new Dictionary<BotSiegeChatType, Func<BotSiegeStrategy, string>>
            {
                [BotSiegeChatType.StrategyAnnounce] = s =>
                {
                    switch (s)
                    {
                        case BotSiegeStrategy.FrontalAssault:
                            return "全员集合，正面强攻城门！大家集中火力！";
                        case BotSiegeStrategy.FlankingAssault:
                            return "采取侧翼偷袭，绕过城门直打城主！";
                        case BotSiegeStrategy.DefensiveCounterAttack:
                            return "全员防守城门，绝对不能被夺城！";
                        case BotSiegeStrategy.SplitAssault:
                            return "分兵突击！主力破城门，突击队偷袭城主！";
                        default:
                            return "准备攻城！";
                    }
                },
                [BotSiegeChatType.GateBroken] = s =>
                    s == BotSiegeStrategy.DefensiveCounterAttack
                        ? "城门被破了！全员回城门附近防守！"
                        : "城门已破！全力进攻城主！",
                [BotSiegeChatType.IntruderAlert] = _ =>
                    "城内发现偷袭者，注意安全！",
                [BotSiegeChatType.VictoryAnnounce] = _ =>
                    "我方已成功占领城堡！",
                [BotSiegeChatType.RetryAttack] = _ =>
                    "重新组织进攻，不要分散！",
                [BotSiegeChatType.DefenseReminder] = _ =>
                    "防守阵型保持住，守住城门就是胜利！",
            };

        /// <summary>
        /// 尝试发送攻城会话（行会频道）。只有行会会长/队长发送，且受冷却时间限制。
        /// </summary>
        private static void TrySendSiegeChat(PlayerObject player, BotSiegeChatType chatType, BotSiegeStrategy strategy)
        {
            if (player?.Connection == null) return;

            GuildInfo guild = player.Character?.Account?.GuildMember?.Guild;
            if (guild == null) return;

            // 冷却检查
            string guildKey = guild.GuildName;
            if (_guildSiegeChatCooldown.TryGetValue(guildKey, out DateTime nextTime) && SEnvir.Now < nextTime)
                return;

            string message = SiegeChatMessages.TryGetValue(chatType, out var msgFunc) ? msgFunc(strategy) : null;
            if (string.IsNullOrEmpty(message)) return;

            _guildSiegeChatCooldown[guildKey] = SEnvir.Now.AddSeconds(BotSiegeChatCooldownSeconds);

            // 通过行会频道广播给所有在线行会成员
            foreach (GuildMemberInfo member in guild.Members)
            {
                if (member.Account?.Connection?.Player == null) continue;

                member.Account.Connection.ReceiveChat(
                    $"[行会] {player.Name}: {message}",
                    MessageType.Guild);
            }
        }

        // ══════════════════════════════════════════════════════════════════════
        //  城门事件检测
        // ══════════════════════════════════════════════════════════════════════

        /// <summary>
        /// 检测城门状态变化（被破事件），触发会话通知。
        /// </summary>
        private static void CheckGateStatusChange(PlayerObject player, ConquestWar war, BotSiegeStrategy strategy)
        {
            if (player == null || war?.Map == null) return;

            int mapIndex = war.Map.Info.Index;

            foreach (MapObject obj in war.Map.Objects)
            {
                if (!(obj is SabukPrimeGate gate)) continue;

                MirDirection currentDir = gate.Direction;

                if (_lastGateDirection.TryGetValue(mapIndex, out MirDirection lastDir))
                {
                    // 检测城门被破：从非 UpLeft 变为 UpLeft
                    if (lastDir != MirDirection.UpLeft && currentDir == MirDirection.UpLeft)
                    {
                        TrySendSiegeChat(player, BotSiegeChatType.GateBroken, strategy);
                    }
                }

                _lastGateDirection[mapIndex] = currentDir;
                return; // 每张地图只处理第一个城门
            }
        }

        // ══════════════════════════════════════════════════════════════════════
        //  攻城策略主入口（供 ProcessBotConquestWarfare 调用）
        // ══════════════════════════════════════════════════════════════════════

        /// <summary>
        /// 策略化攻城主逻辑入口。
        /// 替代原有 ProcessBotConquestWarfare 中固定的目标选择逻辑。
        /// </summary>
        private static bool ProcessBotSiegeWarfare(PlayerObject player, ConquestWar war)
        {
            if (player == null || player.Dead || player.Node == null || war == null)
                return false;

            uint pid = player.ObjectID;

            // 确定策略
            BotSiegeStrategy strategy = DetermineBotSiegeStrategy(player, war);

            // 首次进入攻城时发送战术宣布（只发一次）
            if (!_botSiegeStrategies.ContainsKey(pid))
            {
                _botSiegeStrategies[pid] = strategy;
                TrySendSiegeChat(player, BotSiegeChatType.StrategyAnnounce, strategy);
            }

            // 检测城门状态变化
            CheckGateStatusChange(player, war, strategy);

            // 防守方：定期提醒
            if (strategy == BotSiegeStrategy.DefensiveCounterAttack)
            {
                // 由 TrySendSiegeChat 内部控制冷却，此处不需要额外检查
            }

            // 清理拾取状态
            _botTargetItems.Remove(pid);
            _botWaitingPickup.Remove(pid);

            // 不在攻城地图
            if (player.CurrentMap != war.Map)
            {
                ClearBotPendingCombatActions(player);
                _botTargets.Remove(pid);
                _botTargetSwitchTime.Remove(pid);
                player.PacketWaiting = false;
                return true;
            }

            // 基于策略选择目标
            MapObject target = FindBotSiegeStrategyTarget(player, war, strategy);

            if (target == null)
            {
                ClearBotPendingCombatActions(player);
                _botTargets.Remove(pid);
                _botTargetSwitchTime.Remove(pid);
                player.PacketWaiting = false;
                TryAdvanceBotSiegeStrategy(player, war, strategy);
                return true;
            }

            _botTargets[pid] = target;
            _botTargetSwitchTime[pid] = SEnvir.Now.AddSeconds(BotTargetSwitchTimeout);
            ProcessBotCombatEngagement(player, target);
            return true;
        }

        // ══════════════════════════════════════════════════════════════════════
        //  状态清理
        // ══════════════════════════════════════════════════════════════════════

        /// <summary>
        /// 清理假人攻城策略状态（在 Stop / 掉线 / 移除连接时调用）
        /// </summary>
        private static void ClearBotSiegeState(uint objectId)
        {
            _botSiegeStrategies.Remove(objectId);
        }

        /// <summary>
        /// 清理所有攻城策略状态（攻城结束时调用）
        /// </summary>
        private static void ClearAllSiegeStrategies()
        {
            _botSiegeStrategies.Clear();
            _lastGateDirection.Clear();
            _guildSiegeChatCooldown.Clear();
        }
    }
}
