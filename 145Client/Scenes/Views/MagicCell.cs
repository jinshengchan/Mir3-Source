using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Drawing;
using System.Reflection;
using System.Windows.Forms;
using Client.Controls;
using Client.Envir;
using Client.Extentions;
using Client.Models;
using Client.Scenes;
using Library;
using Library.Network.ClientPackets;
using Library.SystemModels;

public sealed class MagicCell : DXControl
{
    private MagicInfo _Info;

    public DXImageControl BaseImage;

    public DXImageControl Image;

    public DXImageControl ExperienceBar;

    public DXLabel NameLabel;

    public DXLabel LevelLabel;

    public DXLabel ActionLabel;

    public DXLabel KeyLabel;

    public MagicInfo Info
    {
        get
        {
            return _Info;
        }
        set
        {
            if (_Info != value)
            {
                MagicInfo oldValue = _Info;
                _Info = value;
                OnInfoChanged(oldValue, value);
            }
        }
    }


    public event EventHandler<EventArgs> InfoChanged;

    public void OnInfoChanged(MagicInfo oValue, MagicInfo nValue)
    {
        Image.Index = Info.Icon;
        NameLabel.Text = Info.Lang((MagicInfo p) => p.Name);
        Type type = nValue.Action.GetType();
        MemberInfo[] infos = type.GetMember(nValue.Action.ToString());
        DescriptionAttribute description = infos[0].GetCustomAttribute<DescriptionAttribute>();
        ActionLabel.Text = nValue.Action.Lang();
        Refresh();
        this.InfoChanged?.Invoke(this, EventArgs.Empty);
    }

    public MagicCell(MagicInfo magicInfo)
    {
        Size = new Size(368, 53);
        base.DrawTexture = true;
        base.Opacity = 0f;
        BaseImage = new DXImageControl
        {
            Parent = this,
            Index = 815,
            LibraryFile = LibraryFile.GameInter2,
            Location = new Point(4, 5)
        };
        Image = new DXImageControl
        {
            Parent = this,
            LibraryFile = LibraryFile.MagicIcon,
            Location = new Point(10, 10),
            GrayScale = true
        };
        Image.MouseClick += Image_MouseClick;
        Image.KeyDown += Image_KeyDown;
        ActionLabel = new DXLabel
        {
            Parent = this,
            Location = new Point(Size.Width - 50, 10),
            ForeColour = Color.FromArgb(137, 225, 31),
            IsControl = false
        };
        ExperienceBar = new DXImageControl
        {
            Parent = this,
            LibraryFile = LibraryFile.GameInter2,
            FixedSize = true,
            Size = new Size(0, 6),
            Location = new Point(111, 36),
            Index = 812,
            IsControl = false
        };
        NameLabel = new DXLabel
        {
            Parent = this,
            Location = new Point(65, 10),
            ForeColour = Color.FromArgb(233, 233, 225),
            IsControl = false,
            Font = new Font(Config.FontName, CEnvir.FontSize(9f), FontStyle.Bold)
        };
        KeyLabel = new DXLabel
        {
            Parent = Image,
            Font = new Font(Config.FontName, CEnvir.FontSize(10f), FontStyle.Bold),
            IsControl = false,
            ForeColour = Color.Aquamarine,
            AutoSize = false,
            Size = new Size(36, 36),
            DrawFormat = (TextFormatFlags.Bottom | TextFormatFlags.Right)
        };
        KeyLabel.SizeChanged += delegate
        {
            KeyLabel.Location = new Point(Image.Size.Width - KeyLabel.Size.Width, Image.Size.Height - KeyLabel.Size.Height);
        };
        LevelLabel = new DXLabel
        {
            Parent = this,
            ForeColour = NameLabel.ForeColour,
            Location = new Point(NameLabel.Location.X + 1, 33),
            IsControl = false,
            Font = new Font(Config.FontName, CEnvir.FontSize(9f), FontStyle.Bold)
        };
    }

    public void UpdateMagicCellBaseImage(MagicSchool school)
    {
        switch (school)
        {
            case MagicSchool.WeaponSkills:
                BaseImage.Index = 860;
                break;
            case MagicSchool.Passive:
                BaseImage.Index = 861;
                break;
            case MagicSchool.Neutral:
                BaseImage.Index = 862;
                break;
            case MagicSchool.Fire:
                BaseImage.Index = 870;
                break;
            case MagicSchool.Ice:
                BaseImage.Index = 871;
                break;
            case MagicSchool.Lightning:
                BaseImage.Index = 872;
                break;
            case MagicSchool.Wind:
                BaseImage.Index = 873;
                break;
            case MagicSchool.Holy:
                BaseImage.Index = 880;
                break;
            case MagicSchool.Dark:
                BaseImage.Index = 881;
                break;
            case MagicSchool.Phantom:
                BaseImage.Index = 882;
                break;
            case MagicSchool.Unconditional:
                BaseImage.Index = 883;
                break;
            case MagicSchool.Combat:
                BaseImage.Index = 890;
                break;
            case MagicSchool.Assassination:
                BaseImage.Index = 891;
                break;
            case MagicSchool.Assassinatie:
                BaseImage.Index = 892;
                break;
            case MagicSchool.None:
                BaseImage.Index = 883;
                break;
        }
    }

    private void Image_MouseClick(object sender, MouseEventArgs e)
    {
        if (!GameScene.Game.Observer && MapObject.User.Magics.TryGetValue(Info, out var magic))
        {
            switch (GameScene.Game.MagicBarBox.SpellSet)
            {
                case 1:
                    magic.Set1Key = SpellKey.None;
                    break;
                case 2:
                    magic.Set2Key = SpellKey.None;
                    break;
                case 3:
                    magic.Set3Key = SpellKey.None;
                    break;
                case 4:
                    magic.Set4Key = SpellKey.None;
                    break;
            }
            CEnvir.Enqueue(new MagicKey
            {
                Magic = magic.Info.Magic,
                Set1Key = magic.Set1Key,
                Set2Key = magic.Set2Key,
                Set3Key = magic.Set3Key,
                Set4Key = magic.Set4Key
            });
            Refresh();
            GameScene.Game.MagicBarBox.UpdateIcons();
        }
    }

    private void Image_KeyDown(object sender, KeyEventArgs e)
    {
        if (GameScene.Game.Observer || e.Handled || DXControl.MouseControl != Image)
        {
            return;
        }
        SpellKey key = SpellKey.None;
        using (IEnumerator<KeyBindAction> enumerator = CEnvir.GetKeyAction(e.KeyCode).GetEnumerator())
        {
            while (enumerator.MoveNext())
            {
                switch (enumerator.Current)
                {
                    case KeyBindAction.SpellUse01:
                        key = SpellKey.Spell01;
                        break;
                    case KeyBindAction.SpellUse02:
                        key = SpellKey.Spell02;
                        break;
                    case KeyBindAction.SpellUse03:
                        key = SpellKey.Spell03;
                        break;
                    case KeyBindAction.SpellUse04:
                        key = SpellKey.Spell04;
                        break;
                    case KeyBindAction.SpellUse05:
                        key = SpellKey.Spell05;
                        break;
                    case KeyBindAction.SpellUse06:
                        key = SpellKey.Spell06;
                        break;
                    case KeyBindAction.SpellUse07:
                        key = SpellKey.Spell07;
                        break;
                    case KeyBindAction.SpellUse08:
                        key = SpellKey.Spell08;
                        break;
                    case KeyBindAction.SpellUse09:
                        key = SpellKey.Spell09;
                        break;
                    case KeyBindAction.SpellUse10:
                        key = SpellKey.Spell10;
                        break;
                    case KeyBindAction.SpellUse11:
                        key = SpellKey.Spell11;
                        break;
                    case KeyBindAction.SpellUse12:
                        key = SpellKey.Spell12;
                        break;
                    default:
                        continue;
                }
                e.Handled = true;
            }
        }
        if (key == SpellKey.None || !MapObject.User.Magics.TryGetValue(Info, out var magic))
        {
            return;
        }
        switch (GameScene.Game.MagicBarBox.SpellSet)
        {
            case 1:
                magic.Set1Key = key;
                break;
            case 2:
                magic.Set2Key = key;
                break;
            case 3:
                magic.Set3Key = key;
                break;
            case 4:
                magic.Set4Key = key;
                break;
        }
        foreach (KeyValuePair<MagicInfo, ClientUserMagic> pair in MapObject.User.Magics)
        {
            if (pair.Key != magic.Info)
            {
                if (pair.Value.Set1Key == magic.Set1Key && magic.Set1Key != 0)
                {
                    pair.Value.Set1Key = SpellKey.None;
                    GameScene.Game.MagicBox.Magics[pair.Key].Refresh();
                }
                if (pair.Value.Set2Key == magic.Set2Key && magic.Set2Key != 0)
                {
                    pair.Value.Set2Key = SpellKey.None;
                    GameScene.Game.MagicBox.Magics[pair.Key].Refresh();
                }
                if (pair.Value.Set3Key == magic.Set3Key && magic.Set3Key != 0)
                {
                    pair.Value.Set3Key = SpellKey.None;
                    GameScene.Game.MagicBox.Magics[pair.Key].Refresh();
                }
                if (pair.Value.Set4Key == magic.Set4Key && magic.Set4Key != 0)
                {
                    pair.Value.Set4Key = SpellKey.None;
                    GameScene.Game.MagicBox.Magics[pair.Key].Refresh();
                }
            }
        }
        CEnvir.Enqueue(new MagicKey
        {
            Magic = magic.Info.Magic,
            Set1Key = magic.Set1Key,
            Set2Key = magic.Set2Key,
            Set3Key = magic.Set3Key,
            Set4Key = magic.Set4Key
        });
        Refresh();
        GameScene.Game.MagicBarBox.UpdateIcons();
    }

    public override void OnMouseEnter()
    {
        GameScene.Game.MouseMagic = Info;
    }

    public override void OnMouseLeave()
    {
        GameScene.Game.MouseMagic = null;
    }

    private void ExperienceBarAfterDraw(object sender, EventArgs e)
    {
        if (!MapObject.User.Magics.TryGetValue(Info, out var magic))
        {
            return;
        }
        MirImage image = ExperienceBar.Library.CreateImage(69, ImageType.Image);
        if (image == null)
        {
            return;
        }
        int x = (ExperienceBar.Size.Width - image.Width) / 2;
        int y = (ExperienceBar.Size.Height - image.Height) / 2;
        float percent = 1f;
        switch (magic.Level)
        {
            case 0:
                if (magic.Info.Experience1 == 0)
                {
                    return;
                }
                percent = (float)Math.Min(1m, Math.Max(0m, (decimal)magic.Experience / (decimal)magic.Info.Experience1));
                break;
            case 1:
                if (magic.Info.Experience2 == 0)
                {
                    return;
                }
                percent = (float)Math.Min(1m, Math.Max(0m, (decimal)magic.Experience / (decimal)magic.Info.Experience2));
                break;
            case 2:
                if (magic.Info.Experience3 == 0)
                {
                    return;
                }
                percent = (float)Math.Min(1m, Math.Max(0m, (decimal)magic.Experience / (decimal)magic.Info.Experience3));
                break;
            default:
                if (magic.Info.Experience3 == 0)
                {
                    return;
                }
                percent = (float)Math.Min(1m, Math.Max(0m, (decimal)magic.Experience / (decimal)((magic.Level - 2) * 500)));
                break;
        }
        if (percent != 0f)
        {
            DXControl.PresentTexture(image.Image, this, new Rectangle(ExperienceBar.DisplayArea.X + x, ExperienceBar.DisplayArea.Y + y, (int)((float)image.Width * percent), image.Height), Color.White, ExperienceBar);
        }
    }

    public void Refresh()
    {
        if (MapObject.User == null)
        {
            return;
        }
        float percent = 0f;
        if (MapObject.User.Magics.TryGetValue(Info, out var magic))
        {
            LevelLabel.Text = $"Lv {magic.Level}";
            ActionLabel.ForeColour = Color.FromArgb(219, 211, 85);
            NameLabel.ForeColour = Color.FromArgb(250, 240, 240);
            UpdateMagicCellBaseImage(Info.School);
            Image.GrayScale = false;
            SpellKey key = SpellKey.None;
            switch (GameScene.Game.MagicBarBox.SpellSet)
            {
                case 1:
                    key = magic.Set1Key;
                    break;
                case 2:
                    key = magic.Set2Key;
                    break;
                case 3:
                    key = magic.Set3Key;
                    break;
                case 4:
                    key = magic.Set4Key;
                    break;
            }
            Type type = typeof(SpellKey);
            MemberInfo[] infos = type.GetMember(key.ToString());
            DescriptionAttribute description = infos[0].GetCustomAttribute<DescriptionAttribute>();
            KeyLabel.Text = description?.Description;
            if (Info.NeedLevel1 <= MapObject.User.Level)
            {
                switch (magic.Level)
                {
                    case 0:
                        percent = (float)magic.Experience / (float)magic.Info.Experience1;
                        break;
                    case 1:
                        percent = (float)magic.Experience / (float)magic.Info.Experience2;
                        break;
                    case 2:
                        percent = (float)magic.Experience / (float)magic.Info.Experience3;
                        break;
                    default:
                        {
                            int exp4 = Config.SkillExpDrop;
                            percent = ((exp4 > 0) ? ((float)magic.Experience / (float)exp4) : 0f);
                            break;
                        }
                }
            }
        }
        else
        {
            LevelLabel.Text = "";
            ActionLabel.ForeColour = Color.FromArgb(132, 118, 57);
            NameLabel.ForeColour = Color.FromArgb(130, 125, 115);
            BaseImage.Index = 815;
            Image.GrayScale = true;
        }
        ExperienceBar.Size = new Size(Convert.ToInt32(248f * percent), 6);
        if (this == DXControl.MouseControl)
        {
            GameScene.Game.MouseMagic = null;
            GameScene.Game.MouseMagic = Info;
        }
    }

    protected override void Dispose(bool disposing)
    {
        base.Dispose(disposing);
        if (!disposing)
        {
            return;
        }
        _Info = null;
        this.InfoChanged = null;
        if (BaseImage != null)
        {
            if (!BaseImage.IsDisposed)
            {
                BaseImage.Dispose();
            }
            BaseImage = null;
        }
        if (Image != null)
        {
            if (!Image.IsDisposed)
            {
                Image.Dispose();
            }
            Image = null;
        }
        if (ExperienceBar != null)
        {
            if (!ExperienceBar.IsDisposed)
            {
                ExperienceBar.Dispose();
            }
            ExperienceBar = null;
        }
        if (NameLabel != null)
        {
            if (!NameLabel.IsDisposed)
            {
                NameLabel.Dispose();
            }
            NameLabel = null;
        }
        if (LevelLabel != null)
        {
            if (!LevelLabel.IsDisposed)
            {
                LevelLabel.Dispose();
            }
            LevelLabel = null;
        }
        if (ActionLabel != null)
        {
            if (!ActionLabel.IsDisposed)
            {
                ActionLabel.Dispose();
            }
            ActionLabel = null;
        }
        if (KeyLabel != null)
        {
            if (!KeyLabel.IsDisposed)
            {
                KeyLabel.Dispose();
            }
            KeyLabel = null;
        }
    }
}
