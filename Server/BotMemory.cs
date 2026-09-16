using Library;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Runtime.Serialization;
using System.Runtime.Serialization.Json;
using System.Text;

namespace Server.Envir
{
    /// <summary>
    /// 假人学习记忆系统。
    /// 记录地图刷怪效率（跨会话累积）和技能-怪物效果数据，
    /// 用于优化切图决策和技能选择。
    ///
    /// v2 新增：JSON 文件持久化，支持跨会话经验积累。
    /// 数据文件路径：[Server目录]/BotMemory.json
    /// </summary>
    internal static class BotMemory
    {
        // ══════════════════════════════════════════════════════════════════════
        //  持久化文件配置
        // ══════════════════════════════════════════════════════════════════════

        /// <summary>内存数据自动保存间隔（秒）：避免每次更新都写磁盘</summary>
        private const int AutoSaveIntervalSeconds = 300; // 5 分钟自动保存一次

        /// <summary>地图记忆最大保存条数（控制文件大小）</summary>
        private const int MaxMapMemoryEntries = 200;

        /// <summary>技能记忆最大怪物种数（控制文件大小）</summary>
        private const int MaxSkillMonsterEntries = 300;

        private static DateTime _lastSaveTime = DateTime.MinValue;
        private static bool _isDirty; // 是否有未保存的变更

        /// <summary>获取持久化文件路径（与 Server.exe 同目录）</summary>
        private static string GetMemoryFilePath()
        {
            string dir = AppDomain.CurrentDomain.BaseDirectory;
            return Path.Combine(dir, "BotMemory.json");
        }

        // ══════════════════════════════════════════════════════════════════════
        //  JSON 序列化数据合约（DataContractJsonSerializer，不依赖外部库）
        // ══════════════════════════════════════════════════════════════════════

        [DataContract]
        private sealed class BotMapMemoryDto
        {
            [DataMember] public int MapIndex;
            [DataMember] public double TotalActiveSeconds;
            [DataMember] public int TotalKills;
            [DataMember] public int TotalPickups;
            [DataMember] public int TotalBlockedMoves;
            [DataMember] public int TotalMagicFailures;
            [DataMember] public int VisitCount;
            [DataMember] public long LastVisitTimeTicks;
        }

        [DataContract]
        private sealed class SkillMonsterRecordDto
        {
            [DataMember] public int Skill;          // MagicType as int
            [DataMember] public int UseCount;
            [DataMember] public long TotalDamageEstimate;
        }

        [DataContract]
        private sealed class SkillMonsterEntryDto
        {
            [DataMember] public string MonsterName;
            [DataMember] public List<SkillMonsterRecordDto> Records;
        }

        [DataContract]
        private sealed class BotMemoryDataDto
        {
            [DataMember] public int Version = 1;
            [DataMember] public long SavedAtTicks;
            [DataMember] public List<BotMapMemoryDto> MapMemory;
            [DataMember] public List<SkillMonsterEntryDto> SkillMemory;
        }

        // ══════════════════════════════════════════════════════════════════════
        //  地图经验记忆
        // ══════════════════════════════════════════════════════════════════════

        /// <summary>
        /// 单张地图的累积经验记录。
        /// 按 mapIndex 聚合所有假人的数据（共享经验，因为地图特性与玩家无关）。
        /// </summary>
        private sealed class BotMapMemory
        {
            public int MapIndex;
            public double TotalActiveSeconds;
            public int TotalKills;
            public int TotalPickups;
            public int TotalBlockedMoves;
            public int TotalMagicFailures;
            public int VisitCount;
            public DateTime LastVisitTime;

            public double KillsPerMinute
            {
                get
                {
                    double minutes = Math.Max(0.5, TotalActiveSeconds / 60.0);
                    return TotalKills / minutes;
                }
            }

            public double PickupsPerMinute
            {
                get
                {
                    double minutes = Math.Max(0.5, TotalActiveSeconds / 60.0);
                    return TotalPickups / minutes;
                }
            }
        }

        private static readonly Dictionary<int, BotMapMemory> _mapMemory
            = new Dictionary<int, BotMapMemory>();

        private const int MapMemoryMinSeconds = 60;
        private const int MapMemoryMaxScoreBonus = 50;
        private const int MapMemoryMaxScorePenalty = 30;

        // ══════════════════════════════════════════════════════════════════════
        //  技能-怪物效果记忆
        // ══════════════════════════════════════════════════════════════════════

        private sealed class SkillMonsterRecord
        {
            public MagicType Skill;
            public int UseCount;
            public long TotalDamageEstimate;
            public double AverageDamage
            {
                get { return UseCount > 0 ? (double)TotalDamageEstimate / UseCount : 0; }
            }
        }

        private static readonly Dictionary<string, List<SkillMonsterRecord>> _skillMonsterMemory
            = new Dictionary<string, List<SkillMonsterRecord>>();

        private const int SkillMemoryMinUses = 3;
        private const int SkillMemoryMaxEntries = 8;

        // ══════════════════════════════════════════════════════════════════════
        //  公共 API — 地图记忆
        // ══════════════════════════════════════════════════════════════════════

        public static void RecordKill(int mapIndex)
        {
            if (mapIndex < 0) return;
            var mem = GetOrCreateMapMemory(mapIndex);
            mem.TotalKills++;
            mem.LastVisitTime = SEnvir.Now;
            _isDirty = true;
        }

        public static void RecordPickup(int mapIndex)
        {
            if (mapIndex < 0) return;
            var mem = GetOrCreateMapMemory(mapIndex);
            mem.TotalPickups++;
            _isDirty = true;
        }

        public static void RecordBlockedMove(int mapIndex)
        {
            if (mapIndex < 0) return;
            var mem = GetOrCreateMapMemory(mapIndex);
            mem.TotalBlockedMoves++;
            _isDirty = true;
        }

        public static void RecordMagicFailure(int mapIndex)
        {
            if (mapIndex < 0) return;
            var mem = GetOrCreateMapMemory(mapIndex);
            mem.TotalMagicFailures++;
            _isDirty = true;
        }

        public static void RecordMapStay(int mapIndex, double activeSeconds)
        {
            if (mapIndex < 0 || activeSeconds <= 0) return;
            var mem = GetOrCreateMapMemory(mapIndex);
            mem.TotalActiveSeconds += activeSeconds;
            mem.VisitCount++;
            mem.LastVisitTime = SEnvir.Now;
            _isDirty = true;
        }

        public static int GetMapMemoryScoreBonus(int mapIndex)
        {
            if (!_mapMemory.TryGetValue(mapIndex, out BotMapMemory mem))
                return 0;

            if (mem.TotalActiveSeconds < MapMemoryMinSeconds)
                return 0;

            double kpm = mem.KillsPerMinute;
            double pickupsPerMin = mem.PickupsPerMinute;
            double blockedPerMin = mem.TotalBlockedMoves / Math.Max(0.5, mem.TotalActiveSeconds / 60.0);
            double failPerMin = mem.TotalMagicFailures / Math.Max(0.5, mem.TotalActiveSeconds / 60.0);

            int bonus = 0;
            bonus += (int)Math.Round(Math.Min(MapMemoryMaxScoreBonus, kpm * 6 + pickupsPerMin * 4));
            bonus -= (int)Math.Round(Math.Min(MapMemoryMaxScorePenalty, blockedPerMin * 4 + failPerMin * 3));

            return Math.Max(-MapMemoryMaxScorePenalty, Math.Min(MapMemoryMaxScoreBonus, bonus));
        }

        // ══════════════════════════════════════════════════════════════════════
        //  公共 API — 技能记忆
        // ══════════════════════════════════════════════════════════════════════

        public static void RecordSkillUse(string monsterName, MagicType skill, int estimatedDamage)
        {
            if (string.IsNullOrEmpty(monsterName) || skill == MagicType.None)
                return;

            var records = GetOrCreateSkillRecords(monsterName);

            SkillMonsterRecord rec = records.FirstOrDefault(r => r.Skill == skill);
            if (rec == null)
            {
                if (records.Count >= SkillMemoryMaxEntries)
                {
                    SkillMonsterRecord minRec = records.OrderBy(r => r.UseCount).First();
                    records.Remove(minRec);
                }

                rec = new SkillMonsterRecord { Skill = skill };
                records.Add(rec);
            }

            rec.UseCount++;
            rec.TotalDamageEstimate += estimatedDamage;
            _isDirty = true;
        }

        public static MagicType? GetBestSkillForMonster(string monsterName, IEnumerable<MagicType> candidates)
        {
            if (string.IsNullOrEmpty(monsterName) || candidates == null)
                return null;

            if (!_skillMonsterMemory.TryGetValue(monsterName, out List<SkillMonsterRecord> records))
                return null;

            var candidateSet = new HashSet<MagicType>(candidates);
            var validRecords = records
                .Where(r => r.UseCount >= SkillMemoryMinUses && candidateSet.Contains(r.Skill))
                .OrderByDescending(r => r.AverageDamage)
                .ToList();

            if (validRecords.Count == 0)
                return null;

            if (validRecords.Count >= 2)
            {
                double best = validRecords[0].AverageDamage;
                double second = validRecords[1].AverageDamage;
                if (best > second * 1.2)
                    return validRecords[0].Skill;
            }

            return null;
        }

        public static MagicType? GetWorstSkillForMonster(string monsterName, IEnumerable<MagicType> candidates)
        {
            if (string.IsNullOrEmpty(monsterName) || candidates == null)
                return null;

            if (!_skillMonsterMemory.TryGetValue(monsterName, out List<SkillMonsterRecord> records))
                return null;

            var candidateSet = new HashSet<MagicType>(candidates);
            var validRecords = records
                .Where(r => r.UseCount >= SkillMemoryMinUses && candidateSet.Contains(r.Skill))
                .OrderBy(r => r.AverageDamage)
                .ToList();

            if (validRecords.Count < 2)
                return null;

            double worst = validRecords[0].AverageDamage;
            double best = validRecords[validRecords.Count - 1].AverageDamage;
            if (best > 0 && worst < best * 0.6)
                return validRecords[0].Skill;

            return null;
        }

        // ══════════════════════════════════════════════════════════════════════
        //  持久化 API
        // ══════════════════════════════════════════════════════════════════════

        /// <summary>
        /// 从 JSON 文件加载持久化记忆。应在 BotManager.Start() 中调用。
        /// 若文件不存在或读取失败，静默忽略（使用空内存）。
        /// </summary>
        public static void Load()
        {
            string path = GetMemoryFilePath();
            if (!File.Exists(path)) return;

            try
            {
                byte[] bytes = File.ReadAllBytes(path);
                var serializer = new DataContractJsonSerializer(typeof(BotMemoryDataDto));
                BotMemoryDataDto dto;
                using (var ms = new MemoryStream(bytes))
                    dto = (BotMemoryDataDto)serializer.ReadObject(ms);

                if (dto == null) return;

                // 加载地图记忆
                if (dto.MapMemory != null)
                {
                    foreach (var m in dto.MapMemory)
                    {
                        if (m == null) continue;
                        _mapMemory[m.MapIndex] = new BotMapMemory
                        {
                            MapIndex = m.MapIndex,
                            TotalActiveSeconds = m.TotalActiveSeconds,
                            TotalKills = m.TotalKills,
                            TotalPickups = m.TotalPickups,
                            TotalBlockedMoves = m.TotalBlockedMoves,
                            TotalMagicFailures = m.TotalMagicFailures,
                            VisitCount = m.VisitCount,
                            LastVisitTime = new DateTime(m.LastVisitTimeTicks, DateTimeKind.Utc).ToLocalTime(),
                        };
                    }
                }

                // 加载技能记忆
                if (dto.SkillMemory != null)
                {
                    foreach (var entry in dto.SkillMemory)
                    {
                        if (entry == null || string.IsNullOrEmpty(entry.MonsterName)) continue;
                        var records = new List<SkillMonsterRecord>();
                        if (entry.Records != null)
                        {
                            foreach (var r in entry.Records)
                            {
                                if (r == null) continue;
                                records.Add(new SkillMonsterRecord
                                {
                                    Skill = (MagicType)r.Skill,
                                    UseCount = r.UseCount,
                                    TotalDamageEstimate = r.TotalDamageEstimate,
                                });
                            }
                        }
                        _skillMonsterMemory[entry.MonsterName] = records;
                    }
                }

                SEnvir.Log($"[BotMemory] 已加载历史记忆：{_mapMemory.Count} 张地图，{_skillMonsterMemory.Count} 种怪物技能数据。");
            }
            catch (Exception ex)
            {
                SEnvir.Log($"[BotMemory] 加载记忆文件失败（将使用空记忆）：{ex.Message}");
            }
        }

        /// <summary>
        /// 将当前内存数据保存到 JSON 文件。由 Tick() 定时自动调用；Stop/ClearAll 时也强制保存。
        /// </summary>
        public static void Save()
        {
            try
            {
                // 截断超出限制的数据（按最后访问时间保留最近的）
                var mapEntries = _mapMemory.Values
                    .OrderByDescending(m => m.LastVisitTime)
                    .Take(MaxMapMemoryEntries)
                    .Select(m => new BotMapMemoryDto
                    {
                        MapIndex = m.MapIndex,
                        TotalActiveSeconds = m.TotalActiveSeconds,
                        TotalKills = m.TotalKills,
                        TotalPickups = m.TotalPickups,
                        TotalBlockedMoves = m.TotalBlockedMoves,
                        TotalMagicFailures = m.TotalMagicFailures,
                        VisitCount = m.VisitCount,
                        LastVisitTimeTicks = m.LastVisitTime.ToUniversalTime().Ticks,
                    })
                    .ToList();

                var skillEntries = _skillMonsterMemory
                    .OrderByDescending(kv => kv.Value.Sum(r => r.UseCount))
                    .Take(MaxSkillMonsterEntries)
                    .Select(kv => new SkillMonsterEntryDto
                    {
                        MonsterName = kv.Key,
                        Records = kv.Value.Select(r => new SkillMonsterRecordDto
                        {
                            Skill = (int)r.Skill,
                            UseCount = r.UseCount,
                            TotalDamageEstimate = r.TotalDamageEstimate,
                        }).ToList(),
                    })
                    .ToList();

                var dto = new BotMemoryDataDto
                {
                    Version = 1,
                    SavedAtTicks = SEnvir.Now.ToUniversalTime().Ticks,
                    MapMemory = mapEntries,
                    SkillMemory = skillEntries,
                };

                var serializer = new DataContractJsonSerializer(typeof(BotMemoryDataDto));
                string path = GetMemoryFilePath();
                string tmpPath = path + ".tmp";

                using (var fs = new FileStream(tmpPath, FileMode.Create, FileAccess.Write, FileShare.None))
                    serializer.WriteObject(fs, dto);

                // 原子替换：先写临时文件再重命名，避免写入中断损坏文件
                if (File.Exists(path)) File.Delete(path);
                File.Move(tmpPath, path);

                _isDirty = false;
                _lastSaveTime = SEnvir.Now;
            }
            catch (Exception ex)
            {
                SEnvir.Log($"[BotMemory] 保存记忆文件失败：{ex.Message}");
            }
        }

        /// <summary>
        /// 定时维护：每 5 分钟自动保存一次（若有未保存变更）。
        /// 应在 BotTick 主循环中调用。
        /// </summary>
        public static void Tick()
        {
            if (!_isDirty) return;
            if (_lastSaveTime == DateTime.MinValue)
                _lastSaveTime = SEnvir.Now;

            if ((SEnvir.Now - _lastSaveTime).TotalSeconds >= AutoSaveIntervalSeconds)
                Save();
        }

        /// <summary>
        /// 清除所有内存数据，并将当前状态保存到文件（Stop 时调用）。
        /// </summary>
        public static void ClearAll()
        {
            // 先保存再清除，保留本次会话积累的经验
            if (_isDirty)
                Save();

            _mapMemory.Clear();
            _skillMonsterMemory.Clear();
            _isDirty = false;
        }

        // ══════════════════════════════════════════════════════════════════════
        //  内部方法
        // ══════════════════════════════════════════════════════════════════════

        private static BotMapMemory GetOrCreateMapMemory(int mapIndex)
        {
            BotMapMemory mem;
            if (!_mapMemory.TryGetValue(mapIndex, out mem))
            {
                mem = new BotMapMemory { MapIndex = mapIndex };
                _mapMemory[mapIndex] = mem;
            }
            return mem;
        }

        private static List<SkillMonsterRecord> GetOrCreateSkillRecords(string monsterName)
        {
            List<SkillMonsterRecord> records;
            if (!_skillMonsterMemory.TryGetValue(monsterName, out records))
            {
                records = new List<SkillMonsterRecord>();
                _skillMonsterMemory[monsterName] = records;
            }
            return records;
        }
    }
}
