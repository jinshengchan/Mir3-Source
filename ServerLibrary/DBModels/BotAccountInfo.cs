using Library;
using MirDB;
using Server.Envir;
using System;
using System.Collections.Generic;
using System.Linq;

namespace Server.DBModels
{
    /// <summary>
    /// 假人账户信息（用于区分真人和假人）
    /// </summary>
    [UserObject]
    public sealed class BotAccountInfo : DBObject
    {
        /// <summary>
        /// 对应账号
        /// </summary>
        public AccountInfo Account { get; set; }

        /// <summary>
        /// 假人是否已创建角色
        /// </summary>
        public bool CharacterCreated { get; set; }

        /// <summary>
        /// 假人当前状态
        /// </summary>
        public BotState BotState { get; set; }

        /// <summary>
        /// 最后活动时间
        /// </summary>
        public DateTime LastActionTime { get; set; }

        /// <summary>
        /// 当前所在地图
        /// </summary>
        public int CurrentMapIndex { get; set; }

        /// <summary>
        /// 目标地图索引
        /// </summary>
        public int TargetMapIndex { get; set; }

        /// <summary>
        /// 假人唯一标识
        /// </summary>
        public string BotId { get; set; }

        /// <summary>
        /// 已发放的双防奖励等级段数量。
        /// </summary>
        public int DefenseRewardTier { get; set; }

        /// <summary>
        /// 已发放的强元素奖励等级段数量。
        /// </summary>
        public int StrongElementRewardTier { get; set; }

        /// <summary>
        /// 假人等级奖励的实际累计属性，随机结果随账户持久化。
        /// </summary>
        public Stats LevelRewardStats { get; set; }

        protected override internal void OnCreated()
        {
            base.OnCreated();
            BotState = BotState.Idle;
            LastActionTime = Time.Now;
            LevelRewardStats = new Stats();
        }

        protected override internal void OnLoaded()
        {
            base.OnLoaded();
            if (LevelRewardStats == null)
                LevelRewardStats = new Stats();
        }
    }

    /// <summary>
    /// 假人状态
    /// </summary>
    public enum BotState
    {
        Idle,           //空闲
        Registering,    //注册中
        CreatingChar,   //创建角色中
        LoggingIn,      //登录中
        Playing,        //游戏中
        Fighting,       //战斗中
        Trading,        //交易中
        Grouping,       //组队中
        GuildWar,       //行会战中
    }
}
