using System.Drawing;
using System.Linq;
using System.Windows.Forms;
using Client.Controls;
using Client.Extentions;
using Client.Scenes.Views;
using Library;

public sealed class MagicTab : DXTab
{
    public DXMirScrollBar ScrollBar;

    public override void OnSizeChanged(Size oValue, Size nValue)
    {
        base.OnSizeChanged(oValue, nValue);
        base.Location = new Point(0, 23);
        ScrollBar.Size = new Size(16, Size.Height - 62);
        ScrollBar.Location = new Point(Size.Width - 30, 3);
        int height = 7;
        DXControl content = base.Controls.FirstOrDefault((DXControl p) => p.Tag?.ToString() == "content");
        if (content != null)
        {
            foreach (DXControl control in content.Controls)
            {
                if (control is MagicCell)
                {
                    height += control.Size.Height + 6;
                }
            }
        }
        ScrollBar.Change = 59;
        ScrollBar.MaxValue = height + 7;
        ScrollBar.VisibleSize = ScrollBar.Size.Height;
        UpdateLocations();
    }

    public MagicTab(MagicSchool school)
    {
        base.TabButton.LibraryFile = LibraryFile.Interface;
        base.TabButton.Opacity = 0f;
        base.TabButton.Hint = school.ToString();
        base.Border = false;
        base.Opacity = 0f;

        switch (school)
        {
            case MagicSchool.WeaponSkills:
                base.TabButton.Index = 53;
                base.TabButton.Hint = "武技".Lang();
                break;
            case MagicSchool.Passive:
                base.TabButton.Index = 54;
                base.TabButton.Hint = "被动".Lang();
                break;
            case MagicSchool.Neutral:
                base.TabButton.Index = 55;
                base.TabButton.Hint = "转换".Lang();
                break;
            case MagicSchool.Fire:
                base.TabButton.Index = 56;
                base.TabButton.Hint = "火".Lang();
                break;
            case MagicSchool.Ice:
                base.TabButton.Index = 57;
                base.TabButton.Hint = "冰".Lang();
                break;
            case MagicSchool.Lightning:
                base.TabButton.Index = 58;
                base.TabButton.Hint = "雷".Lang();
                break;
            case MagicSchool.Wind:
                base.TabButton.Index = 59;
                base.TabButton.Hint = "风".Lang();
                break;
            case MagicSchool.Holy:
                base.TabButton.Index = 61;
                base.TabButton.Hint = "神圣".Lang();
                break;
            case MagicSchool.Dark:
                base.TabButton.Index = 62;
                base.TabButton.Hint = "暗黑".Lang();
                break;
            case MagicSchool.Phantom:
                base.TabButton.Index = 60;
                base.TabButton.Hint = "幻影".Lang();
                break;
            case MagicSchool.Unconditional:
                base.TabButton.Index = 64;
                base.TabButton.Hint = "无条件".Lang();
                break;
            case MagicSchool.Combat:
                base.TabButton.Index = 65;
                base.TabButton.Hint = "格斗".Lang();
                break;
            case MagicSchool.Assassination:
                base.TabButton.Index = 66;
                base.TabButton.Hint = "刺杀".Lang();
                break;
            case MagicSchool.Assassinatie:
                base.TabButton.Index = 67;
                base.TabButton.Hint = "暗杀".Lang();
                break;
            case MagicSchool.None:
                base.TabButton.Index = 64;
                base.TabButton.Hint = "空置".Lang();
                break;
        }
        ScrollBar = new DXMirScrollBar
        {
            Parent = this
        };
        ScrollBar.ValueChanged += delegate
        {
            UpdateLocations();
        };
    }

    public void UpdateLocations()
    {
        int y = -(ScrollBar.Value - ScrollBar.Value % ScrollBar.Change) + 7;
        DXControl content = base.Controls.FirstOrDefault((DXControl p) => p.Tag?.ToString() == "content");
        if (content == null)
        {
            return;
        }
        foreach (DXControl control in content.Controls)
        {
            control.Location = new Point(5, y);
            y += control.Size.Height + 6;
        }
    }

    public override void OnMouseWheel(MouseEventArgs e)
    {
        base.OnMouseWheel(e);
        UpdateLocations();
    }

    protected override void Dispose(bool disposing)
    {
        base.Dispose(disposing);
        if (disposing && ScrollBar != null)
        {
            if (!ScrollBar.IsDisposed)
            {
                ScrollBar.Dispose();
            }
            ScrollBar = null;
        }
    }
}
