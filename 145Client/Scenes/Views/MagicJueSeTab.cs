using System;
using System.Drawing;
using System.Windows.Forms;
using Client.Controls;
using Client.Extentions;
using Library;

namespace Client.Scenes.Views
{

	public sealed class MagicJueSeTab : DXTab
	{

		public override void OnSizeChanged(Size oValue, Size nValue)
		{
			base.OnSizeChanged(oValue, nValue);
			this.ScrollBar.Size = new Size(15, this.Size.Height - 12);
			this.ScrollBar.Location = new Point(this.Size.Width - 22, 2);
			this.ScrollBar.SetSkin(LibraryFile.UI1, -1, -1, -1, 1672);
			int num = 2;
			foreach (DXControl dxcontrol in base.Controls)
			{
				if (dxcontrol is MagicJueSeCell)
				{
					num += dxcontrol.Size.Height + 4;
				}
			}
			this.ScrollBar.MaxValue = num;
			this.ScrollBar.VisibleSize = this.Size.Height;
			this.UpdateLocations();
		}


		public MagicJueSeTab(MagicSchool school)
		{
			base.TabButton.LibraryFile = LibraryFile.UI1;
			base.TabButton.Hint = school.ToString();
			base.BackColour = Color.Empty;
			base.Location = new Point(-5, 39);
			switch (school)
			{
			case MagicSchool.None:
				base.TabButton.Index = 1610;
				base.TabButton.Hint = "空置".Lang(Array.Empty<object>());
				break;
			case MagicSchool.WeaponSkills:
				base.TabButton.Index = 1600;
				base.TabButton.Hint = "武技".Lang(Array.Empty<object>());
				break;
			case MagicSchool.Passive:
				base.TabButton.Index = 1601;
				base.TabButton.Hint = "被动".Lang(Array.Empty<object>());
				break;
			case MagicSchool.Neutral:
				base.TabButton.Index = 1602;
				base.TabButton.Hint = "转换".Lang(Array.Empty<object>());
				break;
			case MagicSchool.Fire:
				base.TabButton.Index = 1603;
				base.TabButton.Hint = "火".Lang(Array.Empty<object>());
				break;
			case MagicSchool.Ice:
				base.TabButton.Index = 1604;
				base.TabButton.Hint = "冰".Lang(Array.Empty<object>());
				break;
			case MagicSchool.Lightning:
				base.TabButton.Index = 1605;
				base.TabButton.Hint = "雷".Lang(Array.Empty<object>());
				break;
			case MagicSchool.Wind:
				base.TabButton.Index = 1606;
				base.TabButton.Hint = "风".Lang(Array.Empty<object>());
				break;
			case MagicSchool.Holy:
				base.TabButton.Index = 1607;
				base.TabButton.Hint = "神圣".Lang(Array.Empty<object>());
				break;
			case MagicSchool.Dark:
				base.TabButton.Index = 1608;
				base.TabButton.Hint = "暗黑".Lang(Array.Empty<object>());
				break;
			case MagicSchool.Phantom:
				base.TabButton.Index = 1609;
				base.TabButton.Hint = "幻影".Lang(Array.Empty<object>());
				break;
			case MagicSchool.Unconditional:
				base.TabButton.Index = 1610;
				base.TabButton.Hint = "无条件".Lang(Array.Empty<object>());
				break;
			case MagicSchool.Combat:
				base.TabButton.Index = 1611;
				base.TabButton.Hint = "格斗".Lang(Array.Empty<object>());
				break;
			case MagicSchool.Assassination:
				base.TabButton.Index = 1612;
				base.TabButton.Hint = "刺杀".Lang(Array.Empty<object>());
				break;
			case MagicSchool.Assassinatie:
				base.TabButton.Index = 1613;
				base.TabButton.Hint = "暗杀".Lang(Array.Empty<object>());
				break;
			case MagicSchool.InternalSkill:
				base.TabButton.Index = 1610;
				base.TabButton.Hint = "内功";
				base.TabButton.Visible = false;
				break;
			}
			this.ScrollBar = new DXVScrollBar
			{
				Parent = this
			};
			this.ScrollBar.ValueChanged += delegate(object o, EventArgs e)
			{
				this.UpdateLocations();
			};
		}


		public void UpdateLocations()
		{
			int num = -this.ScrollBar.Value + 5;
			foreach (DXControl dxcontrol in base.Controls)
			{
				if (dxcontrol is MagicJueSeCell)
				{
					dxcontrol.Location = new Point(15, num);
					num += dxcontrol.Size.Height + 4;
				}
			}
		}


		public override void OnMouseWheel(MouseEventArgs e)
		{
			base.OnMouseWheel(e);
			this.UpdateLocations();
		}


		protected override void Dispose(bool disposing)
		{
			base.Dispose(disposing);
			if (disposing && this.ScrollBar != null)
			{
				if (!this.ScrollBar.IsDisposed)
				{
					this.ScrollBar.Dispose();
				}
				this.ScrollBar = null;
			}
		}


		public DXVScrollBar ScrollBar;
	}
}
