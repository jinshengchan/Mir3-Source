# PC 韩版魔法技能窗口原版边框实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 仅在 PC 韩版界面中用 `GameInter2.Zl:800-803 + 810` 恢复原版魔法技能窗口边框，并保留当前动态技能列表及全部已修功能。

**Architecture:** `MagicDialog` 的韩版 partial 继续拥有全部韩版实现。新增不可交互的顶框和主体图像层，动态分类按钮改为覆盖顶框图标的透明命中区；列表、滚动数值和技能单元格继续复用现有逻辑。145 分支及共享 `MagicDialog.cs` 不修改。

**Tech Stack:** C# / .NET Framework 4.8 / SharpDX Direct3D9 / Mir3 `DXWindow`、`DXImageControl`、`DXButton`、`DXVScrollBar` / PowerShell 静态契约 / VS 2022 MSBuild。

## Global Constraints

- 生产源码只允许修改 `145Client/Scenes/Views/MagicDialog.Korean.cs`。
- 契约只允许修改 `.diagnostics/test_pc_korean_magic_list_contract.ps1`。
- 日志只更新 `CHANGELOG.md` 现有顶部 2026-08-11/12 韩版魔法窗口记录，不创建重复历史条目。
- 不修改 `MagicDialog.cs`、145 UI、聊天、角色数量、数据库、服务端、移动端、`Mir3.ini` 或任何 `.ZL` 文件。
- 保留 `AugmentEvilSlayer -> 524` 韩版显示回退和 `MagicIcon`/`MagicIcon145` 隔离。
- 未正式验收前不创建新备份；部署时复用现有回滚备份。

---

### Task 1: 韩版完整窗口素材与透明分类命中区

**Files:**
- Modify: `145Client/Scenes/Views/MagicDialog.Korean.cs:17-183`
- Test: `.diagnostics/test_pc_korean_magic_list_contract.ps1`
- Modify: `CHANGELOG.md`

**Interfaces:**
- Consumes: `KoreanClassEmblemIndex(MirClass)` 返回当前职业顶框索引 `800-803`；现有 `KoreanSchoolOrder`、`KoreanSchool_Click`、`SelectKoreanSchool`、`UpdateKoreanRowLocations`。
- Produces: `KoreanHeader` 与 `KoreanBody` 两个不可交互的 `DXImageControl` 背景层；动态 `KoreanSchoolButtons` 只负责透明命中，不重复绘制分类图片。

- [ ] **Step 1: 扩展专项契约并取得 RED**

在 `.diagnostics/test_pc_korean_magic_list_contract.ps1` 增加精确断言：

```powershell
Require ($korean -match 'KoreanHeader\s*=\s*new\s+DXImageControl') 'Korean window must create the original header image layer.'
Require ($korean -match 'KoreanBody\s*=\s*new\s+DXImageControl') 'Korean window must create the original body image layer.'
Require ($korean -match 'KoreanBody[\s\S]{0,260}?LibraryFile\s*=\s*LibraryFile\.GameInter2[\s\S]{0,180}?Index\s*=\s*810') 'Korean body must use GameInter2 index 810.'
Require ($korean -match 'DrawWindowTexture\s*=\s*false') 'Korean mode must disable the generic DXWindow texture.'
Require ($korean -match 'HasTitle\s*=\s*false' -and $korean -match 'HasTopBorder\s*=\s*false') 'Korean mode must not draw the generic title or top border.'
Require ($korean -notmatch 'KoreanClassEmblemViewport|KoreanClassEmblem\s*=') 'Korean mode must not retain the extra cropped class emblem.'
Require ($korean -match 'button\.Index\s*=\s*-1|Index\s*=\s*-1,[\s\S]{0,180}?Tag\s*=\s*group\.Key') 'Korean category controls must use transparent hit regions.'
Require ($korean -match 'button\.FixedSize\s*=\s*true[\s\S]{0,120}?button\.Size\s*=\s*new\s+Size\(60,\s*22\)') 'Korean category hit regions must match the original 60x22 art.'
Require ($korean -match 'int\s+x\s*=\s*53\s*;' -and $korean -match 'button\.Location\s*=\s*new\s+Point\(x,\s*40\)') 'Korean category hit regions must align with the original header icons.'
```

运行：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File D:\相聚假人\Source\.diagnostics\test_pc_korean_magic_list_contract.ps1
```

预期：退出码 `1`，至少因缺少 `KoreanHeader`、`KoreanBody`、仍绘制通用窗口层、仍存在额外职业裁切控件而 RED。

- [ ] **Step 2: 建立韩版顶框和主体背景层**

在 `BuildKoreanInterface()` 中做最小替换：

```csharp
HasTitle = false;
HasFooter = false;
HasTopBorder = false;
DrawWindowTexture = false;
TitleLabel.Visible = false;
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
```

把现有 `KoreanClassEmblemViewport` 与 `KoreanClassEmblem` 字段、构建、定位和释放代码删除。`EnsureKoreanMagicList()` 中将当前职业索引赋给 `KoreanHeader.Index`。

- [ ] **Step 3: 将分类按钮改成原素材上的透明命中区**

创建按钮时保留现有 `Tag`、`Hint`、`MouseClick` 和字典，不再使用 `Interface` 图标：

```csharp
DXButton button = new DXButton
{
    Parent = this,
    Index = -1,
    FixedSize = true,
    Size = new Size(60, 22),
    Tag = group.Key,
    Hint = KoreanSchoolHint(group.Key),
};
button.Label.Visible = false;
```

按原韩版顶框的固定槽位排列：

```csharp
int x = 53;
foreach (IGrouping<MagicSchool, MagicInfo> group in groups)
{
    DXButton button = KoreanSchoolButtons[group.Key];
    button.Location = new Point(x, 40);
    x += 60;
}
```

`Pressed` 仍用于现有逻辑状态，不额外绘制第二层图标。确保透明按钮位于 `KoreanHeader` 之后创建或调用 `BringToFront()`，避免背景遮挡命中。

- [ ] **Step 4: 让列表层适配韩版主体且不产生双边框**

保留 `KoreanListArea` 作为行的裁剪/滚轮容器，但关闭其自绘底色与金色边框：

```csharp
DrawTexture = false,
Border = false,
```

保持 `Location=(14,76)`、`Size=(382,410)`、技能行、滚动范围和鼠标滚轮逻辑不变。`810` 已含右侧滚动轨道外观；保留 `DXVScrollBar` 的数值、拖动和滚轮功能，调整其透明/皮肤绘制不得增加第二条轨道。若现有 `SetSkin(UI1, ..., 1225)` 在截图中产生双轨，契约先加入单轨断言，再仅在韩版 partial 内改为透明交互滑块；不要修改共享 `DXVScrollBar`。

- [ ] **Step 5: 保持关闭与移动功能**

通用窗口纹理关闭后，保留现有 `CloseButton` 控件并置于韩版顶框右上角，确保可点击且不被背景遮挡：

```csharp
CloseButton.Location = new Point(392, 5);
CloseButton.BringToFront();
```

窗口移动逻辑继续由 `DXWindow` 提供；不新增拖动代码。

- [ ] **Step 6: 运行专项契约取得 GREEN**

运行：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File D:\相聚假人\Source\.diagnostics\test_pc_korean_magic_list_contract.ps1
```

预期：退出码 `0`，输出 `PASS: PC Korean magic list contract is satisfied.`；同时确认 `Globals.cs`、`SelectScene.cs`、`MagicDialog.cs`、`ChatTextBox.cs` 和 Server 范围保护哈希未变化。

- [ ] **Step 7: Release/AnyCPU 重新编译**

运行：

```powershell
& 'C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\MSBuild\Current\Bin\MSBuild.exe' `
  'D:\相聚假人\Source\145Client\145Client.csproj' `
  /t:Rebuild /m /v:minimal /p:Configuration=Release /p:Platform=AnyCPU
```

预期：退出码 `0`、0 errors；只允许既有 `BigPatchConfig.ChkLockMonEffect` `CS0649` warning。记录 `D:\Client\Mir3.exe` 的大小、时间和 SHA-256。

- [ ] **Step 8: 更新现有日志并交由主任务复验部署**

只更新 `CHANGELOG.md` 现有顶部韩版魔法窗口条目，记录素材索引、透明命中区、RED/GREEN、构建证据和待实机验证项。主任务重新运行契约、核对完整源码范围和产物哈希；确认 `Mir3` 未运行后覆盖 `D:\Debug\4月18日更新\Client\Mir3.exe`，不创建新备份、不改写 `Mir3.ini`，并把最终部署哈希补入同一条日志。
