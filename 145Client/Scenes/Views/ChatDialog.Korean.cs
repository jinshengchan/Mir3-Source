using Client.Controls;
using Client.Envir;
using Client.Extentions;
using Client.Models;
using Library;
using System;
using System.Drawing;
using System.Windows.Forms;

namespace Client.Scenes.Views
{
    public partial class ChatDialog
    {
        private DXControl KoreanTextBackground;
        private static readonly int[] KoreanChatHeights = { 218, 166, 118 };
        private static readonly int[] KoreanChatLineCounts = { 11, 7, 4 };
        private int KoreanChatResizeLevel = 0;

        private void BuildKoreanInterface()
        {
            Movable = false;
            DrawWindowTexture = false;
            Opacity = 0F;
            HasTitle = false;
            HasTopBorder = false;
            CloseButton.Visible = true;
            CloseButton.LibraryFile = LibraryFile.GameInter;
            CloseButton.Index = 3545;
            CloseButton.Location = new Point(364, 5);
            Border = false;
            BackColour = Color.Black;
            AllowResize = false;
            CanResizeWidth = false;
            CanResizeHeightBottom = false;
            Size = new Size(380, 268);
            History = new System.Collections.Generic.List<Message>();
            ChatLines = new System.Collections.Generic.List<DXLabel>();
            ChatItemLines = new System.Collections.Generic.List<DXLabel>();
            LineCount = 13;
            ChatFont = new Font(Config.FontName, CEnvir.FontSize(9F));
            KeyDown += ChatPanel_KeyDown;
            PassThrough = true;

            BigChatPanel = new DXImageControl
            {
                Parent = this,
                LibraryFile = LibraryFile.GameInter,
                Index = 3502,
                Size = new Size(380, 268),
                Location = Point.Empty,
                Visible = false,
                FixedSize = true,
                PassThrough = true,
            };
            BigChatPanelBackground = new DXImageControl
            {
                Parent = BigChatPanel,
                LibraryFile = LibraryFile.GameInter,
                Index = 3502,
                Size = new Size(380, 268),
                Location = Point.Empty,
                FixedSize = true,
                PassThrough = true,
            };

            ChatPanel = new DXImageControl
            {
                Parent = this,
                LibraryFile = LibraryFile.GameInter,
                Index = 3500,
                ImageOpacity = 0.7F,
                Size = new Size(380, 27),
                Location = Point.Empty,
                Visible = true,
                FixedSize = true,
                PassThrough = true,
            };

            IsAll = true;
            IsNormal = true;
            IsGroup = true;
            IsSystem = true;
            IsGuild = true;
            IsMentor = true;
            IsUnion = true;

            AllButton = CreateKoreanChatButton(4, 3511, 3510, "全部", MessageType.All);
            NormalButton = CreateKoreanChatButton(52, 3516, 3515, "一般", MessageType.Normal);
            GroupButton = CreateKoreanChatButton(100, 3521, 3520, "队伍", MessageType.Group);
            MentorButton = CreateKoreanChatButton(148, 3536, 3535, "师徒", MessageType.Mentor);
            GuildButton = CreateKoreanChatButton(196, 3526, 3525, "门派/行会", MessageType.Guild);
            SystemButton = CreateKoreanChatButton(244, 3531, 3530, "系统", MessageType.System);
            UnionButton = CreateKoreanChatButton(292, 3506, 3505, "同盟", MessageType.Union);
            UpdateKoreanChatButtonColours();

            KoreanTextBackground = new DXControl
            {
                Parent = this,
                BackColour = Color.Black,
                DrawTexture = true,
                Opacity = 0.7F,
                Size = new Size(380, 241),
                Location = new Point(0, 27),
                PassThrough = true,
            };
            KoreanTextBackground.SendToBack();

            TextPanel = new DXControl
            {
                Parent = this,
                Opacity = 0,
                Size = new Size(350, 237),
                Location = new Point(8, 31),
                PassThrough = true,
            };
            TextPanel.MouseWheel += ChatPanel_MouseWheel;

            ScrollBar = new DXVScrollBar
            {
                Parent = this,
                Size = new Size(16, 241),
                VisibleSize = 13,
                Change = 1,
                Location = new Point(360, 27),
            };
            ScrollBar.ValueChanged += (o, e) =>
            {
                StartIndex = ScrollBar.Value;
                Update();
            };
            ScrollBar.SetSkin(LibraryFile.GameInter, -1, 3561, 3562, 3560);
            ScrollBar.PositionBarOffsetX = 2;
            ScrollBar.ScrollHeightPadding = 40;
            ScrollBar.UpButton.Location = new Point(0, 2);

            Photo = new PhotoControl
            {
                Location = Point.Empty,
                Size = new Size(1, 1),
                Parent = this,
                Visible = false,
            };
            BigPatch = new DXButton { Parent = this, Visible = false };
            Upgrade = new DXImageControl { Parent = this, Visible = false };
            LevelLabel = new DXLabel { Parent = this, Visible = false, AutoSize = false, Size = new Size(1, 1) };

            CloseButton.MouseClick += (o, e) =>
            {
                KoreanChatResizeLevel = KoreanChatHeights.Length;
                HideKoreanChat();
            };

            ApplyKoreanChatSize();
        }

        public void CycleKoreanChatSize()
        {
            if (!Visible || KoreanChatResizeLevel >= KoreanChatHeights.Length)
            {
                KoreanChatResizeLevel = 0;
                Visible = true;
            }
            else
            {
                KoreanChatResizeLevel++;
                if (KoreanChatResizeLevel >= KoreanChatHeights.Length)
                {
                    HideKoreanChat();
                    return;
                }
            }

            ApplyKoreanChatSize();
        }

        private void ApplyKoreanChatSize()
        {
            int height = KoreanChatHeights[KoreanChatResizeLevel];

            Size = new Size(380, height);
            Visible = true;
            BigChatPanel.Visible = false;
            BigChatPanelBackground.Visible = false;
            ChatPanel.Visible = true;
            KoreanTextBackground.Visible = true;
            TextPanel.Visible = true;
            ScrollBar.Visible = true;

            KoreanTextBackground.Location = new Point(0, 27);
            KoreanTextBackground.Size = new Size(380, height - 27);
            TextPanel.Parent = this;
            TextPanel.Location = new Point(8, 31);
            TextPanel.Size = new Size(350, height - 31);
            ScrollBar.Parent = this;
            ScrollBar.Location = new Point(360, 27);
            ScrollBar.Size = new Size(16, height - 27);
            LineCount = KoreanChatLineCounts[KoreanChatResizeLevel];
            ScrollBar.VisibleSize = LineCount;

            if (GameScene.Game?.ChatTextBox != null)
                Location = new Point(GameScene.Game.ChatTextBox.Location.X,
                    GameScene.Game.ChatTextBox.Location.Y - height);

            CloseButton.Location = new Point(364, 5);
            CloseButton.BringToFront();
            SyncKoreanTriangle();
            Update();
        }

        private void HideKoreanChat()
        {
            Visible = false;
            BigChatPanel.Visible = false;
            BigChatPanelBackground.Visible = false;
            ChatPanel.Visible = false;
            KoreanTextBackground.Visible = false;
            TextPanel.Visible = false;
            ScrollBar.Visible = false;
            SyncKoreanTriangle();
        }

        private void SyncKoreanTriangle()
        {
            int height = Visible && KoreanChatResizeLevel < KoreanChatHeights.Length
                ? KoreanChatHeights[KoreanChatResizeLevel]
                : 0;

            DxMirButton changeButton = GameScene.Game?.ChatTextBox?.ChangeButton;
            if (changeButton == null) return;

            bool hidden = height == 0;
            changeButton.Index = hidden ? 3542 : 3552;
            changeButton.Hint = hidden
                ? "展开聊天框".Lang()
                : KoreanChatResizeLevel == KoreanChatHeights.Length - 1
                    ? "隐藏聊天框".Lang()
                    : "缩小聊天框".Lang();
        }

        private DXButton CreateKoreanChatButton(int x, int enabledIndex, int disabledIndex, string hint, MessageType type)
        {
            DXButton button = new DXButton
            {
                Parent = ChatPanel,
                LibraryFile = LibraryFile.GameInter,
                Index = enabledIndex,
                Size = new Size(48, 22),
                Location = new Point(x, 0),
                Tag = type,
                Hint = hint.Lang(),
                Label = { Visible = false },
            };
            button.MouseClick += ChatMouseClick;
            button.Tag_0 = disabledIndex;
            return button;
        }

        private void ToggleKoreanChatType(MessageType type)
        {
            switch (type)
            {
                case MessageType.All:
                    IsAll = !IsAll;
                    IsNormal = IsAll;
                    IsGuild = IsAll;
                    IsGroup = IsAll;
                    IsSystem = IsAll;
                    IsUnion = IsAll;
                    IsMentor = IsAll;
                    break;
                case MessageType.Normal:
                    IsNormal = !IsNormal;
                    break;
                case MessageType.Guild:
                    IsGuild = !IsGuild;
                    break;
                case MessageType.Group:
                    IsGroup = !IsGroup;
                    break;
                case MessageType.System:
                    IsSystem = !IsSystem;
                    break;
                case MessageType.Union:
                    IsUnion = !IsUnion;
                    break;
                case MessageType.Mentor:
                    IsMentor = !IsMentor;
                    break;
            }

            UpdateKoreanChatButtonColours();
            Update();
        }

        private void UpdateKoreanChatButtonColours()
        {
            if (AllButton == null) return;

            AllButton.Index = IsAll ? 3511 : 3510;
            NormalButton.Index = IsNormal ? 3516 : 3515;
            GroupButton.Index = IsGroup ? 3521 : 3520;
            MentorButton.Index = IsMentor ? 3536 : 3535;
            GuildButton.Index = IsGuild ? 3526 : 3525;
            SystemButton.Index = IsSystem ? 3531 : 3530;
            UnionButton.Index = IsUnion ? 3506 : 3505;
        }
    }
}
