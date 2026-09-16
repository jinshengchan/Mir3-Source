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
    public static partial class BotManager
    {
        // ══════════════════════════════════════════════════════════════════════
        //  AI – 自动穿戴背包中属性更好的装备
        // ══════════════════════════════════════════════════════════════════════

        /// <summary>自动穿装检查间隔（秒）：穿装是低频操作，无需每帧扫描背包。</summary>
        private const int BotAutoEquipCheckInterval = 5;

        /// <summary>自动穿装冷却时间表：假人 ObjectID → 下次允许检查时间。</summary>
        private static readonly Dictionary<uint, DateTime> _botLastAutoEquipCheckTime
            = new Dictionary<uint, DateTime>();

        private enum BotPotionKind
        {
            None,
            Health,
            Mana,
            Dual,
        }

        private static int GetBotPotionKeepValue(int maxValue, int baseValue, int maxPercent)
        {
            if (maxValue <= 0) return 0;

            int percentValue = (int)Math.Ceiling(maxValue * Math.Max(0, maxPercent) / 100.0);
            int keepValue = Math.Max(Math.Max(0, baseValue), percentValue);
            return Math.Min(maxValue, keepValue);
        }

        private static long GetBotPotionTriggerPct(int maxValue, int keepValue, int baseCriticalPct)
        {
            if (maxValue <= 0) return 100;

            long keepPct = keepValue * 100L / Math.Max(1, maxValue);
            keepPct = Math.Max(0, Math.Min(100, keepPct));
            return Math.Max(baseCriticalPct, keepPct);
        }

        /// <summary>
        /// 独立药水监控：每200ms检查一次血蓝，非紧急背包扫描按800ms退避，不参与选怪/移动/攻击节奏。
        /// 参考真人自动药剂思路：先看是否存在真实血蓝缺口，再按当前百分比决定是否立刻优先喝药；
        /// 不再被 30%/20% 这种硬阈值卡住，也不再受外部 AutoPotionTime 长时间锁死。
        /// ★ 追加：兼容大补贴的“HP/MP保持值 + 最大血蓝百分比”思路，在服务端动态抬高 bot 保线。
        /// ★ 血量低于 BotPotionEmergencyHpPct（15%）时无视冷却强制追喝，防止死于冷却空档。
        /// ★ forceFullRecovery=true 时改成“补到满为止”模式，清怪后会优先把 HP/MP 灌满。
        /// </summary>
        private static bool ProcessBotPotionMonitor(PlayerObject player, bool forceFullRecovery = false)
        {
            if (player == null || player.Dead || player.Node == null || !Config.BotAutoPotionSupply)
                return false;

            uint pid = player.ObjectID;
            DateTime now = SEnvir.Now;

            int maxHP = player.Stats[Stat.Health];
            int maxMP = player.Stats[Stat.Mana];
            if (maxHP <= 0 && maxMP <= 0) return false;

            int missingHP = maxHP > 0 ? Math.Max(0, maxHP - player.CurrentHP) : 0;
            int missingMP = maxMP > 0 ? Math.Max(0, maxMP - player.CurrentMP) : 0;
            if (missingHP <= 0 && missingMP <= 0)
                return false;

            long hpPct = maxHP > 0 ? player.CurrentHP * 100L / maxHP : 100;
            long mpPct = maxMP > 0 ? player.CurrentMP * 100L / maxMP : 100;
            bool needKeepHP = forceFullRecovery ? missingHP > 0 : maxHP > 0 && missingHP > 0 && hpPct < BotPotionHpCriticalPct;
            bool needKeepMP = forceFullRecovery ? missingMP > 0 : maxMP > 0 && missingMP > 0 && mpPct < BotPotionMpCriticalPct;
            if (!needKeepHP && !needKeepMP)
                return false;

            long hpTriggerPct = forceFullRecovery ? 100 : BotPotionHpCriticalPct;
            long mpTriggerPct = forceFullRecovery ? 100 : BotPotionMpCriticalPct;

            // ★ 紧急模式或战后补满模式：血量极低/战后恢复时都允许继续追喝
            bool emergency = hpPct <= BotPotionEmergencyHpPct;
            if (!emergency)
            {
                if (_botPotionCooldownTime.TryGetValue(pid, out DateTime cooldownUntil) && now < cooldownUntil)
                    return false;

                // 非紧急检查失败或暂时无可用药时，避免下一次200ms定时器再次重扫背包。
                _botPotionCooldownTime[pid] = now.AddMilliseconds(BotPotionRetryIntervalMs);
            }

            int potionCooldownMs;
            if (!TryUseBestBotPotion(player, missingHP, missingMP, hpPct, mpPct, hpTriggerPct, mpTriggerPct, out potionCooldownMs, forceFullRecovery))
            {
                if (!TryBuyBotPotionsForImmediateNeed(player, needKeepHP, needKeepMP))
                    return false;

                if (!TryUseBestBotPotion(player, missingHP, missingMP, hpPct, mpPct, hpTriggerPct, mpTriggerPct, out potionCooldownMs, forceFullRecovery))
                    return false;
            }

            DateTime nextPotionTime = SEnvir.Now.AddMilliseconds(potionCooldownMs);
            _botPotionCooldownTime[pid] = nextPotionTime;
            player.AutoPotionTime = nextPotionTime;
            player.DelayItemUse = null;
            return true;
        }

        private static bool TryUseBestBotPotion(PlayerObject player, int missingHP, int missingMP,
            long hpPct, long mpPct, long hpTriggerPct, long mpTriggerPct,
            out int potionCooldownMs, bool forceFullRecovery = false)
        {
            potionCooldownMs = 0;
            if (player?.Inventory == null) return false;

            HashSet<int> excludedSlots = null;
            while (true)
            {
                int potionSlot = FindBestBotPotionSlot(player, missingHP, missingMP, hpPct, mpPct, hpTriggerPct, mpTriggerPct, excludedSlots, forceFullRecovery);
                if (potionSlot < 0)
                    return false;

                if (TryUseBotPotion(player, potionSlot, out potionCooldownMs))
                    return true;

                if (excludedSlots == null)
                    excludedSlots = new HashSet<int>();

                excludedSlots.Add(potionSlot);
                if (excludedSlots.Count >= player.Inventory.Length)
                    return false;
            }
        }

        private static bool IsBotPotionBlockedByMap(PlayerObject player, ItemInfo info)
        {
            string noUseItem = player?.CurrentMap?.Info?.NoUseItem;
            if (string.IsNullOrWhiteSpace(noUseItem) || info == null)
                return false;

            foreach (string raw in noUseItem.Split(','))
            {
                if (string.IsNullOrWhiteSpace(raw)) continue;
                if (!int.TryParse(raw, out int value)) continue;
                if (value < 0 || value == info.Index)
                    return true;
            }

            return false;
        }

        private static bool CanBotActuallyUsePotionNow(PlayerObject player, UserItem item)
        {
            if (player == null || item?.Info == null) return false;
            if (!player.CanUseItem(item)) return false;
            if (GetBotPotionKind(item, out int hpRestore, out int mpRestore) == BotPotionKind.None) return false;
            if (hpRestore <= 0 && mpRestore <= 0) return false;

            // ★ 性能优化：用 foreach 替代 Buffs.Any()，避免 LINQ 委托分配
            var buffs = player.Buffs;
            for (int i = 0; i < buffs.Count; i++)
            {
                if (buffs[i].Type == BuffType.DragonRepulse)
                    return false;
            }

            if ((player.Poison & PoisonType.ElectricShock) == PoisonType.ElectricShock) return false;
            if (IsBotPotionBlockedByMap(player, item.Info)) return false;

            return true;
        }

        private static int FindBestBotPotionSlot(PlayerObject player, int missingHP, int missingMP,
            long hpPct, long mpPct, long hpTriggerPct, long mpTriggerPct,
            HashSet<int> excludedSlots = null, bool forceFullRecovery = false)
        {
            int bestSlot = -1;
            int bestTier = int.MinValue;
            int bestPrimary = int.MinValue;
            int bestSecondary = int.MinValue;

            for (int i = 0; i < player.Inventory.Length; i++)
            {
                if (excludedSlots != null && excludedSlots.Contains(i)) continue;

                UserItem item = player.Inventory[i];
                if (item == null || item.Info == null) continue;
                if (!CanBotActuallyUsePotionNow(player, item)) continue;

                int hpRestore;
                int mpRestore;
                BotPotionKind kind = GetBotPotionKind(item, out hpRestore, out mpRestore);
                if (kind == BotPotionKind.None) continue;

                int tier;
                int primary;
                int secondary;
                if (!TryScoreBotPotionCandidate(kind, hpRestore, mpRestore, missingHP, missingMP, hpPct, mpPct,
                    hpTriggerPct, mpTriggerPct, out tier, out primary, out secondary, forceFullRecovery))
                    continue;

                if (tier > bestTier
                    || (tier == bestTier && primary > bestPrimary)
                    || (tier == bestTier && primary == bestPrimary && secondary > bestSecondary))
                {
                    bestSlot = i;
                    bestTier = tier;
                    bestPrimary = primary;
                    bestSecondary = secondary;
                }
            }

            if (bestSlot >= 0)
                return bestSlot;

            bool allowFallback = forceFullRecovery
                                 || hpPct <= hpTriggerPct
                                 || mpPct <= mpTriggerPct;

            return allowFallback
                ? FindFallbackBotPotionSlot(player, missingHP, missingMP, excludedSlots)
                : -1;
        }

        private static int FindFallbackBotPotionSlot(PlayerObject player, int missingHP, int missingMP, HashSet<int> excludedSlots = null)
        {
            int bestSlot = -1;
            int bestPrimary = int.MinValue;
            int bestSecondary = int.MinValue;

            for (int i = 0; i < player.Inventory.Length; i++)
            {
                if (excludedSlots != null && excludedSlots.Contains(i)) continue;

                UserItem item = player.Inventory[i];
                if (item == null || item.Info == null) continue;
                if (!CanBotActuallyUsePotionNow(player, item)) continue;

                BotPotionKind kind = GetBotPotionKind(item, out int hpRestore, out int mpRestore);
                if (kind == BotPotionKind.None) continue;

                int effectiveHP = Math.Min(Math.Max(0, missingHP), Math.Max(0, hpRestore));
                int effectiveMP = Math.Min(Math.Max(0, missingMP), Math.Max(0, mpRestore));
                if (effectiveHP <= 0 && effectiveMP <= 0) continue;

                int primary = effectiveHP + effectiveMP;
                int secondary = -(Math.Max(0, hpRestore - effectiveHP) + Math.Max(0, mpRestore - effectiveMP));

                if (primary > bestPrimary || (primary == bestPrimary && secondary > bestSecondary))
                {
                    bestSlot = i;
                    bestPrimary = primary;
                    bestSecondary = secondary;
                }
            }

            return bestSlot;
        }

        private static bool HasBotPotionKindInInventory(PlayerObject player, BotPotionKind kind)
        {
            if (player?.Inventory == null || kind == BotPotionKind.None) return false;

            for (int i = 0; i < player.Inventory.Length; i++)
            {
                UserItem item = player.Inventory[i];
                if (item?.Info == null || item.Count == 0) continue;
                if (GetBotPotionKind(item, out _, out _) == kind)
                    return true;
            }

            return false;
        }

        private static bool TryBuyBotPotionsForImmediateNeed(PlayerObject player, bool needHP, bool needMP)
        {
            if (player == null || player.Dead || !Config.BotAutoPotionSupply) return false;

            bool hasHealthPotion = HasBotPotionKindInInventory(player, BotPotionKind.Health);
            bool hasManaPotion = HasBotPotionKindInInventory(player, BotPotionKind.Mana);
            bool hasDualPotion = HasBotPotionKindInInventory(player, BotPotionKind.Dual);

            bool lackHpRecovery = needHP && !hasHealthPotion && !hasDualPotion;
            bool lackMpRecovery = needMP && !hasManaPotion && !hasDualPotion;
            if (!lackHpRecovery && !lackMpRecovery)
                return false;

            uint pid = player.ObjectID;
            DateTime now = SEnvir.Now;
            if (_botUrgentPotionBuyTime.TryGetValue(pid, out DateTime nextBuyTime) && now < nextBuyTime)
                return false;

            _botUrgentPotionBuyTime[pid] = now.AddSeconds(BotPotionShortageBuyCooldownSeconds);

            CountBotPotionStock(player, out int healthCount, out int manaCount, out int dualCount);
            long goldBefore = player.Gold;
            bool boughtAny = false;

            if (lackHpRecovery)
            {
                int buyHealthCount = Math.Max(1, BotTargetHealthPotionCount - healthCount);
                long beforeBuy = player.Gold;
                BotBuyPotion(player, BotPotionKind.Health, buyHealthCount, 0);
                boughtAny |= player.Gold != beforeBuy;
            }

            if (lackMpRecovery)
            {
                int buyManaCount = Math.Max(1, BotTargetManaPotionCount - manaCount);
                long beforeBuy = player.Gold;
                BotBuyPotion(player, BotPotionKind.Mana, buyManaCount, 0);
                boughtAny |= player.Gold != beforeBuy;
            }

            if (dualCount <= 0 && (lackHpRecovery || lackMpRecovery))
            {
                int buyDualCount = Math.Max(1, BotTargetDualPotionCount - dualCount);
                long beforeBuy = player.Gold;
                BotBuyPotion(player, BotPotionKind.Dual, buyDualCount, 0);
                boughtAny |= player.Gold != beforeBuy;
            }

            if (boughtAny)
            {
                _botRestockTime[pid] = now.AddSeconds(BotPotionRestockCooldownSeconds);
                FlushBotGoldState(player, goldBefore);
            }

            return boughtAny;
        }

        private static bool TryScoreBotPotionCandidate(BotPotionKind kind, int hpRestore, int mpRestore,
            int missingHP, int missingMP, long hpPct, long mpPct, long hpTriggerPct, long mpTriggerPct,
            out int tier, out int primary, out int secondary, bool forceFullRecovery = false)
        {
            tier = -1;
            primary = -1;
            secondary = int.MinValue;

            bool needHP = hpRestore > 0 && missingHP > 0 && (forceFullRecovery || hpPct < hpTriggerPct);
            bool needMP = mpRestore > 0 && missingMP > 0 && (forceFullRecovery || mpPct < mpTriggerPct);
            if (!needHP && !needMP)
                return false;

            int effectiveHP = Math.Min(Math.Max(0, missingHP), Math.Max(0, hpRestore));
            int effectiveMP = Math.Min(Math.Max(0, missingMP), Math.Max(0, mpRestore));
            int wastedHP = Math.Max(0, hpRestore - effectiveHP);
            int wastedMP = Math.Max(0, mpRestore - effectiveMP);

            if (needHP && !needMP)
            {
                if (kind == BotPotionKind.Health)
                {
                    tier = 300;
                    primary = effectiveHP;
                    secondary = -wastedHP;
                    return true;
                }

                if (kind == BotPotionKind.Dual)
                {
                    tier = 200;
                    primary = effectiveHP;
                    secondary = effectiveMP - wastedMP;
                    return true;
                }

                return false;
            }

            if (needMP && !needHP)
            {
                if (kind == BotPotionKind.Mana)
                {
                    tier = 300;
                    primary = effectiveMP;
                    secondary = -wastedMP;
                    return true;
                }

                if (kind == BotPotionKind.Dual)
                {
                    tier = 200;
                    primary = effectiveMP;
                    secondary = effectiveHP - wastedHP;
                    return true;
                }

                return false;
            }

            bool hpMoreUrgent = hpPct <= mpPct;
            if (hpMoreUrgent)
            {
                if (kind == BotPotionKind.Health)
                {
                    tier = 300;
                    primary = effectiveHP;
                    secondary = -wastedHP;
                    return true;
                }

                if (kind == BotPotionKind.Dual)
                {
                    tier = 250;
                    primary = effectiveHP + effectiveMP;
                    secondary = -(wastedHP + wastedMP);
                    return true;
                }

                if (kind == BotPotionKind.Mana)
                {
                    tier = 200;
                    primary = effectiveMP;
                    secondary = -wastedMP;
                    return true;
                }

                return false;
            }

            if (kind == BotPotionKind.Mana)
            {
                tier = 300;
                primary = effectiveMP;
                secondary = -wastedMP;
                return true;
            }

            if (kind == BotPotionKind.Dual)
            {
                tier = 250;
                primary = effectiveHP + effectiveMP;
                secondary = -(wastedHP + wastedMP);
                return true;
            }

            if (kind == BotPotionKind.Health)
            {
                tier = 200;
                primary = effectiveHP;
                secondary = -wastedHP;
                return true;
            }

            return false;
        }

        private static bool ShouldBotRecoverResource(int missingValue, int restoreValue, long currentPct, long criticalPct)
        {
            if (missingValue <= 0 || restoreValue <= 0) return false;
            if (currentPct <= criticalPct) return true;

            return missingValue * 100 >= Math.Max(1, restoreValue) * BotPotionEffectiveUsePct;
        }

        private static BotPotionKind GetBotPotionKind(UserItem item, out int hpRestore, out int mpRestore)
        {
            return GetBotPotionKind(item?.Info, out hpRestore, out mpRestore);
        }

        // 硬编码的双效药名称：这些药视作"上金创药+魔法药"同效，直接走 Dual 路径
        private static readonly HashSet<string> BotDualPotionNames = new HashSet<string>(StringComparer.OrdinalIgnoreCase)
        {
            "万年雪霜", "万年雪霜（绑定）",
            "太阳水", "太阳水（绑定）",
            "强效太阳水", "强效太阳水（绑定）",
        };

        private static BotPotionKind GetBotPotionKind(ItemInfo info, out int hpRestore, out int mpRestore)
        {
            hpRestore = 0;
            mpRestore = 0;

            if (info == null) return BotPotionKind.None;
            if (info.ItemType != ItemType.Consumable) return BotPotionKind.None;

            // ★ 先兼容一批特殊双效药：有些配置并不严格依赖 Shape/Stat，直接按名称兜底识别。
            if (!string.IsNullOrEmpty(info.ItemName) && BotDualPotionNames.Contains(info.ItemName))
            {
                hpRestore = Math.Max(1, Math.Max(0, info.Stats[Stat.Health]));
                mpRestore = Math.Max(1, Math.Max(0, info.Stats[Stat.Mana]));
                return BotPotionKind.Dual;
            }

            hpRestore = Math.Max(0, info.Stats[Stat.Health]);
            mpRestore = Math.Max(0, info.Stats[Stat.Mana]);

            // ★ 核心修正：服务端药水识别改为优先复用 ItemInfo.CanAutoPot。
            //   客户端自动喝药、本地辅助面板和编辑器都以 CanAutoPot 标记药品；
            //   之前仅靠 Shape=0 会漏掉部分实际可自动喝的药，导致背包里有药却统计不到、也喝不到。
            if (info.CanAutoPot)
            {
                if (hpRestore > 0 && mpRestore > 0) return BotPotionKind.Dual;
                if (hpRestore > 0) return BotPotionKind.Health;
                if (mpRestore > 0) return BotPotionKind.Mana;
            }

            // 兼容旧物品配置：即便没勾 CanAutoPot，只要确实带 HP/MP 恢复值，也仍按药水识别。
            if (hpRestore > 0 && mpRestore > 0) return BotPotionKind.Dual;
            if (hpRestore > 0) return BotPotionKind.Health;
            if (mpRestore > 0) return BotPotionKind.Mana;

            return BotPotionKind.None;
        }


        private static int GetBotPotionCooldownMs(PlayerObject player, UserItem item)
        {
            if (player == null || item?.Info == null) return 0;

            int cooldownMs = item.Info.Durability;
            cooldownMs -= cooldownMs * player.Stats[Stat.Marvellously] / 100;

            return Math.Max(0, cooldownMs);
        }

        private static bool TryUseBotPotion(PlayerObject player, int slot, out int potionCooldownMs)
        {
            potionCooldownMs = 0;
            if (player?.Inventory == null) return false;
            if (slot < 0 || slot >= player.Inventory.Length) return false;

            UserItem item = player.Inventory[slot];
            if (item?.Info == null)
                return false;

            potionCooldownMs = GetBotPotionCooldownMs(player, item);

            long beforeCount = item.Count;
            DateTime originalUseItemTime = player.UseItemTime;
            DateTime originalAutoPotionTime = player.AutoPotionTime;
            CellLinkInfo originalDelayItemUse = player.DelayItemUse;
            bool used = false;

            try
            {
                player.DelayItemUse = null;

                if (player.AutoPotionTime > SEnvir.Now)
                    player.AutoPotionTime = SEnvir.Now;

                player.UseItemTime = SEnvir.Now;
                player.ItemUse(new CellLinkInfo
                {
                    GridType = GridType.Inventory,
                    Slot = slot,
                    Count = 1,  // ← ParseLinks 要求 Count > 0，否则第一行即 return
                });

                UserItem afterItem = player.Inventory[slot];
                used = afterItem == null || !ReferenceEquals(afterItem, item) || afterItem.Count < beforeCount;
                if (used)
                {
                    player.DelayItemUse = null;
                    RecordBotPotionUsage(player);
                }

                return used;

            }
            finally
            {
                if (!used)
                {
                    player.UseItemTime = originalUseItemTime;
                    player.AutoPotionTime = originalAutoPotionTime;
                    player.DelayItemUse = originalDelayItemUse;
                }
            }
        }

        /// <summary>
        /// 自动使用非药水消耗品：
        ///   • Shape=1 Buff 类（油类、短时加属性类）：对应 ItemBuff 不存在或剩余时间 &lt; 30 秒时自动使用
        /// 药水（Shape=0）由独立的 200ms 药水监控负责，这里不再参与，避免与战斗主循环互相阻塞。
        /// </summary>
        private static void ProcessBotUseConsumable(PlayerObject player)
        {
            if (player.Dead) return;

            for (int i = 0; i < player.Inventory.Length; i++)
            {
                UserItem item = player.Inventory[i];
                if (item == null || item.Info == null) continue;
                if (item.Info.ItemType != ItemType.Consumable) continue;
                if (item.Info.Shape != 1) continue;

                // 找当前玩家是否已有该 ItemBuff
                BuffInfo existing = player.Buffs.FirstOrDefault(
                    x => x.Type == BuffType.ItemBuff && x.ItemIndex == item.Info.Index);

                // 永久 Buff（RemainingTime == MaxValue）无需重复使用
                if (existing != null && existing.RemainingTime == TimeSpan.MaxValue) continue;

                // Buff 剩余时间充足（>30秒）则跳过
                if (existing != null && existing.RemainingTime > TimeSpan.FromSeconds(30)) continue;

                // Buff 不存在或剩余 ≤30 秒 → 使用
                player.ItemUse(new CellLinkInfo
                {
                    GridType = GridType.Inventory,
                    Slot = i,
                });
            }
        }

        /// <summary>
        /// 一键出售背包中所有可出售的物品，获得金币。
        /// 过滤规则与客户端 CheckLink(RootSell) 完全对齐：
        ///   • CanSell == false   ── 系统标记不可出售（赞助币/红包/金币等特殊道具
        ///                           的 CanSell 本身为 false，故自动被拦截，无需额外判断 ItemEffect）
        ///   • Worthless 标记     ── 无价值物品
        ///   • Locked 标记        ── 锁定物品
        ///   • Marriage 标记      ── 婚戒
        /// 对于不可出售（CanSell=false）且不可丢弃（CanDrop=false）的物品，忽略。
        /// 对于不可出售（CanSell=false）但可丢弃（CanDrop=true）的物品：
        ///   非安全区时直接丢弃到地上（IsTemporary=true，和 ItemDrop 逻辑等价）。
        ///   安全区内跳过（不能丢弃）。
        /// 出售逻辑与 NPCRootSell 核心逻辑等价，绕开 NPC 对话流程。
        ///
        /// 冷却机制：
        ///   • 正常情况下每 <see cref="BotSellCooldownSeconds"/> 秒执行一次（避免每Tick扫全背包）。
        ///   • 背包空格 ≤ <see cref="BotSellUrgentFreeSlots"/> 或
        ///     背包负重 ≥ MaxBagWeight × <see cref="BotSellUrgentWeightPct"/>% 时，
        ///     立即绕过冷却强制执行。
        /// </summary>
        private static bool ShouldBotKeepSkillBook(PlayerObject player, UserItem item)
        {
            if (player == null || item?.Info == null || item.Info.ItemType != ItemType.Book)
                return false;

            if (!ClassToRequired.TryGetValue(player.Class, out RequiredClass reqClass))
                reqClass = RequiredClass.All;

            MagicInfo magic = SEnvir.MagicInfoList.Binding.FirstOrDefault(x => x?.Index == item.Info.Shape);
            if (magic == null) return false;
            if (magic.Class != player.Class) return false;
            if (!IsBotSkillBookClassMatch(item.Info, reqClass)) return false;

            return !player.Magics.ContainsKey(magic.Magic);
        }

        private static bool TryGetBotPriorityMissingSkills(PlayerObject player, out List<MagicInfo> missingSkills)
        {
            missingSkills = null;
            if (player == null || player.Dead) return false;

            // 诊断：检查等级范围
            if (player.Level <= 20 || player.Level > 60)
            {
                return false;
            }

            // 诊断：检查强制切图阻挡原因
            var blockReason = GetBotForceLevelRangeSwitchBlockReason(player);
            if (blockReason != BotForceLevelRangeSwitchBlockReason.None)
            {
                return false;
            }

            List<MagicInfo> skills = new List<MagicInfo>();
            foreach (MagicInfo magic in SEnvir.MagicInfoList.Binding)
            {
                if (magic == null || magic.Class != player.Class) continue;
                if (magic.NeedLevel1 <= 20 || magic.NeedLevel1 > player.Level || magic.NeedLevel1 > 60) continue;
                if (player.Magics.ContainsKey(magic.Magic)) continue;

                skills.Add(magic);
            }

            if (skills.Count == 0)
            {
                return false;
            }

            missingSkills = skills
                .OrderBy(x => x.NeedLevel1)
                .ThenBy(x => x.Index)
                .ToList();

            return true;
        }

        private static int GetBotMissingSkillDropScore(PlayerObject player, ItemInfo item, bool partOnly, List<MagicInfo> missingSkills)
        {
            if (player == null || item == null || missingSkills == null || missingSkills.Count == 0)
                return 0;

            if (!ClassToRequired.TryGetValue(player.Class, out RequiredClass reqClass))
                reqClass = RequiredClass.All;

            string itemName = item.ItemName ?? string.Empty;
            int bestScore = 0;

            foreach (MagicInfo magic in missingSkills)
            {
                bool isSkillBook = item.ItemType == ItemType.Book && IsBotSkillBookClassMatch(item, reqClass);
                bool shapeMatch = isSkillBook && item.Shape == magic.Index;
                bool nameMatch = string.Equals(itemName, magic.Name, StringComparison.Ordinal);
                bool manualMatch = string.Equals(itemName, GetBotSkillRecipeManualItemName(magic.Name), StringComparison.Ordinal);
                bool pageMatch = string.Equals(itemName, GetBotSkillRecipePageItemName(magic.Name), StringComparison.Ordinal);
                bool partMatch = partOnly && string.Equals(itemName, magic.Name, StringComparison.Ordinal);

                int score = 0;
                if (manualMatch || (shapeMatch && IsBotDirectManualInfo(item)))
                    score = 320;
                else if (shapeMatch || nameMatch)
                    score = 260;
                else if (pageMatch)
                    score = 220;
                else if (partMatch)
                    score = 180;

                if (score <= 0) continue;

                score += Math.Max(0, 45 - magic.NeedLevel1) * 3;
                bestScore = Math.Max(bestScore, score);
            }

            return bestScore;
        }

        private static int GetBotMissingSkillMonsterDropScore(PlayerObject player, MonsterInfo monster, List<MagicInfo> missingSkills)
        {
            if (player == null || monster?.Drops == null || missingSkills == null || missingSkills.Count == 0)
                return 0;

            int bestScore = 0;
            int totalScore = 0;

            foreach (DropInfo drop in monster.Drops)
            {
                if (drop?.Item == null) continue;

                int dropScore = GetBotMissingSkillDropScore(player, drop.Item, drop.PartOnly, missingSkills);
                if (dropScore <= 0) continue;

                int chanceBonus = (int)Math.Round(Math.Min(80d, Math.Log10(Math.Max(10, drop.Chance)) * 16d));
                int amountBonus = Math.Min(24, Math.Max(0, drop.Amount - 1) * 4);
                dropScore += chanceBonus + amountBonus;

                bestScore = Math.Max(bestScore, dropScore);
                totalScore += dropScore;
            }

            return bestScore * 4 + totalScore;
        }

        private static int GetBotPotionSellKeepCount(BotPotionKind kind, bool emergencyFloor)
        {
            switch (kind)
            {
                case BotPotionKind.Health:
                    return emergencyFloor ? Math.Max(10, Config.BotMinHealthPotionCount / 8) : Config.BotMinHealthPotionCount;
                case BotPotionKind.Mana:
                    return emergencyFloor ? Math.Max(10, Config.BotMinManaPotionCount / 8) : Config.BotMinManaPotionCount;
                case BotPotionKind.Dual:
                    return emergencyFloor ? Math.Max(2, BotMinDualPotionCount / 8) : BotMinDualPotionCount;
                default:
                    return 0;
            }
        }

        private static int SellBotInventoryStack(PlayerObject player, int slot, UserItem item, int count, ref long totalGold)
        {
            if (player == null || item?.Info == null || count <= 0) return 0;

            int sellCount = (int)Math.Min((long)item.Count, count);
            if (sellCount <= 0) return 0;

            long price = item.Price(sellCount);
            if (price <= 0) return 0;

            if (item.Count == (uint)sellCount)
            {
                if (Config.AllowBuyback && item.CanBuyback)
                {
                    item.MarkOwnerless(OwnerlessItemType.UserSold);
                    player.Inventory[slot] = null;
                    SEnvir.AllOwnerlessItemList.Add(item);
                }
                else
                {
                    player.RemoveItem(item);
                    player.Inventory[slot] = null;
                    item.Delete();
                }
            }
            else
            {
                item.Count -= (uint)sellCount;
                player.Enqueue(new S.ItemChanged
                {
                    Link = new CellLinkInfo
                    {
                        GridType = GridType.Inventory,
                        Slot = slot,
                        Count = item.Count,
                    },
                    Success = true,
                });
            }

            totalGold += price;
            return sellCount;
        }

        private static bool TrySellBotPotionPassForWeight(
            PlayerObject player,
            long targetWeight,
            bool emergencyFloor,
            ref long currentWeight,
            ref int healthCount,
            ref int manaCount,
            ref int dualCount,
            ref long totalGold,
            ref int soldCount)
        {
            bool soldAny = false;

            for (int i = player.Inventory.Length - 1; i >= 0 && currentWeight > targetWeight; i--)
            {
                UserItem item = player.Inventory[i];
                if (item?.Info == null) continue;
                if ((item.Flags & UserItemFlags.Locked) == UserItemFlags.Locked) continue;
                if ((item.Flags & UserItemFlags.Marriage) == UserItemFlags.Marriage) continue;
                if ((item.Flags & UserItemFlags.Worthless) == UserItemFlags.Worthless) continue;
                if (!item.Info.CanSell) continue;
                if (!player.CanUseItem(item)) continue;

                BotPotionKind kind = GetBotPotionKind(item, out int _, out int _);
                if (kind == BotPotionKind.None) continue;

                int currentKindCount = 0;
                switch (kind)
                {
                    case BotPotionKind.Health:
                        currentKindCount = healthCount;
                        break;
                    case BotPotionKind.Mana:
                        currentKindCount = manaCount;
                        break;
                    case BotPotionKind.Dual:
                        currentKindCount = dualCount;
                        break;
                }

                int keepCount = GetBotPotionSellKeepCount(kind, emergencyFloor);
                int removable = currentKindCount - keepCount;
                if (removable <= 0) continue;

                int unitWeight = item.Info.Weight;
                if (unitWeight <= 0) continue;

                long needWeightLoss = currentWeight - targetWeight;
                int sellByWeight = (int)Math.Ceiling(needWeightLoss / (double)unitWeight);
                int sellCount = Math.Min(removable, Math.Min((int)item.Count, Math.Max(1, sellByWeight)));
                if (sellCount <= 0) continue;

                int actualSold = SellBotInventoryStack(player, i, item, sellCount, ref totalGold);
                if (actualSold <= 0) continue;

                currentWeight -= (long)actualSold * unitWeight;
                soldCount++;
                soldAny = true;

                switch (kind)
                {
                    case BotPotionKind.Health:
                        healthCount -= actualSold;
                        break;
                    case BotPotionKind.Mana:
                        manaCount -= actualSold;
                        break;
                    case BotPotionKind.Dual:
                        dualCount -= actualSold;
                        break;
                }
            }

            return soldAny;
        }

        private static bool TrySellBotExcessPotionsForWeight(PlayerObject player, long targetWeight, ref long totalGold, ref int soldCount)
        {
            if (player == null || player.Inventory == null) return false;
            if (player.BagWeight <= targetWeight) return false;

            CountBotPotionStock(player, out int healthCount, out int manaCount, out int dualCount);

            long currentWeight = player.BagWeight;
            bool soldAny = TrySellBotPotionPassForWeight(player, targetWeight, false,
                ref currentWeight, ref healthCount, ref manaCount, ref dualCount, ref totalGold, ref soldCount);

            if (currentWeight > targetWeight)
            {
                soldAny |= TrySellBotPotionPassForWeight(player, targetWeight, true,
                    ref currentWeight, ref healthCount, ref manaCount, ref dualCount, ref totalGold, ref soldCount);
            }

            if (soldAny)
                player.RefreshWeight();

            return soldAny;
        }

        private static void ProcessBotSellInventory(PlayerObject player)
        {
            if (player == null || player.Dead || !Config.BotAutoSellTrash) return;

            uint pid = player.ObjectID;

            // ── 紧急条件检测 ────────────────────────────────────────────────────
            int freeSlots = 0;
            for (int i = 0; i < player.Inventory.Length; i++)
                if (player.Inventory[i] == null) freeSlots++;

            int maxBagWeight = player.Stats[Stat.BagWeight];
            bool weightUrgent = maxBagWeight > 0
                && player.BagWeight >= (long)maxBagWeight * BotSellUrgentWeightPct / 100;
            bool slotUrgent = freeSlots <= BotSellUrgentFreeSlots;
            bool isUrgent = slotUrgent || weightUrgent;

            // ── 冷却检查（紧急时跳过）───────────────────────────────────────────
            if (!isUrgent)
            {
                if (_botSellTime.TryGetValue(pid, out DateTime nextSell) && SEnvir.Now < nextSell)
                    return;
            }

            // ── 更新下次出售时间 ────────────────────────────────────────────────
            _botSellTime[pid] = SEnvir.Now.AddSeconds(BotSellCooldownSeconds);

            long totalGold = 0;
            int soldCount = 0;
            int dropCount = 0;

            if (weightUrgent && maxBagWeight > 0)
            {
                long targetWeight = (long)maxBagWeight * BotSellPotionTargetWeightPct / 100;
                if (targetWeight < player.BagWeight)
                    TrySellBotExcessPotionsForWeight(player, targetWeight, ref totalGold, ref soldCount);
            }

            for (int i = player.Inventory.Length - 1; i >= 0; i--)  // 倒序，避免位移问题
            {
                UserItem item = player.Inventory[i];
                if (item == null) continue;

                // 锁定 / 婚戒 不碰（与 CheckLink(RootSell) 一致）
                if ((item.Flags & UserItemFlags.Locked) == UserItemFlags.Locked) continue;
                if ((item.Flags & UserItemFlags.Marriage) == UserItemFlags.Marriage) continue;

                // 只保留当前职业后续还可能学到的技能书；错职业、已学会或无效书直接卖掉。
                if (item.Info.ItemType == ItemType.Book && ShouldBotKeepSkillBook(player, item)) continue;

                // 可用药水必须留着战斗喝；不能用的旧药则允许卖掉，给补货腾位。
                int potionHP;
                int potionMP;
                if (GetBotPotionKind(item, out potionHP, out potionMP) != BotPotionKind.None && player.CanUseItem(item))
                    continue;

                // 攻城申请要用的有效祖玛头像必须保留；无效来源的不保护，避免长期占包。
                if (item.Info.Effect == ItemEffect.UmaKingHorn && IsValidUmaKingHornForConquest(item))
                    continue;

                // 会实际升级到身上的装备必须保留，避免自动出售先于自动换装把候选卖掉。
                if (IsEquipmentItem(item.Info.ItemType) && ShouldBotKeepEquipmentUpgradeCandidate(player, item))
                    continue;

                // 极品装备优先用于真人交易，不要卖掉。评分必须包含当前物品的随机/极品附加属性。
                if (IsEquipmentItem(item.Info.ItemType) && IsItemTradable(player, item))
                {
                    int score = (int)CalculateWeightedItemScore(item, player.Character.Class);
                    if (score >= BotPremiumEquipmentScoreThreshold)
                        continue;
                }

                // ── 尝试出售 ─────────────────────────────────────────────

                if (item.Info.CanSell && (item.Flags & UserItemFlags.Worthless) != UserItemFlags.Worthless)
                {
                    long price = item.Price(item.Count);
                    if (price > 0)
                    {
                        // 回购支持（与 NPCRootSell 一致）
                        if (Config.AllowBuyback && item.CanBuyback)
                        {
                            item.MarkOwnerless(OwnerlessItemType.UserSold);
                            player.Inventory[i] = null;
                            SEnvir.AllOwnerlessItemList.Add(item);
                        }
                        else
                        {
                            player.RemoveItem(item);
                            player.Inventory[i] = null;
                            item.Delete();
                        }

                        totalGold += price;
                        soldCount++;
                        continue;
                    }
                }

                // ── 无法出售 → 非安全区时丢弃 ────────────────────────────
                if (!item.Info.CanDrop) continue;
                if (player.InSafeZone) continue;

                Cell cell = player.GetDropLocation(1, null);
                if (cell == null) continue;

                player.RemoveItem(item);
                player.Inventory[i] = null;
                item.IsTemporary = true;

                ItemObject ob = new ItemObject { Item = item };
                if ((item.Flags & UserItemFlags.Bound) == UserItemFlags.Bound)
                    ob.Account = player.Character.Account;

                ob.Spawn(player.CurrentMap.Info, cell.Location);
                dropCount++;
            }

            if (soldCount > 0 || dropCount > 0)
                player.RefreshWeight();

            if (totalGold > 0)
                ChangeBotGoldSilently(player, totalGold);
        }

        /// <summary>
        /// 自动将背包中的货币类道具兑换为账号赞助币，绕开 NPC 脚本直接执行等价逻辑。
        ///
        /// 处理两类道具：
        ///   1. ItemEffect.GameGold ── 赞助币道具（直接双击等价，item.Count 即赞助币数量）
        ///   2. 名称含"红包/利是/RedPacket/Envelope"的道具
        ///        ── 此类道具在游戏里需前往"比奇钱掌柜"NPC 兑换赞助币，
        ///           兑换逻辑为 TakeItem(红包道具) + GainItem(GameGold道具)；
        ///           GainItem 中 ItemEffect.GameGold 分支会再次自动兑换，
        ///           因此整体效果等价于：直接 ChangeGameGold(item.Count) + 删除道具。
        ///           注：比例为 1:item.Count（堆叠数量即赞助币数量，按服务器配置）。
        ///
        /// 与真人流程的等价性：
        ///   GainItem → ItemEffect.GameGold → account.GameGold += count → item.Delete()
        ///
        /// 不处理：Locked、Marriage 标记的道具。
        /// </summary>
        private static void ProcessBotUseGameGoldItems(PlayerObject player)
        {
            if (player.Dead) return;

            for (int i = player.Inventory.Length - 1; i >= 0; i--)
            {
                UserItem item = player.Inventory[i];
                if (item == null) continue;

                // 锁定 / 婚戒 不碰
                if ((item.Flags & UserItemFlags.Locked) == UserItemFlags.Locked) continue;
                if ((item.Flags & UserItemFlags.Marriage) == UserItemFlags.Marriage) continue;

                bool isGameGoldItem = item.Info.Effect == ItemEffect.GameGold;
                bool isRedPacketItem = !isGameGoldItem && IsRedPacketItem(item.Info.ItemName);

                if (!isGameGoldItem && !isRedPacketItem) continue;

                int amount = (int)item.Count;

                player.RemoveItem(item);
                player.Inventory[i] = null;
                item.IsTemporary = true;
                item.Delete();

                string source = isRedPacketItem ? "假人红包兑换" : "假人自动";
                player.ChangeGameGold(amount, source, CurrencySource.ItemAdd, "ProcessBotUseGameGoldItems()");
            }
        }

        /// <summary>
        /// 判断道具名称是否属于"红包类"道具（需去比奇钱掌柜兑换赞助币的道具）。
        /// 判断规则与客户端 BigPatchDialog 的自动捡取逻辑一致。
        /// </summary>
        private static bool IsRedPacketItem(string itemName)
        {
            if (string.IsNullOrEmpty(itemName)) return false;
            return itemName.Contains("红包")
                || itemName.Contains("利是")
                || itemName.Contains("RedPacket")
                || itemName.Contains("Envelope");
        }

        /// <summary>
        /// 遍历背包，按当前职业权重找出评分高于当前装备槽的物品并换装。
        /// 评分包含基础属性与精炼/附加属性，负属性保留扣分。
        ///
        /// 戒指（Ring）和手镯（Bracelet）各有左右两槽，采用"合并池"策略：
        ///   1. 将身上已穿的 L/R 槽 + 背包中所有同类物品汇入候选池
        ///   2. 按分值降序排列候选池
        ///   3. 分值最高的穿左槽，次高的穿右槽（空槽视为分值 -1）
        ///   4. 原槽位物品被替换时放回背包（由 PutOnEquip 内部处理）
        /// </summary>
        private static void ProcessBotAutoEquip(PlayerObject player)
        {
            if (player == null || player.Dead || !Config.BotAutoEquip) return;

            // ★ 性能优化：自动穿装不需要每 800ms 都执行，每 5 秒检查一次足够
            uint pid = player.ObjectID;
            DateTime now = SEnvir.Now;
            if (_botLastAutoEquipCheckTime.TryGetValue(pid, out DateTime lastCheck) && now < lastCheck)
                return;
            _botLastAutoEquipCheckTime[pid] = now.AddSeconds(BotAutoEquipCheckInterval);

            // ── 单槽装备（非戒指/手镯）：直接对比换装 ──────────────────────────
            for (int i = 0; i < player.Inventory.Length; i++)
            {
                UserItem invItem = player.Inventory[i];
                if (invItem?.Info == null) continue;

                // 只处理可映射到装备槽的物品类型（戒指/手镯已从映射表移除，下方单独处理）
                if (!ItemTypeToSlot.TryGetValue(invItem.Info.ItemType, out EquipmentSlot slot))
                    continue;
                if (!CanBotUsePotionInfo(player, invItem.Info))
                    continue;

                int slotIndex = (int)slot;

                // 计算背包物品综合属性值
                long invScore = CalculateWeightedItemScore(invItem, player.Class);

                // 获取当前装备槽的物品
                UserItem curItem = player.Equipment[slotIndex];
                long curScore = curItem != null ? CalculateWeightedItemScore(curItem, player.Class) : -1L;

                // 仅当背包物品属性更高时换装
                if (invScore > curScore)
                {
                    player.PutOnEquip(invItem, slotIndex);
                }
            }

            // ── 双槽装备：戒指（RingL / RingR）────────────────────────────────
            AutoEquipDualSlot(player, ItemType.Ring,
                EquipmentSlot.RingL, EquipmentSlot.RingR);

            // ── 双槽装备：手镯（BraceletL / BraceletR）──────────────────────────
            AutoEquipDualSlot(player, ItemType.Bracelet,
                EquipmentSlot.BraceletL, EquipmentSlot.BraceletR);
        }

        /// <summary>
        /// 双槽装备自动换装：将身上 slotA / slotB 的物品与背包中同类物品合并，
        /// 按属性分值降序排列后，最高分穿 slotA（左槽），次高分穿 slotB（右槽）。
        ///
        /// 实现要点：
        ///   1. 收集候选池（已穿 + 背包同类）并按分值降序排列
        ///   2. 若目标物品已在装备槽（左或右），先用 ItemMove 将其换回背包，
        ///      以便 PutOnEquip 能找到它（PutOnEquip 只从背包查找）
        ///   3. 依次调用 PutOnEquip 穿入最优两件
        /// </summary>
        private static void AutoEquipDualSlot(
            PlayerObject player,
            ItemType type,
            EquipmentSlot slotA,
            EquipmentSlot slotB)
        {
            int idxA = (int)slotA;
            int idxB = (int)slotB;

            // ── 收集候选池 ──────────────────────────────────────────────────────
            var candidates = new List<UserItem>();

            if (player.Equipment[idxA] != null) candidates.Add(player.Equipment[idxA]);
            if (player.Equipment[idxB] != null) candidates.Add(player.Equipment[idxB]);

            foreach (UserItem inv in player.Inventory)
            {
                if (inv?.Info == null) continue;
                if (inv.Info.ItemType == type && CanBotUsePotionInfo(player, inv.Info)) candidates.Add(inv);
            }

            if (candidates.Count == 0) return;

            // ── 按分值降序排列 ───────────────────────────────────────────────────
            candidates.Sort((a, b) => CalculateWeightedItemScore(b, player.Class)
                .CompareTo(CalculateWeightedItemScore(a, player.Class)));

            UserItem wantA = candidates.Count >= 1 ? candidates[0] : null;
            UserItem wantB = candidates.Count >= 2 ? candidates[1] : null;

            UserItem curA = player.Equipment[idxA];
            UserItem curB = player.Equipment[idxB];

            // 无需任何变化
            if (wantA == curA && wantB == curB) return;

            // ── 若目标物品当前在装备槽，先移回背包（PutOnEquip 从背包查找）──────
            // wantA 可能在 slotB，wantB 可能在 slotA
            MoveEquipToInventory(player, idxA, wantA, wantB);
            MoveEquipToInventory(player, idxB, wantA, wantB);

            // ── 穿入最优的两件 ───────────────────────────────────────────────────
            // 先穿 slotA（分值最高），再穿 slotB（次高）
            if (wantA != null && player.Equipment[idxA] != wantA)
                player.PutOnEquip(wantA, idxA);
            if (wantB != null && player.Equipment[idxB] != wantB)
                player.PutOnEquip(wantB, idxB);
        }

        /// <summary>
        /// 若装备槽 slotIndex 中的物品不是 wantA 也不是 wantB（即该槽内容需要被替换），
        /// 则将其从装备槽移到背包空格，为目标物品腾位。
        /// 若该槽的物品本身就是 wantA 或 wantB，先移回背包以便 PutOnEquip 找到它。
        /// </summary>
        private static void MoveEquipToInventory(
            PlayerObject player,
            int slotIndex,
            UserItem wantA,
            UserItem wantB)
        {
            UserItem cur = player.Equipment[slotIndex];
            if (cur == null) return;

            // 如果当前槽里的物品就是我们要穿的目标之一，也需要先移回背包
            // （PutOnEquip 的前提是物品在背包中）
            bool isTarget = (cur == wantA || cur == wantB);
            if (!isTarget)
            {
                // 当前槽的物品不是目标：判断是否会被换掉
                // 只有当两个目标都不是 cur 时才需要腾位；
                // 但 PutOnEquip 会自动把旧装备放到来源背包格，所以其实不需要预先移动。
                // 仅当目标物品来自装备槽（不在背包）时才需要这里的逻辑，上方 isTarget 已覆盖。
                return;
            }

            // cur 是目标物品 → 移回背包
            int emptySlot = FindEmptyInventorySlot(player);
            if (emptySlot < 0) return; // 背包满了，无法移动

            player.Equipment[slotIndex] = null;
            player.Inventory[emptySlot] = cur;
            cur.Slot = emptySlot;
            player.RefreshStats();
        }

        /// <summary>
        /// 找背包中第一个空格索引，未找到返回 -1。
        /// </summary>
        private static int FindEmptyInventorySlot(PlayerObject player)
        {
            for (int i = 0; i < player.Inventory.Length; i++)
                if (player.Inventory[i] == null) return i;
            return -1;
        }

        // ══════════════════════════════════════════════════════════════════════
        //  装备升级决策系统
        // ══════════════════════════════════════════════════════════════════════

        /// <summary>
        /// 按职业加权计算装备评分。
        /// 战士优先攻击/准确，法师优先魔法，道士优先道术，刺客优先敏捷/暴击。
        /// </summary>
        private static long CalculateWeightedItemScore(ItemInfo info, MirClass playerClass)
        {
            if (info == null) return 0L;

            long score = 0;
            foreach (var kv in info.Stats.Values)
            {
                Stat stat = kv.Key;
                int value = kv.Value;
                double weight = GetStatWeightForClass(stat, playerClass);

                score += (long)(value * weight);
            }

            return score;
        }

        private static long CalculateWeightedItemScore(UserItem item, MirClass playerClass)
        {
            if (item?.Info == null) return 0L;

            long score = CalculateWeightedItemScore(item.Info, playerClass);
            foreach (var kv in item.Stats.Values)
                score += (long)(kv.Value * GetStatWeightForClass(kv.Key, playerClass));

            return score;
        }

        private static bool ShouldBotKeepEquipmentUpgradeCandidate(PlayerObject player, UserItem item)
        {
            if (player == null || item?.Info == null) return false;
            if (!CanBotUsePotionInfo(player, item.Info)) return false;

            if (item.Info.ItemType == ItemType.Ring)
            {
                IEnumerable<UserItem> candidates = player.Equipment
                    .Where(x => x?.Info?.ItemType == ItemType.Ring)
                    .Concat(player.Inventory.Where(x => x?.Info?.ItemType == ItemType.Ring && CanBotUsePotionInfo(player, x.Info)));
                return candidates.OrderByDescending(x => CalculateWeightedItemScore(x, player.Class)).Take(2).Contains(item);
            }

            if (item.Info.ItemType == ItemType.Bracelet)
            {
                IEnumerable<UserItem> candidates = player.Equipment
                    .Where(x => x?.Info?.ItemType == ItemType.Bracelet)
                    .Concat(player.Inventory.Where(x => x?.Info?.ItemType == ItemType.Bracelet && CanBotUsePotionInfo(player, x.Info)));
                return candidates.OrderByDescending(x => CalculateWeightedItemScore(x, player.Class)).Take(2).Contains(item);
            }

            if (!ItemTypeToSlot.TryGetValue(item.Info.ItemType, out EquipmentSlot slot))
                return false;

            UserItem equippedItem = player.Equipment[(int)slot];
            return equippedItem == null
                || CalculateWeightedItemScore(item, player.Class) > CalculateWeightedItemScore(equippedItem, player.Class);
        }

        /// <summary>
        /// 根据职业获取属性的权重。
        /// 战士：DC/准确权重高，MR/HP中等
        /// 法师：MC权重高，MP/HP中等
        /// 道士：SC权重高，MP/HP中等
        /// 刺客：敏捷/暴击权重高，DC/准确次之
        /// </summary>
        private static double GetStatWeightForClass(Stat stat, MirClass playerClass)
        {
            switch (playerClass)
            {
                case MirClass.Warrior:
                    // 战士优先 DC、准确、AC、MR
                    switch (stat)
                    {
                        case Stat.MinDC:
                        case Stat.MaxDC:
                            return 2.0;
                        case Stat.Accuracy:
                            return 1.5;
                        case Stat.MinAC:
                        case Stat.MaxAC:
                        case Stat.MinMR:
                        case Stat.MaxMR:
                        case Stat.Health:
                            return 1.0;
                        default:
                            return 0.5;
                    }

                case MirClass.Wizard:
                    // 法师优先 MC
                    switch (stat)
                    {
                        case Stat.MinMC:
                        case Stat.MaxMC:
                            return 2.5;
                        case Stat.Mana:
                            return 1.5;
                        case Stat.MinMR:
                        case Stat.MaxMR:
                        case Stat.Health:
                            return 1.0;
                        default:
                            return 0.5;
                    }

                case MirClass.Taoist:
                    // 道士优先 SC
                    switch (stat)
                    {
                        case Stat.MinSC:
                        case Stat.MaxSC:
                            return 2.5;
                        case Stat.Mana:
                            return 1.5;
                        case Stat.MinMR:
                        case Stat.MaxMR:
                        case Stat.Health:
                            return 1.0;
                        default:
                            return 0.5;
                    }

                case MirClass.Assassin:
                    // 刺客优先敏捷、暴击、DC
                    switch (stat)
                    {
                        case Stat.Agility:
                            return 2.5;
                        case Stat.Luck:
                        case Stat.CriticalDamage:
                            return 2.0;
                        case Stat.MinDC:
                        case Stat.MaxDC:
                            return 1.5;
                        case Stat.Accuracy:
                            return 1.2;
                        case Stat.MinAC:
                        case Stat.MaxAC:
                        case Stat.MinMR:
                        case Stat.MaxMR:
                        case Stat.Health:
                            return 1.0;
                        default:
                            return 0.5;
                    }

                default:
                    return 1.0;
            }
        }

        /// <summary>
        /// 判断新装备相比当前装备是否有显著提升。
        /// 同时满足：分数差值 >= 阈值 且 提升百分比 >= 最小百分比。
        /// </summary>
        private static bool HasSignificantUpgrade(long currentScore, long newScore)
        {
            if (newScore <= currentScore) return false;

            // 避免除零：如果当前评分为0，直接看差值是否达标
            if (currentScore <= 0)
                return newScore >= BotEquipmentSignificantUpgradeThreshold;

            long scoreDiff = newScore - currentScore;
            decimal upgradePercent = (decimal)scoreDiff / currentScore;

            return scoreDiff >= BotEquipmentSignificantUpgradeThreshold
                   && upgradePercent >= BotEquipmentMinUpgradePercent;
        }

        /// <summary>
        /// 检查商店装备，找出当前装备有显著提升的升级选项。
        /// </summary>
        private static bool CheckBotShopEquipmentUpgrades(
            PlayerObject player,
            out List<(ItemInfo newInfo, long cost, EquipmentSlot slot)> upgrades)
        {
            upgrades = new List<(ItemInfo, long, EquipmentSlot)>();
            if (player == null) return false;

            uint pid = player.ObjectID;

            // 检查是否到了检查间隔
            if (_botLastEquipmentUpgradeCheckTime.TryGetValue(pid, out DateTime lastCheckTime))
            {
                if (SEnvir.Now < lastCheckTime.AddSeconds(BotEquipmentUpgradeCheckInterval))
                    return false;
            }

            _botLastEquipmentUpgradeCheckTime[pid] = SEnvir.Now;

            long availableBudget = CalculateAvailableUpgradeBudget(player);
            if (availableBudget <= 0) return false;

            // 遍历所有装备槽，排除非装备槽位（毒药等）
            foreach (EquipmentSlot slot in Enum.GetValues(typeof(EquipmentSlot)))
            {
                if (slot == EquipmentSlot.Poison) continue;

                // 获取当前装备评分
                UserItem currentItem = GetBotCurrentEquipment(player, slot);
                long currentScore = currentItem != null
                    ? CalculateWeightedItemScore(currentItem, player.Class)
                    : 0;

                // 如果当前装备为空，使用优先级购买逻辑（不在这里处理）
                if (currentScore == 0) continue;

                // 查找商店中更好且符合预算的装备
                if (TryFindBestShopUpgrade(
                        player, slot, currentScore, availableBudget,
                        out ItemInfo bestUpgrade, out long upgradeCost))
                {
                    upgrades.Add((bestUpgrade, upgradeCost, slot));
                }
            }

            return upgrades.Count > 0;
        }

        /// <summary>
        /// 获取当前装备槽的物品（支持双槽装备）。
        /// </summary>
        private static UserItem GetBotCurrentEquipment(PlayerObject player, EquipmentSlot slot)
        {
            if (player == null) return null;

            // 双槽装备：返回分值更高的那件
            if (slot == EquipmentSlot.RingL || slot == EquipmentSlot.RingR)
            {
                int idxL = (int)EquipmentSlot.RingL;
                int idxR = (int)EquipmentSlot.RingR;
                UserItem left = player.Equipment[idxL];
                UserItem right = player.Equipment[idxR];

                if (left == null && right == null) return null;
                if (left == null) return right;
                if (right == null) return left;

                return CalculateWeightedItemScore(left, player.Class) >= CalculateWeightedItemScore(right, player.Class)
                    ? left
                    : right;
            }

            if (slot == EquipmentSlot.BraceletL || slot == EquipmentSlot.BraceletR)
            {
                int idxL = (int)EquipmentSlot.BraceletL;
                int idxR = (int)EquipmentSlot.BraceletR;
                UserItem left = player.Equipment[idxL];
                UserItem right = player.Equipment[idxR];

                if (left == null && right == null) return null;
                if (left == null) return right;
                if (right == null) return left;

                return CalculateWeightedItemScore(left, player.Class) >= CalculateWeightedItemScore(right, player.Class)
                    ? left
                    : right;
            }

            int idx = (int)slot;
            return player.Equipment[idx];
        }

        /// <summary>
        /// 计算可用于装备升级的预算（扣除药水保留金和经济保留金）。
        /// </summary>
        private static long CalculateAvailableUpgradeBudget(PlayerObject player)
        {
            if (player == null || player.Dead) return 0;

            long potionReserve = GetBotPotionReserveGold(player);
            long economyReserveTarget = GetBotEconomyReserveTarget(player);

            return Math.Max(0, player.Gold - potionReserve - economyReserveTarget);
        }

        /// <summary>
        /// 查找商店中比当前装备有显著提升的装备。
        /// </summary>
        private static bool TryFindBestShopUpgrade(
            PlayerObject player,
            EquipmentSlot slot,
            long currentScore,
            long maxBudget,
            out ItemInfo bestUpgrade,
            out long upgradeCost)
        {
            bestUpgrade = null;
            upgradeCost = 0;

            if (player == null) return false;

            long bestScore = currentScore;

            foreach (ItemInfo info in SEnvir.ItemInfoList.Binding)
            {
                if (info == null) continue;

                // 只匹配对应槽位的装备类型
                if (!GetItemTypeForSlot(slot, out ItemType targetItemType))
                    continue;

                if (info.ItemType != targetItemType) continue;

                // 检查是否可穿戴
                if (!CanBotUsePotionInfo(player, info)) continue;

                // 检查预算
                if (!TryGetBotDirectBuyCost(info, out long cost) || cost > maxBudget)
                    continue;

                // 计算新装备评分
                long newScore = CalculateWeightedItemScore(info, player.Class);

                // 检查是否有显著提升
                if (!HasSignificantUpgrade(currentScore, newScore))
                    continue;

                // 选择性价比最高的（分数提升 / 成本）
                long scoreDiff = newScore - currentScore;
                double costEffectiveness = scoreDiff / (double)cost;
                double bestEffectiveness = bestUpgrade != null
                    ? (bestScore - currentScore) / (double)upgradeCost
                    : double.MinValue;

                if (costEffectiveness > bestEffectiveness)
                {
                    bestUpgrade = info;
                    upgradeCost = cost;
                    bestScore = newScore;
                }
            }

            return bestUpgrade != null;
        }

        /// <summary>
        /// 获取装备槽对应的物品类型。
        /// </summary>
        private static bool GetItemTypeForSlot(EquipmentSlot slot, out ItemType itemType)
        {
            itemType = ItemType.Nothing;

            foreach (var kv in ItemTypeToSlot)
            {
                if (kv.Value == slot)
                {
                    itemType = kv.Key;
                    return true;
                }
            }

            // 双槽装备单独处理
            switch (slot)
            {
                case EquipmentSlot.RingL:
                case EquipmentSlot.RingR:
                    itemType = ItemType.Ring;
                    return true;
                case EquipmentSlot.BraceletL:
                case EquipmentSlot.BraceletR:
                    itemType = ItemType.Bracelet;
                    return true;
                default:
                    return false;
            }
        }

        // ══════════════════════════════════════════════════════════════════════
        //  新手初始化：1 级及以下假人赠送乌木剑 + 对应性别布衣 + 初始金币
        // ══════════════════════════════════════════════════════════════════════

        /// <summary>道士新角色额外的初始金币数量。</summary>
        private const long BotTaoistStarterExtraGold = 200_000L;

        /// <summary>
        /// 假人登录后的初始化：
        ///   1. 若等级 ≤ 1 且武器槽为空，赠送"乌木剑"并穿上；
        ///   2. 若等级 ≤ 1 且衣服槽为空，按性别赠送"布衣（男）"/"布衣（女）"并穿上。
        /// 以上均不扣金币，只在对应槽/背包无装备时触发一次。
        /// </summary>
        private static void EquipStarterWeapon(PlayerObject player)
        {
            if (player == null || player.Dead) return;

            // 初始资金和初始装备只属于 1 级及以下的新手初始化，成长后由正常打金经济系统接管。
            if (player.Level > 1) return;

            // ── 1. 乌木剑 ───────────────────────────────────────────────────
            int weaponSlot = (int)EquipmentSlot.Weapon;
            bool hasWeapon = player.Equipment[weaponSlot] != null
                || player.Inventory.Any(x => x?.Info?.ItemType == ItemType.Weapon);
            if (!hasWeapon)
            {
                ItemInfo swordInfo = SEnvir.ItemInfoList.Binding
                    .FirstOrDefault(x => x != null
                        && x.ItemType == ItemType.Weapon
                        && x.ItemName == "乌木剑");
                if (swordInfo != null)
                {
                    try
                    {
                        UserItem sword = SEnvir.CreateFreshItem(swordInfo);
                        player.GainItem(sword);
                    }
                    catch (Exception) { }
                }
            }

            // ── 2. 布衣（对应性别）──────────────────────────────────────────
            int armourSlot = (int)EquipmentSlot.Armour;
            bool hasArmour = player.Equipment[armourSlot] != null
                || player.Inventory.Any(x => x?.Info?.ItemType == ItemType.Armour);
            if (!hasArmour)
            {
                string armourName = player.Gender == MirGender.Female ? "布衣（女）" : "布衣（男）";
                ItemInfo armourInfo = SEnvir.ItemInfoList.Binding
                    .FirstOrDefault(x => x != null
                        && x.ItemType == ItemType.Armour
                        && x.ItemName == armourName);
                if (armourInfo != null)
                {
                    try
                    {
                        UserItem armour = SEnvir.CreateFreshItem(armourInfo);
                        player.GainItem(armour);
                    }
                    catch (Exception) { }
                }
            }

            // ── 3. 一次性装备上 ──────────────────────────────────────────────
            if (Config.BotAutoEquip)
                ProcessBotAutoEquip(player);
        }

        // ══════════════════════════════════════════════════════════════════════
        //  AI – 自动购买适合自己职业/性别的装备（缺槽时触发）
        // ══════════════════════════════════════════════════════════════════════

        private static int CountBotOwnedEquipmentType(PlayerObject player, ItemType itemType)
        {
            if (player == null) return 0;

            int count = 0;
            foreach (UserItem item in player.Equipment)
            {
                if (item?.Info?.ItemType == itemType)
                    count++;
            }

            foreach (UserItem item in player.Inventory)
            {
                if (item?.Info?.ItemType == itemType)
                    count++;
            }

            return count;
        }

        private static readonly Dictionary<string, decimal> BotFallbackDirectBuyRates
            = new Dictionary<string, decimal>(StringComparer.OrdinalIgnoreCase)
        {
            { "基本剑术（秘籍）", 1.1m },
            { "火球术（秘籍）", 1.1m },
            { "治愈术（秘籍）", 1.1m },
            { "金创药（小）", 1.1m },
            { "金创药（中）", 1.1m },
            { "金创药（大）", 1.1m },
            { "金创药（特）", 3m },
            { "魔法药（小）", 1.1m },
            { "魔法药（中）", 1.1m },
            { "魔法药（大）", 1.1m },
            { "魔法药（特）", 3m },
            { "太阳水", 1.1m },
            { "木剑", 1.1m },
            { "匕首", 1.1m },
            { "青铜剑", 1.1m },
            { "铁剑", 1.1m },
            { "乌木剑", 1.1m },
            { "青铜斧", 1.1m },
            { "海魂", 1.1m },
            { "半月", 1.1m },
            { "斩马刀", 1.1m },
            { "偃月", 1.1m },
            { "降魔", 1.1m },
            { "鹤嘴锄", 1.1m },
            { "风之鹤嘴锄", 1.1m },
            { "六绝星环", 1.1m },
            { "指环", 1.1m },
            { "牛角戒指", 1.1m },
            { "水晶魔戒", 1.1m },
            { "古铜戒指", 1.1m },
            { "蓝色水晶戒指", 1.1m },
            { "黑色水晶戒指", 1.1m },
            { "珍珠戒指", 1.1m },
            { "蛇眼戒指", 1.1m },
            { "魅力戒指", 1.1m },
            { "道德戒指", 1.1m },
            { "铁手镯", 1.1m },
            { "小手镯", 1.1m },
            { "银手镯", 1.1m },
            { "皮制手套", 1.1m },
            { "金项链", 1.1m },
            { "传统项链", 1.1m },
            { "布衣（男）", 1.1m },
            { "布衣（女）", 1.1m },
            { "轻型盔甲（男）", 1.1m },
            { "轻型盔甲（女）", 1.1m },
            { "草鞋", 1.1m },
            { "青铜头盔", 1.1m },
            { "魔法头盔", 1.1m },
            { "蜡烛", 1.1m },
            { "亮蜡烛", 1.1m },
            { "火把", 1.1m },
            { "亮火把", 1.1m },
            { "回城卷", 1.1m },
            { "随机传送卷", 1.1m },
            { "黄色药粉", 1.2m },
            { "黄色药粉（小）", 1.2m },
            { "黄色药粉（中）", 1.2m },
            { "黄色药粉（大）", 1.2m },
            { "灰色药粉", 1.2m },
            { "灰色药粉（小）", 1.2m },
            { "灰色药粉（中）", 1.2m },
            { "灰色药粉（大）", 1.2m },
            { "修复油", 16m },
            { "护身符", 1.1m },
            { "火焰护身符", 1.1m },
            { "寒气护身符", 1.1m },
            { "霹雷护身符", 1.1m },
            { "狂风护身符", 1.1m },
            { "神圣护身符", 1.1m },
            { "暗黑护身符", 1.1m },
            { "幻影护身符", 1.1m },
            { "灵魂护身符", 1.1m },
            { "护身符（小）", 1.1m },
            { "狂风护身符（小）", 1.1m },
            { "霹雷护身符（小）", 1.1m },
            { "幻影护身符（小）", 1.1m },
            { "寒气护身符（小）", 1.1m },
            { "神圣护身符（小）", 1.1m },
            { "火焰护身符（小）", 1.1m },
            { "暗黑护身符（小）", 1.1m },
            { "灵魂护身符（小）", 1.1m },
        };

        private static long GetBotFallbackDirectBuyCost(ItemInfo info)
        {
            if (info == null || info.Price <= 0) return 0;
            if (!BotFallbackDirectBuyRates.TryGetValue(info.ItemName, out decimal rate)) return 0;

            return Math.Max(1L, (long)Math.Round(info.Price * rate, MidpointRounding.AwayFromZero));
        }

        private static IEnumerable<ClientNPCGood> EnumerateBotTownNpcGoods()
        {
            if (SEnvir.NPCInfoList == null) yield break;

            foreach (NPCInfo npcInfo in SEnvir.NPCInfoList.Binding)
            {
                if (npcInfo == null || string.IsNullOrEmpty(npcInfo.NPCFile)) continue;

                NPCObject npc = SEnvir.GetNpcObject(npcInfo.Index);
                if (npc?.CurrentMap?.HasSafeZone != true) continue;

                NPCScript script = NPCScript.Get(npcInfo.NPCFile);
                if (script?.Goods == null) continue;

                foreach (ClientNPCGood good in script.Goods)
                {
                    if (good?.Item == null || string.IsNullOrEmpty(good.ItemName)) continue;
                    if (!string.Equals(good.Currency, Globals.Currency, StringComparison.OrdinalIgnoreCase)) continue;

                    yield return good;
                }
            }
        }

        private static bool TryGetBotDirectBuyCost(ItemInfo info, out long cost)
        {
            cost = 0;
            if (info == null || info.Price <= 0 || string.IsNullOrEmpty(info.ItemName)) return false;

            int bestNpcCost = int.MaxValue;
            foreach (ClientNPCGood good in EnumerateBotTownNpcGoods())
            {
                if (!string.Equals(good.ItemName, info.ItemName, StringComparison.OrdinalIgnoreCase)) continue;

                int unitCost = GetBotNpcGoodUnitCost(good);
                if (unitCost <= 0 || unitCost >= int.MaxValue / 4) continue;
                if (unitCost < bestNpcCost)
                    bestNpcCost = unitCost;
            }

            if (bestNpcCost < int.MaxValue)
            {
                cost = bestNpcCost;
                return true;
            }

            long fallbackCost = GetBotFallbackDirectBuyCost(info);
            if (fallbackCost <= 0) return false;

            cost = fallbackCost;
            return true;
        }

        private static bool DoesBotNeedEquipmentType(PlayerObject player, ItemType itemType)
        {
            if (player == null) return false;

            switch (itemType)
            {
                case ItemType.Bracelet:
                case ItemType.Ring:
                    return CountBotOwnedEquipmentType(player, itemType) < 2;
                default:
                    if (!ItemTypeToSlot.TryGetValue(itemType, out EquipmentSlot slot))
                        return false;

                    return player.Equipment[(int)slot] == null
                           && !player.Inventory.Any(x => x?.Info?.ItemType == itemType);
            }
        }

        private static bool TryGetBestBotEquipmentPurchase(PlayerObject player, ItemType itemType, long maxBudget,
            out ItemInfo bestInfo, out long bestCost)
        {
            bestInfo = null;
            bestCost = 0;
            if (player == null || maxBudget <= 0) return false;

            long bestScore = long.MinValue;
            foreach (ItemInfo info in SEnvir.ItemInfoList.Binding)
            {
                if (info == null) continue;
                if (info.ItemType != itemType) continue;
                if (!TryGetBotDirectBuyCost(info, out long directCost) || directCost > maxBudget) continue;
                if (!CanBotUsePotionInfo(player, info)) continue;

                long score = CalculateWeightedItemScore(info, player.Class);
                if (score > bestScore
                    || (score == bestScore && directCost < bestCost)
                    || (score == bestScore && directCost == bestCost && info.RequiredAmount < (bestInfo?.RequiredAmount ?? int.MaxValue)))
                {
                    bestInfo = info;
                    bestCost = directCost;
                    bestScore = score;
                }
            }

            return bestInfo != null;
        }

        private static long GetBotNextEquipmentReserveGold(PlayerObject player)
        {
            if (player == null || player.Dead) return 0;

            foreach (ItemType itemType in BotEquipmentPurchasePriority)
            {
                if (!DoesBotNeedEquipmentType(player, itemType))
                    continue;

                if (TryGetBestBotEquipmentPurchase(player, itemType, long.MaxValue, out ItemInfo _, out long bestCost))
                    return Math.Max(0, bestCost);
            }

            return 0;
        }

        private static long GetBotPotionReserveCost(PlayerObject player, BotPotionKind kind, int currentCount, int minimumCount)
        {
            if (player == null || currentCount >= minimumCount) return 0;

            ItemInfo bestInfo = FindBestBotPotionInfo(player, kind, out long bestCost);
            if (bestInfo == null || bestCost <= 0) return 0;

            int missingCount = Math.Max(0, minimumCount - currentCount);
            return (long)missingCount * bestCost;
        }

        private static long GetBotPotionReserveGold(PlayerObject player)
        {
            if (player == null || player.Dead) return 0;

            CountBotPotionStock(player, out int healthCount, out int manaCount, out int dualCount);

            return GetBotPotionReserveCost(player, BotPotionKind.Health, healthCount, Config.BotMinHealthPotionCount)
                 + GetBotPotionReserveCost(player, BotPotionKind.Mana, manaCount, Config.BotMinManaPotionCount)
                 + GetBotPotionReserveCost(player, BotPotionKind.Dual, dualCount, BotMinDualPotionCount);
        }

        /// <summary>
        /// 检测 bot 当前缺的核心装备，并在保留最低药钱的前提下，从全局物品表里挑一件当前预算内属性最好的商店装。
        /// 这样不会因为药水补货把金币全花光，也不会为了买装备把保命药钱清空。
        ///
        /// 同时集成装备升级决策：定期检查商店装备，与当前装备对比，有显著提升则主动购买。
        /// 按职业加权：战士优先攻击/准确，法师优先魔法，道士优先道术，刺客优先敏捷/暴击。
        /// </summary>
        private static void ProcessBotBuyEquip(PlayerObject player)
        {
            if (player == null || player.Dead) return;

            // ── 1. 优先处理装备升级（如果有显著提升）──────────────────────────
            if (CheckBotShopEquipmentUpgrades(player,
                    out List<(ItemInfo newInfo, long cost, EquipmentSlot slot)> upgrades))
            {
                // 按优先级排序购买，每次只买一件（避免超支）
                var sortedUpgrades = upgrades
                    .OrderBy(u => GetUpgradePriorityWeight(u.slot))
                    .ThenBy(u => u.cost)
                    .ToList();

                foreach (var (newInfo, cost, _) in sortedUpgrades)
                {
                    // 再次确认预算（可能在排序过程中被其他逻辑消耗）
                    long potionReserve = GetBotPotionReserveGold(player);
                    long economyReserveTarget = GetBotEconomyReserveTarget(player);
                    long availableBudget = Math.Max(0, player.Gold - potionReserve - economyReserveTarget);

                    if (availableBudget < cost) continue;

                    try
                    {
                        ChangeBotGoldSilently(player, -cost);

                        UserItem newItem = SEnvir.CreateFreshItem(newInfo);
                        player.GainItem(newItem);

                        ProcessBotAutoEquip(player);

                        // 每次只购买一件升级装备，避免一次 Tick 消耗过多金币
                        break;
                    }
                    catch (Exception)
                    {
                        ChangeBotGoldSilently(player, cost);
                        continue;
                    }
                }
            }

            // ── 2. 处理缺装（装备槽位为空时购买基础装备）────────────────────
            long economyReserveTarget2 = GetBotEconomyReserveTarget(player);

            foreach (ItemType needType in BotEquipmentPurchasePriority)
            {
                if (!DoesBotNeedEquipmentType(player, needType))
                    continue;

                if (ShouldBotDeferEquipmentPurchase(player, needType))
                    continue;

                long potionReserve = GetBotPotionReserveGold(player);
                long savingsReserve = Math.Max(0, economyReserveTarget2);
                long availableBudget = Math.Max(0, player.Gold - potionReserve - savingsReserve);

                if (availableBudget <= 0)
                    break;

                if (!TryGetBestBotEquipmentPurchase(player, needType, availableBudget, out ItemInfo bestInfo, out long bestCost))
                    continue;

                try
                {
                    ChangeBotGoldSilently(player, -bestCost);

                    UserItem newItem = SEnvir.CreateFreshItem(bestInfo);
                    player.GainItem(newItem);
                }
                catch (Exception)
                {
                    ChangeBotGoldSilently(player, bestCost);
                    continue;
                }

                ProcessBotAutoEquip(player);
            }
        }

        /// <summary>
        /// 获取装备槽的优先级权重（数值越小优先级越高）。
        /// </summary>
        private static int GetUpgradePriorityWeight(EquipmentSlot slot)
        {
            switch (slot)
            {
                case EquipmentSlot.Weapon: return 1;
                case EquipmentSlot.Armour: return 2;
                case EquipmentSlot.Helmet: return 3;
                case EquipmentSlot.Necklace: return 4;
                case EquipmentSlot.Shoes: return 5;
                case EquipmentSlot.RingL:
                case EquipmentSlot.RingR: return 6;
                case EquipmentSlot.BraceletL:
                case EquipmentSlot.BraceletR: return 7;
                default: return 99;
            }
        }

        // ══════════════════════════════════════════════════════════════════════
        //  AI – 自动接受组队邀请 & 批量组队开关
        // ══════════════════════════════════════════════════════════════════════

        /// <summary>
        /// 假人自动接受挂起的组队邀请。
        /// 仅在 Config.BotAllowGroup == true 时生效。
        ///
        /// 规则：
        ///   - 邀请方是假人 且 假人处于真人邀请保护期 → 拒绝，等保护期结束后再接受假人邀请
        ///   - 邀请方是真人 且 假人已在某个假人队伍里 → 先离队，再进入1分钟保护期，然后接受邀请
        ///   - 其余情况：直接接受
        /// </summary>
        private static void ProcessBotGroupAccept(PlayerObject player)
        {
            if (!Config.BotAllowGroup) return;
            if (player.GroupInvitation == null) return;

            // 邀请者已离线或死亡，清除挂起邀请
            if (player.GroupInvitation.Node == null)
            {
                player.GroupInvitation = null;
                return;
            }

            uint pid = player.ObjectID;
            PlayerObject inviter = player.GroupInvitation;
            bool inviterIsBot = botPlayers.Contains(inviter);

            // ── 情况1：邀请方是假人，且假人处于真人邀请保护期 → 跳过，等保护期结束 ──
            if (inviterIsBot
                && _botHumanInviteCooldown.TryGetValue(pid, out DateTime protectUntil)
                && SEnvir.Now < protectUntil)
            {
                // 保护期内不接受假人邀请，但保留 GroupInvitation 让下一个 Tick 继续判断
                // 如果保护期结束前邀请超时，GroupInvitation 会因 Node==null 被清除
                return;
            }

            // ── 情况1b：强制按档切图后的保护期内，不再接受任何 bot 邀请，避免新队伍被旧邀请拉回去 ──
            if (inviterIsBot && IsBotForcedGroupLockActive(player))
            {
                player.GroupInvitation = null;
                return;
            }

            // ── 情况2：邀请方是假人，若当前是 bot-only 历史队伍，则允许脱离旧队重组 ──
            if (inviterIsBot && player.GroupMembers != null)
            {
                if (ReferenceEquals(player.GroupMembers, inviter?.GroupMembers))
                {
                    player.GroupInvitation = null;
                    return;
                }

                if (!CanBotLeaveCurrentGroupForBotInvite(player, inviter))
                {
                    player.GroupInvitation = null;
                    return;
                }

                try
                {
                    player.GroupLeave();
                }
                catch (Exception)
                {
                    player.GroupInvitation = null;
                    return;
                }
            }

            // ── 情况3：邀请方是真人（非假人），且假人当前已在任意队伍里 → 先离队，再立刻转入真人队伍 ──
            if (!inviterIsBot && player.GroupMembers != null)
            {
                try
                {
                    player.GroupLeave();
                }
                catch (Exception)
                {
                }

                // 进入保护期：1分钟内不接受假人邀请，优先稳住真人队伍
                _botHumanInviteCooldown[pid] = SEnvir.Now.AddSeconds(BotHumanInviteProtectSeconds);
            }

            // ── 情况4：正常接受邀请 ──
            // 若邀请方是真人，且假人之前在假人队伍里（情况3），则保持保护期
            // 若邀请方是真人，但假人本来就是单人，则不设置保护期，允许立即参与假人互组
            // 这样可以避免假人接受真人邀请后长时间无法参与自动组队
            // 只有当假人已经在真人队伍中时，才会在 ProcessBotGroupAccept 的 else 分支设置保护期

            try
            {
                // SEnvir.Log($"[ProcessBotGroupAccept] 玩家={player.Name}, 邀请方={inviter?.Name}, 是假人={inviterIsBot}");
                player.GroupJoin();

                // 记录社交记忆：组队关系
                if (inviter != null && inviter.Node != null)
                    BotSocialMemory.RecordGroupJoin(player, inviter);
            }
            catch (Exception)
            {
            }
            finally
            {
                player.GroupInvitation = null;
            }
        }

        /// <summary>
        /// 组队跟随模块：队员与队长距离过远或不在同图时，直接跟随传送靠近。
        /// 站位纠偏完成后继续允许后续拾取/协战，避免贴队后整 Tick 继续发呆。
        /// </summary>
        private static void ProcessBotGroupFollow(PlayerObject player)
        {
            if (!Config.BotAllowGroup) return;
            if (player?.GroupMembers == null || player.GroupMembers.Count <= 1) return;
            if (player.GroupMembers[0] == player) return;

            PlayerObject leader = player.GroupMembers[0];
            if (leader?.Node == null || leader.Dead || leader.CurrentMap == null) return;

            BotBehaviorProfile profile = GetBotBehaviorProfile(player);
            int followMaxDist = Math.Max(6, BotFollowLeaderMaxDist + (profile?.FollowSlack ?? 0));

            bool needFollow = leader.CurrentMap != player.CurrentMap;
            if (!needFollow)
            {
                int leaderDist = MaxChebyshevDistance(player.CurrentLocation, leader.CurrentLocation);
                needFollow = leaderDist > followMaxDist;
            }


            if (!needFollow) return;

            Point dest = leader.CurrentMap.GetRandomLocation(leader.CurrentLocation, 3, 20);
            if (dest == Point.Empty) dest = leader.CurrentLocation;

            if (!player.Teleport(leader.CurrentMap, dest))
                return;

            player.AddAllObjects();

            uint pid = player.ObjectID;
            _botTargets.Remove(pid);
            _botTargetSwitchTime.Remove(pid);
            _botRoamDir.Remove(pid);
            _botRoamTime.Remove(pid);
            _botLastSnapPos.Remove(pid);
            _botLastSnapTime.Remove(pid);
            _botDriftAnchorPos.Remove(pid);
            _botDriftAnchorTime.Remove(pid);
            _botLastAttackTime[pid] = SEnvir.Now;
        }

        /// <summary>
        /// 假人自动组队参与概率（百分比）。
        /// 只对当前空闲 bot 生效，未命中的 bot 本轮保持单刷。
        /// </summary>
        private const int BotAutoGroupParticipationChance = 90;

        /// <summary>
        /// 自动组队模板权重：不组队。
        /// </summary>
        private const int BotAutoGroupNoGroupWeight = 10;

        /// <summary>
        /// 自动组队模板权重：2 人组。
        /// </summary>
        private const int BotAutoGroupDuoWeight = 70;

        /// <summary>
        /// 自动组队模板权重：3 人组（1 战 1 法 1 道）。
        /// </summary>
        private const int BotAutoGroupTriadWeight = 50;

        /// <summary>
        /// 自动组队模板权重：6 人组（2 战 2 法 2 道）。
        /// </summary>
        private const int BotAutoGroupSixManWeight = 30;

        /// <summary>
        /// 自动组队模板权重：直接组满当前队伍上限。
        /// </summary>
        private const int BotAutoGroupFullWeight = 10;

        /// <summary>
        /// 低级假人(45级以下)自动组队模板权重：不组队。
        /// 保持较低概率，允许部分低级假人单刷。
        /// </summary>
        private const int BotAutoGroupLowLevelNoGroupWeight = 5;

        /// <summary>
        /// 低级假人(45级以下)自动组队模板权重：2 人组。
        /// 降低权重，因为 2 人组效率可能不够。
        /// </summary>
        private const int BotAutoGroupLowLevelDuoWeight = 30;

        /// <summary>
        /// 低级假人(45级以下)自动组队模板权重：3 人组。
        /// 提高权重，3 人组（1 战 1 法 1 道）更稳定，适合低级假人。
        /// </summary>
        private const int BotAutoGroupLowLevelTriadWeight = 50;

        /// <summary>
        /// 低级假人(45级以下)自动组队模板权重：6 人组（尽量少用，只有10%概率）。
        /// </summary>
        private const int BotAutoGroupLowLevelSixManWeight = 10;

        /// <summary>
        /// 60+ BOSS 图强制扩编的最短重试间隔（秒），避免每个 Tick 都重复拉人。
        /// </summary>
        private const int BotHighBossGroupPrepareRetrySeconds = 5;

        private static DateTime _botNextPeriodicGroupTime = DateTime.MinValue;

        private static bool ShouldRunPeriodicBotGrouping()
        {
            if (!Config.BotAllowGroup || !Config.BotAutoGroup || Config.BotPeriodicGroupSeconds <= 0)
            {
                _botNextPeriodicGroupTime = DateTime.MinValue;
                return false;
            }

            DateTime now = SEnvir.Now;
            if (now < _botNextPeriodicGroupTime)
                return false;

            _botNextPeriodicGroupTime = now.AddSeconds(Math.Max(1, Config.BotPeriodicGroupSeconds));
            return ShouldTriggerScaledBehavior(Config.BotGroupTendencyPercent,
                (uint)Math.Max(0, botPlayers.Count), now.Ticks / TimeSpan.TicksPerSecond);
        }

        /// <summary>
        /// 高阶 BOSS 图预热提前量：离正式切图阈值只差这么多分时，就先开始拉满编。
        /// </summary>
        private const int BotHighBossGroupPreheatScoreBuffer = 20;

        private enum BotAutoGroupPattern
        {
            None,
            Full,
            SixMan,
            Triad,
            Duo,
            Solo,
        }

        private static bool RollBotAutoGroupChance(int percent)
        {
            percent = Math.Max(0, Math.Min(100, percent));
            if (percent <= 0) return false;
            if (percent >= 100) return true;

            return SEnvir.Random.Next(100) < percent;
        }

        private static int GetConfiguredBotAutoGroupChance()
        {
            return ScaleLegacyChance(BotAutoGroupParticipationChance, Config.BotGroupTendencyPercent);
        }

        private static void ShuffleBotCandidates(List<PlayerObject> bots)
        {
            if (bots == null || bots.Count <= 1) return;

            for (int i = bots.Count - 1; i > 0; i--)
            {
                int swapIndex = SEnvir.Random.Next(i + 1);
                if (swapIndex == i) continue;

                PlayerObject temp = bots[i];
                bots[i] = bots[swapIndex];
                bots[swapIndex] = temp;
            }
        }

        private static bool TryTakeRandomBotMembers(List<PlayerObject> source, Func<PlayerObject, bool> predicate, int count, List<PlayerObject> result)
        {
            if (count <= 0) return true;
            if (source == null || result == null) return false;

            List<PlayerObject> matches = source.Where(predicate).ToList();
            if (matches.Count < count) return false;

            ShuffleBotCandidates(matches);

            for (int i = 0; i < count; i++)
            {
                PlayerObject member = matches[i];
                result.Add(member);
                source.Remove(member);
            }

            return true;
        }

        private static bool CanBuildBalancedBotGroup(List<PlayerObject> pool, int warriorCount, int wizardCount, int taoistCount)
        {
            if (pool == null) return false;

            return pool.Count(x => x.Class == MirClass.Warrior) >= warriorCount
                   && pool.Count(x => x.Class == MirClass.Wizard) >= wizardCount
                   && pool.Count(x => x.Class == MirClass.Taoist) >= taoistCount;
        }

        private static List<PlayerObject> TryBuildBalancedBotGroup(List<PlayerObject> pool, int warriorCount, int wizardCount, int taoistCount)
        {
            if (!CanBuildBalancedBotGroup(pool, warriorCount, wizardCount, taoistCount))
                return null;

            List<PlayerObject> remaining = new List<PlayerObject>(pool);
            List<PlayerObject> result = new List<PlayerObject>();

            if (!TryTakeRandomBotMembers(remaining, x => x.Class == MirClass.Warrior, warriorCount, result)) return null;
            if (!TryTakeRandomBotMembers(remaining, x => x.Class == MirClass.Wizard, wizardCount, result)) return null;
            if (!TryTakeRandomBotMembers(remaining, x => x.Class == MirClass.Taoist, taoistCount, result)) return null;

            ShuffleBotCandidates(result);
            return result;
        }

        private static List<PlayerObject> TryBuildBotDuoGroup(List<PlayerObject> pool)
        {
            if (pool == null || pool.Count < 2) return null;

            List<PlayerObject> shuffled = new List<PlayerObject>(pool);
            ShuffleBotCandidates(shuffled);

            foreach (PlayerObject leader in shuffled)
            {
                PlayerObject partner = shuffled.FirstOrDefault(x => x != leader && x.Class != leader.Class);
                if (partner != null)
                    return new List<PlayerObject> { leader, partner };
            }

            return shuffled.Take(2).ToList();
        }

        private static bool IsBotOnlyGroup(PlayerObject player)
        {
            if (player?.GroupMembers == null || player.GroupMembers.Count == 0) return false;

            foreach (PlayerObject member in player.GroupMembers)
            {
                if (member == null || !botPlayers.Contains(member))
                    return false;
            }

            return true;
        }

        private static bool CanBotLeaveCurrentGroupForBotInvite(PlayerObject player, PlayerObject inviter)
        {
            if (player?.Node == null || player.Dead) return false;
            if (inviter?.Node == null || inviter.Dead || !botPlayers.Contains(inviter)) return false;
            if (player == inviter) return false;
            if (ShouldBotEmergencyGoldFarm(player)) return false;
            if (_botHumanInviteCooldown.TryGetValue(player.ObjectID, out DateTime protectUntil) && SEnvir.Now < protectUntil)
                return false;

            if (inviter.GroupMembers != null)
            {
                if (inviter.GroupMembers[0] != inviter) return false;
                if (inviter.GroupMembers.Count >= Globals.GroupLimit) return false;
            }

            if (player.GroupMembers == null || player.GroupMembers.Count == 0)
                return player.GroupInvitation == null;

            if (ReferenceEquals(player.GroupMembers, inviter.GroupMembers)) return false;
            if (!IsBotOnlyGroup(player)) return false;
            if (player.GroupMembers.Count >= Globals.GroupLimit) return false;

            return player.GroupInvitation == null || player.GroupInvitation == inviter;
        }

        private static bool IsBotHighLevelBossMap(Map map)
        {
            return map != null && MapHasBossAboveLevel(map, BotHighLevelBossThreshold);
        }

        private static Map GetBotUpcomingHighBossGroupTarget(PlayerObject player)
        {
            if (player == null) return null;

            if (_botUpcomingHighBossGroupTargets.TryGetValue(player.ObjectID, out Map targetMap)
                && IsBotHighLevelBossMap(targetMap))
                return targetMap;

            _botUpcomingHighBossGroupTargets.Remove(player.ObjectID);
            return null;
        }

        private static void SetBotUpcomingHighBossGroupTarget(PlayerObject player, Map targetMap)
        {
            if (player == null) return;

            if (IsBotHighLevelBossMap(targetMap))
                _botUpcomingHighBossGroupTargets[player.ObjectID] = targetMap;
            else
                _botUpcomingHighBossGroupTargets.Remove(player.ObjectID);
        }

        private static void ClearBotUpcomingHighBossGroupTarget(PlayerObject player)
        {
            if (player == null) return;

            _botUpcomingHighBossGroupTargets.Remove(player.ObjectID);
        }

        private static bool TryGetBotHighBossGroupTarget(PlayerObject player, out Map targetMap)
        {
            targetMap = null;
            if (player?.Node == null || player.Dead) return false;

            if (IsBotHighLevelBossMap(player.CurrentMap))
            {
                ClearBotUpcomingHighBossGroupTarget(player);
                targetMap = player.CurrentMap;
                return true;
            }

            targetMap = GetBotUpcomingHighBossGroupTarget(player);
            return targetMap != null;
        }

        private static bool ShouldBotForceFullAutoGroup(PlayerObject player)
        {
            return TryGetBotHighBossGroupTarget(player, out _);
        }

        /// <summary>
        /// 判断假人是否需要使用低级组队优先级(45级以下)。
        /// 条件：
        /// 1. 等级 < 45
        /// 2. 不处于攻城期间
        /// 3. 不被真人组队中
        /// </summary>
        private static bool ShouldUseLowLevelGroupPriority(PlayerObject player)
        {
            if (player == null || player.Node == null || player.Dead) return false;

            // 检查等级
            if (player.Level >= 45) return false;

            // 检查是否处于攻城期间(通过判断是否在攻城战的行会中且正在攻城)
            GuildInfo guild = player?.Character?.Account?.GuildMember?.Guild;
            if (guild != null)
            {
                ConquestWar war = SEnvir.ConquestWars.FirstOrDefault(w => w != null
                    && w.IsWaring
                    && w.Participants != null
                    && w.Participants.Contains(guild));
                if (war != null) return false;
            }

            // 检查是否被真人组队中(队伍里有非假人玩家)
            if (player.GroupMembers != null && player.GroupMembers.Count > 0)
            {
                PlayerObject leader = player.GroupMembers[0];
                if (leader != null && !leader.BotPlayer)
                    return false;
            }

            return true;
        }

        private static bool TryPrepareBotFullGroupForUpcomingHighBossMap(PlayerObject player, Map targetMap)
        {
            if (!IsBotHighLevelBossMap(targetMap)) return true;
            if (!Config.BotAllowGroup) return false;
            if (player?.Node == null || player.Dead) return false;

            int targetSize = GetDynamicFullGroupTarget();
            PlayerObject leader = player;
            if (leader.GroupMembers != null && leader.GroupMembers.Count > 0)
                leader = leader.GroupMembers[0];

            if (leader?.Node == null || leader.Dead) return false;
            if (leader != player) return false;
            if (leader.GroupMembers != null && leader.GroupMembers.Count >= targetSize) return true;
            if (leader.GroupInvitation != null) return false;

            HashSet<PlayerObject> existingMembers = new HashSet<PlayerObject>();
            if (leader.GroupMembers != null)
            {
                foreach (PlayerObject member in leader.GroupMembers)
                {
                    if (member != null)
                        existingMembers.Add(member);
                }
            }
            existingMembers.Add(leader);

            int slotsNeeded = targetSize - existingMembers.Count;
            if (slotsNeeded <= 0) return true;

            List<PlayerObject> candidates = botPlayers.Where(p =>
                    p?.Node != null
                    && !p.Dead
                    && p != leader
                    && !existingMembers.Contains(p)
                    && CanBotLeaveCurrentGroupForBotInvite(p, leader))
                .OrderByDescending(p => GetBotUpcomingHighBossGroupTarget(p) == targetMap)
                .ThenByDescending(p => p.CurrentMap == leader.CurrentMap)
                .ThenByDescending(p => p.CurrentMap == targetMap)
                .ThenBy(p => p.GroupMembers != null ? 1 : 0)
                .ThenBy(p => p.CurrentMap == leader.CurrentMap
                    ? Functions.Distance(p.CurrentLocation, leader.CurrentLocation)
                    : int.MaxValue)
                .ToList();

            foreach (PlayerObject target in candidates)
            {
                if (slotsNeeded <= 0) break;

                try
                {
                    // SEnvir.Log($"[高阶BOSS图满队] 队长={leader.Name}, 邀请={target.Name}, 剩余空位={slotsNeeded}, 目标满编={targetSize}");
                    leader.GroupInvite(target.Name);
                    slotsNeeded--;
                }
                catch (Exception ex)
                {
                    SEnvir.Log($"假人高阶BOSS图提前满队邀请异常 [{leader.Name}→{target.Name}]: {ex.Message}");
                }
            }

            return leader.GroupMembers != null && leader.GroupMembers.Count >= targetSize;
        }

        private static void ProcessBotHighBossGroupMaintenance(PlayerObject player)
        {
            if (!Config.BotAllowGroup) return;
            if (player?.Node == null || player.Dead) return;

            // 记录当前地图（调试用）
            if (player?.CurrentMap != null && IsBotHighLevelBossMap(player.CurrentMap))
            {
                // 已移除调试日志
            }

            int targetSize = GetDynamicFullGroupTarget();
            PlayerObject leader = player;
            if (leader.GroupMembers != null && leader.GroupMembers.Count > 0)
            {
                leader = leader.GroupMembers[0];
                if (leader != player) return;
            }

            if (leader?.Node == null || leader.Dead) return;
            if (!ShouldRunBotMaintenance(_botHighBossMaintenanceTime, leader.ObjectID, BotHighBossMaintenanceIntervalSeconds))
                return;
            if (!TryGetBotHighBossGroupTarget(leader, out Map targetMap))
            {
                _botHighBossGroupPrepareTime.Remove(leader.ObjectID);
                return;
            }

            if (leader.GroupMembers != null && leader.GroupMembers.Count >= targetSize)
            {
                _botHighBossGroupPrepareTime.Remove(leader.ObjectID);

                // 队伍满员后，清除该BOSS图的满队进度锁
                if (targetMap != null && _botHighBossGroupFullInProgress.ContainsKey(targetMap))
                    _botHighBossGroupFullInProgress.Remove(targetMap);

                if (targetMap != leader.CurrentMap)
                    _botMapEvalTime[leader.ObjectID] = SEnvir.Now;
                return;
            }

            // 检查是否有其他队长正在补满同一个BOSS图
            if (targetMap != null && _botHighBossGroupFullInProgress.TryGetValue(targetMap, out DateTime inProgressSince))
            {
                // 如果已经有队长在补满，且未超时，则跳过本次
                if (SEnvir.Now < inProgressSince.AddSeconds(60)) // 60秒内不允许重复补满
                {
                    return;
                }
                // 超时后清除旧锁，允许重新补满
                _botHighBossGroupFullInProgress.Remove(targetMap);
            }

            if (_botHighBossGroupPrepareTime.TryGetValue(leader.ObjectID, out DateTime nextTryTime)
                && SEnvir.Now < nextTryTime)
                return;

            // 标记该BOSS图正在补满
            if (targetMap != null)
                _botHighBossGroupFullInProgress[targetMap] = SEnvir.Now;

            bool fullReady = TryPrepareBotFullGroupForUpcomingHighBossMap(leader, targetMap);
            _botHighBossGroupPrepareTime[leader.ObjectID] = SEnvir.Now.AddSeconds(BotHighBossGroupPrepareRetrySeconds);

            // 如果补满失败（未达到目标满编人数），清除进度锁，允许其他队长重试
            if (!fullReady && targetMap != null)
                _botHighBossGroupFullInProgress.Remove(targetMap);

            if (fullReady && targetMap != leader.CurrentMap)
                _botMapEvalTime[leader.ObjectID] = SEnvir.Now;
        }

        /// <summary>
        /// 根据在线假人总数动态获取满编目标人数。
        /// 在线 < 20 人时，满编降至 4 人；
        /// 20-40 人时，满编降至 6 人；
        /// 40-60 人时，满编降至 10 人；
        /// 60 人以上时，满编使用系统默认（15 人）。
        /// </summary>
        private static int GetDynamicFullGroupTarget()
        {
            int onlineBotCount = botPlayers.Count;

            if (onlineBotCount < 20) return 4;
            if (onlineBotCount < 40) return 6;
            if (onlineBotCount < 60) return 10;
            return Globals.GroupLimit;  // 默认 15 人
        }

        private static List<PlayerObject> TryBuildBotFullGroup(List<PlayerObject> pool, PlayerObject seed = null)
        {
            int targetSize = GetDynamicFullGroupTarget();
            if (pool == null || pool.Count < targetSize) return null;

            List<PlayerObject> shuffled = new List<PlayerObject>(pool);
            ShuffleBotCandidates(shuffled);

            List<PlayerObject> result = new List<PlayerObject>();
            if (seed != null && shuffled.Remove(seed))
                result.Add(seed);

            if (seed?.CurrentMap != null)
            {
                List<PlayerObject> sameMap = shuffled.Where(x => x?.CurrentMap == seed.CurrentMap).ToList();
                ShuffleBotCandidates(sameMap);

                foreach (PlayerObject member in sameMap)
                {
                    if (result.Count >= targetSize) break;

                    result.Add(member);
                    shuffled.Remove(member);
                }
            }

            foreach (PlayerObject member in shuffled)
            {
                if (result.Count >= targetSize) break;
                result.Add(member);
            }

            return result.Count >= targetSize ? result.Take(targetSize).ToList() : null;
        }

        private static BotAutoGroupPattern SelectBotAutoGroupPattern(List<PlayerObject> pool)
        {
            // 判断是否使用低级组队优先级(优先检查池子里的假人)
            // 改为：如果池子中 50% 以上是 45 级以下，则使用低级权重
            bool useLowLevelPriority = pool != null && pool.Count > 0;
            if (useLowLevelPriority)
            {
                int lowLevelCount = pool.Count(p => p != null && ShouldUseLowLevelGroupPriority(p));
                useLowLevelPriority = lowLevelCount * 2 > pool.Count; // 50% 以上是低级假人
            }

            List<KeyValuePair<BotAutoGroupPattern, int>> options = new List<KeyValuePair<BotAutoGroupPattern, int>>();

            // 根据是否使用低级优先级选择不同的权重
            int fullWeight = useLowLevelPriority ? 10 : BotAutoGroupFullWeight;
            int sixManWeight = useLowLevelPriority ? BotAutoGroupLowLevelSixManWeight : BotAutoGroupSixManWeight;
            int triadWeight = useLowLevelPriority ? BotAutoGroupLowLevelTriadWeight : BotAutoGroupTriadWeight;
            int duoWeight = useLowLevelPriority ? BotAutoGroupLowLevelDuoWeight : BotAutoGroupDuoWeight;
            int soloWeight = useLowLevelPriority ? BotAutoGroupLowLevelNoGroupWeight : BotAutoGroupNoGroupWeight;

            if (TryBuildBotFullGroup(pool) != null)
                options.Add(new KeyValuePair<BotAutoGroupPattern, int>(BotAutoGroupPattern.Full, fullWeight));

            if (CanBuildBalancedBotGroup(pool, 2, 2, 2))
                options.Add(new KeyValuePair<BotAutoGroupPattern, int>(BotAutoGroupPattern.SixMan, sixManWeight));

            if (CanBuildBalancedBotGroup(pool, 1, 1, 1))
                options.Add(new KeyValuePair<BotAutoGroupPattern, int>(BotAutoGroupPattern.Triad, triadWeight));

            if (pool != null && pool.Count >= 2)
                options.Add(new KeyValuePair<BotAutoGroupPattern, int>(BotAutoGroupPattern.Duo, duoWeight));

            if (pool != null && pool.Count >= 1)
                options.Add(new KeyValuePair<BotAutoGroupPattern, int>(BotAutoGroupPattern.Solo, soloWeight));

            if (options.Count == 0) return BotAutoGroupPattern.None;

            int totalWeight = options.Sum(x => x.Value);
            int roll = SEnvir.Random.Next(totalWeight);

            foreach (KeyValuePair<BotAutoGroupPattern, int> option in options)
            {
                if (roll < option.Value)
                    return option.Key;

                roll -= option.Value;
            }

            return options[options.Count - 1].Key;
        }

        private static List<PlayerObject> BuildBotAutoGroupMembers(List<PlayerObject> pool)
        {
            BotAutoGroupPattern pattern = SelectBotAutoGroupPattern(pool);
            // SEnvir.Log($"假人组队模式选择: 池子={pool?.Count ?? 0}人, 模式={pattern}");
            switch (pattern)
            {
                case BotAutoGroupPattern.Full:
                    return TryBuildBotFullGroup(pool);
                case BotAutoGroupPattern.SixMan:
                    return TryBuildBalancedBotGroup(pool, 2, 2, 2);
                case BotAutoGroupPattern.Triad:
                    return TryBuildBalancedBotGroup(pool, 1, 1, 1);
                case BotAutoGroupPattern.Duo:
                    return TryBuildBotDuoGroup(pool);
                case BotAutoGroupPattern.Solo:
                    if (pool == null || pool.Count == 0) return null;

                    List<PlayerObject> solo = new List<PlayerObject>(pool);
                    ShuffleBotCandidates(solo);
                    return new List<PlayerObject> { solo[0] };
                default:
                    return null;
            }
        }

        /// <summary>
        /// 批量同步所有在线假人的 AllowGroup 状态，并根据开关决定是否自动邀请假人互相组队。
        /// 由 BotConfigView 的勾选框即时触发，也会在新假人上线后补跑一次，避免后登录成员落单。
        /// </summary>
        public static void ApplyGroupSwitchToAllBots(bool allow)
        {
            SEnvir.BotActionQueue.Enqueue(() =>
            {
                try
                {
                    foreach (PlayerObject player in botPlayers)
                    {
                        if (player?.Node == null || player.Dead) continue;
                        // 同步账号级别开关（GroupSwitch 会在关闭时自动触发 GroupLeave）
                        player.GroupSwitch(allow);
                    }

                    if (!allow || !Config.BotAutoGroup)
                    {
                        _botGroupRebuildPending = false;
                        _botNextGroupRebuildTime = DateTime.MinValue;
                        return;
                    }

                    List<PlayerObject> freeBots = botPlayers.Where(p =>
                        p?.Node != null
                        && !p.Dead
                        && !IsBotInWarmup(p)
                        && p.GroupMembers == null
                        && p.GroupInvitation == null
                        && !IsBotForcedGroupLockActive(p)
                        && !ShouldBotEmergencyGoldFarm(p)
                        && (!_botHumanInviteCooldown.TryGetValue(p.ObjectID, out DateTime pt) || SEnvir.Now >= pt)
                    ).ToList();

                    if (freeBots.Count < 2)
                    {
                        SEnvir.Log($"[ApplyGroupSwitchToAllBots] freeBots={freeBots.Count}, 不足2人，跳过自动组队");
                        return;
                    }

                    List<PlayerObject> availableBots = new List<PlayerObject>(freeBots);
                    List<PlayerObject> priorityFullBots = availableBots.Where(ShouldBotForceFullAutoGroup).ToList();

                    // 低级假人(45级以下)有最高组队优先级,除了攻城期间和被真人组队
                    List<PlayerObject> lowLevelPriorityBots = availableBots.Where(ShouldUseLowLevelGroupPriority).ToList();
                    List<PlayerObject> candidateBots = availableBots.Where(p =>
                            priorityFullBots.Contains(p)
                            || lowLevelPriorityBots.Contains(p)  // 低级假人优先
                            || RollBotAutoGroupChance(GetConfiguredBotAutoGroupChance()))
                        .ToList();

                    SEnvir.Log($"[ApplyGroupSwitchToAllBots] freeBots={freeBots.Count}, priorityFull={priorityFullBots.Count}, lowLevel={lowLevelPriorityBots.Count}, candidate={candidateBots.Count}");

                    // ============ 建议 1：分离高优先级池 ============
                    // 先为所有高优先级假人尝试满编，避免普通模板占满高优先级假人
                    if (priorityFullBots.Count > 0)
                    {
                        List<PlayerObject> processedForcedFull = new List<PlayerObject>();

                        foreach (PlayerObject forcedFullLeader in priorityFullBots)
                        {
                            if (!candidateBots.Contains(forcedFullLeader)) continue;
                            if (forcedFullLeader?.Node == null || forcedFullLeader.Dead) continue;

                            List<PlayerObject> team = TryBuildBotFullGroup(availableBots, forcedFullLeader);
                            if (team == null || team.Count == 0)
                            {
                                // 无法满编，从候选池中移除，但不从可用池中移除（可能被其他队长拉）
                                candidateBots.Remove(forcedFullLeader);
                                continue;
                            }

                            // 从候选池和可用池中移除已组队成员
                            foreach (PlayerObject member in team)
                            {
                                candidateBots.Remove(member);
                                availableBots.Remove(member);
                                processedForcedFull.Add(member);
                            }

                            if (team.Count < 2) continue;

                            // 发送组队邀请
                            PlayerObject leader = team[0];
                            for (int i = 1; i < team.Count; i++)
                            {
                                PlayerObject target = team[i];
                                if (target?.Node == null || target.Dead) continue;
                                if (target.GroupMembers != null || target.GroupInvitation != null) continue;
                                if (_botHumanInviteCooldown.TryGetValue(target.ObjectID, out DateTime pt) && SEnvir.Now < pt) continue;

                                try
                                {
                                    // SEnvir.Log($"[高优先级满编] 队长={leader.Name}, 邀请={target.Name}, 队伍人数={team.Count}, 目标BOSS图={GetBotUpcomingHighBossGroupTarget(leader)?.Info.FileName ?? leader.CurrentMap?.Info.FileName}");
                                    leader.GroupInvite(target.Name);
                                }
                                catch (Exception ex)
                                {
                                    SEnvir.Log($"高优先级满编邀请异常 [{leader.Name}→{target.Name}]: {ex.Message}");
                                }
                            }
                        }

                        SEnvir.Log($"[ApplyGroupSwitchToAllBots] 高优先级满编完成: priorityFull={priorityFullBots.Count}, processed={processedForcedFull.Count}, 剩余可用={availableBots.Count}");

                        // 如果没有剩余可用假人，直接返回
                        if (availableBots.Count < 2)
                        {
                            // SEnvir.Log($"[ApplyGroupSwitchToAllBots] 高优先级满编后剩余可用假人不足2人，跳过普通组队");
                            return;
                        }
                    }

                    // 再处理普通假人组队
                    List<PlayerObject> normalBots = availableBots.Where(p =>
                            lowLevelPriorityBots.Contains(p)
                            || RollBotAutoGroupChance(GetConfiguredBotAutoGroupChance()))
                        .ToList();

                    SEnvir.Log($"[ApplyGroupSwitchToAllBots] 普通组队池: normalBots={normalBots.Count}, 剩余可用={availableBots.Count}");

                    if (normalBots.Count < 2) return;

                    ShuffleBotCandidates(normalBots);

                    while (normalBots.Count > 0)
                    {
                        List<PlayerObject> team = BuildBotAutoGroupMembers(normalBots);
                        if (team == null || team.Count == 0) break;

                        foreach (PlayerObject member in team)
                        {
                            normalBots.Remove(member);
                            availableBots.Remove(member);
                        }

                        if (team.Count < 2) continue;

                        PlayerObject leader = team[0];
                        if (leader?.Node == null || leader.Dead || leader.GroupMembers != null || leader.GroupInvitation != null)
                            continue;

                        for (int i = 1; i < team.Count; i++)
                        {
                            PlayerObject target = team[i];
                            if (target?.Node == null || target.Dead) continue;
                            if (target.GroupMembers != null || target.GroupInvitation != null) continue;
                            if (_botHumanInviteCooldown.TryGetValue(target.ObjectID, out DateTime pt) && SEnvir.Now < pt) continue;

                            try
                            {
                                // SEnvir.Log($"[普通组队] 队长={leader.Name}, 邀请={target.Name}, 队伍人数={team.Count}");
                                leader.GroupInvite(target.Name);
                            }
                            catch (Exception ex)
                            {
                                SEnvir.Log($"普通组队邀请异常 [{leader.Name}→{target.Name}]: {ex.Message}");
                            }
                        }
                    }
                }
                catch (Exception ex)
                {
                    SEnvir.Log($"ApplyGroupSwitchToAllBots 异常: {ex.Message}");
                }
            });
        }

        // ══════════════════════════════════════════════════════════════════════
        //  AI – 道士专用：自动购买符咒/毒药 & 换装备槽 & 召唤宝宝
        // ══════════════════════════════════════════════════════════════════════

        // 购买符/毒冷却：ObjectID → 下次允许检查购买的时间（避免每 Tick 刷购买）
        private static readonly Dictionary<uint, DateTime> _botTaoistBuyTime
            = new Dictionary<uint, DateTime>();

        // 召唤冷却：ObjectID → 下次允许尝试召唤的时间
        private static readonly Dictionary<uint, DateTime> _botTaoistSummonTime
            = new Dictionary<uint, DateTime>();

        /// <summary>
        /// 道士装备槽中符/毒数量低于此阈值时触发自动补货。
        /// </summary>
        private const int BotTaoistSupplyMinCount = 100;

        /// <summary>
        /// 道士自动补货批量（每次购买的数量）。
        /// </summary>
        private const int BotTaoistSupplyBuyCount = 500;

        /// <summary>
        /// 低等级道士在完全断粮时赠送的启动补给数量，避免没金币时永远放不出符/毒。
        /// </summary>
        private const int BotTaoistStarterSupplyCount = 50;

        /// <summary>
        /// 道士召唤宝宝冷却时间（秒）：避免每 Tick 重复调用 Attack(Summon)。
        /// </summary>
        private const int BotTaoistSummonCooldown = 8;

        /// <summary>
        /// 道士毒药使用计数：记录施毒次数。
        /// </summary>
        private static readonly Dictionary<uint, int> _botTaoistPoisonUseCount
            = new Dictionary<uint, int>();

        /// <summary>
        /// 道士上次施毒记录：玩家ID → (目标ID, 施毒时间, 施毒类型)
        /// 用于确认施毒 500ms 延迟后，怪物才真正中毒
        /// </summary>
        internal static readonly Dictionary<uint, (uint targetId, DateTime time, int poisonShape)> _botTaoistLastPoisonCast
            = new Dictionary<uint, (uint, DateTime, int)>();

        private static bool IsBotUsableTaoistAmuletInfo(ItemInfo info)
        {
            return info != null
                   && info.ItemType == ItemType.Amulet
                   && info.Shape >= 1
                   && info.Shape <= 8;
        }

        private static bool IsBotUsableTaoistAmulet(UserItem item)
        {
            return item?.Info != null
                   && IsBotUsableTaoistAmuletInfo(item.Info)
                   && item.Count > 0;
        }

        private static bool TryGetBotTaoistAmuletRequirement(MagicType magicType, out int requiredCount, out bool requiresSoulAmulet)
        {
            requiredCount = 0;
            requiresSoulAmulet = false;

            switch (magicType)
            {
                case MagicType.ExplosiveTalisman:
                case MagicType.ImprovedExplosiveTalisman:
                case MagicType.EvilSlayer:
                case MagicType.GreaterEvilSlayer:
                case MagicType.GreaterHolyStrike:
                case MagicType.MagicResistance:
                case MagicType.ElementalSuperiority:
                case MagicType.SummonSkeleton:
                case MagicType.Neutralize:
                    requiredCount = 1;
                    return true;
                case MagicType.Resilience:
                case MagicType.BloodLust:
                case MagicType.LifeSteal:
                case MagicType.TrapOctagon:
                case MagicType.SummonJinSkeleton:
                case MagicType.Invisibility:
                case MagicType.MassInvisibility:
                case MagicType.MassTransparency:
                case MagicType.Purification:
                    requiredCount = 2;
                    return true;
                case MagicType.SummonShinsu:
                case MagicType.StrengthOfFaith:
                    requiredCount = 5;
                    return true;
                case MagicType.Transparency:
                case MagicType.CelestialLight:
                    requiredCount = 10;
                    return true;
                case MagicType.DemonExplosion:
                    requiredCount = 20;
                    return true;
                case MagicType.SummonDemonicCreature:
                    requiredCount = 25;
                    return true;
                case MagicType.Resurrection:
                    requiredCount = 1;
                    requiresSoulAmulet = true;
                    return true;
                default:
                    return false;
            }
        }

        private static int GetBotTaoistConsumableCount(PlayerObject player, ItemType type, int minShape, int maxShape)
        {
            if (player == null) return 0;

            int count = 0;
            EquipmentSlot slot = type == ItemType.Poison ? EquipmentSlot.Poison : EquipmentSlot.Amulet;
            UserItem equipped = player.Equipment[(int)slot];
            if (equipped?.Info?.ItemType == type
                && equipped.Info.Shape >= minShape
                && equipped.Info.Shape <= maxShape)
                count += (int)equipped.Count;

            foreach (UserItem item in player.Inventory)
            {
                if (item?.Info?.ItemType != type
                    || item.Info.Shape < minShape
                    || item.Info.Shape > maxShape)
                    continue;

                count += (int)item.Count;
            }

            return count;
        }

        /// <summary>
        /// 道士自动购买符咒和毒药。
        /// 触发条件：
        ///   1. 职业 == Taoist
        ///   2. 已学习对应技能（施毒/施毒大法 → 买毒；灵魂火符/灭魂火符 → 买符）
        ///   3. 装备槽（Poison / Amulet）中对应道具数量 &lt; BotTaoistSupplyMinCount
        ///   4. 每60秒最多检查一次（冷却）
        ///
        /// 毒药：购买两种毒药（黄色药粉 Shape=1 和 灰色药粉 Shape=0），各购买 BotTaoistSupplyBuyCount 数量
        /// </summary>
        private static void ProcessBotTaoistSupply(PlayerObject player)
        {
            if (player == null || player.Dead) return;
            if (player.Class != MirClass.Taoist) return;

            uint pid = player.ObjectID;
            // 冷却：60 秒检查一次
            if (_botTaoistBuyTime.TryGetValue(pid, out DateTime nextBuy) && SEnvir.Now < nextBuy) return;
            _botTaoistBuyTime[pid] = SEnvir.Now.AddSeconds(60);

            // ── 买毒（施毒术 / 施毒大法 已学时才买）──────────────────────────
            // 两种毒药都购买：黄色药粉（Shape=1 红毒）和灰色药粉（Shape=0 绿毒）
            bool needsPoison = (player.Magics.ContainsKey(MagicType.PoisonDust)
                                || player.Magics.ContainsKey(MagicType.GreaterPoisonDust));
            if (needsPoison)
            {
                if (GetBotTaoistConsumableCount(player, ItemType.Poison, 1, 1) < BotTaoistSupplyMinCount)
                    BotBuyPoisonByShape(player, 1, BotTaoistSupplyBuyCount);

                if (GetBotTaoistConsumableCount(player, ItemType.Poison, 0, 0) < BotTaoistSupplyMinCount)
                    BotBuyPoisonByShape(player, 0, BotTaoistSupplyBuyCount);
            }

            bool needsNormalAmulet = false;
            bool needsSoulAmulet = false;
            foreach (MagicType magicType in player.Magics.Keys)
            {
                if (!TryGetBotTaoistAmuletRequirement(
                        magicType,
                        out int requiredCount,
                        out bool requiresSoulAmulet)
                    || requiredCount <= 0)
                    continue;

                if (requiresSoulAmulet)
                    needsSoulAmulet = true;
                else
                    needsNormalAmulet = true;
            }

            if (needsNormalAmulet
                && GetBotTaoistConsumableCount(player, ItemType.Amulet, 1, 8) < BotTaoistSupplyMinCount)
                BotBuyConsumable(player, ItemType.Amulet, 1, 8, BotTaoistSupplyBuyCount, true);

            if (needsSoulAmulet
                && GetBotTaoistConsumableCount(player, ItemType.Amulet, 0, 0) < BotTaoistSupplyMinCount)
                BotBuyConsumable(player, ItemType.Amulet, 0, 0, BotTaoistSupplyBuyCount, false);
        }

        /// <summary>
        /// 当低等级道士既没金币也没有库存时，免费补一小批启动用的符/毒，避免永远卡在无法升级的死循环里。
        /// </summary>
        private static bool TryGrantTaoistStarterConsumable(PlayerObject player, ItemType type, ItemInfo itemInfo)
        {
            if (player == null || player.Dead || itemInfo == null) return false;
            if (player.Class != MirClass.Taoist || player.Level > 7) return false;
            if (!player.Inventory.Any(x => x == null)) return false;

            int totalCount = 0;
            switch (type)
            {
                case ItemType.Poison:
                    totalCount += (int)(player.Equipment[(int)EquipmentSlot.Poison]?.Count ?? 0);
                    break;
                case ItemType.Amulet:
                    UserItem equippedAmulet = player.Equipment[(int)EquipmentSlot.Amulet];
                    totalCount += IsBotUsableTaoistAmulet(equippedAmulet) ? (int)equippedAmulet.Count : 0;
                    break;
                default:
                    return false;
            }

            foreach (var inv in player.Inventory)
            {
                if (inv?.Info == null || inv.Info.ItemType != type) continue;
                if (type == ItemType.Amulet && !IsBotUsableTaoistAmulet(inv)) continue;

                totalCount += (int)inv.Count;
            }

            if (totalCount > 0) return false;

            try
            {
                UserItem newItem = SEnvir.CreateFreshItem(itemInfo);
                newItem.Count = (uint)BotTaoistStarterSupplyCount;
                player.GainItem(newItem);
                ProcessBotTaoistEquipSupply(player);
                return true;
            }
            catch (Exception)
            {
                return false;
            }
        }

        /// <summary>
        /// 从真实商店售卖列表中查找指定类型（Poison / Amulet）的最便宜可购物品，
        /// 扣金币后 CreateFreshItem 并设置 Count，放入背包。
        /// </summary>
        private static void BotBuyConsumable(PlayerObject player, ItemType type, int minShape, int maxShape, int count, bool allowStarterSupply)
        {
            ItemInfo bestInfo = null;
            long bestPrice = long.MaxValue;

            foreach (ItemInfo info in SEnvir.ItemInfoList.Binding)
            {
                if (info == null) continue;
                if (info.ItemType != type) continue;
                if (info.Shape < minShape || info.Shape > maxShape) continue;
                if (!TryGetBotDirectBuyCost(info, out long directCost)) continue;
                if (directCost < bestPrice)
                {
                    bestPrice = directCost;
                    bestInfo = info;
                }
            }

            if (bestInfo == null || bestPrice <= 0) return;

            // 计算总花费（单价 * 数量，但符/毒是堆叠道具，Price 通常指单价）
            long totalCost = bestPrice * count;
            if (player.Gold < totalCost)
            {
                // 金币不足时，能买多少买多少；若低等级道士彻底断粮，则先送一小批启动补给
                count = (int)(player.Gold / bestPrice);
                if (count <= 0)
                {
                    if (allowStarterSupply)
                        TryGrantTaoistStarterConsumable(player, type, bestInfo);
                    return;
                }
                totalCost = bestPrice * count;
            }

            while (count > 0
                && !player.CanGainItems(true, new ItemCheck(bestInfo, count, UserItemFlags.None, TimeSpan.Zero)))
            {
                count--;
            }

            if (count <= 0) return;

            totalCost = bestPrice * count;

            try
            {
                ChangeBotGoldSilently(player, -totalCost);

                UserItem newItem = SEnvir.CreateFreshItem(bestInfo);
                newItem.Count = (uint)count;
                player.GainItem(newItem);
            }
            catch (Exception)
            {
                ChangeBotGoldSilently(player, totalCost);   // 回滚
                // SEnvir.Log($"假人 [{player.Name}] 道士补货异常（已回滚金币）: {ex.Message}");
            }
        }

        /// <summary>
        /// 购买指定 Shape 的毒药（Shape=0 灰色药粉/绿毒，Shape=1 黄色药粉/红毒）。
        /// 扣金币后 CreateFreshItem 并设置 Count，放入背包。
        /// </summary>
        private static void BotBuyPoisonByShape(PlayerObject player, int shape, int count)
        {
            ItemInfo bestInfo = null;
            long bestPrice = long.MaxValue;

            foreach (ItemInfo info in SEnvir.ItemInfoList.Binding)
            {
                if (info == null) continue;
                if (info.ItemType != ItemType.Poison) continue;
                if (info.Shape != shape) continue;

                if (!TryGetBotDirectBuyCost(info, out long directCost))
                    continue;
                if (directCost <= 0)
                    continue;

                if (directCost < bestPrice)
                {
                    bestPrice = directCost;
                    bestInfo = info;
                }
            }

            if (bestInfo == null || bestPrice <= 0)
                return;


            // 计算总花费（单价 * 数量，但毒是堆叠道具，Price 通常指单价）
            long totalCost = bestPrice * count;
            if (player.Gold < totalCost)
            {
                // 金币不足时，能买多少买多少；若低等级道士彻底断粮，则先送一小批启动补给
                count = (int)(player.Gold / bestPrice);
                if (count <= 0)
                {
                    TryGrantTaoistStarterConsumable(player, ItemType.Poison, bestInfo);
                    return;
                }
                totalCost = bestPrice * count;
            }

            while (count > 0
                && !player.CanGainItems(true, new ItemCheck(bestInfo, count, UserItemFlags.None, TimeSpan.Zero)))
            {
                count--;
            }

            if (count <= 0) return;

            totalCost = bestPrice * count;

            try
            {
                ChangeBotGoldSilently(player, -totalCost);

                UserItem newItem = SEnvir.CreateFreshItem(bestInfo);
                newItem.Count = (uint)count;
                player.GainItem(newItem);
            }
            catch (Exception)
            {
                ChangeBotGoldSilently(player, totalCost);   // 回滚
                // SEnvir.Log($"假人 [{player.Name}] 道士补毒异常（已回滚金币）: {ex.Message}");
            }
        }

        // ══════════════════════════════════════════════════════════════════════
        //  AI – 回城休息期补给：补充药水 & 道士补符/毒
        // ══════════════════════════════════════════════════════════════════════

        /// <summary>
        /// 回城休息期间主动补充消耗品：
        ///   1. 所有职业：强制把 HP/MP/双效药补到目标库存。
        ///   2. 道士额外：复用 ProcessBotTaoistSupply 逻辑，补充符/毒至足量。
        ///   3. 回城待机期间正常调用独立药水监控喝药，无需在这里重复触发用药。
        /// </summary>
        private static void ProcessBotReplenishSupplies(PlayerObject player)
        {
            if (player == null || player.Dead) return;

            long goldBefore = player.Gold;
            uint pid = player.ObjectID;

            ProcessBotPotionSupply(player, true);

            // ── 2. 道士：复用 ProcessBotTaoistSupply 补符/毒 ─────────────────
            // ProcessBotTaoistSupply 内部有60秒冷却，无需额外冷却控制
            if (player.Class == MirClass.Taoist)
            {
                // 强制重置冷却，让回城期间立即检查一次（正常60秒才检查）
                if (_botTaoistBuyTime.TryGetValue(pid, out DateTime taoistBuyTime)
                    && SEnvir.Now < taoistBuyTime)
                {
                    // 若距上次检查已超过10秒，允许在回城期提前触发
                    if ((taoistBuyTime - SEnvir.Now).TotalSeconds > 50)
                        _botTaoistBuyTime[pid] = SEnvir.Now; // 重置冷却，让下一句立即执行
                }
                ProcessBotTaoistSupply(player);
                ProcessBotTaoistEquipSupply(player);
            }

            FlushBotGoldState(player, goldBefore);
        }

        /// <summary>
        /// 定期检查并补充 HP/MP/双效药库存；forceFullRestock=true 时直接补到目标数量。
        /// </summary>
        private static void ProcessBotPotionSupply(PlayerObject player, bool forceFullRestock)
        {
            if (player == null || player.Dead) return;
            if (!Config.BotAutoPotionSupply) return;

            uint pid = player.ObjectID;
            if (!forceFullRestock
                && _botRestockTime.TryGetValue(pid, out DateTime nextRestock)
                && SEnvir.Now < nextRestock)
                return;

            _botRestockTime[pid] = SEnvir.Now.AddSeconds(BotPotionRestockCooldownSeconds);

            int healthCount;
            int manaCount;
            int dualCount;
            CountBotPotionStock(player, out healthCount, out manaCount, out dualCount);

            TryRestockBotPotionKind(player, BotPotionKind.Health, healthCount,
                Config.BotMinHealthPotionCount, BotTargetHealthPotionCount, forceFullRestock);
            TryRestockBotPotionKind(player, BotPotionKind.Mana, manaCount,
                Config.BotMinManaPotionCount, BotTargetManaPotionCount, forceFullRestock);
            TryRestockBotPotionKind(player, BotPotionKind.Dual, dualCount,
                BotMinDualPotionCount, BotTargetDualPotionCount, forceFullRestock);
        }

        private static void CountBotPotionStock(PlayerObject player, out int healthCount, out int manaCount, out int dualCount)
        {
            healthCount = 0;
            manaCount = 0;
            dualCount = 0;

            if (player == null || player.Inventory == null) return;

            for (int i = 0; i < player.Inventory.Length; i++)
            {
                UserItem item = player.Inventory[i];
                if (item == null || item.Info == null) continue;

                int hpRestore;
                int mpRestore;
                switch (GetBotPotionKind(item, out hpRestore, out mpRestore))
                {
                    case BotPotionKind.Health:
                        healthCount += (int)item.Count;
                        break;
                    case BotPotionKind.Mana:
                        manaCount += (int)item.Count;
                        break;
                    case BotPotionKind.Dual:
                        dualCount += (int)item.Count;
                        break;
                }
            }
        }

        private static void TryRestockBotPotionKind(PlayerObject player, BotPotionKind kind, int currentCount,
            int minCount, int targetCount, bool forceFullRestock)
        {
            if (player == null || kind == BotPotionKind.None) return;
            if (!forceFullRestock && currentCount >= minCount) return;

            int buyCount = targetCount - currentCount;
            if (buyCount <= 0) return;

            bool criticalShortage = currentCount <= Math.Max(5, minCount / 4);
            long reservedGold = criticalShortage ? 0 : GetBotNextEquipmentReserveGold(player);
            BotBuyPotion(player, kind, buyCount, reservedGold);
        }

        /// <summary>
        /// 为假人购买指定类型的药水：按恢复量与价格综合择优，分别补充 HP/MP/双效药。
        /// 非紧急缺药时会预留下一件商店装备的钱，避免 bot 一有金币就全砸进药水里。
        /// </summary>
        private static void BotBuyPotion(PlayerObject player, BotPotionKind kind, int count, long reservedGold = 0)
        {
            if (player == null || count <= 0 || kind == BotPotionKind.None) return;

            ItemInfo bestInfo = FindBestBotPotionInfo(player, kind, out long bestCost);
            if (bestInfo == null || bestCost <= 0) return;

            long spendableGold = Math.Max(0, player.Gold - Math.Max(0, reservedGold));
            int maxAffordableCount = (int)(spendableGold / bestCost);
            if (maxAffordableCount <= 0) return;

            int remaining = Math.Min(count, maxAffordableCount);
            int boughtCount = 0;
            long totalCost = 0;
            int maxChunk = Math.Max(1, bestInfo.StackSize);

            while (remaining > 0)
            {
                int chunk = Math.Min(remaining, maxChunk);

                while (chunk > 0
                    && !player.CanGainItems(true, new ItemCheck(bestInfo, chunk, UserItemFlags.None, TimeSpan.Zero)))
                {
                    chunk--;
                }


                if (chunk <= 0)
                    break;

                long chunkCost = bestCost * chunk;
                if (player.Gold - chunkCost < Math.Max(0, reservedGold))
                    break;

                try
                {
                    UserItem newItem = SEnvir.CreateFreshItem(bestInfo);
                    newItem.Count = (uint)chunk;

                    ChangeBotGoldSilently(player, -chunkCost);
                    player.GainItem(newItem);

                    boughtCount += chunk;
                    totalCost += chunkCost;
                    remaining -= chunk;
                }
                catch (Exception)
                {
                    ChangeBotGoldSilently(player, chunkCost);
                    // SEnvir.Log($"假人 [{player.Name}] 购买 {GetBotPotionKindName(kind)} 药水分批入包异常（已回滚本批金币）: {ex.Message}");
                    break;
                }
            }

        }

        private static ItemInfo FindBestBotPotionInfo(PlayerObject player, BotPotionKind kind, out long bestCost)
        {
            ItemInfo bestInfo = null;
            bestCost = 0;
            long bestUnitPriceScore = long.MaxValue;
            long bestSinglePrice = long.MaxValue;
            int bestRestore = int.MinValue;

            foreach (ItemInfo info in SEnvir.ItemInfoList.Binding)
            {
                if (!TryGetBotPotionPurchaseScore(player, info, kind, out int restoreAmount, out long unitPriceScore, out long directCost))
                    continue;

                if (unitPriceScore < bestUnitPriceScore
                    || (unitPriceScore == bestUnitPriceScore && directCost < bestSinglePrice)
                    || (unitPriceScore == bestUnitPriceScore && directCost == bestSinglePrice && restoreAmount > bestRestore))
                {
                    bestInfo = info;
                    bestUnitPriceScore = unitPriceScore;
                    bestSinglePrice = directCost;
                    bestCost = directCost;
                    bestRestore = restoreAmount;
                }
            }

            return bestInfo;
        }

        private static bool CanBotUsePotionInfo(PlayerObject player, ItemInfo info)
        {
            if (player == null || info == null) return false;

            switch (player.Gender)
            {
                case MirGender.Male:
                    if ((info.RequiredGender & RequiredGender.Male) != RequiredGender.Male)
                        return false;
                    break;
                case MirGender.Female:
                    if ((info.RequiredGender & RequiredGender.Female) != RequiredGender.Female)
                        return false;
                    break;
            }

            switch (player.Class)
            {
                case MirClass.Warrior:
                    if ((info.RequiredClass & RequiredClass.Warrior) != RequiredClass.Warrior)
                        return false;
                    break;
                case MirClass.Wizard:
                    if ((info.RequiredClass & RequiredClass.Wizard) != RequiredClass.Wizard)
                        return false;
                    break;
                case MirClass.Taoist:
                    if ((info.RequiredClass & RequiredClass.Taoist) != RequiredClass.Taoist)
                        return false;
                    break;
                case MirClass.Assassin:
                    if ((info.RequiredClass & RequiredClass.Assassin) != RequiredClass.Assassin)
                        return false;
                    break;
            }

            switch (info.RequiredType)
            {
                case RequiredType.Level:
                    if (player.Level < info.RequiredAmount && player.Stats[Stat.Rebirth] == 0) return false;
                    break;
                case RequiredType.MaxLevel:
                    if (player.Level > info.RequiredAmount || player.Stats[Stat.Rebirth] > 0) return false;
                    break;
                case RequiredType.CompanionLevel:
                    if (player.Companion == null || player.Companion.UserCompanion.Level < info.RequiredAmount) return false;
                    break;
                case RequiredType.MaxCompanionLevel:
                    if (player.Companion == null || player.Companion.UserCompanion.Level > info.RequiredAmount) return false;
                    break;
                case RequiredType.AC:
                    if (player.Stats[Stat.MaxAC] < info.RequiredAmount) return false;
                    break;
                case RequiredType.MR:
                    if (player.Stats[Stat.MaxMR] < info.RequiredAmount) return false;
                    break;
                case RequiredType.DC:
                    if (player.Stats[Stat.MaxDC] < info.RequiredAmount) return false;
                    break;
                case RequiredType.MC:
                    if (player.Stats[Stat.MaxMC] < info.RequiredAmount) return false;
                    break;
                case RequiredType.SC:
                    if (player.Stats[Stat.MaxSC] < info.RequiredAmount) return false;
                    break;
                case RequiredType.Health:
                    if (player.Stats[Stat.Health] < info.RequiredAmount) return false;
                    break;
                case RequiredType.Mana:
                    if (player.Stats[Stat.Mana] < info.RequiredAmount) return false;
                    break;
                case RequiredType.Accuracy:
                    if (player.Stats[Stat.Accuracy] < info.RequiredAmount) return false;
                    break;
                case RequiredType.Agility:
                    if (player.Stats[Stat.Agility] < info.RequiredAmount) return false;
                    break;
                case RequiredType.RebirthLevel:
                    if (player.Stats[Stat.Rebirth] < info.RequiredAmount) return false;
                    break;
                case RequiredType.MaxRebirthLevel:
                    if (player.Stats[Stat.Rebirth] > info.RequiredAmount) return false;
                    break;
            }

            return true;
        }

        private static bool TryGetBotPotionPurchaseScore(PlayerObject player, ItemInfo info, BotPotionKind kind,
            out int restoreAmount, out long unitPriceScore, out long directCost)
        {
            restoreAmount = 0;
            unitPriceScore = long.MaxValue;
            directCost = 0;

            if (player == null || info == null || info.Price <= 0) return false;
            if (!TryGetBotDirectBuyCost(info, out directCost)) return false;
            if (!CanBotUsePotionInfo(player, info)) return false;

            switch (info.Effect)
            {
                case ItemEffect.Gold:
                case ItemEffect.GameGold:
                case ItemEffect.Prestige:
                case ItemEffect.Contribute:
                case ItemEffect.Experience:
                    return false;
            }

            int hpRestore;
            int mpRestore;
            if (GetBotPotionKind(info, out hpRestore, out mpRestore) != kind)
                return false;

            switch (kind)
            {
                case BotPotionKind.Health:
                    restoreAmount = hpRestore;
                    break;
                case BotPotionKind.Mana:
                    restoreAmount = mpRestore;
                    break;
                case BotPotionKind.Dual:
                    restoreAmount = hpRestore + mpRestore;
                    break;
            }

            if (restoreAmount <= 0) return false;

            unitPriceScore = directCost * 1000 / restoreAmount;
            return true;
        }

        private static string GetBotPotionKindName(BotPotionKind kind)
        {
            switch (kind)
            {
                case BotPotionKind.Health:
                    return "HP";
                case BotPotionKind.Mana:
                    return "MP";
                case BotPotionKind.Dual:
                    return "双效";
                default:
                    return "未知";
            }
        }


        /// <summary>
        /// 将背包中的符咒 / 毒药装备到对应槽位（装备槽为空或比背包物品数量少时触发）。
        /// 规则：
        ///   - Poison 槽空 且 背包有 ItemType.Poison → 装备到 Poison 槽
        ///   - Amulet 槽空 且 背包有 ItemType.Amulet → 装备到 Amulet 槽
        ///   - 若装备槽已有同类物品但背包中有 Shape 匹配的存量，先不替换（已有即可用）
        /// </summary>
        private static bool TryEquipBotTaoistPoisonForShape(PlayerObject player, int targetShape)
        {
            if (player == null || player.Dead || player.Class != MirClass.Taoist)
                return false;
            if (targetShape != 0 && targetShape != 1)
                return false;

            UserItem equipped = player.Equipment[(int)EquipmentSlot.Poison];
            if (equipped?.Info?.ItemType == ItemType.Poison
                && equipped.Count > 0
                && equipped.Info.Shape == targetShape)
                return true;

            for (int i = 0; i < player.Inventory.Length; i++)
            {
                UserItem candidate = player.Inventory[i];
                if (candidate?.Info?.ItemType != ItemType.Poison
                    || candidate.Count <= 0
                    || candidate.Info.Shape != targetShape)
                    continue;
                if (equipped != null && FindEmptyInventorySlot(player) < 0)
                    return false;

                try
                {
                    player.PutOnEquip(candidate, (int)EquipmentSlot.Poison);
                    UserItem current = player.Equipment[(int)EquipmentSlot.Poison];
                    return current?.Info?.ItemType == ItemType.Poison
                           && current.Count > 0
                           && current.Info.Shape == targetShape;
                }
                catch (Exception)
                {
                    return false;
                }
            }

            return false;
        }

        private static bool TryEquipBotTaoistAmuletForMagic(PlayerObject player, MagicType magicType)
        {
            if (player == null || player.Dead || player.Class != MirClass.Taoist)
                return false;
            if (!TryGetBotTaoistAmuletRequirement(
                    magicType,
                    out int requiredCount,
                    out bool requiresSoulAmulet))
                return false;

            int minShape = requiresSoulAmulet ? 0 : 1;
            int maxShape = requiresSoulAmulet ? 0 : 8;
            UserItem equipped = player.Equipment[(int)EquipmentSlot.Amulet];
            if (equipped?.Info?.ItemType == ItemType.Amulet
                && equipped.Count >= requiredCount
                && equipped.Info.Shape >= minShape
                && equipped.Info.Shape <= maxShape)
                return true;

            for (int i = 0; i < player.Inventory.Length; i++)
            {
                UserItem candidate = player.Inventory[i];
                if (candidate?.Info?.ItemType != ItemType.Amulet
                    || candidate.Count < requiredCount
                    || candidate.Info.Shape < minShape
                    || candidate.Info.Shape > maxShape)
                    continue;
                if (equipped != null && FindEmptyInventorySlot(player) < 0)
                    return false;

                try
                {
                    player.PutOnEquip(candidate, (int)EquipmentSlot.Amulet);
                    UserItem current = player.Equipment[(int)EquipmentSlot.Amulet];
                    return current?.Info?.ItemType == ItemType.Amulet
                           && current.Count >= requiredCount
                           && current.Info.Shape >= minShape
                           && current.Info.Shape <= maxShape;
                }
                catch (Exception)
                {
                    return false;
                }
            }

            return false;
        }

        private static void ProcessBotTaoistEquipSupply(PlayerObject player)
        {
            if (player == null || player.Dead) return;
            if (player.Class != MirClass.Taoist) return;

            UserItem equippedPoison = player.Equipment[(int)EquipmentSlot.Poison];
            if (equippedPoison == null || equippedPoison.Count <= 0)
            {
                for (int i = 0; i < player.Inventory.Length; i++)
                {
                    UserItem inv = player.Inventory[i];
                    if (inv?.Info?.ItemType != ItemType.Poison || inv.Count <= 0) continue;

                    try { player.PutOnEquip(inv, (int)EquipmentSlot.Poison); }
                    catch (Exception) { }
                    break;
                }
            }

            UserItem equippedAmulet = player.Equipment[(int)EquipmentSlot.Amulet];
            if (equippedAmulet == null || equippedAmulet.Count <= 0)
            {
                for (int i = 0; i < player.Inventory.Length; i++)
                {
                    UserItem inv = player.Inventory[i];
                    if (inv?.Info?.ItemType != ItemType.Amulet
                        || inv.Count <= 0
                        || inv.Info.Shape < 0
                        || inv.Info.Shape > 8)
                        continue;

                    try { player.PutOnEquip(inv, (int)EquipmentSlot.Amulet); }
                    catch (Exception) { }
                    break;
                }
            }
        }

        /// <summary>
        /// 道士自动召唤宝宝，并在宝宝死亡后自动重召。
        /// 优先级：超强召唤骷髅（SummonJinSkeleton）> 召唤骷髅（SummonSkeleton）；
        ///         召唤神兽（SummonShinsu）独立判断。
        /// 条件：
        ///   1. 职业 == Taoist
        ///   2. 已学对应召唤技能，且技能不在冷却
        ///   3. 装备槽 Amulet 中有足够数量的符咒
        ///   4. Pets 列表中无存活的对应宠物（新召唤 / 宝宝已死时触发）
        ///   5. 冷却 BotTaoistSummonCooldown 秒防止重复召唤
        /// </summary>
        private static void ProcessBotTaoistSummon(PlayerObject player)
        {
            if (player == null || player.Dead) return;
            if (player.Class != MirClass.Taoist) return;

            uint pid = player.ObjectID;
            if (_botTaoistSummonTime.TryGetValue(pid, out DateTime nextSummon) && SEnvir.Now < nextSummon) return;

            bool summoned = false;

            // ── 召唤骷髅 / 超强召唤骷髅 ──────────────────────────────────────
            // 有超强技能时优先用超强；否则用普通召唤骷髅
            bool hasJin = player.Magics.TryGetValue(MagicType.SummonJinSkeleton, out UserMagic jinMagic);
            bool hasSkeleton = player.Magics.TryGetValue(MagicType.SummonSkeleton, out UserMagic skelMagic);

            if (hasJin || hasSkeleton)
            {
                // 检查是否已有存活骷髅类宠物
                bool hasLivingSkeleton = player.Pets.Any(p =>
                    p != null && !p.Dead && p.Node != null
                    && (p.MonsterInfo?.Flag == MonsterFlag.Skeleton
                        || p.MonsterInfo?.Flag == MonsterFlag.JinSkeleton));

                if (!hasLivingSkeleton)
                {
                    // 优先超强召唤骷髅（两个技能都有时才用超强）
                    MagicType summonType = (hasJin && jinMagic.Cooldown <= SEnvir.Now)
                        ? MagicType.SummonJinSkeleton
                        : (hasSkeleton && skelMagic.Cooldown <= SEnvir.Now)
                            ? MagicType.SummonSkeleton
                            : MagicType.None;

                    UserMagic summonMagic = summonType == MagicType.SummonJinSkeleton ? jinMagic : skelMagic;
                    if (summonType != MagicType.None && summonMagic != null)
                    {
                        if (TryCastBotMagic(player, player.Direction, summonType, player, player.CurrentLocation))
                        {
                            _botTaoistSummonTime[pid] = SEnvir.Now.AddSeconds(BotTaoistSummonCooldown);
                            summoned = true;
                        }
                    }
                }
            }

            // ── 召唤神兽 ─────────────────────────────────────────────────────
            if (!summoned && player.Magics.TryGetValue(MagicType.SummonShinsu, out UserMagic shinsuMagic))
            {
                bool hasLivingShinsu = player.Pets.Any(p =>
                    p != null && !p.Dead && p.Node != null
                    && p.MonsterInfo?.Flag == MonsterFlag.Shinsu);

                if (!hasLivingShinsu && shinsuMagic.Cooldown <= SEnvir.Now)
                {
                    if (TryCastBotMagic(player, player.Direction, MagicType.SummonShinsu, player, player.CurrentLocation))
                        _botTaoistSummonTime[pid] = SEnvir.Now.AddSeconds(BotTaoistSummonCooldown);
                }
            }
        }

        // 道士防御BUFF冷却：ObjectID → 下次允许尝试施放防御BUFF的时间
        private static readonly Dictionary<uint, DateTime> _botTaoistBuffTime
            = new Dictionary<uint, DateTime>();

        // 法师防御BUFF冷却：ObjectID → 下次允许尝试施放防御技能的时间
        private static readonly Dictionary<uint, DateTime> _botWizardBuffTime
            = new Dictionary<uint, DateTime>();

        // 刺客防御BUFF冷却：ObjectID → 下次允许尝试施放防御技能的时间
        private static readonly Dictionary<uint, DateTime> _botAssassinBuffTime
            = new Dictionary<uint, DateTime>();

        /// <summary>
        /// 道士防御BUFF冷却时间（秒）：避免每 Tick 重复施放。
        /// </summary>
        private const int BotTaoistBuffCooldown = 5;

        /// <summary>
        /// 法师防御技能冷却时间（秒）：避免每 Tick 重复施放。
        /// </summary>
        private const int BotWizardBuffCooldown = 5;

        /// <summary>
        /// 刺客防御技能冷却时间（秒）：避免每 Tick 重复施放。
        /// </summary>
        private const int BotAssassinBuffCooldown = 5;

        /// <summary>
        /// 法师自动施放攻击增益技能：凝血离魂。
        /// 触发条件：
        ///   1. 职业 == Wizard
        ///   2. 已学习对应技能
        ///   3. 对应攻击 BUFF 当前不存在
        ///   4. 每 BotWizardBuffCooldown 秒最多尝试一次
        /// </summary>
        private static void ProcessBotWizardAttackBuff(PlayerObject player)
        {
            if (player == null || player.Dead) return;
            if (player.Class != MirClass.Wizard) return;

            uint pid = player.ObjectID;
            if (_botWizardBuffTime.TryGetValue(pid, out DateTime nextBuff) && SEnvir.Now < nextBuff) return;

            // ── 凝血离魂（增伤Buff，与怪物无关）────────────────────────
            if (player.Magics.TryGetValue(MagicType.Renounce, out UserMagic renounceMagic)
                && renounceMagic.Info != null
                && player.Level >= renounceMagic.Info.NeedLevel1
                && renounceMagic.Cooldown <= SEnvir.Now
                && !player.Buffs.Any(x => x.Type == BuffType.Renounce))
            {
                if (renounceMagic.Cost > player.CurrentMP)
                {
                    ProcessBotPotionMonitor(player);
                }
                else if (TryCastBotMagic(player, player.Direction, MagicType.Renounce, player, player.CurrentLocation))
                {
                    _botWizardBuffTime[pid] = SEnvir.Now.AddSeconds(BotWizardBuffCooldown);
                    return;
                }
            }
        }

        /// <summary>
        /// 法师自动施放防御增益技能：护身法盾、魔法盾。
        /// 触发条件：
        ///   1. 职业 == Wizard
        ///   2. 已学习对应技能
        ///   3. 对应防御 BUFF 当前不存在
        ///   4. 每 BotWizardBuffCooldown 秒最多尝试一次
        /// 优先级：护身法盾 > 魔法盾（两者不共存，护身法盾会移除魔法盾）。
        /// </summary>
        private static void ProcessBotWizardDefenceBuff(PlayerObject player)
        {
            if (player == null || player.Dead) return;
            if (player.Class != MirClass.Wizard) return;

            uint pid = player.ObjectID;
            if (_botWizardBuffTime.TryGetValue(pid, out DateTime nextBuff) && SEnvir.Now < nextBuff) return;

            // ── 护身法盾（优先）──────────────────────────────────────────────
            if (player.Magics.TryGetValue(MagicType.SuperiorMagicShield, out UserMagic superiorShieldMagic)
                && superiorShieldMagic.Info != null
                && player.Level >= superiorShieldMagic.Info.NeedLevel1
                && superiorShieldMagic.Cooldown <= SEnvir.Now
                && !player.Buffs.Any(x => x.Type == BuffType.SuperiorMagicShield))
            {
                if (superiorShieldMagic.Cost > player.CurrentMP)
                {
                    ProcessBotPotionMonitor(player);
                }
                else if (TryCastBotMagic(player, player.Direction, MagicType.SuperiorMagicShield, player, player.CurrentLocation))
                {
                    _botWizardBuffTime[pid] = SEnvir.Now.AddSeconds(BotWizardBuffCooldown);
                    return;
                }
            }

            // ── 魔法盾（次选，护身法盾不存在时才尝试）────────────────────────
            if (player.Magics.TryGetValue(MagicType.MagicShield, out UserMagic magicShield)
                && magicShield.Info != null
                && player.Level >= magicShield.Info.NeedLevel1
                && magicShield.Cooldown <= SEnvir.Now
                && !player.Buffs.Any(x => x.Type == BuffType.MagicShield)
                && !player.Buffs.Any(x => x.Type == BuffType.SuperiorMagicShield))
            {
                if (magicShield.Cost > player.CurrentMP)
                {
                    ProcessBotPotionMonitor(player);
                }
                else if (TryCastBotMagic(player, player.Direction, MagicType.MagicShield, player, player.CurrentLocation))
                {
                    _botWizardBuffTime[pid] = SEnvir.Now.AddSeconds(BotWizardBuffCooldown);
                }
            }
        }

        /// <summary>
        /// 刺客自动施放防御增益技能，统一使用 BotSkillSelector 的权威顺序。
        /// 触发条件：
        ///   1. 职业 == Assassin
        ///   2. 已学习对应技能
        ///   3. 对应防御 BUFF 当前不存在
        ///   4. 每 BotAssassinBuffCooldown 秒最多尝试一次
        /// </summary>
        private static void ProcessBotAssassinDefenceBuff(PlayerObject player)
        {
            if (player == null || player.Dead) return;
            if (player.Class != MirClass.Assassin) return;

            uint pid = player.ObjectID;
            if (_botAssassinBuffTime.TryGetValue(pid, out DateTime nextBuff) && SEnvir.Now < nextBuff) return;

            MagicType buffMagic = BotSkillSelector.GetAssassinBuffMagic(player);
            if (buffMagic == MagicType.None) return;

            if (TryCastBotMagic(player, player.Direction, buffMagic, player, player.CurrentLocation))
                _botAssassinBuffTime[pid] = SEnvir.Now.AddSeconds(BotAssassinBuffCooldown);
        }

        /// <summary>
        /// 道士自动施放防御增益技能：神圣战甲术、强魔震法、阴阳盾。
        /// 触发条件：
        ///   1. 职业 == Taoist
        ///   2. 已学习对应技能
        ///   3. 对应防御 BUFF 当前不存在
        ///   4. 每 BotTaoistBuffCooldown 秒最多尝试一次
        /// 优先级：神圣战甲术 > 强魔震法 > 阴阳盾
        /// </summary>
        /// <summary>
        /// 道士自动施放防御增益技能：幽灵盾、神圣战甲术、强魔震法、猛虎强势、阴阳法环、养生术。
        /// 触发条件：
        ///   1. 职业 == Taoist
        ///   2. 已学习对应技能
        ///   3. 对应防御 BUFF 当前不存在
        ///   4. 每 BotTaoistBuffCooldown 秒最多尝试一次
        /// 优先级：给自己加 > 给队友加（按 HP 从低到高）
        /// </summary>
        private static void ProcessBotTaoistDefenceBuff(PlayerObject player)
        {
            if (player == null || player.Dead) return;
            if (player.Class != MirClass.Taoist) return;

            uint pid = player.ObjectID;
            if (_botTaoistBuffTime.TryGetValue(pid, out DateTime nextBuff) && SEnvir.Now < nextBuff) return;

            // 收集需要加防御的目标（自己 + 队友）
            List<PlayerObject> targets = new List<PlayerObject> { player };
            if (player.GroupMembers != null && player.GroupMembers.Count > 1)
            {
                // 添加队友（不包括自己，因为已经在列表里了）
                foreach (PlayerObject member in player.GroupMembers)
                {
                    if (member != null && !member.Dead && member.Node != null && member != player)
                    {
                        targets.Add(member);
                    }
                }
            }

            // ── 幽灵盾（增加物理防御）────────────────────────────────────
            ProcessTaoistDefenseSkill(player, targets, MagicType.MagicResistance, BuffType.MagicResistance);
            if (_botTaoistBuffTime.ContainsKey(pid) && _botTaoistBuffTime[pid] > SEnvir.Now) return;

            // ── 神圣战甲术（群体增防，优先）────────────────────────────────
            ProcessTaoistDefenseSkill(player, targets, MagicType.Resilience, BuffType.Resilience);
            if (_botTaoistBuffTime.ContainsKey(pid) && _botTaoistBuffTime[pid] > SEnvir.Now) return;

            // ── 强魔震法（增加魔法防御）──────────────────────────────────
            ProcessTaoistDefenseSkill(player, targets, MagicType.ElementalSuperiority, BuffType.ElementalSuperiority);
            if (_botTaoistBuffTime.ContainsKey(pid) && _botTaoistBuffTime[pid] > SEnvir.Now) return;

            // ── 猛虎强势（增加攻击力）──────────────────────────────────────
            ProcessTaoistDefenseSkill(player, targets, MagicType.BloodLust, BuffType.BloodLust);
            if (_botTaoistBuffTime.ContainsKey(pid) && _botTaoistBuffTime[pid] > SEnvir.Now) return;

            // ── 阴阳法环（反射伤害）──────────────────────────────────────
            ProcessTaoistDefenseSkill(player, targets, MagicType.CelestialLight, BuffType.CelestialLight);
            if (_botTaoistBuffTime.ContainsKey(pid) && _botTaoistBuffTime[pid] > SEnvir.Now) return;

            // ── 养生术（持续回血）──────────────────────────────────────────
            ProcessTaoistDefenseSkill(player, targets, MagicType.EmpoweredHealing, BuffType.Heal);
        }

        /// <summary>
        /// 帮助方法：为道士施放防御技能
        /// </summary>
        private static void ProcessTaoistDefenseSkill(PlayerObject player, List<PlayerObject> targets, MagicType magicType, BuffType buffType)
        {
            uint pid = player.ObjectID;

            // 优先给自己加
            if (player.Magics.TryGetValue(magicType, out UserMagic magic)
                && magic.Info != null
                && player.Level >= magic.Info.NeedLevel1
                && magic.Cooldown <= SEnvir.Now
                && !player.Buffs.Any(x => x.Type == buffType))
            {
                if (magic.Cost > player.CurrentMP)
                {
                    ProcessBotPotionMonitor(player);
                }
                else if (TryCastBotMagic(player, player.Direction, magicType, player, player.CurrentLocation))
                {
                    _botTaoistBuffTime[pid] = SEnvir.Now.AddSeconds(BotTaoistBuffCooldown);
                    return;
                }
            }

            // 给队友加（按 HP 从低到高）
            if (targets.Count > 1)
            {
                // 按排序：HP 百分比从低到高
                var sortedTargets = targets
                    .Where(t => t != player && !t.Dead && t.Node != null)
                    .Where(t => !t.Buffs.Any(x => x.Type == buffType)) // 没有这个 Buff
                    .OrderBy(t => (double)t.CurrentHP / t.Stats[Stat.Health])
                    .ToList();

                foreach (PlayerObject target in sortedTargets)
                {
                    // 检查距离
                    int dist = MaxChebyshevDistance(player.CurrentLocation, target.CurrentLocation);
                    if (dist > 10) // 10 格范围内
                        continue;

                    if (player.Magics.TryGetValue(magicType, out UserMagic magic2)
                        && magic2.Info != null
                        && player.Level >= magic2.Info.NeedLevel1
                        && magic2.Cooldown <= SEnvir.Now)
                    {
                        if (magic2.Cost > player.CurrentMP)
                        {
                            ProcessBotPotionMonitor(player);
                        }
                        else if (TryCastBotMagic(player, player.Direction, magicType, target, target.CurrentLocation))
                        {
                            _botTaoistBuffTime[pid] = SEnvir.Now.AddSeconds(BotTaoistBuffCooldown);
                            return;
                        }
                    }
                }
            }
        }

        /// <summary>
        /// 道士自动施放隐身和治愈技能：群体隐身、隐身、群体治愈、单体治愈。
        /// 触发条件：
        ///   1. 职业 == Taoist
        ///   2. 已学习对应技能
        ///   3. 根据实际情况判断是否需要使用
        ///   4. 每 BotTaoistBuffCooldown 秒最多尝试一次
        /// 优先级：隐身技能（生命威胁时） > 治愈技能（HP不满时）
        /// </summary>
        private static void ProcessBotTaoistSupportBuff(PlayerObject player)
        {
            if (player == null || player.Dead) return;
            if (player.Class != MirClass.Taoist) return;

            uint pid = player.ObjectID;
            if (_botTaoistBuffTime.TryGetValue(pid, out DateTime nextBuff) && SEnvir.Now < nextBuff) return;

            bool hasGroup = player.GroupMembers != null && player.GroupMembers.Count > 1;

            // ── 优先处理生命威胁（使用隐身）──────────────────────────────
            if (HasLifeThreat(player))
            {
                bool usedInvisibility = false;

                // 群体隐身（有队伍时，队友一起隐身）
                if (hasGroup
                    && player.Magics.TryGetValue(MagicType.MassInvisibility, out UserMagic massInvisMagic)
                    && massInvisMagic.Info != null
                    && player.Level >= massInvisMagic.Info.NeedLevel1
                    && massInvisMagic.Cooldown <= SEnvir.Now)
                {
                    if (massInvisMagic.Cost > player.CurrentMP)
                    {
                        ProcessBotPotionMonitor(player);
                    }
                    else if (TryCastBotMagic(player, player.Direction, MagicType.MassInvisibility, player, player.CurrentLocation))
                    {
                        _botTaoistBuffTime[pid] = SEnvir.Now.AddSeconds(BotTaoistBuffCooldown);
                        usedInvisibility = true;
                    }
                }

                // 单体隐身（自己，群体隐身失败或没有队伍时）
                if (!usedInvisibility
                    && player.Magics.TryGetValue(MagicType.Invisibility, out UserMagic invisMagic)
                    && invisMagic.Info != null
                    && player.Level >= invisMagic.Info.NeedLevel1
                    && invisMagic.Cooldown <= SEnvir.Now
                    && !player.Buffs.Any(x => x.Type == BuffType.Invisibility))
                {
                    if (invisMagic.Cost > player.CurrentMP)
                    {
                        ProcessBotPotionMonitor(player);
                    }
                    else if (TryCastBotMagic(player, player.Direction, MagicType.Invisibility, player, player.CurrentLocation))
                    {
                        _botTaoistBuffTime[pid] = SEnvir.Now.AddSeconds(BotTaoistBuffCooldown);
                        usedInvisibility = true;
                    }
                }

                // 如果使用了隐身技能，直接返回（隐身是最高优先级）
                if (usedInvisibility)
                    return;
            }

            // ── 处理HP恢复（使用治愈技能）──────────────────────────────
            if (NeedHeal(player))
            {
                bool usedHeal = false;

                // 群体治愈（有队伍时，治疗队友）
                if (hasGroup
                    && player.Magics.TryGetValue(MagicType.MassHeal, out UserMagic massHealMagic)
                    && massHealMagic.Info != null
                    && player.Level >= massHealMagic.Info.NeedLevel1
                    && massHealMagic.Cooldown <= SEnvir.Now)
                {
                    // 检查队友中是否有 HP 不满且没有 Heal BUFF 的成员
                    bool needHeal = player.GroupMembers.Any(m =>
                        m != null && !m.Dead && m.Node != null
                        && m.CurrentHP < m.Stats[Stat.Health] * 0.8  // HP低于80%才治疗
                        && !m.Buffs.Any(x => x.Type == BuffType.Heal));

                    if (needHeal)
                    {
                        if (massHealMagic.Cost > player.CurrentMP)
                        {
                            ProcessBotPotionMonitor(player);
                        }
                        else if (TryCastBotMagic(player, player.Direction, MagicType.MassHeal, null, player.CurrentLocation))
                        {
                            _botTaoistBuffTime[pid] = SEnvir.Now.AddSeconds(BotTaoistBuffCooldown);
                            usedHeal = true;
                        }
                    }
                }

                // 单体治愈（治疗HP最低的目标，可以是队友或自己）
                if (!usedHeal
                    && player.Magics.TryGetValue(MagicType.Heal, out UserMagic healMagic)
                    && healMagic.Info != null
                    && player.Level >= healMagic.Info.NeedLevel1
                    && healMagic.Cooldown <= SEnvir.Now)
                {
                    // 目标优先：队友中（含自身）HP 最低且 HP 低于 80% 且无 Heal BUFF 的对象
                    PlayerObject healTarget = null;
                    int lowestHPPct = 100;

                    // 收集候选目标（队伍成员 + 自身）
                    IEnumerable<PlayerObject> candidates = hasGroup
                        ? player.GroupMembers
                        : (IEnumerable<PlayerObject>)new[] { player };

                    foreach (PlayerObject member in candidates)
                    {
                        if (member == null || member.Dead || member.Node == null) continue;
                        
                        int hpPct = (int)(member.CurrentHP * 100.0 / member.Stats[Stat.Health]);
                        if (hpPct >= 80) continue;  // HP高于80%不治疗
                        if (member.Buffs.Any(x => x.Type == BuffType.Heal)) continue;

                        if (hpPct < lowestHPPct)
                        {
                            lowestHPPct = hpPct;
                            healTarget = member;
                        }
                    }

                    if (healTarget != null)
                    {
                        if (healMagic.Cost > player.CurrentMP)
                        {
                            ProcessBotPotionMonitor(player);
                        }
                        else if (TryCastBotMagic(player, player.Direction, MagicType.Heal, healTarget, healTarget.CurrentLocation))
                        {
                            _botTaoistBuffTime[pid] = SEnvir.Now.AddSeconds(BotTaoistBuffCooldown);
                            usedHeal = true;
                        }
                    }
                }
            }
        }

        /// <summary>
        /// 判断道士是否面临生命威胁（需要使用隐身技能）。
        /// 判断标准：
        ///   1. HP < 30%（紧急状态）
        ///   2. 周围有敌对怪物且自己HP < 50%（中等威胁）
        /// </summary>
        private static bool HasLifeThreat(PlayerObject player)
        {
            if (player == null || player.Dead) return false;

            // 紧急状态：HP < 30%
            int hpPct = (int)(player.CurrentHP * 100.0 / player.Stats[Stat.Health]);
            if (hpPct < 30)
                return true;

            // 中等威胁：HP < 50% 且周围有敌对怪物
            if (hpPct < 50)
            {
                // 检查周围 8 格内是否有敌对怪物
                MonsterObject hostileMob = GetNearbyHostileMonster(player, 8);
                if (hostileMob != null)
                    return true;
            }

            return false;
        }

        /// <summary>
        /// 判断道士是否需要使用治愈技能。
        /// 判断标准：
        ///   1. 自己 HP < 80%
        ///   2. 有队伍时，队友中有人 HP < 80%
        /// </summary>
        private static bool NeedHeal(PlayerObject player)
        {
            if (player == null || player.Dead) return false;

            bool hasGroup = player.GroupMembers != null && player.GroupMembers.Count > 1;

            // 检查自己是否需要治疗
            int selfHpPct = (int)(player.CurrentHP * 100.0 / player.Stats[Stat.Health]);
            if (selfHpPct < 80)
                return true;

            // 检查队友是否需要治疗
            if (hasGroup)
            {
                bool teammateNeedsHeal = player.GroupMembers.Any(m =>
                    m != null && !m.Dead && m.Node != null
                    && m.CurrentHP < m.Stats[Stat.Health] * 0.8);

                if (teammateNeedsHeal)
                    return true;
            }

            return false;
        }

        /// <summary>
        /// 获取指定范围内最近的敌对怪物。
        /// </summary>
        private static MonsterObject GetNearbyHostileMonster(PlayerObject player, int range)
        {
            if (player == null || player.CurrentMap == null) return null;

            Point location = player.CurrentLocation;
            Map map = player.CurrentMap;

            // 扫描范围内所有怪物
            for (int x = Math.Max(0, location.X - range); x <= Math.Min(map.Width - 1, location.X + range); x++)
            {
                for (int y = Math.Max(0, location.Y - range); y <= Math.Min(map.Height - 1, location.Y + range); y++)
                {
                    Cell cell = map.GetCell(x, y);
                    if (cell == null || cell.Objects == null) continue;

                    foreach (MapObject obj in cell.Objects)
                    {
                        if (obj is MonsterObject mob && !mob.Dead && mob.Target == player)
                            return mob;
                    }
                }
            }

            return null;
        }


        // ══════════════════════════════════════════════════════════════════════
        //  AI – 自动学习职业技能
        // ══════════════════════════════════════════════════════════════════════

        // 技能学习冷却时间表：ObjectID → 下次允许尝试学技能的时间（避免每 Tick 重复学）
        private const int BotAutoLearnMaxNeedLevel = 35;
        private static readonly Dictionary<uint, DateTime> _botSkillLearnTime
            = new Dictionary<uint, DateTime>();

        // 高阶BOSS图扩编冷却：ObjectID → 下次允许重试补满队伍的时间。
        private static readonly Dictionary<uint, DateTime> _botHighBossGroupPrepareTime
            = new Dictionary<uint, DateTime>();

        // 高阶BOSS图预热目标：ObjectID → 最近判定可能切去的高阶BOSS地图。
        private static readonly Dictionary<uint, Map> _botUpcomingHighBossGroupTargets
            = new Dictionary<uint, Map>();

        // 高阶BOSS图满队进度锁：Map → 开始补满队伍的时间。
        // 防止多个队长同时补满同一个BOSS图，导致互相抢人。
        private static readonly Dictionary<Map, DateTime> _botHighBossGroupFullInProgress
            = new Dictionary<Map, DateTime>();

        // 真人邀请保护期：ObjectID → 保护截止时间。
        // 当真人邀请假人时，假人会先离开当前假人队伍，然后在此时间内不再接受任何假人发起的组队邀请，
        // 以确保真人有足够时间将假人邀请入自己的队伍。
        private static readonly Dictionary<uint, DateTime> _botHumanInviteCooldown
            = new Dictionary<uint, DateTime>();

        /// <summary>
        /// 真人邀请保护时长（秒）：假人离开假人队伍后，在此时间内不接受假人发起的组队邀请。
        /// 缩短到 15 秒，避免大量假人因真人邀请保护期而无法参与自动组队。
        /// </summary>
        private const int BotHumanInviteProtectSeconds = 15;

        /// <summary>
        /// 自动学习职业技能：
        ///   NeedLevel1 ≤ 35 且不高于当前等级：直接授予；
        ///   NeedLevel1 ≥ 36：必须先走技能书正式链路（背包秘籍 / 合成鉴定 / 残页兑换 / 商店购买）。
        /// </summary>
        private static void ProcessBotLearnSkill(PlayerObject player)
        {
            if (player == null || player.Dead || !Config.BotAutoLearnSkill) return;

            uint pid = player.ObjectID;
            if (_botSkillLearnTime.TryGetValue(pid, out DateTime nextLearn)
                && SEnvir.Now < nextLearn)
                return;
            _botSkillLearnTime[pid] = SEnvir.Now.AddSeconds(30);

            MirClass cls = player.Class;
            int level = player.Level;

            if (!ClassToRequired.TryGetValue(cls, out RequiredClass reqClass))
                reqClass = RequiredClass.All;

            foreach (MagicInfo magic in SEnvir.MagicInfoList.Binding)
            {
                if (magic == null || magic.Class != cls) continue;
                if (player.Magics.ContainsKey(magic.Magic)) continue;

                if (magic.NeedLevel1 > level)
                {
                    continue;
                }

                if (magic.NeedLevel1 <= BotAutoLearnMaxNeedLevel)
                {
                    try
                    {
                        UserMagic userMagic = SEnvir.UserMagicList.CreateNewObject();
                        userMagic.Character = player.Character;
                        userMagic.Info = magic;
                        player.Magics[magic.Magic] = userMagic;

                        player.Enqueue(new S.NewMagic { Magic = userMagic.ToClientInfo() });
                        player.RefreshStats();
                    }
                    catch (Exception)
                    {
                    }
                    continue;
                }

                int readyBookSlot = FindBotReadySkillBookSlot(player, magic, reqClass);
                if (readyBookSlot >= 0)
                {
                    if (SEnvir.Now < player.UseItemTime)
                    {
                        _botSkillLearnTime[pid] = SEnvir.Now.AddSeconds(BotSkillActionRetrySeconds);
                        return;
                    }

                    try
                    {
                        player.ItemUse(new CellLinkInfo
                        {
                            GridType = GridType.Inventory,
                            Slot = readyBookSlot,
                            Count = 1,
                        });
                    }
                    catch (Exception)
                    {
                    }
                    return;
                }

                if (TryBotAppraiseRecipeSkillBook(player, magic, reqClass))
                {
                    _botSkillLearnTime[pid] = SEnvir.Now.AddSeconds(BotSkillActionRetrySeconds);
                    return;
                }

                ItemInfo bookInfo = FindBotSkillBookInfo(magic, reqClass);

                if (TryBotRefineInventorySkillBooks(player, magic, reqClass))
                {
                    _botSkillLearnTime[pid] = SEnvir.Now.AddSeconds(BotSkillActionRetrySeconds);
                    return;
                }

                if (bookInfo != null && TryBotComposeRecipeSkillBookFromPages(player, magic, bookInfo))
                {
                    _botSkillLearnTime[pid] = SEnvir.Now.AddSeconds(BotSkillActionRetrySeconds);
                    return;
                }

                if (bookInfo != null && TryBotComposeRecipeSkillBook(player, magic, bookInfo))
                {
                    _botSkillLearnTime[pid] = SEnvir.Now.AddSeconds(BotSkillActionRetrySeconds);
                    return;
                }

                if (bookInfo != null && TryBotComposeSkillBookFromItemParts(player, magic, bookInfo))
                {
                    TryBotRefineInventorySkillBooks(player, magic, reqClass);
                    _botSkillLearnTime[pid] = SEnvir.Now.AddSeconds(BotSkillActionRetrySeconds);
                    return;
                }

                if (TryBotBuySkillBook(player, magic, reqClass))
                {
                    TryBotRefineInventorySkillBooks(player, magic, reqClass);
                    _botSkillLearnTime[pid] = SEnvir.Now.AddSeconds(BotSkillActionRetrySeconds);
                    return;
                }
            }
        }

        private static bool IsBotSkillBookClassMatch(ItemInfo info, RequiredClass reqClass)
        {
            if (info == null || info.ItemType != ItemType.Book) return false;
            return info.RequiredClass == RequiredClass.All || (info.RequiredClass & reqClass) != 0;
        }

        private static bool IsBotDirectManualInfo(ItemInfo info)
        {
            if (info == null) return false;
            if (!string.IsNullOrEmpty(info.ItemName) && info.ItemName.Contains("秘籍")) return true;
            return info.Durability >= 100;
        }

        private static string GetBotSkillRecipePageItemName(string skillName)
        {
            return string.IsNullOrEmpty(skillName) ? string.Empty : $"{skillName}（残页）";
        }

        private static string GetBotSkillRecipeManualItemName(string skillName)
        {
            return string.IsNullOrEmpty(skillName) ? string.Empty : $"{skillName}（秘籍）";
        }

        private static ItemCheck CreateBotScriptItemCheck(ItemInfo info)
        {
            UserItemFlags flags = UserItemFlags.None;
            if (info != null && !info.CanDrop)
                flags |= UserItemFlags.Bound;

            TimeSpan duration = info == null ? TimeSpan.Zero : TimeSpan.FromSeconds(info.Duration);
            if (duration != TimeSpan.Zero)
                flags |= UserItemFlags.Expirable;

            return new ItemCheck(info, 1, flags, duration);
        }

        private static int FindBotReadySkillBookSlot(PlayerObject player, MagicInfo magic, RequiredClass reqClass)
        {
            if (player == null || magic == null) return -1;

            int bestSlot = -1;
            int bestDurability = -1;
            for (int i = 0; i < player.Inventory.Length; i++)
            {
                UserItem item = player.Inventory[i];
                if (item?.Info == null) continue;
                if (item.Info.Shape != magic.Index) continue;
                if (!IsBotSkillBookClassMatch(item.Info, reqClass)) continue;
                if (item.CurrentDurability < 100) continue;

                if (item.CurrentDurability > bestDurability)
                {
                    bestDurability = item.CurrentDurability;
                    bestSlot = i;
                }
            }

            return bestSlot;
        }

        private static ItemInfo FindBotSkillBookInfo(MagicInfo magic, RequiredClass reqClass)
        {
            ItemInfo exactBaseInfo = null;
            int exactBasePrice = int.MaxValue;
            int exactBaseDurability = -1;

            ItemInfo fallbackBaseInfo = null;
            int fallbackBasePrice = int.MaxValue;
            int fallbackBaseDurability = -1;

            ItemInfo bestAnyInfo = null;
            int bestAnyPrice = int.MaxValue;
            int bestAnyDurability = -1;

            foreach (ItemInfo info in SEnvir.ItemInfoList.Binding)
            {
                if (info == null || info.ItemType != ItemType.Book) continue;
                if (info.Shape != magic.Index) continue;
                if (!IsBotSkillBookClassMatch(info, reqClass)) continue;

                int price = info.Price > 0 ? info.Price : int.MaxValue / 4;
                if (bestAnyInfo == null
                    || price < bestAnyPrice
                    || (price == bestAnyPrice && info.Durability > bestAnyDurability))
                {
                    bestAnyInfo = info;
                    bestAnyPrice = price;
                    bestAnyDurability = info.Durability;
                }

                if (IsBotDirectManualInfo(info)) continue;

                bool exactBaseName = string.Equals(info.ItemName, magic.Name, StringComparison.Ordinal);
                if (exactBaseName)
                {
                    if (exactBaseInfo == null
                        || price < exactBasePrice
                        || (price == exactBasePrice && info.Durability > exactBaseDurability))
                    {
                        exactBaseInfo = info;
                        exactBasePrice = price;
                        exactBaseDurability = info.Durability;
                    }

                    continue;
                }

                if (fallbackBaseInfo == null
                    || price < fallbackBasePrice
                    || (price == fallbackBasePrice && info.Durability > fallbackBaseDurability))
                {
                    fallbackBaseInfo = info;
                    fallbackBasePrice = price;
                    fallbackBaseDurability = info.Durability;
                }
            }

            return exactBaseInfo ?? fallbackBaseInfo ?? bestAnyInfo;
        }

        private static int GetBotNpcGoodUnitCost(ClientNPCGood good)
        {
            if (good?.Item == null) return int.MaxValue / 4;

            if (good.Currency != Globals.Currency)
                return good.CurrencyCost > 0 ? good.CurrencyCost : int.MaxValue / 4;

            if (good.Cost > 0) return good.Cost;
            if (good.RealCost > 0) return good.RealCost;

            decimal rate = good.Rate > 0 ? good.Rate : (good.RealRate > 0 ? good.RealRate : 1m);
            return (int)Math.Max(1, Math.Ceiling(rate * good.Item.Price));
        }

        private static bool TryBotCanAffordNpcGood(PlayerObject player, ClientNPCGood good, int amount)
        {
            if (player == null || good?.Item == null || amount <= 0) return false;

            if (good.Currency != Globals.Currency)
            {
                int unitCost = good.CurrencyCost > 0 ? good.CurrencyCost : int.MaxValue / 4;
                return unitCost < int.MaxValue / 4 && player.GetItemCount(good.Currency) >= (long)unitCost * amount;
            }

            int cost = GetBotNpcGoodUnitCost(good);
            return cost < int.MaxValue / 4 && player.Gold >= (long)cost * amount;
        }

        private static bool TryBotConsumeNpcGoodCost(PlayerObject player, ClientNPCGood good, int amount)
        {
            if (!TryBotCanAffordNpcGood(player, good, amount)) return false;

            if (good.Currency != Globals.Currency)
            {
                player.TakeItem(good.Currency, (long)good.CurrencyCost * amount);
                return true;
            }

            long totalCost = (long)GetBotNpcGoodUnitCost(good) * amount;
            if (totalCost <= 0 || player.Gold < totalCost) return false;

            ChangeBotGoldSilently(player, -totalCost);
            return true;
        }

        private static int TryBotBuySkillBookCopies(PlayerObject player, ClientNPCGood good, int requestedCount, string skillName)
        {
            if (player == null || good?.Item == null || requestedCount <= 0) return 0;

            int bought = 0;
            ItemCheck check = new ItemCheck(good.Item, 1, UserItemFlags.NonRefinable, TimeSpan.Zero);
            for (int i = 0; i < requestedCount; i++)
            {
                if (!player.CanGainItems(true, check)) break;
                if (!TryBotConsumeNpcGoodCost(player, good, 1)) break;

                UserItem book = SEnvir.CreateFreshItem(check);
                if (IsBotDirectManualInfo(good.Item))
                    book.CurrentDurability = 100;

                SEnvir.RecordTrackingInfo(book, player.CurrentMap?.Info?.Description, ObjectType.None, "假人自动购书", player.Name);
                player.GainItem(book);
                bought++;
            }

            return bought;
        }

        private static bool TryBotRefineInventorySkillBooks(PlayerObject player, MagicInfo magic, RequiredClass reqClass)
        {
            if (player == null || magic == null) return false;

            List<int> slots = new List<int>();
            for (int i = 0; i < player.Inventory.Length; i++)
            {
                UserItem item = player.Inventory[i];
                if (item?.Info == null) continue;
                if (item.Info.Shape != magic.Index) continue;
                if (!IsBotSkillBookClassMatch(item.Info, reqClass)) continue;
                if (item.CurrentDurability >= 100) continue;
                slots.Add(i);
            }

            if (slots.Count < 2) return false;

            slots = slots.OrderByDescending(x => player.Inventory[x]?.CurrentDurability ?? 0).ToList();
            foreach (int targetSlot in slots)
            {
                UserItem targetBook = player.Inventory[targetSlot];
                if (targetBook?.Info == null) continue;

                int totalDurability = Math.Max(0, targetBook.CurrentDurability);
                long materialDurability = 0;
                List<int> materialSlots = new List<int>();

                foreach (int materialSlot in slots)
                {
                    if (materialSlot == targetSlot) continue;

                    UserItem materialBook = player.Inventory[materialSlot];
                    if (materialBook?.Info == null) continue;
                    if (materialBook.Info.ItemName != targetBook.Info.ItemName) continue;

                    int pages = Math.Max(0, materialBook.CurrentDurability);
                    if (pages <= 0) continue;

                    materialSlots.Add(materialSlot);
                    materialDurability += pages;
                    totalDurability += pages;
                    if (totalDurability >= 100) break;
                }

                if (totalDurability < 100 || materialSlots.Count == 0) continue;

                long cost = (long)Math.Max(0, targetBook.Info.RequiredAmount) * 1000L
                            + materialDurability * Globals.BookCombineFeePerDurability;
                if (player.Gold < cost) continue;

                materialSlots.Sort();
                materialSlots.Reverse();
                foreach (int materialSlot in materialSlots)
                {
                    UserItem materialBook = player.Inventory[materialSlot];
                    if (materialBook == null) continue;

                    player.RemoveItem(materialBook);
                    player.Inventory[materialSlot] = null;
                    materialBook.Delete();
                    player.Enqueue(new S.ItemChanged
                    {
                        Link = new CellLinkInfo { GridType = GridType.Inventory, Slot = materialSlot },
                        Success = true,
                    });
                }

                targetBook.CurrentDurability = 100;
                ChangeBotGoldSilently(player, -cost);
                player.RefreshWeight();
                player.Enqueue(new S.ItemChanged
                {
                    Link = new CellLinkInfo { GridType = GridType.Inventory, Slot = targetSlot, Count = targetBook.Count },
                    Success = true,
                });

                return true;
            }

            return false;
        }

        private static bool TryBotAppraiseRecipeSkillBook(PlayerObject player, MagicInfo magic, RequiredClass reqClass)
        {
            if (player == null || magic == null) return false;
            if (!BotSkillBookRecipes.TryGetValue(magic.Name, out BotSkillBookRecipe recipe)) return false;
            if (recipe.AppraiseGold <= 0 || player.Gold < recipe.AppraiseGold) return false;

            int bookSlot = -1;
            int bestDurability = -1;
            for (int i = 0; i < player.Inventory.Length; i++)
            {
                UserItem item = player.Inventory[i];
                if (item?.Info == null) continue;
                if (item.Info.ItemType != ItemType.Book) continue;
                if (item.Info.Shape != magic.Index) continue;
                if (!IsBotSkillBookClassMatch(item.Info, reqClass)) continue;
                if (!string.Equals(item.Info.ItemName, magic.Name, StringComparison.Ordinal)) continue;
                if (item.CurrentDurability >= 100) continue;

                if (item.CurrentDurability > bestDurability)
                {
                    bestDurability = item.CurrentDurability;
                    bookSlot = i;
                }
            }

            if (bookSlot < 0) return false;

            string manualItemName = GetBotSkillRecipeManualItemName(magic.Name);
            ItemInfo manualInfo = SEnvir.ItemInfoList.Binding.FirstOrDefault(x => x != null
                                                                                  && x.ItemType == ItemType.Book
                                                                                  && x.Shape == magic.Index
                                                                                  && IsBotSkillBookClassMatch(x, reqClass)
                                                                                  && string.Equals(x.ItemName, manualItemName, StringComparison.Ordinal));

            UserItem sourceBook = player.Inventory[bookSlot];
            if (sourceBook == null) return false;

            ChangeBotGoldSilently(player, -recipe.AppraiseGold);

            if (manualInfo != null)
            {
                player.TakeItem(bookSlot, 1);

                ItemCheck manualCheck = CreateBotScriptItemCheck(manualInfo);
                UserItem manualBook = SEnvir.CreateFreshItem(manualCheck);
                manualBook.CurrentDurability = 100;
                SEnvir.RecordTrackingInfo(manualBook, player.CurrentMap?.Info?.Description, ObjectType.None, "假人技能书鉴定", player.Name);
                player.GainItem(manualBook);
            }
            else
            {
                sourceBook.CurrentDurability = 100;
                player.Enqueue(new S.ItemDurability
                {
                    GridType = GridType.Inventory,
                    Slot = bookSlot,
                    CurrentDurability = sourceBook.CurrentDurability,
                });
                player.Enqueue(new S.ItemChanged
                {
                    Link = new CellLinkInfo { GridType = GridType.Inventory, Slot = bookSlot, Count = sourceBook.Count },
                    Success = true,
                });
            }

            return true;
        }

        private static bool TryBotComposeRecipeSkillBookFromPages(PlayerObject player, MagicInfo magic, ItemInfo bookInfo)
        {
            if (player == null || magic == null || bookInfo == null) return false;
            if (!BotSkillBookRecipes.TryGetValue(magic.Name, out BotSkillBookRecipe recipe)) return false;
            if (recipe.PageCount <= 0 || recipe.ComposeGold <= 0) return false;

            string pageItemName = GetBotSkillRecipePageItemName(magic.Name);
            if (string.IsNullOrEmpty(pageItemName)) return false;

            long pageCount = player.GetItemCount(pageItemName);
            if (pageCount < recipe.PageCount) return false;
            if (player.Gold < recipe.ComposeGold) return false;

            ItemCheck check = CreateBotScriptItemCheck(bookInfo);
            if (!player.CanGainItems(true, check)) return false;

            player.TakeItem(pageItemName, recipe.PageCount);
            ChangeBotGoldSilently(player, -recipe.ComposeGold);

            UserItem book = SEnvir.CreateFreshItem(check);
            SEnvir.RecordTrackingInfo(book, player.CurrentMap?.Info?.Description, ObjectType.None, "假人残页合书", player.Name);
            player.GainItem(book);

            return true;
        }

        private static bool TryBotComposeRecipeSkillBook(PlayerObject player, MagicInfo magic, ItemInfo bookInfo)
        {
            if (player == null || magic == null || bookInfo == null) return false;
            if (!BotSkillBookRecipes.TryGetValue(magic.Name, out BotSkillBookRecipe recipe)) return false;
            if (recipe.PageCount <= 0 || recipe.ComposeGold <= 0) return false;

            long pageCount = player.GetItemPartsCount(bookInfo.ItemName);
            if (pageCount < recipe.PageCount) return false;
            if (player.Gold < recipe.ComposeGold) return false;

            ItemCheck check = CreateBotScriptItemCheck(bookInfo);
            if (!player.CanGainItems(true, check)) return false;

            player.TakeItemParts(bookInfo.ItemName, recipe.PageCount);
            ChangeBotGoldSilently(player, -recipe.ComposeGold);

            UserItem book = SEnvir.CreateFreshItem(check);
            SEnvir.RecordTrackingInfo(book, player.CurrentMap?.Info?.Description, ObjectType.None, "假人残页兑换", player.Name);
            player.GainItem(book);

            return true;
        }

        private static bool TryBotComposeSkillBookFromItemParts(PlayerObject player, MagicInfo magic, ItemInfo bookInfo)
        {
            if (player == null || magic == null || bookInfo == null) return false;
            if (bookInfo.PartCount < 1) return false;

            long partCount = player.GetItemPartsCount(bookInfo.ItemName);
            if (partCount < bookInfo.PartCount) return false;

            ItemCheck check = new ItemCheck(bookInfo, 1, UserItemFlags.NonRefinable, TimeSpan.Zero);
            if (!player.CanGainItems(true, check)) return false;

            player.TakeItemParts(bookInfo.ItemName, bookInfo.PartCount);

            UserItem book = SEnvir.CreateFreshItem(check);
            if (IsBotDirectManualInfo(bookInfo))
                book.CurrentDurability = 100;

            SEnvir.RecordTrackingInfo(book, player.CurrentMap?.Info?.Description, ObjectType.None, "假人碎片合成", player.Name);
            player.GainItem(book);

            return true;
        }

        private static bool TryBotBuySkillBook(PlayerObject player, MagicInfo magic, RequiredClass reqClass)
        {
            if (player == null || magic == null) return false;

            List<ClientNPCGood> goods = new List<ClientNPCGood>();
            foreach (NPCScript script in SEnvir.NPCScripts.Values)
            {
                if (script?.Goods == null) continue;

                foreach (ClientNPCGood good in script.Goods)
                {
                    if (good?.Item == null) continue;
                    if (good.Item.ItemType != ItemType.Book) continue;
                    if (good.Item.Shape != magic.Index) continue;
                    if (!IsBotSkillBookClassMatch(good.Item, reqClass)) continue;
                    goods.Add(good);
                }
            }

            if (goods.Count == 0) return false;

            ClientNPCGood directGood = null;
            int directCost = int.MaxValue;
            foreach (ClientNPCGood good in goods)
            {
                if (!IsBotDirectManualInfo(good.Item)) continue;
                if (!TryBotCanAffordNpcGood(player, good, 1)) continue;

                int unitCost = GetBotNpcGoodUnitCost(good);
                if (unitCost < directCost)
                {
                    directGood = good;
                    directCost = unitCost;
                }
            }

            if (directGood != null)
                return TryBotBuySkillBookCopies(player, directGood, 1, magic.Name) > 0;

            ClientNPCGood bestGood = null;
            double bestScore = double.MaxValue;
            foreach (ClientNPCGood good in goods)
            {
                if (IsBotDirectManualInfo(good.Item)) continue;

                int unitCost = GetBotNpcGoodUnitCost(good);
                if (unitCost >= int.MaxValue / 4) continue;

                int pagesPerCopy = Math.Max(1, good.Item.Durability);
                double score = unitCost / (double)pagesPerCopy;
                if (score < bestScore)
                {
                    bestScore = score;
                    bestGood = good;
                }
            }

            if (bestGood == null) return false;

            int ownedPages = 0;
            for (int i = 0; i < player.Inventory.Length; i++)
            {
                UserItem item = player.Inventory[i];
                if (item?.Info == null) continue;
                if (item.Info.ItemName != bestGood.Item.ItemName) continue;
                ownedPages += Math.Max(0, item.CurrentDurability);
            }

            int pagesNeeded = Math.Max(1, 100 - ownedPages);
            int pagesPerBook = Math.Max(1, bestGood.Item.Durability);
            int requestedCopies = (int)Math.Ceiling(pagesNeeded / (double)pagesPerBook);

            return TryBotBuySkillBookCopies(player, bestGood, requestedCopies, magic.Name) > 0;
        }

        /// <summary>
        /// 切比雪夫距离（8方向距离，Max(|Δx|, |Δy|)），与游戏攻击/移动范围判断一致。
        /// </summary>
        private static int MaxChebyshevDistance(Point a, Point b)
        {
            return Math.Max(Math.Abs(a.X - b.X), Math.Abs(a.Y - b.Y));
        }

        private static void InitializeBotGroupStateOnLogin(PlayerObject player)
        {
            if (player?.Character?.Account == null) return;

            uint pid = player.ObjectID;

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

            if (player.Character.Account.AllowGroup)
                player.GroupSwitch(false);
            else
                player.Character.Account.AllowGroup = false;

            if (Config.BotAllowGroup)
                player.GroupSwitch(true);

            _botHumanInviteCooldown.Remove(pid);
            _botForcedGroupLockUntil.Remove(pid);
            RecordBotGroupReset(player);
        }

        /// <summary>
        /// 获取假人对应的玩家对象
        /// </summary>
        private static PlayerObject GetBotPlayer(BotAccountInfo bot)
        {
            return botPlayers.FirstOrDefault(p => p.Character.Account == bot.Account);
        }


        /// <summary>
        /// 登录假人账号并进入游戏
        /// </summary>
        private static void LoginBot(BotAccountInfo bot)
        {
            try
            {
                if (bot.Account == null)
                {
                    SEnvir.Log("假人登录异常：账号对象为空");
                    bot.BotState = DBModels.BotState.Idle;
                    return;
                }

                if (!IsBotWithinTargetCount(bot))
                {
                    bot.BotState = DBModels.BotState.Idle;
                    return;
                }

                var character = bot.Account.Characters.FirstOrDefault(x => !x.Deleted);
                if (character == null)
                {
                    SEnvir.Log($"假人登录异常 [{bot.Account.EMailAddress}]：未找到可用角色");
                    bot.BotState = DBModels.BotState.Idle;
                    return;
                }

                var fakeConnection = CreateBotConnection(bot.Account);
                if (fakeConnection == null)
                {
                    bot.BotState = DBModels.BotState.Idle;
                    return;
                }

                PlayerObject player = new PlayerObject(character, fakeConnection);
                player.BotPlayer = true;
                player.IsBot = true;  // 同步标记，供 ServerLibrary 层（如 PlayerGroup）读取，避免反向依赖

                // 假人默认允许被观察（无需玩家手动开启）
                character.Observable = true;

                // 根据服务器配置同步假人组队开关
                character.Account.AllowGroup = Config.BotAllowGroup;

                // 假人始终允许被交易、加好友、加入行会
                character.Account.AllowTrade = true;
                character.Account.AllowFriend = true;
                character.Account.AllowGuild = Config.BotGuildSystem;

                // 假人默认不能停在和平模式，否则 CanAttackTarget 对野怪永远返回 false。
                if (character.AttackMode == AttackMode.Peace)
                    character.AttackMode = AttackMode.Group;

                try
                {
                    player.StartGame();
                }
                catch (Exception ex)
                {
                    SEnvir.Log($"假人StartGame异常 [{character.CharacterName}]: {ex.Message}\n{ex.StackTrace}");
                }

                // ★ StartGame 失败时会将 Character = null，此时不能加入主循环
                // 否则主循环调 ProcessRegen() → Class => Character.Class → NullReferenceException
                if (player.Character == null)
                {
                    SEnvir.Log($"假人登录异常 [{character.CharacterName}]：StartGame 未完成初始化");
                    bot.BotState = DBModels.BotState.Idle;
                    return;
                }

                AddBotPlayer(player);

                // 将假人连接添加到连接列表
                SEnvir.Connections.Add(player.Connection);

                // 更新状态
                bot.BotState = DBModels.BotState.Playing;
                bot.LastActionTime = Time.Now;

                BeginBotLoginWarmup(player);

                // ★ 假人首次登录初始化：赠送初始金币 + 1 级及以下装配乌木剑和布衣
                ApplyInitialGoldFloor(player);
                ApplyBotLevelRewards(player);
                EquipStarterWeapon(player);

                // 每次 bot 上线都先把旧组队引用/邀请状态重置掉，再重新参与本轮自动组队。
                InitializeBotGroupStateOnLogin(player);

                // 连续登录期间只延后一次自动组队重建，避免每登一个就全量扫一次在线 bot。
                if (Config.BotAllowGroup && Config.BotAutoGroup)
                {
                    // SEnvir.Log($"[LoginBot] 触发 ScheduleBotAutoGroupRebuild, 新登录假人={player.Name}");
                    ScheduleBotAutoGroupRebuild();
                }

                // 假人自动加入已有托管行会；是否允许新建托管行会由管理面板 BotCreateGuild 控制。
                AssignBotToGuild(player);

            }
            catch (Exception ex)
            {
                SEnvir.Log($"假人登录失败: {ex.Message}\n{ex.StackTrace}");
                bot.BotState = DBModels.BotState.Idle;
            }
        }

        // ══════════════════════════════════════════════════════════════════════
        //  AI – 假人行会管理
        // ══════════════════════════════════════════════════════════════════════

        private const int BotGuildMemberLimit = 30;
        private const int BotConquestApplyCooldownSeconds = 15;

        private static bool IsBotManagedGuildName(string guildName)

        {
            if (string.IsNullOrWhiteSpace(guildName))
                return false;

            foreach (string configuredName in GetConfiguredBotGuildNames())
            {
                if (string.IsNullOrWhiteSpace(configuredName))
                    continue;

                if (string.Equals(guildName, configuredName, StringComparison.OrdinalIgnoreCase))
                    return true;

                if (guildName.Length > configuredName.Length &&
                    guildName.StartsWith(configuredName, StringComparison.OrdinalIgnoreCase) &&
                    guildName.Substring(configuredName.Length).All(char.IsDigit))
                    return true;
            }

            return false;
        }

        private static string GetNextBotGuildName()
        {
            List<string> baseNames = GetConfiguredBotGuildNames()
                .Where(x => !string.IsNullOrWhiteSpace(x))
                .Distinct(StringComparer.OrdinalIgnoreCase)
                .OrderBy(x => _botRandom.Next())
                .ToList();

            if (baseNames.Count == 0)
            {
                baseNames = GetDefaultBotGuildNames()
                    .Distinct(StringComparer.OrdinalIgnoreCase)
                    .OrderBy(x => _botRandom.Next())
                    .ToList();
            }

            foreach (string baseName in baseNames)
            {
                if (!SEnvir.GuildInfoList.Binding.Any(g => string.Equals(g.GuildName, baseName, StringComparison.OrdinalIgnoreCase)))
                    return baseName;
            }

            foreach (string baseName in baseNames)
            {
                for (int seq = 2; seq <= 9999; seq++)
                {
                    string candidate = BuildIndexedBotGuildName(baseName, seq);
                    if (!IsValidBotGuildNameConfigEntry(candidate))
                        continue;

                    if (!SEnvir.GuildInfoList.Binding.Any(g => string.Equals(g.GuildName, candidate, StringComparison.OrdinalIgnoreCase)))
                        return candidate;
                }
            }

            return BuildIndexedBotGuildName(baseNames[0], SEnvir.GuildInfoList.Binding.Count + 1);
        }

        private static string BuildIndexedBotGuildName(string baseName, int seq)
        {
            string suffix = Math.Max(2, seq).ToString();
            string safeBaseName = string.IsNullOrWhiteSpace(baseName) ? "BOT" : baseName.Trim();
            int maxBaseLength = Math.Max(1, Globals.MaxGuildNameLength - suffix.Length);

            if (safeBaseName.Length > maxBaseLength)
                safeBaseName = safeBaseName.Substring(0, maxBaseLength);

            string candidate = safeBaseName + suffix;

            if (candidate.Length < Globals.MinGuildNameLength)
                candidate = candidate.PadRight(Globals.MinGuildNameLength, '0');

            return candidate;
        }

        private static bool IsBotManagedGuildLeader(PlayerObject player)
        {
            GuildMemberInfo member = player?.Character?.Account?.GuildMember;
            if (member?.Guild == null) return false;
            if ((member.Permission & GuildPermission.Leader) != GuildPermission.Leader) return false;

            return IsBotManagedGuildName(member.Guild.GuildName);
        }

        private static bool TryGetBotValidUmaKingHorn(PlayerObject player, out UserItem horn)
        {
            horn = null;
            if (player?.Inventory == null) return false;

            foreach (UserItem item in player.Inventory)
            {
                if (!IsValidUmaKingHornForConquest(item)) continue;

                horn = item;
                return true;
            }

            return false;
        }

        private static double GetBotConquestStartDelaySeconds(CastleInfo castle)
        {
            if (castle == null) return double.MaxValue;

            TimeSpan delay = castle.StartTime - SEnvir.Now.TimeOfDay;
            if (delay < TimeSpan.Zero)
                delay += TimeSpan.FromDays(1);

            return delay.TotalSeconds;
        }

        private static CastleInfo GetBotPreferredConquestCastle(PlayerObject player)
        {
            GuildInfo guild = player?.Character?.Account?.GuildMember?.Guild;
            if (guild == null) return null;

            return SEnvir.CastleInfoList.Binding
                .Where(castle => castle?.Item?.Effect == ItemEffect.UmaKingHorn && guild.Castle != castle)
                .OrderBy(castle => SEnvir.UserConquestList.Binding.Count(x => x.Castle == castle && x.WarDate.Date >= SEnvir.Now.Date))
                .ThenBy(castle => GetBotConquestStartDelaySeconds(castle))
                .ThenBy(castle => castle.Index)
                .FirstOrDefault();
        }

        private static void ProcessBotConquestApply(PlayerObject player)
        {
            if (!Config.BotParticipateConquest || !Config.BotGuildSystem
                || player == null || player.Dead || player.Node == null) return;
            if (!IsBotManagedGuildLeader(player)) return;

            GuildInfo guild = player.Character.Account.GuildMember?.Guild;
            if (guild == null || guild.Castle != null) return;
            if (SEnvir.ConquestWars.Count > 0) return;
            if (!TryGetBotValidUmaKingHorn(player, out _)) return;

            uint pid = player.ObjectID;
            if (_botConquestApplyTime.TryGetValue(pid, out DateTime nextApplyTime) && SEnvir.Now < nextApplyTime)
                return;

            DateTime targetWarDate = SEnvir.Now.AddDays(Config.WarsTime).Date;
            if (SEnvir.UserConquestList.Binding.Any(x => x.Guild == guild && x.WarDate.Date == targetWarDate))
                return;

            CastleInfo castle = GetBotPreferredConquestCastle(player);
            if (castle == null) return;

            _botConquestApplyTime[pid] = SEnvir.Now.AddSeconds(BotConquestApplyCooldownSeconds);
            player.GuildConquest(castle.Index);
        }

        /// <summary>
        /// 为假人分配行会：

        ///   1. 已在行会 → 跳过。
        ///   2. 存在未满的假人托管行会 → 随机加入其中一个。
        ///   3. 没有未满的托管行会时，只有管理面板勾选 BotCreateGuild 才会从 假人行会名字.txt 取名创建新行会。
        /// </summary>
        private static void AssignBotToGuild(PlayerObject player)
        {
            if (!Config.BotGuildSystem || player?.Character?.Account == null) return;

            // 已在行会，不处理
            if (player.Character.Account.GuildMember != null) return;

            try
            {
                // 找出所有 bot 自动维护且成员数 < 30 的行会
                var availableGuilds = SEnvir.GuildInfoList.Binding
                    .Where(g => IsBotManagedGuildName(g.GuildName)
                                && g.Members.Count < BotGuildMemberLimit)
                    .ToList();

                GuildInfo targetGuild;

                if (availableGuilds.Count > 0)
                {
                    // 随机选一个未满行会
                    targetGuild = availableGuilds[_botRandom.Next(availableGuilds.Count)];
                }
                else
                {
                    if (!Config.BotCreateGuild || !Config.BotGuildSystem)
                        return;

                    targetGuild = SEnvir.GuildInfoList.CreateNewObject();
                    targetGuild.GuildName = GetNextBotGuildName();
                    targetGuild.MemberLimit = BotGuildMemberLimit;
                    targetGuild.StorageSize = 10;
                    targetGuild.GuildLevel = 1;
                }


                // 将假人加入目标行会
                bool isFirstMember = targetGuild.Members.Count == 0;
                GuildMemberInfo memberInfo = SEnvir.GuildMemberInfoList.CreateNewObject();
                memberInfo.Account = player.Character.Account;
                memberInfo.Guild = targetGuild;
                memberInfo.Rank = isFirstMember ? "会长" : "成员";
                memberInfo.JoinDate = SEnvir.Now;
                memberInfo.Permission = isFirstMember
                    ? GuildPermission.Leader
                    : targetGuild.DefaultPermission;

                // 推行会信息给假人客户端
                player.SendGuildInfo();

                // 广播外观变化（头顶行会名）
                player.Broadcast(new S.GuildChanged
                {
                    ObjectID = player.ObjectID,
                    GuildName = targetGuild.GuildName,
                    GuildRank = memberInfo.Rank
                });
            }
            catch (Exception)
            {
                // SEnvir.Log($"假人 [{player.Name}] 行会分配异常: {ex.Message}");
            }
        }


        /// <summary>
        /// 创建假人连接
        /// </summary>

        private static SConnection CreateBotConnection(AccountInfo account)
        {
            try
            {
                // 直接使用假人专用构造函数，无需反射和 MockTcpClient
                var conn = new SConnection(account, "127.0.0.1");

                // 订阅假人断开事件，在 Server 层处理清理，避免 ServerLibrary → Server 的循环依赖
                conn.OnBotDisconnected += (sender, e) =>
                {
                    if (sender is SConnection bc)
                        RemoveBotConnection(bc);
                };

                return conn;
            }
            catch (Exception ex)
            {
                SEnvir.Log($"创建假人连接失败 [{account?.EMailAddress ?? "未知账号"}]: {ex.Message}\n{ex.StackTrace}");
                return null;
            }
        }

        /// <summary>
        /// 移除假人连接（由 SConnection.OnBotDisconnected 事件触发）
        /// </summary>
        public static void RemoveBotConnection(SConnection conn)
        {
            try
            {
                var player = botPlayers.FirstOrDefault(p => p.Connection == conn);
                if (player != null)
                {
                    RemoveBotPlayer(player);
                    _botStates.TryRemove(player.ObjectID, out _);
                    _botTargets.Remove(player.ObjectID);
                    _botTargetSwitchTime.Remove(player.ObjectID);
                    _botRoamDir.Remove(player.ObjectID);
                    _botRoamTime.Remove(player.ObjectID);
                    _botTargetItems.Remove(player.ObjectID);
                    _botWaitingPickup.Remove(player.ObjectID);
                    _botLastAttackTime.Remove(player.ObjectID);
                    _botLastSnapPos.Remove(player.ObjectID);
                    _botLastSnapTime.Remove(player.ObjectID);
                    _botDriftAnchorPos.Remove(player.ObjectID);
                    _botDriftAnchorTime.Remove(player.ObjectID);
                    _botMapEvalTime.Remove(player.ObjectID);
                    _botMapStayMapIndex.Remove(player.ObjectID);
                    _botMapStayStartTime.Remove(player.ObjectID);
                    _botRecallUntil.Remove(player.ObjectID);
                    _botSkillLearnTime.Remove(player.ObjectID);
                    _botSellTime.Remove(player.ObjectID);
                    _botRestockTime.Remove(player.ObjectID);
                    _botPotionCooldownTime.Remove(player.ObjectID);
                    _botUrgentPotionBuyTime.Remove(player.ObjectID);
                    _botAssassinSupportTime.Remove(player.ObjectID);
                    _botNextSocialTime.Remove(player.ObjectID);
                    _botPendingChatReplies.Remove(player.ObjectID);
                    _botHighBossGroupPrepareTime.Remove(player.ObjectID);
                    _botUpcomingHighBossGroupTargets.Remove(player.ObjectID);
                    _botHumanInviteCooldown.Remove(player.ObjectID);
                    _botForcedGroupLockUntil.Remove(player.ObjectID);
                    _botTelemetry.Remove(player.ObjectID);
                    _botBehaviorProfiles.Remove(player.ObjectID);
                    _botLoginWarmupUntil.Remove(player.ObjectID);
                    _botConquestApplyTime.Remove(player.ObjectID);
                    UnmarkBotQueued(_botQueued, player.ObjectID);
                    _botLastEquipmentUpgradeCheckTime.Remove(player.ObjectID);
                    _botLastTradeWithBotCheckTime.Remove(player.ObjectID);
                    _botLastTradeWithHumanCheckTime.Remove(player.ObjectID);
                    _botTradeCooldownUntil.Remove(player.ObjectID);
                    _botLastTradePartner.Remove(player.ObjectID);
                     BotPvPStrategy.ClearPvPState(player.ObjectID);
                     ClearBotSiegeState(player.ObjectID);
                     BotSocialMemory.ClearBot(player.ObjectID);

                     _botEquipmentMaintenanceTime.Remove(player.ObjectID);
                     _botConsumableMaintenanceTime.Remove(player.ObjectID);
                     _botInventoryMaintenanceTime.Remove(player.ObjectID);
                     _botClassSupportTime.Remove(player.ObjectID);
                     _botHighBossMaintenanceTime.Remove(player.ObjectID);

                     UnmarkBotQueued(_botPotionQueued, player.ObjectID);
                    // 离开队伍，通知其他队员

                    if (player.GroupMembers != null)
                        try { player.GroupLeave(); } catch { }
                    SEnvir.Players.Remove(player);
                    if (SnapshotBotPlayers().Length == 0)
                        ResetRuntimeQuickTuning("最后一名假人已下线");
                    SEnvir.Log($"假人已移除: {player.Character?.CharacterName}，剩余: {botPlayers.Count}");
                }

                // SEnvir.Connections 已在 SConnection.Disconnect() 的 IsBot 分支里 Remove 过，
                // 此处仅做兜底（Remove 不存在的元素是安全的，不会 throw）
                SEnvir.Connections.Remove(conn);

                // 重置对应 bot 状态为 Idle，让下次 Tick 重新登录
                var bot = botAccounts.FirstOrDefault(b => b.Account == conn.Account);
                if (bot != null)
                    bot.BotState = DBModels.BotState.Idle;
            }
            catch (Exception ex)
            {
                SEnvir.Log($"移除假人连接异常: {ex.Message}");
            }
        }

        /// <summary>
        /// 假人是否正在运行
        /// </summary>
        public static bool IsRunning => isRunning;

        /// <summary>
        /// 获取当前假人数量
        /// </summary>
        public static int BotCount => botPlayers.Count;

        /// <summary>
        /// 判断指定玩家是否为假人。
        /// </summary>
        public static bool IsBot(PlayerObject player) => player != null && botPlayers.Contains(player);

        /// <summary>
        /// 假人账号列表
        /// </summary>
        public static List<BotAccountInfo> BotAccounts => botAccounts;

        /// <summary>
        /// 假人玩家列表
        /// </summary>
        public static List<PlayerObject> BotPlayers => botPlayers;

        private sealed class BotManualMapSwitchCandidate
        {
            public Map Map;
            public Point Point;
            public int Score;
            public int Danger;
        }

        public sealed class BotManualLevelRangeRequest
        {
            public string Text;
            public int MinLevel;
            public int MaxLevel;
        }

        public sealed class BotForceSwitchRangeSummary
        {
            public string RangeText;
            public int MatchedCount;
            public int SwitchedCount;
            public int BlockedByHumanGroup;
            public int BlockedByConquestWar;
            public int NoCandidateCount;
            public int TeamCount;
            public int TeamMemberCount;
            public int RemainingSoloCount;
            public string TeamLeaderNames;
            public string TargetMapName;
            public int TargetMapIndex = -1;
        }

        private sealed class BotForceGroupRebuildResult
        {
            public int TeamCount;
            public int MemberCount;
            public int SoloCount;
            public List<string> LeaderNames = new List<string>();
        }


        public sealed class BotForceSwitchAllRangesResult
        {
            public bool TimedOut;
            public string ErrorMessage;
            public bool GroupRebuildTriggered;
            public List<BotForceSwitchRangeSummary> Summaries = new List<BotForceSwitchRangeSummary>();
        }


        private enum BotManualMapSwitchBlockReason
        {
            None,
            HumanLeader,
            ConquestWar,
            LowHealth,
            PickingUp,
            InCombat,
        }

        private enum BotForceLevelRangeSwitchBlockReason
        {
            None,
            HumanGroup,
            ConquestWar,
        }

        private static bool IsBotLevelInManualRange(int level, int minLevel, int maxLevel)
        {
            return level >= minLevel && (maxLevel == int.MaxValue || level <= maxLevel);
        }

        private static string GetBotManualRangeText(int minLevel, int maxLevel)
        {
            return maxLevel == int.MaxValue
                ? $"{minLevel}级以上"
                : $"{minLevel}-{maxLevel}级";
        }

        private static BotManualMapSwitchBlockReason GetBotManualMapSwitchBlockReason(PlayerObject player)
        {
            if (player?.Node == null || player.Dead || player.CurrentMap == null)
                return BotManualMapSwitchBlockReason.None;

            GetBotGroupLeaderContext(player, out PlayerObject groupLeader, out bool hasHumanLeader);
            if (hasHumanLeader && groupLeader != null)
                return BotManualMapSwitchBlockReason.HumanLeader;

            if (GetBotActiveConquestWar(player) != null || player.IsWarPartake())
                return BotManualMapSwitchBlockReason.ConquestWar;

            int maxHP = Math.Max(1, player.Stats[Stat.Health]);
            long hpPct = player.CurrentHP * 100L / maxHP;
            if (hpPct < BotFleeHpPct)
                return BotManualMapSwitchBlockReason.LowHealth;

            if (_botWaitingPickup.ContainsKey(player.ObjectID))
                return BotManualMapSwitchBlockReason.PickingUp;

            if (_botTargetItems.TryGetValue(player.ObjectID, out ItemObject targetItem)
                && IsValidBotPickupTarget(player, targetItem))
                return BotManualMapSwitchBlockReason.PickingUp;

            if (_botTargets.TryGetValue(player.ObjectID, out MapObject target)
                && target != null
                && target.Node != null
                && !target.Dead
                && target.CurrentMap == player.CurrentMap
                && player.CanAttackTarget(target))
                return BotManualMapSwitchBlockReason.InCombat;

            if (player.PacketWaiting || (player.ActionList?.Count ?? 0) > 0)
                return BotManualMapSwitchBlockReason.InCombat;

            return BotManualMapSwitchBlockReason.None;
        }

        private static string GetBotManualMapSwitchBlockReasonText(BotManualMapSwitchBlockReason reason)
        {
            switch (reason)
            {
                case BotManualMapSwitchBlockReason.HumanLeader:
                    return "真人带队保护";
                case BotManualMapSwitchBlockReason.ConquestWar:
                    return "城战/攻城中保护";
                case BotManualMapSwitchBlockReason.LowHealth:
                    return "低血保护";
                case BotManualMapSwitchBlockReason.PickingUp:
                    return "拾取中保护";
                case BotManualMapSwitchBlockReason.InCombat:
                    return "战斗中保护";
                default:
                    return string.Empty;
            }
        }

        public static string GetBotManualMapSwitchBlockedReason(PlayerObject player)
        {
            return GetBotManualMapSwitchBlockReasonText(GetBotManualMapSwitchBlockReason(player));
        }

        public static bool IsBotManualMapSwitchBlocked(PlayerObject player)
        {
            return GetBotManualMapSwitchBlockReason(player) != BotManualMapSwitchBlockReason.None;
        }

        private static BotForceLevelRangeSwitchBlockReason GetBotForceLevelRangeSwitchBlockReason(PlayerObject player)
        {
            if (player?.Node == null || player.Dead || player.CurrentMap == null)
                return BotForceLevelRangeSwitchBlockReason.None;

            if (player.GroupMembers != null)
            {
                foreach (PlayerObject member in player.GroupMembers)
                {
                    if (member != null && !botPlayers.Contains(member))
                        return BotForceLevelRangeSwitchBlockReason.HumanGroup;
                }
            }

            if (GetBotActiveConquestWar(player) != null || player.IsWarPartake())
                return BotForceLevelRangeSwitchBlockReason.ConquestWar;

            return BotForceLevelRangeSwitchBlockReason.None;
        }

        private static string GetBotForceLevelRangeSwitchBlockReasonText(BotForceLevelRangeSwitchBlockReason reason)
        {
            switch (reason)
            {
                case BotForceLevelRangeSwitchBlockReason.HumanGroup:
                    return "真人队伍中保护";
                case BotForceLevelRangeSwitchBlockReason.ConquestWar:
                    return "城战/攻城中保护";
                default:
                    return string.Empty;
            }
        }

        public static string GetBotForceLevelRangeSwitchBlockedReason(PlayerObject player)
        {
            return GetBotForceLevelRangeSwitchBlockReasonText(GetBotForceLevelRangeSwitchBlockReason(player));
        }

        private static bool TryFindRandomMapForManualSwitch(PlayerObject player, int minLevel, int maxLevel, out Map map, out Point point)
        {
            map = null;
            point = Point.Empty;
            if (player?.CurrentMap == null) return false;

            GetBotGoldFarmContext(player, out bool goldFarmMode, out bool emergencyGoldFarmMode);
            List<BotManualMapSwitchCandidate> candidates = new List<BotManualMapSwitchCandidate>();

            foreach (KeyValuePair<MapInfo, Map> kv in SEnvir.Maps)
            {
                Map candidateMap = kv.Value;
                if (candidateMap == null || candidateMap == player.CurrentMap) continue;

                int avgMonsterLevel;
                int dangerScore;
                int score = GetBotMapScore(candidateMap, player, goldFarmMode, emergencyGoldFarmMode, out avgMonsterLevel, out dangerScore);
                if (score == int.MinValue) continue;
                if (!IsBotLevelInManualRange(avgMonsterLevel, minLevel, maxLevel)) continue;

                Point dest = GetBotPreferredProgressionPoint(candidateMap, player);
                if (dest == Point.Empty)
                    dest = GetRandomWalkablePoint(candidateMap);
                if (dest == Point.Empty) continue;

                candidates.Add(new BotManualMapSwitchCandidate
                {
                    Map = candidateMap,
                    Point = dest,
                    Score = score,
                    Danger = dangerScore,
                });
            }

            if (candidates.Count == 0)
                return TryFindMonsterRangeFallbackMapForManualSwitch(player, minLevel, maxLevel, out map, out point);

            int bestScore = candidates.Max(x => x.Score);
            List<BotManualMapSwitchCandidate> shortlist = candidates
                .Where(x => x.Score >= bestScore - 180)
                .OrderByDescending(x => x.Score)
                .ThenBy(x => x.Danger)
                .Take(6)
                .ToList();

            if (shortlist.Count == 0)
                shortlist = candidates.OrderByDescending(x => x.Score).ThenBy(x => x.Danger).Take(6).ToList();

            BotManualMapSwitchCandidate selected = shortlist[_botRandom.Next(shortlist.Count)];
            map = selected.Map;
            point = selected.Point;
            return true;
        }

        private static bool TryFindMonsterRangeFallbackMapForManualSwitch(PlayerObject player, int minLevel, int maxLevel, out Map map, out Point point)
        {
            map = null;
            point = Point.Empty;
            if (player?.CurrentMap == null) return false;

            List<BotManualMapSwitchCandidate> candidates = BuildMonsterRangeFallbackMapCandidates(new List<PlayerObject> { player }, minLevel, maxLevel);
            if (candidates.Count == 0)
                return false;

            int bestScore = candidates.Max(x => x.Score);
            List<BotManualMapSwitchCandidate> shortlist = candidates
                .Where(x => x.Score >= bestScore - 120)
                .OrderByDescending(x => x.Score)
                .ThenBy(x => x.Danger)
                .Take(6)
                .ToList();

            if (shortlist.Count == 0)
                shortlist = candidates.OrderByDescending(x => x.Score).ThenBy(x => x.Danger).Take(6).ToList();

            BotManualMapSwitchCandidate selected = shortlist[_botRandom.Next(shortlist.Count)];
            map = selected.Map;
            point = selected.Point;
            return true;
        }

        private static string GetBotSwitchMapDisplayName(Map map)

        {
            if (map?.Info == null)
                return "无";

            return string.IsNullOrWhiteSpace(map.Info.Description)
                ? $"MapIndex={map.Info.Index}"
                : $"{map.Info.Description} (Index={map.Info.Index})";
        }

        private static bool TryFindSharedMapForForcedLevelRangeSwitch(List<PlayerObject> players, int minLevel, int maxLevel, out Map map, out Point point)
        {
            map = null;
            point = Point.Empty;
            if (players == null || players.Count == 0) return false;

            foreach (PlayerObject player in players
                .Where(p => p?.Node != null && !p.Dead && p.CurrentMap != null)
                .OrderBy(p => p.Level)
                .ThenBy(p => p.CurrentHP))
            {
                if (TryFindRandomMapForManualSwitch(player, minLevel, maxLevel, out map, out point))
                    return true;
            }

            return TryFindMonsterRangeFallbackMapForForcedLevelRangeSwitch(players, minLevel, maxLevel, out map, out point);
        }

        private static List<BotManualMapSwitchCandidate> BuildMonsterRangeFallbackMapCandidates(List<PlayerObject> players, int minLevel, int maxLevel)
        {
            List<PlayerObject> validPlayers = players?
                .Where(p => p?.Node != null && !p.Dead && p.CurrentMap != null)
                .Distinct()
                .ToList() ?? new List<PlayerObject>();

            List<BotManualMapSwitchCandidate> candidates = new List<BotManualMapSwitchCandidate>();
            if (validPlayers.Count == 0)
                return candidates;

            int rangeCenter = maxLevel == int.MaxValue
                ? Math.Max(minLevel, minLevel + 5)
                : (minLevel + maxLevel) / 2;

            foreach (KeyValuePair<MapInfo, Map> kv in SEnvir.Maps)
            {
                Map candidateMap = kv.Value;
                if (candidateMap?.Info == null) continue;
                if (validPlayers.Any(player => candidateMap == player.CurrentMap)) continue;
                if (candidateMap.Info.IsDynamic || candidateMap.Info.BanAndroidPlayer) continue;
                if (MapHasBoss(candidateMap)) continue;

                BotMapMonsterProfile profile;
                if (!TryGetMapMonsterProfile(candidateMap, out profile)) continue;
                if (!IsBotLevelInManualRange(profile.AverageLevel, minLevel, maxLevel)) continue;

                Point dest = Point.Empty;
                foreach (PlayerObject player in validPlayers.OrderByDescending(x => x.Level))
                {
                    dest = GetBotPreferredProgressionPoint(candidateMap, player);
                    if (dest == Point.Empty)
                        dest = GetRandomWalkablePoint(candidateMap);
                    if (dest != Point.Empty)
                        break;
                }

                if (dest == Point.Empty) continue;

                int bestSafeScore = int.MinValue;
                int bestDanger = int.MaxValue;
                foreach (PlayerObject player in validPlayers)
                {
                    GetBotGoldFarmContext(player, out bool goldFarmMode, out bool emergencyGoldFarmMode);
                    int dangerScore;
                    int avgMonsterLevel;
                    int safeScore = GetBotMapScore(candidateMap, player, goldFarmMode, emergencyGoldFarmMode, out avgMonsterLevel, out dangerScore);
                    if (safeScore == int.MinValue) continue;

                    if (safeScore > bestSafeScore)
                        bestSafeScore = safeScore;
                    if (dangerScore < bestDanger)
                        bestDanger = dangerScore;
                }

                int score = Math.Max(0, 500 - Math.Abs(profile.AverageLevel - rangeCenter) * 20)
                            + Math.Max(1, Math.Max(candidateMap.Info.ExperienceRate, candidateMap.Info.MaxExperienceRate)) / 8
                            + Math.Max(1, Math.Max(candidateMap.Info.DropRate, candidateMap.Info.MaxDropRate)) / 16
                            + Math.Min(80, profile.Count / 2);

                if (bestSafeScore != int.MinValue)
                    score += Math.Max(0, bestSafeScore / 4);

                candidates.Add(new BotManualMapSwitchCandidate
                {
                    Map = candidateMap,
                    Point = dest,
                    Score = score,
                    Danger = bestDanger == int.MaxValue ? 999999 : bestDanger,
                });
            }

            return candidates;
        }

        private static bool TryFindMonsterRangeFallbackMapForForcedLevelRangeSwitch(List<PlayerObject> players, int minLevel, int maxLevel, out Map map, out Point point)
        {
            map = null;
            point = Point.Empty;

            List<BotManualMapSwitchCandidate> candidates = BuildMonsterRangeFallbackMapCandidates(players, minLevel, maxLevel);
            if (candidates.Count == 0)
                return false;

            BotManualMapSwitchCandidate selected = candidates
                .OrderByDescending(x => x.Score)
                .ThenBy(x => x.Danger)
                .First();

            map = selected.Map;
            point = selected.Point;
            return true;
        }

        private static void PrepareBotForForcedLevelRangeSwitch(PlayerObject player)


        {
            if (player == null) return;

            uint pid = player.ObjectID;

            if (player.GroupInvitation != null)
                player.GroupInvitation = null;

            if (player.GroupMembers != null && IsBotOnlyGroup(player))
            {
                try
                {
                    player.GroupLeave();
                }
                catch (Exception)
                {
                }
            }

            ClearBotPendingCombatActions(player);
            ClearBotUpcomingHighBossGroupTarget(player);
            _botHumanInviteCooldown.Remove(pid);
            _botRecallUntil.Remove(pid);
            _botTargets.Remove(pid);
            _botTargetSwitchTime.Remove(pid);
            _botTargetItems.Remove(pid);
            _botWaitingPickup.Remove(pid);
            _botKiteMode.Remove(pid);
            _botRoamDir.Remove(pid);
            _botRoamTime.Remove(pid);
            _botLastSnapPos.Remove(pid);
            _botLastSnapTime.Remove(pid);
            _botDriftAnchorPos.Remove(pid);
            _botDriftAnchorTime.Remove(pid);
            ClearBotSiegeState(pid);
        }

        private static List<PlayerObject> BuildBotForcedGroupMembers(List<PlayerObject> pool)
        {
            // 强制组队也要使用权重随机选择模式，避免总是倾向组满
            // 直接复用 BuildBotAutoGroupMembers，它已经包含了权重逻辑
            return BuildBotAutoGroupMembers(pool);
        }

        private static BotForceGroupRebuildResult ForceRebuildBotGroupsForLevelRange(List<PlayerObject> players)
        {
            BotForceGroupRebuildResult result = new BotForceGroupRebuildResult();

            if (!Config.BotAllowGroup || players == null || players.Count < 2)
                return result;

            List<PlayerObject> rebuildPlayers = players
                .Where(p => p?.Node != null && !p.Dead)
                .Distinct()
                .ToList();

            foreach (PlayerObject player in rebuildPlayers)
            {
                if (!player.Character.Account.AllowGroup)
                    player.GroupSwitch(true);

                if (player.GroupInvitation != null)
                    player.GroupInvitation = null;

                // 强制重组时，所有假人-only队伍都需要离队
                // 不管是不是队长，只要在假人-only队伍里就离队
                bool needLeave = player.GroupMembers != null && IsBotOnlyGroup(player);
                // SEnvir.Log($"假人强制按档重组检查 [{player.Name}]: GroupMembers={(player.GroupMembers != null ? player.GroupMembers.Count : 0)}, NeedLeave={needLeave}");

                if (needLeave)
                {
                    try
                    {
                        player.GroupLeave();
                        // SEnvir.Log($"假人强制按档重组离队 [{player.Name}]");
                    }
                    catch (Exception ex)
                    {
                        SEnvir.Log($"假人强制按档重组离队异常 [{player.Name}]: {ex.Message}");
                    }
                }
            }

            List<PlayerObject> freeBots = rebuildPlayers
                .Where(p => p?.Node != null
                            && !p.Dead
                            && p.GroupMembers == null
                            && p.GroupInvitation == null)
                .ToList();

            // SEnvir.Log($"假人强制按档重组: 总数={rebuildPlayers.Count}, freeBots={freeBots.Count}");

                while (freeBots.Count > 0)
                {
                    List<PlayerObject> team = BuildBotForcedGroupMembers(freeBots);
                    if (team == null || team.Count == 0)
                        break;

                    // SEnvir.Log($"假人强制重组: 剩余={freeBots.Count}人, 本次组队={team.Count}人, 队长={team[0]?.Name}");

                    foreach (PlayerObject member in team)
                        freeBots.Remove(member);

                if (team.Count < 2)
                    continue;

                PlayerObject leader = team[0];
                if (leader?.Node == null || leader.Dead || leader.GroupMembers != null || leader.GroupInvitation != null)
                    continue;

                for (int i = 1; i < team.Count; i++)
                {
                    PlayerObject target = team[i];
                    if (target?.Node == null || target.Dead) continue;
                    if (target.GroupMembers != null || target.GroupInvitation != null) continue;

                    try
                    {
                        // SEnvir.Log($"[强制按档重组] 队长={leader.Name}, 邀请={target.Name}, 队伍人数={team.Count}");
                        leader.GroupInvite(target.Name);

                        if (target.GroupInvitation == leader)
                            target.GroupJoin();
                    }
                    catch (Exception ex)
                    {
                        SEnvir.Log($"假人强制按档重组异常 [{leader.Name}→{target.Name}]: {ex.Message}");
                    }
                    finally
                    {
                        if (target.GroupInvitation == leader)
                            target.GroupInvitation = null;
                    }
                }

                if (leader.GroupMembers != null && leader.GroupMembers.Count >= 2)
                {
                    result.TeamCount++;
                    result.MemberCount += leader.GroupMembers.Count;
                    result.LeaderNames.Add(leader.Name);
                }
            }

            result.SoloCount = rebuildPlayers.Count(player => player?.Node != null
                                                       && !player.Dead
                                                       && (player.GroupMembers == null || player.GroupMembers.Count < 2));

            return result;
        }




        public static BotForceSwitchAllRangesResult ForceSwitchOnlineBotsByLevelRangesAndRebuild(List<BotManualLevelRangeRequest> requests, int waitMilliseconds = 8000)
        {
            BotForceSwitchAllRangesResult result = new BotForceSwitchAllRangesResult();

            if (!isRunning)
            {
                result.ErrorMessage = "假人系统未运行。";
                return result;
            }

            List<BotManualLevelRangeRequest> normalizedRequests = requests?
                .Where(x => x != null)
                .Select(x => new BotManualLevelRangeRequest
                {
                    Text = string.IsNullOrWhiteSpace(x.Text) ? GetBotManualRangeText(Math.Max(0, x.MinLevel), x.MaxLevel < x.MinLevel ? int.MaxValue : x.MaxLevel) : x.Text,
                    MinLevel = Math.Max(0, x.MinLevel),
                    MaxLevel = x.MaxLevel < x.MinLevel ? int.MaxValue : x.MaxLevel,
                })
                .OrderBy(x => x.MinLevel)
                .ToList();

            if (normalizedRequests == null || normalizedRequests.Count == 0)
            {
                result.ErrorMessage = "没有可执行的等级档位。";
                return result;
            }

            using (ManualResetEventSlim waitHandle = new ManualResetEventSlim(false))
            {
                SEnvir.BotActionQueue.Enqueue(() =>
                {
                    try
                    {
                        result.Summaries = ExecuteForceSwitchOnlineBotsByLevelRangesAndRebuild(normalizedRequests, out bool groupRebuildTriggered);
                        result.GroupRebuildTriggered = groupRebuildTriggered;
                    }
                    catch (Exception ex)
                    {
                        result.ErrorMessage = ex.Message;
                        SEnvir.Log($"假人强制一键按档切图异常: {ex.Message}");
                    }
                    finally
                    {
                        waitHandle.Set();
                    }
                });

                if (!waitHandle.Wait(Math.Max(1000, waitMilliseconds)))
                {
                    result.TimedOut = true;
                    result.ErrorMessage = "等待假人强制一键按档切图结果超时，请稍后查看日志。";
                }
            }

            return result;
        }

        private static List<BotForceSwitchRangeSummary> ExecuteForceSwitchOnlineBotsByLevelRangesAndRebuild(List<BotManualLevelRangeRequest> requests, out bool groupRebuildTriggered)
        {
            groupRebuildTriggered = false;
            List<BotForceSwitchRangeSummary> summaries = new List<BotForceSwitchRangeSummary>();

            if (requests == null || requests.Count == 0)
                return summaries;

            _botGroupRebuildPending = false;
            _botNextGroupRebuildTime = DateTime.MinValue;

            DateTime now = SEnvir.Now;
            SetBotAutoGroupRebuildLock(now.AddSeconds(BotAutoGroupRebuildLockSeconds));

            foreach (BotManualLevelRangeRequest request in requests)
            {
                BotForceSwitchRangeSummary summary = new BotForceSwitchRangeSummary
                {
                    RangeText = string.IsNullOrWhiteSpace(request.Text)
                        ? GetBotManualRangeText(request.MinLevel, request.MaxLevel)
                        : request.Text,
                };

                List<PlayerObject> matchedPlayers = botPlayers
                    .Where(player => player != null
                                     && player.Node != null
                                     && !player.Dead
                                     && player.CurrentMap != null
                                     && IsBotLevelInManualRange(player.Level, request.MinLevel, request.MaxLevel))
                    .ToList();

                summary.MatchedCount = matchedPlayers.Count;

                List<PlayerObject> eligiblePlayers = new List<PlayerObject>();
                foreach (PlayerObject player in matchedPlayers)
                {
                    switch (GetBotForceLevelRangeSwitchBlockReason(player))
                    {
                        case BotForceLevelRangeSwitchBlockReason.HumanGroup:
                            summary.BlockedByHumanGroup++;
                            continue;
                        case BotForceLevelRangeSwitchBlockReason.ConquestWar:
                            summary.BlockedByConquestWar++;
                            continue;
                        default:
                            eligiblePlayers.Add(player);
                            break;
                    }
                }

                if (eligiblePlayers.Count == 0)
                {
                    summaries.Add(summary);
                    continue;
                }

                if (!TryFindSharedMapForForcedLevelRangeSwitch(eligiblePlayers, request.MinLevel, request.MaxLevel, out Map targetMap, out Point targetPoint))
                {
                    summary.NoCandidateCount = eligiblePlayers.Count;
                    summaries.Add(summary);
                    continue;
                }

                summary.TargetMapName = GetBotSwitchMapDisplayName(targetMap);
                summary.TargetMapIndex = targetMap?.Info?.Index ?? -1;

                List<PlayerObject> switchedPlayers = new List<PlayerObject>();
                foreach (PlayerObject player in eligiblePlayers)
                {
                    uint pid = player.ObjectID;
                    PrepareBotForForcedLevelRangeSwitch(player);

                    Point dest = targetPoint;
                    if (targetMap != null)
                    {
                        Point spreadPoint = targetMap.GetRandomLocation(targetPoint, 3, 18);
                        if (spreadPoint != Point.Empty)
                            dest = spreadPoint;
                    }

                    if (!player.Teleport(targetMap, dest))
                        continue;

                    RecordBotMapSwitch(player, targetMap);
                    ResetBotMapStayState(player, targetMap, now);
                    SetBotUpcomingHighBossGroupTarget(player, targetMap);
                    SetBotForcedGroupLock(player, now.AddSeconds(BotForcedGroupLockSeconds));
                    _botLastAttackTime[pid] = now;
                    GetBotGoldFarmContext(player, out bool goldFarmMode, out bool _);
                    _botMapEvalTime[pid] = now.AddSeconds(goldFarmMode ? BotGoldFarmMapEvalInterval : BotMapEvalInterval);
                    switchedPlayers.Add(player);
                }

                summary.SwitchedCount = switchedPlayers.Count;
                if (switchedPlayers.Count > 0)
                {
                    BotForceGroupRebuildResult rebuildResult = ForceRebuildBotGroupsForLevelRange(switchedPlayers);
                    summary.TeamCount = rebuildResult.TeamCount;
                    summary.TeamMemberCount = rebuildResult.MemberCount;
                    summary.RemainingSoloCount = rebuildResult.SoloCount;
                    summary.TeamLeaderNames = rebuildResult.LeaderNames.Count > 0
                        ? string.Join("、", rebuildResult.LeaderNames)
                        : null;
                    groupRebuildTriggered |= summary.TeamCount > 0;
                }


                summaries.Add(summary);
            }

            // SEnvir.Log("假人强制一键按档切图完成：" + string.Join("；", summaries.Select(summary =>
            // {
            //     List<string> extra = new List<string>
            //     {
            //         $"切图={summary.SwitchedCount}",
            //         $"目标={summary.TargetMapName ?? "无"}",
            //         $"真人队伍保护={summary.BlockedByHumanGroup}",
            //         $"城战/攻城保护={summary.BlockedByConquestWar}",
            //         $"无地图={summary.NoCandidateCount}",
            //         $"实际成队={summary.TeamCount}队/{summary.TeamMemberCount}人",
            //         $"剩余单人={summary.RemainingSoloCount}"
            //     };
            //
            //     if (!string.IsNullOrWhiteSpace(summary.TeamLeaderNames))
            //         extra.Add($"队长={summary.TeamLeaderNames}");
            //
            //
            //     return $"{summary.RangeText}: {string.Join(", ", extra)}";
            // })));

            return summaries;
        }


        public static BotBatchResult SwitchOnlineBotsMapByLevelRange(int minLevel, int maxLevel)
        {
            if (!isRunning)
            {
                // SEnvir.Log("假人切图：假人系统未运行，操作取消");
                return new BotBatchResult { Failed = 1, ErrorMessage = "假人系统未运行" };
            }

            int normalizedMin = Math.Max(0, minLevel);
            int normalizedMax = maxLevel < normalizedMin ? int.MaxValue : maxLevel;
            string rangeText = GetBotManualRangeText(normalizedMin, normalizedMax);
            BotBatchResult result = new BotBatchResult
            {
                Queued = SnapshotBotPlayers().Length,
            };

            // SEnvir.Log($"假人切图：收到按档随机切图指令，档位={rangeText}，当前在线假人数={botPlayers.Count}，将在下次 BotTick 执行");
            using (ManualResetEventSlim waitHandle = new ManualResetEventSlim(false))
            {
                SEnvir.BotActionQueue.Enqueue(() =>
                {
                    try
                    {
                        ExecuteSwitchOnlineBotsMapByLevelRange(normalizedMin, normalizedMax, result);
                    }
                    catch (Exception ex)
                    {
                        result.Failed++;
                        result.ErrorMessage = ex.Message;
                        RecordManagementLog(BotLogKind.Operation, "按档切图执行失败: " + ex.Message);
                    }
                    finally
                    {
                        waitHandle.Set();
                    }
                });

                if (!waitHandle.Wait(8000))
                {
                    result.Timeout = 1;
                    result.ErrorMessage = "等待按档切图结果超时，请稍后查看操作日志";
                }
            }

            RecordManagementLog(BotLogKind.Operation,
                "GM 按档切图 " + rangeText + "：成功 " + result.Succeeded
                + "，保护 " + result.Protected + "，跳过 " + result.Skipped
                + "，失败 " + result.Failed + "，超时 " + result.Timeout);
            return result;
        }

        private static void ExecuteSwitchOnlineBotsMapByLevelRange(int minLevel, int maxLevel, BotBatchResult result)
        {
            if (botPlayers.Count == 0)
            {
                // SEnvir.Log("假人切图：当前没有在线假人，跳过执行");
                result.Skipped = 1;
                return;
            }

            DateTime now = SEnvir.Now;
            int matched = 0;
            int switched = 0;
            int skipped = 0;
            int protectedByHumanLeader = 0;
            int protectedByConquestWar = 0;
            int protectedByLowHealth = 0;
            int protectedByPickup = 0;
            int protectedByCombat = 0;
            int noCandidate = 0;
            int failed = 0;
            string rangeText = GetBotManualRangeText(minLevel, maxLevel);

            foreach (PlayerObject player in SnapshotBotPlayers())
            {
                try
                {
                    if (player == null || player.Node == null || player.Dead || player.CurrentMap == null)
                    {
                        skipped++;
                        continue;
                    }

                    if (!IsBotLevelInManualRange(player.Level, minLevel, maxLevel))
                        continue;

                    matched++;

                    BotManualMapSwitchBlockReason blockReason = GetBotManualMapSwitchBlockReason(player);
                    switch (blockReason)
                    {
                        case BotManualMapSwitchBlockReason.HumanLeader:
                            protectedByHumanLeader++;
                            skipped++;
                            continue;
                        case BotManualMapSwitchBlockReason.ConquestWar:
                            protectedByConquestWar++;
                            skipped++;
                            continue;
                        case BotManualMapSwitchBlockReason.LowHealth:
                            protectedByLowHealth++;
                            skipped++;
                            continue;
                        case BotManualMapSwitchBlockReason.PickingUp:
                            protectedByPickup++;
                            skipped++;
                            continue;
                        case BotManualMapSwitchBlockReason.InCombat:
                            protectedByCombat++;
                            skipped++;
                            continue;
                    }

                    if (!TryFindRandomMapForManualSwitch(player, minLevel, maxLevel, out Map newMap, out Point dest))
                    {
                        noCandidate++;
                        skipped++;
                        continue;
                    }

                    uint pid = player.ObjectID;
                    ClearBotPendingCombatActions(player);
                    ClearBotUpcomingHighBossGroupTarget(player);
                    _botRecallUntil.Remove(pid);
                    _botTargets.Remove(pid);
                    _botTargetSwitchTime.Remove(pid);
                    _botTargetItems.Remove(pid);
                    _botWaitingPickup.Remove(pid);
                    _botKiteMode.Remove(pid);
                    _botRoamDir.Remove(pid);
                    _botRoamTime.Remove(pid);
                    _botLastSnapPos.Remove(pid);
                    _botLastSnapTime.Remove(pid);
                    _botDriftAnchorPos.Remove(pid);
                    _botDriftAnchorTime.Remove(pid);
                    ClearBotSiegeState(pid);

                    if (!player.Teleport(newMap, dest))
                    {
                        failed++;
                        continue;
                    }

                    RecordBotMapSwitch(player, newMap);
                    ResetBotMapStayState(player, newMap, now);
                    _botLastAttackTime[pid] = now;
                    GetBotGoldFarmContext(player, out bool goldFarmMode, out bool _);
                    _botMapEvalTime[pid] = now.AddSeconds(goldFarmMode ? BotGoldFarmMapEvalInterval : BotMapEvalInterval);
                    switched++;
                }
                catch (Exception)
                {
                    failed++;
                    // SEnvir.Log($"假人切图异常 [{player?.Name ?? "未知假人"}]: {ex.Message}");
                }
            }

            int protectedTotal = protectedByHumanLeader + protectedByConquestWar + protectedByLowHealth + protectedByPickup + protectedByCombat;
            result.Succeeded = switched;
            result.Failed = failed;
            result.Protected = protectedTotal;
            result.Skipped = Math.Max(0, skipped - protectedTotal);
            result.ErrorMessage = noCandidate > 0
                ? "部分假人没有找到符合条件的地图"
                : result.ErrorMessage;
            // SEnvir.Log($"假人切图完成：档位={rangeText}，命中={matched}，成功切图={switched}，真人带队保护={protectedByHumanLeader}，城战/攻城保护={protectedByConquestWar}，低血保护={protectedByLowHealth}，拾取中保护={protectedByPickup}，战斗中保护={protectedByCombat}，无合适地图={noCandidate}，其余跳过/失败={Math.Max(0, skipped - protectedTotal - noCandidate)}");
        }

        /// <summary>
        /// 将所有在线假人传送回道馆（地图 Index=<see cref="BotHomeMapIndex"/>，坐标 <see cref="BotHomePoint"/> 附近），
        /// 并冻结打怪升级行为 <see cref="BotRecallRestSeconds"/> 秒（默认2分钟）。
        /// 此方法线程安全：仅设置标志位，实际传送在 BotTick 主线程中执行。
        /// </summary>
        public static BotBatchResult RecallAllBots()
        {
            if (!isRunning)
            {
                // SEnvir.Log("假人回城：假人系统未运行，操作取消");
                return new BotBatchResult { Failed = 1, ErrorMessage = "假人系统未运行" };
            }

            PlayerObject[] players = SnapshotBotPlayers();
            if (players.Length == 0)
            {
                RecordManagementLog(BotLogKind.Operation, "GM 全员回城：当前没有在线假人");
                return new BotBatchResult { Skipped = 1 };
            }

            if (_pendingRecallAll)
            {
                return new BotBatchResult
                {
                    Skipped = players.Length,
                    ErrorMessage = "已有全员回城操作正在执行",
                };
            }

            _pendingRecallResult = new BotBatchResult { Queued = players.Length };
            _botRecallBatchOffset = 0;
            _botNextRecallBatchTime = DateTime.MinValue;
            _pendingRecallAll = true;
            RecordManagementLog(BotLogKind.Operation, "GM 已投递全员回城，数量: " + players.Length);
            return _pendingRecallResult;
        }

        /// <summary>
        /// 执行全体假人回城传送（在 BotTick 主线程环境中调用）。
        /// </summary>
        private static void ExecuteRecallAllBots()
        {
            if (!_pendingRecallAll)
            {
                _recallActionQueued = false;
                return;
            }

            BotBatchResult result = _pendingRecallResult ?? new BotBatchResult();

            PlayerObject[] players = SnapshotBotPlayers();
            if (players.Length == 0)
            {
                // SEnvir.Log("假人回城：当前没有在线假人，跳过传送");
                result.Skipped++;
                _pendingRecallAll = false;
                _recallActionQueued = false;
                return;
            }

            // 查找道馆地图
            Map homeMap = SEnvir.GetMap(BotHomeMapIndex);
            if (homeMap == null)
            {
                // SEnvir.Log($"假人回城失败：找不到地图 Index={BotHomeMapIndex}，" +
                //            $"请确认地图数据库中道馆的 Index 是否为 {BotHomeMapIndex}");
                result.Failed++;
                result.ErrorMessage = "找不到道馆地图";
                _pendingRecallAll = false;
                _recallActionQueued = false;
                return;
            }

            // SEnvir.Log($"假人回城：找到目标地图 [{homeMap.Info?.Description}] Index={BotHomeMapIndex}，" +
            //            $"目标坐标 {BotHomePoint}，开始传送 {botPlayers.Count} 名假人");

            DateTime now = SEnvir.Now;
            DateTime restUntil = now.AddSeconds(BotRecallRestSeconds);
            int batchSize = Math.Max(1, Math.Min(10000, Config.BotRecallBatchSize));
            int start = Math.Min(_botRecallBatchOffset, players.Length);
            int end = Math.Min(players.Length, start + batchSize);

            for (int index = start; index < end; index++)
            {
                PlayerObject player = players[index];
                try
                {
                    if (player == null) { result.Skipped++; continue; }
                    if (player.Node == null) { result.Skipped++; continue; }
                    if (player.Dead) { result.Skipped++; continue; }

                    // 在目标坐标附近随机散布（半径15格），避免堆叠
                    // 使用地图自带方法，只要格子可走即可，道馆全是安全区也能正常散布
                    Point dest = homeMap.GetRandomLocation(BotHomePoint, 15, 50);
                    if (dest == Point.Empty) dest = BotHomePoint; // 兜底

                    uint pid = player.ObjectID;

                    // 设置回城冻结时间
                    _botRecallUntil[pid] = restUntil;

                    // 重置战斗状态，避免回城后残留旧目标
                    _botTargets.Remove(pid);
                    _botTargetSwitchTime.Remove(pid);
                    _botRoamDir.Remove(pid);
                    _botRoamTime.Remove(pid);
                    _botLastSnapPos.Remove(pid);
                    _botLastSnapTime.Remove(pid);
                    _botDriftAnchorPos.Remove(pid);
                    _botDriftAnchorTime.Remove(pid);
                    _botLastAttackTime[pid] = SEnvir.Now;
                    // 回城后等1分钟再做地图评估
                    _botMapEvalTime[pid] = restUntil;

                    if (!player.Teleport(homeMap, dest))
                    {
                        result.Failed++;
                        continue;
                    }

                    RecordBotMapSwitch(player, homeMap);
                    result.Succeeded++;

                }
                catch (Exception)
                {
                    result.Failed++;
                }
            }

            _botRecallBatchOffset = end;
            if (end < players.Length)
            {
                _botNextRecallBatchTime = now.AddMilliseconds(Math.Max(1, Config.BotRecallBatchIntervalMs));
                _recallActionQueued = false;
                return;
            }

            _pendingRecallAll = false;
            _pendingRecallResult = null;
            _botRecallBatchOffset = 0;
            _botNextRecallBatchTime = DateTime.MinValue;
            _recallActionQueued = false;
            RecordManagementLog(BotLogKind.Operation,
                "GM 全员回城完成：成功 " + result.Succeeded + "，跳过 " + result.Skipped
                + "，失败 " + result.Failed);
        }

        // ══════════════════════════════════════════════════════════════════════
        //  特修系统：耐久低于50%自动特修装备
        // ══════════════════════════════════════════════════════════════════════

        /// <summary>
        /// 检查并修复耐久低于50%的装备（按NPC特修脚本逻辑）。
        /// </summary>
        private static void ProcessBotEquipmentRepair(PlayerObject player)
        {
            if (player == null || player.Dead || player.Node == null || !Config.BotAutoSpecialRepair) return;
            if (player.InSafeZone) return; // 安全区特修（避免战斗中频繁检查）

            uint pid = player.ObjectID;

            // 检查是否到了检查间隔
            if (_botLastEquipmentRepairCheckTime.TryGetValue(pid, out DateTime lastCheckTime))
            {
                if (SEnvir.Now < lastCheckTime.AddSeconds(BotEquipmentRepairCheckInterval))
                    return;
            }

            _botLastEquipmentRepairCheckTime[pid] = SEnvir.Now;

            // 检查所有装备槽的耐久度
            var equipmentSlots = new EquipmentSlot[]
            {
                EquipmentSlot.Weapon,
                EquipmentSlot.Armour,
                EquipmentSlot.Helmet,
                EquipmentSlot.Shoes,
                EquipmentSlot.Shield,
                EquipmentSlot.Necklace,
                EquipmentSlot.BraceletL,
                EquipmentSlot.BraceletR,
                EquipmentSlot.RingL,
                EquipmentSlot.RingR,
                EquipmentSlot.Torch,
                EquipmentSlot.Emblem
            };

            List<EquipmentSlot> needRepairSlots = new List<EquipmentSlot>();

            foreach (EquipmentSlot slot in equipmentSlots)
            {
                int slotIdx = (int)slot;
                UserItem item = player.Equipment[slotIdx];

                if (item == null) continue;
                if (item.Info == null) continue;

                // 检查装备是否支持修理
                if (!item.Info.CanRepair) continue;

                // 左戒指结婚戒指不能特修
                if (slot == EquipmentSlot.RingL && (item.Flags & UserItemFlags.Marriage) != UserItemFlags.Marriage)
                    continue;

                // 检查耐久是否低于配置阈值
                int thresholdPercent = Math.Max(0, Math.Min(100, Config.BotSpecialRepairThresholdPercent));
                if (item.CurrentDurability < item.MaxDurability * thresholdPercent / 100.0)
                {
                    needRepairSlots.Add(slot);
                }
            }

            // 如果没有需要修理的装备，直接返回
            if (needRepairSlots.Count == 0) return;

            // 计算总特修费用（按NPC脚本的1.5倍）
            long totalRepairCost = 0;
            foreach (EquipmentSlot slot in needRepairSlots)
            {
                int slotIdx = (int)slot;
                UserItem item = player.Equipment[slotIdx];
                if (item == null || item.Info == null) continue;

                long cost = item.RepairCost(true); // true = 特修（恢复到满）
                totalRepairCost += cost;
            }

            // 特修费用按NPC脚本的1.5倍
            long actualRepairCost = (long)(totalRepairCost * 1.5);

            // 检查金币是否足够
            if (player.Gold < actualRepairCost)
            {
                // 金币不足，不进行特修
                return;
            }

            // 扣除特修费用
            ChangeBotGoldSilently(player, -actualRepairCost);

            // 执行特修：将所有需要修理的装备恢复到满耐久
            foreach (EquipmentSlot slot in needRepairSlots)
            {
                int slotIdx = (int)slot;
                UserItem item = player.Equipment[slotIdx];
                if (item == null || item.Info == null) continue;

                // 恢复到满耐久
                item.CurrentDurability = item.MaxDurability;

                // 刷新耐久显示
                player.Enqueue(new S.ItemDurability
                {
                    GridType = GridType.Equipment,
                    Slot = slotIdx,
                    CurrentDurability = item.CurrentDurability
                });
            }

            // 刷新角色属性
            player.RefreshStats();

            // 发送系统提示
            if (player.Connection != null)
            {
                player.Connection.ReceiveChat($"已特修{needRepairSlots.Count}件装备，费用{actualRepairCost}金币", MessageType.System);
            }
        }

    }
}
