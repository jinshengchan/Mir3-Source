using Client.Controls;
using Client.Envir;
using Client.Extentions;
using Client.Models;
using Client.Scenes.Configs;
using Client.UserModels;
using Library;
using Library.SystemModels;
using System;
using System.Collections.Generic;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Threading.Tasks;
using System.Windows.Forms;
using C = Library.Network.ClientPackets;
using Color = System.Drawing.Color;
using Point = System.Drawing.Point;
using Rectangle = System.Drawing.Rectangle;

namespace Client.Scenes.Views
{
    /// <summary>
    /// 大地图功能
    /// </summary>
    public sealed class BigMapDialog : DXWindow
    {
        #region Properties

        #region SelectedInfo
        /// <summary>
        /// 选择信息
        /// </summary>
        public MapInfo SelectedInfo
        {
            get { return _SelectedInfo; }
            set
            {
                if (_SelectedInfo == value) return;

                MapInfo oldValue = _SelectedInfo;
                _SelectedInfo = value;
                OnSelectedInfoChanged(oldValue, value);
            }
        }
        private MapInfo _SelectedInfo;
        public event EventHandler<EventArgs> SelectedInfoChanged;
        public void OnSelectedInfoChanged(MapInfo oValue, MapInfo nValue)  //选定信息更改时
        {
            SelectedInfoChanged?.Invoke(this, EventArgs.Empty);
            WorldMapVisible = false;
            SetDetailVisibility();

            foreach (DXControl control in MapInfoObjects.Values)
                control.Dispose();

            MapInfoObjects.Clear();
            foreach (DXLabel label in MovementLabels.Values)
                label.Dispose();

            MovementLabels.Clear();

            ClearNpcList();
            ClearNpcSelection();

            if (SelectedInfo == null)
            {
                UpdateFrameVisibility();
                return;
            }

            Title.Text = SelectedInfo.Description;
            MapSearchBox.TextBox.Text = SelectedInfo.Description;
            Title.Location = new Point((Size.Width - Title.Size.Width) / 2, 8);
            Image.Index = WorldDetailMiniMap ?? SelectedInfo.MiniMap;
            Image.ZoomSize = MapPanelSize;
            Image.Zoom = true;

            Size imageSize = Image.ScalingSize;
            MapDisplaySize = MapPanelSize;
            Image.Location = new Point((Panel.Size.Width - imageSize.Width) / 2, (Panel.Size.Height - imageSize.Height) / 2);

            Location = new Point((GameScene.Game.Size.Width - Size.Width) / 2, (GameScene.Game.Size.Height - Size.Height) / 2);
            Opacity = 0F;

            Size size = GetMapSize(SelectedInfo.FileName);
            ScaleX = size.Width > 0 ? imageSize.Width / (float)size.Width : 1F;
            ScaleY = size.Height > 0 ? imageSize.Height / (float)size.Height : 1F;

            foreach (NPCInfo ob in Globals.NPCInfoList.Binding)
                Update(ob);

            UpdateNpcList();

            foreach (MovementInfo ob in Globals.MovementInfoList.Binding)
                Update(ob);

            foreach (ClientObjectData ob in GameScene.Game.DataDictionary.Values)
                Update(ob);

            UpdatePathToDraw = true;
            UpdateMapControlLocations();
            UpdateFrameVisibility();
        }
        /// <summary>
        /// 设置地图大小
        /// </summary>
        /// <param name="fileName"></param>
        /// <returns></returns>
        private Size GetMapSize(string fileName)
        {
            if (!File.Exists(Config.MapPath + fileName + ".map")) return Size.Empty;

            using (FileStream stream = File.OpenRead(Config.MapPath + fileName + ".map"))
            using (BinaryReader reader = new BinaryReader(stream))
            {
                //stream.Seek(22, SeekOrigin.Begin);
                //return new Size(reader.ReadInt16(), reader.ReadInt16());

                //地图扩展
                byte[] mapBytes = reader.ReadBytes(40);
                //(0-99) c#自定义地图格式 title:
                if (mapBytes[2] == 0x43 && mapBytes[3] == 0x23)
                {
                    int offset = 4;
                    if (mapBytes[0] != 1 || mapBytes[1] != 0) return Size.Empty; ;//only support version 1 atm
                    int Width = BitConverter.ToInt16(mapBytes, offset);
                    offset += 2;
                    int Height = BitConverter.ToInt16(mapBytes, offset);
                    return new Size(Width, Height);
                }
                //(200-299) 韩版传奇3 title:
                else if (mapBytes[0] == 0)
                {
                    int offset = 20;
                    short Attribute = BitConverter.ToInt16(mapBytes, offset);
                    int Width = (int)(BitConverter.ToInt16(mapBytes, offset += 2));
                    int Height = (int)(BitConverter.ToInt16(mapBytes, offset += 2));
                    return new Size(Width, Height);
                }
                //(300-399) 盛大传奇3 title: (C) SNDA, MIR3.
                else if (mapBytes[0] == 0x0F && mapBytes[5] == 0x53 && mapBytes[14] == 0x33)
                {
                    int offset = 16;
                    int Width = BitConverter.ToInt16(mapBytes, offset);
                    offset += 2;
                    int Height = BitConverter.ToInt16(mapBytes, offset);
                    return new Size(Width, Height);
                }
                //(400-499) 应该是盛大传奇3第二种格式，未知？无参考
                else if (mapBytes[0] == 0x0F && mapBytes[5] == 0x4D && mapBytes[14] == 0x33)
                {
                    int offset = 16;
                    int Width = BitConverter.ToInt16(mapBytes, offset);
                    offset += 2;
                    int Height = BitConverter.ToInt16(mapBytes, offset);
                    return new Size(Width, Height);
                }
                //(0-99) wemades antihack map (laby maps) title start with: Mir2 AntiHack
                else if (mapBytes[0] == 0x15 && mapBytes[4] == 0x32 && mapBytes[6] == 0x41 && mapBytes[19] == 0x31)
                {
                    int offset = 31;
                    int w = BitConverter.ToInt16(mapBytes, offset);
                    offset += 2;
                    int xor = BitConverter.ToInt16(mapBytes, offset);
                    offset += 2;
                    int h = BitConverter.ToInt16(mapBytes, offset);
                    int Width = (w ^ xor);
                    int Height = (h ^ xor);
                    return new Size(Width, Height);
                }
                //(0-99) wemades 2010 map format i guess title starts with: Map 2010 Ver 1.0
                else if (mapBytes[0] == 0x10 && mapBytes[2] == 0x61 && mapBytes[7] == 0x31 && mapBytes[14] == 0x31)
                {
                    int offset = 21;
                    int w = BitConverter.ToInt16(mapBytes, offset);
                    offset += 2;
                    int xor = BitConverter.ToInt16(mapBytes, offset);
                    offset += 2;
                    int h = BitConverter.ToInt16(mapBytes, offset);
                    int Width = (w ^ xor);
                    int Height = (h ^ xor);
                    return new Size(Width, Height);
                }
                //(100-199) shanda's 2012 format and one of shandas(wemades) older formats share same header info, only difference is the filesize
                else if ((mapBytes[4] == 0x0F || (mapBytes[4] == 0x03)) && mapBytes[18] == 0x0D && mapBytes[19] == 0x0A)
                {
                    int offset = 0;
                    int Width = BitConverter.ToInt16(mapBytes, offset);
                    offset += 2;
                    int Height = BitConverter.ToInt16(mapBytes, offset);
                    return new Size(Width, Height);
                }
                //(0-99) 3/4 heroes map format (myth/lifcos i guess)
                else if (mapBytes[0] == 0x0D && mapBytes[1] == 0x4C && mapBytes[7] == 0x20 && mapBytes[11] == 0x6D)
                {
                    int offset = 21;
                    int Width = BitConverter.ToInt16(mapBytes, offset);
                    offset += 4;
                    int Height = BitConverter.ToInt16(mapBytes, offset);
                    return new Size(Width, Height);
                }
                //if it's none of the above load the default old school format
                else
                {
                    int offset = 0;
                    int Width = BitConverter.ToInt16(mapBytes, offset);
                    offset += 2;
                    int Height = BitConverter.ToInt16(mapBytes, offset);
                    return new Size(Width, Height);
                }
            }
        }

        #endregion
        public DXImageControl TopLeft, TopRight, LeftLower, LowerRight;
        public Rectangle Area;   //矩形区域
        public DXImageControl Background;
        public DXImageControl Image;  //图像控制
        public DXImageControl WorldMapImage;
        public DXImageControl CurrentWorldMap;
        public DXImageControl SearchBoxFrame;
        public DXTextBox MapSearchBox;
        public DxMirButton WorldMapButton, CurrentMapButton, SearchButton;
        public DXControl Panel;  //控制面板
        public DXControl NpcPanel;
        public DXMirScrollBar NpcScrollBar;
        public List<DXLabel> NpcList = new List<DXLabel>();
        public DXAnimatedControl MapTitle;
        public DXLabel MapTitleText, Title, OverPanel;
        public Dictionary<string, DXControl> WorldPanels = new Dictionary<string, DXControl>();
        public DXButton MapCloseButton;
        private readonly Dictionary<NPCInfo, NpcMapPoint> NpcPoints = new Dictionary<NPCInfo, NpcMapPoint>();
        private NPCInfo SelectedNpc;
        private DXLabel SelectedNpcLabel, NpcTargetPoint;

        public static float ScaleX, ScaleY;

        private const int MapControlHeight = 34;
        private static readonly Size MapPanelSize = new Size(600, 420);
        private bool WorldMapVisible;
        private int? WorldDetailMiniMap;
        private Size MapDisplaySize;

        public Dictionary<object, DXControl> MapInfoObjects = new Dictionary<object, DXControl>();
        public Dictionary<MovementInfo, DXLabel> MovementLabels = new Dictionary<MovementInfo, DXLabel>();

        public bool UpdatePathToDraw
        {
            get;
            set;
        }

        public override void OnClientAreaChanged(Rectangle oValue, Rectangle nValue)  //客户端区域更改
        {
            base.OnClientAreaChanged(oValue, nValue);

            UpdateMapControlLocations();
        }
        public override void OnIsVisibleChanged(bool oValue, bool nValue)  //打开可见更改
        {
            base.OnIsVisibleChanged(oValue, nValue);

            if (IsVisible)
            {
                if (SelectedInfo == null)
                    ShowCurrentMap();
            }
            else
                SelectedInfo = null;

        }
        public override void OnOpacityChanged(float oValue, float nValue)  //不透明度改变时
        {
            base.OnOpacityChanged(oValue, nValue);

            foreach (DXControl control in Controls)
                control.Opacity = nValue;

            foreach (DXControl control in MapInfoObjects.Values)
                control.Opacity = nValue;

            if (Image != null)
            {
                Image.Opacity = nValue;
                Image.ImageOpacity = 0.85F;
            }

            if (WorldMapImage != null)
            {
                WorldMapImage.Opacity = nValue;
                WorldMapImage.ImageOpacity = nValue;
            }
        }


        public override WindowType Type => WindowType.None;
        public override bool CustomSize => false;
        public override bool AutomaticVisibility => false;

        #endregion

        /// <summary>
        /// 大地图界面
        /// </summary>
        public BigMapDialog()
        {
            HasTitle = false;  //字幕标题不显示
            HasTopBorder = false; //不显示上边框
            TitleLabel.Visible = false; //不显示标题
            DrawWindowTexture = false;
            BackColour = Color.Black;  //背景色  黑色
            HasFooter = false;  //不显示页脚
            Opacity = 0F;

            AllowResize = false;  //允许调整大小

            Background = new DXImageControl
            {
                Parent = this,
                LibraryFile = LibraryFile.GameInter,
                Index = 6100,
            };
            Size = Background.Size;
            CloseButton.Visible = false;
            MapCloseButton = new DXButton
            {
                Parent = this,
                LibraryFile = LibraryFile.UI1,
                Index = 1221,
                Sort = true,
                Visible = true,
            };
            MapCloseButton.MouseClick += (o, e) =>
            {
                ClearNpcSelection();
                HideWorldRegion();
                Visible = false;
            };

            Title = new DXLabel
            {
                Parent = Background,
                ForeColour = Color.White,
                Font = new Font(Config.FontName, CEnvir.FontSize(9F), FontStyle.Bold),
                DrawFormat = TextFormatFlags.HorizontalCenter | TextFormatFlags.VerticalCenter,
            };

            Panel = new DXControl
            {
                Parent = Background,
                Location = new Point(8, 45),
                Size = MapPanelSize,
                BackColour = Color.Black,
            };

            Image = new DXImageControl
            {
                Parent = Panel,
                LibraryFile = LibraryFile.MiniMap,
                ZoomSize = MapPanelSize,
                Zoom = true,
                ImageOpacity = 0.9F,
            };

            WorldMapImage = new DXImageControl
            {
                Parent = Background,
                LibraryFile = LibraryFile.WorldMap,
                Index = 0,
                FixedSize = true,
                Size = new Size(770, 415),
                Location = Panel.Location,
                ImageOpacity = 1F,
                Visible = false,
            };

            CurrentWorldMap = new DXImageControl
            {
                Parent = WorldMapImage,
                LibraryFile = LibraryFile.WorldMap,
                Visible = false,
                ImageOpacity = 1F,
                PassThrough = true,
                Sort = true,
            };

            OverPanel = new DXLabel
            {
                Parent = WorldMapImage,
                Size = WorldMapImage.Size,
                BackColour = Color.Black,
                Border = false,
                Opacity = 0.8F,
                PassThrough = true,
                Visible = false,
            };

            MapTitle = new DXAnimatedControl
            {
                Parent = WorldMapImage,
                LibraryFile = LibraryFile.GameInter,
                BaseIndex = 6160,
                FrameCount = 5,
                AnimationDelay = TimeSpan.FromMilliseconds(300),
                Loop = false,
                PassThrough = true,
                Location = new Point((WorldMapImage.Size.Width - 180) / 2, 4),
                Visible = false,
            };
            MapTitleText = new DXLabel
            {
                Parent = WorldMapImage,
                Border = false,
                Outline = false,
                PassThrough = true,
                ForeColour = Color.FromArgb(58, 58, 42),
                Font = new Font(Config.FontName, CEnvir.FontSize(18F)),
                Visible = false,
            };
            MapTitle.AfterAnimation += (o, e) =>
            {
                if (MapTitle.FrameCount != 6) return;
                MapTitle.BaseIndex = 6160;
                MapTitle.FrameCount = 5;
                MapTitle.AnimationStart = DateTime.MinValue;
                MapTitle.Animated = true;
            };

            CreateWorldRegions();

            NpcPanel = new DXControl
            {
                Parent = Background,
                Location = new Point(Size.Width - 170, 83),
                Size = new Size(140, 340),
            };
            NpcScrollBar = new DXMirScrollBar
            {
                Parent = Background,
                Location = new Point(NpcPanel.Location.X + NpcPanel.Size.Width + 4, NpcPanel.Location.Y - 2),
                Size = new Size(16, NpcPanel.Size.Height + 8),
            };
            NpcScrollBar.Change = 19;
            NpcScrollBar.VisibleSize = NpcScrollBar.Size.Height;
            NpcScrollBar.ValueChanged += (o, e) => UpdateNpcLocations();

            SearchButton = new DxMirButton
            {
                Parent = Background,
                LibraryFile = LibraryFile.GameInter,
                Index = 6187,
                MirButtonType = MirButtonType.FourStatu,
            };
            SearchButton.MouseClick += (o, e) => SearchMap();

            SearchBoxFrame = new DXImageControl
            {
                Parent = Background,
                LibraryFile = LibraryFile.GameInter,
                Index = 6190,
            };
            MapSearchBox = new DXTextBox
            {
                Parent = Background,
                Border = false,
                DrawTexture = false,
                BackColour = Color.FromArgb(19, 8, 6),
                ForeColour = Color.White,
                Size = new Size(SearchBoxFrame.Size.Width - 6, SearchBoxFrame.Size.Height - 4),
            };

            WorldMapButton = new DxMirButton
            {
                Parent = Background,
                LibraryFile = LibraryFile.GameInter,
                Index = 6177,
                MirButtonType = MirButtonType.FourStatu,
            };
            WorldMapButton.MouseClick += (o, e) => ShowWorldMap();

            CurrentMapButton = new DxMirButton
            {
                Parent = Background,
                LibraryFile = LibraryFile.GameInter,
                Index = 6172,
                MirButtonType = MirButtonType.FourStatu,
            };
            CurrentMapButton.MouseClick += (o, e) => ShowCurrentMap();

            MapSearchBox.TextBox.KeyPress += (o, e) =>
            {
                if (e.KeyChar != (char)Keys.Enter) return;

                e.Handled = true;
                SearchMap();
            };

            ClickTick = CEnvir.Now;
            Image.MouseMove += Image_MouseMove;  //显示鼠标指向坐标
            Image.MouseClick += Image_MouseClick;  //地图鼠标单击
            SetDetailVisibility();
            UpdateMapControlLocations();
        }

        private void SetDetailVisibility()
        {
            if (Background == null) return;

            Panel.Visible = true;
            Image.Visible = true;
            WorldMapImage.Visible = false;
            NpcPanel.Visible = true;
            NpcScrollBar.Visible = true;
            OverPanel.Visible = false;
            CurrentWorldMap.Visible = false;
            MapTitle.Visible = false;
            MapTitleText.Visible = false;
        }

        private void SetWorldVisibility()
        {
            Panel.Visible = false;
            Image.Visible = false;
            WorldMapImage.Visible = true;
            NpcPanel.Visible = false;
            NpcScrollBar.Visible = false;
            OverPanel.Visible = false;
            CurrentWorldMap.Visible = false;
            MapTitle.Visible = false;
            MapTitleText.Visible = false;
        }

        private void CreateWorldRegions()
        {
            AddWorldRegion("15", "泰山", 29, 201, new Size(110, 136), new Point(350, 20));
            AddWorldRegion("D009", "月河渊", 38, 213, new Size(174, 64), new Point(595, 0));
            AddWorldRegion("XY8", "雪原村落", 28, 137, new Size(226, 112), new Point(420, 0));
            AddWorldRegion("9", "失乐园", 25, 5, new Size(124, 120), new Point(525, 95));
            AddWorldRegion("0", "比奇城", 20, 1, new Size(156, 144), new Point(615, 85));
            AddWorldRegion("5", "沙漠土城", 23, 9, new Size(184, 148), new Point(435, 150));
            AddWorldRegion("3", "沙巴克", 21, 7, new Size(116, 86), new Point(600, 178));
            AddWorldRegion("41", "诺玛村庄", 24, 8, new Size(216, 192), new Point(375, 185));
            AddWorldRegion("2", "潘夜村落", 22, 6, new Size(95, 95), new Point(687, 278));
            AddWorldRegion("8", "潘夜岛", 35, 164, new Size(90, 64), new Point(605, 308));
            AddWorldRegion("D010", "鬼蜮", 26, -1, new Size(156, 94), new Point(580, 45));
            AddWorldRegion("D005", "本国领土", 27, 138, new Size(110, 88), new Point(475, 65));
            AddWorldRegion("15_001", "泰山长城", 30, 202, new Size(142, 102), new Point(270, 25));
            AddWorldRegion("15_003", "塞外", 31, 204, new Size(146, 110), new Point(260, 85));
            AddWorldRegion("D3904", "额头族部落", 32, 222, new Size(154, 142), new Point(150, 65));
            AddWorldRegion("19", "陆家村", 33, 211, new Size(262, 220), new Point(138, 155));
            AddWorldRegion("17", "绿洲沙漠", 34, 209, new Size(198, 196), new Point(43, 230));
            AddWorldRegion("20", "奔马岛", 36, 302, new Size(94, 86), new Point(515, 335));
            AddWorldRegion("D3400", "深虎滩海边", 37, 218, new Size(114, 82), new Point(670, 345));
            AddWorldRegion("1", "道馆", 39, -1, new Size(98, 97), new Point(540, 103));
            AddWorldRegion("12", "灌木林", 40, -1, new Size(74, 120), new Point(695, 183));
            AddWorldRegion("HFZ01", "永丰长城", 41, -1, new Size(80, 210), new Point(330, 145));
            AddWorldRegion("D3901", "义马林", 42, -1, new Size(139, 98), new Point(45, 70));
            AddWorldRegion("15_002", "迷失地域", 43, -1, new Size(150, 75), new Point(201, 0));
        }

        private void AddWorldRegion(string fileName, string displayName, int index, int miniMap, Size size, Point location)
        {
            DXControl panel = new DXControl
            {
                Parent = WorldMapImage,
                Size = size,
                Location = location,
                Tag = new WorldRegion { FileName = fileName, DisplayName = displayName, Index = index, MiniMap = miniMap },
            };
            panel.MouseEnter += WorldPanel_MouseEnter;
            panel.MouseLeave += (o, e) =>
            {
                HideWorldRegion();
            };
            panel.MouseClick += WorldRegion_MouseClick;
            WorldPanels[fileName] = panel;
        }

        private void WorldPanel_MouseEnter(object sender, EventArgs e)
        {
            DXControl panel = sender as DXControl;
            WorldRegion region = panel?.Tag as WorldRegion;
            if (region == null) return;

            if (CurrentWorldMap.Visible && CurrentWorldMap.Tag == region) return;

            CurrentWorldMap.Index = region.Index;
            CurrentWorldMap.Location = panel.Location;
            CurrentWorldMap.Tag = region;
            CurrentWorldMap.Visible = true;

            OverPanel.Visible = true;
            MapTitleText.Text = region.DisplayName;
            MapTitleText.Location = new Point((WorldMapImage.Size.Width - MapTitleText.Size.Width) / 2, MapTitle.Location.Y + 10);
            MapTitleText.Visible = true;
            MapTitle.BaseIndex = 6164;
            MapTitle.FrameCount = 6;
            MapTitle.Visible = true;
            MapTitle.AnimationStart = DateTime.MinValue;
            MapTitle.Animated = true;
            OverPanel.BringToFront();
            CurrentWorldMap.BringToFront();
            MapTitle.BringToFront();
            MapTitleText.BringToFront();
        }

        private void HideWorldRegion()
        {
            CurrentWorldMap.Visible = false;
            CurrentWorldMap.Tag = null;
            OverPanel.Visible = false;
            MapTitle.Visible = false;
            MapTitleText.Visible = false;
        }

        private void WorldRegion_MouseClick(object sender, MouseEventArgs e)
        {
            DXControl panel = sender as DXControl;
            WorldRegion region = panel?.Tag as WorldRegion;
            if (region == null) return;

            MapInfo map = ResolveWorldMap(region);
            if (map == null) return;

            try
            {
                WorldDetailMiniMap = ResolveWorldDetailMiniMap(region, map);
                if (SelectedInfo == map)
                    OnSelectedInfoChanged(map, map);
                else
                    SelectedInfo = map;
            }
            finally
            {
                WorldDetailMiniMap = null;
            }
        }

        private int? ResolveWorldDetailMiniMap(WorldRegion region, MapInfo map)
        {
            if (region.MiniMap < 0) return null;

            MirLibrary library;
            if (!CEnvir.LibraryList.TryGetValue(LibraryFile.MiniMap, out library))
                return region.MiniMap;

            MirImage image = library.GetImage(region.MiniMap);
            return image != null && image.IsZirconVersion ? region.MiniMap : map.MiniMap;
        }

        private MapInfo ResolveWorldMap(WorldRegion region)
        {
            if (region == null || Globals.MapInfoList?.Binding == null) return null;

            List<MapInfo> matches = Globals.MapInfoList.Binding
                .Where(x => x.FileName == region.FileName)
                .Take(2)
                .ToList();

            return matches.Count == 1 ? matches[0] : null;
        }

        private void ClearNpcList()
        {
            if (NpcList == null) return;

            foreach (DXLabel label in NpcList)
            {
                if (label != null && !label.IsDisposed)
                    label.Dispose();
            }

            NpcList.Clear();
        }

        private void ClearNpcSelection()
        {
            if (SelectedNpcLabel != null && !SelectedNpcLabel.IsDisposed)
            {
                SelectedNpcLabel.Border = false;
                SelectedNpcLabel.BorderColour = Color.Empty;
                SelectedNpcLabel.ForeColour = Color.White;
            }

            SelectedNpc = null;
            SelectedNpcLabel = null;

            if (NpcTargetPoint != null)
            {
                if (!NpcTargetPoint.IsDisposed)
                    NpcTargetPoint.Dispose();

                NpcTargetPoint = null;
            }
        }

        private void UpdateNpcList()
        {
            ClearNpcList();
            NpcPoints.Clear();
            if (SelectedInfo == null || NpcPanel == null) return;

            int index = 0;
            foreach (NPCInfo ob in Globals.NPCInfoList.Binding)
            {
                if (ob.Region?.Map != SelectedInfo) continue;
                if (!MapInfoObjects.TryGetValue(ob, out DXControl control)) continue;

                DXLabel label = new DXLabel
                {
                    Parent = NpcPanel,
                    AutoSize = false,
                    Size = new Size(NpcPanel.Size.Width, 16),
                    Location = new Point(0, index * 19),
                    Text = string.IsNullOrEmpty(ob.NPCName) ? "NPC" : ob.NPCName,
                    ForeColour = Color.White,
                    DrawFormat = TextFormatFlags.VerticalCenter,
                    Tag = control,
                };
                NpcPoints[ob] = new NpcMapPoint
                {
                    Point = new Point((int)((control.Location.X + control.Size.Width / 2) / ScaleX), (int)((control.Location.Y + control.Size.Height / 2) / ScaleY)),
                    Location = control.Location,
                };
                label.MouseClick += (o, e) => SelectNpc(ob, label);
                NpcList.Add(label);
                index++;
            }

            NpcScrollBar.Value = 0;
            NpcScrollBar.MaxValue = 19 * NpcList.Count;
            NpcScrollBar.VisibleSize = NpcScrollBar.Size.Height;
            UpdateNpcLocations();
        }

        private void UpdateNpcLocations()
        {
            if (NpcScrollBar == null || NpcList == null) return;

            int y = -(NpcScrollBar.Value - NpcScrollBar.Value % NpcScrollBar.Change);
            foreach (DXLabel label in NpcList)
            {
                label.Location = new Point(0, y);
                y += 19;
            }
        }

        private void SelectNpc(NPCInfo npc, DXLabel label)
        {
            if (!NpcPoints.TryGetValue(npc, out NpcMapPoint point)) return;

            if (SelectedNpcLabel != null && !SelectedNpcLabel.IsDisposed)
            {
                SelectedNpcLabel.Border = false;
                SelectedNpcLabel.BorderColour = Color.Empty;
                SelectedNpcLabel.ForeColour = Color.White;
            }

            SelectedNpc = npc;
            SelectedNpcLabel = label;
            label.Border = true;
            label.BorderColour = Color.Gold;
            label.ForeColour = Color.Yellow;

            if (NpcTargetPoint == null || NpcTargetPoint.IsDisposed)
            {
                NpcTargetPoint = new DXLabel
                {
                    Parent = Image,
                    AutoSize = false,
                    Size = new Size(9, 9),
                    Text = "●",
                    Font = new Font(Config.FontName, CEnvir.FontSize(9F), FontStyle.Bold),
                    DrawFormat = TextFormatFlags.HorizontalCenter | TextFormatFlags.VerticalCenter,
                    ForeColour = Color.Yellow,
                    Outline = true,
                    OutlineColour = Color.Black,
                    IsControl = false,
                    Sort = true,
                };
            }

            NpcTargetPoint.Location = new Point((int)(ScaleX * point.Point.X) - NpcTargetPoint.Size.Width / 2, (int)(ScaleY * point.Point.Y) - NpcTargetPoint.Size.Height / 2);
            NpcTargetPoint.Visible = true;
            NpcTargetPoint.BringToFront();

            if (SelectedInfo != GameScene.Game.MapControl.MapInfo) return;

            if (point.Point.X < 0 || point.Point.Y < 0 || point.Point.X >= GameScene.Game.MapControl.Width || point.Point.Y >= GameScene.Game.MapControl.Height) return;
            if (GameScene.Game.MapControl.Cells[point.Point.X, point.Point.Y].Flag) return;
            if (GameScene.Game.MapControl.PathFinder.bSearching) return;

            GameScene.Game.MapControl.PathFinder.bSearching = true;
            Task.Run(() =>
            {
                try
                {
                    GameScene.Game.MapControl.InitCurrentPath(point.Point.X, point.Point.Y);
                }
                finally
                {
                    GameScene.Game.MapControl.PathFinder.bSearching = false;
                }
            });
        }

        public void ShowCurrentMap()
        {
            ShowMap(GameScene.Game.MapControl.MapInfo);
        }

        public void ShowWorldMap()
        {
            ClearNpcSelection();
            Title.Text = "世界地图";
            WorldMapVisible = true;
            SetWorldVisibility();
            MapDisplaySize = WorldMapImage.Size;
            UpdateMapControlLocations();
            UpdateFrameVisibility();
        }

        private void ShowMap(MapInfo map)
        {
            WorldMapVisible = false;

            if (map != null)
            {
                Title.Text = map.Description;
                if (SelectedInfo == map)
                {
                    SetDetailVisibility();
                    UpdateNpcList();
                    UpdateMapControlLocations();
                }
                else
                    SelectedInfo = map;
            }

            UpdateFrameVisibility();
        }

        private void SearchMap()
        {
            string searchText = MapSearchBox?.TextBox?.Text?.Trim();
            if (string.IsNullOrEmpty(searchText) || Globals.MapInfoList == null) return;

            MapInfo map = Globals.MapInfoList.Binding.FirstOrDefault(x =>
                string.Equals(x.Description, searchText, StringComparison.OrdinalIgnoreCase));

            if (map == null)
            {
                map = Globals.MapInfoList.Binding.FirstOrDefault(x =>
                    x.Description?.IndexOf(searchText, StringComparison.OrdinalIgnoreCase) >= 0);
            }

            if (map != null)
                ShowMap(map);
        }

        private void UpdateMapControlLocations()
        {
            if (Background == null || SearchButton == null || MapSearchBox == null || SearchBoxFrame == null || WorldMapButton == null || CurrentMapButton == null) return;

            int y = Size.Height - 49;
            int x = 15;
            SearchButton.Location = new Point(x, y);
            int searchX = SearchButton.Location.X + SearchButton.Size.Width + 5;
            SearchBoxFrame.Location = new Point(searchX, y + 5);
            MapSearchBox.Location = new Point(searchX + 4, y + 6);
            MapSearchBox.Size = new Size(SearchBoxFrame.Size.Width - 6, SearchBoxFrame.Size.Height - 4);

            int currentMapX = Size.Width - CurrentMapButton.Size.Width - 15;
            WorldMapButton.Location = new Point(currentMapX - WorldMapButton.Size.Width - 15, y + 2);
            CurrentMapButton.Location = new Point(currentMapX, y + 2);
            MapCloseButton.Location = new Point(Size.Width - MapCloseButton.Size.Width - 5, 5);
            MapCloseButton.BringToFront();
            Title.Location = new Point((Size.Width - Title.Size.Width) / 2, 8);
        }

        private void UpdateFrameVisibility()
        {
            bool visible = Background != null && Background.Size.Width > 1 && Background.Size.Height > 1;
            if (Background != null)
                Background.Visible = visible;
            if (MapCloseButton != null)
                MapCloseButton.Visible = visible;
            if (Title != null)
                Title.Visible = visible && (WorldMapVisible || SelectedInfo != null);
        }

        public override void OnVisibleChanged(bool oValue, bool nValue) //无地图 则隐藏边角
        {
            base.OnVisibleChanged(oValue, nValue);
            UpdateFrameVisibility();
        }
        /// <summary>
        /// 显示鼠标指向坐标
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void Image_MouseMove(object sender, MouseEventArgs e)
        {
            int x = (int)((e.Location.X - Image.DisplayArea.X) / ScaleX);
            int y = (int)((e.Location.Y - Image.DisplayArea.Y) / ScaleY);
            Image.Hint = string.Format("{0},{1}", x, y, ScaleX, ScaleY);
        }

        //自动寻路状态
        public DateTime ClickTick;
        /// <summary>
        /// 鼠标单击地图
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void Image_MouseClick(object sender, MouseEventArgs e)
        {
            //修复大地图没有停止寻路时卡顿
            if (GameScene.Game.MapControl.AutoPath)
            {
                GameScene.Game.MapControl.AutoPath = false;
                GameScene.Game.ReceiveChat("BigMap.PathfindingOff".Lang(), MessageType.Hint);
            }

            //if (MapObject.User.Buffs.All(z => z.Type != BuffType.Developer))
            //if (!SelectedInfo.AllowRT || !SelectedInfo.AllowTT || !GameScene.Game.MapControl.MapInfo.AllowRT || !GameScene.Game.MapControl.MapInfo.AllowTT) return;
            int x = (int)((e.Location.X - Image.DisplayArea.X) / ScaleX);
            int y = (int)((e.Location.Y - Image.DisplayArea.Y) / ScaleY);
            if ((e.Button & MouseButtons.Right) == MouseButtons.Right)
            {
                //传送戒指               
                CEnvir.Enqueue(new C.TeleportRing { Location = new Point(x, y), Index = SelectedInfo.Index });
            }
            else if ((e.Button & MouseButtons.Left) == MouseButtons.Left)
            {
                if (BigPatchConfig.AndroidPlayer) return;
                //如果面板显示的不是当前地图，返回
                if (SelectedInfo != GameScene.Game.MapControl.MapInfo) return;

                DateTime _Last = ClickTick;
                ClickTick = CEnvir.Now;
                if (_Last.AddSeconds(1) > ClickTick)
                {
                    GameScene.Game.ReceiveChat("BigMap.PathfindingClick".Lang(), MessageType.System);
                    return;
                }

                //如果目标是不可移动区域
                if (GameScene.Game.MapControl.Cells[x, y].Flag)
                {
                    GameScene.Game.ReceiveChat("BigMap.PathfindingMove".Lang(), MessageType.System);
                    return;
                }

                //开始寻路
                if (!GameScene.Game.MapControl.PathFinder.bSearching)
                {
                    GameScene.Game.MapControl.PathFinder.bSearching = true;
                    Task.Run(() =>
                    {
                        try
                        {
                            GameScene.Game.MapControl.InitCurrentPath(x, y);

                            GameScene.Game.MapControl.PathFinder.bSearching = false;
                        }
                        catch
                        {
                            GameScene.Game.MapControl.PathFinder.bSearching = false;
                        }
                    });

                    GameScene.Game.ReceiveChat("BigMap.PathfindingOn".Lang(), MessageType.Hint);
                }
                else
                {
                    GameScene.Game.ReceiveChat("BigMap.PathfindingNotFinished".Lang(), MessageType.System);
                }
            }
        }

        #region Methods

        /// <summary>
        /// 绘制
        /// </summary>
        public override void Draw()
        {
            if (!IsVisible || Size.Width == 0 || Size.Height == 0) return;

            if (UpdatePathToDraw)
                UpdatePathForDraw();

            OnBeforeDraw();
            DrawControl();
            DrawWindow();
            OnBeforeChildrenDraw();
            DrawChildControls();
            DrawBorder();
            OnAfterDraw();

            if (UpdatePathToDraw)
                UpdatePathToDraw = false;
        }
        /// <summary>
        /// 更新自动寻路线条
        /// </summary>
        public void UpdatePathForDraw()
        {
            if (SelectedInfo == null || MapInfoObjects == null || SelectedInfo.Index != GameScene.Game.MapControl.MapInfo.Index)
            {
                return;
            }
            lock (MapInfoObjects)
            {
                if (!GameScene.Game.MapControl.AutoPath)
                {
                    for (int i = MapInfoObjects.Count - 1; i >= 0; i--)
                    {
                        KeyValuePair<object, DXControl> keyValuePair = MapInfoObjects.ElementAt(i);
                        if (keyValuePair.Key is Node)
                        {
                            keyValuePair.Value?.Dispose();
                            MapInfoObjects.Remove(keyValuePair);
                        }
                    }
                    return;
                }

                if (GameScene.Game.MapControl.CurrentPath == null) return;

                lock (GameScene.Game.MapControl.CurrentPath)
                {
                    for (int i = MapInfoObjects.Count - 1; i >= 0; i--)
                    {
                        KeyValuePair<object, DXControl> element = MapInfoObjects.ElementAt(i);
                        if (element.Key is Node && GameScene.Game.MapControl.CurrentPath.Any((Node x) => x.Location != element.Value.Location))
                        {
                            element.Value.Dispose();
                            MapInfoObjects.Remove(element);
                        }
                    }
                    for (int i = 0; i < GameScene.Game.MapControl.CurrentPath.Count; i += (int)(12 / ScaleX))
                    {
                        Node ob = GameScene.Game.MapControl.CurrentPath[i];
                        if (ob == null) continue;

                        if (MapInfoObjects.TryGetValue(ob, out var value) && !MapInfoObjects.Any((KeyValuePair<object, DXControl> x) => x.Key is Node && x.Value.Location != ob.Location))
                        {
                            if (ob != null)
                            {
                                value?.Dispose();
                                MapInfoObjects.Remove(ob);
                            }
                            continue;
                        }
                        DXControl obj = new DXControl
                        {
                            DrawTexture = true,
                            Parent = Image,
                        };
                        MapInfoObjects[ob] = obj;
                        Size size = new Size(3, 3);
                        obj.BackColour = Color.White;
                        obj.Size = size;
                        obj.Location = new Point((int)(ScaleX * (float)ob.Location.X) - size.Width / 2, (int)(ScaleY * (float)ob.Location.Y) - size.Height / 2);
                    }
                }
            }
            base.TextureValid = false;
        }
        /// <summary>
        /// 更新NPC信息
        /// </summary>
        /// <param name="ob"></param>
        public void Update(NPCInfo ob)
        {
            if (SelectedInfo == null) return;  //如果选择信息等零 返回

            DXControl control;

            if (!MapInfoObjects.TryGetValue(ob, out control))  //如果 地图信息对象 尝试获取值
            {
                if (ob.Region?.Map != SelectedInfo) return;  //如果 区域地图 不是选择信息 返回

                control = GameScene.Game.GetNPCControl(ob);
                control.Parent = Image;         //  来源=图片
                control.Visible = false;        //  不显示
                MapInfoObjects[ob] = control;   //地图信息对象 = 选择
            }
            else if ((QuestIcon)control.Tag == ob.CurrentIcon) return;  //如果 任务图标 等 当前图标  返回

            control.Dispose();
            MapInfoObjects.Remove(ob);
            if (ob.Region?.Map != SelectedInfo) return;

            control = GameScene.Game.GetNPCControl(ob);
            control.Visible = control.GetType() == typeof(DXImageControl);    //显示NPC任务标记
            control.Parent = Image;
            MapInfoObjects[ob] = control;

            Size size = GetMapSize(SelectedInfo.FileName);

            if (ob.Region.PointList == null)
                ob.Region.CreatePoints(size.Width);

            int minX = size.Width, maxX = 0, minY = size.Height, maxY = 0;

            foreach (Point point in ob.Region.PointList)
            {
                if (point.X < minX)
                    minX = point.X;
                if (point.X > maxX)
                    maxX = point.X;

                if (point.Y < minY)
                    minY = point.Y;
                if (point.Y > maxY)
                    maxY = point.Y;
            }

            int x = (minX + maxX) / 2;
            int y = (minY + maxY) / 2;

            control.Location = new Point((int)(ScaleX * x) - control.Size.Width / 2, (int)(ScaleY * y) - control.Size.Height / 2);
        }
        /// <summary>
        /// 更新怪物信息
        /// </summary>
        /// <param name="ob"></param>
        public void Update(MovementInfo ob)
        {
            if (ob.SourceRegion == null || ob.SourceRegion.Map != SelectedInfo) return;
            if (ob.DestinationRegion?.Map == null || ob.Icon == MapIcon.None) return;

            Size size = GetMapSize(SelectedInfo.FileName);

            if (ob.SourceRegion.PointList == null)
                ob.SourceRegion.CreatePoints(size.Width);

            int minX = size.Width, maxX = 0, minY = size.Height, maxY = 0;

            foreach (Point point in ob.SourceRegion.PointList)
            {
                if (point.X < minX)
                    minX = point.X;
                if (point.X > maxX)
                    maxX = point.X;

                if (point.Y < minY)
                    minY = point.Y;
                if (point.Y > maxY)
                    maxY = point.Y;
            }

            int x = (minX + maxX) / 2;
            int y = (minY + maxY) / 2;

            DXImageControl control;
            MapInfoObjects[ob] = control = new DXImageControl
            {
                LibraryFile = LibraryFile.WorldMap,
                Parent = Image,
                Opacity = 1,
                ImageOpacity = 1,
                Hint = ob.DestinationRegion.Map.Description,
            };
            control.OpacityChanged += (o, e) => control.ImageOpacity = control.Opacity;

            switch (ob.Icon)  //入口图片
            {
                case MapIcon.Cave:
                    control.Index = 70;
                    control.ForeColour = Color.Red;
                    control.LibraryFile = LibraryFile.Interface;
                    break;
                case MapIcon.Exit:
                    control.Index = 70;
                    control.ForeColour = Color.Green;
                    control.LibraryFile = LibraryFile.Interface;
                    break;
                case MapIcon.Down:
                    control.Index = 500;
                    control.LibraryFile = LibraryFile.WorldMap;
                    break;
                case MapIcon.Up:
                    control.Index = 501;
                    control.LibraryFile = LibraryFile.WorldMap;
                    break;
                case MapIcon.Province:
                    control.Index = 101;
                    control.LibraryFile = LibraryFile.WorldMap;
                    break;
                case MapIcon.Building:
                    control.Index = 6124;
                    control.LibraryFile = LibraryFile.GameInter;
                    break;
                //各种入口图标
                case MapIcon.Entrance550:
                    control.Index = 550;
                    control.LibraryFile = LibraryFile.WorldMap;
                    break;
                case MapIcon.Entrance551:
                    control.Index = 551;
                    control.LibraryFile = LibraryFile.WorldMap;
                    break;
                case MapIcon.Entrance552:
                    control.Index = 552;
                    control.LibraryFile = LibraryFile.WorldMap;
                    break;
                case MapIcon.Entrance553:
                    control.Index = 553;
                    control.LibraryFile = LibraryFile.WorldMap;
                    break;
                case MapIcon.Entrance554:
                    control.Index = 554;
                    control.LibraryFile = LibraryFile.WorldMap;
                    break;
                case MapIcon.Entrance555:
                    control.Index = 555;
                    control.LibraryFile = LibraryFile.WorldMap;
                    break;
                case MapIcon.Entrance556:
                    control.Index = 556;
                    control.LibraryFile = LibraryFile.WorldMap;
                    break;
                case MapIcon.Entrance557:
                    control.Index = 557;
                    control.LibraryFile = LibraryFile.WorldMap;
                    break;
                case MapIcon.Entrance558:
                    control.Index = 558;
                    control.LibraryFile = LibraryFile.WorldMap;
                    break;
                case MapIcon.Entrance559:
                    control.Index = 559;
                    control.LibraryFile = LibraryFile.WorldMap;
                    break;
                case MapIcon.Entrance560:
                    control.Index = 560;
                    control.LibraryFile = LibraryFile.WorldMap;
                    break;
                case MapIcon.Entrance561:
                    control.Index = 561;
                    control.LibraryFile = LibraryFile.WorldMap;
                    break;
                case MapIcon.Entrance562:
                    control.Index = 562;
                    control.LibraryFile = LibraryFile.WorldMap;
                    break;
                case MapIcon.Entrance563:
                    control.Index = 563;
                    control.LibraryFile = LibraryFile.WorldMap;
                    break;
                //连接图标
                case MapIcon.Connect100:
                    control.Index = 100;
                    control.LibraryFile = LibraryFile.WorldMap;
                    break;
                case MapIcon.Connect102:
                    control.Index = 102;
                    control.LibraryFile = LibraryFile.WorldMap;
                    break;
                case MapIcon.Connect103:
                    control.Index = 103;
                    control.LibraryFile = LibraryFile.WorldMap;
                    break;
                case MapIcon.Connect104:
                    control.Index = 104;
                    control.LibraryFile = LibraryFile.WorldMap;
                    break;
                case MapIcon.Connect120:
                    control.Index = 120;
                    control.LibraryFile = LibraryFile.WorldMap;
                    break;
                case MapIcon.Connect121:
                    control.Index = 121;
                    control.LibraryFile = LibraryFile.WorldMap;
                    break;
                case MapIcon.Connect122:
                    control.Index = 122;
                    control.LibraryFile = LibraryFile.WorldMap;
                    break;
                case MapIcon.Connect123:
                    control.Index = 123;
                    control.LibraryFile = LibraryFile.WorldMap;
                    break;
                case MapIcon.Connect140:
                    control.Index = 140;
                    control.LibraryFile = LibraryFile.WorldMap;
                    break;
                case MapIcon.Connect141:
                    control.Index = 141;
                    control.LibraryFile = LibraryFile.WorldMap;
                    break;
                case MapIcon.Connect142:
                    control.Index = 142;
                    control.LibraryFile = LibraryFile.WorldMap;
                    break;
                case MapIcon.Connect143:
                    control.Index = 143;
                    control.LibraryFile = LibraryFile.WorldMap;
                    break;
                case MapIcon.Connect160:
                    control.Index = 160;
                    control.LibraryFile = LibraryFile.WorldMap;
                    break;
                case MapIcon.Connect161:
                    control.Index = 161;
                    control.LibraryFile = LibraryFile.WorldMap;
                    break;
                case MapIcon.Connect162:
                    control.Index = 162;
                    control.LibraryFile = LibraryFile.WorldMap;
                    break;
                case MapIcon.Connect300:
                    control.Index = 300;
                    control.LibraryFile = LibraryFile.WorldMap;
                    break;
                case MapIcon.Connect301:
                    control.Index = 301;
                    control.LibraryFile = LibraryFile.WorldMap;
                    break;
                case MapIcon.Connect302:
                    control.Index = 302;
                    control.LibraryFile = LibraryFile.WorldMap;
                    break;
                case MapIcon.Connect510:
                    control.Index = 510;
                    control.LibraryFile = LibraryFile.WorldMap;
                    break;
                case MapIcon.Connect511:
                    control.Index = 511;
                    control.LibraryFile = LibraryFile.WorldMap;
                    break;
                case MapIcon.Connect570:
                    control.Index = 570;
                    control.LibraryFile = LibraryFile.WorldMap;
                    break;
                case MapIcon.Connect571:
                    control.Index = 571;
                    control.LibraryFile = LibraryFile.WorldMap;
                    break;
                case MapIcon.Connect572:
                    control.Index = 572;
                    control.LibraryFile = LibraryFile.WorldMap;
                    break;
            }
            control.MouseClick += (o, e) => SelectedInfo = ob.DestinationRegion.Map;
            control.Location = new Point((int)(ScaleX * x) - control.Size.Width / 2, (int)(ScaleY * y) - control.Size.Height / 2);

            DXLabel destinationLabel = new DXLabel
            {
                Parent = Image,
                Text = ob.DestinationRegion.Map.Description,
                ForeColour = Color.Yellow,
                Outline = true,
                OutlineColour = Color.Black,
                DrawFormat = TextFormatFlags.VerticalCenter,
                IsControl = false,
            };
            destinationLabel.Location = new Point(control.Location.X + control.Size.Width + 2, control.Location.Y + (control.Size.Height - destinationLabel.Size.Height) / 2);
            MovementLabels[ob] = destinationLabel;
        }
        /// <summary>
        /// 更新玩家数据
        /// </summary>
        /// <param name="ob"></param>
        public void Update(ClientObjectData ob)
        {
            if (SelectedInfo == null) return;

            DXControl control;

            if (!MapInfoObjects.TryGetValue(ob, out control))
            {
                if (ob.MapIndex != SelectedInfo.Index) return;
                //if (ob.ItemInfo != null && ob.ItemInfo.Rarity == Rarity.Common) return;
                if (ob.ItemInfo != null) return;
                if (ob.MonsterInfo != null && ob.Dead) return;


                MapInfoObjects[ob] = control = new DXControl
                {
                    DrawTexture = true,
                    Parent = Image,
                    Opacity = 1,
                };
            }
            else if (ob.MapIndex != SelectedInfo.Index || (ob.MonsterInfo != null && ob.Dead) || (ob.ItemInfo != null && ob.ItemInfo.Rarity == Rarity.Common))
            {
                control.Dispose();
                MapInfoObjects.Remove(ob);
                return;
            }

            Size size = new Size(3, 3);
            Color colour = Color.White;
            string name = ob.Name;

            if (ob.MonsterInfo != null)
            {
                string _temname;
                // 只过滤结尾的数字
                _temname = ob.MonsterInfo.MonsterName.TrimEnd(new char[] { '0', '1', '2', '3', '4', '5', '6', '7', '8', '9' });
                name = $"{_temname}";
                if (ob.MonsterInfo.AI < 0)
                {
                    colour = Color.LightBlue;
                }
                else
                {
                    colour = Color.Red;

                    if (GameScene.Game.HasQuest(ob.MonsterInfo, GameScene.Game.MapControl.MapInfo))
                        colour = Color.Orange;
                }

                if (ob.MonsterInfo.IsBoss)
                {
                    size = new Size(8, 8);

                    if (control.Controls.Count == 0)
                    {
                        new DXControl
                        {
                            Parent = control,
                            Location = new Point(1, 1),
                            BackColour = Color.Magenta,
                            DrawTexture = true,
                            Size = new Size(6, 6)
                        };
                    }
                    else
                        control.Controls[0].BackColour = Color.Magenta;

                    colour = Color.Pink;

                }

                if (!string.IsNullOrEmpty(ob.PetOwner))
                {
                    name += $" ({ob.PetOwner})";
                    control.DrawTexture = false;
                }
            }
            else if (ob.ItemInfo != null)
            {
                colour = Color.DarkBlue;
            }
            else
            {
                if (MapObject.User.ObjectID == ob.ObjectID)
                {
                    size = new Size(7, 7);

                    if (control.Controls.Count == 0)
                    {
                        new DXControl
                        {
                            Parent = control,
                            Location = new Point(1, 1),
                            BackColour = Color.DarkOrange,
                            DrawTexture = true,
                            Size = new Size(3, 3)
                        };
                    }
                    //else
                    //	control.Controls[0].BackColour = Color.White;
                    colour = Color.Lime;
                }
                else if (GameScene.Game.Observer)
                {
                    control.Visible = false;
                }
                else if (GameScene.Game.GroupBox.Members.Any(x => x.ObjectID == ob.ObjectID))
                {
                    colour = Color.Lime;
                }
                else if (GameScene.Game.Partner != null && GameScene.Game.Partner.ObjectID == ob.ObjectID)
                {
                    colour = Color.DeepPink;
                }
                else if (GameScene.Game.GuildBox.GuildInfo != null && GameScene.Game.GuildBox.GuildInfo.Members.Any(x => x.ObjectID == ob.ObjectID))
                {
                    colour = Color.DeepSkyBlue;
                }
            }

            control.Hint = name;
            control.BackColour = colour;
            control.Size = size;
            control.Location = new Point((int)(ScaleX * ob.Location.X) - size.Width / 2, (int)(ScaleY * ob.Location.Y) - size.Height / 2);
        }
        /// <summary>
        /// 移除
        /// </summary>
        /// <param name="ob"></param>
        public void Remove(object ob)
        {
            DXControl control;

            if (MapInfoObjects.TryGetValue(ob, out control))
            {
                control.Dispose();
                MapInfoObjects.Remove(ob);
            }

            if (ob is MovementInfo movement && MovementLabels.TryGetValue(movement, out DXLabel destinationLabel))
            {
                destinationLabel.Dispose();
                MovementLabels.Remove(movement);
            }
        }

        #endregion

        #region IDisposable

        protected override void Dispose(bool disposing)
        {
            if (disposing)
                ClearNpcSelection();

            base.Dispose(disposing);

            if (disposing)
            {
                _SelectedInfo = null;
                SelectedInfoChanged = null;

                Area = Rectangle.Empty;
                ScaleX = 0;
                ScaleY = 0;

                foreach (KeyValuePair<object, DXControl> pair in MapInfoObjects)
                {
                    if (pair.Value == null) continue;
                    if (pair.Value.IsDisposed) continue;

                    pair.Value.Dispose();
                }

                MapInfoObjects.Clear();
                MapInfoObjects = null;
                foreach (DXLabel label in MovementLabels.Values)
                {
                    if (label == null) continue;
                    if (label.IsDisposed) continue;

                    label.Dispose();
                }

                MovementLabels.Clear();
                NpcPoints.Clear();
                ClearNpcList();

                if (MapCloseButton != null)
                {
                    if (!MapCloseButton.IsDisposed)
                        MapCloseButton.Dispose();

                    MapCloseButton = null;
                }


                if (Image != null)
                {
                    if (!Image.IsDisposed)
                        Image.Dispose();

                    Image = null;
                }

                if (WorldMapImage != null)
                {
                    if (!WorldMapImage.IsDisposed)
                        WorldMapImage.Dispose();

                    WorldMapImage = null;
                }

                if (Panel != null)
                {
                    if (!Panel.IsDisposed)
                        Panel.Dispose();

                    Panel = null;
                }

                if (Background != null)
                {
                    if (!Background.IsDisposed)
                        Background.Dispose();

                    Background = null;
                }
            }
        }

        #endregion

        private sealed class WorldRegion
        {
            public string FileName;
            public string DisplayName;
            public int Index;
            public int MiniMap;
        }

        private sealed class NpcMapPoint
        {
            public Point Location;
            public Point Point;
        }
    }
}
