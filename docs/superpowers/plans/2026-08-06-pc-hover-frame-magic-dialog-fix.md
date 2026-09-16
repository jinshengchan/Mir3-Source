# PC Hover Frame And Magic Dialog Fix Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将装备外观与属性合并为带竖线的单一外框，并恢复 PC 魔法技能窗口完整的11个分类和扩展布局。

**Architecture:** `GameScene` 复用现有 `EquipmentAppearanceLabel` 作为共同外层容器，把 `ItemLabel` 变为无背景、无边框的右区子控件，并用1像素子控件绘制分隔线。`MagicDialog` 仅从现有正确备份定点恢复扩展宽度、按钮、页面和切换逻辑，不整体覆盖当前文件。

**Tech Stack:** C# 8.0、.NET Framework 4.8、SharpDX、现有 DXControl/DXWindow/MirLibrary UI 系统。

## Global Constraints

- 装备外观和物品属性共用一个外框，中间只有一条 `1` 像素金色竖线。
- 人物与装备素材继续动态最小宽度，不缩放、不裁切。
- 右侧装备比较面板保持独立。
- 魔法技能窗口完整显示11个分类和对应页面。
- 禁止整体覆盖 `MagicDialog.cs`，只恢复与完整显示直接相关的代码。
- 不修改服务端、封包、安卓端或资源文件。

---

### Task 1: 装备悬停单一外框

**Files:**
- Modify: `145Client/Scenes/GameScene.cs`
- Test: 临时 PowerShell 源码契约与 PC 编译

**Interfaces:**
- Consumes: `EquipmentAppearanceLabel`、`ItemLabel`、动态 `appearanceWidth/alignedHeight`
- Produces: 共用外框、右区属性子控件、1像素分隔线

- [ ] **Step 1: 运行失败契约**

  检查当前源码尚未把 `ItemLabel.Parent` 设置为 `EquipmentAppearanceLabel`，且尚未关闭 `ItemLabel` 自身边框；预期检查失败。

- [ ] **Step 2: 将外观控件改为共同容器**

  外层宽度设置为 `appearanceWidth + 1 + itemWidth`，高度保持 `alignedHeight`；外层继续负责统一背景与边框。

- [ ] **Step 3: 将属性框放入右区**

  保存原属性宽度，把 `ItemLabel` 设置为外层子控件，位置为 `appearanceWidth + 1, 0`，关闭自身背景、纹理和边框，不移动任何文字子控件。

- [ ] **Step 4: 增加竖向分隔线**

  在外层创建宽 `1`、高 `alignedHeight - 2` 的金色 `DXControl`，位置为 `appearanceWidth, 1`。

- [ ] **Step 5: 调整绘制和比较面板定位**

  有共用外框时只手动绘制外层容器，由子控件流程绘制 `ItemLabel`；装备比较面板放在共同外框右侧 `4` 像素处。非装备物品保持原绘制路径。

### Task 2: 恢复完整魔法技能窗口

**Files:**
- Modify: `145Client/Scenes/Views/MagicDialog.cs`
- Reference only: `145Client/Scenes/Views/MagicDialog.cs.bak-rollback-20260730-2355`
- Test: 临时 PowerShell 完整窗口契约与 PC 编译

**Interfaces:**
- Consumes: `MagicSchool.Combat/Assassination/Assassinatie`、UI1 素材 `1711～1718/1741～1743/1750～1755`
- Produces: 加宽窗口、11个按钮、11个页面及完整切换逻辑

- [ ] **Step 1: 保留已运行的失败契约**

  当前 `extraWidth`、三个按钮、三个页面和扩展火系页面共8项均为 `False`，作为修复前红灯。

- [ ] **Step 2: 恢复窗口扩展布局**

  加入 `extraWidth = 30`、右侧背景延伸层，并把关闭按钮横坐标增加 `extraWidth`；滚动条继续使用 `Size.Width - 42` 自动跟随新右边框。

- [ ] **Step 3: 恢复11个分类按钮**

  将八个基础按钮坐标恢复为 `8/40/71/103/134/167/200/233`，新增格斗/刺杀/暗杀按钮坐标 `262/290/320`，素材使用 `1750/1752/1754`。

- [ ] **Step 4: 恢复11个技能页面**

  八个基础页面素材恢复为 `1711～1718`；新增三个页面素材 `1741～1743`，分别调用 `AddMagics` 并接入鼠标滚轮。

- [ ] **Step 5: 恢复点击切换**

  `School_Click` 同步三个新增按钮按下素材 `1751/1753/1755`，并切换三个新增页面可见性和 `CureentSchool`。

- [ ] **Step 6: 防止技能重复加入**

  `WeaponSkills` 页面只收集 `WeaponSkills/Neutral/Passive/Unconditional`，格斗、刺杀、暗杀由各自页面单独收集，避免 `Magics.Add` 重复键。

- [ ] **Step 7: 运行完整窗口契约**

  要求8项失败契约全部转为 `True`，并额外确认三个按钮按下素材、三个页面切换及武器页面排除三类刺客技能。

### Task 3: 编译、客户端和更新日志

**Files:**
- Modify: `CHANGELOG.md`
- Backup: `145Client/Scenes/GameScene.cs.bak-20260806-hover-shared-frame`
- Backup: `145Client/Scenes/Views/MagicDialog.cs.bak-20260806-complete-magic-window`
- Backup: `D:/Debug/4月18日更新/Client/Mir3.exe.bak-20260806-hover-magic-fix`

**Interfaces:**
- Consumes: `145Client/145Client.csproj`
- Produces: 更新后的 PC `Mir3.exe` 和可回滚记录

- [ ] **Step 1: 备份两个源码文件和目标客户端**

  每个目标只生成一个独立备份，不创建新产物目录。

- [ ] **Step 2: Rebuild PC 客户端**

  使用 Debug/AnyCPU 完整重建，要求退出码为 `0`。

- [ ] **Step 3: 覆盖客户端并验证哈希**

  复制到 `D:/Debug/4月18日更新/Client/Mir3.exe`，确认与编译输出 SHA-256 相同。

- [ ] **Step 4: 更新日志**

  记录两个根因、两个源码文件、备份、测试结果和最终哈希。

- [ ] **Step 5: 人工验收**

  悬停衣服确认单一外框与竖线；打开魔法窗口逐一点击11个分类，确认右上角无遮挡且技能树完整。
