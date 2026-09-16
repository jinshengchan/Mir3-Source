using Library;
using Server.DBModels;
using Server.Models;
using System;
using System.Collections.Generic;
using System.Linq;

namespace Server.Envir
{
    public sealed class BotRewardGap
    {
        public string BotId { get; set; }
        public string CharacterName { get; set; }
        public int Level { get; set; }
        public int MissingDefenseTiers { get; set; }
        public int MissingStrongElementTiers { get; set; }

        public bool HasMissingRewards => MissingDefenseTiers > 0 || MissingStrongElementTiers > 0;
    }

    public static partial class BotManager
    {
        private static readonly Stat[] BotRewardElementStats =
        {
            Stat.FireAttack,
            Stat.IceAttack,
            Stat.LightningAttack,
            Stat.WindAttack,
            Stat.HolyAttack,
            Stat.DarkAttack,
            Stat.PhantomAttack,
        };

        public static IReadOnlyList<BotRewardGap> GetMissingBotRewardReport()
        {
            List<BotRewardGap> result = new List<BotRewardGap>();
            foreach (BotAccountInfo bot in GetBotRewardAccounts())
            {
                CharacterInfo character = GetBotRewardCharacter(bot);
                if (character == null) continue;

                int expectedDefense = GetExpectedDefenseTier(character.Level);
                int expectedStrongElement = GetExpectedStrongElementTier(character.Level);
                int missingDefense = Math.Max(0, expectedDefense - Math.Max(0, bot.DefenseRewardTier));
                int missingStrongElement = Math.Max(0,
                    expectedStrongElement - Math.Max(0, bot.StrongElementRewardTier));
                if (missingDefense == 0 && missingStrongElement == 0) continue;

                result.Add(new BotRewardGap
                {
                    BotId = bot.BotId ?? string.Empty,
                    CharacterName = character.CharacterName ?? string.Empty,
                    Level = character.Level,
                    MissingDefenseTiers = missingDefense,
                    MissingStrongElementTiers = missingStrongElement,
                });
            }

            return result.AsReadOnly();
        }

        public static BotBatchResult BackfillMissingBotRewards()
        {
            BotBatchResult result = new BotBatchResult();
            foreach (BotAccountInfo bot in GetBotRewardAccounts())
            {
                CharacterInfo character = GetBotRewardCharacter(bot);
                if (character == null)
                {
                    result.Skipped++;
                    continue;
                }

                try
                {
                    PlayerObject onlinePlayer = botPlayers.FirstOrDefault(player =>
                        player?.IsBot == true && player.Character?.Account == bot.Account);
                    if (ApplyBotLevelRewards(bot, character.Level, onlinePlayer))
                        result.Succeeded++;
                    else
                        result.Skipped++;
                }
                catch (Exception ex)
                {
                    result.Failed++;
                    result.ErrorMessage = ex.Message;
                    RecordManagementLog(BotLogKind.Operation,
                        "假人奖励补发失败 [" + (character.CharacterName ?? string.Empty) + "]: " + ex.Message);
                }
            }

            RecordManagementLog(BotLogKind.Operation,
                "GM 执行假人奖励补发：成功 " + result.Succeeded + "，失败 " + result.Failed
                + "，跳过 " + result.Skipped);
            return result;
        }

        public static void ApplyBotLevelRewards(PlayerObject player)
        {
            if (player == null || !player.IsBot || player.Character?.Account == null)
                return;

            BotAccountInfo bot = FindBotRewardAccount(player.Character.Account);
            if (bot == null) return;

            if (ApplyBotLevelRewards(bot, player.Level, player))
            {
                RecordManagementLog(BotLogKind.Activity,
                    "假人等级奖励已补发 [" + (player.Name ?? string.Empty) + "]");
            }
        }

        private static bool ApplyBotLevelRewards(BotAccountInfo bot, int level, PlayerObject onlinePlayer)
        {
            if (bot == null) return false;

            bool changed = false;
            lock (bot)
            {
                Stats rewardStats = bot.LevelRewardStats == null
                    ? new Stats()
                    : new Stats(bot.LevelRewardStats);

                int expectedDefense = GetExpectedDefenseTier(level);
                int currentDefense = Math.Max(0, bot.DefenseRewardTier);
                if (expectedDefense > currentDefense && Config.BotDefenseBonusPerTier > 0)
                {
                    int tierCount = expectedDefense - currentDefense;
                    long amountLong = (long)tierCount * Config.BotDefenseBonusPerTier;
                    int amount = (int)Math.Min(int.MaxValue, Math.Max(0L, amountLong));
                    rewardStats[Stat.MinAC] += amount;
                    rewardStats[Stat.MaxAC] += amount;
                    rewardStats[Stat.MinMR] += amount;
                    rewardStats[Stat.MaxMR] += amount;
                    bot.DefenseRewardTier = expectedDefense;
                    changed = amount > 0;
                }

                int expectedStrongElement = GetExpectedStrongElementTier(level);
                int currentStrongElement = Math.Max(0, bot.StrongElementRewardTier);
                int typeCount = Math.Max(0, Math.Min(BotRewardElementStats.Length,
                    Config.BotStrongElementTypeCount));
                if (typeCount > 0 && expectedStrongElement > currentStrongElement)
                {
                    for (int tier = currentStrongElement + 1; tier <= expectedStrongElement; tier++)
                    {
                        List<Stat> candidates = new List<Stat>(BotRewardElementStats);
                        for (int i = 0; i < typeCount; i++)
                        {
                            int selectedIndex = SEnvir.Random.Next(candidates.Count);
                            Stat selected = candidates[selectedIndex];
                            candidates.RemoveAt(selectedIndex);
                            rewardStats[selected]++;
                        }

                        bot.LevelRewardStats = new Stats(rewardStats);
                        bot.StrongElementRewardTier = tier;
                        changed = true;
                    }
                }

                if (changed && bot.LevelRewardStats == null)
                    bot.LevelRewardStats = new Stats(rewardStats);
                else if (changed && !ReferenceEquals(bot.LevelRewardStats, rewardStats))
                    bot.LevelRewardStats = new Stats(rewardStats);
            }

            if (changed && onlinePlayer != null && onlinePlayer.Node != null)
                onlinePlayer.RefreshStats();

            return changed;
        }

        private static List<BotAccountInfo> GetBotRewardAccounts()
        {
            if (SEnvir.BotAccountInfoList?.Binding == null)
                return new List<BotAccountInfo>();

            return SEnvir.BotAccountInfoList.Binding
                .Where(bot => bot != null && bot.Account != null)
                .ToList();
        }

        private static CharacterInfo GetBotRewardCharacter(BotAccountInfo bot)
        {
            return bot?.Account?.Characters?.FirstOrDefault(character => character != null && !character.Deleted);
        }

        private static BotAccountInfo FindBotRewardAccount(AccountInfo account)
        {
            if (account == null || SEnvir.BotAccountInfoList?.Binding == null)
                return null;

            return SEnvir.BotAccountInfoList.Binding.FirstOrDefault(bot => bot?.Account == account);
        }

        private static int GetExpectedDefenseTier(int level)
        {
            int interval = Config.BotDefenseLevelInterval;
            return interval <= 0 ? 0 : Math.Max(0, level) / interval;
        }

        private static int GetExpectedStrongElementTier(int level)
        {
            if (Config.BotStrongElementStartLevel <= 0
                || Config.BotStrongElementLevelInterval <= 0
                || Config.BotStrongElementTypeCount <= 0
                || level < Config.BotStrongElementStartLevel)
                return 0;

            return (level - Config.BotStrongElementStartLevel)
                / Config.BotStrongElementLevelInterval + 1;
        }
    }
}
