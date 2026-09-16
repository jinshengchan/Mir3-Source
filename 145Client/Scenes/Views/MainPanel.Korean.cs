using Client.Controls;
using Client.Envir;
using Client.Extentions;
using Client.Models;
using Client.Scenes.Configs;
using Client.UserModels;
using Library;
using System;
using System.Drawing;
using System.Windows.Forms;
using C = Library.Network.ClientPackets;

namespace Client.Scenes.Views
{
    public sealed partial class MainPanel
    {
        private void BuildKoreanInterface()
        {
            DrawImage = false;
            PassThrough = true;
            Size = new Size(Math.Min(1024, GameScene.Game.Size.Width), 68);

            _ = new DXImageControl
            {
                Parent = this,
                LibraryFile = LibraryFile.GameInter,
                Index = 50,
                Size = new Size(1024, 68),
                Location = Point.Empty,
                PassThrough = true,
            };

            CreateKoreanImage(60, new Point(276, 20));
            CreateKoreanImage(61, new Point(276, 40));
            CreateKoreanImage(62, new Point(360, 20));
            CreateKoreanImage(63, new Point(360, 40));
            CreateKoreanImage(64, new Point(447, 20));
            CreateKoreanImage(65, new Point(447, 40));
            CreateKoreanImage(66, new Point(536, 40));

            ExperienceBar = new DXImageControl
            {
                Parent = this,
                LibraryFile = LibraryFile.GameInter,
                Index = 51,
                Location = new Point((Size.Width - 992) / 2 + 1, 3),
                Size = new Size(992, 10),
                PassThrough = false,
            };
            ExperienceBar.BeforeDraw += (o, e) =>
            {
                if (MapObject.User == null) return;
                DrawKoreanExperience();
            };

            HealthBar = new DXControl
            {
                Parent = this,
                Location = new Point(35, 22),
                Size = new Size(220, 8),
                PassThrough = true,
            };
            HealthBar.BeforeDraw += (o, e) =>
            {
                if (MapObject.User == null) return;
                DrawKoreanBar(HealthBar, 52, MapObject.User.CurrentHP, MapObject.User.Stats[Stat.Health]);
            };

            ManaBar = new DXControl
            {
                Parent = this,
                Location = new Point(35, 36),
                Size = new Size(220, 8),
                PassThrough = true,
            };
            ManaBar.BeforeDraw += (o, e) =>
            {
                if (MapObject.User == null) return;
                DrawKoreanBar(ManaBar, 54, MapObject.User.CurrentMP, MapObject.User.Stats[Stat.Mana]);
            };

            BagWeightBar = new DXControl
            {
                Parent = this,
                Location = Point.Empty,
                Size = Size.Empty,
                Visible = false,
                PassThrough = true,
            };

            HealthLabel = CreateKoreanLabel(new Point(35, 18), new Size(220, 16));
            ManaLabel = CreateKoreanLabel(new Point(35, 32), new Size(220, 16));
            ExperienceLabel = CreateKoreanLabel(Point.Empty, Size.Empty, false);
            WeightLabel = CreateKoreanLabel(Point.Empty, Size.Empty, false);
            GridLabel = CreateKoreanLabel(Point.Empty, Size.Empty, false);

            ClassLabel = CreateKoreanLabel(new Point(299, 20), new Size(61, 16));
            LevelLabel = CreateKoreanLabel(new Point(299, 40), new Size(61, 16));
            DXLabel koreanFPLabel = CreateKoreanLabel(new Point(383, 20), new Size(62, 16));
            DXLabel koreanCPLabel = CreateKoreanLabel(new Point(383, 40), new Size(62, 16));
            koreanFPLabel.Text = string.Empty;
            koreanCPLabel.Text = string.Empty;

            DCLabel = CreateKoreanLabel(new Point(469, 20), new Size(62, 16));
            ACLabel = CreateKoreanLabel(new Point(469, 40), new Size(62, 16));
            MCLabel = CreateKoreanLabel(new Point(568, 40), new Size(62, 16));
            MRLabel = CreateKoreanLabel(Point.Empty, Size.Empty, false);
            SCLabel = CreateKoreanLabel(Point.Empty, Size.Empty, false);

            AClabel = CreateKoreanImage(Point.Empty, false);
            MRlabel = CreateKoreanImage(Point.Empty, false);
            DClabel = CreateKoreanImage(Point.Empty, false);
            MClabel = CreateKoreanImage(Point.Empty, false);
            SClabel = CreateKoreanImage(Point.Empty, false);

            AttackModeLabel = CreateKoreanLabel(new Point(35, 46), new Size(115, 16));
            AttackModeLabel.ForeColour = Color.Cyan;
            PetModeLabel = CreateKoreanLabel(new Point(150, 46), new Size(105, 16));
            PetModeLabel.ForeColour = Color.Cyan;

            DXButton characterButton = CreateKoreanIconButton(82, new Rectangle(650, 23, 36, 34), "角色窗口".Lang(), (o, e) =>
                GameScene.Game.CharacterBox.Visible = !GameScene.Game.CharacterBox.Visible);
            DXButton inventoryButton = CreateKoreanIconButton(87, new Rectangle(689, 23, 36, 34), "包裹窗口".Lang(), (o, e) =>
                GameScene.Game.InventoryBox.Visible = !GameScene.Game.InventoryBox.Visible);
            DXButton magicButton = CreateKoreanIconButton(92, new Rectangle(728, 23, 36, 34), "魔法窗口".Lang(), (o, e) =>
            {
                if (GameScene.Game.Observer) return;
                GameScene.Game.MagicBox.Visible = !GameScene.Game.MagicBox.Visible;
            });
            DXButton questButton = CreateKoreanIconButton(112, new Rectangle(767, 23, 36, 34), "任务窗口".Lang(), (o, e) =>
            {
                if (GameScene.Game.Observer) return;
                GameScene.Game.QuestBox.Visible = !GameScene.Game.QuestBox.Visible;
            });
            DXButton mailButton = CreateKoreanIconButton(97, new Rectangle(806, 23, 36, 34), "邮件窗口".Lang(), (o, e) =>
            {
                if (GameScene.Game.Observer) return;
                GameScene.Game.CommunicationBox.Visible = !GameScene.Game.CommunicationBox.Visible;
            });
            DXButton beltButton = CreateKoreanIconButton(107, new Rectangle(845, 23, 36, 34), "物品快捷栏".Lang(), (o, e) =>
                GameScene.Game.BeltBox.Visible = !GameScene.Game.BeltBox.Visible);
            DXButton guildButton = CreateKoreanIconButton(102, new Rectangle(884, 23, 36, 34), "行会".Lang(), (o, e) =>
            {
                if (GameScene.Game.Observer) return;
                GameScene.Game.GuildBox.Visible = !GameScene.Game.GuildBox.Visible;
            });
            DXButton menuButton = CreateKoreanIconButton(117, new Rectangle(923, 23, 36, 34), "主菜单".Lang(), (o, e) =>
            {
                if (GameScene.Game.KoreanMenuBox != null)
                    GameScene.Game.KoreanMenuBox.Visible = !GameScene.Game.KoreanMenuBox.Visible;
            });
            DXButton shopButton = CreateKoreanIconButton(122, new Rectangle(972, 16, 48, 48), "商城".Lang(), (o, e) =>
            {
                if (GameScene.Game.Observer) return;

                if (GameScene.Game.MarketPlaceBox.TabControl.IsVisible)
                    GameScene.Game.MarketPlaceBox.Visible = false;
                else
                {
                    GameScene.Game.MarketPlaceBox.Visible = true;
                    GameScene.Game.MarketPlaceBox.TabControl.Visible = true;
                }
            });

            NewMailIcon = new DXImageControl
            {
                Parent = mailButton,
                LibraryFile = LibraryFile.GameInter,
                Index = 240,
                IsControl = false,
                Location = new Point(2, 2),
                Visible = false,
            };
            AvailableQuestIcon = new DXImageControl
            {
                Parent = questButton,
                LibraryFile = LibraryFile.GameInter,
                Index = 240,
                IsControl = false,
                Location = new Point(2, 2),
                Visible = false,
            };
            CompletedQuestIcon = new DXImageControl
            {
                Parent = questButton,
                LibraryFile = LibraryFile.GameInter,
                Index = 241,
                IsControl = false,
                Location = new Point(2, 2),
                Visible = false,
            };
            AvailableQuestIcon.VisibleChanged += (o, e) =>
            {
                CompletedQuestIcon.Location = AvailableQuestIcon.Visible
                    ? new Point(questButton.Size.Width - CompletedQuestIcon.Size.Width, questButton.Size.Height - CompletedQuestIcon.Size.Height)
                    : new Point(2, 2);
            };
        }

        private DXLabel CreateKoreanLabel(Point location, Size size, bool visible = true)
        {
            return new DXLabel
            {
                Parent = this,
                Location = location,
                Size = size,
                AutoSize = false,
                Visible = visible,
                ForeColour = Color.White,
                Outline = true,
                OutlineColour = Color.Black,
                DrawFormat = TextFormatFlags.VerticalCenter | TextFormatFlags.HorizontalCenter,
            };
        }

        private void DrawKoreanExperience()
        {
            if (!CEnvir.LibraryList.TryGetValue(LibraryFile.GameInter, out MirLibrary library)) return;
            if (MapObject.User.MaxExperience <= 0M) return;

            MirImage image = library.CreateImage(56, ImageType.Image);
            if (image == null) return;

            decimal percent = Math.Min(1M, Math.Max(0M, MapObject.User.Experience / MapObject.User.MaxExperience));
            if (percent <= 0M) return;

            int x = (ExperienceBar.Size.Width - image.Width) / 2;
            int y = (ExperienceBar.Size.Height - image.Height) / 2;
            PresentTexture(image.Image, this, new Rectangle(ExperienceBar.DisplayArea.X + x, ExperienceBar.DisplayArea.Y + y - 1, (int)(image.Width * percent), image.Height), Color.White, ExperienceBar);
        }

        private void DrawKoreanBar(DXControl control, int index, decimal current, decimal maximum)
        {
            if (maximum <= 0M || current <= 0M) return;
            if (!CEnvir.LibraryList.TryGetValue(LibraryFile.GameInter, out MirLibrary library)) return;

            MirImage image = library.CreateImage(index, ImageType.Image);
            if (image == null) return;

            decimal percent = Math.Min(1M, Math.Max(0M, current / maximum));
            if (percent <= 0M) return;

            PresentTexture(image.Image, this, new Rectangle(control.DisplayArea.X, control.DisplayArea.Y, (int)(image.Width * percent), image.Height), Color.White, control);
        }

        private DXImageControl CreateKoreanImage(int index, Point location)
        {
            return new DXImageControl
            {
                Parent = this,
                LibraryFile = LibraryFile.GameInter,
                Index = index,
                Location = location,
                IsControl = false,
                PassThrough = true,
            };
        }

        private DXImageControl CreateKoreanImage(Point location, bool visible)
        {
            return new DXImageControl
            {
                Parent = this,
                Location = location,
                Visible = visible,
            };
        }

        private DXButton CreateKoreanIconButton(int index, Rectangle bounds, string hint, EventHandler<MouseEventArgs> click)
        {
            DXButton button = new DXButton
            {
                Parent = this,
                LibraryFile = LibraryFile.GameInter,
                Index = index,
                Location = bounds.Location,
                Size = bounds.Size,
                Hint = hint,
                Label = { Visible = false },
            };
            button.MouseClick += click;
            return button;
        }

        private void ShowExitDialog()
        {
            if (CEnvir.Now < MapObject.User.CombatTime.AddSeconds(10) && !GameScene.Game.Observer && !BigPatchConfig.ChkQuickSelect)
            {
                GameScene.Game.ReceiveChat("战斗中无法退出游戏".Lang(), MessageType.System);
                return;
            }

            if (BigPatchConfig.ChkQuickSelect)
            {
                CEnvir.Enqueue(new C.Logout());
                return;
            }

            GameScene.Game.ExitBox.Visible = true;
            GameScene.Game.ExitBox.BringToFront();
        }

        public sealed class MenuDialog : DXWindow
        {
            public override WindowType Type => WindowType.None;
            public override bool CustomSize => true;
            public override bool AutomaticVisibility => false;

            public MenuDialog()
            {
                HasTitle = false;
                HasTopBorder = false;
                HasFooter = false;
                Size = new Size(150, 240);
                Movable = false;
                Visible = false;
                CloseButton.LibraryFile = LibraryFile.GameInter;
                CloseButton.Index = 3545;
                CloseButton.Location = new Point(128, 4);
                CloseButton.BringToFront();

                DXLabel titleLabel = new DXLabel
                {
                    Parent = this,
                    Text = "主菜单".Lang(),
                    Location = new Point(25, 4),
                    Size = new Size(100, 20),
                    AutoSize = false,
                    ForeColour = Color.FromArgb(198, 166, 99),
                    Outline = true,
                    OutlineColour = Color.Black,
                    DrawFormat = TextFormatFlags.HorizontalCenter | TextFormatFlags.VerticalCenter,
                };

                CreateMenuButton(30, "环境设置", (o, e) => GameScene.Game.ConfigBox.Visible = !GameScene.Game.ConfigBox.Visible);
                CreateMenuButton(59, "队伍信息", (o, e) => GameScene.Game.GroupBox.Visible = !GameScene.Game.GroupBox.Visible);
                CreateMenuButton(88, "掉落查询", (o, e) =>
                {
                    if (CEnvir.ClientControl.RateQueryShowCheck)
                        GameScene.Game.RateQueryBox.Visible = !GameScene.Game.RateQueryBox.Visible;
                });
                CreateMenuButton(117, "玛法排行榜", (o, e) =>
                {
                    if (!GameScene.Game.Observer)
                        GameScene.Game.RankingBox.Visible = !GameScene.Game.RankingBox.Visible && CEnvir.Connection != null;
                });
                CreateMenuButton(146, "宠物状态", (o, e) => GameScene.Game.CompanionBox.Visible = !GameScene.Game.CompanionBox.Visible);
                CreateMenuButton(175, "辅助设置", (o, e) =>
                {
                    if (GameScene.Game.Observer || GameScene.Game.BigPatchBox == null) return;
                    GameScene.Game.BigPatchBox.Visible = !GameScene.Game.BigPatchBox.Visible;
                });
                CreateMenuButton(204, "结束游戏", (o, e) => GameScene.Game.MainPanel.ShowExitDialog());
            }

            private DXButton CreateMenuButton(int y, string hint, EventHandler<MouseEventArgs> click)
            {
                string text = hint.Lang();
                DXButton button = new DXButton
                {
                    Parent = this,
                    ButtonType = ButtonType.Default,
                    Location = new Point(25, y),
                    Size = new Size(100, 26),
                    Hint = text,
                    Label =
                    {
                        Visible = true,
                        Text = text,
                        ForeColour = Color.FromArgb(198, 166, 99),
                        Outline = true,
                        OutlineColour = Color.Black,
                        DrawFormat = TextFormatFlags.HorizontalCenter | TextFormatFlags.VerticalCenter,
                    },
                };
                button.MouseClick += click;
                return button;
            }
        }
    }
}
