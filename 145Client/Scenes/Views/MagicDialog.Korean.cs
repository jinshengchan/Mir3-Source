using Client.Controls;
using Client.Envir;
using Client.Extentions;
using Client.Models;
using Library;
using Library.SystemModels;
using System;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;
using System.Windows.Forms;

namespace Client.Scenes.Views
{
    public sealed partial class MagicDialog
    {
        private const int KoreanWindowWidth = 423;
        private const int KoreanWindowHeight = 518;
        private const int KoreanListTop = 76;
        private const int KoreanListLeft = 14;
        private const int KoreanListWidth = 382;
        private const int KoreanListHeight = 410;
        private const int KoreanRowHeight = 56;
        private const int KoreanRowGap = 4;

        private bool KoreanLayout;
        private MirClass? KoreanBuiltClass;
        private MagicSchool? KoreanSelectedSchool;
        private DXControl KoreanListArea;
        private DXVScrollBar KoreanScrollBar;
        private DXImageControl KoreanHeader;
        private DXImageControl KoreanBody;
        private readonly Dictionary<MagicSchool, DXButton> KoreanSchoolButtons = new Dictionary<MagicSchool, DXButton>();
        private readonly Dictionary<MagicInfo, KoreanMagicRow> KoreanRows = new Dictionary<MagicInfo, KoreanMagicRow>();

        private void BuildKoreanInterface()
        {
            KoreanLayout = true;
            HasTitle = false;
            HasFooter = false;
            HasTopBorder = false;
            DrawWindowTexture = false;
            DrawTexture = false;
            TitleLabel.Visible = false;
            CloseButton.Hint = "关闭".Lang();
            Size = new Size(KoreanWindowWidth, KoreanWindowHeight);
            BackColour = Color.Empty;

            KoreanHeader = new DXImageControl
            {
                Parent = this,
                LibraryFile = LibraryFile.GameInter2,
                Index = -1,
                Location = Point.Empty,
                IsControl = false,
                PassThrough = true,
            };

            KoreanBody = new DXImageControl
            {
                Parent = this,
                LibraryFile = LibraryFile.GameInter2,
                Index = 810,
                Location = new Point(0, 66),
                IsControl = false,
                PassThrough = true,
            };

            KoreanListArea = new DXControl
            {
                Parent = this,
                Location = new Point(KoreanListLeft, KoreanListTop),
                Size = new Size(KoreanListWidth, KoreanListHeight),
                DrawTexture = false,
                BackColour = Color.Empty,
                Border = false,
                IsControl = true,
            };

            KoreanScrollBar = new DXVScrollBar
            {
                Parent = this,
                Location = new Point(397, KoreanListTop),
                Size = new Size(18, KoreanListHeight),
                Change = 60,
                VisibleSize = KoreanListHeight,
            };
            KoreanScrollBar.SetSkin(LibraryFile.UI1, -1, -1, -1, 1225);
            KoreanScrollBar.ValueChanged += KoreanScrollBar_ValueChanged;
            KoreanListArea.MouseWheel += KoreanScrollBar.DoMouseWheel;
            MouseWheel += KoreanScrollBar.DoMouseWheel;
            VisibleChanged += KoreanVisibleChanged;

            CloseButton.Location = new Point(392, 5);
            CloseButton.BringToFront();
        }

        public void InitializeForUser()
        {
            if (!KoreanLayout) return;
            EnsureKoreanMagicList();
            RefreshKoreanMagicRows();
        }

        private void KoreanVisibleChanged(object sender, EventArgs e)
        {
            if (!Visible) return;
            EnsureKoreanMagicList();
            RefreshKoreanMagicRows();
        }

        private void KoreanScrollBar_ValueChanged(object sender, EventArgs e)
        {
            UpdateKoreanRowLocations();
        }

        private void EnsureKoreanMagicList()
        {
            if (!KoreanLayout || MapObject.User == null) return;
            if (KoreanBuiltClass.HasValue && KoreanBuiltClass.Value == MapObject.User.Class) return;

            ClearKoreanEntries();

            List<IGrouping<MagicSchool, MagicInfo>> groups = Globals.MagicInfoList.Binding
                .Where(p => p.Class == MapObject.User.Class && p.School != MagicSchool.None && p.School != MagicSchool.InternalSkill)
                .GroupBy(p => p.School)
                .OrderBy(p => KoreanSchoolOrder(MapObject.User.Class, p.Key))
                .ThenBy(p => (int)p.Key)
                .ToList();

            KoreanBuiltClass = MapObject.User.Class;
            KoreanHeader.Index = KoreanClassEmblemIndex(MapObject.User.Class);

            foreach (IGrouping<MagicSchool, MagicInfo> group in groups)
            {
                DXButton button = new DXButton
                {
                    Parent = this,
                    Index = -1,
                    DrawImage = false,
                    FixedSize = true,
                    Size = new Size(60, 22),
                    Tag = group.Key,
                    Hint = KoreanSchoolHint(group.Key),
                };
                button.Label.Visible = false;
                button.MouseClick += KoreanSchool_Click;
                KoreanSchoolButtons[group.Key] = button;

                int rowIndex = 0;
                foreach (MagicInfo info in group.OrderBy(p => p.NeedLevel1).ThenBy(p => p.Name))
                {
                    KoreanMagicRow row = new KoreanMagicRow(info, group.Key, rowIndex++, KoreanScrollBar)
                    {
                        Parent = this,
                    };
                    KoreanRows[info] = row;
                    Magics[info] = row.MagicCell;
                }
            }

            int x = 53;
            foreach (IGrouping<MagicSchool, MagicInfo> group in groups)
            {
                DXButton button = KoreanSchoolButtons[group.Key];
                button.Location = new Point(x, 40);
                x += 60;
            }
            CloseButton.BringToFront();

            MagicSchool? selectedSchool = KoreanSelectedSchool;
            if (!selectedSchool.HasValue || !KoreanSchoolButtons.ContainsKey(selectedSchool.Value))
                selectedSchool = KoreanSchoolButtons.Keys.FirstOrDefault();

            if (KoreanSchoolButtons.Count == 0)
            {
                KoreanSelectedSchool = null;
                KoreanScrollBar.MaxValue = 0;
                KoreanScrollBar.Value = 0;
            }
            else
            {
                SelectKoreanSchool(selectedSchool.Value);
            }
        }

        private void KoreanSchool_Click(object sender, MouseEventArgs e)
        {
            DXButton button = sender as DXButton;
            if (button?.Tag is MagicSchool school)
                SelectKoreanSchool(school);
        }

        private void SelectKoreanSchool(MagicSchool school)
        {
            if (!KoreanSchoolButtons.ContainsKey(school)) return;

            KoreanSelectedSchool = school;
            foreach (KeyValuePair<MagicSchool, DXButton> pair in KoreanSchoolButtons)
                pair.Value.Pressed = pair.Key == school;

            KoreanScrollBar.Value = 0;
            UpdateKoreanRowLocations();
        }

        private void RefreshKoreanMagicRows()
        {
            if (!KoreanLayout || MapObject.User == null) return;
            EnsureKoreanMagicList();

            foreach (KoreanMagicRow row in KoreanRows.Values)
                row.Refresh();

            UpdateKoreanRowLocations();
        }

        private void UpdateKoreanRowLocations()
        {
            if (!KoreanLayout || KoreanScrollBar == null) return;

            List<KoreanMagicRow> rows = KoreanSelectedSchool.HasValue
                ? KoreanRows.Values.Where(p => p.School == KoreanSelectedSchool.Value).OrderBy(p => p.Index).ToList()
                : new List<KoreanMagicRow>();

            KoreanScrollBar.VisibleSize = KoreanListHeight;
            KoreanScrollBar.MaxValue = rows.Count * (KoreanRowHeight + KoreanRowGap);

            foreach (KoreanMagicRow row in KoreanRows.Values)
            {
                if (!KoreanSelectedSchool.HasValue || row.School != KoreanSelectedSchool.Value)
                {
                    row.Visible = false;
                    continue;
                }

                int y = KoreanListTop + row.Index * (KoreanRowHeight + KoreanRowGap) - KoreanScrollBar.Value;
                row.Location = new Point(KoreanListLeft, y);
                row.Visible = y < KoreanListTop + KoreanListHeight && y + row.Size.Height > KoreanListTop;
            }
        }

        private static int KoreanSchoolOrder(MirClass characterClass, MagicSchool school)
        {
            MagicSchool[] preferred = KoreanPreferredSchools(characterClass);
            int index = Array.IndexOf(preferred, school);
            return index < 0 ? int.MaxValue : index;
        }

        private static MagicSchool[] KoreanPreferredSchools(MirClass characterClass)
        {
            switch (characterClass)
            {
                case MirClass.Warrior:
                    return new[] { MagicSchool.WeaponSkills, MagicSchool.Passive, MagicSchool.Neutral };
                case MirClass.Wizard:
                    return new[] { MagicSchool.Fire, MagicSchool.Ice, MagicSchool.Lightning, MagicSchool.Wind };
                case MirClass.Taoist:
                    return new[] { MagicSchool.Holy, MagicSchool.Dark, MagicSchool.Phantom };
                case MirClass.Assassin:
                    return new[] { MagicSchool.Combat, MagicSchool.Assassination, MagicSchool.Assassinatie };
                default:
                    return new MagicSchool[0];
            }
        }

        private static int KoreanClassEmblemIndex(MirClass characterClass)
        {
            switch (characterClass)
            {
                case MirClass.Warrior: return 800;
                case MirClass.Wizard: return 801;
                case MirClass.Taoist: return 802;
                case MirClass.Assassin: return 803;
                default: return -1;
            }
        }

        private static string KoreanSchoolHint(MagicSchool school)
        {
            switch (school)
            {
                case MagicSchool.WeaponSkills: return "武技".Lang();
                case MagicSchool.Fire: return "火".Lang();
                case MagicSchool.Ice: return "冰".Lang();
                case MagicSchool.Lightning: return "雷".Lang();
                case MagicSchool.Wind: return "风".Lang();
                case MagicSchool.Holy: return "神圣".Lang();
                case MagicSchool.Dark: return "暗黑".Lang();
                case MagicSchool.Phantom: return "幻影".Lang();
                case MagicSchool.Combat: return "格斗".Lang();
                case MagicSchool.Assassination: return "刺杀".Lang();
                case MagicSchool.Assassinatie: return "暗杀".Lang();
                default: return school.Lang();
            }
        }

        private void ClearKoreanEntries()
        {
            foreach (KoreanMagicRow row in KoreanRows.Values.ToList())
            {
                if (!row.IsDisposed)
                    row.Dispose();
            }
            foreach (DXButton button in KoreanSchoolButtons.Values.ToList())
            {
                if (!button.IsDisposed)
                    button.Dispose();
            }

            KoreanRows.Clear();
            KoreanSchoolButtons.Clear();
            KoreanSelectedSchool = null;
            if (Magics != null)
                Magics.Clear();
        }

        private void DisposeKoreanInterface()
        {
            VisibleChanged -= KoreanVisibleChanged;
            if (KoreanScrollBar != null)
            {
                MouseWheel -= KoreanScrollBar.DoMouseWheel;
                KoreanScrollBar.ValueChanged -= KoreanScrollBar_ValueChanged;
            }

            ClearKoreanEntries();
            if (KoreanHeader != null && !KoreanHeader.IsDisposed)
                KoreanHeader.Dispose();
            if (KoreanBody != null && !KoreanBody.IsDisposed)
                KoreanBody.Dispose();
            KoreanListArea = null;
            KoreanScrollBar = null;
            KoreanHeader = null;
            KoreanBody = null;
            KoreanBuiltClass = null;
            KoreanSelectedSchool = null;
            KoreanLayout = false;
        }

        private sealed class KoreanMagicRow : DXControl
        {
            public readonly MagicInfo Info;
            public readonly MagicSchool School;
            public readonly int Index;
            public readonly MagicCell MagicCell;
            public readonly DXLabel NameLabel;
            public readonly DXLabel StatusLabel;
            public readonly DXControl ProgressBackground;
            public readonly DXControl ProgressFill;

            public KoreanMagicRow(MagicInfo info, MagicSchool school, int index, DXVScrollBar scrollBar)
            {
                Info = info;
                School = school;
                Index = index;
                Size = new Size(KoreanListWidth, KoreanRowHeight);
                DrawTexture = true;
                BackColour = Color.FromArgb(45, 30, 20);
                Border = true;
                BorderColour = Color.FromArgb(95, 70, 40);

                MagicCell = new MagicCell
                {
                    Parent = this,
                    Info = info,
                    ShowUnlearnedIcon = true,
                    Location = new Point(4, -1),
                };
                MagicCell.Image.LibraryFile = LibraryFile.MagicIcon;
                ApplyKoreanIconFallback();

                NameLabel = new DXLabel
                {
                    Parent = this,
                    Location = new Point(70, 7),
                    Size = new Size(180, 20),
                    AutoSize = false,
                    IsControl = false,
                    Text = info.Lang(p => p.Name),
                    ForeColour = Color.FromArgb(198, 166, 99),
                    Font = new Font(Config.FontName, CEnvir.FontSize(9F), FontStyle.Bold),
                };

                StatusLabel = new DXLabel
                {
                    Parent = this,
                    Location = new Point(250, 7),
                    Size = new Size(125, 20),
                    AutoSize = false,
                    IsControl = false,
                    DrawFormat = TextFormatFlags.Right | TextFormatFlags.VerticalCenter,
                    ForeColour = Color.Red,
                    Font = new Font(Config.FontName, CEnvir.FontSize(9F)),
                };

                ProgressBackground = new DXControl
                {
                    Parent = this,
                    Location = new Point(70, 35),
                    Size = new Size(300, 8),
                    DrawTexture = true,
                    BackColour = Color.FromArgb(20, 15, 12),
                    Border = true,
                    BorderColour = Color.FromArgb(95, 70, 40),
                    PassThrough = true,
                };

                ProgressFill = new DXControl
                {
                    Parent = ProgressBackground,
                    Location = Point.Empty,
                    Size = new Size(0, 8),
                    DrawTexture = true,
                    BackColour = Color.FromArgb(198, 166, 99),
                    PassThrough = true,
                };

                MouseWheel += scrollBar.DoMouseWheel;
                MagicCell.MouseWheel += scrollBar.DoMouseWheel;
                MagicCell.Image.MouseWheel += scrollBar.DoMouseWheel;
                NameLabel.MouseWheel += scrollBar.DoMouseWheel;
                StatusLabel.MouseWheel += scrollBar.DoMouseWheel;
                ProgressBackground.MouseWheel += scrollBar.DoMouseWheel;
                ProgressFill.MouseWheel += scrollBar.DoMouseWheel;
            }

            private void ApplyKoreanIconFallback()
            {
                if (Info.Magic == MagicType.AugmentEvilSlayer)
                    MagicCell.Image.Index = 524;
            }

            public void Refresh()
            {
                if (MapObject.User == null) return;

                if (!MapObject.User.Magics.TryGetValue(Info, out ClientUserMagic magic))
                {
                    StatusLabel.Text = $"要求等级: {Info.NeedLevel1}";
                    StatusLabel.ForeColour = Color.Red;
                    ProgressFill.Size = new Size(0, ProgressFill.Size.Height);
                    MagicCell.Refresh();
                    ApplyKoreanIconFallback();
                    return;
                }

                StatusLabel.Text = $"技能等级: {magic.Level}";
                StatusLabel.ForeColour = Color.FromArgb(198, 166, 99);
                int required = magic.Level == 0 ? Info.Experience1 :
                               magic.Level == 1 ? Info.Experience2 :
                               magic.Level == 2 ? Info.Experience3 : 0;
                double ratio = required <= 0 ? 1D : Math.Min(1D, Math.Max(0D, magic.Experience / (double)required));
                ProgressFill.Size = new Size((int)(300 * ratio), ProgressFill.Size.Height);
                MagicCell.Refresh();
                ApplyKoreanIconFallback();
            }
        }
    }
}
