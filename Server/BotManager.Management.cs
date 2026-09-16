using Library;
using Server;
using Server.Models;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Threading;

namespace Server.Envir
{
    public enum BotRuntimeQuickTuningTarget
    {
        Aggression,
        Activity,
        PotionMinimums
    }

    public sealed class BotRuntimeQuickTuningSnapshot
    {
        public bool Active { get; private set; }
        public bool Changed { get; private set; }
        public int AggressionPercent { get; private set; }
        public int ActivityPercent { get; private set; }
        public int MinHealthPotionCount { get; private set; }
        public int MinManaPotionCount { get; private set; }
        public string Message { get; private set; }

        public BotRuntimeQuickTuningSnapshot(bool active, bool changed, int aggressionPercent,
            int activityPercent, int minHealthPotionCount, int minManaPotionCount, string message)
        {
            Active = active;
            Changed = changed;
            AggressionPercent = aggressionPercent;
            ActivityPercent = activityPercent;
            MinHealthPotionCount = minHealthPotionCount;
            MinManaPotionCount = minManaPotionCount;
            Message = message ?? string.Empty;
        }
    }

    public enum BotLogKind
    {
        Activity,
        Operation
    }

    public sealed class BotBatchResult
    {
        public int Succeeded { get; set; }
        public int Failed { get; set; }
        public int Protected { get; set; }
        public int Skipped { get; set; }
        public int Timeout { get; set; }
        public int Queued { get; set; }
        public string ErrorMessage { get; set; }
    }

    public sealed class BotManagementRow
    {
        public string Name { get; set; }
        public int Level { get; set; }
        public int MapIndex { get; set; }
        public long Gold { get; set; }
        public string State { get; set; }
    }

    public sealed class BotManagementSnapshot
    {
        public bool IsRunning { get; private set; }
        public bool IsPaused { get; private set; }
        public int OnlineBotCount { get; private set; }
        public long TotalKills { get; private set; }
        public long TotalDeaths { get; private set; }
        public int CoveredMapCount { get; private set; }
        public long TotalGold { get; private set; }
        public double AverageLevel { get; private set; }
        public IReadOnlyList<BotManagementRow> Bots { get; private set; }
        public IReadOnlyList<string> ActivityLogs { get; private set; }
        public IReadOnlyList<string> OperationLogs { get; private set; }

        public BotManagementSnapshot(bool isRunning, bool isPaused, int onlineBotCount,
            long totalKills, long totalDeaths, int coveredMapCount, long totalGold,
            double averageLevel, IEnumerable<BotManagementRow> bots,
            IEnumerable<string> activityLogs, IEnumerable<string> operationLogs)
        {
            IsRunning = isRunning;
            IsPaused = isPaused;
            OnlineBotCount = onlineBotCount;
            TotalKills = totalKills;
            TotalDeaths = totalDeaths;
            CoveredMapCount = coveredMapCount;
            TotalGold = totalGold;
            AverageLevel = averageLevel;
            Bots = new List<BotManagementRow>(bots ?? Enumerable.Empty<BotManagementRow>()).AsReadOnly();
            ActivityLogs = new List<string>(activityLogs ?? Enumerable.Empty<string>()).AsReadOnly();
            OperationLogs = new List<string>(operationLogs ?? Enumerable.Empty<string>()).AsReadOnly();
        }
    }

    public static partial class BotManager
    {
        private const int ManagementLogCapacity = 300;
        private static readonly object _managementSync = new object();
        private static readonly List<string> _activityLogs = new List<string>();
        private static readonly List<string> _operationLogs = new List<string>();
        private static readonly System.Collections.Concurrent.ConcurrentDictionary<uint, long> _botRecoverySeconds
            = new System.Collections.Concurrent.ConcurrentDictionary<uint, long>();
        private static int _managementPaused;
        private static long _sessionKills;
        private static long _sessionDeaths;
        private static bool _runtimeQuickTuningBaselineCaptured;
        private static int _runtimeQuickTuningBaselineAggression;
        private static int _runtimeQuickTuningBaselineActivity;
        private static int _runtimeQuickTuningBaselineMinHealthPotion;
        private static int _runtimeQuickTuningBaselineMinManaPotion;

        public static bool IsPaused => Volatile.Read(ref _managementPaused) != 0;

        public static BotRuntimeQuickTuningSnapshot AdjustRuntimeQuickTuning(
            BotRuntimeQuickTuningTarget target, int delta)
        {
            string message;
            BotRuntimeQuickTuningSnapshot snapshot;

            lock (_managementSync)
            {
                int onlineCount = SnapshotBotPlayers().Count(player => player != null && player.Node != null);
                if (onlineCount == 0)
                {
                    message = "当前没有在线假人，快捷调整未执行";
                    snapshot = CreateRuntimeQuickTuningSnapshotUnsafe(message);
                }
                else if (target != BotRuntimeQuickTuningTarget.Aggression
                    && target != BotRuntimeQuickTuningTarget.Activity
                    && target != BotRuntimeQuickTuningTarget.PotionMinimums)
                {
                    message = "快捷调整目标无效";
                    snapshot = CreateRuntimeQuickTuningSnapshotUnsafe(message);
                }
                else
                {
                    if (!_runtimeQuickTuningBaselineCaptured)
                        CaptureRuntimeQuickTuningBaselineUnsafe();

                    int oldValue;
                    int nextValue;
                    string targetName;
                    bool valueChanged = false;
                    string changeSummary = string.Empty;
                    switch (target)
                    {
                        case BotRuntimeQuickTuningTarget.Aggression:
                            oldValue = Config.BotAggressionPercent;
                            nextValue = ClampRuntimeQuickTuning(oldValue, delta, 0, 100);
                            Config.BotAggressionPercent = nextValue;
                            targetName = "攻击性";
                            valueChanged = nextValue != oldValue;
                            changeSummary = string.Format("{0}{1}",
                                nextValue - oldValue >= 0 ? "+" : string.Empty, nextValue - oldValue);
                            break;
                        case BotRuntimeQuickTuningTarget.Activity:
                            oldValue = Config.BotActivityPercent;
                            nextValue = ClampRuntimeQuickTuning(oldValue, delta, 0, 100);
                            Config.BotActivityPercent = nextValue;
                            targetName = "活跃度";
                            valueChanged = nextValue != oldValue;
                            changeSummary = string.Format("{0}{1}",
                                nextValue - oldValue >= 0 ? "+" : string.Empty, nextValue - oldValue);
                            break;
                        default:
                            oldValue = Config.BotMinHealthPotionCount;
                            int oldManaValue = Config.BotMinManaPotionCount;
                            nextValue = ClampRuntimeQuickTuning(oldValue, delta, 0, 10000);
                            int nextManaValue = ClampRuntimeQuickTuning(oldManaValue, delta, 0, 10000);
                            Config.BotMinHealthPotionCount = nextValue;
                            Config.BotMinManaPotionCount = nextManaValue;
                            targetName = "药水补给";
                            valueChanged = nextValue != oldValue || nextManaValue != oldManaValue;
                            changeSummary = string.Format("HP {0}->{1}, MP {2}->{3}",
                                oldValue, nextValue, oldManaValue, nextManaValue);
                            break;
                    }

                    if (!valueChanged)
                        message = targetName + (delta < 0 ? "已达到下限" : "已达到上限");
                    else
                        message = string.Format("快捷调整已应用：{0} {1}", targetName, changeSummary);
                    snapshot = CreateRuntimeQuickTuningSnapshotUnsafe(message);
                }
            }

            RecordManagementLog(BotLogKind.Operation, message);
            return snapshot;
        }

        public static BotRuntimeQuickTuningSnapshot GetRuntimeQuickTuningSnapshot()
        {
            lock (_managementSync)
                return CreateRuntimeQuickTuningSnapshotUnsafe(string.Empty);
        }

        public static bool ResetRuntimeQuickTuning(string reason)
        {
            bool reset;
            lock (_managementSync)
            {
                if (!_runtimeQuickTuningBaselineCaptured)
                    return false;

                Config.BotAggressionPercent = _runtimeQuickTuningBaselineAggression;
                Config.BotActivityPercent = _runtimeQuickTuningBaselineActivity;
                Config.BotMinHealthPotionCount = _runtimeQuickTuningBaselineMinHealthPotion;
                Config.BotMinManaPotionCount = _runtimeQuickTuningBaselineMinManaPotion;
                _runtimeQuickTuningBaselineCaptured = false;
                reset = true;
            }

            if (reset)
                RecordManagementLog(BotLogKind.Operation,
                    "运行时快捷调整已恢复保存基线" + (string.IsNullOrWhiteSpace(reason) ? string.Empty : "：" + reason));
            return reset;
        }

        public static void CommitRuntimeQuickTuningBaseline()
        {
            lock (_managementSync)
                CommitRuntimeQuickTuningBaselineUnsafe();
        }

        private static void CaptureRuntimeQuickTuningBaselineUnsafe()
        {
            _runtimeQuickTuningBaselineAggression = Config.BotAggressionPercent;
            _runtimeQuickTuningBaselineActivity = Config.BotActivityPercent;
            _runtimeQuickTuningBaselineMinHealthPotion = Config.BotMinHealthPotionCount;
            _runtimeQuickTuningBaselineMinManaPotion = Config.BotMinManaPotionCount;
            _runtimeQuickTuningBaselineCaptured = true;
        }

        private static void CommitRuntimeQuickTuningBaselineUnsafe()
        {
            _runtimeQuickTuningBaselineAggression = Config.BotAggressionPercent;
            _runtimeQuickTuningBaselineActivity = Config.BotActivityPercent;
            _runtimeQuickTuningBaselineMinHealthPotion = Config.BotMinHealthPotionCount;
            _runtimeQuickTuningBaselineMinManaPotion = Config.BotMinManaPotionCount;
            _runtimeQuickTuningBaselineCaptured = false;
        }

        private static BotRuntimeQuickTuningSnapshot CreateRuntimeQuickTuningSnapshotUnsafe(string message)
        {
            bool changed = _runtimeQuickTuningBaselineCaptured
                && (Config.BotAggressionPercent != _runtimeQuickTuningBaselineAggression
                    || Config.BotActivityPercent != _runtimeQuickTuningBaselineActivity
                    || Config.BotMinHealthPotionCount != _runtimeQuickTuningBaselineMinHealthPotion
                    || Config.BotMinManaPotionCount != _runtimeQuickTuningBaselineMinManaPotion);
            return new BotRuntimeQuickTuningSnapshot(_runtimeQuickTuningBaselineCaptured, changed,
                Config.BotAggressionPercent, Config.BotActivityPercent,
                Config.BotMinHealthPotionCount, Config.BotMinManaPotionCount, message);
        }

        private static int ClampRuntimeQuickTuning(int value, int delta, int minimum, int maximum)
        {
            long next = (long)value + delta;
            return (int)Math.Max(minimum, Math.Min(maximum, next));
        }

        public static bool ShouldTriggerScaledBehavior(int percent, uint stableKey, long window)
        {
            percent = Math.Max(0, Math.Min(100, percent));
            if (percent <= 0) return false;
            if (percent == 50 || percent >= 100) return true;

            unchecked
            {
                ulong value = ((ulong)stableKey * 11400714819323198485UL)
                              ^ ((ulong)window * 7046029254386353131UL);
                return (value % 100UL) < (ulong)(percent * 2);
            }
        }

        private static int ScaleLegacyChance(int legacyPercent, int behaviorPercent)
        {
            legacyPercent = Math.Max(0, Math.Min(100, legacyPercent));
            behaviorPercent = Math.Max(0, Math.Min(100, behaviorPercent));
            if (behaviorPercent <= 0) return 0;
            if (behaviorPercent == 50) return legacyPercent;
            return Math.Min(100, legacyPercent * behaviorPercent * 2 / 100);
        }

        public static void SetPaused(bool paused)
        {
            int next = paused ? 1 : 0;
            int previous = Interlocked.Exchange(ref _managementPaused, next);
            if (previous == next) return;

            RecordManagementLog(BotLogKind.Operation, paused ? "GM 暂停假人普通 AI" : "GM 继续假人普通 AI");
        }

        public static bool TryApplyManagementSettings(BotManagementSettings settings, bool persist, out string error)
        {
            error = string.Empty;
            if (settings == null)
            {
                error = "假人管理配置为空";
                RecordManagementLog(BotLogKind.Operation, error);
                return false;
            }

            if (!settings.TryValidate(out error))
            {
                RecordManagementLog(BotLogKind.Operation, "配置校验失败: " + error);
                return false;
            }

            lock (_managementSync)
            {
                BotManagementSettings oldSettings = BotManagementSettings.FromConfig();
                int oldCount = botCount;
                string oldFilePath = botFilePath;

                try
                {
                    settings.WriteToConfig();
                    if (persist) ConfigReader.Save();

                    botFilePath = settings.BotFilePath ?? string.Empty;
                    Interlocked.Exchange(ref botCount, settings.BotCount);

                    if (isRunning)
                    {
                        botTimer?.Change(0, Math.Max(1, Config.BotMainLoopIntervalMs));
                        botPotionTimer?.Change(0, Math.Max(1, Config.BotPotionMonitorIntervalMs));
                    }

                    RecordManagementLog(BotLogKind.Operation, persist ? "GM 已保存并应用假人配置" : "GM 已应用假人配置");
                    SEnvir.BotActionQueue.Enqueue(SynchronizeOnlineBotsOnMainThread);
                    if (persist) CommitRuntimeQuickTuningBaselineUnsafe();
                    return true;
                }
                catch (Exception ex)
                {
                    oldSettings.WriteToConfig();
                    botFilePath = oldFilePath;
                    Interlocked.Exchange(ref botCount, oldCount);
                    error = "假人管理配置应用失败: " + ex.Message;
                    RecordManagementLog(BotLogKind.Operation, error);
                    return false;
                }
            }
        }

        public static BotManagementSnapshot GetManagementSnapshot()
        {
            PlayerObject[] players = SnapshotBotPlayers();
            List<BotManagementRow> rows = new List<BotManagementRow>(players.Length);
            HashSet<int> maps = new HashSet<int>();
            long totalGold = 0;
            long totalLevel = 0;

            foreach (PlayerObject player in players)
            {
                if (player == null || player.Node == null) continue;

                int mapIndex = player.CurrentMap?.Info?.Index ?? -1;
                if (mapIndex >= 0) maps.Add(mapIndex);
                totalGold += Math.Max(0, player.Gold);
                totalLevel += Math.Max(0, player.Level);
                rows.Add(new BotManagementRow
                {
                    Name = player.Name ?? string.Empty,
                    Level = player.Level,
                    MapIndex = mapIndex,
                    Gold = player.Gold,
                    State = player.Connection != null && player.Connection.Connected ? "Online" : "Disconnected"
                });
            }

            string[] activity;
            string[] operations;
            lock (_managementSync)
            {
                activity = _activityLogs.ToArray();
                operations = _operationLogs.ToArray();
            }

            int count = rows.Count;
            return new BotManagementSnapshot(
                isRunning,
                IsPaused,
                count,
                Interlocked.Read(ref _sessionKills),
                Interlocked.Read(ref _sessionDeaths),
                maps.Count,
                totalGold,
                count == 0 ? 0 : (double)totalLevel / count,
                rows.ToArray(),
                activity,
                operations);
        }

        public static string GetBotMapProbabilityReport()
        {
            BotManagementSnapshot snapshot = GetManagementSnapshot();
            if (snapshot.Bots.Count == 0)
                return "当前没有在线假人。";

            int total = snapshot.Bots.Count;
            List<string> lines = new List<string>
            {
                "在线假人地图分布（当前快照）",
                "地图池加成: " + Config.BotMapPoolBonus,
                ""
            };

            foreach (IGrouping<int, BotManagementRow> group in snapshot.Bots
                .GroupBy(row => row.MapIndex)
                .OrderByDescending(group => group.Count())
                .ThenBy(group => group.Key))
            {
                Map map = group.Key >= 0 ? SEnvir.GetMap(group.Key) : null;
                string mapName = map?.Info?.Description;
                if (string.IsNullOrWhiteSpace(mapName))
                    mapName = group.Key < 0 ? "未知地图" : "MapIndex=" + group.Key;

                lines.Add(string.Format("{0} (Index={1}): {2} 名 ({3:0.00}%)",
                    mapName, group.Key, group.Count(), group.Count() * 100.0 / total));
            }

            return string.Join(Environment.NewLine, lines);
        }

        public static BotBatchResult SetTargetOnlineCount(int count)
        {
            if (count < 0 || count > 10000)
            {
                string error = "在线假人数量必须在 0 到 10000 之间";
                RecordManagementLog(BotLogKind.Operation, error);
                return new BotBatchResult { Failed = 1, ErrorMessage = error };
            }

            Interlocked.Exchange(ref botCount, count);
            Config.BotCount = count;
            RecordManagementLog(BotLogKind.Operation, "GM 将假人目标数量设为 " + count + "；不立即踢出当前在线假人");
            return new BotBatchResult { Succeeded = 1 };
        }

        public static BotBatchResult SyncOnlineBots()
        {
            PlayerObject[] players = SnapshotBotPlayers();
            if (players.Length == 0)
            {
                RecordManagementLog(BotLogKind.Operation, "GM 同步在线假人：当前没有在线假人");
                return new BotBatchResult { Skipped = 1 };
            }

            SEnvir.BotActionQueue.Enqueue(SynchronizeOnlineBotsOnMainThread);
            RecordManagementLog(BotLogKind.Operation, "GM 已投递在线假人同步，数量: " + players.Length);
            return new BotBatchResult { Queued = players.Length };
        }

        public static BotBatchResult TrimOnlineBotsToMaxOnline()
        {
            BotManagementSnapshot snapshot = GetManagementSnapshot();
            int excess = Math.Max(0, snapshot.OnlineBotCount - Math.Max(0, Config.BotMaxOnline));
            if (excess == 0)
                return new BotBatchResult { Skipped = 1, ErrorMessage = "当前在线数量未超过最大在线" };

            BotBatchResult result = new BotBatchResult { Queued = excess };
            using (ManualResetEventSlim waitHandle = new ManualResetEventSlim(false))
            {
                SEnvir.BotActionQueue.Enqueue(() =>
                {
                    try
                    {
                        PlayerObject[] players = SnapshotBotPlayers()
                            .Where(player => player != null && player.Node != null && !player.Dead)
                            .OrderByDescending(player => player.ObjectID)
                            .Take(excess)
                            .ToArray();

                        foreach (PlayerObject player in players)
                        {
                            try
                            {
                                if (player.Connection == null || !player.Connection.Connected)
                                {
                                    result.Skipped++;
                                    continue;
                                }

                                player.Connection.Disconnect();
                                result.Succeeded++;
                            }
                            catch (Exception ex)
                            {
                                result.Failed++;
                                RecordManagementLog(BotLogKind.Operation,
                                    "下线超额假人失败 [" + (player.Name ?? string.Empty) + "]: " + ex.Message);
                            }
                        }

                        result.Skipped += Math.Max(0, excess - players.Length);
                    }
                    catch (Exception ex)
                    {
                        result.Failed++;
                        result.ErrorMessage = ex.Message;
                    }
                    finally
                    {
                        waitHandle.Set();
                    }
                });

                if (!waitHandle.Wait(8000))
                {
                    result.Timeout = 1;
                    result.ErrorMessage = "等待超额在线处理结果超时";
                }
            }

            RecordManagementLog(BotLogKind.Operation,
                "GM 处理超额在线：成功 " + result.Succeeded + "，失败 " + result.Failed
                + "，跳过 " + result.Skipped + "，超时 " + result.Timeout);
            return result;
        }

        private static void SynchronizeOnlineBotsOnMainThread()
        {
            foreach (PlayerObject player in SnapshotBotPlayers())
            {
                if (player == null || player.Node == null)
                {
                    RecordManagementLog(BotLogKind.Operation, "在线假人同步跳过：角色已离开地图");
                    continue;
                }

                try
                {
                    ApplyInitialGoldFloor(player);
                    ApplyBotConfigurationToOnlinePlayer(player);
                }
                catch (Exception ex)
                {
                    RecordManagementLog(BotLogKind.Operation,
                        "在线假人同步失败 [" + (player.Name ?? "") + "]: " + ex.Message);
                }
            }
        }

        private static void ApplyBotConfigurationToOnlinePlayer(PlayerObject player)
        {
            if (player?.Character?.Account == null) return;
            player.Character.Account.AllowGroup = Config.BotAllowGroup;
        }

        public static void ApplyInitialGoldFloor(PlayerObject player)
        {
            if (player == null) return;
            long floor = Math.Max(0L, Config.BotInitialGoldFloor);
            if (player.Gold >= floor) return;

            player.Gold = floor;
            player.GoldChanged();
        }

        public static void ProcessConfiguredRecovery(PlayerObject player)
        {
            if (player == null || player.Node == null || player.Dead) return;
            bool percentEnabled = Config.BotPercentRecoveryEnabled;
            bool fixedEnabled = Config.BotFixedRecoveryEnabled;
            if (percentEnabled == fixedEnabled) return;

            long second = SEnvir.Now.Ticks / TimeSpan.TicksPerSecond;
            if (_botRecoverySeconds.TryGetValue(player.ObjectID, out long lastSecond) && lastSecond == second)
                return;
            _botRecoverySeconds[player.ObjectID] = second;

            int maxHealth = Math.Max(0, player.Stats[Stat.Health]);
            int maxMana = Math.Max(0, player.Stats[Stat.Mana]);
            int healthGain;
            int manaGain;
            if (percentEnabled)
            {
                healthGain = (int)Math.Max(0L, maxHealth * (long)Math.Max(0, Config.BotPercentRecoveryPerSecond) / 100L);
                manaGain = (int)Math.Max(0L, maxMana * (long)Math.Max(0, Config.BotPercentRecoveryPerSecond) / 100L);
            }
            else
            {
                healthGain = Math.Max(0, Config.BotFixedRecoveryPerSecond);
                manaGain = healthGain;
            }

            if (healthGain > 0 && maxHealth > 0)
                player.SetHP(Math.Min(maxHealth, player.CurrentHP + healthGain));
            if (manaGain > 0 && maxMana > 0)
                player.SetMP(Math.Min(maxMana, player.CurrentMP + manaGain));
        }

        private static bool TryProcessBotAutoRebirth(PlayerObject player)
        {
            if (!Config.BotAutoRebirth || player == null || player.Character == null
                || player.Dead || player.Node == null || !player.InSafeZone)
                return false;

            int requiredLevel = Math.Max(1, Config.BotAutoRebirthLevel);
            int maxRebirth = Math.Max(0, Config.BotAutoRebirthMaxCount);
            if (player.Level < requiredLevel || player.Character.Rebirth >= maxRebirth)
                return false;

            try
            {
                player.NPCRebirth();
                RecordManagementLog(BotLogKind.Activity,
                    "假人自动转生 [" + (player.Name ?? string.Empty) + "]，转数: " + player.Character.Rebirth);
                return true;
            }
            catch (Exception ex)
            {
                RecordManagementLog(BotLogKind.Operation,
                    "假人自动转生失败 [" + (player.Name ?? string.Empty) + "]: " + ex.Message);
                return false;
            }
        }

        public static void RecordManagementLog(BotLogKind kind, string message)
        {
            string line = "[" + DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss.fff") + "] " + (message ?? string.Empty);
            lock (_managementSync)
            {
                List<string> buffer = kind == BotLogKind.Activity ? _activityLogs : _operationLogs;
                if (buffer.Count >= ManagementLogCapacity) buffer.RemoveAt(0);
                buffer.Add(line);
            }

            try
            {
                string directory = string.IsNullOrWhiteSpace(Config.BotLogDirectory) ? "./BotLogs" : Config.BotLogDirectory;
                Directory.CreateDirectory(directory);
                string fileName = kind == BotLogKind.Activity ? "activity.log" : "operations.log";
                File.AppendAllText(Path.Combine(directory, fileName), line + Environment.NewLine);
            }
            catch
            {
                // 日志目录不可写时保留内存缓冲，不影响服务器运行。
            }
        }

        public static void IncrementBotKillCount()
        {
            Interlocked.Increment(ref _sessionKills);
        }

        public static void IncrementBotDeathCount()
        {
            Interlocked.Increment(ref _sessionDeaths);
        }

        private static void ResetManagementCounters()
        {
            Interlocked.Exchange(ref _sessionKills, 0);
            Interlocked.Exchange(ref _sessionDeaths, 0);
        }
    }
}
