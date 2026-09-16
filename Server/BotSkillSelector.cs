using Library;
using Library.SystemModels;
using Server.DBModels;
using Server.Models;
using System;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;

namespace Server.Envir
{
    /// <summary>
    /// 假人技能选择器：支持基于伤害评估的智能技能选择
    /// </summary>
    internal static class BotSkillSelector
    {
        /// <summary>
        /// 怪物视觉颜色状态（模拟客户端渲染结果）
        /// </summary>
        private enum MonsterVisualState
        {
            Normal,     // 正常颜色（无中毒）
            RedPoison,  // 粉紫色（中红毒）
            GreenPoison // 绿色（中绿毒）
        }

        /// <summary>
        /// 获取怪物的视觉颜色状态（模拟客户端判断）
        /// 对应客户端 MapObject.cs 648-652 行的绘制逻辑
        /// </summary>
        private static MonsterVisualState GetMonsterVisualState(MapObject target)
        {
            if (target == null || target.Dead)
                return MonsterVisualState.Normal;

            // 优先级：绿毒 > 红毒（客户端绘制顺序：先红后绿，但绿毒会覆盖红毒的颜色）
            bool hasGreenPoison = (target.Poison & PoisonType.Green) != PoisonType.None;
            bool hasRedPoison   = (target.Poison & PoisonType.Red)   != PoisonType.None;

            if (hasGreenPoison)
                return MonsterVisualState.GreenPoison;  // 绿色
            else if (hasRedPoison)
                return MonsterVisualState.RedPoison;   // 粉紫色
            else
                return MonsterVisualState.Normal;      // 正常
        }
        private struct BotSkillSelectionCacheEntry
        {
            public uint TargetObjectID;
            public MagicType Skill;
        }

        /// <summary>
        /// 假人技能选择缓存：地图ID → 玩家ID → 技能类型（单攻/群攻）→ 当前目标的推荐技能。
        /// 目标改变时立即重新评估，避免换怪后继续沿用旧技能。
        /// </summary>
        private static readonly Dictionary<int, Dictionary<uint, Dictionary<bool, BotSkillSelectionCacheEntry>>> _botSkillSelectionCache
            = new Dictionary<int, Dictionary<uint, Dictionary<bool, BotSkillSelectionCacheEntry>>>();
        private static readonly MagicType[] WarriorChargedAttackPriority =
        {
            MagicType.FlamingSword,
            MagicType.BladeStorm,
            MagicType.MaelstromBlade,
        };
        private static readonly MagicType[] WarriorSingleTargetPriority =
        {
            MagicType.FlamingSword,
            MagicType.DestructiveSurge,
            MagicType.SwiftBlade,
            MagicType.Slaying,
            MagicType.Thrusting,
        };

        private static readonly MagicType[] WarriorAreaPriority =
        {
            MagicType.FlamingSword,
            MagicType.DestructiveSurge,
            MagicType.HalfMoon,
            MagicType.SwiftBlade,
            MagicType.Slaying,
            MagicType.Thrusting,
        };

        private static readonly MagicType[] WarriorAdaptivePhysicalSinglePriority =
        {
            MagicType.DestructiveSurge,
            MagicType.SwiftBlade,
            MagicType.Slaying,
            MagicType.Thrusting,
        };

        private static readonly MagicType[] WarriorAdaptivePhysicalAreaPriority =
        {
            MagicType.DestructiveSurge,
            MagicType.HalfMoon,
            MagicType.SwiftBlade,
            MagicType.Slaying,
            MagicType.Thrusting,
        };

        private static readonly MagicType[] WarriorFirePriority =
        {
            MagicType.FlamingSword,
        };

        private static readonly MagicType[] WarriorAdaptiveSingleFallback =
        {
            MagicType.FlamingSword,
            MagicType.DestructiveSurge,
            MagicType.SwiftBlade,
            MagicType.Slaying,
            MagicType.Thrusting,
        };

        private static readonly MagicType[] WarriorAdaptiveAreaFallback =
        {
            MagicType.FlamingSword,
            MagicType.DestructiveSurge,
            MagicType.HalfMoon,
            MagicType.SwiftBlade,
            MagicType.Slaying,
            MagicType.Thrusting,
        };

        private static readonly MagicType[] WizardRangedPriority =
        {
            MagicType.FireBall,
            MagicType.LightningBall,
            MagicType.IceBolt,
            MagicType.GustBlast,
            MagicType.AdamantineFireBall,
            MagicType.ThunderBolt,
            MagicType.Cyclone,
            MagicType.ScortchedEarth,
        };

        private static readonly MagicType[] WizardFirePriority =
        {
            MagicType.MeteorShower,
            MagicType.FireStorm,
            MagicType.ScortchedEarth,
            MagicType.AdamantineFireBall,
            MagicType.FireBall,
        };

        private static readonly MagicType[] WizardIcePriority =
        {
            MagicType.GreaterFrozenEarth,
            MagicType.FrozenEarth,
            MagicType.IceBlades,
            MagicType.IceBolt,
        };

        private static readonly MagicType[] WizardLightningPriority =
        {
            MagicType.JudgementOfHeaven,
            MagicType.ChainLightning,
            MagicType.LightningBeam,
            MagicType.ThunderBolt,
            MagicType.LightningBall,
        };

        private static readonly MagicType[] WizardWindPriority =
        {
            MagicType.Tempest,
            MagicType.Cyclone,
            MagicType.GustBlast,
        };

        private static readonly MagicType[] WizardAdaptiveFallback =
        {
            MagicType.MeteorShower,
            MagicType.FireStorm,
            MagicType.GreaterFrozenEarth,
            MagicType.JudgementOfHeaven,
            MagicType.ChainLightning,
            MagicType.LightningBeam,
            MagicType.Tempest,
            MagicType.ScortchedEarth,
            MagicType.FrozenEarth,
            MagicType.IceBlades,
            MagicType.AdamantineFireBall,
            MagicType.ThunderBolt,
            MagicType.Cyclone,
            MagicType.GustBlast,
            MagicType.FireBall,
            MagicType.LightningBall,
            MagicType.IceBolt,
        };

        // 施毒技能优先级（按目标数量选择）
        // 单体施毒：施毒术（PoisonDust）
        // 群体施毒：施毒大法（GreaterPoisonDust）
        // 毒的类型由装备槽药粉 Shape 决定：Shape=1 黄色药粉 → 红毒，Shape=0 灰色药粉 → 绿毒
        private static readonly MagicType[] TaoistSinglePoisonPriority =
        {
            MagicType.PoisonDust,  // 施毒术（单体）
        };

        private static readonly MagicType[] TaoistMassPoisonPriority =
        {
            MagicType.GreaterPoisonDust,  // 施毒大法（群体）
        };

        // 所有施毒技能（用于自适应选择）
        private static readonly MagicType[] TaoistAllPoisonPriority =
        {
            MagicType.GreaterPoisonDust,
            MagicType.PoisonDust,
        };

        // 道士远程攻击技能（符咒类，按经济性选择）
        // 单体攻击：灵魂火符、月魂断玉、月魂灵波
        // 群体攻击：灭魂火符、吸星大法、迷魂大法
        private static readonly MagicType[] TaoistRangedPriority =
        {
            MagicType.ExplosiveTalisman,           // 灵魂火符（单体）
            MagicType.EvilSlayer,                 // 月魂断玉（单体）
            MagicType.GreaterEvilSlayer,           // 月魂灵波（单体）
            MagicType.ImprovedExplosiveTalisman,    // 灭魂火符（群体）
            MagicType.LifeSteal,                  // 吸星大法（群体）
            MagicType.Scarecrow,                  // 迷魂大法（群体）
        };

        // 道士近战物理技能
        // 单体攻击：空拳刀法
        // 群体攻击：横扫千军
        private static readonly MagicType[] TaoistMeleePriority =
        {
            MagicType.TaoistCombatKick,  // 空拳刀法（单体）
            MagicType.ThunderKick,        // 横扫千军（群体）
        };

        // 道士召唤宝宝技能（均为单体召唤）
        private static readonly MagicType[] TaoistSummonPriority =
        {
            MagicType.SummonSkeleton,       // 召唤骷髅（单体）
            MagicType.SummonShinsu,        // 召唤神兽（单体）
            MagicType.SummonJinSkeleton,    // 超强召唤骷髅（单体）
            MagicType.SummonDemonicCreature, // 焰魔召唤术（单体）
        };

        // 道士增加防御技能
        // 群体Buff：幽灵盾、神圣战甲术、强魔震法、猛虎强势
        // 单体Buff：阴阳法环、养生术
        private static readonly MagicType[] TaoistDefensePriority =
        {
            MagicType.MagicResistance,           // 幽灵盾（群体）
            MagicType.Resilience,                // 神圣战甲术（群体）
            MagicType.ElementalSuperiority,      // 强魔震法（群体）
            MagicType.BloodLust,                 // 猛虎强势（群体）
            MagicType.CelestialLight,            // 阴阳法环（单体）
            MagicType.EmpoweredHealing,          // 养生术（单体）
        };

        // 道士限制/削弱技能
        // 单体限制：施毒术、困魔咒、移花接玉
        // 群体限制：施毒大法、云寂术
        private static readonly MagicType[] TaoistDebuffPriority =
        {
            MagicType.PoisonDust,               // 施毒术（单体）
            MagicType.TrapOctagon,             // 困魔咒（单体）
            MagicType.GreaterPoisonDust,        // 施毒大法（群体）
            MagicType.Purification,            // 云寂术（群体）
            MagicType.StrengthOfFaith,         // 移花接玉（单体）
        };

        // 道士解负面状态技能
        // 群体解负面：云寂术
        // 单体解负面：魔焰强解术、回生术（部分版本可解负面）
        private static readonly MagicType[] TaoistPurgePriority =
        {
            MagicType.Purification,            // 云寂术（群体解负面）
            MagicType.DemonExplosion,         // 魔焰强解术（单体）
            MagicType.Resurrection,            // 回生术（单体，部分版本可解负面）
        };

        // 道士救人技能
        private static readonly MagicType[] TaoistRevivePriority =
        {
            MagicType.Resurrection,         // 回生术
        };

        // 道士治疗技能
        // 单体治疗：治愈术
        // 群体治疗：群体治愈术
        private static readonly MagicType[] TaoistHealPriority =
        {
            MagicType.Heal,              // 治愈术（单体）
            MagicType.MassHeal,          // 群体治愈术（群体）
        };

        // 道士特殊状态技能
        // 单体状态：隐身术、妙影无踪
        // 群体状态：集体隐身术
        // 注意：心灵启示技能在当前版本中未找到
        private static readonly MagicType[] TaoistStealthPriority =
        {
            MagicType.Invisibility,              // 隐身术（单体）
            MagicType.MassInvisibility,         // 集体隐身术（群体）
            MagicType.Transparency,             // 妙影无踪（单体）
        };

        private static readonly MagicType[] TaoistFirePriority =
        {
            MagicType.ImprovedExplosiveTalisman,
            MagicType.ExplosiveTalisman,
        };

        private static readonly MagicType[] TaoistHolyPriority =
        {
            MagicType.GreaterHolyStrike,
            MagicType.GreaterEvilSlayer,
            MagicType.EvilSlayer,
        };

        private static readonly MagicType[] TaoistDirectAttackPriority =
        {
            MagicType.ExplosiveTalisman,
            MagicType.EvilSlayer,
            MagicType.GreaterEvilSlayer,
        };

        private static readonly MagicType[] TaoistAdaptiveFallback =
        {
            MagicType.GreaterHolyStrike,
            MagicType.ImprovedExplosiveTalisman,
            MagicType.GreaterEvilSlayer,
            MagicType.ExplosiveTalisman,
            MagicType.EvilSlayer,
            MagicType.GreaterPoisonDust,
            MagicType.PoisonDust,
        };

        private static readonly MagicType[] AssassinMeleePriority =
        {
            MagicType.FullBloom,
            MagicType.WhiteLotus,
            MagicType.RedLotus,
            MagicType.SweetBrier,
        };

        private static readonly MagicType[] AssassinFireMeleePriority =
        {
            MagicType.FlameSplash,
        };

        private static readonly MagicType[] AssassinPhantomPriority =
        {
            MagicType.FullBloom,
            MagicType.WhiteLotus,
            MagicType.RedLotus,
            MagicType.SweetBrier,
        };

        private static readonly MagicType[] AssassinAreaDarkPriority =
        {
            MagicType.PoisonousCloud,
        };

        private static readonly MagicType[] AssassinAreaPhysicalPriority =
        {
            MagicType.Rake,
        };

        private static readonly MagicType[] AssassinTargetDarkPriority =
        {
            MagicType.WraithGrip,
        };

        private static readonly MagicType[] AssassinTargetFirePriority =
        {
            MagicType.HellFire,
        };

        private static readonly MagicType[] AssassinAdaptiveFallback =
        {
            MagicType.FlameSplash,
            MagicType.FullBloom,
            MagicType.WhiteLotus,
            MagicType.RedLotus,
            MagicType.SweetBrier,
        };

        private static readonly MagicType[] AssassinBuffPriority =
        {
            MagicType.RagingWind,
            MagicType.Evasion,
            MagicType.DarkConversion,
            MagicType.Concentration,
        };


        public static MagicType GetWarriorChargeMagic(PlayerObject player)
        {
            if (player == null)
                return MagicType.None;

            List<MagicType> chargeable = WarriorChargedAttackPriority
                .Where(magicType => IsWarriorChargeMagicReady(player, magicType))
                .ToList();
            if (chargeable.Count == 0)
                return MagicType.None;

            long seed = (SEnvir.Now.Ticks / TimeSpan.TicksPerSecond) + player.ObjectID;
            return chargeable[(int)(Math.Abs(seed) % chargeable.Count)];
        }

        public static MagicType GetWarriorMeleeAttackMagic(PlayerObject player, MapObject target, int nearbyMobCount)
        {
            bool isAreaAttack = nearbyMobCount >= 3;

            MagicType chargedMagic = SelectRotatingReadyMagic(player, WarriorChargedAttackPriority);
            if (chargedMagic != MagicType.None)
                return chargedMagic;

            // 优先使用伤害评估模块选择技能
            MagicType bestSkill = SelectHighestDamageSkill(
                player,
                target,
                isAreaAttack ? WarriorAreaPriority : WarriorSingleTargetPriority,
                isAreaAttack,
                nearbyMobCount);

            if (bestSkill != MagicType.None)
                return bestSkill;

            // 兜底：使用怪物抗性自适应选择
            if (ShouldUseMonsterAdaptiveSkillSelection(player, target))
            {
                Dictionary<Element, MagicType[]> skillMap = new Dictionary<Element, MagicType[]>
                {
                    { Element.None, isAreaAttack ? WarriorAdaptivePhysicalAreaPriority : WarriorAdaptivePhysicalSinglePriority },
                    { Element.Fire, WarriorFirePriority },
                };

                MagicType adaptiveMagic = SelectAdaptiveMonsterMagic(player, target, skillMap, isAreaAttack ? WarriorAdaptiveAreaFallback : WarriorAdaptiveSingleFallback);
                if (adaptiveMagic != MagicType.None)
                    return adaptiveMagic;
            }

            // 最后兜底：轮转选择
            return SelectRotatingReadyMagic(player, isAreaAttack ? WarriorAreaPriority : WarriorSingleTargetPriority);
        }

        public static MagicType GetWizardRangedMagic(PlayerObject player, MapObject target, int nearbyMobCount)
        {
            if (nearbyMobCount >= 3)
            {
                MagicType areaMagic = SelectRotatingReadyMagic(
                    player,
                    WizardAdaptiveFallback.Where(IsAreaAttackMagic));
                if (areaMagic != MagicType.None)
                    return areaMagic;
            }

            return SelectRotatingReadySingleTargetMagic(player, WizardRangedPriority);
        }

        public static MagicType GetTaoistRangedMagic(PlayerObject player, MapObject target, int nearbyMobCount = 0)
        {
            MagicType directMagic = GetTaoistReadyDirectAttacks(player).FirstOrDefault();
            return directMagic != MagicType.None
                ? directMagic
                : GetTaoistOptionalPoisonMagic(player, target, nearbyMobCount);
        }

        internal static MagicType GetTaoistOptionalPoisonMagic(PlayerObject player, MapObject target, int nearbyMobCount = 0)
        {
            if (player == null || player.Dead || target == null || target.Dead)
                return MagicType.None;

            int neededShape;
            switch (GetMonsterVisualState(target))
            {
                case MonsterVisualState.Normal:
                    neededShape = 1;
                    break;
                case MonsterVisualState.RedPoison:
                    neededShape = 0;
                    break;
                default:
                    return MagicType.None;
            }

            UserItem equippedPoison = player.Equipment[(int)EquipmentSlot.Poison];
            if (equippedPoison == null || equippedPoison.Count <= 0 || equippedPoison.Info.Shape != neededShape)
                return MagicType.None;
            if (!IsMagicReady(player, MagicType.PoisonDust))
                return MagicType.None;

            bool shouldUseMassPoison = nearbyMobCount >= 3 && IsMagicReady(player, MagicType.GreaterPoisonDust);
            MagicType[] poisonPriority = shouldUseMassPoison ? TaoistMassPoisonPriority : TaoistSinglePoisonPriority;
            foreach (MagicType poisonSkill in poisonPriority)
            {
                if (IsMagicReady(player, poisonSkill))
                    return poisonSkill;
            }

            return MagicType.None;
        }

        /// <summary>
        /// 道士符咒攻击（按经济性选择）
        /// </summary>
        private static MagicType SelectTalismanAttack(PlayerObject player, MapObject target, int nearbyMobCount)
        {
            foreach (MagicType magicType in TaoistDirectAttackPriority)
            {
                if (IsMagicReady(player, magicType))
                    return magicType;
            }

            return MagicType.None;
        }

        internal static IEnumerable<MagicType> GetTaoistReadyDirectAttacks(PlayerObject player)
        {
            if (player == null || player.Dead)
                yield break;

            foreach (MagicType magicType in TaoistDirectAttackPriority)
            {
                if (IsMagicReady(player, magicType))
                    yield return magicType;
            }
        }

        public static MagicType GetTaoistAttackMagic(PlayerObject player, MapObject target, int nearbyMobCount = 0)
        {
            MagicType directMagic = GetTaoistReadyDirectAttacks(player).FirstOrDefault();
            return directMagic != MagicType.None
                ? directMagic
                : GetTaoistOptionalPoisonMagic(player, target, nearbyMobCount);
        }

        public static MagicType GetAssassinBuffMagic(PlayerObject player)
        {
            if (player == null || player.Dead)
                return MagicType.None;

            foreach (MagicType magicType in AssassinBuffPriority)
            {
                if (HasRelatedBuff(player, magicType))
                    continue;

                if (IsMagicReady(player, magicType))
                    return magicType;
            }

            return MagicType.None;
        }

        public static MagicType GetAssassinSummonMagic(PlayerObject player)
        {
            if (player == null || player.Dead)
                return MagicType.None;

            bool hasLivingPuppet = player.Pets.Any(p =>
                p != null && !p.Dead && p.Node != null && p.MonsterInfo?.Flag == MonsterFlag.SummonPuppet);

            if (hasLivingPuppet)
                return MagicType.None;

            return IsMagicReady(player, MagicType.SummonPuppet) ? MagicType.SummonPuppet : MagicType.None;
        }

        /// <summary>
        /// 获取道士给自己增加防御的技能
        /// </summary>
        public static MagicType GetTaoistSelfDefenseMagic(PlayerObject player)
        {
            if (player == null || player.Dead)
                return MagicType.None;

            // 遍历所有防御技能，优先给自己加还没加的
            foreach (MagicType defenseSkill in TaoistDefensePriority)
            {
                if (HasRelatedBuff(player, defenseSkill))
                    continue; // 已经有这个 Buff 了

                if (IsMagicReady(player, defenseSkill))
                    return defenseSkill;
            }

            return MagicType.None;
        }

        /// <summary>
        /// 获取道士快速防御技能（根据是否组队选择单体/群体）
        /// 如果没有队友，优先使用单体防御技能；如果有队友，优先使用群体防御技能
        /// </summary>
        private static MagicType GetTaoistQuickDefenseMagic(PlayerObject player)
        {
            if (player == null || player.Dead)
                return MagicType.None;

            // 检查是否在队伍中
            bool hasTeammates = player.GroupMembers != null && player.GroupMembers.Count > 1;
            
            // 单体防御技能：阴阳法环、养生术
            // 群体防御技能：幽灵盾、神圣战甲术、强魔震法、猛虎强势
            MagicType[] singleDefenseSkills = 
            {
                MagicType.CelestialLight,   // 阴阳法环（单体）
                MagicType.EmpoweredHealing   // 养生术（单体）
            };
            
            MagicType[] groupDefenseSkills = 
            {
                MagicType.MagicResistance,       // 幽灵盾（群体）
                MagicType.Resilience,           // 神圣战甲术（群体）
                MagicType.ElementalSuperiority, // 强魔震法（群体）
                MagicType.BloodLust               // 猛虎强势（群体）
            };

            // 根据是否组队选择技能列表
            MagicType[] defenseSkills = hasTeammates ? groupDefenseSkills : singleDefenseSkills;

            // 遍历技能，优先使用还没加的
            foreach (MagicType defenseSkill in defenseSkills)
            {
                if (HasRelatedBuff(player, defenseSkill))
                    continue; // 已经有这个 Buff 了

                if (IsMagicReady(player, defenseSkill))
                    return defenseSkill;
            }

            return MagicType.None;
        }

        /// <summary>
        /// 获取道士给队友增加防御的技能
        /// </summary>
        public static MagicType GetTaoistGroupDefenseMagic(PlayerObject player, PlayerObject teammate)
        {
            if (player == null || player.Dead || teammate == null || teammate.Dead)
                return MagicType.None;

            // 只能给自己附近的队友加防御
            int dist = MaxChebyshevDistance(player.CurrentLocation, teammate.CurrentLocation);
            if (dist > 10) // 10 格范围内
                return MagicType.None;

            // 遍历所有防御技能，优先给还没加的队友加
            foreach (MagicType defenseSkill in TaoistDefensePriority)
            {
                if (HasRelatedBuff(teammate, defenseSkill))
                    continue; // 队友已经有这个 Buff 了

                if (IsMagicReady(player, defenseSkill))
                    return defenseSkill;
            }

            return MagicType.None;
        }

        public static MagicType GetAssassinAreaMagic(PlayerObject player, MapObject target, int nearbyMobCount)
        {
            if (nearbyMobCount < 3)
                return MagicType.None;

            bool isAreaAttack = true;

            // 优先使用伤害评估模块选择技能
            List<MagicType> areaCandidates = new List<MagicType>();
            areaCandidates.AddRange(AssassinAreaDarkPriority);
            areaCandidates.AddRange(AssassinAreaPhysicalPriority);

            MagicType bestSkill = SelectHighestDamageSkill(
                player,
                target,
                areaCandidates,
                isAreaAttack,
                nearbyMobCount);

            if (bestSkill != MagicType.None)
                return bestSkill;

            // 兜底：使用怪物抗性自适应选择
            if (ShouldUseMonsterAdaptiveSkillSelection(player, target))
            {
                Dictionary<Element, MagicType[]> skillMap = new Dictionary<Element, MagicType[]>
                {
                    { Element.Dark, AssassinAreaDarkPriority },
                    { Element.None, AssassinAreaPhysicalPriority },
                };

                MagicType adaptiveMagic = SelectAdaptiveMonsterMagic(player, target, skillMap, AssassinAreaDarkPriority.Concat(AssassinAreaPhysicalPriority));
                if (adaptiveMagic != MagicType.None)
                    return adaptiveMagic;
            }

            // 最后兜底：按优先级选择
            if (IsMagicReady(player, MagicType.PoisonousCloud))
                return MagicType.PoisonousCloud;

            if (IsMagicReady(player, MagicType.Rake))
                return MagicType.Rake;

            return MagicType.None;
        }

        public static MagicType GetAssassinTargetMagic(PlayerObject player, MapObject target)
        {
            if (player == null || target == null || target.Dead)
                return MagicType.None;

            Dictionary<Element, MagicType[]> skillMap = new Dictionary<Element, MagicType[]>();
            List<MagicType> fallback = new List<MagicType>();

            if ((target.Poison & PoisonType.WraithGrip) != PoisonType.WraithGrip)
            {
                skillMap[Element.Dark] = AssassinTargetDarkPriority;
                fallback.AddRange(AssassinTargetDarkPriority);
            }

            if ((target.Poison & PoisonType.HellFire) != PoisonType.HellFire)
            {
                skillMap[Element.Fire] = AssassinTargetFirePriority;
                fallback.AddRange(AssassinTargetFirePriority);
            }

            if (skillMap.Count == 0)
                return MagicType.None;

            // 优先使用伤害评估模块选择技能
            MagicType bestSkill = SelectHighestDamageSkill(
                player,
                target,
                fallback,
                false,
                1);

            if (bestSkill != MagicType.None)
                return bestSkill;

            // 兜底：使用怪物抗性自适应选择
            if (ShouldUseMonsterAdaptiveSkillSelection(player, target))
            {
                MagicType adaptiveMagic = SelectAdaptiveMonsterMagic(player, target, skillMap, fallback);
                if (adaptiveMagic != MagicType.None)
                    return adaptiveMagic;
            }

            // 最后兜底：轮转选择
            return SelectRotatingReadyMagic(player, fallback);
        }

        public static MagicType GetAssassinGapCloserMagic(PlayerObject player, int distance)
        {
            if (distance <= 1 || distance > 5)
                return MagicType.None;

            return IsMagicReady(player, MagicType.DanceOfSwallow) ? MagicType.DanceOfSwallow : MagicType.None;
        }

        public static MagicType GetAssassinMeleeAttackMagic(PlayerObject player, MapObject target, int nearbyMobCount)
        {
            if (player == null || player.Dead)
                return MagicType.None;

            if (CanUseAssassinKarma(player))
                return MagicType.Karma;

            bool isAreaAttack = nearbyMobCount >= 3;

            // 优先使用伤害评估模块选择技能
            List<MagicType> candidates = new List<MagicType>();
            if (isAreaAttack)
            {
                candidates.Add(MagicType.FlameSplash);
            }
            candidates.AddRange(AssassinMeleePriority);

            MagicType bestSkill = SelectHighestDamageSkill(
                player,
                target,
                candidates,
                isAreaAttack,
                nearbyMobCount);

            if (bestSkill != MagicType.None)
                return bestSkill;

            // 兜底：使用怪物抗性自适应选择
            if (ShouldUseMonsterAdaptiveSkillSelection(player, target))
            {
                Dictionary<Element, MagicType[]> skillMap = new Dictionary<Element, MagicType[]>
                {
                    { Element.Fire, AssassinFireMeleePriority },
                    { Element.Phantom, AssassinPhantomPriority },
                    { Element.None, AssassinPhantomPriority },
                };

                MagicType adaptiveMagic = SelectAdaptiveMonsterMagic(player, target, skillMap, AssassinAdaptiveFallback);
                if (adaptiveMagic != MagicType.None)
                    return adaptiveMagic;
            }

            // 最后兜底：按优先级选择
            if (isAreaAttack && IsMagicReady(player, MagicType.FlameSplash))
                return MagicType.FlameSplash;

            return SelectRotatingReadyMagic(player, AssassinMeleePriority);
        }


        public static int CountNearbyAttackableMonsters(PlayerObject player, Point center, int range)

        {
            if (player == null || range < 0)
                return 0;

            int count = 0;
            int maxDist = range * range; // 用距离平方避免开方

            foreach (var ob in player.VisibleObjects)
            {
                var mob = ob as MonsterObject;
                if (mob == null || mob.Node == null || mob.Dead)
                    continue;
                if (mob.PetOwner != null)
                    continue;
                if (!player.CanAttackTarget(mob))
                    continue;

                int dx = center.X - mob.CurrentLocation.X;
                int dy = center.Y - mob.CurrentLocation.Y;
                // 切比雪夫距离: max(|dx|, |dy|) <= range
                if (Math.Max(Math.Abs(dx), Math.Abs(dy)) <= range)
                    count++;
            }

            return count;
        }

        private static MagicType SelectFirstReadyMagic(PlayerObject player, IEnumerable<MagicType> priority)
        {
            if (player == null)
                return MagicType.None;

            foreach (MagicType magicType in priority)
                if (IsMagicReady(player, magicType))
                    return magicType;

            return MagicType.None;
        }

        private static MagicType SelectRotatingReadyMagic(PlayerObject player, IEnumerable<MagicType> priority)
        {
            if (player == null)
                return MagicType.None;

            // 优先用静态数组直接索引，避免 LINQ 分配
            MagicType[] arr = priority as MagicType[];
            int count = 0;
            int readyIndex = -1;

            if (arr != null)
            {
                // 静态数组：逐个检查 IsMagicReady，用 readyIndex 记录轮转候选
                for (int i = 0; i < arr.Length; i++)
                {
                    if (IsMagicReady(player, arr[i]))
                    {
                        count++;
                        readyIndex = i;
                    }
                }
            }
            else
            {
                // 兜底：非数组场景（极少触发）
                List<MagicType> ready = priority
                    .Distinct()
                    .Where(magicType => IsMagicReady(player, magicType))
                    .ToList();
                if (ready.Count == 0) return MagicType.None;
                long fbSeed = (SEnvir.Now.Ticks / TimeSpan.TicksPerSecond) + player.ObjectID;
                return ready[(int)(Math.Abs(fbSeed) % ready.Count)];
            }

            if (count == 0)
                return MagicType.None;
            if (count == 1)
                return arr[readyIndex];

            // 轮转逻辑：基于时间的确定性选择
            long seed = (SEnvir.Now.Ticks / TimeSpan.TicksPerSecond) + player.ObjectID;
            int selectedOrdinal = (int)(Math.Abs(seed) % count);

            // 找到第 selectedOrdinal 个就绪技能
            for (int i = 0; i < arr.Length; i++)
            {
                if (IsMagicReady(player, arr[i]))
                {
                    if (selectedOrdinal-- == 0)
                        return arr[i];
                }
            }

            return arr[readyIndex];
        }

        /// <summary>
        /// 轮转选择可用的技能（过滤掉群体技能，用于法师/道士单攻场景）
        /// </summary>
        private static MagicType SelectRotatingReadySingleTargetMagic(PlayerObject player, IEnumerable<MagicType> priority)
        {
            if (player == null)
                return MagicType.None;

            MagicType[] arr = priority as MagicType[];
            if (arr == null)
            {
                // 兜底非数组
                List<MagicType> ready = priority
                    .Distinct()
                    .Where(magicType => IsMagicReady(player, magicType))
                    .Where(magicType => !IsAreaAttackMagic(magicType))
                    .ToList();
                if (ready.Count == 0) return MagicType.None;
                long fbSeed2 = (SEnvir.Now.Ticks / TimeSpan.TicksPerSecond) + player.ObjectID;
                return ready[(int)(Math.Abs(fbSeed2) % ready.Count)];
            }

            int count = 0;
            int readyIndex = -1;
            for (int i = 0; i < arr.Length; i++)
            {
                if (IsMagicReady(player, arr[i]) && !IsAreaAttackMagic(arr[i]))
                {
                    count++;
                    readyIndex = i;
                }
            }

            if (count == 0)
                return MagicType.None;
            if (count == 1)
                return arr[readyIndex];

            long seed = (SEnvir.Now.Ticks / TimeSpan.TicksPerSecond) + player.ObjectID;
            int selectedOrdinal = (int)(Math.Abs(seed) % count);
            for (int i = 0; i < arr.Length; i++)
            {
                if (IsMagicReady(player, arr[i]) && !IsAreaAttackMagic(arr[i]))
                {
                    if (selectedOrdinal-- == 0)
                        return arr[i];
                }
            }
            return arr[readyIndex];
        }

        private static MagicType SelectRandomReadyMagic(PlayerObject player, IEnumerable<MagicType> priority)
        {
            if (player == null)
                return MagicType.None;

            MagicType[] arr = priority as MagicType[];
            if (arr == null)
            {
                List<MagicType> ready = priority
                    .Distinct()
                    .Where(magicType => IsMagicReady(player, magicType))
                    .ToList();
                if (ready.Count == 0) return MagicType.None;
                return ready[SEnvir.Random.Next(ready.Count)];
            }

            MagicType last = MagicType.None;
            int count = 0;
            for (int i = 0; i < arr.Length; i++)
            {
                if (IsMagicReady(player, arr[i]))
                {
                    count++;
                    last = arr[i];
                }
            }
            if (count == 0) return MagicType.None;
            if (count == 1) return last;

            // Fisher-Yates 风格：随机选第 N 个就绪技能
            int skip = SEnvir.Random.Next(count);
            for (int i = 0; i < arr.Length; i++)
            {
                if (IsMagicReady(player, arr[i]))
                {
                    if (skip-- == 0)
                        return arr[i];
                }
            }
            return last;
        }

        /// <summary>
        /// 随机选择可用的技能（过滤掉群体技能，用于法师/道士单攻场景）
        /// </summary>
        private static MagicType SelectRandomReadySingleTargetMagic(PlayerObject player, IEnumerable<MagicType> priority)
        {
            if (player == null)
                return MagicType.None;

            MagicType[] arr = priority as MagicType[];
            if (arr == null)
            {
                List<MagicType> ready = priority
                    .Distinct()
                    .Where(magicType => IsMagicReady(player, magicType))
                    .Where(magicType => !IsAreaAttackMagic(magicType))
                    .ToList();
                if (ready.Count == 0) return MagicType.None;
                return ready[SEnvir.Random.Next(ready.Count)];
            }

            MagicType last = MagicType.None;
            int count = 0;
            for (int i = 0; i < arr.Length; i++)
            {
                if (IsMagicReady(player, arr[i]) && !IsAreaAttackMagic(arr[i]))
                {
                    count++;
                    last = arr[i];
                }
            }
            if (count == 0) return MagicType.None;
            if (count == 1) return last;

            int skip = SEnvir.Random.Next(count);
            for (int i = 0; i < arr.Length; i++)
            {
                if (IsMagicReady(player, arr[i]) && !IsAreaAttackMagic(arr[i]))
                {
                    if (skip-- == 0)
                        return arr[i];
                }
            }
            return last;
        }

        private static MagicType SelectAdaptiveMonsterMagic(PlayerObject player, MapObject target, IDictionary<Element, MagicType[]> skillMap, IEnumerable<MagicType> fallback, bool filterAreaAttack = false)
        {
            if (player == null || target == null || skillMap == null || skillMap.Count == 0)
                return MagicType.None;

            List<Element> resistanceOrder = GetMonsterResistanceOrder(target, skillMap.Keys);
            foreach (Element element in resistanceOrder)
            {
                // 根据是否过滤群体技能选择不同的选择函数
                MagicType magic = filterAreaAttack
                    ? SelectRotatingReadySingleTargetMagic(player, skillMap[element])
                    : SelectRotatingReadyMagic(player, skillMap[element]);
                if (magic != MagicType.None)
                    return magic;
            }

            // 根据是否过滤群体技能选择不同的选择函数
            return filterAreaAttack
                ? SelectRandomReadySingleTargetMagic(player, fallback)
                : SelectRandomReadyMagic(player, fallback);
        }

        private static List<Element> GetMonsterResistanceOrder(MapObject target, IEnumerable<Element> supportedElements)
        {
            MonsterObject monster = target as MonsterObject;
            if (monster == null || monster.Node == null || monster.Dead)
                return new List<Element>();

            List<KeyValuePair<Element, int>> resistances = supportedElements
                .Distinct()
                .Select(element => new KeyValuePair<Element, int>(element, target.Stats.GetResistanceValue(element)))
                .ToList();

            if (resistances.Count == 0)
                return new List<Element>();

            int firstValue = resistances[0].Value;
            bool hasVariance = resistances.Any(pair => pair.Value != firstValue);
            bool hasWeakness = resistances.Any(pair => pair.Value < 0);

            if (!hasVariance && !hasWeakness)
                return new List<Element>();

            return resistances
                .OrderBy(pair => pair.Value)
                .ThenBy(pair => (int)pair.Key)
                .Select(pair => pair.Key)
                .ToList();
        }

        private static MagicType GetAdaptiveTaoistMonsterMagic(PlayerObject player, MapObject target, bool filterAreaAttack = false)
        {
            if (!ShouldUseMonsterAdaptiveSkillSelection(player, target))
                return MagicType.None;

            Dictionary<Element, MagicType[]> skillMap = new Dictionary<Element, MagicType[]>();
            List<MagicType> fallback = new List<MagicType>();

            if (HasTaoistAvailablePoisonSkill(player, target))
            {
                skillMap[Element.Dark] = TaoistAllPoisonPriority;
                fallback.AddRange(TaoistAllPoisonPriority);
            }

            if (HasEquipmentItem(player, EquipmentSlot.Amulet, ItemType.Amulet))
            {
                skillMap[Element.Fire] = TaoistFirePriority;
                skillMap[Element.Holy] = TaoistHolyPriority;
                fallback.AddRange(TaoistHolyPriority);
                fallback.AddRange(TaoistFirePriority);
            }

            if (fallback.Count == 0)
                return MagicType.None;

            return SelectAdaptiveMonsterMagic(player, target, skillMap, fallback, filterAreaAttack);
        }

        private static bool ShouldUseMonsterAdaptiveSkillSelection(PlayerObject player, MapObject target)
        {
            return player != null
                   && !player.Dead
                   && player.Level >= 30
                   && target != null
                   && target.Race == ObjectType.Monster
                   && target.Node != null
                   && !target.Dead;
        }

        private static bool IsMagicReady(PlayerObject player, MagicType magicType)
        {
            if (!TryGetReadyMagic(player, magicType, out UserMagic magic))
                return false;

            return player.CurrentMP >= magic.Cost;
        }

        private static bool TryGetReadyMagic(PlayerObject player, MagicType magicType, out UserMagic magic)
        {
            magic = null;
            if (player == null)
                return false;

            if (!player.Magics.TryGetValue(magicType, out magic))
                return false;

            if (magic.Info == null || player.Level < magic.Info.NeedLevel1)
                return false;

            if (magic.Cooldown > SEnvir.Now)
                return false;

            switch (magicType)
            {
                case MagicType.FlamingSword:
                    return player.CanFlamingSword;
                case MagicType.BladeStorm:
                    return player.CanBladeStorm;
                case MagicType.MaelstromBlade:
                    return player.CanMaelstromBlade;
                default:
                    return true;
            }
        }

        private static bool IsWarriorChargeMagicReady(PlayerObject player, MagicType magicType)
        {
            if (player == null || !player.Magics.TryGetValue(magicType, out UserMagic magic) || magic?.Info == null)
                return false;
            if (player.Level < magic.Info.NeedLevel1 || magic.Cooldown > SEnvir.Now || magic.Cost > player.CurrentMP)
                return false;

            switch (magicType)
            {
                case MagicType.FlamingSword:
                    return !player.CanFlamingSword;
                case MagicType.BladeStorm:
                    return !player.CanBladeStorm;
                case MagicType.MaelstromBlade:
                    return !player.CanMaelstromBlade;
                default:
                    return false;
            }
        }

        private static bool HasEquipmentItem(PlayerObject player, EquipmentSlot slot, ItemType itemType)
        {
            if (player == null)
                return false;

            UserItem item = player.Equipment[(int)slot];
            return item != null && item.Info.ItemType == itemType && item.Count > 0;
        }

        private static bool HasTaoistAvailablePoisonSkill(PlayerObject player, MapObject target)
        {
            // 只有在目标没有双毒的情况下，才允许使用施毒技能
            if (target == null || target.Dead)
                return false;

            if (!HasEquipmentItem(player, EquipmentSlot.Poison, ItemType.Poison))
                return false;

            bool hasGreenPoison = (target.Poison & PoisonType.Green) != PoisonType.None;
            bool hasRedPoison = (target.Poison & PoisonType.Red) != PoisonType.None;

            // 只有在没有双毒的情况下，才允许施毒
            return !hasGreenPoison || !hasRedPoison;
        }




        private static bool HasRelatedBuff(PlayerObject player, MagicType magicType)

        {
            switch (magicType)
            {
                case MagicType.RagingWind:
                    return player.Buffs.Any(x => x.Type == BuffType.RagingWind);
                case MagicType.Evasion:
                    return player.Buffs.Any(x => x.Type == BuffType.Evasion);
                case MagicType.DarkConversion:
                    return player.Buffs.Any(x => x.Type == BuffType.DarkConversion);
                case MagicType.Concentration:
                    return player.Buffs.Any(x => x.Type == BuffType.Concentration);
                // 道士防御技能 Buff
                case MagicType.MagicResistance:           // 幽灵盾
                    return player.Buffs.Any(x => x.Type == BuffType.MagicResistance);
                case MagicType.Resilience:                // 神圣战甲术
                    return player.Buffs.Any(x => x.Type == BuffType.Resilience);
                case MagicType.ElementalSuperiority:      // 强魔震法
                    return player.Buffs.Any(x => x.Type == BuffType.ElementalSuperiority);
                case MagicType.BloodLust:                 // 猛虎强势
                    return player.Buffs.Any(x => x.Type == BuffType.BloodLust);
                case MagicType.CelestialLight:            // 阴阳法环
                    return player.Buffs.Any(x => x.Type == BuffType.CelestialLight);
                case MagicType.EmpoweredHealing:          // 养生术
                    return player.Buffs.Any(x => x.Type == BuffType.Heal); // 养生术使用 Heal Buff
                default:
                    return false;
            }
        }

        private static bool CanUseAssassinKarma(PlayerObject player)
        {
            if (player == null)
                return false;

            if (!player.Buffs.Any(x => x.Type == BuffType.Cloak))
                return false;

            if (!TryGetReadyMagic(player, MagicType.Karma, out UserMagic magic))
                return false;

            int hpCost = player.Stats[Stat.Health] * magic.Cost / 100;
            return hpCost < player.CurrentHP && player.CurrentHP > player.Stats[Stat.Health] / 10;
        }

        private static int MaxChebyshevDistance(Point a, Point b)
        {
            return Math.Max(Math.Abs(a.X - b.X), Math.Abs(a.Y - b.Y));
        }

        /// <summary>
        /// 获取怪物名称（用于学习记忆的 key）
        /// </summary>
        private static string GetMonsterNameForMemory(MapObject target)
        {
            if (target is MonsterObject monster && monster.MonsterInfo != null)
                return monster.MonsterInfo.MonsterName;
            return string.Empty;
        }

        #region 技能伤害评估模块

        /// <summary>
        /// 计算技能预期平均伤害值
        /// </summary>
        public static int GetSkillExpectedDamage(PlayerObject player, UserMagic magic, MapObject target = null)
        {
            if (player == null || magic == null || magic.Info == null)
                return 0;

            // 基础伤害：技能基础伤害 + 等级加成伤害
            int skillLevel = GetMagicLevel(player, magic);
            int minBase = magic.Info.MinBasePower + skillLevel * magic.Info.MinLevelPower;
            int maxBase = magic.Info.MaxBasePower + skillLevel * magic.Info.MaxLevelPower;
            int baseDamage = (minBase + maxBase) / 2;

            if (baseDamage <= 0)
                return 0;

            // 玩家魔法攻击加成（MinMC、MaxMC 或 MinSC、MaxSC）
            int playerMinMagic = 0, playerMaxMagic = 0;
            GetPlayerMagicAttack(player, out playerMinMagic, out playerMaxMagic);
            int playerMagic = (playerMinMagic + playerMaxMagic) / 2;

            // 总伤害 = 基础伤害 + 玩家魔法攻击
            int totalDamage = baseDamage + playerMagic;

            // 考虑目标的魔法抗性（如果有目标）
            if (target != null && target is MonsterObject monster)
            {
                // 考虑元素抗性（基于技能元素）
                if (monster.Node != null && !monster.Dead)
                {
                    Element element = GetMagicElement(magic.Info.Magic);
                    int elementResist = monster.Stats.GetResistanceValue(element);
                    totalDamage = totalDamage * (100 - elementResist) / 100;
                }
            }

            return Math.Max(0, totalDamage);
        }

        /// <summary>
        /// 获取技能等级（0-3）
        /// </summary>
        private static int GetMagicLevel(PlayerObject player, UserMagic magic)
        {
            if (player == null || magic == null || magic.Info == null)
                return 0;

            int level = 0;

            if (player.Level >= magic.Info.NeedLevel3 && magic.Experience >= magic.Info.Experience3)
                level = 3;
            else if (player.Level >= magic.Info.NeedLevel2 && magic.Experience >= magic.Info.Experience2)
                level = 2;
            else if (player.Level >= magic.Info.NeedLevel1)
                level = 1;

            return level;
        }

        /// <summary>
        /// 获取玩家的魔法攻击值
        /// </summary>
        private static void GetPlayerMagicAttack(PlayerObject player, out int minMagic, out int maxMagic)
        {
            minMagic = maxMagic = 0;

            if (player == null)
                return;

            // 优先使用自然系魔法（MinMC/MaxMC），否则使用灵魂系魔法（MinSC/MaxSC）
            int minMC = player.Stats[Stat.MinMC];
            int maxMC = player.Stats[Stat.MaxMC];
            int minSC = player.Stats[Stat.MinSC];
            int maxSC = player.Stats[Stat.MaxSC];

            if (minMC > 0 || maxMC > 0)
            {
                minMagic = minMC;
                maxMagic = maxMC;
            }
            else
            {
                minMagic = minSC;
                maxMagic = maxSC;
            }
        }

        /// <summary>
        /// 获取技能的元素类型
        /// </summary>
        private static Element GetMagicElement(MagicType magicType)
        {
            // 根据技能类型返回元素
            switch (magicType)
            {
                case MagicType.FireBall:
                case MagicType.MeteorShower:
                case MagicType.FireStorm:
                case MagicType.ExplosiveTalisman:
                case MagicType.ImprovedExplosiveTalisman:
                case MagicType.FlamingSword:
                case MagicType.FlameSplash:
                case MagicType.HellFire:
                    return Element.Fire;

                case MagicType.IceBolt:
                case MagicType.FrozenEarth:
                case MagicType.GreaterFrozenEarth:
                case MagicType.IceBlades:
                    return Element.Ice;

                case MagicType.LightningBall:
                case MagicType.ThunderBolt:
                case MagicType.LightningBeam:
                case MagicType.ChainLightning:
                case MagicType.JudgementOfHeaven:
                    return Element.Lightning;

                case MagicType.GustBlast:
                case MagicType.Cyclone:
                case MagicType.BlowEarth:
                case MagicType.DragonTornado:
                case MagicType.Tempest:
                    return Element.Wind;

                case MagicType.PoisonDust:
                case MagicType.GreaterPoisonDust:
                case MagicType.PoisonousCloud:
                    return Element.Dark;

                case MagicType.EvilSlayer:
                case MagicType.GreaterEvilSlayer:
                case MagicType.GreaterHolyStrike:
                    return Element.Holy;

                default:
                    return Element.None;
            }
        }

        /// <summary>
        /// 从候选技能中选择最高伤害的技能（考虑单攻/群攻场景）
        /// </summary>
        public static MagicType SelectHighestDamageSkill(
            PlayerObject player,
            MapObject target,
            IEnumerable<MagicType> candidates,
            bool isAreaAttack,
            int nearbyMobCount = 1)
        {
            if (player == null || !candidates.Any())
                return MagicType.None;

            uint targetObjectID = target?.ObjectID ?? 0;

            // 只复用同一目标的结果；目标改变后重新做伤害/抗性评估。
            if (player.CurrentMap != null)
            {
                int mapId = player.CurrentMap.Info.Index;
                if (_botSkillSelectionCache.TryGetValue(mapId, out var mapCache)
                    && mapCache.TryGetValue(player.ObjectID, out var playerCache))
                {
                    if (playerCache.TryGetValue(isAreaAttack, out BotSkillSelectionCacheEntry cachedEntry))
                    {
                        if (cachedEntry.TargetObjectID == targetObjectID && IsMagicReady(player, cachedEntry.Skill))
                            return cachedEntry.Skill;
                    }
                }
            }

            // 当怪物数量<3只时，强制只从单体技能中选择，不考虑群体技能
            bool forceSingleTarget = nearbyMobCount < 3;

            // 评估所有候选技能的伤害
            MagicType bestSkill = MagicType.None;
            int bestDamage = -1;
            int bestCost = int.MaxValue; // 蓝耗，越低越好

            foreach (MagicType magicType in candidates)
            {
                if (!player.Magics.TryGetValue(magicType, out UserMagic magic) || magic?.Info == null)
                    continue;

                if (!IsMagicReady(player, magicType))
                    continue;

                // 强制单体模式：跳过所有群体技能
                if (forceSingleTarget && IsAreaAttackMagic(magicType))
                    continue;

                // 群体攻击模式但怪物数量不足：跳过群体技能
                if (isAreaAttack && nearbyMobCount < 3 && IsAreaAttackMagic(magicType))
                    continue;

                int skillDamage = GetSkillExpectedDamage(player, magic, target);

                // 群体攻击技能需要考虑总伤害（单次伤害 × 怪物数量）
                if (isAreaAttack && nearbyMobCount >= 3 && IsAreaAttackMagic(magicType))
                {
                    skillDamage = skillDamage * nearbyMobCount;
                }

                int currentCost = magic.Cost;

                // 优先选择高伤害技能；伤害相近（差距<5%）时优先选择蓝耗低的
                bool chooseThisSkill = false;
                if (bestDamage < 0)
                {
                    chooseThisSkill = true;
                }
                else if (skillDamage > bestDamage * 1.05) // 伤害高5%以上，直接选择
                {
                    chooseThisSkill = true;
                }
                else if (skillDamage * 1.05 >= bestDamage) // 伤害相近，优先选择蓝耗低的
                {
                    if (currentCost < bestCost)
                    {
                        chooseThisSkill = true;
                    }
                }

                if (chooseThisSkill)
                {
                    bestDamage = skillDamage;
                    bestSkill = magicType;
                    bestCost = currentCost;
                }
            }

            // 缓存结果
            if (bestSkill != MagicType.None && player.CurrentMap != null)
            {
                int mapId = player.CurrentMap.Info.Index;
                if (!_botSkillSelectionCache.TryGetValue(mapId, out var mapCache))
                {
                    mapCache = new Dictionary<uint, Dictionary<bool, BotSkillSelectionCacheEntry>>();
                    _botSkillSelectionCache[mapId] = mapCache;
                }

                if (!mapCache.TryGetValue(player.ObjectID, out var playerCache))
                {
                    playerCache = new Dictionary<bool, BotSkillSelectionCacheEntry>();
                    mapCache[player.ObjectID] = playerCache;
                }

                playerCache[isAreaAttack] = new BotSkillSelectionCacheEntry
                {
                    TargetObjectID = targetObjectID,
                    Skill = bestSkill,
                };
            }

            // 学习记忆：记录选中技能对目标怪物的预估伤害
            if (bestSkill != MagicType.None && target != null)
            {
                string monsterName = GetMonsterNameForMemory(target);
                int estimatedDamage = bestDamage > 0 ? bestDamage : 0;
                BotMemory.RecordSkillUse(monsterName, bestSkill, estimatedDamage);
            }

            return bestSkill;
        }

        /// <summary>
        /// 判断技能是否为群体攻击技能
        /// </summary>
        private static bool IsAreaAttackMagic(MagicType magicType)
        {
            // 战士群体技能
            if (magicType == MagicType.HalfMoon || magicType == MagicType.BladeStorm ||
                magicType == MagicType.DestructiveSurge || magicType == MagicType.MaelstromBlade)
                return true;

            // 法师群体技能
            // GustBlast（风掌）和 Cyclone（击风）是单体技能，已移除
            // LightningBeam（激光）、BlowEarth（风震天）、ScortchedEarth（地狱火）、FrozenEarth（冰沙掌）是群体直线技能
            if (magicType == MagicType.MeteorShower || magicType == MagicType.FireStorm ||
                magicType == MagicType.LightningBeam || magicType == MagicType.ChainLightning ||
                magicType == MagicType.Tempest || magicType == MagicType.BlowEarth ||
                magicType == MagicType.ScortchedEarth || magicType == MagicType.FrozenEarth)
                return true;

            // 道士群体攻击技能
            if (magicType == MagicType.ImprovedExplosiveTalisman ||  // 灭魂火符（群体）
                magicType == MagicType.LifeSteal ||                 // 吸星大法（群体）
                magicType == MagicType.Scarecrow ||               // 迷魂大法（群体）
                magicType == MagicType.ThunderKick)                // 横扫千军（群体近战）
                return true;

            // 刺客群体技能
            if (magicType == MagicType.PoisonousCloud || magicType == MagicType.Rake)
                return true;

            return false;
        }

        /// <summary>
        /// 清除假人的技能选择缓存（切图时调用）
        /// </summary>
        public static void ClearBotSkillCache(uint playerObjectID, int? mapId = null)
        {
            if (mapId.HasValue)
            {
                // 只清除指定地图的缓存
                if (_botSkillSelectionCache.TryGetValue(mapId.Value, out var mapCache))
                {
                    mapCache.Remove(playerObjectID);
                }
            }
            else
            {
                // 清除所有地图的缓存
                foreach (var mapCache in _botSkillSelectionCache.Values)
                {
                    mapCache.Remove(playerObjectID);
                }
            }
        }

        #endregion
    }
}
