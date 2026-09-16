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
    /// 手机UI左上主面板715590
    /// </summary>
    public sealed class PhoneLeftUpUserPanel : DXControl
    {
        #region Properties
        private DXControl HealthBar, ManaBar;
        public DXControl Hpmpbar;
        private DXImageControl /*FlagImage, */PhotoImage, dynamicImage, LevelImage;
        public DXImageControl ChatBackImag, ClassImage;
        public DXLabel HealthBarLabel, ManaBarLabel, LevelLabel;
        public DXButton AttackModeButton, PetModeButton, /*TownReviveButton, */PartnerTeleportButton;
        public DXLabel TotalPowerLabel; // 新增总战力标签
        public DXLabel CharacterNameLabel; // 新增角色名字标签
        #endregion

        /// <summary>
        /// 左上头像框
        /// </summary>
        public PhoneLeftUpUserPanel()
        {
            Size = new Size(720, 768);
            PassThrough = true;  //穿透开启

            CEnvir.LibraryList.TryGetValue(LibraryFile.PhoneUI, out var Library);

            //FlagImage = new DXImageControl
            //{
            //    Parent = this,
            //    LibraryFile = LibraryFile.PhoneUI,
            //    Index = 4,
            //    ImageOpacity = 1.0F,
            //    Visible = true,
            //    Location = new Point(0, 0),
            //};

            /*Hpmpbar = new DXImageControl
            {
                Parent = this,
                Location = new Point(245, 450),
                IsControl = false,
            };

            HealthBar = new DXControl
            {
                Parent = this,
                Size = new Size(38, 75),    // 固定原始尺寸
                Location = new Point(270, 418),
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
                Location = new Point(301, 420),
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
                Location = new Point(210, 415),
                IsControl = false,
            };


            HealthBarLabel = new DXLabel
            {
                DrawFormat = TextFormatFlags.VerticalCenter | TextFormatFlags.Left,
                Parent = ChatBackImag,
                AutoSize = false,
                Size = new Size(60, 30), // 指定明确宽度
                Location = new Point(37, 82),
                Font = new MonoGame.Extended.Font(Config.FontName, 10),
                ForeColour = Color.Red,
                IsControl = false,
            };

            ManaBarLabel = new DXLabel
            {
                Parent = ChatBackImag,
                AutoSize = false,
                Size = new Size(60, 30),
                Location = new Point(78, 82),
                ForeColour = Color.Blue,
                Font = new MonoGame.Extended.Font(Config.FontName, 10),
                DrawFormat = TextFormatFlags.VerticalCenter | TextFormatFlags.Right,
                IsControl = false,
            };
            */

            AttackModeButton = new DXButton
            {
                Parent = this,
                LibraryFile = LibraryFile.PhoneUI,
                Index = 22,
            };
            AttackModeButton.Location = new Point(80, 90);
            AttackModeButton.TouchUp += (o, e) =>
            {
                if (GameScene.Game.Observer) return;
                GameScene.Game.User.AttackMode = (AttackMode)(((int)GameScene.Game.User.AttackMode + 1) % 5);
                CEnvir.Enqueue(new C.ChangeAttackMode { Mode = GameScene.Game.User.AttackMode });
            };

            PetModeButton = new DXButton
            {
                Parent = this,
                LibraryFile = LibraryFile.PhoneUI,
                Index = 31,
                Location = new Point(68, 160),
                Visible = true,
            };
            PetModeButton.Location = new Point(AttackModeButton.Location.X + AttackModeButton.Size.Width - 17, AttackModeButton.Location.Y);
            PetModeButton.TouchUp += (o, e) =>
            {
                if (GameScene.Game.Observer) return;

                GameScene.Game.User.PetMode = (PetMode)(((int)GameScene.Game.User.PetMode + 1) % 5);
                CEnvir.Enqueue(new C.ChangePetMode { Mode = GameScene.Game.User.PetMode });
            };

            //TownReviveButton = new DXButton
            //{
            //    Parent = this,
            //    LibraryFile = LibraryFile.PhoneUI,
            //    Index = 32,
            //    Location = new Point(98, 160),
            //    Visible = true,
            //};
            //TownReviveButton.Location = new Point(PetModeButton.Location.X + PetModeButton.Size.Width + 5, AttackModeButton.Location.Y);
            //TownReviveButton.TouchUp += (o, e) =>
            //{
            //    if (GameScene.Game.Observer) return;

            //    if (!GameScene.Game.User.Dead) return;
            //    //沙巴克复活时间增加15秒  地图是沙巴克地图  处于攻城时间
            //    CastleInfo warCastle = GameScene.Game.ConquestWars.FirstOrDefault(x => x.Map == GameScene.Game.MapControl.MapInfo);
            //    if (CEnvir.Now < MapObject.User.WarReviveTime.AddSeconds(15) && GameScene.Game.MapControl.MapInfo.Index == 25 && warCastle != null)
            //    {
            //        foreach (CastleInfo castle in GameScene.Game.ConquestWars)   //攻城时的颜色设置 遍历行会攻城站
            //        {
            //            if (castle.Map != GameScene.Game.MapControl.MapInfo) continue;   //如果攻城站地图信息不对 继续

            //            if (GameScene.Game.CastleOwners.TryGetValue(castle, out string ownerGuild))
            //            {
            //                if (ownerGuild == GameScene.Game.User.Title)
            //                {
            //                    GameScene.Game.ReceiveChat($"死亡复活冷却延迟 {(MapObject.User.WarReviveTime.AddSeconds(15) - CEnvir.Now).TotalSeconds.ToString("0")} 秒。", MessageType.System);
            //                    return;
            //                }
            //                else
            //                {
            //                    CEnvir.Enqueue(new C.TownRevive());
            //                    return;
            //                }
            //            }
            //        }
            //    }
            //    CEnvir.Enqueue(new C.TownRevive());
            //};

            PartnerTeleportButton = new DXButton
            {
                Parent = this,
                LibraryFile = LibraryFile.PhoneUI,
                Index = 33,
                Location = new Point(68, 160),
                Visible = true,
            };
            PartnerTeleportButton.Location = new Point(PetModeButton.Location.X + PetModeButton.Size.Width - 17, AttackModeButton.Location.Y);
            PartnerTeleportButton.TouchUp += (o, e) =>
            {
                if (GameScene.Game.Observer) return;

                CEnvir.Enqueue(new C.MarriageTeleport());
            };

            PhotoImage = new DXImageControl
            {
                Parent = this,
                LibraryFile = LibraryFile.PhoneUI,
                Index = 40,
                ImageOpacity = 1.0F,
                Visible = true,
                Location = new Point(13, 20),
                IsControl = false,
            };
            PhotoImage.BeforeDraw += (o, e) =>
            {
                if (MapObject.User == null) return;

                PhotoImage.Index = (MapObject.User.Class == MirClass.Warrior && MapObject.User.Gender == MirGender.Male) ? 40 :
                        ((MapObject.User.Class == MirClass.Warrior && MapObject.User.Gender == MirGender.Female) ? 41 :
                        ((MapObject.User.Class == MirClass.Wizard && MapObject.User.Gender == MirGender.Male) ? 42 :
                        ((MapObject.User.Class == MirClass.Wizard && MapObject.User.Gender == MirGender.Female) ? 43 :
                        ((MapObject.User.Class == MirClass.Taoist && MapObject.User.Gender == MirGender.Male) ? 44 :
                        ((MapObject.User.Class == MirClass.Taoist && MapObject.User.Gender == MirGender.Female) ? 45 :
                        ((MapObject.User.Class == MirClass.Assassin && MapObject.User.Gender == MirGender.Male) ? 46 : 47))))));
            };

            DXImageControl photoImage = new DXImageControl
            {
                Parent = this,
                LibraryFile = LibraryFile.PhoneUI,
                Index = 1,
                ImageOpacity = 1.0F,
                Visible = true,
                Location = new Point(0, 20),
            };
            photoImage.TouchUp += (o, e) =>
            {
                GameScene.Game.UserFunctionControl.Visible = !GameScene.Game.UserFunctionControl.Visible;
            };

            ClassImage = new DXImageControl
            {
                Parent = this,
                LibraryFile = LibraryFile.PhoneUI,
                Index = 20,
                ImageOpacity = 1.0F,
                Visible = true,
                Location = new Point(11, 9),
                IsControl = false,
            };


              DXImageControl dynamicImage = new DXImageControl
            {
                Parent = ClassImage,
                 LibraryFile = LibraryFile.PhoneUI,
                Index = 130, // 初始索引
                ImageOpacity = 1.0F,
                Visible = true,
                Location = new Point(90, 12),
                IsControl = false,
            };

            // 记录当前帧索引和上一帧更新时间
            int currentFrame = 130;
            DateTime lastUpdateTime = DateTime.Now;
            const int frameCount = 8; // 总帧数
            const int frameInterval = 500; // 帧间隔时间（毫秒）

            dynamicImage.BeforeDraw += (o, e) =>
            {
                 DateTime now = DateTime.Now;
                // 检查是否达到帧间隔时间
                if ((now - lastUpdateTime).TotalMilliseconds >= frameInterval) 
                {
                    currentFrame = 130 + (currentFrame + 1 - 130) % frameCount; // 确保在 130 - 137 范围内循环
                    dynamicImage.Index = currentFrame;
                    lastUpdateTime = now;
                }
            };

            /*
            // 添加一个标签来显示职业名称和性别
            DXLabel classAndGenderLabel = new DXLabel
            {
                Parent = ClassImage,
                AutoSize = true,
                Font = new MonoGame.Extended.Font(Config.FontName, 10),
                ForeColour = Color.Red,
                DrawFormat = TextFormatFlags.VerticalCenter | TextFormatFlags.HorizontalCenter,
                IsControl = false,
            };

            classAndGenderLabel.BeforeDraw += (o, e) =>
            {
                if (MapObject.User == null) return;

                string classStr = "";
                switch (MapObject.User.Class)
                {
                    case MirClass.Warrior:
                        classStr = "战士";
                        break;
                    case MirClass.Wizard:
                        classStr = "法师";
                        break;
                    case MirClass.Taoist:
                        classStr = "道士";
                        break;
                    case MirClass.Assassin:
                        classStr = "刺客";
                        break;
                }

                string genderStr = MapObject.User.Gender == MirGender.Male ? "男" : "女";
                classAndGenderLabel.Text = $"{classStr}{genderStr}";
            };
            */
            LevelImage = new DXImageControl
            {
                Parent = this,
                LibraryFile = LibraryFile.PhoneUI,
                Index = 5,
                ImageOpacity = 1.0F,
                Visible = true,
                Location = new Point(210, 56),
                IsControl = false,
            };
            LevelImage = new DXImageControl
            {
                Parent = this,
                LibraryFile = LibraryFile.PhoneUI,
                Index = 5,
                ImageOpacity = 1.0F,
                Visible = true,
                Location = new Point(210, 56),
                IsControl = false,
            };
            LevelLabel = new DXLabel
            {
                Parent = LevelImage,
                AutoSize = false,
                Size = LevelImage.Size,
                ForeColour = Color.FromArgb(255, 255, 128, 0),
                DrawFormat = TextFormatFlags.VerticalCenter | TextFormatFlags.HorizontalCenter,
                IsControl = false,
            };

            // 新增总战力标签初始化
            TotalPowerLabel = new DXLabel
            {
                Parent = this,
                AutoSize = false,
                Size = new Size(200, 30),
                Location = new Point(160, 23),
                ForeColour = Color.White,
                Font = new MonoGame.Extended.Font(Config.FontName, 14),
                DrawFormat = TextFormatFlags.VerticalCenter | TextFormatFlags.Left,
                IsControl = false,
            };

            TotalPowerLabel.BeforeDraw += (o, e) =>
            {
                if (MapObject.User == null) return;
                
                // 计算攻击力、魔法力、道术力总和
                int totalPower = MapObject.User.Stats[Stat.MaxDC] + 
                               MapObject.User.Stats[Stat.MaxMC] + 
                               MapObject.User.Stats[Stat.MaxSC];
                
                TotalPowerLabel.Text = $" {totalPower}";
            };

            // 角色名字标签 - 添加在角色头像右侧x110 y50位置
            CharacterNameLabel = new DXLabel
            {
                Parent = this,
                AutoSize = false,
                Size = new Size(150, 29),
                Location = new Point(105, 54),
                ForeColour = Color.White,
                Font = new MonoGame.Extended.Font(Config.FontName, 13),
                DrawFormat = TextFormatFlags.VerticalCenter | TextFormatFlags.Left,
                IsControl = false,
            };

            CharacterNameLabel.BeforeDraw += (o, e) =>
            {
                if (MapObject.User == null) return;
                CharacterNameLabel.Text = MapObject.User.Name;
            };

        }

        public void AttackModeChanged()
        {
            if (MapObject.User == null) return;

            switch (MapObject.User.AttackMode)
            {
                case AttackMode.Peace:
                    AttackModeButton.Index = 22;
                    break;
                case AttackMode.Group:
                    AttackModeButton.Index = 23;
                    break;
                case AttackMode.Guild:
                    AttackModeButton.Index = 24;
                    break;
                case AttackMode.WarRedBrown:
                    AttackModeButton.Index = 25;
                    break;
                case AttackMode.All:
                    AttackModeButton.Index = 26;
                    break;
            }
        }

        public void PetModeChanged()
        {
            if (MapObject.User == null) return;

            switch (MapObject.User.PetMode)
            {
                case PetMode.Both:
                    PetModeButton.Index = 27;
                    break;
                case PetMode.Move:
                    PetModeButton.Index = 28;
                    break;
                case PetMode.Attack:
                    PetModeButton.Index = 29;
                    break;
                case PetMode.PvP:
                    PetModeButton.Index = 30;
                    break;
                case PetMode.None:
                    PetModeButton.Index = 31;
                    break;
            }
        }

        #region IDisposable

        protected override void Dispose(bool disposing)
        {
            base.Dispose(disposing);

            if (disposing) 
            {
        
            if (HealthBar != null)
        {
            if (!HealthBar.IsDisposed)
                HealthBar.Dispose();

            HealthBar = null;
        }
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

                //if (FlagImage != null)
                //{
                //    if (!FlagImage.IsDisposed)
                //        FlagImage.Dispose();

                //    FlagImage = null;
                //}

                if (LevelImage != null)
                {
                    if (!LevelImage.IsDisposed)
                        LevelImage.Dispose();

                    LevelImage = null;
                }

                if (LevelLabel != null)
                {
                    if (!LevelLabel.IsDisposed)
                        LevelLabel.Dispose();

                    LevelLabel = null;
                }

                if (PhotoImage != null)
                {
                    if (!PhotoImage.IsDisposed)
                        PhotoImage.Dispose();

                    PhotoImage = null;
                }
                if (dynamicImage != null)
                {
                    if (!dynamicImage.IsDisposed)
                        dynamicImage.Dispose();

                    dynamicImage = null;
                }


                if (AttackModeButton != null)
                {
                    if (!AttackModeButton.IsDisposed)
                        AttackModeButton.Dispose();

                    AttackModeButton = null;
                }

                if (PetModeButton != null)
                {
                    if (!PetModeButton.IsDisposed)
                        PetModeButton.Dispose();

                    PetModeButton = null;
                }

                //if (TownReviveButton != null)
                //{
                //    if (!TownReviveButton.IsDisposed)
                //        TownReviveButton.Dispose();

                //    TownReviveButton = null;
                //}

                if (PartnerTeleportButton != null)
                {
                    if (!PartnerTeleportButton.IsDisposed)
                        PartnerTeleportButton.Dispose();

                    PartnerTeleportButton = null;
                }

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

                if (TotalPowerLabel != null)
                {
                    if (!TotalPowerLabel.IsDisposed)
                        TotalPowerLabel.Dispose();

                    TotalPowerLabel = null;
                }

                if (CharacterNameLabel != null)
                {
                    if (!CharacterNameLabel.IsDisposed)
                        CharacterNameLabel.Dispose();

                    CharacterNameLabel = null;
                }
            }
        }
        #endregion

    }

    public class PhoneUserFunctionControl : DXControl
    {
        private DXButton DKeyButton,WarWeaponButton, /*RankingButton, */BonusPoolButton, BigPatchButton, RateQueryButton, CompanionButton, FixedPointButton, ExitButton;

        /// <summary>
        /// 商城按钮
        /// </summary>
        private DXButton MarketPlace;
        public PhoneUserFunctionControl()
        {
            DrawTexture = true;
            BackColour = Color.Black;
            Opacity = 0.7f;
            Size = new Size(72, 6 * 27 + 19 * 10);
            //LibraryFile = LibraryFile.PhoneUI;
            //Index = 100;

            //GuildButton = new DXButton
            //{
            //    Parent = this,
            //    LibraryFile = LibraryFile.PhoneUI,
            //    Index = 108,
            //};
            //GuildButton.Location = new Point((Size.Width - GuildButton.Size.Width) / 2, 10);
            //GuildButton.TouchUp += (o, e) =>
            //{
            //    if (GameScene.Game.Observer) return;
            //    GameScene.Game.GuildBox.Visible = !GameScene.Game.GuildBox.Visible;
            //};


            DKeyButton = new DXButton   //D先屏蔽
            {
                Parent = this,
                LibraryFile = LibraryFile.PhoneUI,
                Index = 119,
            };
            DKeyButton.Location = new Point((Size.Width - DKeyButton.Size.Width) / 2, 10);
            DKeyButton.TouchUp += (o, e) =>
            {
                if (GameScene.Game.Observer) return;
                if (GameScene.Game.NPCBox.Visible == true)
                {
                    GameScene.Game.NPCBox.Visible = false;
                    return;
                }
                if (GameScene.Game.NPCDKeyBox.Visible == true)
                {
                    GameScene.Game.NPCDKeyBox.Visible = false;
                    return;
                }
                //发包 D键
                CEnvir.Enqueue(new C.DKey { });
            };



            WarWeaponButton = new DXButton
            {
                Parent = this,
                LibraryFile = LibraryFile.PhoneUI,
                Index = 110,
            };
            //WarWeaponButton.Location = new Point((Size.Width - WarWeaponButton.Size.Width) / 2, 10);
            WarWeaponButton.Location = new Point(DKeyButton.Location.X, DKeyButton.Location.Y + DKeyButton.Size.Height + 10);
            WarWeaponButton.TouchUp += (o, e) =>
            {
                if (GameScene.Game.Observer) return;
                if (GameScene.Game.WarWeaponID != 0)
                    GameScene.Game.WarWeaponBox.Visible = !GameScene.Game.WarWeaponBox.Visible;
                else
                    GameScene.Game.WarWeaponBox.Visible = false;
            };

            //RankingButton = new DXButton
            //{
            //    Parent = this,
            //    LibraryFile = LibraryFile.PhoneUI,
            //    Index = 112,
            //};
            //RankingButton.Location = new Point(WarWeaponButton.Location.X, WarWeaponButton.Location.Y + WarWeaponButton.Size.Height + 10);
            //RankingButton.TouchUp += (o, e) =>
            //{
            //    if (!CEnvir.ClientControl.RankingShowCheck) return;  //排行榜设置不显示就不设置快捷
            //    GameScene.Game.RankingBox.Visible = !GameScene.Game.RankingBox.Visible && CEnvir.Connection != null;
            //    //GameScene.Game.RankingBox.Location = new Point((GameScene.Game.Size.Width - GameScene.Game.RankingBox.Size.Width) / 2, (GameScene.Game.Size.Height - GameScene.Game.RankingBox.Size.Height) / 2);
            //};

            MarketPlace = new DXButton
            {
                Parent = this,
                LibraryFile = LibraryFile.PhoneUI,
                Index = 124,
            };
            MarketPlace.Location = new Point(WarWeaponButton.Location.X, WarWeaponButton.Location.Y + WarWeaponButton.Size.Height + 10);
            MarketPlace.TouchUp += (o, e) =>
            {
                if (GameScene.Game.Observer) return;
                GameScene.Game.MarketPlaceBox.Visible = !GameScene.Game.MarketPlaceBox.Visible;
            };

            BonusPoolButton = new DXButton
            {
                Parent = this,
                LibraryFile = LibraryFile.PhoneUI,
                Index = 114,
            };
            BonusPoolButton.Location = new Point(MarketPlace.Location.X, MarketPlace.Location.Y + MarketPlace.Size.Height + 10);
            BonusPoolButton.TouchUp += (o, e) =>
            {
                if (GameScene.Game.Observer) return;
                GameScene.Game.BonusPoolVersionBox.Visible = !GameScene.Game.BonusPoolVersionBox.Visible;
            };


            CompanionButton = new DXButton  //宠物按钮
            {
                Parent = this,
                LibraryFile = LibraryFile.PhoneUI,
                Index = 128,  // 注释掉原Index设置

            };
            CompanionButton.Location = new Point(BonusPoolButton.Location.X, BonusPoolButton.Location.Y + BonusPoolButton.Size.Height + 10);
            CompanionButton.TouchUp += (o, e) =>
            {
                if (Globals.CompanionInfoList.Count == 0)
                {
                    CompanionButton.Visible = false;
                }
                else
                {
                    CompanionButton.Visible = true;
                    CompanionButton.Hint = "宠物".Lang() + "(I)";
                    CompanionButton.MouseClick += (o, e) => GameScene.Game.CompanionBox.Visible = !GameScene.Game.CompanionBox.Visible;
                }
            };


            BigPatchButton = new DXButton
            {
                Parent = this,
                LibraryFile = LibraryFile.PhoneUI,
                Index = 116,
            };
            BigPatchButton.Location = new Point(CompanionButton.Location.X, CompanionButton.Location.Y + CompanionButton.Size.Height + 10);
            BigPatchButton.TouchUp += (o, e) =>
            {
                if (GameScene.Game.Observer) return;
                if (null == GameScene.Game.BigPatchBox) return;
                GameScene.Game.BigPatchBox.Visible = !GameScene.Game.BigPatchBox.Visible;
                //Mir3.Droid.Activity1.MainActivity.ShowHook = true;
            };



            //ConfigButton = new DXButton
            //{
            //    Parent = this,
            //    LibraryFile = LibraryFile.PhoneUI,
            //    Index = 118,
            //};
            //ConfigButton.Location = new Point(BigPatchButton.Location.X, BigPatchButton.Location.Y + BigPatchButton.Size.Height + 10);
            //ConfigButton.TouchUp += (o, e) =>
            //{
            //    if (GameScene.Game.Observer) return;   //如果是观察者 返回
            //    GameScene.Game.ConfigBox.Visible = !GameScene.Game.ConfigBox.Visible;
            //    //GameScene.Game.ConfigBox.Location = new Point((GameScene.Game.Size.Width - GameScene.Game.ConfigBox.Size.Width) / 2, (GameScene.Game.Size.Height - GameScene.Game.ConfigBox.Size.Height) / 2);
            //};

            RateQueryButton = new DXButton //爆率查询
            {
                Parent = this,
                LibraryFile = LibraryFile.PhoneUI,
                Index = 121,
            };
            RateQueryButton.Location = new Point(BigPatchButton.Location.X, BigPatchButton.Location.Y + BigPatchButton.Size.Height + 10);
            RateQueryButton.TouchUp += (o, e) =>
            {
                    if (!CEnvir.ClientControl.RateQueryShowCheck) return;  //爆率查询设置不显示就不设置快捷
                GameScene.Game.RateQueryBox.Visible = !GameScene.Game.RateQueryBox.Visible;
                //GameScene.Game.ConfigBox.Location = new Point((GameScene.Game.Size.Width - GameScene.Game.ConfigBox.Size.Width) / 2, (GameScene.Game.Size.Height - GameScene.Game.ConfigBox.Size.Height) / 2);
            };

            FixedPointButton = new DXButton //定位
            {
                Parent = this,
                LibraryFile = LibraryFile.PhoneUI,
                Index = 129,
            };
            FixedPointButton.Location = new Point(RateQueryButton.Location.X, RateQueryButton.Location.Y + RateQueryButton.Size.Height + 10);
            FixedPointButton.TouchUp += (o, e) =>
            {
                if (!CEnvir.ClientControl.UseFixedPoint) return;  //记忆传送设置不显示就不设置快捷
                if (GameScene.Game.Observer) return;
                GameScene.Game.FixedPointBox.Visible = !GameScene.Game.FixedPointBox.Visible;
                //GameScene.Game.ConfigBox.Location = new Point((GameScene.Game.Size.Width - GameScene.Game.ConfigBox.Size.Width) / 2, (GameScene.Game.Size.Height - GameScene.Game.ConfigBox.Size.Height) / 2);
            };

            ExitButton = new DXButton   //结束游戏按钮
            {
                Parent = this,
                LibraryFile = LibraryFile.PhoneUI,
                Index = 126,
            };
            ExitButton.Location = new Point(FixedPointButton.Location.X, FixedPointButton.Location.Y + FixedPointButton.Size.Height + 10);
            ExitButton.TouchUp += (o, e) =>
            {
                //if (GameScene.Game.Observer) return;

                if (CEnvir.Now < MapObject.User.CombatTime.AddSeconds(10) && !GameScene.Game.Observer && !BigPatchConfig.ChkQuickSelect)
                {
                    GameScene.Game.ReceiveChat("战斗中无法退出游戏".Lang(), MessageType.System);
                    return;
                }

                if (BigPatchConfig.ChkQuickSelect)
                {
                    CEnvir.Enqueue(new C.Logout());
                }
                else
                {
                    GameScene.Game.ExitBox.Visible = true;
                    GameScene.Game.ExitBox.BringToFront();
                }
            };
        }

        #region IDisposable

        protected override void Dispose(bool disposing)
        {
            base.Dispose(disposing);

            if (disposing)
            {
                //if (GuildButton != null)
                //{
                //    if (!GuildButton.IsDisposed)
                //        GuildButton.Dispose();

                //    GuildButton = null;
                //}

                if (WarWeaponButton != null)
                {
                    if (!WarWeaponButton.IsDisposed)
                        WarWeaponButton.Dispose();

                    WarWeaponButton = null;
                }

                //if (RankingButton != null)
                //{
                //    if (!RankingButton.IsDisposed)
                //        RankingButton.Dispose();

                //    RankingButton = null;
                //}

                if (MarketPlace != null)
                {
                    if (!MarketPlace.IsDisposed)
                        MarketPlace.Dispose();

                    MarketPlace = null;
                }

                if (BonusPoolButton != null)
                {
                    if (!BonusPoolButton.IsDisposed)
                        BonusPoolButton.Dispose();

                    BonusPoolButton = null;
                }

                if (BigPatchButton != null)
                {
                    if (!BigPatchButton.IsDisposed)
                        BigPatchButton.Dispose();

                    BigPatchButton = null;
                }

                //if (ConfigButton != null)
                //{
                //    if (!ConfigButton.IsDisposed)
                //        ConfigButton.Dispose();

                //    ConfigButton = null;
                //}

                if (ExitButton != null)
                {
                    if (!ExitButton.IsDisposed)
                        ExitButton.Dispose();

                    ExitButton = null;
                }
            }
        }
        #endregion
    }

    /*
    public class PhoneAttackModeControl : DXControl
    {
        private DXButton Peace, Group, Guild, WarRedBrown, All;
        public PhoneAttackModeControl()
        {
            DrawTexture = false;

            Peace = new DXButton
            {
                Parent = this,
                LibraryFile = LibraryFile.PhoneUI,
                Index = 22,
                Location = new Point(0, 0),
            };
            Peace.TouchUp += (o, e) =>
            {
                if (GameScene.Game.Observer) return;
                CEnvir.Enqueue(new C.ChangeAttackMode { Mode = AttackMode.Peace });
                Visible = false;
            };

            Group = new DXButton
            {
                Parent = this,
                LibraryFile = LibraryFile.PhoneUI,
                Index = 23,
                Location = new Point(0, Peace.Location.Y + Peace.Size.Height + 5),
            };
            Group.TouchUp += (o, e) =>
            {
                if (GameScene.Game.Observer) return;
                CEnvir.Enqueue(new C.ChangeAttackMode { Mode = AttackMode.Group });
                Visible = false;
            };

            Guild = new DXButton
            {
                Parent = this,
                LibraryFile = LibraryFile.PhoneUI,
                Index = 24,
                Location = new Point(0, Group.Location.Y + Group.Size.Height + 5),
            };
            Guild.TouchUp += (o, e) =>
            {
                if (GameScene.Game.Observer) return;
                CEnvir.Enqueue(new C.ChangeAttackMode { Mode = AttackMode.Guild });
                Visible = false;
            };

            WarRedBrown = new DXButton
            {
                Parent = this,
                LibraryFile = LibraryFile.PhoneUI,
                Index = 25,
                Location = new Point(0, Guild.Location.Y + Guild.Size.Height + 5),
            };
            WarRedBrown.TouchUp += (o, e) =>
            {
                if (GameScene.Game.Observer) return;
                CEnvir.Enqueue(new C.ChangeAttackMode { Mode = AttackMode.WarRedBrown });
                Visible = false;
            };

            All = new DXButton
            {
                Parent = this,
                LibraryFile = LibraryFile.PhoneUI,
                Index = 26,
                Location = new Point(0, WarRedBrown.Location.Y + WarRedBrown.Size.Height + 5),
            };
            All.TouchUp += (o, e) =>
            {
                if (GameScene.Game.Observer) return;
                CEnvir.Enqueue(new C.ChangeAttackMode { Mode = AttackMode.All });
                Visible = false;
            };

            Size = new Size(106, All.Location.Y + All.Size.Height);
        }

        #region IDisposable

        protected override void Dispose(bool disposing)
        {
            base.Dispose(disposing);

            if (disposing)
            {
                if (Peace != null)
                {
                    if (!Peace.IsDisposed)
                        Peace.Dispose();

                    Peace = null;
                }

                if (Group != null)
                {
                    if (!Group.IsDisposed)
                        Group.Dispose();

                    Group = null;
                }

                if (Guild != null)
                {
                    if (!Guild.IsDisposed)
                        Guild.Dispose();

                    Guild = null;
                }

                if (WarRedBrown != null)
                {
                    if (!WarRedBrown.IsDisposed)
                        WarRedBrown.Dispose();

                    WarRedBrown = null;
                }

                if (All != null)
                {
                    if (!All.IsDisposed)
                        All.Dispose();

                    All = null;
                }

            }
        }
        #endregion
    }

    public class PhonePetModeControl : MonoControl
    {
        private MonoButton Both, Move, Attack, PvP, None;
        public PhonePetModeControl()
        {
            DrawTexture = false;
            ZoomRate = 1F;
            UI_Offset_X = 0;

            Both = new MonoButton
            {
                Parent = this,
                LibraryFile = LibraryFile.PhoneUI,
                Index = 28,
                Location = new Point(0, 0),
            };
            Both.TouchUp += (o, e) =>
            {
                if (GameScene.Game.Observer) return;
                CEnvir.Enqueue(new C.ChangePetMode { Mode = PetMode.Both });
                Visible = false;
            };

            Move = new MonoButton
            {
                Parent = this,
                LibraryFile = LibraryFile.PhoneUI,
                Index = 28,
                Location = new Point(0, Both.Location.Y + Both.Size.Height + 5),
            };
            Move.TouchUp += (o, e) =>
            {
                if (GameScene.Game.Observer) return;
                CEnvir.Enqueue(new C.ChangePetMode { Mode = PetMode.Move });
                Visible = false;
            };

            Attack = new MonoButton
            {
                Parent = this,
                LibraryFile = LibraryFile.PhoneUI,
                Index = 29,
                Location = new Point(0, Move.Location.Y + Move.Size.Height + 5),
            };
            Attack.TouchUp += (o, e) =>
            {
                if (GameScene.Game.Observer) return;
                CEnvir.Enqueue(new C.ChangePetMode { Mode = PetMode.Attack });
                Visible = false;
            };

            PvP = new MonoButton
            {
                Parent = this,
                LibraryFile = LibraryFile.PhoneUI,
                Index = 29,
                Location = new Point(0, Attack.Location.Y + Attack.Size.Height + 5),
            };
            PvP.TouchUp += (o, e) =>
            {
                if (GameScene.Game.Observer) return;
                CEnvir.Enqueue(new C.ChangePetMode { Mode = PetMode.PvP });
                Visible = false;
            };

            None = new MonoButton
            {
                Parent = this,
                LibraryFile = LibraryFile.PhoneUI,
                Index = 27,
                Location = new Point(0, PvP.Location.Y + PvP.Size.Height + 5),
            };
            None.TouchUp += (o, e) =>
            {
                if (GameScene.Game.Observer) return;
                CEnvir.Enqueue(new C.ChangePetMode { Mode = PetMode.None });
                Visible = false;
            };

            Size = new Size(146, None.Location.Y + None.Size.Height);
        }

        #region IDisposable

        protected override void Dispose(bool disposing)
        {
            base.Dispose(disposing);

            if (disposing)
            {
                if (Both != null)
                {
                    if (!Both.IsDisposed)
                        Both.Dispose();

                    Both = null;
                }

                if (Move != null)
                {
                    if (!Move.IsDisposed)
                        Move.Dispose();

                    Move = null;
                }

                if (Attack != null)
                {
                    if (!Attack.IsDisposed)
                        Attack.Dispose();

                    Attack = null;
                }

                if (PvP != null)
                {
                    if (!PvP.IsDisposed)
                        PvP.Dispose();

                    PvP = null;
                }

                if (None != null)
                {
                    if (!None.IsDisposed)
                        None.Dispose();

                    None = null;
                }

            }
        }
        #endregion
    }
    */
}
