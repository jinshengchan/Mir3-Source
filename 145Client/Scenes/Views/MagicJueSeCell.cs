using System;
using System.Collections.Generic;
using System.Drawing;
using System.Windows.Forms;
using Client.Controls;
using Client.Envir;
using Client.Models;
using Library;
using Library.SystemModels;

namespace Client.Scenes.Views
{

	public sealed class MagicJueSeCell : DXControl
	{

		public MagicInfo Info
		{
			get
			{
				return this._Info;
			}
			set
			{
				if (this._Info == value)
				{
					return;
				}
				MagicInfo info = this._Info;
				this._Info = value;
				this.OnInfoChanged(info, value);
			}
		}


		public event EventHandler<EventArgs> InfoChanged;


		public void OnInfoChanged(MagicInfo oValue, MagicInfo nValue)
		{
			this.Image.Index = this.Info.Icon;
			EventHandler<EventArgs> infoChanged = this.InfoChanged;
			if (infoChanged == null)
			{
				return;
			}
			infoChanged(this, EventArgs.Empty);
		}


		public MagicJueSeCell()
		{
			this.Size = new Size(58, 58);
			base.DrawTexture = true;
			this.Image1 = new DXImageControl
			{
				Parent = this,
				LibraryFile = LibraryFile.Interface,
				Index = 107,
				Location = new Point(0, 0),
				IsControl = false,
				PassThrough = true,
				Visible = false
			};
			this.Image1.MouseEnter += this.ShowMagic;
			this.Image1.MouseLeave += this.HideMagic;
			this.Image1.MouseWheel += delegate(object s, MouseEventArgs e)
			{
				this.OnMouseWheel(e);
			};
			this.Image = new DXImageControl
			{
				Parent = this,
				LibraryFile = LibraryFile.MagicIcon145,
				Location = new Point(7, 7),
				BorderColour = Color.Yellow,
				Border = false
			};
			this.Image.MouseEnter += this.ShowMagic;
			this.Image.MouseLeave += this.HideMagic;
			this.Image.MouseClick += this.Image_MouseClick;
			this.Image.MouseWheel += delegate(object s, MouseEventArgs e)
			{
				this.OnMouseWheel(e);
			};
			this.MagicLevel = new DXLabel
			{
				DrawFormat = TextFormatFlags.Default,
				Parent = this,
				Location = new Point(43, 43),
				Size = new Size(10, 12),
				IsControl = false,
				Text = "",
				ForeColour = Color.Yellow,
				Visible = true
			};
		}


		private void HideMagic(object sender, EventArgs e)
		{
			GameScene.Game.MouseMagic = null;
		}


		private void ShowMagic(object sender, EventArgs e)
		{
			GameScene.Game.MouseMagic = this.Info;
		}


		private void Image_MouseClick(object sender, MouseEventArgs e)
		{
			if (GameScene.Game.Observer)
			{
				return;
			}
			ClientUserMagic clientUserMagic;
			if (!MapObject.User.Magics.TryGetValue(this.Info, out clientUserMagic))
			{
				return;
			}
			GameScene.Game.MagicBox.MagicNameLabel.Text = clientUserMagic.Info.Name;
			GameScene.Game.MagicBox.MagicNameLabel.Visible = true;
			int level = clientUserMagic.Level;
			string text = ((level == 3) ? "Level : MAX" : string.Format("Level : {0}", level));
			GameScene.Game.MagicBox.MagicLevelLabel.Text = text;
			GameScene.Game.MagicBox.MagicLevelLabel.Visible = true;
			if (level < 3)
			{
				switch (clientUserMagic.Level)
				{
				case 0:
					text = string.Format("Exp : {0}/{1}", clientUserMagic.Experience, clientUserMagic.Info.Experience1);
					break;
				case 1:
					text = string.Format("Exp : {0}/{1}", clientUserMagic.Experience, clientUserMagic.Info.Experience2);
					break;
				case 2:
					text = string.Format("Exp : {0}/{1}", clientUserMagic.Experience, clientUserMagic.Info.Experience3);
					break;
				default:
					text = string.Format("Exp : {0}/{1}", clientUserMagic.Experience, (clientUserMagic.Level - 2) * 500);
					break;
				}
				GameScene.Game.MagicBox.MagicExperienceLabel.Text = text;
				GameScene.Game.MagicBox.MagicExperienceLabel.Visible = true;
				return;
			}
			GameScene.Game.MagicBox.MagicExperienceLabel.Visible = false;
		}


		private void Image_KeyDown(object sender, KeyEventArgs e)
		{
			if (GameScene.Game.Observer)
			{
				return;
			}
			if (e.Handled)
			{
				return;
			}
			if (DXControl.MouseControl != this.Image)
			{
				return;
			}
			SpellKey spellKey = SpellKey.None;
			using (IEnumerator<KeyBindAction> enumerator = CEnvir.GetKeyAction(e.KeyCode).GetEnumerator())
			{
				while (enumerator.MoveNext())
				{
					switch (enumerator.Current)
					{
					case KeyBindAction.SpellUse01:
						spellKey = SpellKey.Spell01;
						break;
					case KeyBindAction.SpellUse02:
						spellKey = SpellKey.Spell02;
						break;
					case KeyBindAction.SpellUse03:
						spellKey = SpellKey.Spell03;
						break;
					case KeyBindAction.SpellUse04:
						spellKey = SpellKey.Spell04;
						break;
					case KeyBindAction.SpellUse05:
						spellKey = SpellKey.Spell05;
						break;
					case KeyBindAction.SpellUse06:
						spellKey = SpellKey.Spell06;
						break;
					case KeyBindAction.SpellUse07:
						spellKey = SpellKey.Spell07;
						break;
					case KeyBindAction.SpellUse08:
						spellKey = SpellKey.Spell08;
						break;
					case KeyBindAction.SpellUse09:
						spellKey = SpellKey.Spell09;
						break;
					case KeyBindAction.SpellUse10:
						spellKey = SpellKey.Spell10;
						break;
					case KeyBindAction.SpellUse11:
						spellKey = SpellKey.Spell11;
						break;
					case KeyBindAction.SpellUse12:
						spellKey = SpellKey.Spell12;
						break;
					case KeyBindAction.ToggleItemLock:
					case KeyBindAction.FortuneWindow:
					case KeyBindAction.BigPatchBoxWindow:
					case KeyBindAction.SetAutoOnHookBox:
					case KeyBindAction.NPCDKeyWindow:
					case KeyBindAction.ChatWindow:
					case KeyBindAction.FixedPointWindow:
					case KeyBindAction.BuffWindow:
					case KeyBindAction.TownReviveWindow:
					case KeyBindAction.AuctionsWindow:
					case KeyBindAction.BonusPoolWindow:
					case KeyBindAction.WarWeaponWindow:
					case KeyBindAction.GroupFrameWindow:
						continue;
					case KeyBindAction.SpellUse13:
						spellKey = SpellKey.Spell13;
						break;
					case KeyBindAction.SpellUse14:
						spellKey = SpellKey.Spell14;
						break;
					case KeyBindAction.SpellUse15:
						spellKey = SpellKey.Spell15;
						break;
					case KeyBindAction.SpellUse16:
						spellKey = SpellKey.Spell16;
						break;
					case KeyBindAction.SpellUse17:
						spellKey = SpellKey.Spell17;
						break;
					case KeyBindAction.SpellUse18:
						spellKey = SpellKey.Spell18;
						break;
					case KeyBindAction.SpellUse19:
						spellKey = SpellKey.Spell19;
						break;
					case KeyBindAction.SpellUse20:
						spellKey = SpellKey.Spell20;
						break;
					case KeyBindAction.SpellUse21:
						spellKey = SpellKey.Spell21;
						break;
					case KeyBindAction.SpellUse22:
						spellKey = SpellKey.Spell22;
						break;
					case KeyBindAction.SpellUse23:
						spellKey = SpellKey.Spell23;
						break;
					case KeyBindAction.SpellUse24:
						spellKey = SpellKey.Spell24;
						break;
					default:
						continue;
					}
					e.Handled = true;
				}
			}
			if (spellKey == SpellKey.None)
			{
				return;
			}
			ClientUserMagic clientUserMagic;
			if (!MapObject.User.Magics.TryGetValue(this.Info, out clientUserMagic))
			{
				return;
			}
			switch (GameScene.Game.MagicBarBox.SpellSet)
			{
			case 1:
				clientUserMagic.Set1Key = spellKey;
				break;
			case 2:
				clientUserMagic.Set2Key = spellKey;
				break;
			case 3:
				clientUserMagic.Set3Key = spellKey;
				break;
			case 4:
				clientUserMagic.Set4Key = spellKey;
				break;
			}
			foreach (KeyValuePair<MagicInfo, ClientUserMagic> keyValuePair in MapObject.User.Magics)
			{
				if (keyValuePair.Key != clientUserMagic.Info)
				{
					if (keyValuePair.Value.Set1Key == clientUserMagic.Set1Key && clientUserMagic.Set1Key != SpellKey.None)
					{
						keyValuePair.Value.Set1Key = SpellKey.None;
						GameScene.Game.MagicBox.Magics[keyValuePair.Key].Refresh();
					}
					if (keyValuePair.Value.Set2Key == clientUserMagic.Set2Key && clientUserMagic.Set2Key != SpellKey.None)
					{
						keyValuePair.Value.Set2Key = SpellKey.None;
						GameScene.Game.MagicBox.Magics[keyValuePair.Key].Refresh();
					}
					if (keyValuePair.Value.Set3Key == clientUserMagic.Set3Key && clientUserMagic.Set3Key != SpellKey.None)
					{
						keyValuePair.Value.Set3Key = SpellKey.None;
						GameScene.Game.MagicBox.Magics[keyValuePair.Key].Refresh();
					}
					if (keyValuePair.Value.Set4Key == clientUserMagic.Set4Key && clientUserMagic.Set4Key != SpellKey.None)
					{
						keyValuePair.Value.Set4Key = SpellKey.None;
						GameScene.Game.MagicBox.Magics[keyValuePair.Key].Refresh();
					}
				}
			}
			GameScene.Game.MagicBarBox.UpdateIcons();
		}

	
		public void Refresh()
		{
			if (MapObject.User == null)
			{
				return;
			}
			ClientUserMagic clientUserMagic;
			if (MapObject.User.Magics.TryGetValue(this.Info, out clientUserMagic))
			{
				switch (GameScene.Game.MagicBarBox.SpellSet)
				{
				case 1:
				{
					SpellKey spellKey = clientUserMagic.Set1Key;
					break;
				}
				case 2:
				{
					SpellKey spellKey = clientUserMagic.Set2Key;
					break;
				}
				case 3:
				{
					SpellKey spellKey = clientUserMagic.Set3Key;
					break;
				}
				case 4:
				{
					SpellKey spellKey = clientUserMagic.Set4Key;
					break;
				}
				}
				this.MagicLevel.Visible = true;
				this.Image.Index = this.Info.Icon;
				this.Image.ImageOpacity = 1f;
				this.MagicLevel.Text = clientUserMagic.Level.ToString();
			}
			else
			{
				this.Image.ImageOpacity = 0f;
			}
			if (this == DXControl.MouseControl)
			{
				GameScene.Game.MouseMagic = null;
				GameScene.Game.MouseMagic = this.Info;
			}
		}


		protected override void Dispose(bool disposing)
		{
			base.Dispose(disposing);
			if (disposing)
			{
				this._Info = null;
				this.InfoChanged = null;
				if (this.Image != null)
				{
					if (!this.Image.IsDisposed)
					{
						this.Image.Dispose();
					}
					this.Image = null;
				}
			}
		}


		private MagicInfo _Info;


		public DXImageControl Image;


		public DXImageControl Image1;


		public DXLabel MagicLevel;
	}
}
