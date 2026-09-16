using Client.Controls;
using Client.Envir;
using Client.Extentions;
using Client.Models;
using Client.Scenes.Configs;
using Library;
using MonoGame.Extended;
using System;
using System.Drawing;
using C = Library.Network.ClientPackets;
using Color = System.Drawing.Color;
using Point = System.Drawing.Point;
using Rectangle = System.Drawing.Rectangle;

//Cleaned
namespace Client.Scenes.Views
{
    /// <summary>
    /// UI底部主面板qq715590
    /// </summary>
    public sealed class PhoneMainPanel : DXControl
    {
        #region Properties
        private DXControl HealthBar;
        private DXControl ManaBar;
        public DXControl Hpmpbar;
        public DXImageControl ChatBackImag;
        public DXLabel HealthBarLabel, ManaBarLabel;
        //private DXButton SystemButtion, SpeakButtion;
        private DXButton MagicButton;
        private DXButton MarketPlace;
        private DXButton ChatButton;
        #endregion

        /// <summary>
        /// 底部UI界面左边框
        /// </summary>
        public PhoneMainPanel()
        {
            Size = new Size(550, 200);
            PassThrough = true;  //穿透开启

            CEnvir.LibraryList.TryGetValue(LibraryFile.PhoneUI, out var Library);

            Hpmpbar = new DXImageControl
            {
                Parent = this,
                Location = new Point(245, 24),
                IsControl = false,
            };

            HealthBar = new DXControl
            {
                Parent = this,
                Size = new Size(38, 75),    // 固定原始尺寸
                Location = new Point(270, 24),
                IsControl = false,
            };

            HealthBar.BeforeDraw += (o, e) =>
            {
                if (Library == null) return;

                if (MapObject.User.Stats[Stat.Health] == 0) return;

                float percent = Math.Min(1, Math.Max(0, MapObject.User.CurrentHP / (float)MapObject.User.Stats[Stat.Health]));

                if (percent == 0) return;

                Size image = Library.GetSize(1374);

                if (image == Size.Empty) return;

                // 修改为垂直方向裁剪
                int offset = (int)(image.Height * (1.0 - percent));
                Rectangle area = new Rectangle(0, offset, image.Width, image.Height - offset);
                Library.Draw(1374, HealthBar.DisplayArea.X, HealthBar.DisplayArea.Y + offset, Color.White, area, 1F, ImageType.Image, zoomRate: ZoomRate, uiOffsetX: UI_Offset_X);
            };

            ManaBar = new DXControl
            {
                Parent = this,
                Size = new Size(33, 73),
                Location = new Point(301, 24),
                IsControl = false,
            };

            ManaBar.BeforeDraw += (o, e) =>
            {
                if (Library == null) return;

                if (MapObject.User.Stats[Stat.Mana] == 0) return;

                float percent = Math.Min(1, Math.Max(0, MapObject.User.CurrentMP / (float)MapObject.User.Stats[Stat.Mana]));

                if (percent == 0) return;

                Size image = Library.GetSize(1375);

                if (image == Size.Empty) return;

                // 修改为垂直方向裁剪
                int offset = (int)(image.Height * (1.0 - percent));
                Rectangle area = new Rectangle(0, offset, image.Width, image.Height - offset);
                Library.Draw(1375, ManaBar.DisplayArea.X, ManaBar.DisplayArea.Y + offset, Color.White, area, 1F, ImageType.Image, zoomRate: ZoomRate, uiOffsetX: UI_Offset_X);
            };
			
            ChatBackImag = new DXImageControl
            {
                Parent = this,
                LibraryFile = LibraryFile.PhoneUI,
                Index = 1377,
                ImageOpacity = 1.0F,
                Visible = true,
                Location = new Point(210, 20),
                IsControl = false,
            };


            HealthBarLabel = new DXLabel
            {
                DrawFormat = TextFormatFlags.VerticalCenter | TextFormatFlags.Left,
                Parent = ChatBackImag,
                AutoSize = false,
                Size = new Size(60, 30), // 指定明确宽度
                Location = new Point(27, 82),
                Font = new MonoGame.Extended.Font(Config.FontName, 10),
               // ForeColour = Color.Red,
                ForeColour = Color.White,
                IsControl = false,
            };

            ManaBarLabel = new DXLabel
            {
                Parent = ChatBackImag,
                AutoSize = false,
                Size = new Size(60, 30),
                Location = new Point(77, 82),
                //ForeColour = Color.Blue,
                ForeColour = Color.White,
                Font = new MonoGame.Extended.Font(Config.FontName, 10),
                DrawFormat = TextFormatFlags.VerticalCenter | TextFormatFlags.Right,
                IsControl = false,
            };
            /*
            MarketPlace = new DXButton
            {
                Parent = this,
                LibraryFile = LibraryFile.PhoneUI,
                Index = 151,
            };
            MarketPlace.Location = new Point(0, 0);
            MarketPlace.TouchUp += (o, e) =>
            {
                if (GameScene.Game.Observer) return;
                GameScene.Game.MarketPlaceBox.Visible = !GameScene.Game.MarketPlaceBox.Visible;
            };
            */
            /*
            MagicButton = new DXButton
            {
                Parent = this,
                LibraryFile = LibraryFile.PhoneUI,
                Index = 150,
            };
            MagicButton.Location = new Point(MarketPlace.Location.X, MarketPlace.Location.Y + MagicButton.Size.Height + 5);
            MagicButton.TouchUp += (o, e) =>
            {
                if (GameScene.Game.Observer) return;
                GameScene.Game.MagicBox.Visible = !GameScene.Game.MagicBox.Visible;
            };

            ChatButton = new DXButton
            {
                Parent = this,
                LibraryFile = LibraryFile.PhoneUI,
                Index = 150,
            };
            ChatButton.Location = new Point(Size.Width - ChatButton.Size.Width, MagicButton.Location.Y);
            ChatButton.TouchUp += (o, e) =>
            {
                if (GameScene.Game.Observer) return;
                GameScene.Game.ChatBox.Visible = !GameScene.Game.ChatBox.Visible;
            };*/

        }

        #region IDisposable

        protected override void Dispose(bool disposing)
        {
            base.Dispose(disposing);

            if (disposing)
            {
                //if (SystemButtion != null)
                //{
                //    if (!SystemButtion.IsDisposed)
                //        SystemButtion.Dispose();

                //    SystemButtion = null;
                //}

                //if (SpeakButtion != null)
                //{
                //    if (!SpeakButtion.IsDisposed)
                //        SpeakButtion.Dispose();

                //    SpeakButtion = null;
                //}
                if (HealthBar != null)
                {
                    if (!HealthBar.IsDisposed)
                        HealthBar.Dispose();

                    HealthBar = null;
                }

                if (ManaBar != null)
                {
                    if (!ManaBar.IsDisposed)
                        ManaBar.Dispose();

                    ManaBar = null;
                }

                /*
                if (MagicButton != null)
                {
                    if (!MagicButton.IsDisposed)
                        MagicButton.Dispose();

                    MagicButton = null;
                }

                if (MarketPlace != null)
                {
                    if (!MarketPlace.IsDisposed)
                        MarketPlace.Dispose();

                    MarketPlace = null;
                }
                */
                if (HealthBarLabel != null)
                {
                    if (!HealthBarLabel.IsDisposed)
                        HealthBarLabel.Dispose();

                    HealthBarLabel = null;
                }

                if (ManaBarLabel != null)
                {
                    if (!ManaBarLabel.IsDisposed)
                        ManaBarLabel.Dispose();

                    ManaBarLabel = null;
                }

                if (ChatBackImag != null)
                {
                    if (!ChatBackImag.IsDisposed)
                        ChatBackImag.Dispose();

                    ChatBackImag = null;
                }
            }
        }
        #endregion

    }
}
