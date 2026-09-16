using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Runtime.Serialization;
using System.Runtime.Serialization.Json;
using Library;
using Server.Models;

namespace Server.Envir
{
    /// <summary>
    /// 假人社交关系记忆系统：记录与每个玩家的互动历史，
    /// 支持亲密度、PVP敌对、交易历史、组队关系等多维度社交评估，
    /// 为聊天和交易决策提供上下文感知能力。
    ///
    /// v2 新增：JSON 文件持久化，支持跨会话记住"谁杀过我、谁帮过我"。
    /// 数据文件路径：[Server目录]/BotSocialMemory.json
    /// </summary>
    internal static class BotSocialMemory
    {
        // ─────────────────────── 常量 ───────────────────────

        private const int MaxSocialRecordsPerBot = 80;
        private const int RelationshipDecayIntervalSeconds = 600;
        private const int RelationshipDecayAmount = 1;
        private const int MemoryExpireMinutes = 120;
        private const int AcquaintanceThreshold = 10;
        private const int FriendThreshold = 30;
        private const int CloseFriendThreshold = 60;
        private const int EnemyThreshold = 20;

        // ─────────────────────── 持久化配置 ───────────────────────

        private const int AutoSaveIntervalSeconds = 300;
        private const int MaxBotsToSave = 100;          // 最多保存多少个 bot 的记忆
        private const int MaxRecordsPerBotToSave = 50;  // 每个 bot 最多保存多少条社交记录
        private const int MaxInteractionsToSave = 10;   // 每条社交记录保存最近多少次互动

        private static DateTime _lastSaveTime = DateTime.MinValue;
        private static bool _isDirty;

        private static string GetMemoryFilePath()
        {
            string dir = AppDomain.CurrentDomain.BaseDirectory;
            return Path.Combine(dir, "BotSocialMemory.json");
        }

        // ─────────────────────── 数据结构 ───────────────────────

        public enum SocialRelation
        {
            Stranger,
            Acquaintance,
            Friend,
            CloseFriend,
            Enemy,
        }

        private enum InteractionType
        {
            GroupJoin,
            FightTogether,
            Rescued,
            TradeSuccess,
            Chat,
            Attacked,
            Killed,
            KilledBy,
            SiegeTogether,
            SameGuild,
        }

        private sealed class InteractionRecord
        {
            public InteractionType Type;
            public DateTime Time;
            public int AffinityDelta;
            public int HostilityDelta;
            public string Detail;
        }

        private sealed class SocialRecord
        {
            public uint TargetObjectID;
            public string TargetName;
            public MirClass? TargetClass;
            public int Affinity;
            public int Hostility;
            public List<InteractionRecord> Interactions = new List<InteractionRecord>();
            public DateTime LastInteractionTime;
            public DateTime FirstMetTime;
            public int ChatCount;
            public int FightTogetherCount;
            public int TradeCount;
            public int GroupCount;
            public int TimesKilledTarget;
            public int TimesKilledBy;
            public string LastChatTopic;
            public string LastChatContext;
        }

        private static readonly Dictionary<uint, Dictionary<uint, SocialRecord>> _socialMemory
            = new Dictionary<uint, Dictionary<uint, SocialRecord>>();

        private static DateTime _lastDecayTime = DateTime.MinValue;

        // ─────────────────────── JSON DTO ───────────────────────

        [DataContract]
        private sealed class InteractionRecordDto
        {
            [DataMember] public int Type;          // InteractionType as int
            [DataMember] public long TimeTicks;
            [DataMember] public int AffinityDelta;
            [DataMember] public int HostilityDelta;
            [DataMember] public string Detail;
        }

        [DataContract]
        private sealed class SocialRecordDto
        {
            [DataMember] public uint TargetObjectID;
            [DataMember] public string TargetName;
            [DataMember] public int? TargetClass;  // MirClass as int, null if unknown
            [DataMember] public int Affinity;
            [DataMember] public int Hostility;
            [DataMember] public long LastInteractionTimeTicks;
            [DataMember] public long FirstMetTimeTicks;
            [DataMember] public int ChatCount;
            [DataMember] public int FightTogetherCount;
            [DataMember] public int TradeCount;
            [DataMember] public int GroupCount;
            [DataMember] public int TimesKilledTarget;
            [DataMember] public int TimesKilledBy;
            [DataMember] public string LastChatTopic;
            [DataMember] public List<InteractionRecordDto> Interactions;
        }

        [DataContract]
        private sealed class BotSocialEntryDto
        {
            [DataMember] public uint BotObjectID;
            [DataMember] public string BotName;    // 仅用于人工查阅
            [DataMember] public List<SocialRecordDto> Records;
        }

        [DataContract]
        private sealed class BotSocialMemoryDataDto
        {
            [DataMember] public int Version = 1;
            [DataMember] public long SavedAtTicks;
            [DataMember] public List<BotSocialEntryDto> Bots;
        }

        // ─────────────────────── 记录接口 ───────────────────────

        public static void RecordGroupJoin(PlayerObject bot, PlayerObject target)
        {
            if (bot == null || target == null || bot.ObjectID == target.ObjectID) return;
            RecordInteraction(bot, target, InteractionType.GroupJoin, 3, 0, "组队");
        }

        public static void RecordFightTogether(PlayerObject bot, PlayerObject target)
        {
            if (bot == null || target == null || bot.ObjectID == target.ObjectID) return;
            var record = GetOrCreateRecord(bot.ObjectID, target.ObjectID, target.Name, target.Class);
            record.FightTogetherCount++;
            if (record.FightTogetherCount % 5 == 0)
                RecordInteraction(bot, target, InteractionType.FightTogether, 1, 0, "并肩战斗");
        }

        public static void RecordRescue(PlayerObject bot, PlayerObject rescuer)
        {
            if (bot == null || rescuer == null || bot.ObjectID == rescuer.ObjectID) return;
            RecordInteraction(bot, rescuer, InteractionType.Rescued, 5, 0, "救命之恩");
        }

        public static void RecordTradeSuccess(PlayerObject bot, PlayerObject partner)
        {
            if (bot == null || partner == null || bot.ObjectID == partner.ObjectID) return;
            var record = GetOrCreateRecord(bot.ObjectID, partner.ObjectID, partner.Name, partner.Class);
            record.TradeCount++;
            RecordInteraction(bot, partner, InteractionType.TradeSuccess, 4, 0, $"第{record.TradeCount}次交易");
        }

        public static void RecordChat(PlayerObject bot, PlayerObject target, string topic, string context = null)
        {
            if (bot == null || target == null || bot.ObjectID == target.ObjectID) return;
            var record = GetOrCreateRecord(bot.ObjectID, target.ObjectID, target.Name, target.Class);
            record.ChatCount++;
            record.LastChatTopic = topic;
            record.LastChatContext = context;
            record.LastInteractionTime = SEnvir.Now;
            if (record.ChatCount % 3 == 0)
                RecordInteraction(bot, target, InteractionType.Chat, 2, 0, topic);
        }

        public static void RecordAttacked(PlayerObject bot, PlayerObject attacker, int damage)
        {
            if (bot == null || attacker == null || bot.ObjectID == attacker.ObjectID) return;
            int hostilityDelta = Math.Min(5, Math.Max(1, damage / 100));
            RecordInteraction(bot, attacker, InteractionType.Attacked, -1, hostilityDelta, $"受到{damage}伤害");
            var record = GetRecord(bot.ObjectID, attacker.ObjectID);
            if (record != null && record.Hostility >= EnemyThreshold)
                record.Affinity = Math.Max(0, record.Affinity - 2);
        }

        public static void RecordKillTarget(PlayerObject bot, PlayerObject target)
        {
            if (bot == null || target == null || bot.ObjectID == target.ObjectID) return;
            var record = GetOrCreateRecord(bot.ObjectID, target.ObjectID, target.Name, target.Class);
            record.TimesKilledTarget++;
            RecordInteraction(bot, target, InteractionType.Killed, -2, 3, "击杀了对方");
        }

        public static void RecordKilledBy(PlayerObject bot, PlayerObject killer)
        {
            if (bot == null || killer == null || bot.ObjectID == killer.ObjectID) return;
            var record = GetOrCreateRecord(bot.ObjectID, killer.ObjectID, killer.Name, killer.Class);
            record.TimesKilledBy++;
            RecordInteraction(bot, killer, InteractionType.KilledBy, -1, 4, "被对方击杀");
        }

        public static void RecordSiegeTogether(PlayerObject bot, PlayerObject ally)
        {
            if (bot == null || ally == null || bot.ObjectID == ally.ObjectID) return;
            var record = GetRecord(bot.ObjectID, ally.ObjectID);
            if (record != null)
            {
                var lastSiege = record.Interactions
                    .Where(x => x.Type == InteractionType.SiegeTogether)
                    .OrderByDescending(x => x.Time)
                    .FirstOrDefault();
                if (lastSiege != null && (SEnvir.Now - lastSiege.Time).TotalMinutes < 10)
                    return;
            }
            RecordInteraction(bot, ally, InteractionType.SiegeTogether, 3, 0, "并肩攻城");
        }

        public static void RecordSameGuild(PlayerObject bot, PlayerObject guildMate)
        {
            if (bot == null || guildMate == null || bot.ObjectID == guildMate.ObjectID) return;
            var record = GetOrCreateRecord(bot.ObjectID, guildMate.ObjectID, guildMate.Name, guildMate.Class);
            if (!record.Interactions.Any(x => x.Type == InteractionType.SameGuild))
                RecordInteraction(bot, guildMate, InteractionType.SameGuild, 5, 0, "同公会");
        }

        // ─────────────────────── 查询接口 ───────────────────────

        public static SocialRelation GetRelation(PlayerObject bot, PlayerObject target)
        {
            if (bot == null || target == null || bot.ObjectID == target.ObjectID)
                return SocialRelation.Stranger;
            var record = GetRecord(bot.ObjectID, target.ObjectID);
            if (record == null) return SocialRelation.Stranger;
            if (record.Hostility >= EnemyThreshold) return SocialRelation.Enemy;
            if ((SEnvir.Now - record.LastInteractionTime).TotalMinutes > MemoryExpireMinutes)
                return SocialRelation.Stranger;
            if (record.Affinity >= CloseFriendThreshold) return SocialRelation.CloseFriend;
            if (record.Affinity >= FriendThreshold) return SocialRelation.Friend;
            if (record.Affinity >= AcquaintanceThreshold) return SocialRelation.Acquaintance;
            return SocialRelation.Stranger;
        }

        public static int GetAffinity(PlayerObject bot, PlayerObject target)
        {
            if (bot == null || target == null) return 0;
            return GetRecord(bot.ObjectID, target.ObjectID)?.Affinity ?? 0;
        }

        public static int GetHostility(PlayerObject bot, PlayerObject target)
        {
            if (bot == null || target == null) return 0;
            return GetRecord(bot.ObjectID, target.ObjectID)?.Hostility ?? 0;
        }

        public static int GetTradeCount(PlayerObject bot, PlayerObject target)
        {
            if (bot == null || target == null) return 0;
            return GetRecord(bot.ObjectID, target.ObjectID)?.TradeCount ?? 0;
        }

        public static int GetChatCount(PlayerObject bot, PlayerObject target)
        {
            if (bot == null || target == null) return 0;
            return GetRecord(bot.ObjectID, target.ObjectID)?.ChatCount ?? 0;
        }

        public static string GetRememberedName(PlayerObject bot, uint targetId)
        {
            if (bot == null) return null;
            return GetRecord(bot.ObjectID, targetId)?.TargetName;
        }

        public static string GetLastChatContext(PlayerObject bot, PlayerObject target)
        {
            if (bot == null || target == null) return null;
            var record = GetRecord(bot.ObjectID, target.ObjectID);
            if (record == null) return null;
            if (record.LastChatContext != null)
            {
                var lastChat = record.Interactions
                    .Where(x => x.Type == InteractionType.Chat)
                    .OrderByDescending(x => x.Time)
                    .FirstOrDefault();
                if (lastChat != null && (SEnvir.Now - lastChat.Time).TotalMinutes <= 5)
                    return record.LastChatContext;
            }
            return null;
        }

        public static List<SocialRecordSnapshot> GetAllRelationships(PlayerObject bot)
        {
            var result = new List<SocialRecordSnapshot>();
            if (bot == null) return result;
            Dictionary<uint, SocialRecord> records;
            if (!_socialMemory.TryGetValue(bot.ObjectID, out records)) return result;
            foreach (var kvp in records)
            {
                var record = kvp.Value;
                if (record == null) continue;
                result.Add(new SocialRecordSnapshot
                {
                    TargetObjectID = record.TargetObjectID,
                    TargetName = record.TargetName,
                    Relation = GetRelation(bot, null),
                    Affinity = record.Affinity,
                    Hostility = record.Hostility,
                    ChatCount = record.ChatCount,
                    TradeCount = record.TradeCount,
                    FightTogetherCount = record.FightTogetherCount,
                    LastInteractionTime = record.LastInteractionTime,
                });
            }
            return result.OrderByDescending(x => x.Affinity).ToList();
        }

        public static List<PlayerObject> GetKnownPlayersOnMap(PlayerObject bot, int mapIndex)
        {
            var result = new List<PlayerObject>();
            if (bot == null) return result;
            Dictionary<uint, SocialRecord> records;
            if (!_socialMemory.TryGetValue(bot.ObjectID, out records)) return result;
            foreach (var kvp in records)
            {
                if (kvp.Value == null) continue;
                var player = SEnvir.Players.FirstOrDefault(p =>
                    p != null && p.ObjectID == kvp.Key && p.CurrentMap?.Info?.Index == mapIndex);
                if (player != null)
                    result.Add(player);
            }
            return result;
        }

        public static bool IsKnownPlayer(PlayerObject bot, PlayerObject target)
        {
            if (bot == null || target == null) return false;
            return GetRelation(bot, target) != SocialRelation.Stranger;
        }

        // ─────────────────────── 聊天增强接口 ───────────────────────

        public static string GetPreferredChatTopic(PlayerObject bot, PlayerObject target)
        {
            if (target == null) return null;
            var record = GetRecord(bot.ObjectID, target.ObjectID);
            if (record == null) return null;
            if (!string.IsNullOrEmpty(record.LastChatTopic))
            {
                var lastChat = record.Interactions
                    .Where(x => x.Type == InteractionType.Chat)
                    .OrderByDescending(x => x.Time)
                    .FirstOrDefault();
                if (lastChat != null && (SEnvir.Now - lastChat.Time).TotalMinutes <= 10)
                    return record.LastChatTopic;
            }
            return null;
        }

        public static string GetRelationPrefix(PlayerObject bot, PlayerObject target)
        {
            if (bot == null || target == null) return string.Empty;
            var relation = GetRelation(bot, target);
            return relation == SocialRelation.CloseFriend ? "老" : string.Empty;
        }

        public static bool ShouldIgnoreChat(PlayerObject bot, PlayerObject target)
        {
            if (bot == null || target == null) return false;
            var relation = GetRelation(bot, target);
            if (relation == SocialRelation.Enemy)
                return _botSocialRandom.Next(100) < 30;
            return false;
        }

        // ─────────────────────── 交易增强接口 ───────────────────────

        public static bool ShouldAcceptTrade(PlayerObject bot, PlayerObject requester)
        {
            if (bot == null || requester == null) return false;
            var relation = GetRelation(bot, requester);
            return relation != SocialRelation.Enemy;
        }

        // ─────────────────────── 维护接口 ───────────────────────

        /// <summary>
        /// 定期维护：衰减亲密度、清理过期记忆、自动保存。
        /// 应在每个 BotTick 中调用。
        /// </summary>
        public static void Tick()
        {
            // 亲密度衰减（每 10 分钟）
            if (_lastDecayTime == DateTime.MinValue)
                _lastDecayTime = SEnvir.Now;

            if ((SEnvir.Now - _lastDecayTime).TotalSeconds >= RelationshipDecayIntervalSeconds)
            {
                _lastDecayTime = SEnvir.Now;
                DecayRelationships();
            }

            // 自动保存（每 5 分钟）
            if (_isDirty)
            {
                if (_lastSaveTime == DateTime.MinValue)
                    _lastSaveTime = SEnvir.Now;

                if ((SEnvir.Now - _lastSaveTime).TotalSeconds >= AutoSaveIntervalSeconds)
                    Save();
            }
        }

        public static void ClearBot(uint botObjectId)
        {
            _socialMemory.Remove(botObjectId);
        }

        /// <summary>
        /// 清理所有社交记忆，并保存当前状态到文件（Stop 时调用）。
        /// </summary>
        public static void ClearAll()
        {
            if (_isDirty)
                Save();

            _socialMemory.Clear();
            _lastDecayTime = DateTime.MinValue;
            _isDirty = false;
        }

        // ─────────────────────── 持久化 API ───────────────────────

        /// <summary>
        /// 从 JSON 文件加载持久化社交记忆。应在 BotManager.Start() 中调用。
        /// </summary>
        public static void Load()
        {
            string path = GetMemoryFilePath();
            if (!File.Exists(path)) return;

            try
            {
                byte[] bytes = File.ReadAllBytes(path);
                var serializer = new DataContractJsonSerializer(typeof(BotSocialMemoryDataDto));
                BotSocialMemoryDataDto dto;
                using (var ms = new MemoryStream(bytes))
                    dto = (BotSocialMemoryDataDto)serializer.ReadObject(ms);

                if (dto?.Bots == null) return;

                int totalRecords = 0;
                foreach (var botEntry in dto.Bots)
                {
                    if (botEntry?.Records == null) continue;

                    var botRecords = new Dictionary<uint, SocialRecord>();
                    foreach (var r in botEntry.Records)
                    {
                        if (r == null) continue;

                        var interactions = new List<InteractionRecord>();
                        if (r.Interactions != null)
                        {
                            foreach (var i in r.Interactions)
                            {
                                if (i == null) continue;
                                interactions.Add(new InteractionRecord
                                {
                                    Type = (InteractionType)i.Type,
                                    Time = new DateTime(i.TimeTicks, DateTimeKind.Utc).ToLocalTime(),
                                    AffinityDelta = i.AffinityDelta,
                                    HostilityDelta = i.HostilityDelta,
                                    Detail = i.Detail,
                                });
                            }
                        }

                        botRecords[r.TargetObjectID] = new SocialRecord
                        {
                            TargetObjectID = r.TargetObjectID,
                            TargetName = r.TargetName ?? string.Empty,
                            TargetClass = r.TargetClass.HasValue ? (MirClass?)r.TargetClass.Value : null,
                            Affinity = r.Affinity,
                            Hostility = r.Hostility,
                            LastInteractionTime = new DateTime(r.LastInteractionTimeTicks, DateTimeKind.Utc).ToLocalTime(),
                            FirstMetTime = new DateTime(r.FirstMetTimeTicks, DateTimeKind.Utc).ToLocalTime(),
                            ChatCount = r.ChatCount,
                            FightTogetherCount = r.FightTogetherCount,
                            TradeCount = r.TradeCount,
                            GroupCount = r.GroupCount,
                            TimesKilledTarget = r.TimesKilledTarget,
                            TimesKilledBy = r.TimesKilledBy,
                            LastChatTopic = r.LastChatTopic,
                            Interactions = interactions,
                        };
                        totalRecords++;
                    }

                    if (botRecords.Count > 0)
                        _socialMemory[botEntry.BotObjectID] = botRecords;
                }

                SEnvir.Log($"[BotSocialMemory] 已加载历史社交记忆：{dto.Bots.Count} 个假人，共 {totalRecords} 条关系记录。");
            }
            catch (Exception ex)
            {
                SEnvir.Log($"[BotSocialMemory] 加载社交记忆文件失败（将使用空记忆）：{ex.Message}");
            }
        }

        /// <summary>
        /// 将当前社交记忆保存到 JSON 文件。
        /// 仅保存有实质意义的关系（亲密度 ≥ 好友级别 或 敌对 / 杀戮记录），避免文件过大。
        /// </summary>
        public static void Save()
        {
            try
            {
                var bots = new List<BotSocialEntryDto>();

                foreach (var botKvp in _socialMemory.Take(MaxBotsToSave))
                {
                    if (botKvp.Value == null) continue;

                    // 只保存有价值的关系：杀戮记录、好友级以上、仇敌
                    var valuableRecords = botKvp.Value.Values
                        .Where(r => r != null && (
                            r.TimesKilledBy > 0 ||   // 被杀记录（跨会话报仇）
                            r.TimesKilledTarget > 0 || // 击杀记录
                            r.Affinity >= FriendThreshold || // 好友以上
                            r.Hostility >= EnemyThreshold || // 仇敌
                            r.TradeCount >= 2              // 多次交易伙伴
                        ))
                        .OrderByDescending(r => r.Affinity + r.Hostility + r.TimesKilledBy * 5)
                        .Take(MaxRecordsPerBotToSave)
                        .Select(r => new SocialRecordDto
                        {
                            TargetObjectID = r.TargetObjectID,
                            TargetName = r.TargetName,
                            TargetClass = r.TargetClass.HasValue ? (int?)r.TargetClass.Value : null,
                            Affinity = r.Affinity,
                            Hostility = r.Hostility,
                            LastInteractionTimeTicks = r.LastInteractionTime.ToUniversalTime().Ticks,
                            FirstMetTimeTicks = r.FirstMetTime.ToUniversalTime().Ticks,
                            ChatCount = r.ChatCount,
                            FightTogetherCount = r.FightTogetherCount,
                            TradeCount = r.TradeCount,
                            GroupCount = r.GroupCount,
                            TimesKilledTarget = r.TimesKilledTarget,
                            TimesKilledBy = r.TimesKilledBy,
                            LastChatTopic = r.LastChatTopic,
                            Interactions = r.Interactions
                                .OrderByDescending(i => i.Time)
                                .Take(MaxInteractionsToSave)
                                .Select(i => new InteractionRecordDto
                                {
                                    Type = (int)i.Type,
                                    TimeTicks = i.Time.ToUniversalTime().Ticks,
                                    AffinityDelta = i.AffinityDelta,
                                    HostilityDelta = i.HostilityDelta,
                                    Detail = i.Detail,
                                })
                                .ToList(),
                        })
                        .ToList();

                    if (valuableRecords.Count == 0) continue;

                    // 尝试获取 bot 名字（用于人工查阅）
                    string botName = string.Empty;
                    var botPlayer = SEnvir.Players.FirstOrDefault(p => p?.ObjectID == botKvp.Key);
                    if (botPlayer != null) botName = botPlayer.Name ?? string.Empty;

                    bots.Add(new BotSocialEntryDto
                    {
                        BotObjectID = botKvp.Key,
                        BotName = botName,
                        Records = valuableRecords,
                    });
                }

                var dto = new BotSocialMemoryDataDto
                {
                    Version = 1,
                    SavedAtTicks = SEnvir.Now.ToUniversalTime().Ticks,
                    Bots = bots,
                };

                var serializer = new DataContractJsonSerializer(typeof(BotSocialMemoryDataDto));
                string path = GetMemoryFilePath();
                string tmpPath = path + ".tmp";

                using (var fs = new FileStream(tmpPath, FileMode.Create, FileAccess.Write, FileShare.None))
                    serializer.WriteObject(fs, dto);

                if (File.Exists(path)) File.Delete(path);
                File.Move(tmpPath, path);

                _isDirty = false;
                _lastSaveTime = SEnvir.Now;
            }
            catch (Exception ex)
            {
                SEnvir.Log($"[BotSocialMemory] 保存社交记忆文件失败：{ex.Message}");
            }
        }

        // ─────────────────────── 内部实现 ───────────────────────

        private static readonly Random _botSocialRandom = new Random();

        public sealed class SocialRecordSnapshot
        {
            public uint TargetObjectID;
            public string TargetName;
            public SocialRelation Relation;
            public int Affinity;
            public int Hostility;
            public int ChatCount;
            public int TradeCount;
            public int FightTogetherCount;
            public DateTime LastInteractionTime;
        }

        private static void RecordInteraction(PlayerObject bot, PlayerObject target, InteractionType type,
            int affinityDelta, int hostilityDelta, string detail = null)
        {
            var record = GetOrCreateRecord(bot.ObjectID, target.ObjectID, target.Name, target.Class);

            record.Affinity = Math.Max(0, record.Affinity + affinityDelta);
            record.Hostility = Math.Max(0, record.Hostility + hostilityDelta);
            record.LastInteractionTime = SEnvir.Now;
            if (record.FirstMetTime == DateTime.MinValue)
                record.FirstMetTime = SEnvir.Now;

            if (type == InteractionType.GroupJoin)
                record.GroupCount++;

            record.Interactions.Add(new InteractionRecord
            {
                Type = type,
                Time = SEnvir.Now,
                AffinityDelta = affinityDelta,
                HostilityDelta = hostilityDelta,
                Detail = detail,
            });

            if (record.Interactions.Count > 20)
                record.Interactions.RemoveAt(0);

            TrimSocialRecords(bot.ObjectID);
            _isDirty = true;
        }

        private static SocialRecord GetOrCreateRecord(uint botId, uint targetId, string targetName, MirClass? targetClass)
        {
            Dictionary<uint, SocialRecord> records;
            if (!_socialMemory.TryGetValue(botId, out records))
            {
                records = new Dictionary<uint, SocialRecord>();
                _socialMemory[botId] = records;
            }

            SocialRecord record;
            if (!records.TryGetValue(targetId, out record))
            {
                record = new SocialRecord
                {
                    TargetObjectID = targetId,
                    TargetName = targetName ?? string.Empty,
                    TargetClass = targetClass,
                };
                records[targetId] = record;
            }
            else
            {
                if (!string.IsNullOrEmpty(targetName))
                    record.TargetName = targetName;
                if (targetClass.HasValue)
                    record.TargetClass = targetClass;
            }

            return record;
        }

        private static SocialRecord GetRecord(uint botId, uint targetId)
        {
            Dictionary<uint, SocialRecord> records;
            if (!_socialMemory.TryGetValue(botId, out records)) return null;
            SocialRecord record;
            return records.TryGetValue(targetId, out record) ? record : null;
        }

        private static void TrimSocialRecords(uint botId)
        {
            Dictionary<uint, SocialRecord> records;
            if (!_socialMemory.TryGetValue(botId, out records)) return;
            if (records.Count <= MaxSocialRecordsPerBot) return;

            var toRemove = records
                .Where(x => x.Value != null)
                .OrderBy(x => x.Value.LastInteractionTime)
                .Take(records.Count - MaxSocialRecordsPerBot)
                .Select(x => x.Key)
                .ToList();

            foreach (var key in toRemove)
                records.Remove(key);
        }

        private static void DecayRelationships()
        {
            foreach (var botKvp in _socialMemory)
            {
                if (botKvp.Value == null) continue;

                var toRemove = new List<uint>();

                foreach (var kvp in botKvp.Value)
                {
                    if (kvp.Value == null) continue;

                    if ((SEnvir.Now - kvp.Value.LastInteractionTime).TotalMinutes > MemoryExpireMinutes)
                    {
                        if (kvp.Value.Affinity < FriendThreshold && kvp.Value.Hostility < EnemyThreshold)
                        {
                            toRemove.Add(kvp.Key);
                            continue;
                        }
                    }

                    if (kvp.Value.Affinity > 0)
                        kvp.Value.Affinity = Math.Max(0, kvp.Value.Affinity - RelationshipDecayAmount);

                    if (kvp.Value.Hostility > 0)
                        kvp.Value.Hostility = Math.Max(0, kvp.Value.Hostility - RelationshipDecayAmount);
                }

                foreach (var key in toRemove)
                    botKvp.Value.Remove(key);
            }
        }
    }
}
