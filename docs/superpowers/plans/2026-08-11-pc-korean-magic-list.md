# PC 韩版职业技能列表窗口 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 仅在 PC 韩版界面中，把魔法技能树替换为按当前职业技能分类动态生成的纵向技能列表，同时完整保留145界面技能树。

**Architecture:** `GameScene` 继续只持有一个 `MagicDialog`。`MagicDialog` 构造时仅根据 `KoreanInterface` 选择构建路径；145原构造代码保持原样，韩版代码放入新的 partial 文件。由于 `MagicDialog` 创建早于 `MapObject.User`，韩版窗口先构建空壳，在窗口首次显示或 `RefreshAll` 时按当前角色职业延迟生成分类和条目。

**Tech Stack:** C#、.NET Framework 4.8、WinForms/SharpDX 自定义控件、PowerShell 源码契约、VS 2022 Build Tools MSBuild。

## Global Constraints

- 仅韩版 UI 使用列表窗口；145 UI 的背景、按钮、技能树、滚动和快捷键行为保持不变。
- 顶部按钮不是职业切换，而是当前职业实际存在的非空 `MagicSchool` 分类。
- 当前职业全部技能都显示；未学习技能显示图标和红色要求等级，但不能设置快捷键。
- `WeaponSkills`、`Neutral`、`Passive`、`Unconditional` 合并为基础/武技分类。
- 不修改安卓、服务端、网络封包、数据库、登录、聊天、怪物窗口及其他无关功能。
- 不替换现有 `UI1.Zl`、`MIcon.Zl`；本次最小实现复用当前资源索引。`D:\Video\英雄客户端\Data` 只作为视觉参考，不复制未经索引兼容性验证的资源。
- 不修改或覆盖 `Mir3.ini`。
- 源码目录不是 Git 仓库；不得伪造提交。用变更前/后 SHA-256、文件清单和完整源码差异代替 commit 证据。
- 正式验证通过前不重复备份；最终部署覆盖 `Mir3.exe` 前只做一次备份。

---

### Task 1: 建立韩版技能列表源码契约

**Files:**
- Create: `.diagnostics/test_pc_korean_magic_list_contract.ps1`
- Inspect only: `145Client/Scenes/Views/MagicDialog.cs`
- Inspect only: `145Client/Scenes/GameScene.cs`
- Inspect only: `Library/Network/ClientPackets.cs`

**Interfaces:**
- Consumes: 当前 `MagicDialog`、`MagicCell`、`MagicInfo` 和 `MapObject.User.Class`。
- Produces: 一个可重复运行的 PowerShell 合同，约束韩版分支、当前职业筛选、动态分类、未学习技能可见和145隔离。

- [ ] **Step 1: 记录基线哈希和文件状态**

Run:

```powershell
$root = 'D:\相聚假人\Source'
Get-FileHash "$root\145Client\Scenes\Views\MagicDialog.cs", "$root\145Client\Scenes\GameScene.cs", "$root\Library\Network\ClientPackets.cs", "$root\CHANGELOG.md" -Algorithm SHA256
Get-Item 'D:\Debug\4月18日更新\Client\Mir3.exe', 'D:\Debug\4月18日更新\Client\Mir3.ini' | Select-Object FullName, Length, LastWriteTime
Get-FileHash 'D:\Debug\4月18日更新\Client\Mir3.exe', 'D:\Debug\4月18日更新\Client\Mir3.ini' -Algorithm SHA256
```

Expected: all listed files exist; record hashes verbatim in the Luna return.

- [ ] **Step 2: 写入失败的聚焦源码契约**

Create `.diagnostics/test_pc_korean_magic_list_contract.ps1` with these exact assertions:

```powershell
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$errors = [System.Collections.Generic.List[string]]::new()

function Read-Source([string] $relativePath) {
    Get-Content -LiteralPath (Join-Path $root $relativePath) -Raw -Encoding UTF8
}
function Require([bool] $condition, [string] $message) {
    if (-not $condition) { $errors.Add($message) }
}

$project = Read-Source '145Client/145Client.csproj'
$dialog = Read-Source '145Client/Scenes/Views/MagicDialog.cs'
$gameScene = Read-Source '145Client/Scenes/GameScene.cs'
$korean = if (Test-Path (Join-Path $root '145Client/Scenes/Views/MagicDialog.Korean.cs')) {
    Read-Source '145Client/Scenes/Views/MagicDialog.Korean.cs'
} else { '' }
$packetsPath = Join-Path $root 'Library/Network/ClientPackets.cs'

Require ($dialog -match 'public\s+sealed\s+partial\s+class\s+MagicDialog') 'MagicDialog must be partial.'
Require ($dialog -match 'GameScene\.Game\?\.KoreanInterface\s*==\s*true') 'MagicDialog must branch on KoreanInterface.'
Require ($dialog -match 'BuildKoreanInterface\s*\(\s*\)\s*;\s*return\s*;') 'Korean constructor path must return before the 145 tree is built.'
Require ($gameScene -match 'MagicBox\?\.InitializeForUser\s*\(\s*\)\s*;') 'GameScene.User must initialize the Korean magic dictionary before magic packets index it.'
Require ($dialog -match 'LibraryFile\s*=\s*LibraryFile\.UI1\s*,\s*Index\s*=\s*1620') '145 skill-tree background must remain.'
Require ($dialog -match 'AddMagics\s*\(\s*MagicSchool\.Fire\s*,\s*FirePage\s*\)') '145 Fire tree population must remain.'
Require ($project -match '<Compile Include="Scenes\\Views\\MagicDialog\.Korean\.cs"\s*/>') 'Project must compile MagicDialog.Korean.cs.'

Require ($korean -match 'MapObject\.User\.Class') 'Korean list must use the current character class.'
Require ($korean -match 'p\.Class\s*==\s*MapObject\.User\.Class') 'Korean list must filter MagicInfo by current class.'
Require ($korean -match 'NormalizeKoreanSchool') 'Korean list must normalize merged schools.'
foreach ($school in 'WeaponSkills','Neutral','Passive','Unconditional') {
    Require ($korean -match "MagicSchool\.$school") "Merged Korean school is missing: $school"
}
Require ($korean -match 'GroupBy\s*\(.*NormalizeKoreanSchool') 'Korean categories must be generated dynamically from grouped data.'
Require ($korean -notmatch 'for\s*\([^\)]*<\s*5\s*;') 'Korean category button count must not be hard-coded to five.'
Require ($korean -match 'NeedLevel1') 'Unlearned rows must display the first required level.'
Require ($korean -match 'ShowUnlearnedIcon\s*=\s*true') 'Korean rows must keep unlearned icons visible.'
Require ($dialog -match 'KoreanListMode\)\s*return\s*;') 'Learned Korean row clicks must not dereference the 145-only footer labels.'
Require ($korean -match 'DXVScrollBar') 'Korean list must have a real scroll bar.'
Require ($korean -match 'DoMouseWheel') 'Korean list must support mouse-wheel scrolling.'
Require ((Get-FileHash -LiteralPath $packetsPath -Algorithm SHA256).Hash -eq '87E4E80AD2A30967D5BDD21A0CC7ED87CCBA5412AB2FDEB4856F8CC0D883BCD6') 'ClientPackets.cs changed; packet definitions are out of scope.'

if ($errors.Count -gt 0) {
    $errors | ForEach-Object { Write-Output "FAIL: $_" }
    exit 1
}
Write-Output 'PASS: PC Korean magic list contract is satisfied.'
```

- [ ] **Step 3: 运行契约并确认先失败**

Run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File 'D:\相聚假人\Source\.diagnostics\test_pc_korean_magic_list_contract.ps1'
```

Expected: exit code 1, with failures for missing partial Korean implementation; packet hash assertion must not fail.

---

### Task 2: 实现韩版延迟生成的动态分类列表

**Files:**
- Modify: `145Client/Scenes/Views/MagicDialog.cs`
- Create: `145Client/Scenes/Views/MagicDialog.Korean.cs`
- Modify: `145Client/Scenes/GameScene.cs`
- Modify: `145Client/145Client.csproj`

**Interfaces:**
- Consumes: `GameScene.Game.KoreanInterface`, `Globals.MagicInfoList.Binding`, `MapObject.User.Class`, `MapObject.User.Magics`, `MagicInfo`, `ClientUserMagic`, `DXButton`, `DXVScrollBar`, `MagicCell`。
- Produces: `BuildKoreanInterface()`, `InitializeForUser()`, `EnsureKoreanMagicList()`, `NormalizeKoreanSchool(MagicSchool)`, `SelectKoreanSchool(MagicSchool)`, `RefreshKoreanMagicRows()`, `DisposeKoreanInterface()` and `KoreanMagicRow`。

- [ ] **Step 1: 为现有窗口增加严格隔离的韩版入口**

In `MagicDialog.cs`:

```csharp
public sealed partial class MagicDialog : DXWindow
```

At the first line of `MagicDialog()` before current145 property assignments:

```csharp
if (GameScene.Game?.KoreanInterface == true)
{
    BuildKoreanInterface();
    return;
}
```

Do not wrap, reformat, or move the existing145 constructor body.

Expose a read-only mode flag used by the existing `MagicCell` click path:

```csharp
internal bool KoreanListMode => KoreanLayout;
```

In the `GameScene.User` setter, immediately after `UserChanged();`, add:

```csharp
MagicBox?.InitializeForUser();
```

`InitializeForUser()` must be a no-op for145 and must synchronously populate the Korean `Magics` dictionary. This call must finish before later magic packets use `MagicBox.Magics[p.Magic.Info]`.

- [ ] **Step 2: 让 `MagicCell` 可在韩版中显示未学习图标**

Add one opt-in property to `MagicCell`:

```csharp
public bool ShowUnlearnedIcon { get; set; }
```

Change only the unlearned branch of `MagicCell.Refresh()`:

```csharp
else
{
    KeyImage.Visible = false;
    MagicLevel.Visible = false;
    Image.Index = Info.Icon;
    Image.ImageOpacity = ShowUnlearnedIcon ? 0.65F : 0F;
}
```

The default remains `false`, so145 cells retain the current hidden-unlearned behavior. Existing click and key handlers already return when `MapObject.User.Magics.TryGetValue` fails; do not duplicate packet logic.

Immediately after the existing learned-skill assignment `GameScene.Game.MagicBox.SelectedMagic = this;` in `Image_MouseClick`, add:

```csharp
if (GameScene.Game.MagicBox.KoreanListMode) return;
```

This retains selection highlighting but prevents the Korean path from dereferencing `MagicNameLabel`, `MagicLevelLabel`, and `MagicExperienceLabel`, which belong only to the145 footer.

- [ ] **Step 3: 建立韩版窗口骨架和延迟初始化**

Create `MagicDialog.Korean.cs` as the same namespace and partial class. Use these fixed geometry constants:

```csharp
private const int KoreanWindowWidth = 423;
private const int KoreanWindowHeight = 518;
private const int KoreanListTop = 76;
private const int KoreanListLeft = 14;
private const int KoreanListWidth = 382;
private const int KoreanListHeight = 410;
private const int KoreanRowHeight = 56;
private const int KoreanRowGap = 4;
```

Declare:

```csharp
private bool KoreanLayout;
private MirClass? KoreanBuiltClass;
private MagicSchool? KoreanSelectedSchool;
private DXControl KoreanListArea;
private DXVScrollBar KoreanScrollBar;
private readonly Dictionary<MagicSchool, DXButton> KoreanSchoolButtons = new Dictionary<MagicSchool, DXButton>();
private readonly Dictionary<MagicInfo, KoreanMagicRow> KoreanRows = new Dictionary<MagicInfo, KoreanMagicRow>();
```

`BuildKoreanInterface()` must set `KoreanLayout = true`, use a movable default `DXWindow` with title `魔法技能`, size `423x518`, create a dark list area at `(14,76)` with size `382x410`, and create the scrollbar at `(397,76)` with size `18x410`, `Change = 60`, `VisibleSize = 410`. Use `SetSkin(LibraryFile.UI1, -1, -1, -1, 1225)`. Subscribe both `VisibleChanged` and scrollbar `ValueChanged`; when the window becomes visible call `EnsureKoreanMagicList()` and `RefreshKoreanMagicRows()`.

Do not enumerate skills inside the constructor before `MapObject.User` exists.

Implement the lifecycle entry point exactly as a theme guard followed by the existing ensure/refresh pair:

```csharp
public void InitializeForUser()
{
    if (!KoreanLayout) return;
    EnsureKoreanMagicList();
    RefreshKoreanMagicRows();
}
```

- [ ] **Step 4: 动态生成当前职业的非空分类**

Use these exact normalization and exclusion rules:

```csharp
private static MagicSchool NormalizeKoreanSchool(MagicSchool school)
{
    switch (school)
    {
        case MagicSchool.Neutral:
        case MagicSchool.Passive:
        case MagicSchool.Unconditional:
            return MagicSchool.WeaponSkills;
        default:
            return school;
    }
}

private static bool IsKoreanSchoolVisible(MagicSchool school)
{
    return school != MagicSchool.None && school != MagicSchool.InternalSkill;
}
```

`EnsureKoreanMagicList()` must return while `MapObject.User == null`; otherwise query:

```csharp
List<IGrouping<MagicSchool, MagicInfo>> groups = Globals.MagicInfoList.Binding
    .Where(p => p.Class == MapObject.User.Class && IsKoreanSchoolVisible(p.School))
    .GroupBy(p => NormalizeKoreanSchool(p.School))
    .OrderBy(p => p.Key == MagicSchool.WeaponSkills ? 0 : (int)p.Key + 1)
    .ToList();
```

Create exactly one top button per group. Reuse current `UI1` school icon indices: WeaponSkills 1600, Fire 1603, Ice 1604, Lightning 1605, Wind 1606, Holy 1607, Dark 1608, Phantom 1609, Combat 1611, Assassination 1612, Assassinatie 1613. Use the existing Chinese hints from `MagicTab`. Center the actual button set horizontally; do not allocate blank buttons.

For each group, create rows ordered by `NeedLevel1`, then `Name`. Create one embedded `MagicCell` per skill with `ShowUnlearnedIcon = true`, add that cell to the existing `Magics` dictionary, and forward mouse-wheel events from the row, icon, labels and progress controls to `KoreanScrollBar.DoMouseWheel`.

- [ ] **Step 5: 实现条目状态和滚动可见性**

`KoreanMagicRow` must contain an embedded 58x58 `MagicCell`, name label, right status label, dark progress background and gold progress fill. `Refresh()` must behave as follows:

```csharp
if (!MapObject.User.Magics.TryGetValue(Info, out ClientUserMagic magic))
{
    StatusLabel.Text = $"要求等级: {Info.NeedLevel1}";
    StatusLabel.ForeColour = Color.Red;
    ProgressFill.Size = new Size(0, ProgressFill.Size.Height);
    MagicCell.Refresh();
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
```

`SelectKoreanSchool` must retain the selected school, reset scroll value to zero, set button selected state, and call one layout method. That layout method must only set `Visible = true` for rows in the selected category whose translated Y range intersects `(76,486)`; all other rows must be invisible. Set `MaxValue` from selected row count × 60 and preserve `VisibleSize = 410`. This prevents controls from drawing outside the list area without adding a new clipping framework.

- [ ] **Step 6: 接入刷新和释放，不破坏145**

At the start of `RefreshAll()`:

```csharp
if (KoreanLayout)
{
    EnsureKoreanMagicList();
    RefreshKoreanMagicRows();
    return;
}
```

For the145 loop, replace the direct dictionary index with `TryGetValue` so a missing entry cannot throw; keep behavior otherwise identical. In `Dispose(bool)`, call `DisposeKoreanInterface()` only when `KoreanLayout` is true, then retain the existing145 cleanup. `DisposeKoreanInterface()` must detach the two event handlers and clear only Korean-owned dictionaries/references.

- [ ] **Step 7: 将新 partial 文件加入旧式项目**

Add exactly:

```xml
<Compile Include="Scenes\Views\MagicDialog.Korean.cs" />
```

adjacent to `MagicDialog.cs` in `145Client.csproj`. Do not change Fody, debug symbols, target framework or build configuration.

- [ ] **Step 8: 运行聚焦契约**

Run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File 'D:\相聚假人\Source\.diagnostics\test_pc_korean_magic_list_contract.ps1'
```

Expected: exit code 0 and `PASS: PC Korean magic list contract is satisfied.`

---

### Task 3: 构建并验证韩版/145隔离

**Files:**
- Modify only if assertions need the new approved behavior: `.diagnostics/test_pc_korean_magic_list_contract.ps1`
- Build output: `D:\Client\Mir3.exe`
- Inspect only: all previously existing `.diagnostics/test_pc_*contract.ps1`

**Interfaces:**
- Consumes: Task 2 implementation and existing Release build pipeline。
- Produces: Release `Mir3.exe`, focused contract evidence, broad PC contract evidence, exact changed-file list and hashes。

- [ ] **Step 1: 运行完整相关源码契约**

Run the new focused contract, then every pre-existing `test_pc_*contract.ps1` except scripts whose own documented fixture is unavailable:

```powershell
$root = 'D:\相聚假人\Source'
powershell -NoProfile -ExecutionPolicy Bypass -File "$root\.diagnostics\test_pc_korean_magic_list_contract.ps1"
Get-ChildItem "$root\.diagnostics" -Filter 'test_pc_*contract.ps1' |
    Where-Object Name -ne 'test_pc_korean_magic_list_contract.ps1' |
    ForEach-Object {
        & powershell -NoProfile -ExecutionPolicy Bypass -File $_.FullName
        if ($LASTEXITCODE -ne 0) { throw "Contract failed: $($_.Name)" }
    }
```

Expected: every invoked script exits 0. Do not weaken stale assertions unless they directly contradict this approved Korean-only design; report any unavoidable excluded script by exact name and reason.

- [ ] **Step 2: Release/AnyCPU 编译**

Run:

```powershell
& 'C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\MSBuild\Current\Bin\MSBuild.exe' `
  'D:\相聚假人\Source\145Client\145Client.csproj' `
  /t:Rebuild /p:Configuration=Release /p:Platform=AnyCPU /m /v:minimal
```

Expected: exit code 0, zero build errors, output `D:\Client\Mir3.exe` exists.

- [ ] **Step 3: 检查范围和产物**

Run:

```powershell
Get-Item 'D:\Client\Mir3.exe' | Select-Object FullName, Length, LastWriteTime
Get-FileHash 'D:\Client\Mir3.exe' -Algorithm SHA256
Get-FileHash 'D:\Debug\4月18日更新\Client\Mir3.ini' -Algorithm SHA256
```

Expected: executable has a fresh timestamp; `Mir3.ini` hash remains the Task 1 baseline. Changed source scope is limited to the two MagicDialog files, `GameScene.cs`, csproj, focused contract, plan/spec docs, and later CHANGELOG.

- [ ] **Step 4: 运行可执行文件冒烟检查**

Start the newly built executable from a temporary client copy or the existing build output context, observe process startup for at least 10 seconds, and close it normally. Capture `SysLogs`/`Errors` produced during the run.

Expected: process does not terminate with an unhandled exception or immediately black-screen because of a missing resource. This does not replace in-game Direct3D acceptance for the two UI modes.

---

### Task 4: 最终部署、日志和人工验收交接

**Files:**
- Modify: `CHANGELOG.md`
- Final overwrite after verification: `D:\Debug\4月18日更新\Client\Mir3.exe`
- Must not modify: `D:\Debug\4月18日更新\Client\Mir3.ini`

**Interfaces:**
- Consumes: accepted Release artifact and verification evidence。
- Produces: one final backup, deployed executable, unchanged configuration hash, complete change log and manual two-theme checklist。

- [ ] **Step 1: 确认客户端已关闭并做唯一一次最终备份**

Check no running process is using the deployed executable. Create one timestamped backup of the current deployed `Mir3.exe` immediately before overwrite; do not create intermediate backups.

Expected: backup contains the exact pre-deploy executable hash recorded in Task 1.

- [ ] **Step 2: 覆盖最终可执行文件并验证哈希**

Copy `D:\Client\Mir3.exe` to `D:\Debug\4月18日更新\Client\Mir3.exe`. Then run:

```powershell
Get-FileHash 'D:\Client\Mir3.exe', 'D:\Debug\4月18日更新\Client\Mir3.exe' -Algorithm SHA256
Get-FileHash 'D:\Debug\4月18日更新\Client\Mir3.ini' -Algorithm SHA256
```

Expected: source and deployed executable hashes match; `Mir3.ini` still matches Task 1 baseline.

- [ ] **Step 3: 更新 CHANGELOG**

Add a dated `2026-08-11` entry listing:

- Korean-only dynamic current-class skill categories.
- All current-class skills shown, including red required-level state for unlearned skills.
- Learned-skill hover/key binding reuse and real scrollbar/wheel support.
- 145 skill-tree isolation.
- Exact changed source/test files.
- Exact MSBuild command, result, artifact size/SHA-256, deployed path, backup path and unchanged `Mir3.ini` SHA-256.

- [ ] **Step 4: 交付人工回归清单**

Ask the user to verify in game:

1. 韩版：战士、法师、道士、刺客分别只出现本职业的非空分类。
2. 韩版：分类按钮数量随数据库实际分类变化，切换后列表内容正确。
3. 韩版：未学习技能图标可见、要求等级为红色、不能绑定快捷键。
4. 韩版：已学习技能悬停说明、等级、熟练度、快捷键和进度刷新正常。
5. 韩版：滚轮和右侧滚动条都能滚动，边界无重复绘制、错位或卡死。
6. 145：原技能树、顶部全部分类按钮、技能位置、滚动和快捷键完全不变。

Expected: user can perform runtime visual acceptance using the deployed executable; any correction returns to the same Luna task and reruns Tasks 3-4 evidence.
