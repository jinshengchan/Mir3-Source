using Library;
using Server.Models;
using System;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;

namespace Server.Envir
{
    /// <summary>
    /// 假人 PVP 策略系统。
    /// 四种核心策略：反击、风筝、集火、逃跑。
    /// 通过 EvaluateAndDecide(player) 返回决策，BotManager 负责执行。
    /// </summary>
    public static class BotPvPStrategy
    {
        // ══════════════════════════════════════════════════════════════════════
        //  枚举 / 结构体
        // ══════════════════════════════════════════════════════════════════════

        public enum PvPStrategy
        {
            None,
            CounterAttack, // 反击：正面硬刚
            Kite,          // 风筝：远程保持距离边退边打
            FocusFire,     // 集火：跟队友优先击杀最大威胁
            Flee,          // 逃跑：撤离保命
        }

        public enum PvPAction
        {
            None,
            Attack,
            Retreat,
            Flee,
        }

        public struct PvPStrategyDecision
        {
            public PvPStrategy Strategy;
            public PvPAction Action;
            public PlayerObject Target;    // 攻击目标（Attack时有效）
            public MirDirection FleeDir;   // 逃跑方向（Flee/Retreat时有效）
            public bool NeedKiteSkill;     // 风筝模式下应优先使用减速/控制技能
        }

        // ══════════════════════════════════════════════════════════════════════
        //  威胁记录
        // ══════════════════════════════════════════════════════════════════════

        private sealed class ThreatRecord
        {
            public uint AttackerObjectId;
            public int TotalDamage;
            public int MaxSingleDamage;
            public DateTime LastActiveTime;
            public DateTime FirstSeenTime;
        }

        // 假人 ObjectID → 攻击者列表
        private static readonly Dictionary<uint, List<ThreatRecord>> _threatMap
            = new Dictionary<uint, List<ThreatRecord>>();

        // 假人 ObjectID → 当前激活的策略
        private static readonly Dictionary<uint, PvPStrategy> _activeStrategy
            = new Dictionary<uint, PvPStrategy>();

        // 假人 ObjectID → 当前策略激活时间（保护期内不切换）
        private static readonly Dictionary<uint, DateTime> _strategyActivatedTime
            = new Dictionary<uint, DateTime>();

        // 假人 ObjectID → 强制逃跑激活时间（最多逃 10 秒后重评）
        private static readonly Dictionary<uint, DateTime> _fleeActivatedTime
            = new Dictionary<uint, DateTime>();

        private const int ThreatWindowSeconds = 15;
        private const int ThreatExpireSeconds = 30;
        private const double StrategyProtectSeconds = 3.0;
        private const double FleeMaxSeconds = 10.0;

        // 触发逃跑的血量阈值（%）
        private const int FleeHpThresholdPct = 20;

        // 风筝安全距离
        private const int KiteSafeDistance = 5;

        // 战士反击→风筝切换血量阈值（%）：低于此值战士改用风筝策略
        private const int WarriorKiteHpThresholdPct = 40;

        // 风筝极限血量阈值（%）：低于此值所有职业跳过风筝直接逃
        private const int CriticalHpForFleePct = 25;

        // 停止逃跑的条件：已跑出威胁格数 且 附近无威胁
        private const int FleeStopDistance = 10;

        // 地形检查：逃跑方向尝试偏移的最大角度（1=±45°，2=±90°）
        private const int FleeTerrainMaxDeviation = 2;

        // ══════════════════════════════════════════════════════════════════════
        //  公共 API
        // ══════════════════════════════════════════════════════════════════════

        /// <summary>
        /// 记录 PVP 伤害（被真人攻击时调用）。
        /// </summary>
        public static void RecordPvPDamage(uint botObjectId, uint attackerObjectId, int damage)
        {
            if (damage <= 0) return;

            List<ThreatRecord> list;
            if (!_threatMap.TryGetValue(botObjectId, out list))
            {
                list = new List<ThreatRecord>();
                _threatMap[botObjectId] = list;
            }

            ThreatRecord rec = list.FirstOrDefault(x => x.AttackerObjectId == attackerObjectId);
            if (rec == null)
            {
                rec = new ThreatRecord
                {
                    AttackerObjectId = attackerObjectId,
                    FirstSeenTime = SEnvir.Now,
                };
                list.Add(rec);
            }

            rec.TotalDamage += damage;
            rec.MaxSingleDamage = Math.Max(rec.MaxSingleDamage, damage);
            rec.LastActiveTime = SEnvir.Now;
        }

        /// <summary>
        /// 强制切换为逃跑策略（紧急逃脱时调用）。
        /// </summary>
        public static void ForceFlee(uint botObjectId)
        {
            _activeStrategy[botObjectId] = PvPStrategy.Flee;
            _strategyActivatedTime[botObjectId] = SEnvir.Now;
            _fleeActivatedTime[botObjectId] = SEnvir.Now;
        }

        /// <summary>
        /// 是否处于 PVP 策略激活状态（有威胁记录且未过期）。
        /// </summary>
        public static bool IsInPvPStrategy(uint botObjectId)
        {
            List<ThreatRecord> list;
            if (!_threatMap.TryGetValue(botObjectId, out list)) return false;

            DateTime expiry = SEnvir.Now.AddSeconds(-ThreatExpireSeconds);
            return list.Any(x => x.LastActiveTime > expiry);
        }

        /// <summary>
        /// 评估威胁并返回策略决策。
        /// </summary>
        public static PvPStrategyDecision EvaluateAndDecide(PlayerObject player)
        {
            var decision = new PvPStrategyDecision { Strategy = PvPStrategy.None, Action = PvPAction.None };

            if (player == null || player.Dead || player.Node == null) return decision;

            CleanExpiredThreats(player.ObjectID);

            List<ThreatRecord> threats = GetActiveThreats(player.ObjectID);
            List<PlayerObject> threatPlayers = ResolveThreatPlayers(player, threats);

            if (threatPlayers.Count == 0)
            {
                // 没有威胁，清除策略
                _activeStrategy.Remove(player.ObjectID);
                return decision;
            }

            bool reachedFleeStopDistance = HasReachedFleeStopDistance(player, threatPlayers);
            if (_activeStrategy.TryGetValue(player.ObjectID, out PvPStrategy current)
                && current == PvPStrategy.Flee && reachedFleeStopDistance)
            {
                _activeStrategy.Remove(player.ObjectID);
                _strategyActivatedTime.Remove(player.ObjectID);
                _fleeActivatedTime.Remove(player.ObjectID);
            }

            // 评估是否应该逃跑
            bool shouldFlee = !reachedFleeStopDistance && ShouldFlee(player, threatPlayers);

            // 检查强制逃跑是否仍然有效
            if (_activeStrategy.TryGetValue(player.ObjectID, out current) && current == PvPStrategy.Flee)
            {
                DateTime fleeStart;
                if (!_fleeActivatedTime.TryGetValue(player.ObjectID, out fleeStart)
                    || (SEnvir.Now - fleeStart).TotalSeconds > FleeMaxSeconds)
                {
                    // 逃跑超时，重评
                    _activeStrategy.Remove(player.ObjectID);
                }
                else
                {
                    return BuildFleeDecision(player, threatPlayers);
                }
            }

            if (shouldFlee)
            {
                ForceFlee(player.ObjectID);
                return BuildFleeDecision(player, threatPlayers);
            }

            // 策略保护期内不切换
            DateTime activatedAt;
            if (_strategyActivatedTime.TryGetValue(player.ObjectID, out activatedAt)
                && (SEnvir.Now - activatedAt).TotalSeconds < StrategyProtectSeconds
                && _activeStrategy.TryGetValue(player.ObjectID, out current)
                && current != PvPStrategy.None)
            {
                return BuildDecisionFromStrategy(player, current, threatPlayers);
            }

            // 选择新策略
            PvPStrategy newStrategy = SelectStrategy(player, threatPlayers);
            _activeStrategy[player.ObjectID] = newStrategy;
            _strategyActivatedTime[player.ObjectID] = SEnvir.Now;

            return BuildDecisionFromStrategy(player, newStrategy, threatPlayers);
        }

        /// <summary>
        /// 清除某假人的所有 PVP 状态（死亡时调用）。
        /// </summary>
        public static void ClearPvPState(uint botObjectId)
        {
            _threatMap.Remove(botObjectId);
            _activeStrategy.Remove(botObjectId);
            _strategyActivatedTime.Remove(botObjectId);
            _fleeActivatedTime.Remove(botObjectId);
        }

        /// <summary>
        /// 清除所有假人的 PVP 状态（Stop 时调用）。
        /// </summary>
        public static void ClearAllPvPStates()
        {
            _threatMap.Clear();
            _activeStrategy.Clear();
            _strategyActivatedTime.Clear();
            _fleeActivatedTime.Clear();
        }

        // ══════════════════════════════════════════════════════════════════════
        //  内部逻辑
        // ══════════════════════════════════════════════════════════════════════

        private static bool ShouldFlee(PlayerObject player, List<PlayerObject> threatPlayers)
        {
            int maxHP = player.Stats[Stat.Health];
            if (maxHP <= 0) return false;

            int hpPct = player.CurrentHP * 100 / maxHP;
            if (hpPct <= FleeHpThresholdPct) return true;

            // 极限血量（<25%）：即使只有1个威胁也逃
            if (hpPct <= CriticalHpForFleePct) return true;

            // 被 ≥2 人围攻且无队友 → 逃
            bool hasGroupmate = player.GroupMembers != null && player.GroupMembers.Count > 1;
            if (threatPlayers.Count >= 2 && !hasGroupmate) return true;

            // 被 ≥4 人围攻有队友 → 逃
            if (threatPlayers.Count >= 4) return true;

            return false;
        }

        /// <summary>
        /// 获取玩家当前 HP 百分比（0~100）
        /// </summary>
        private static int GetHpPercent(PlayerObject player)
        {
            int maxHP = player.Stats[Stat.Health];
            if (maxHP <= 0) return 0;
            return player.CurrentHP * 100 / maxHP;
        }

        private static PvPStrategy SelectStrategy(PlayerObject player, List<PlayerObject> threatPlayers)
        {
            int hpPct = GetHpPercent(player);

            // 有队友时集火
            if (player.GroupMembers != null && player.GroupMembers.Count > 1)
                return PvPStrategy.FocusFire;

            // 战士：血量高正面硬刚，血量低改用风筝
            if (player.Class == MirClass.Warrior)
            {
                if (hpPct >= WarriorKiteHpThresholdPct)
                    return PvPStrategy.CounterAttack;
                // 血量低但还能打 → 风筝（拉距离喝药回血再回来）
                return PvPStrategy.Kite;
            }

            // 远程职业风筝
            if (player.Class == MirClass.Wizard || player.Class == MirClass.Taoist || player.Class == MirClass.Assassin)
                return PvPStrategy.Kite;

            // 默认反击
            return PvPStrategy.CounterAttack;
        }

        private static PvPStrategyDecision BuildDecisionFromStrategy(PlayerObject player, PvPStrategy strategy, List<PlayerObject> threats)
        {
            switch (strategy)
            {
                case PvPStrategy.CounterAttack:
                    return BuildCounterAttackDecision(player, threats);
                case PvPStrategy.Kite:
                    return BuildKiteDecision(player, threats);
                case PvPStrategy.FocusFire:
                    return BuildFocusFireDecision(player, threats);
                case PvPStrategy.Flee:
                    return BuildFleeDecision(player, threats);
                default:
                    return new PvPStrategyDecision { Strategy = PvPStrategy.None, Action = PvPAction.None };
            }
        }

        private static PvPStrategyDecision BuildCounterAttackDecision(PlayerObject player, List<PlayerObject> threats)
        {
            PlayerObject target = GetHighestThreatPlayer(threats, player.ObjectID);
            return new PvPStrategyDecision
            {
                Strategy = PvPStrategy.CounterAttack,
                Action = PvPAction.Attack,
                Target = target,
            };
        }

        private static PvPStrategyDecision BuildKiteDecision(PlayerObject player, List<PlayerObject> threats)
        {
            PlayerObject closestThreat = threats
                .Where(t => t != null && t.Node != null)
                .OrderBy(t => Functions.Distance(player.CurrentLocation, t.CurrentLocation))
                .FirstOrDefault();

            if (closestThreat == null)
                return new PvPStrategyDecision { Strategy = PvPStrategy.Kite, Action = PvPAction.None };

            int dist = Functions.Distance(player.CurrentLocation, closestThreat.CurrentLocation);

            if (dist < KiteSafeDistance)
            {
                // 太近，后退（地形感知）
                MirDirection awayDir = Functions.DirectionFromPoint(closestThreat.CurrentLocation, player.CurrentLocation);
                MirDirection safeDir = FindPassableDirection(player, awayDir);
                return new PvPStrategyDecision
                {
                    Strategy = PvPStrategy.Kite,
                    Action = PvPAction.Retreat,
                    FleeDir = safeDir,
                    Target = closestThreat,
                    NeedKiteSkill = true,  // 被迫后退时优先用减速技能
                };
            }

            // 距离合适，攻击
            PlayerObject target = GetHighestThreatPlayer(threats, player.ObjectID);
            return new PvPStrategyDecision
            {
                Strategy = PvPStrategy.Kite,
                Action = PvPAction.Attack,
                Target = target,
                NeedKiteSkill = false,
            };
        }

        private static PvPStrategyDecision BuildFocusFireDecision(PlayerObject player, List<PlayerObject> threats)
        {
            // 优先跟随队友集火目标
            PlayerObject focusTarget = null;

            if (player.GroupMembers != null)
            {
                foreach (var member in player.GroupMembers)
                {
                    var memberPlayer = member as PlayerObject;
                    if (memberPlayer == null || memberPlayer == player) continue;

                    // 找队友的目标（简化：找威胁列表中对队友造成伤害的）
                    List<ThreatRecord> memberThreats;
                    if (_threatMap.TryGetValue(memberPlayer.ObjectID, out memberThreats) && memberThreats.Count > 0)
                    {
                        var resolved = ResolveThreatPlayers(player, memberThreats);
                        if (resolved.Count > 0)
                        {
                            focusTarget = GetHighestThreatPlayer(resolved, memberPlayer.ObjectID);
                            break;
                        }
                    }
                }
            }

            if (focusTarget == null)
                focusTarget = GetHighestThreatPlayer(threats, player.ObjectID);

            return new PvPStrategyDecision
            {
                Strategy = PvPStrategy.FocusFire,
                Action = PvPAction.Attack,
                Target = focusTarget,
            };
        }

        private static PvPStrategyDecision BuildFleeDecision(PlayerObject player, List<PlayerObject> threats)
        {
            // 计算所有威胁的合力方向的反方向
            double dx = 0, dy = 0;
            foreach (PlayerObject t in threats.Where(t => t != null && t.Node != null))
            {
                double vx = player.CurrentLocation.X - t.CurrentLocation.X;
                double vy = player.CurrentLocation.Y - t.CurrentLocation.Y;
                double len = Math.Sqrt(vx * vx + vy * vy);
                if (len > 0) { dx += vx / len; dy += vy / len; }
            }

            // 映射到 8 方向
            MirDirection fleeDir = MirDirection.Up;
            if (Math.Abs(dx) > 0.01 || Math.Abs(dy) > 0.01)
            {
                Point escapePoint = new Point(
                    player.CurrentLocation.X + Math.Sign(dx),
                    player.CurrentLocation.Y + Math.Sign(dy));

                // 8方向映射（0=Up=北，按游戏坐标系）
                fleeDir = Functions.DirectionFromPoint(player.CurrentLocation, escapePoint);
            }

            // 地形感知：检查逃跑方向是否可通行，不行则尝试偏移
            fleeDir = FindPassableDirection(player, fleeDir);

            return new PvPStrategyDecision
            {
                Strategy = PvPStrategy.Flee,
                Action = PvPAction.Flee,
                FleeDir = fleeDir,
            };
        }

        /// <summary>
        /// 地形感知方向选择：从首选方向开始检查前方是否可通行，
        /// 如果被墙挡住则逐步偏转（±45°、±90°）直到找到可通行方向。
        /// </summary>
        private static MirDirection FindPassableDirection(PlayerObject player, MirDirection preferredDir)
        {
            if (player == null || player.CurrentMap == null) return preferredDir;

            // 先检查首选方向
            if (IsDirectionPassable(player, preferredDir))
                return preferredDir;

            // 尝试偏转 ±45°、±90° 等
            for (int deviation = 1; deviation <= FleeTerrainMaxDeviation; deviation++)
            {
                MirDirection cwDir = RotateDirectionClockwise(preferredDir, deviation);
                if (IsDirectionPassable(player, cwDir))
                    return cwDir;

                MirDirection ccwDir = RotateDirectionCounterClockwise(preferredDir, deviation);
                if (IsDirectionPassable(player, ccwDir))
                    return ccwDir;
            }

            // 都走不通，返回首选方向让 TryMoveBotAlongDirection 自己处理侧移
            return preferredDir;
        }

        /// <summary>
        /// 检查玩家当前位置向指定方向是否可通行（检查1~2格）。
        /// 只看静态地形（边界、门口/传送点），不检查动态对象（怪物/玩家）。
        /// </summary>
        private static bool IsDirectionPassable(PlayerObject player, MirDirection dir)
        {
            if (player == null || player.CurrentMap == null) return true;

            Point current = player.CurrentLocation;

            for (int step = 1; step <= 2; step++)
            {
                Point target = Functions.Move(current, dir, step);
                var cell = player.CurrentMap.GetCell(target);
                if (cell == null) return false;          // 地图边界
                if (cell.Movements != null) return false; // 门口/传送点
            }

            return true;
        }

        /// <summary>
        /// 顺时针旋转方向（每次+1，8方向循环）
        /// </summary>
        private static MirDirection RotateDirectionClockwise(MirDirection dir, int steps)
        {
            return (MirDirection)(((int)dir + steps) % 8);
        }

        /// <summary>
        /// 逆时针旋转方向（每次-1，8方向循环）
        /// </summary>
        private static MirDirection RotateDirectionCounterClockwise(MirDirection dir, int steps)
        {
            return (MirDirection)(((int)dir - steps + 8) % 8);
        }

        private static PlayerObject GetHighestThreatPlayer(List<PlayerObject> players, uint selfObjectId)
        {
            if (players == null || players.Count == 0) return null;

            PlayerObject best = null;
            int bestScore = -1;

            foreach (PlayerObject p in players.Where(x => x != null && x.Node != null))
            {
                List<ThreatRecord> records;
                if (!_threatMap.TryGetValue(selfObjectId, out records)) continue;

                ThreatRecord rec = records.FirstOrDefault(r => r.AttackerObjectId == p.ObjectID);
                if (rec == null) continue;

                // 威胁评分：累计伤害 * 0.4 + 最大单次 * 0.4 + 活跃度 * 0.2
                double recentSecs = Math.Max(0, (SEnvir.Now - rec.LastActiveTime).TotalSeconds);
                int activity = Math.Max(0, ThreatWindowSeconds - (int)recentSecs);
                int score = (int)(rec.TotalDamage * 0.4 + rec.MaxSingleDamage * 0.4 + activity * 50 * 0.2);

                if (score > bestScore)
                {
                    bestScore = score;
                    best = p;
                }
            }

            return best ?? players.FirstOrDefault(x => x != null && x.Node != null);
        }

        private static List<ThreatRecord> GetActiveThreats(uint botObjectId)
        {
            List<ThreatRecord> list;
            if (!_threatMap.TryGetValue(botObjectId, out list)) return new List<ThreatRecord>();

            DateTime cutoff = SEnvir.Now.AddSeconds(-ThreatWindowSeconds);
            return list.Where(x => x.LastActiveTime > cutoff).ToList();
        }

        private static bool HasReachedFleeStopDistance(PlayerObject player, List<PlayerObject> threats)
        {
            return player != null
                   && threats != null
                   && threats.Count > 0
                   && threats.All(t => t != null
                                       && Functions.Distance(player.CurrentLocation, t.CurrentLocation) >= FleeStopDistance);
        }

        private static List<PlayerObject> ResolveThreatPlayers(PlayerObject player, List<ThreatRecord> threats)
        {
            var result = new List<PlayerObject>();
            if (player == null || threats == null) return result;

            foreach (ThreatRecord t in threats)
            {
                foreach (PlayerObject p in SEnvir.Players)
                {
                    if (p == null || p.ObjectID != t.AttackerObjectId || p == player) continue;
                    if (p.Node == null || p.Dead || p.CurrentMap != player.CurrentMap) continue;
                    if (!Functions.InRange(player.CurrentLocation, p.CurrentLocation, Config.MaxViewRange)) continue;
                    if (!player.CanAttackTarget(p)) continue;

                    result.Add(p);
                    break;
                }
            }
            return result;
        }

        private static void CleanExpiredThreats(uint botObjectId)
        {
            List<ThreatRecord> list;
            if (!_threatMap.TryGetValue(botObjectId, out list)) return;

            DateTime expiry = SEnvir.Now.AddSeconds(-ThreatExpireSeconds);
            list.RemoveAll(x => x.LastActiveTime <= expiry);
        }
    }
}
