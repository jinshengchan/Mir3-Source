using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using Library;
using Server.Models;

namespace Server.Envir
{
    /// <summary>
    /// 假人聊天模块：变量模板、社交对话、词池管理。
    /// BotManager.cs 只需调用 ProcessBotSocialModule / LoadBotChatConfig 等公共入口。
    /// </summary>
    public static partial class BotManager
    {
        // ─────────────────────── 内部类型 ───────────────────────

        private sealed class BotChatDialogSet
        {
            public List<string> Openers = new List<string>();
            public List<string> Replies = new List<string>();
        }

        private sealed class BotPendingChatReply
        {
            public uint ReplyToObjectID;
            public string Text;
            public DateTime ReplyTime;
            public DateTime ExpireTime;
            public string SpeakerName;
        }

        // ─────────────────────── 常量 ───────────────────────

        private const string BotChatTopicCombat = "combat";
        private const string BotChatTopicLoot = "loot";
        private const string BotChatTopicGroup = "group";
        private const string BotChatTopicGold = "gold";
        private const string BotChatTopicGeneral = "general";

        private const int BotSocialMinIntervalSeconds = 30;
        private const int BotSocialMaxIntervalSeconds = 60;
        private const int BotSocialInitialDelayMinSeconds = 30;
        private const int BotSocialInitialDelayMaxSeconds = 60;
        private const int BotSocialReplyMinDelayMs = 1200;
        private const int BotSocialReplyMaxDelayMs = 2800;
        private const int BotSocialReplyExpireSeconds = 12;
        private const int BotSocialNearbyRange = 12;

        // ─────────────────────── 默认词池 ───────────────────────

        private static readonly Dictionary<string, BotChatDialogSet> BotDefaultChatDialogs
            = new Dictionary<string, BotChatDialogSet>(StringComparer.OrdinalIgnoreCase)
        {
            {
                BotChatTopicCombat,
                CreateBotChatDialogSet(
                    new[]
                    {
                        "上上上！别给它喘气的机会", "这怪刮痧呢，随缘打吧", "哎哟这怪的攻击有点东西",
                        "法师你远程输出就行，别凑过来送", "道士先给这怪上个毒，磨死它",
                        "这怪掉血挺快的，大家加把劲", "哎我今天手感好差，砍空好几刀了",
                        "稳住稳住，这波不急", "这怪经验还可以，多刷几只",
                        "小心这怪会暴击，血少的注意点", "这只怪血厚得离谱……",
                        "法师火球铺起来啊！别偷懒", "前排顶住，后排放心输出",
                        "这怪走路慢得跟乌龟似的，追都追不上", "我蓝不够了，省着点放技能",
                        "来来来集火这只，别分散火力", "这只弱爆了，闭着眼打",
                        "妈呀这怪攻速好快，我血条都在抖", "打完这只我去买药，快见底了",
                        "今天运气不错，怪一个接一个送", "兄弟们配合好啊，清得飞快",
                        "这玩意儿什么抗性啊，打不动", "快快快，别让旁边那只凑过来",
                        "前面那一片全是怪，冲啊", "别打那只大的，先清小的",
                        "这怪刷新好快，感觉永远打不完", "一阵风就带走了，下一只",
                        "这怪掉的东西应该还行吧", "小心脚下别被卡住了",
                        "大家站位散一点，别挤一堆", "这怪也太丑了，看着就来气",
                        "打Boss等练高点再来，现在纯送", "我都怀疑这怪是不是开挂了",
                        "这经验给得也太抠了", "好耶又一只经验宝宝",
                        "你这走位能再风骚点吗", "战法道配合完美，继续继续",
                        // ── 变量模板 ──
                        "这{怪物}也太硬了吧，打了半天不掉血", "{怪物}又来了，烦死了",
                        "我{等级}级了还没见过Boss，难受", "这{怪物}经验给得还可以",
                        "谁打{怪物}也掉线了？笑死", "这只{怪物}比上一只难打多了",
                        "{队友}你快跟上，别掉队了", "{地图}这地方怪也太多了吧",
                        "你们有没有觉得{怪物}越来越难打了", "这{怪物}一巴掌就快把我秒了",
                    },
                    new[]
                    {
                        "来了一起上，早点清完早点歇", "收到收到，马上就位",
                        "你负责左边那只，我右边", "行，我先把毒上了",
                        "稳住，我的蓝还够撑一阵", "哈哈这怪也太脆了",
                        "我这就来，别急", "你打你的，别管我",
                        "哎呀刚才差点被打死，吓出一身冷汗", "这怪我打了半天了，你帮我分担点",
                        "好嘞，集火就集火", "没事没事，能打",
                        "你这伤害有点刮啊兄弟", "法师大佬带我飞",
                        "你先撤，我来顶", "收到，前面那只我来收",
                        "别喊了别喊了，在打了在打了", "行行行，马上马上",
                        "这怪我也觉得难缠", "你蓝够吗？不够先喝瓶",
                        "打完这个我去补给，你们继续", "配合默契啊今天",
                        "放心，死不了", "这只我单挑够了，你去打别的",
                        "别怕别怕，伤害不够而已", "行，听你指挥",
                        "我药还多，不慌", "再来再来，手感刚热起来",
                        // ── 变量模板（回复时 {玩家}=说话者名字）──
                        "行{玩家}，你先打那只{怪物}", "{玩家}你注意血条啊",
                        "收到{玩家}，我这就来", "你放心{玩家}，我帮你顶",
                        "{玩家}你蓝够吗？我药还多", "哈哈{玩家}说得对",
                        "{玩家}别急，马上清完了", "{玩家}这波配合不错",
                    })
            },
            {
                BotChatTopicLoot,
                CreateBotChatDialogSet(
                    new[]
                    {
                        "哎哎哎地上亮了！我去看看", "掉好东西了！等我捡回来",
                        "让让让，这块掉落归我了", "有东西！别抢啊先让我看看",
                        "地上这一坨是什么？我去摸摸", "捡完这波我感觉要发财",
                        "你们继续打，掉落我包了", "这掉的啥啊，看半天没看懂",
                        "发财了发财了！别拦我", "这边也有一个，捡不完根本捡不完",
                        "你们先顶住，我捡个东西马上回来", "这怪掉的东西还挺好",
                        "我先捡为敬了啊", "地上这么多东西谁不掉的？",
                        "完了完了，背包快满了", "捡捡捡，闲着也是闲着",
                        "这个颜色看着像好东西", "捡完继续，不能耽误进度",
                        "哎呀捡到个破烂……", "捡了捡了，你们别停",
                        "让我过去让我过去，掉落在那边", "又掉又掉，今天掉落率不错啊",
                        "这东西能卖多少钱？", "地上还有谁的东西？没人要我就捡了啊",
                        "终于捡到了，不容易", "你们打你们的，捡东西交给我",
                        "捡个东西怎么这么费劲，怪老踩着", "这掉落被怪堵住了，等它挪开我再捡",
                        "啧，又是些卖店货",
                        // ── 变量模板 ──
                        "{怪物}掉的东西能卖多少？", "在{地图}捡了好几次了",
                        "背包快满了，回去卖一波杂物", "这{怪物}掉落还行",
                    },
                    new[]
                    {
                        "你去吧，我帮你看着", "捡完快回来啊，别磨蹭",
                        "哎好的好的，我不动", "捡到啥好东西了？分我点",
                        "你慢慢捡，我们打怪不差这点时间", "行你去，别走太远",
                        "捡完赶紧回来补药", "别光顾着捡，怪上来了",
                        "没事，这波我扛得住", "你去捡，那只小的我来清",
                        "看到好东西记得吱一声", "捡到极品了吗？",
                        "别捡了别捡了，先清完这波", "去吧去吧，动作快点",
                        "捡完赶紧跟上啊", "行，等你的",
                        "你捡你的，别耽误输出", "那个东西我也要！",
                        "捡到啥了给我看看", "哈哈发财了吧",
                        "你还挺积极", "别光看地上，注意血条",
                        "捡完赶紧归队", "等你回来接着推",
                        "东西太多捡不过来吧？", "没捡到就算了，别恋战",
                        // ── 变量模板（回复时 {玩家}=说话者名字）──
                        "行{玩家}，你快捡", "{玩家}捡到啥了？",
                        "你慢慢捡{玩家}，我看着", "{玩家}别恋战啊",
                    })
            },
            {
                BotChatTopicGroup,
                CreateBotChatDialogSet(
                    new[]
                    {
                        "集合集合！别各打各的了", "队长你走慢点，我跟不上了",
                        "这队伍配置不错啊，继续刷", "人齐了没？齐了就走",
                        "法师站后排去，别冲前面送", "大家跟紧了，别走散",
                        "这队也太猛了，怪根本不够打", "有人掉队了，等等啊",
                        "谁没跟上？回头看看", "组满人就是爽，清怪像割草",
                        "队长这路线选得好", "换张图？这张刷腻了",
                        "大家药都带够了吗？", "今天这个队配置完美",
                        "走走走，别在城里待着了", "等下等等，还有个法师没上线",
                        "新来的跟紧老队员", "这队战法道都有，稳了稳了",
                        "大家注意配合，别抢怪", "先清完这片再休息",
                        "谁药不够跟我说，我匀你点", "差不多了吧，准备出发",
                        "别在安全区发呆了，走起", "队长带得飞快，我跟得有点吃力",
                        "你们走慢点，我还要买药呢", "新图新气象，冲冲冲",
                        "换个队长？我有点迷路了", "这队伍活人好多啊",
                        "有没有人想换个图刷？", "行，继续跟着队里混",
                        "组队刷就是效率高",
                        // ── 变量模板 ──
                        "在{地图}组队刷怪真爽", "这队配置不错，{队友}输出挺猛",
                        "队长{队长}走太快了吧", "我都{等级}级了还是这么穷",
                        "{队友}跟上，别掉队", "跟着{队长}混稳得很",
                    },
                    new[]
                    {
                        "来了来了，在路上了", "收到，马上归队",
                        "跟上了跟上了，别催", "我不怕，跟着队里走就行",
                        "行，听队长安排", "好的好的，我这边搞定了就过去",
                        "跟上跟上，不掉队", "我这马上完事，等我10秒",
                        "收到收到，不乱跑", "别急别急，我追得上",
                        "OK，随时准备出发", "我也觉得这张图不错",
                        "行，再刷半小时就撤", "跟着大佬混就是舒服",
                        "你走你走，我殿后", "收到，保持队形",
                        "这队真给力", "不急不急，稳步推进",
                        "我在这呢，没掉队", "放心，跟得上",
                        "行行行，你们决定", "没问题，跟着走就是了",
                        "先清完这片再说", "好嘞，等你们信号",
                        // ── 变量模板（回复时 {玩家}=说话者名字）──
                        "收到{玩家}，马上跟上", "行{玩家}，跟着你走",
                        "{玩家}你去哪我跟到哪", "好的{玩家}，保持队形",
                    })
            },
            {
                BotChatTopicGold,
                CreateBotChatDialogSet(
                    new[]
                    {
                        "钱包比脸还干净，努力搬砖中", "再不打钱连药都买不起了",
                        "今天目标：攒够换武器的钱", "这破怪掉的金币也太少了吧",
                        "又穷又菜说的就是我", "药钱都快掏不出了，赶紧攒钱",
                        "穷鬼路过，别拦我搬砖", "金币啊金币，你何时才能填满我的口袋",
                        "打金打金，为了明天更好的生活", "金币不够用啊，得省着花",
                        "卖了一波杂物，回血了", "今天掉落太差了，全是白板",
                        "赚钱好慢，心累", "有没有人组队打金？效率高点",
                        "我怀疑这图根本不掉金币", "攒了好久终于攒够了买药钱",
                        "这怪不掉金只掉破烂，亏了亏了", "谁能借我点药钱……算了还是自己赚吧",
                        "再刷十只我就回城卖东西了", "金币到账的声音真好听",
                        "卖杂物赚了点小钱，蚊子腿也是肉", "打金模式启动！",
                        "背包快满了，回去卖一波", "药太贵了，赚钱速度赶不上花",
                        "唉有钱人真多，羡慕", "今天运气还行，捡到个能卖钱的",
                        "又穷了一天，习惯就好", "搬砖人搬砖魂",
                        "金币不够花怎么办？在线等急", "再不赚钱我就要去卖装备了",
                        // ── 变量模板 ──
                        "我才{金币}了，穷得叮当响", "在{地图}搬砖真累",
                        "这{怪物}掉的金币也太少了吧", "我{等级}级了连买药的钱都没有",
                        "再刷二十只我就有买药钱了", "背包快满了，回去卖一波杂物",
                    },
                    new[]
                    {
                        "慢慢来，总能攒够的", "别急，先活下去再说",
                        "是啊这图掉率确实感人", "省着点花，药别乱喝",
                        "我也是穷鬼一枚", "坚持住，刷完这波就有钱了",
                        "加油加油，金币会有的", "习惯就好，打金人的日常",
                        "你这也太惨了吧哈哈", "没事，穷人有穷人的活法",
                        "打完回城卖一波就回血了", "慢慢攒，别想着一夜暴富",
                        "我这边也不富裕，互相体谅", "你先刷着，别想太多",
                        "省钱才是王道", "尽力了就行，别太勉强",
                        "我上次也是穷得叮当响，后来就好了", "别放弃，金币总会有的",
                        "打金嘛就是细水长流", "你背包里有没有能卖的？",
                        "卖了换药，先保证能打", "省药就是省钱",
                        "别太拼了，活着才能继续赚", "加油兄弟，挺你",
                        // ── 变量模板（回复时 {玩家}=说话者名字）──
                        "加油{玩家}，金币会有的", "慢慢来{玩家}，别急",
                        "{玩家}你背包里有能卖的吗？", "我也是穷鬼一枚{玩家}",
                    })
            },
            {
                BotChatTopicGeneral,
                CreateBotChatDialogSet(
                    new[]
                    {
                        "这地图逛了几十遍了，闭着眼都能走", "药还够，继续清",
                        "今天状态不错，继续推", "前面还行，往里再看看",
                        "这片怪刷得还挺快的", "等级又涨了，离出师又近了一步",
                        "感觉自己的伤害又高了亿点点", "今天有没有什么好活动？",
                        "这地图的BGM听着还挺带感的", "你们有没有觉得怪越来越难打了",
                        "我好想换个技能啊，这个太弱了", "刷怪刷累了，想找人聊天",
                        "有没有人组队啊，一个人刷太无聊", "这装备是不是该换了？感觉打不动怪了",
                        "法师和道士谁刷怪更快？", "这个图来来回回走了好几遍了",
                        "快升级了吧？感觉经验快满了", "今天手气不错，怪一个接一个送",
                        "有人打到过极品装备吗？", "我怀疑这游戏 RNG 针对我",
                        "刷了好久都没见过Boss", "这张图我熟，闭着眼都能清完",
                        "有没有好打的图推荐一下？", "这游戏真肝啊",
                        "完了药又要喝完了", "等级高了之后刷怪会不会更快？",
                        "等有钱了我要买一套神装", "有没有人一起切磋一下？",
                        "新手路过，求带", "大家今天都打到什么好东西了？",
                        // ── 关系感知台词（熟人打招呼） ──
                        "哟{玩家}，又见面了", "嘿{玩家}，今天也在这刷啊",
                        "{玩家}你也来这张图了？真巧", "老朋友又碰上了{玩家}",
                        // ── 关系感知台词（好友互动） ──
                        "老{玩家}！一起组队推一波？", "{玩家}你装备换了吧，看着好猛",
                        "{玩家}上次那波配合太溜了，再来再来", "老{玩家}带带我呗",
                        "{玩家}你这等级升得真快啊", "嘿{玩家}，有没有啥好图推荐",
                        // ── 变量模板 ──
                        "这{地图}逛了无数遍了，闭着眼都能走", "我是{职业}，刷怪就是费蓝",
                        "都{等级}级了还在{地图}混", "有没有{地图}的老玩家？带带我",
                        "这{怪物}好难打，有没有人组队", "感觉{地图}经验还行",
                        "刚升到{等级}级，爽", "今天在{地图}运气不错",
                        // ── 关系感知变量模板 ──
                        "{玩家}你觉得{地图}刷怪怎么样？", "老{玩家}又一起刷{地图}了",
                    },
                    new[]
                    {
                        "嗯，这里还能刷一阵", "行，继续往前推",
                        "稳着来，别着急", "看起来还能再打一轮",
                        "别催，让怪刷新一下", "是啊，越往后怪越猛",
                        "等级不够先别去高级图", "慢慢来，急也没用",
                        "我上次在那边打到个不错的", "装备能穿就穿，别太挑",
                        "嗯确实，一个人打确实无聊", "同感同感",
                        "加油，快了快了", "别想太多，先刷完这片",
                        "装备差就先去低级图刷", "慢慢升，总有出头之日",
                        "有道理，回头我试试", "行，跟你混了",
                        "哈哈我也是", "差不多该回城了吧",
                        "今天刷够了，该休息了", "别太拼，注意血条",
                        "我也在想换图", "嗯嗯继续继续",
                        "差不多行了，别贪", "还好还好，还能打",
                        "说得有道理", "行吧听你的",
                        // ── 关系感知回复（熟人） ──
                        "可不是嘛{玩家}，最近老碰见你", "{玩家}你也在这？一起刷呗",
                        "哈哈{玩家}，缘分啊", "又见面了{玩家}，今天运气怎么样",
                        // ── 关系感知回复（好友） ──
                        "老{玩家}！走走走一起", "{玩家}你来了我就放心了",
                        "没问题{玩家}，随时", "老{玩家}你今天打啥呢？",
                        "行啊{玩家}，老搭档了", "哈哈老{玩家}，必须配合",
                        // ── 关系感知回复（仇敌冷淡） ──
                        "...", "哦", "无所谓", "关你什么事",
                        // ── 变量模板（回复时 {玩家}=说话者名字）──
                        "说得对{玩家}", "嗯嗯{玩家}继续继续",
                        "{玩家}你多少级了？", "哈哈{玩家}我也是这么想的",
                        // ── 关系感知变量模板（熟人） ──
                        "{玩家}你在{地图}刷了多久了？", "老熟人了{玩家}，不用客气",
                    })
            },
        };

        // ─────────────────────── 运行时状态 ───────────────────────

        private static readonly Dictionary<string, BotChatDialogSet> _botChatDialogs
            = new Dictionary<string, BotChatDialogSet>(StringComparer.OrdinalIgnoreCase);

        // 假人主动说话节奏：ObjectID → 下次允许主动开口的时间
        private static readonly Dictionary<uint, DateTime> _botNextSocialTime
            = new Dictionary<uint, DateTime>();

        // 假人互聊的待回复状态：ObjectID → 延迟回复内容
        private static readonly Dictionary<uint, BotPendingChatReply> _botPendingChatReplies
            = new Dictionary<uint, BotPendingChatReply>();

        // 聊天配置文件路径（LoadBotChatConfig 内部使用）
        private static string botChatFilePath = "";

        // 关系感知：每个 bot 记住最近跟谁聊过什么（ObjectID → 最近聊天的话题）
        private static readonly Dictionary<uint, string> _botLastChatTopicWith
            = new Dictionary<uint, string>();

        // 关系感知：每个 bot 记住最近聊天对象（ObjectID → 最近聊天的 target ObjectID）
        private static readonly Dictionary<uint, uint> _botLastChatTarget
            = new Dictionary<uint, uint>();

        // 每个话题的最近使用时间（防止连续说同一话题）
        private static readonly Dictionary<string, DateTime> _botLastTopicUseTime
            = new Dictionary<string, DateTime>(StringComparer.OrdinalIgnoreCase);

        // 话题冷却时间（同一 bot 连续两次不同话题间的最短间隔）
        private const int BotTopicCooldownSeconds = 60;

        // ─────────────────────── 词池管理 ───────────────────────

        private static BotChatDialogSet CreateBotChatDialogSet(IEnumerable<string> openers, IEnumerable<string> replies)
        {
            var dialog = new BotChatDialogSet();

            if (openers != null)
                dialog.Openers.AddRange(openers.Where(x => !string.IsNullOrWhiteSpace(x)).Select(x => x.Trim()));

            if (replies != null)
                dialog.Replies.AddRange(replies.Where(x => !string.IsNullOrWhiteSpace(x)).Select(x => x.Trim()));

            return dialog;
        }

        /// <summary>
        /// 加载假人聊天配置：先用内置默认词池初始化，再从 假人聊天.txt 合并自定义台词。
        /// </summary>
        private static void LoadBotChatConfig()
        {
            try
            {
                _botChatDialogs.Clear();
                foreach (var pair in BotDefaultChatDialogs)
                    _botChatDialogs[pair.Key] = CreateBotChatDialogSet(pair.Value.Openers, pair.Value.Replies);

                botChatFilePath = ResolveBotChatFilePath();
                EnsureBotChatFileExists(botChatFilePath);

                if (!File.Exists(botChatFilePath))
                {
                    SEnvir.Log($"假人聊天配置不存在，当前回退到内置默认词池: {botChatFilePath}");
                    return;
                }

                string currentTopic = null;
                bool currentIsReply = false;
                int loadedLineCount = 0;

                foreach (string rawLine in File.ReadAllLines(botChatFilePath, Encoding.UTF8))
                {
                    if (string.IsNullOrWhiteSpace(rawLine))
                        continue;

                    string line = rawLine.Trim();
                    if (line.Length == 0 || line.StartsWith("#") || line.StartsWith("//") || line.StartsWith(";"))
                        continue;

                    if (line.StartsWith("[") && line.EndsWith("]"))
                    {
                        if (!TryResolveBotChatSection(line.Substring(1, line.Length - 2), out currentTopic, out currentIsReply))
                            currentTopic = null;

                        continue;
                    }

                    if (string.IsNullOrWhiteSpace(currentTopic))
                        continue;

                    BotChatDialogSet dialog;
                    if (!_botChatDialogs.TryGetValue(currentTopic, out dialog))
                    {
                        dialog = CreateBotChatDialogSet(null, null);
                        _botChatDialogs[currentTopic] = dialog;
                    }

                    List<string> targetLines = currentIsReply ? dialog.Replies : dialog.Openers;
                    if (targetLines.Any(x => string.Equals(x, line, StringComparison.OrdinalIgnoreCase)))
                        continue;

                    targetLines.Add(line);
                    loadedLineCount++;
                }

                SEnvir.Log($"假人聊天配置已加载: {botChatFilePath}, 自定义台词 {loadedLineCount} 条");
            }
            catch (Exception ex)
            {
                SEnvir.Log($"加载假人聊天配置失败: {ex.Message}");
            }
        }

        private static string ResolveBotChatFilePath()
        {
            var candidates = new List<string>();

            try
            {
                if (!string.IsNullOrWhiteSpace(botFilePath))
                {
                    string fullBotPath = Path.IsPathRooted(botFilePath) ? botFilePath : Path.GetFullPath(botFilePath);
                    string botDir = Path.GetDirectoryName(fullBotPath);

                    if (!string.IsNullOrWhiteSpace(botDir))
                        candidates.Add(Path.Combine(botDir, "假人聊天.txt"));
                }
            }
            catch
            {
            }

            string baseDir = AppDomain.CurrentDomain.BaseDirectory;
            if (!string.IsNullOrWhiteSpace(baseDir))
                candidates.Add(Path.Combine(baseDir, "假人聊天.txt"));

            string currentDir = Environment.CurrentDirectory;
            if (!string.IsNullOrWhiteSpace(currentDir))
                candidates.Add(Path.Combine(currentDir, "假人聊天.txt"));

            string existingPath = candidates.FirstOrDefault(File.Exists);
            return existingPath ?? candidates.FirstOrDefault() ?? "假人聊天.txt";
        }

        private static void EnsureBotChatFileExists(string path)
        {
            if (string.IsNullOrWhiteSpace(path) || File.Exists(path))
                return;

            try
            {
                string directory = Path.GetDirectoryName(path);
                if (!string.IsNullOrWhiteSpace(directory) && !Directory.Exists(directory))
                    Directory.CreateDirectory(directory);

                File.WriteAllLines(path, BuildDefaultBotChatFileLines(), new UTF8Encoding(true));
                SEnvir.Log($"已自动创建假人聊天配置: {path}");
            }
            catch (Exception ex)
            {
                SEnvir.Log($"创建假人聊天配置失败: {ex.Message}");
            }
        }

        private static string[] BuildDefaultBotChatFileLines()
        {
            var lines = new List<string>
            {
                "# 假人聊天配置",
                "# 用法：每个分组一行一句；空行、#、;、// 开头的行会被忽略。",
                "# 当前版本修改后需要重启假人系统才会重新加载。",
                string.Empty,
            };

            AppendBotChatSection(lines, "战斗开场", BotDefaultChatDialogs[BotChatTopicCombat].Openers);
            AppendBotChatSection(lines, "战斗回复", BotDefaultChatDialogs[BotChatTopicCombat].Replies);
            AppendBotChatSection(lines, "拾取开场", BotDefaultChatDialogs[BotChatTopicLoot].Openers);
            AppendBotChatSection(lines, "拾取回复", BotDefaultChatDialogs[BotChatTopicLoot].Replies);
            AppendBotChatSection(lines, "组队开场", BotDefaultChatDialogs[BotChatTopicGroup].Openers);
            AppendBotChatSection(lines, "组队回复", BotDefaultChatDialogs[BotChatTopicGroup].Replies);
            AppendBotChatSection(lines, "打金开场", BotDefaultChatDialogs[BotChatTopicGold].Openers);
            AppendBotChatSection(lines, "打金回复", BotDefaultChatDialogs[BotChatTopicGold].Replies);
            AppendBotChatSection(lines, "闲聊开场", BotDefaultChatDialogs[BotChatTopicGeneral].Openers);
            AppendBotChatSection(lines, "闲聊回复", BotDefaultChatDialogs[BotChatTopicGeneral].Replies);

            return lines.ToArray();
        }

        private static void AppendBotChatSection(List<string> lines, string sectionName, IEnumerable<string> values)
        {
            lines.Add($"[{sectionName}]");

            if (values != null)
            {
                foreach (string value in values)
                {
                    if (string.IsNullOrWhiteSpace(value)) continue;
                    lines.Add(value.Trim());
                }
            }

            lines.Add(string.Empty);
        }

        private static bool TryResolveBotChatSection(string sectionName, out string topicKey, out bool isReply)
        {
            topicKey = null;
            isReply = false;

            if (string.IsNullOrWhiteSpace(sectionName))
                return false;

            string normalized = sectionName.Trim().Replace(" ", string.Empty);
            if (normalized.EndsWith("开场", StringComparison.OrdinalIgnoreCase))
            {
                isReply = false;
                normalized = normalized.Substring(0, normalized.Length - 2);
            }
            else if (normalized.EndsWith("回复", StringComparison.OrdinalIgnoreCase))
            {
                isReply = true;
                normalized = normalized.Substring(0, normalized.Length - 2);
            }
            else
            {
                return false;
            }

            switch (normalized.ToLowerInvariant())
            {
                case "战斗":
                case "combat":
                    topicKey = BotChatTopicCombat;
                    return true;
                case "拾取":
                case "掉落":
                case "loot":
                    topicKey = BotChatTopicLoot;
                    return true;
                case "组队":
                case "跟队":
                case "group":
                    topicKey = BotChatTopicGroup;
                    return true;
                case "打金":
                case "金币":
                case "gold":
                    topicKey = BotChatTopicGold;
                    return true;
                case "闲聊":
                case "普通":
                case "general":
                    topicKey = BotChatTopicGeneral;
                    return true;
                default:
                    return false;
            }
        }

        private static string GetRandomBotChatLine(string topic, bool reply)
        {
            BotChatDialogSet dialog;
            if (!_botChatDialogs.TryGetValue(topic ?? string.Empty, out dialog))
                _botChatDialogs.TryGetValue(BotChatTopicGeneral, out dialog);

            List<string> lines = reply ? dialog?.Replies : dialog?.Openers;
            if (lines == null || lines.Count == 0)
                return string.Empty;

            return lines[_botRandom.Next(lines.Count)];
        }

        // ─────────────────────── 社交模块入口 ───────────────────────

        /// <summary>
        /// 假人社交模块：按当前战斗/拾取/组队/打金场景，从 假人聊天.txt 里抽台词主动说话，
        /// 并给附近假人安排延迟回复，形成简单互聊。
        /// </summary>
        internal static void ProcessBotSocialModule(PlayerObject player)
        {
            if (!CanBotUseSocialChat(player)) return;
            if (!Config.BotEnableChat
                || !ShouldTriggerScaledBehavior(Config.BotChatFrequencyPercent, player.ObjectID,
                    SEnvir.Now.Ticks / TimeSpan.TicksPerSecond))
                return;

            if (TryProcessBotPendingChatReply(player))
                return;

            uint pid = player.ObjectID;
            DateTime nextSocialTime;
            if (!_botNextSocialTime.TryGetValue(pid, out nextSocialTime))
            {
                ScheduleNextBotSocialTime(player, BotSocialInitialDelayMinSeconds, BotSocialInitialDelayMaxSeconds);
                return;
            }

            if (SEnvir.Now < nextSocialTime)
                return;

            string topic = ResolveBotChatTopicWithSocial(player);

            // 关系感知：优先和熟人打招呼（10% 概率触发熟人专属开场白）
            string opener = TryGetRelationAwareOpener(player);
            if (string.IsNullOrWhiteSpace(opener))
                opener = GetRandomBotChatLine(topic, false);

            if (string.IsNullOrWhiteSpace(opener))
            {
                ScheduleNextBotSocialTime(player, BotSocialMinIntervalSeconds, BotSocialMaxIntervalSeconds);
                return;
            }

            opener = ExpandBotChatTemplate(opener, player);
            player.Chat(opener);
            RecordBotSocialMessage(player);
            ScheduleNextBotSocialTime(player, BotSocialMinIntervalSeconds, BotSocialMaxIntervalSeconds);

            // 记录社交记忆
            RecordSocialChat(player, topic);
            QueueBotChatReply(player, topic);
        }

        private static bool CanBotUseSocialChat(PlayerObject player)
        {
            return player != null
                   && !player.Dead
                   && player.Node != null
                   && player.Connection != null
                   && player.Connection.Connected
                   && player.Character != null
                   && player.CurrentMap != null
                   && player.CurrentMap.Info != null
                   && player.CurrentMap.Info.CanNoChat != true
                   && SEnvir.Now >= player.Character.Account.ChatBanExpiry;
        }

        private static bool TryProcessBotPendingChatReply(PlayerObject player)
        {
            if (player == null) return false;

            BotPendingChatReply pending;
            if (!_botPendingChatReplies.TryGetValue(player.ObjectID, out pending))
                return false;

            if (pending == null || SEnvir.Now > pending.ExpireTime)
            {
                _botPendingChatReplies.Remove(player.ObjectID);
                return false;
            }

            if (SEnvir.Now < pending.ReplyTime)
                return false;

            PlayerObject target = botPlayers.FirstOrDefault(x => x != null && x.ObjectID == pending.ReplyToObjectID);
            if (!CanBotUseSocialChat(target)
                || target.CurrentMap != player.CurrentMap
                || Functions.Distance(target.CurrentLocation, player.CurrentLocation) > BotSocialNearbyRange)
            {
                _botPendingChatReplies.Remove(player.ObjectID);
                return false;
            }

            _botPendingChatReplies.Remove(player.ObjectID);

            if (string.IsNullOrWhiteSpace(pending.Text))
            {
                ScheduleNextBotSocialTime(player, BotSocialMinIntervalSeconds, BotSocialMaxIntervalSeconds);
                return false;
            }

            string expandedReply = ExpandBotChatTemplate(pending.Text, player, pending.SpeakerName);
            player.Chat(expandedReply);
            RecordBotSocialMessage(player);
            ScheduleNextBotSocialTime(player, BotSocialMinIntervalSeconds, BotSocialMaxIntervalSeconds);
            return true;
        }

        private static void QueueBotChatReply(PlayerObject speaker, string topic)
        {
            if (speaker == null) return;

            string replyText = GetRandomBotChatLine(topic, true);
            if (string.IsNullOrWhiteSpace(replyText))
                return;

            List<PlayerObject> candidates = botPlayers
                .Where(x => x != null
                            && x != speaker
                            && CanBotUseSocialChat(x)
                            && x.CurrentMap == speaker.CurrentMap
                            && Functions.Distance(x.CurrentLocation, speaker.CurrentLocation) <= BotSocialNearbyRange)
                .OrderByDescending(x => speaker.GroupMembers != null && speaker.GroupMembers.Contains(x))
                .ThenByDescending(x => BotSocialMemory.IsKnownPlayer(x, speaker) ? 1 : 0)  // 熟人优先
                .ThenBy(x => Functions.Distance(x.CurrentLocation, speaker.CurrentLocation))
                .ToList();

            foreach (PlayerObject candidate in candidates)
            {
                // 仇敌 30% 概率不回复
                if (BotSocialMemory.ShouldIgnoreChat(candidate, speaker))
                    continue;

                BotPendingChatReply existing;
                if (_botPendingChatReplies.TryGetValue(candidate.ObjectID, out existing) && existing != null && SEnvir.Now <= existing.ExpireTime)
                    continue;

                // 关系感知：对熟人/好友选择关系感知回复（如果可用）
                string relationReply = TryGetRelationAwareReply(candidate, speaker, topic);
                string finalReplyText = !string.IsNullOrWhiteSpace(relationReply) ? relationReply : replyText;

                int delayMs = BotSocialReplyMinDelayMs;
                if (BotSocialReplyMaxDelayMs > BotSocialReplyMinDelayMs)
                    delayMs += _botRandom.Next(BotSocialReplyMaxDelayMs - BotSocialReplyMinDelayMs + 1);

                // 熟人回复更快（减少延迟）
                if (BotSocialMemory.IsKnownPlayer(candidate, speaker))
                    delayMs = Math.Max(BotSocialReplyMinDelayMs, delayMs - 500);

                DateTime replyTime = ApplyBotSocialDelayBias(candidate, SEnvir.Now.AddMilliseconds(delayMs), 250);
                _botPendingChatReplies[candidate.ObjectID] = new BotPendingChatReply
                {
                    ReplyToObjectID = speaker.ObjectID,
                    Text = finalReplyText,
                    ReplyTime = replyTime,
                    ExpireTime = replyTime.AddSeconds(BotSocialReplyExpireSeconds),
                    SpeakerName = speaker.Name,
                };

                _botNextSocialTime[candidate.ObjectID] = replyTime.AddSeconds(1);

                // 记录回复方的社交记忆
                RecordSocialChat(candidate, topic);
                return;
            }
        }

        private static DateTime ApplyBotSocialDelayBias(PlayerObject player, DateTime baseTime, int minLeadMs = 0)
        {
            BotBehaviorProfile profile = GetBotBehaviorProfile(player);
            int biasMs = Math.Max(-800, Math.Min(1200, profile?.SocialDelayBiasMs ?? 0));
            DateTime adjustedTime = baseTime.AddMilliseconds(biasMs);
            DateTime earliestTime = SEnvir.Now.AddMilliseconds(Math.Max(0, minLeadMs));

            return adjustedTime < earliestTime ? earliestTime : adjustedTime;
        }

        private static void ScheduleNextBotSocialTime(PlayerObject player, int minSeconds, int maxSeconds)
        {
            if (player == null) return;

            int configuredInterval = Config.BotGlobalChatIntervalSeconds;
            if (configuredInterval > 0)
            {
                minSeconds = configuredInterval;
                maxSeconds = Math.Max(minSeconds, configuredInterval * 2);
            }

            minSeconds = Math.Max(1, minSeconds);
            maxSeconds = Math.Max(minSeconds, maxSeconds);

            int delaySeconds = minSeconds;
            if (maxSeconds > minSeconds)
                delaySeconds += _botRandom.Next(maxSeconds - minSeconds + 1);

            DateTime scheduledTime = SEnvir.Now.AddSeconds(delaySeconds);
            _botNextSocialTime[player.ObjectID] = ApplyBotSocialDelayBias(player, scheduledTime, 1000);
        }

        private static string ResolveBotChatTopic(PlayerObject player)
        {
            if (player == null)
                return BotChatTopicGeneral;

            if (_botWaitingPickup.ContainsKey(player.ObjectID) || _botTargetItems.ContainsKey(player.ObjectID))
                return BotChatTopicLoot;

            MapObject target;
            if (_botTargets.TryGetValue(player.ObjectID, out target) && target != null && !target.Dead)
                return BotChatTopicCombat;

            bool goldFarmMode;
            bool emergencyGoldFarmMode;
            GetBotGoldFarmContext(player, out goldFarmMode, out emergencyGoldFarmMode);
            if (goldFarmMode)
                return BotChatTopicGold;

            if (player.GroupMembers != null && player.GroupMembers.Count > 1)
                return BotChatTopicGroup;

            return BotChatTopicGeneral;
        }

        // ─────────────────────── 变量模板 ───────────────────────

        /// <summary>
        /// 将聊天模板中的变量占位符替换为假人当前上下文信息。
        /// 支持的变量：
        ///   {地图}    → 当前地图名 (CurrentMap.Info.Description)
        ///   {怪物}    → 当前锁定目标怪物名
        ///   {等级}    → 当前等级
        ///   {职业}    → 职业名 (战士/法师/道士/刺客)
        ///   {名字}    → 自己的角色名
        ///   {队友}    → 随机一个队友的名字
        ///   {队长}    → 队长的名字
        ///   {玩家}    → 附近随机一个其他玩家的名字（用于回复场景）
        ///   {金币}    → 当前金币（带"万"缩写）
        /// </summary>
        private static string ExpandBotChatTemplate(string template, PlayerObject player, string speakerName = null)
        {
            if (string.IsNullOrWhiteSpace(template) || player == null)
                return template ?? string.Empty;

            string result = template;

            // {地图}
            string mapName = player.CurrentMap?.Info?.Description;
            if (!string.IsNullOrEmpty(mapName))
                result = result.Replace("{地图}", mapName);

            // {怪物}
            MapObject botTarget;
            if (_botTargets.TryGetValue(player.ObjectID, out botTarget) && botTarget != null && !botTarget.Dead)
                result = result.Replace("{怪物}", botTarget.Name);

            // {等级}
            result = result.Replace("{等级}", player.Level.ToString());

            // {职业}
            string className = GetBotChatClassName(player.Class);
            if (!string.IsNullOrEmpty(className))
                result = result.Replace("{职业}", className);

            // {名字}
            result = result.Replace("{名字}", player.Name);

            // {队友} — 随机一个同队非自己的队友名
            if (player.GroupMembers != null && player.GroupMembers.Count > 1)
            {
                var teammates = player.GroupMembers
                    .Where(m => m != null && m != player)
                    .ToList();
                if (teammates.Count > 0)
                {
                    string randomTeammate = teammates[_botRandom.Next(teammates.Count)].Name;
                    result = result.Replace("{队友}", randomTeammate);
                }
            }

            // {队长}
            if (player.GroupMembers != null && player.GroupMembers.Count > 1)
            {
                string leaderName = player.GroupMembers[0]?.Name;
                if (!string.IsNullOrEmpty(leaderName))
                    result = result.Replace("{队长}", leaderName);
            }

            // {玩家} — 说话者的名字（回复场景用）
            if (!string.IsNullOrEmpty(speakerName))
                result = result.Replace("{玩家}", speakerName);

            // {金币}
            result = result.Replace("{金币}", FormatBotChatGold(player.Gold));

            return result;
        }

        private static string GetBotChatClassName(MirClass cls)
        {
            switch (cls)
            {
                case MirClass.Warrior:  return "战士";
                case MirClass.Wizard:   return "法师";
                case MirClass.Taoist:   return "道士";
                case MirClass.Assassin: return "刺客";
                default:                return string.Empty;
            }
        }

        private static string FormatBotChatGold(long gold)
        {
            if (gold >= 10000)
                return (gold / 10000.0).ToString("F1") + "万";
            return gold.ToString();
        }

        // ─────────────────────── 关系感知辅助方法 ───────────────────────

        /// <summary>
        /// 带社交关系感知的话题选择：
        /// 如果有熟人在附近且上次聊过某个话题（10 分钟内），有一定概率延续该话题。
        /// 否则走原始场景话题逻辑。
        /// </summary>
        private static string ResolveBotChatTopicWithSocial(PlayerObject player)
        {
            // 基础话题（场景驱动）
            string baseTopic = ResolveBotChatTopic(player);

            // 30% 概率尝试延续与熟人的上次话题
            if (_botRandom.Next(100) >= 30)
                return baseTopic;

            // 查找附近的熟人
            List<PlayerObject> nearby = botPlayers
                .Where(x => x != null
                            && x != player
                            && x.CurrentMap == player.CurrentMap
                            && Functions.Distance(x.CurrentLocation, player.CurrentLocation) <= BotSocialNearbyRange
                            && BotSocialMemory.IsKnownPlayer(player, x))
                .ToList();

            if (nearby.Count == 0)
                return baseTopic;

            // 随机选一个熟人，检查上次话题
            PlayerObject knownPlayer = nearby[_botRandom.Next(nearby.Count)];
            string preferredTopic = BotSocialMemory.GetPreferredChatTopic(player, knownPlayer);

            if (!string.IsNullOrEmpty(preferredTopic))
                return preferredTopic;

            return baseTopic;
        }

        /// <summary>
        /// 尝试获取关系感知开场白。
        /// 如果附近有熟人/好友，有概率触发专属开场白。
        /// 返回 null 表示不触发，由调用方回退到普通开场白。
        /// </summary>
        private static string TryGetRelationAwareOpener(PlayerObject player)
        {
            // 只从 general 话题池中尝试（关系感知台词在 general 中）
            List<PlayerObject> nearby = botPlayers
                .Where(x => x != null
                            && x != player
                            && CanBotUseSocialChat(x)
                            && x.CurrentMap == player.CurrentMap
                            && Functions.Distance(x.CurrentLocation, player.CurrentLocation) <= BotSocialNearbyRange)
                .ToList();

            if (nearby.Count == 0)
                return null;

            // 随机选一个附近的人
            PlayerObject target = nearby[_botRandom.Next(nearby.Count)];
            var relation = BotSocialMemory.GetRelation(player, target);

            // 陌生人 15% 概率打招呼
            // 熟人 25% 概率打招呼
            // 好友 40% 概率打招呼
            // 密友 60% 概率打招呼
            // 仇敌 5% 概率挑衅
            int chance;
            switch (relation)
            {
                case BotSocialMemory.SocialRelation.CloseFriend: chance = 60; break;
                case BotSocialMemory.SocialRelation.Friend: chance = 40; break;
                case BotSocialMemory.SocialRelation.Acquaintance: chance = 25; break;
                case BotSocialMemory.SocialRelation.Enemy: chance = 5; break;
                default: chance = 15; break;
            }

            if (_botRandom.Next(100) >= chance)
                return null;

            // 记录聊天对象
            _botLastChatTarget[player.ObjectID] = target.ObjectID;

            // 使用 {玩家} 变量指向 target，让开场白带有对方名字
            // 从 general 话题池随机选一条带 {玩家} 的台词
            BotChatDialogSet dialog;
            if (!_botChatDialogs.TryGetValue(BotChatTopicGeneral, out dialog))
                return null;

            List<string> linesWithPlayer = dialog.Openers
                .Where(x => x.Contains("{玩家}"))
                .ToList();

            if (linesWithPlayer.Count == 0)
                return null;

            string template = linesWithPlayer[_botRandom.Next(linesWithPlayer.Count)];
            return ExpandBotChatTemplate(template, player, target.Name);
        }

        /// <summary>
        /// 尝试获取关系感知回复。
        /// 如果回复方和说话方有社交关系，有概率选择关系感知的回复。
        /// </summary>
        private static string TryGetRelationAwareReply(PlayerObject replier, PlayerObject speaker, string topic)
        {
            if (!BotSocialMemory.IsKnownPlayer(replier, speaker))
                return null;

            // 20% 概率使用关系感知回复（避免每条都走关系路线）
            if (_botRandom.Next(100) >= 20)
                return null;

            BotChatDialogSet dialog;
            if (!_botChatDialogs.TryGetValue(topic ?? string.Empty, out dialog))
            {
                if (!_botChatDialogs.TryGetValue(BotChatTopicGeneral, out dialog))
                    return null;
            }

            // 从回复池中找带 {玩家} 的台词
            List<string> relationReplies = dialog.Replies
                .Where(x => x.Contains("{玩家}"))
                .ToList();

            if (relationReplies.Count == 0)
                return null;

            string template = relationReplies[_botRandom.Next(relationReplies.Count)];

            // 对密友用"老{玩家}"前缀
            var relation = BotSocialMemory.GetRelation(replier, speaker);
            if (relation == BotSocialMemory.SocialRelation.CloseFriend)
            {
                // 30% 概率在回复中加上"老"前缀（如果台词以名字开头的话）
                string prefix = BotSocialMemory.GetRelationPrefix(replier, speaker);
                if (!string.IsNullOrEmpty(prefix) && !template.StartsWith("老"))
                    template = template.Replace("{玩家}", prefix + "{玩家}");
            }

            return ExpandBotChatTemplate(template, replier, speaker.Name);
        }

        /// <summary>
        /// 记录聊天到社交记忆系统
        /// </summary>
        private static void RecordSocialChat(PlayerObject bot, string topic)
        {
            // 记录话题
            _botLastChatTopicWith[bot.ObjectID] = topic;
            _botLastTopicUseTime[topic] = SEnvir.Now;

            // 如果有聊天对象，记录到社交记忆
            uint lastTargetId;
            if (_botLastChatTarget.TryGetValue(bot.ObjectID, out lastTargetId))
            {
                PlayerObject target = SEnvir.Players.FirstOrDefault(p => p != null && p.ObjectID == lastTargetId);
                if (target != null)
                    BotSocialMemory.RecordChat(bot, target, topic);
            }
        }

        // ─────────────────────── 遥测 ───────────────────────

        private static void RecordBotSocialMessage(PlayerObject player)
        {
            BotTelemetryWindow telemetry = GetBotTelemetry(player);
            if (telemetry == null) return;

            telemetry.SocialMessages++;
        }
    }
}
