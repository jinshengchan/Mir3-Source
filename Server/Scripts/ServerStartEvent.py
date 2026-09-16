# -*- coding: utf-8 -*-
import Server.Envir.SEnvir as SEnvir
from Library import *

def OnServerStart():
	# 这里可以添加服务器启动时 需要执行的代码
	SEnvir.Log("服务器启动触发脚本执行完毕")
	
	# 这里可以增加对应的地图技能限制
	# 下面是参考范例，去掉＃号即可实现沙巴克地图的技能限制  沙巴克 限制 法师 雷电术 大火球
	SEnvir.AddMagicRestrictionToMap('沙巴克', [MagicType.Teleportation, MagicType.PotionMastery])
	SEnvir.AddMagicRestrictionToMap('沃玛神殿', [MagicType.GeoManipulation, MagicType.PotionMastery])
	SEnvir.AddMagicRestrictionToMap('沃玛神殿2层', [MagicType.GeoManipulation])
	SEnvir.AddMagicRestrictionToMap('祖玛神殿7-1层', [MagicType.GeoManipulation])
	SEnvir.AddMagicRestrictionToMap('祖玛神殿7-2层', [MagicType.GeoManipulation])
	SEnvir.AddMagicRestrictionToMap('祖玛神殿7-3层', [MagicType.GeoManipulation])
	SEnvir.AddMagicRestrictionToMap('祖玛教主宫廷', [MagicType.GeoManipulation, MagicType.PotionMastery])
	SEnvir.AddMagicRestrictionToMap('神舰3层', [MagicType.GeoManipulation])
	SEnvir.AddMagicRestrictionToMap('神舰2层', [MagicType.GeoManipulation])
	SEnvir.AddMagicRestrictionToMap('神舰1层', [MagicType.GeoManipulation])
	SEnvir.AddMagicRestrictionToMap('调控室', [MagicType.GeoManipulation])
	SEnvir.AddMagicRestrictionToMap('生死关', [MagicType.GeoManipulation])
	SEnvir.AddMagicRestrictionToMap('石阁7层', [MagicType.GeoManipulation, MagicType.PotionMastery])
	SEnvir.AddMagicRestrictionToMap('赤月山谷5层', [MagicType.GeoManipulation])
	SEnvir.AddMagicRestrictionToMap('赤月恶魔洞穴', [MagicType.GeoManipulation, MagicType.PotionMastery])
	SEnvir.AddMagicRestrictionToMap('潘夜神殿8层', [MagicType.GeoManipulation])
	SEnvir.AddMagicRestrictionToMap('潘夜神殿', [MagicType.GeoManipulation])
	SEnvir.AddMagicRestrictionToMap('真天宫北馆5层', [MagicType.GeoManipulation])
	SEnvir.AddMagicRestrictionToMap('黑度宫4层', [MagicType.GeoManipulation])
	SEnvir.AddMagicRestrictionToMap('真天宫', [MagicType.GeoManipulation])
	SEnvir.AddMagicRestrictionToMap('黑度宫', [MagicType.GeoManipulation])
	SEnvir.AddMagicRestrictionToMap('诺玛遗址4层', [MagicType.GeoManipulation])
	SEnvir.AddMagicRestrictionToMap('诺玛遗址5层', [MagicType.GeoManipulation])
	SEnvir.AddMagicRestrictionToMap('诺玛勇士坟墓', [MagicType.GeoManipulation, MagicType.PotionMastery])
	SEnvir.AddMagicRestrictionToMap('百花山庄', [MagicType.GeoManipulation, MagicType.PotionMastery])
	SEnvir.AddMagicRestrictionToMap('雪原神宫4层', [MagicType.GeoManipulation])
	SEnvir.AddMagicRestrictionToMap('龙血深渊4层', [MagicType.GeoManipulation])
	SEnvir.AddMagicRestrictionToMap('诺玛土坡', [MagicType.GeoManipulation, MagicType.PotionMastery])
	SEnvir.AddMagicRestrictionToMap('诺玛山谷', [MagicType.GeoManipulation, MagicType.PotionMastery])
	SEnvir.AddMagicRestrictionToMap('诺玛城', [MagicType.GeoManipulation, MagicType.PotionMastery])
	SEnvir.AddMagicRestrictionToMap('沙漠地下3层', [MagicType.GeoManipulation])
	SEnvir.AddMagicRestrictionToMap('地下魔宫', [MagicType.GeoManipulation])
	SEnvir.AddMagicRestrictionToMap('地底宫殿', [MagicType.GeoManipulation])
	SEnvir.AddMagicRestrictionToMap('沙漠地监', [MagicType.GeoManipulation])
	SEnvir.AddMagicRestrictionToMap('深渊', [MagicType.GeoManipulation])
	SEnvir.AddMagicRestrictionToMap('黎明女王的房间', [MagicType.GeoManipulation, MagicType.PotionMastery])
	SEnvir.AddMagicRestrictionToMap('龙血深渊5层朱雀屋', [MagicType.GeoManipulation, MagicType.PotionMastery])
	SEnvir.AddMagicRestrictionToMap('龙血深渊5层玄武屋', [MagicType.GeoManipulation, MagicType.PotionMastery])
	SEnvir.AddMagicRestrictionToMap('龙血深渊5层青龙屋', [MagicType.GeoManipulation, MagicType.PotionMastery])
	SEnvir.AddMagicRestrictionToMap('龙血深渊5层白虎屋', [MagicType.GeoManipulation, MagicType.PotionMastery])
	SEnvir.AddMagicRestrictionToMap('圣诞活动地图', [MagicType.GeoManipulation, MagicType.PotionMastery])
	SEnvir.AddMagicRestrictionToMap('赤龙城', [MagicType.GeoManipulation, MagicType.PotionMastery])
	SEnvir.AddMagicRestrictionToMap('赤龙城5层', [MagicType.GeoManipulation])
	SEnvir.AddMagicRestrictionToMap('BOSS火影地牢挑战场', [MagicType.GeoManipulation, MagicType.PotionMastery])
	SEnvir.AddMagicRestrictionToMap('火影地牢', [MagicType.GeoManipulation])
	SEnvir.AddMagicRestrictionToMap('异界神舰1层', [MagicType.GeoManipulation, MagicType.PotionMastery])
	SEnvir.AddMagicRestrictionToMap('异界神舰2-2层', [MagicType.GeoManipulation])
	SEnvir.AddMagicRestrictionToMap('异界神舰2-1层', [MagicType.GeoManipulation])
	SEnvir.AddMagicRestrictionToMap('异界神舰3层', [MagicType.GeoManipulation])
	SEnvir.AddMagicRestrictionToMap('异界神舰操控室', [MagicType.GeoManipulation])
	SEnvir.AddMagicRestrictionToMap('桃源仙境入口', [MagicType.GeoManipulation])
	SEnvir.AddMagicRestrictionToMap('桃源仙境禅林', [MagicType.GeoManipulation])
	SEnvir.AddMagicRestrictionToMap('桃源圣殿', [MagicType.GeoManipulation])
	SEnvir.AddMagicRestrictionToMap('灵鹫宫3层', [MagicType.GeoManipulation])
	SEnvir.AddMagicRestrictionToMap('灵鹫宫岔路', [MagicType.GeoManipulation])
	SEnvir.AddMagicRestrictionToMap('沃玛神殿【普通】', [MagicType.GeoManipulation])
	SEnvir.AddMagicRestrictionToMap('沃玛神殿【噩梦】', [MagicType.GeoManipulation])
	SEnvir.AddMagicRestrictionToMap('沃玛神殿【地狱】', [MagicType.GeoManipulation])
	SEnvir.AddMagicRestrictionToMap('祖玛宫廷【普通】', [MagicType.GeoManipulation])
	SEnvir.AddMagicRestrictionToMap('祖玛宫廷【噩梦】', [MagicType.GeoManipulation])
	SEnvir.AddMagicRestrictionToMap('祖玛宫廷【地狱】', [MagicType.GeoManipulation])
	SEnvir.AddMagicRestrictionToMap('生死关【普通】', [MagicType.GeoManipulation])
	SEnvir.AddMagicRestrictionToMap('生死关【噩梦】', [MagicType.GeoManipulation])
	SEnvir.AddMagicRestrictionToMap('生死关【地狱】', [MagicType.GeoManipulation])
	SEnvir.AddMagicRestrictionToMap('石阁神庙【普通】', [MagicType.GeoManipulation])
	SEnvir.AddMagicRestrictionToMap('石阁神庙【噩梦】', [MagicType.GeoManipulation])
	SEnvir.AddMagicRestrictionToMap('石阁神庙【地狱】', [MagicType.GeoManipulation])
	SEnvir.AddMagicRestrictionToMap('调控室【普通】', [MagicType.GeoManipulation])
	SEnvir.AddMagicRestrictionToMap('调控室【地狱】', [MagicType.GeoManipulation])
	SEnvir.AddMagicRestrictionToMap('调控室【噩梦】', [MagicType.GeoManipulation])
	SEnvir.AddMagicRestrictionToMap('赤月恶魔洞穴【普通】', [MagicType.GeoManipulation])
	SEnvir.AddMagicRestrictionToMap('赤月恶魔洞穴【噩梦】', [MagicType.GeoManipulation])
	SEnvir.AddMagicRestrictionToMap('赤月恶魔洞穴【地狱】', [MagicType.GeoManipulation])
	SEnvir.AddMagicRestrictionToMap('潘夜神殿【普通】', [MagicType.GeoManipulation])
	SEnvir.AddMagicRestrictionToMap('潘夜神殿【噩梦】', [MagicType.GeoManipulation])
	SEnvir.AddMagicRestrictionToMap('潘夜神殿【地狱】', [MagicType.GeoManipulation])
	SEnvir.AddMagicRestrictionToMap('潘夜石窟【普通】', [MagicType.GeoManipulation])
	SEnvir.AddMagicRestrictionToMap('潘夜石窟【噩梦】', [MagicType.GeoManipulation])
	SEnvir.AddMagicRestrictionToMap('潘夜石窟【地狱】', [MagicType.GeoManipulation])
	SEnvir.AddMagicRestrictionToMap('真天宫【普通】', [MagicType.GeoManipulation])
	SEnvir.AddMagicRestrictionToMap('真天宫【噩梦】', [MagicType.GeoManipulation])
	SEnvir.AddMagicRestrictionToMap('真天宫【地狱】', [MagicType.GeoManipulation])
	SEnvir.AddMagicRestrictionToMap('黑度宫【普通】', [MagicType.GeoManipulation])
	SEnvir.AddMagicRestrictionToMap('黑度宫【噩梦】', [MagicType.GeoManipulation])
	SEnvir.AddMagicRestrictionToMap('黑度宫【地狱】', [MagicType.GeoManipulation])
	SEnvir.AddMagicRestrictionToMap('诺玛勇士坟墓【普通】', [MagicType.GeoManipulation])
	SEnvir.AddMagicRestrictionToMap('诺玛勇士坟墓【噩梦】', [MagicType.GeoManipulation])
	SEnvir.AddMagicRestrictionToMap('诺玛勇士坟墓【地狱】', [MagicType.GeoManipulation])
	SEnvir.AddMagicRestrictionToMap('地下魔宫【普通】', [MagicType.GeoManipulation])
	SEnvir.AddMagicRestrictionToMap('地下魔宫【噩梦】', [MagicType.GeoManipulation])
	SEnvir.AddMagicRestrictionToMap('地下魔宫【地狱】', [MagicType.GeoManipulation])


#所有MagicType
'''
        [Description("置空")]
        None,

        #region 战士
        /// <summary>
        /// 基本剑术
        /// </summary>
        [Description("基本剑术")]
        Swordsmanship = 100,

        /// <summary>
        /// 运气术
        /// </summary>
        [Description("运气术")]
        PotionMastery = 101,

        /// <summary>
        /// 攻杀剑术
        /// </summary>
        [Description("攻杀剑术")]
        Slaying = 102,

        /// <summary>
        /// 刺杀剑术
        /// </summary>
        [Description("刺杀剑术")]
        Thrusting = 103,

        /// <summary>
        /// 半月弯刀
        /// </summary>
        [Description("半月弯刀")]
        HalfMoon = 104,

        /// <summary>
        /// 野蛮冲撞
        /// </summary>
        [Description("野蛮冲撞")]
        ShoulderDash = 105,

        /// <summary>
        /// 烈火剑法
        /// </summary>
        [Description("烈火剑法")]
        FlamingSword = 106,

        /// <summary>
        /// 翔空剑法
        /// </summary>
        [Description("翔空剑法")]
        DragonRise = 107,

        /// <summary>
        /// 莲月剑法
        /// </summary>
        [Description("莲月剑法")]
        BladeStorm = 108,

        /// <summary>
        /// 十方斩
        /// </summary>
        [Description("十方斩")]
        DestructiveSurge = 109,

        /// <summary>
        /// 乾坤大挪移
        /// </summary>
        [Description("乾坤大挪移")]
        Interchange = 110,

        /// <summary>
        /// 铁布衫
        /// </summary>
        [Description("铁布衫")]
        Defiance = 111,

        /// <summary>
        /// 斗转星移
        /// </summary>
        [Description("斗转星移")]
        Beckon = 112,

        /// <summary>
        /// 破血狂杀
        /// </summary>
        [Description("破血狂杀")]
        Might = 113,

        /// <summary>
        /// 快刀斩马
        /// </summary>
        [Description("快刀斩马")]
        SwiftBlade = 114,

        /// <summary>
        /// 狂暴冲撞
        /// </summary>
        [Description("狂暴冲撞(无效)")]
        Assault = 115,

        /// <summary>
        /// 金刚之躯
        /// </summary>
        [Description("金刚之躯")]
        Endurance = 116,

        /// <summary>
        /// 移花接木
        /// </summary>
        [Description("移花接木")]
        ReflectDamage = 117,

        /// <summary>
        /// 泰山压顶
        /// </summary>
        [Description("泰山压顶")]
        Fetter = 118,

        /// <summary>
        /// 旋风斩
        /// </summary>
        [Description("旋风斩(无效)")]
        SwirlingBlade = 119,

        /// <summary>
        /// 君临步
        /// </summary>
        [Description("君临步")]
        ReigningStep = 120,

        /// <summary>
        /// 屠龙斩
        /// </summary>
        [Description("屠龙斩(Z版技能)")]
        MaelstromBlade = 121,

        /// <summary>
        /// 高级运气术
        /// </summary>
        [Description("高级运气术(Z版技能)")]
        AdvancedPotionMastery = 122,

        /// <summary>
        /// 挑衅
        /// </summary>
        [Description("挑衅")]
        MassBeckon = 123,

        /// <summary>
        /// 天雷锤
        /// </summary>
        [Description("天雷锤")]
        SeismicSlam = 124,

        /// <summary>
        /// 空破斩
        /// </summary>
        [Description("空破斩")]
        CrushingWave = 125,

        /// <summary>
        /// 无敌
        /// </summary>
        [Description("无敌")]
        Invincibility = 126,

        #endregion

        #region 法师
        /// <summary>
        /// 火球术
        /// </summary>
        [Description("火球术")]
        FireBall = 201,

        /// <summary>
        /// 霹雳掌
        /// </summary>
        [Description("霹雳掌")]
        LightningBall = 202,

        /// <summary>
        /// 冰月神掌
        /// </summary>
        [Description("冰月神掌")]
        IceBolt = 203,

        /// <summary>
        /// 风掌
        /// </summary>
        [Description("风掌")]
        GustBlast = 204,

        /// <summary>
        /// 抗拒火环
        /// </summary>
        [Description("抗拒火环")]
        Repulsion = 205,

        /// <summary>
        /// 诱惑之光
        /// </summary>
        [Description("诱惑之光")]
        ElectricShock = 206,

        /// <summary>
        /// 瞬息移动
        /// </summary>
        [Description("瞬息移动")]
        Teleportation = 207,

        /// <summary>
        /// 大火球
        /// </summary>
        [Description("大火球")]
        AdamantineFireBall = 208,

        /// <summary>
        /// 雷电术
        /// </summary>
        [Description("雷电术")]
        ThunderBolt = 209,

        /// <summary>
        /// 冰月震天
        /// </summary>
        [Description("冰月震天")]
        IceBlades = 210,

        /// <summary>
        /// 击风
        /// </summary>
        [Description("击风")]
        Cyclone = 211,

        /// <summary>
        /// 地狱火
        /// </summary>
        [Description("地狱火")]
        ScortchedEarth = 212,

        /// <summary>
        /// 疾光电影
        /// </summary>
        [Description("疾光电影")]
        LightningBeam = 213,

        /// <summary>
        /// 冰沙掌
        /// </summary>
        [Description("冰沙掌")]
        FrozenEarth = 214,

        /// <summary>
        /// 风震天
        /// </summary>
        [Description("风震天")]
        BlowEarth = 215,

        /// <summary>
        /// 火墙
        /// </summary>
        [Description("火墙")]
        FireWall = 216,

        /// <summary>
        /// 圣言术
        /// </summary>
        [Description("圣言术")]
        ExpelUndead = 217,

        /// <summary>
        /// 移形换位
        /// </summary>
        [Description("移形换位")]
        GeoManipulation = 218,

        /// <summary>
        /// 魔法盾
        /// </summary>
        [Description("魔法盾")]
        MagicShield = 219,

        /// <summary>
        /// 爆裂火焰
        /// </summary>
        [Description("爆裂火焰")]
        FireStorm = 220,

        /// <summary>
        /// 地狱雷光
        /// </summary>
        [Description("地狱雷光")]
        LightningWave = 221,

        /// <summary>
        /// 冰咆哮
        /// </summary>
        [Description("冰咆哮")]
        IceStorm = 222,

        /// <summary>
        /// 龙卷风
        /// </summary>
        [Description("龙卷风")]
        DragonTornado = 223,

        /// <summary>
        /// 魄冰刺
        /// </summary>
        [Description("魄冰刺")]
        GreaterFrozenEarth = 224,

        /// <summary>
        /// 怒神霹雳
        /// </summary>
        [Description("怒神霹雳")]
        ChainLightning = 225,

        /// <summary>
        /// 焰天火雨
        /// </summary>
        [Description("焰天火雨")]
        MeteorShower = 226,

        /// <summary>
        /// 凝血离魂
        /// </summary>
        [Description("凝血离魂")]
        Renounce = 227,

        /// <summary>
        /// 旋风墙
        /// </summary>
        [Description("旋风墙")]
        Tempest = 228,

        /// <summary>
        /// 天打雷劈
        /// </summary>
        [Description("天打雷劈")]
        JudgementOfHeaven = 229,

        /// <summary>
        /// 电闪雷鸣
        /// </summary>
        [Description("电闪雷鸣")]
        ThunderStrike = 230,

        /// <summary>
        /// 透心链
        /// </summary>
        [Description("透心链(无效)")]
        RayOfLight = 231,

        /// <summary>
        /// 混元掌
        /// </summary>
        [Description("混元掌(无效)")]
        BurstOfEnergy = 232,

        /// <summary>
        /// 魔光盾
        /// </summary>
        [Description("魔光盾(无效)")]
        ShieldOfPreservation = 233,

        /// <summary>
        /// 焚魂魔功
        /// </summary>
        [Description("焚魂魔功(无效)")]
        RetrogressionOfEnergy = 234,

        /// <summary>
        /// 魔爆术
        /// </summary>
        [Description("魔爆术(无效)")]
        FuryBlast = 235,

        /// <summary>
        /// 地狱魔焰
        /// </summary>
        [Description("地狱魔焰(无效)")]
        TempestOfUnstableEnergy = 236,

        /// <summary>
        /// 分身术
        /// </summary>
        [Description("分身术")]
        MirrorImage = 237,

        /// <summary>
        /// 高级凝血离魂
        /// </summary>
        [Description("高级凝血离魂(Z版技能)")]
        AdvancedRenounce = 238,

        /// <summary>
        /// 护身冰环
        /// </summary>
        [Description("护身冰环")]
        FrostBite = 239,

        /// <summary>
        /// 天之怒火
        /// </summary>
        [Description("天之怒火")]
        Asteroid = 240,

        /// <summary>
        /// 离魂邪风
        /// </summary>
        [Description("离魂邪风")]
        ElementalHurricane = 241,

        /// <summary>
        /// 护身法盾
        /// </summary>
        [Description("护身法盾")]
        SuperiorMagicShield = 242,

        /// <summary>
        /// 冰雨
        /// </summary>
        [Description("冰雨")]
        IceRain = 243,

        #endregion

        #region 道士
        /// <summary>
        /// 治愈术
        /// </summary>
        [Description("治愈术")]
        Heal = 300,

        /// <summary>
        /// 精神力战法
        /// </summary>
        [Description("精神力战法")]
        SpiritSword = 301,

        /// <summary>
        /// 施毒术
        /// </summary>
        [Description("施毒术")]
        PoisonDust = 302,

        /// <summary>
        /// 灵魂火符
        /// </summary>
        [Description("灵魂火符")]
        ExplosiveTalisman = 303,

        /// <summary>
        /// 月魂断玉
        /// </summary>
        [Description("月魂断玉")]
        EvilSlayer = 304,

        /// <summary>
        /// 隐身术
        /// </summary>
        [Description("隐身术")]
        Invisibility = 305,

        /// <summary>
        /// 幽灵盾
        /// </summary>
        [Description("幽灵盾")]
        MagicResistance = 306,

        /// <summary>
        /// 集体隐身术
        /// </summary>
        [Description("集体隐身术")]
        MassInvisibility = 307,

        /// <summary>
        /// 月魂灵波
        /// </summary>
        [Description("月魂灵波")]
        GreaterEvilSlayer = 308,

        /// <summary>
        /// 神圣战甲术
        /// </summary>
        [Description("神圣战甲术")]
        Resilience = 309,

        /// <summary>
        /// 困魔咒
        /// </summary>
        [Description("困魔咒")]
        TrapOctagon = 310,

        /// <summary>
        /// 空拳刀法
        /// </summary>
        [Description("空拳刀法")]
        TaoistCombatKick = 311,

        /// <summary>
        /// 强魔震法
        /// </summary>
        [Description("强魔震法")]
        ElementalSuperiority = 312,

        /// <summary>
        /// 群体治愈术
        /// </summary>
        [Description("群体治愈术")]
        MassHeal = 313,

        /// <summary>
        /// 猛虎强势
        /// </summary>
        [Description("猛虎强势")]
        BloodLust = 314,

        /// <summary>
        /// 回生术
        /// </summary>
        [Description("回生术")]
        Resurrection = 315,

        /// <summary>
        /// 云寂术
        /// </summary>
        [Description("云寂术")]
        Purification = 316,

        /// <summary>
        /// 妙影无踪
        /// </summary>
        [Description("妙影无踪")]
        Transparency = 317,

        /// <summary>
        /// 阴阳法环
        /// </summary>
        [Description("阴阳法环")]
        CelestialLight = 318,

        /// <summary>
        /// 养生术
        /// </summary>
        [Description("养生术")]
        EmpoweredHealing = 319,

        /// <summary>
        /// 吸星大法
        /// </summary>
        [Description("吸星大法")]
        LifeSteal = 320,

        /// <summary>
        /// 灭魂火符
        /// </summary>
        [Description("灭魂火符")]
        ImprovedExplosiveTalisman = 321,

        /// <summary>
        /// 施毒大法
        /// </summary>
        [Description("施毒大法")]
        GreaterPoisonDust = 322,

        /// <summary>
        /// 迷魂大法
        /// </summary>
        [Description("迷魂大法")]
        Scarecrow = 323,

        /// <summary>
        /// 横扫千军
        /// </summary>
        [Description("横扫千军")]
        ThunderKick = 324,

        /// <summary>
        /// 神灵守护
        /// </summary>
        [Description("神灵守护(无效)")]
        DragonBreath = 325,

        /// <summary>
        /// 隐魂术
        /// </summary>
        [Description("隐魂术(Z版技能)")]
        MassTransparency = 326,

        /// <summary>
        /// 月明波
        /// </summary>
        [Description("月明波(Z版技能)")]
        GreaterHolyStrike = 327,

        /// <summary>
        /// 群体灵魂火符
        /// </summary>
        [Description("群体灵魂火符(Z版技能)")]
        AugmentExplosiveTalisman = 328,

        /// <summary>
        /// 群体月魂灵波
        /// </summary>
        [Description("群体月魂灵波(Z版技能)")]
        AugmentEvilSlayer = 329,

        /// <summary>
        /// 强化云寂术
        /// </summary>
        [Description("强化云寂术(Z版技能)")]
        AugmentPurification = 330,

        /// <summary>
        /// 强化回生术
        /// </summary>
        [Description("强化回生术(Z版技能)")]
        OathOfThePerished = 331,

        /// <summary>
        /// 召唤骷髅
        /// </summary>
        [Description("召唤骷髅")]
        SummonSkeleton = 332,

        /// <summary>
        /// 召唤神兽
        /// </summary>
        [Description("召唤神兽")]
        SummonShinsu = 333,

        /// <summary>
        /// 超强召唤骷髅
        /// </summary>
        [Description("超强召唤骷髅")]
        SummonJinSkeleton = 334,

        /// <summary>
        /// 移花接玉
        /// </summary>
        [Description("移花接玉")]
        StrengthOfFaith = 335,

        /// <summary>
        /// 焰魔召唤术
        /// </summary>
        [Description("焰魔召唤术")]
        SummonDemonicCreature = 336,

        /// <summary>
        /// 魔焰强解术
        /// </summary>
        [Description("魔焰强解术")]
        DemonExplosion = 337,

        /// <summary>
        /// 传染
        /// </summary>
        [Description("传染")]
        Infection = 338,

        /// <summary>
        /// 地狱回疗
        /// </summary>
        [Description("地狱回疗(Z版技能)")]
        DemonicRecovery = 339,

        /// <summary>
        /// 虚弱化
        /// </summary>
        [Description("虚弱化")]
        Neutralize = 340,

        /// <summary>
        /// 强化虚弱化
        /// </summary>
        [Description("强化虚弱化(Z版技能)")]
        AugmentNeutralize = 341,

        /// <summary>
        /// 暗鬼阵
        /// </summary>
        [Description("暗鬼阵")]
        DarkSoulPrison = 342,

        #endregion

        #region 刺客
        /// <summary>
        /// 垂柳舞
        /// </summary>
        [Description("垂柳舞")]
        WillowDance = 401,

        /// <summary>
        /// 蔓藤舞
        /// </summary>
        [Description("蔓藤舞")]
        VineTreeDance = 402,

        /// <summary>
        /// 磨炼
        /// </summary>
        [Description("磨炼")]
        Discipline = 403,

        /// <summary>
        /// 毒云
        /// </summary>
        [Description("毒云")]
        PoisonousCloud = 404,

        /// <summary>
        /// 盛开
        /// </summary>
        [Description("盛开")]
        FullBloom = 405,

        /// <summary>
        /// 潜行
        /// </summary>
        [Description("潜行")]
        Cloak = 406,

        /// <summary>
        /// 白莲
        /// </summary>
        [Description("白莲")]
        WhiteLotus = 407,

        /// <summary>
        /// 满月恶狼
        /// </summary>
        [Description("满月恶狼")]
        CalamityOfFullMoon = 408,

        /// <summary>
        /// 亡灵束缚
        /// </summary>
        [Description("亡灵束缚")]
        WraithGrip = 409,

        /// <summary>
        /// 红莲
        /// </summary>
        [Description("红莲")]
        RedLotus = 410,

        /// <summary>
        /// 烈焰
        /// </summary>
        [Description("烈焰")]
        HellFire = 411,

        /// <summary>
        /// 血禅
        /// </summary>
        [Description("血禅")]
        PledgeOfBlood = 412,

        /// <summary>
        /// 血之盟约
        /// </summary>
        [Description("血之盟约")]
        Rake = 413,

        /// <summary>
        /// 月季
        /// </summary>
        [Description("月季")]
        SweetBrier = 414,

        /// <summary>
        /// 亡灵替身
        /// </summary>
        [Description("亡灵替身")]
        SummonPuppet = 415,

        /// <summary>
        /// 孽报
        /// </summary>
        [Description("孽报")]
        Karma = 416,

        /// <summary>
        /// 亡灵之手
        /// </summary>
        [Description("亡灵之手")]
        TouchOfTheDeparted = 417,

        /// <summary>
        /// 残月之乱
        /// </summary>
        [Description("残月之乱")]
        WaningMoon = 418,

        /// <summary>
        /// 鬼灵步
        /// </summary>
        [Description("鬼灵步")]
        GhostWalk = 419,

        /// <summary>
        /// 神机妙算
        /// </summary>
        [Description("神机妙算")]
        ElementalPuppet = 420,

        /// <summary>
        /// 深渊
        /// </summary>
        [Description("深渊")]
        Rejuvenation = 421,

        /// <summary>
        /// 决意
        /// </summary>
        [Description("决意")]
        Resolution = 422,

        /// <summary>
        /// 切换
        /// </summary>
        [Description("切换(未完成)")]
        ChangeOfSeasons = 423,

        /// <summary>
        /// 解放
        /// </summary>
        [Description("解放")]
        Release = 424,

        /// <summary>
        /// 新月爆炎龙
        /// </summary>
        [Description("新月爆炎龙")]
        FlameSplash = 425,

        /// <summary>
        /// 百花盛开
        /// </summary>
        [Description("百花盛开(Z版技能)")]
        BloodyFlower = 426,

        /// <summary>
        /// 心机一转
        /// </summary>
        [Description("心机一转")]
        TheNewBeginning = 427,

        /// <summary>
        /// 鹰击
        /// </summary>
        [Description("鹰击")]
        DanceOfSwallow = 428,

        /// <summary>
        /// 黄泉旅者
        /// </summary>
        [Description("黄泉旅者")]
        DarkConversion = 429,

        /// <summary>
        /// 狂涛涌泉
        /// </summary>
        [Description("狂涛涌泉")]
        DragonRepulse = 430,

        /// <summary>
        /// 修罗降临
        /// </summary>
        [Description("修罗降临")]
        AdventOfDemon = 431,

        /// <summary>
        /// 罗刹降临
        /// </summary>
        [Description("罗刹降临")]
        AdventOfDevil = 432,

        /// <summary>
        /// 深渊苦海
        /// </summary>
        [Description("深渊苦海")]
        Abyss = 433,

        /// <summary>
        /// 日闪
        /// </summary>
        [Description("日闪")]
        FlashOfLight = 434,

        /// <summary>
        /// 隐沦
        /// </summary>
        [Description("隐沦")]
        Stealth = 435,

        /// <summary>
        /// 风之闪避
        /// </summary>
        [Description("风之闪避")]
        Evasion = 436,

        /// <summary>
        /// 风之守护
        /// </summary>
        [Description("风之守护")]
        RagingWind = 437,

        /// <summary>
        /// 高级百花盛开
        /// </summary>
        [Description("高级百花盛开(Z版技能)")]
        AdvancedBloodyFlower = 438,

        /// <summary>
        /// 最后抵抗
        /// </summary>
        [Description("最后抵抗")]
        Massacre = 439,

        /// <summary>
        /// 暗影艺术
        /// </summary>
        [Description("暗影艺术")]
        ArtOfShadows = 440,
        /// <summary>
        /// 集中
        /// </summary>
        [Description("集中")]
        Concentration = 441,
        /// <summary>
        /// 业火
        /// </summary>
        [Description("业火")]
        SwordOfVengeance = 442,
        /// <summary>
        /// 千刃杀风
        /// </summary>
        [Description("千刃杀风")]
        ThousandBlades = 443,

        #endregion

'''