using Client.Controls;
using Client.Envir;
using Client.Extentions;
using Client.Models;
using Library;
using System;
using System.Drawing;
using C = Library.Network.ClientPackets;

namespace Client.Scenes.Views
{
    /// <summary>
    /// 屏幕中下按钮栏
    /// </summary>
    public sealed class PhoneDownCentPanel : DXControl
    {
        #region Properties
        /// <summary>
        /// 挖肉按钮
        /// </summary>
        private DXButton HarvestButton;
        /// <summary>
        /// 自动按钮
        /// </summary>
        public DXButton AutoAttackButton;
        /// <summary>
        /// 骑马按钮
        /// </summary>
        private DXButton HorseButton;
        /// <summary>
        /// 背包按钮
        /// </summary>
        //private DXButton InventoryButton;
        /// <summary>
        /// 技能按钮
        /// </summary>
        private DXButton MagicButton;
        /// <summary>
        /// 商城按钮
        /// </summary>
        //private DXButton MarketPlace;
        /// <summary>
        /// 排行榜按钮
        /// </summary>
        private DXButton RankingButton;
        /// <summary>
        /// 设置按钮
        /// </summary>
        private DXButton ConfigButton;
        /// <summary>
        /// 聊天按钮
        /// </summary>
        private DXButton ChatButton;
        /// <summary>
        /// 左右箭头开关按钮
        /// </summary>
        //private DXButton ToggleButtons;
       // private bool areButtonsVisible = true;

        #endregion

        /// <summary>
        /// 屏幕中下按钮栏
        /// </summary>
        public PhoneDownCentPanel()
        {
            DrawTexture = false;
            PassThrough = true;  //穿透开启

            //骑马按钮
            HorseButton = new DXButton
            {
                Parent = this,
                LibraryFile = LibraryFile.PhoneUI,
                Index = 154,
            };
            HorseButton.Tap += (o, e) =>
            {
                if (GameScene.Game.Observer) return;

                if (CEnvir.Now < GameScene.Game.User.NextActionTime || GameScene.Game.User.ActionQueue.Count > 0) return;
                if (CEnvir.Now < GameScene.Game.User.ServerTime) return;
                if (CEnvir.Now < MapObject.User.CombatTime.AddSeconds(10) && !GameScene.Game.Observer && GameScene.Game.User.Horse == HorseType.None)
                {
                    GameScene.Game.ReceiveChat("战斗中无法骑马".Lang(), MessageType.System);
                    return;
                }

                GameScene.Game.User.ServerTime = CEnvir.Now.AddSeconds(5);
                CEnvir.Enqueue(new C.Mount());
            };
            MagicButton = new DXButton //技能按钮
            {
               Parent = this,
                LibraryFile = LibraryFile.PhoneUI,
                Index = 150,
            };
            MagicButton.TouchUp += (o, e) =>
            {
                if (GameScene.Game.Observer) return;
                GameScene.Game.MagicBox.Visible = !GameScene.Game.MagicBox.Visible;
            };

            //自动按钮
            AutoAttackButton = new DXButton
            {
                Parent = this,
                LibraryFile = LibraryFile.PhoneUI,
                Index = 148,
                ForeColour = Color.DarkGray,
            };
            AutoAttackButton.TouchUp += (o, e) =>
            {
                if (GameScene.Game.MapControl.MapInfo.BanAndroidPlayer == true)
                    GameScene.Game.ReceiveChat("当前地图禁止挂机".Lang(), MessageType.System);   //提示并跳过
                else if (GameScene.Game.User.AutoTime == 0)   //判断挂机时间=0
                    GameScene.Game.ReceiveChat("[挂机时间不足]".Lang(), MessageType.System);
                else
                    GameScene.Game.BigPatchBox.Helper.AndroidPlayer.Checked = !GameScene.Game.BigPatchBox.Helper.AndroidPlayer.Checked;

                    GameScene.Game.AutoAttack = !GameScene.Game.AutoAttack;

                AutoAttackButton.ForeColour = GameScene.Game.AutoAttack ? Color.White : Color.DarkGray;

            };

            //挖肉按钮
            HarvestButton = new DXButton
            {
                Parent = this,
                LibraryFile = LibraryFile.PhoneUI,
                Index = 153,
            };
            HarvestButton.Tap += (o, e) =>
            {
                if (GameScene.Game.Observer) return;
                GameScene.Game.MapControl.Harvest = !GameScene.Game.MapControl.Harvest;
            };
            
            //排行榜按钮
            RankingButton = new DXButton
            {
                Parent = this,
                LibraryFile = LibraryFile.PhoneUI,
                Index = 146,
            };
            RankingButton.TouchUp += (o, e) =>
            {
                if (!CEnvir.ClientControl.RankingShowCheck) return;  //排行榜设置不显示就不设置快捷
                GameScene.Game.RankingBox.Visible = !GameScene.Game.RankingBox.Visible && CEnvir.Connection != null;
                //GameScene.Game.RankingBox.Location = new Point((GameScene.Game.Size.Width - GameScene.Game.RankingBox.Size.Width) / 2, (GameScene.Game.Size.Height - GameScene.Game.RankingBox.Size.Height) / 2);
            };
            //设置按钮
            ConfigButton = new DXButton
            {
                Parent = this,
                LibraryFile = LibraryFile.PhoneUI,
                Index = 147,
            };
            ConfigButton.TouchUp += (o, e) =>
            {
                if (GameScene.Game.Observer) return;   //如果是观察者 返回
                GameScene.Game.ConfigBox.Visible = !GameScene.Game.ConfigBox.Visible;
                //GameScene.Game.ConfigBox.Location = new Point((GameScene.Game.Size.Width - GameScene.Game.ConfigBox.Size.Width) / 2, (GameScene.Game.Size.Height - GameScene.Game.ConfigBox.Size.Height) / 2);
            };

            //聊天按钮
            ChatButton = new DXButton
            {
                Parent = this,
                LibraryFile = LibraryFile.PhoneUI,
                Index = 149,
            };
            ChatButton.Tap += (o, e) =>
            {
                if (GameScene.Game.Observer) return;
                GameScene.Game.ChatBox.Visible = !GameScene.Game.ChatBox.Visible;
            };

            //// 添加左右箭头开关按钮  //注释了  调到下边了 QQ715590
            //ToggleButtons = new DXButton
            //{
            //    Parent = this,
            //    LibraryFile = LibraryFile.PhoneUI,
            //    Index = 36, // 左箭头图标
            //    Location = new Point(0, 0),
            //    Size = new Size(30, 30)
            //};
            
            //ToggleButtons.TouchUp += (o, e) => 
            //{
            //    if (GameScene.Game.Observer) return;
                
            //    areButtonsVisible = !areButtonsVisible;
            //    ToggleButtons.Index = areButtonsVisible ? 36 : 37; // 切换箭头方向
                
            //    // 切换所有按钮的可见性
            //    AutoAttackButton.Visible = areButtonsVisible;
            //    MagicButton.Visible = areButtonsVisible;
            //    ChatButton.Visible = areButtonsVisible;
            //    RankingButton.Visible = areButtonsVisible;
            //    ConfigButton.Visible = areButtonsVisible;
            //    HarvestButton.Visible = areButtonsVisible;
            //    HorseButton.Visible = areButtonsVisible;
            //};

            //// 按照用户要求将所有按钮排成一行，每个按钮之间的间距为Width + 5
            //AutoAttackButton.Location = new Point(60, 0);
            //HarvestButton.Location = new Point(AutoAttackButton.Location.X + AutoAttackButton.Size.Width + 5, 0);
            //RankingButton.Location = new Point(HarvestButton.Location.X + HarvestButton.Size.Width + 5, 0);
            //HorseButton.Location = new Point(RankingButton.Location.X + RankingButton.Size.Width + 5, 0);
            //MagicButton.Location = new Point(HorseButton.Location.X + HorseButton.Size.Width + 5, 0);
            //ConfigButton.Location = new Point(MagicButton.Location.X + MagicButton.Size.Width + 5, 0);
            //ChatButton.Location = new Point(ConfigButton.Location.X + ConfigButton.Size.Width + 5, 0);
            //ToggleButtons.Location = new Point(ChatButton.Location.X + ChatButton.Size.Width + 5, 0);
            
            // 更新总大小
        //    Size = new Size(
        //        ToggleButtons.Location.X + ToggleButtons.Size.Width,
        //        Math.Max(
        //            AutoAttackButton.Size.Height,
        //            Math.Max(
        //                HarvestButton.Size.Height,
        //                Math.Max(
        //                    RankingButton.Size.Height,
        //                    Math.Max(
        //                        HorseButton.Size.Height,
        //                        Math.Max(
        //                            MagicButton.Size.Height,
        //                            Math.Max(ConfigButton.Size.Height, 
        //                            Math.Max(ChatButton.Size.Height, ToggleButtons.Size.Height))
        //                        )
        //                    )
        //                )
        //            )
        //        )
        //    );
        }
        #region Methods

        #endregion

        #region IDisposable

        protected override void Dispose(bool disposing)
        {
            base.Dispose(disposing);

            if (disposing)
            {
                if (HorseButton != null)
                {
                    if (!HorseButton.IsDisposed)
                        HorseButton.Dispose();

                    HorseButton = null;
                }
                if (MagicButton != null)
                {
                    if (!MagicButton.IsDisposed)
                        MagicButton.Dispose();

                    MagicButton = null;
                }
                if (HarvestButton != null)
                {
                    if (!HarvestButton.IsDisposed)
                        HarvestButton.Dispose();

                    HarvestButton = null;
                }

                //if (InventoryButton != null)
                //{
                //    if (!InventoryButton.IsDisposed)
                //        InventoryButton.Dispose();

                //    InventoryButton = null;
                //}

                if (MagicButton != null)
                {
                    if (!MagicButton.IsDisposed)
                        MagicButton.Dispose();

                    MagicButton = null;
                }

                //if (MarketPlace != null)
                //{
                //    if (!MarketPlace.IsDisposed)
                //        MarketPlace.Dispose();

                //    MarketPlace = null;
                //}

                if (RankingButton != null)
                {
                    if (!RankingButton.IsDisposed)
                        RankingButton.Dispose();

                    RankingButton = null;
                }

                if (ConfigButton != null)
                {
                    if (!ConfigButton.IsDisposed)
                        ConfigButton.Dispose();

                    ConfigButton = null;
                }

                if (ChatButton != null)
                {
                    if (!ChatButton.IsDisposed)
                        ChatButton.Dispose();

                    ChatButton = null;
                }

                //if (ToggleButtons != null)
                //{
                //    if (!ToggleButtons.IsDisposed)
                //        ToggleButtons.Dispose();

                //    ToggleButtons = null;
                //}

            }
        }
        #endregion
    }
}
