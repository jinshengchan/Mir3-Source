# PC 超强骷髅模型与掉落查询文案 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 让 PC 客户端中的 `JinSkeleton` 稳定使用现有 `WhiteBone` 模型，并把主菜单和查询窗口标题统一显示为“掉落查询”。

**Architecture:** 在怪物客户端渲染库选择入口按 `MonsterFlag.JinSkeleton` 做单点模型覆盖，其他怪物仍尊重数据库的 `MonsterInfo.Image`。UI 只替换两处玩家可见字符串，不改内部类型、快捷键、配置、数据库、资源或服务端。

**Tech Stack:** C# 7.3、.NET Framework 4.8、WinForms、SharpDX Direct3D9、Windows PowerShell 5.1、VS 2022 Build Tools MSBuild。

## Global Constraints

- 仅修改 PC 桌面客户端 `145Client`；不得修改 `Mir3.Mobile`、`Mir3.Mobile000` 或服务端工程。
- 允许的生产文件只有 `145Client/Models/MonsterObject.cs`、`145Client/Scenes/Views/MainPanel.Korean.cs`、`145Client/Scenes/Views/RateQueryDiglog.cs`。
- 允许新增 `.diagnostics/test_pc_jin_skeleton_drop_query_contract.ps1`；不得修改数据库、`.Zl` 资源或部署目录。
- `JinSkeleton` 只改变客户端模型与既有 `WhiteBone` 音效分支；不得改变召唤、AI、属性、伤害或网络协议。
- 类名、快捷键、配置项、注释和内部 `RateQuery` 标识保持不变。
- 不部署或覆盖 `D:\Debug\4月18日更新\Client\Mir3.exe`；Release 构建输出仍按项目配置写到 `D:\Client\Mir3.exe`。
- 当前目录不是 Git 仓库，因此本计划不执行 `git add`、`git commit`、分支、PR 或任何 Git 初始化。

## File Map

- Create: `.diagnostics/test_pc_jin_skeleton_drop_query_contract.ps1` — 聚焦 RED/GREEN 静态契约。
- Modify: `145Client/Models/MonsterObject.cs:292` — `JinSkeleton` 的客户端模型解析兜底。
- Modify: `145Client/Scenes/Views/MainPanel.Korean.cs:337` — 主菜单玩家可见文案。
- Modify: `145Client/Scenes/Views/RateQueryDiglog.cs:39` — 查询窗口标题。
- Verify only: `145Client/145Client.csproj` — Release/AnyCPU 构建入口，不修改。
- Verify only: `D:\Debug\4月18日更新\Client\Mir3.exe` — 受保护部署产物，只记录哈希，不覆盖。

---

### Task 1: 聚焦契约 RED、最小源码修复与 GREEN

**Files:**
- Create: `.diagnostics/test_pc_jin_skeleton_drop_query_contract.ps1`
- Modify: `145Client/Models/MonsterObject.cs:292`
- Modify: `145Client/Scenes/Views/MainPanel.Korean.cs:337`
- Modify: `145Client/Scenes/Views/RateQueryDiglog.cs:39`

**Interfaces:**
- Consumes: `MonsterInfo.Flag`, `MonsterInfo.Image`, `MonsterFlag.JinSkeleton`, `MonsterImage.WhiteBone`, `RateQueryShowCheck`, `GameScene.Game.RateQueryBox`。
- Produces: `MonsterObject.Image` 在 `JinSkeleton` 时为 `WhiteBone`，其他怪物仍为 `MonsterInfo.Image`；两处玩家可见标题均为“掉落查询”。

- [ ] **Step 1: 记录执行时基线与受保护产物哈希**

Run:

```powershell
$paths = @(
    'D:\相聚假人\Source\145Client\Models\MonsterObject.cs',
    'D:\相聚假人\Source\145Client\Scenes\Views\MainPanel.Korean.cs',
    'D:\相聚假人\Source\145Client\Scenes\Views\RateQueryDiglog.cs',
    'D:\Debug\4月18日更新\Client\Mir3.exe',
    'D:\Debug\4月18日更新\Client\Data\ClientSystem.db',
    'D:\Debug\4月18日更新\Client\Data\Mon-6.Zl',
    'D:\Debug\4月18日更新\Client\Data\Mon-26.Zl'
)
Get-FileHash -Algorithm SHA256 -LiteralPath $paths | Format-Table Path, Hash -AutoSize
```

Expected: 七个路径均输出 SHA-256；保存结果供 Step 8 比对。若任一路径不存在，停止并报告，不扩大搜索或改用其他部署树。

- [ ] **Step 2: 写入能够捕获三个目标行为的失败契约**

Create `.diagnostics/test_pc_jin_skeleton_drop_query_contract.ps1` with exactly:

```powershell
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$monsterPath = Join-Path $root '145Client\Models\MonsterObject.cs'
$menuPath = Join-Path $root '145Client\Scenes\Views\MainPanel.Korean.cs'
$dialogPath = Join-Path $root '145Client\Scenes\Views\RateQueryDiglog.cs'

foreach ($path in @($monsterPath, $menuPath, $dialogPath)) {
    if (-not (Test-Path -LiteralPath $path)) {
        Write-Error "Missing $path"
        exit 2
    }
}

$monster = Get-Content -LiteralPath $monsterPath -Raw -Encoding UTF8
$menu = Get-Content -LiteralPath $menuPath -Raw -Encoding UTF8
$dialog = Get-Content -LiteralPath $dialogPath -Raw -Encoding UTF8
$pass = 0
$fail = 0

function Assert-Contract([string]$name, [bool]$condition) {
    if ($condition) {
        Write-Host "PASS $name"
        $script:pass++
    }
    else {
        Write-Host "FAIL $name"
        $script:fail++
    }
}

Assert-Contract 'jin-skeleton-resolves-to-white-bone' (
    $monster -match 'Image\s*=\s*MonsterInfo\.Flag\s*==\s*MonsterFlag\.JinSkeleton\s*\?\s*MonsterImage\.WhiteBone\s*:\s*MonsterInfo\.Image\s*;'
)
Assert-Contract 'removes-unconditional-monster-image-selection' (
    $monster -notmatch '(?m)^\s*Image\s*=\s*MonsterInfo\.Image\s*;\s*$'
)
Assert-Contract 'keeps-white-bone-resource-path' (
    $monster -match '(?s)case\s+MonsterImage\.WhiteBone\s*:.*?LibraryFile\.Mon_6.*?BodyShape\s*=\s*6\s*;'
)
Assert-Contract 'main-menu-shows-drop-query' (
    $menu -match 'CreateMenuButton\s*\(\s*88\s*,\s*"\u6389\u843d\u67e5\u8be2"'
)
Assert-Contract 'main-menu-removes-old-rate-query-label' (
    $menu -notmatch 'CreateMenuButton\s*\(\s*88\s*,\s*"\u7206\u7387\u67e5\u8be2"'
)
Assert-Contract 'main-menu-keeps-rate-query-action' (
    $menu -match '(?s)CreateMenuButton\s*\(\s*88\s*,.*?RateQueryShowCheck.*?RateQueryBox\.Visible'
)
Assert-Contract 'dialog-title-shows-drop-query' (
    $dialog -match 'TitleLabel\.Text\s*=\s*"\u6389\u843d\u67e5\u8be2"\.Lang\(\)\s*;'
)
Assert-Contract 'dialog-title-removes-old-query-labels' (
    $dialog -notmatch 'TitleLabel\.Text\s*=\s*"(?:\u66b4|\u7206)\u7387\u67e5\u8be2"\.Lang\(\)\s*;'
)

Write-Host "TOTAL PASS $pass FAIL $fail"
if ($fail -gt 0) { exit 1 }
exit 0
```

- [ ] **Step 3: 运行契约并确认真实 RED**

Run:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File 'D:\相聚假人\Source\.diagnostics\test_pc_jin_skeleton_drop_query_contract.ps1'
```

Expected: exit code `1`；`keeps-white-bone-resource-path` 与 `main-menu-keeps-rate-query-action` 为 PASS，其余六项为 FAIL；汇总必须为 `TOTAL PASS 2 FAIL 6`。如果输出不同，先修正契约使其准确描述当前基线，不得改生产代码来迎合错误契约。

- [ ] **Step 4: 应用唯一的模型解析改动**

In `145Client/Models/MonsterObject.cs`, replace:

```csharp
Image = MonsterInfo.Image;
```

with:

```csharp
Image = MonsterInfo.Flag == MonsterFlag.JinSkeleton ? MonsterImage.WhiteBone : MonsterInfo.Image;
```

Do not change the existing `case MonsterImage.WhiteBone` branch, sounds, frame tables, or any database object.

- [ ] **Step 5: 应用两处玩家可见文案改动**

In `145Client/Scenes/Views/MainPanel.Korean.cs`, replace only:

```csharp
CreateMenuButton(88, "爆率查询", (o, e) =>
```

with:

```csharp
CreateMenuButton(88, "掉落查询", (o, e) =>
```

In `145Client/Scenes/Views/RateQueryDiglog.cs`, replace only:

```csharp
TitleLabel.Text = "暴率查询".Lang();
```

with:

```csharp
TitleLabel.Text = "掉落查询".Lang();
```

Do not rename `RateQueryDiglog`, `RateQueryBox`, `RateQueryShowCheck`, `KeyBindAction.FortuneWindow`, or comments outside the two visible strings.

- [ ] **Step 6: 运行契约并确认 GREEN**

Run:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File 'D:\相聚假人\Source\.diagnostics\test_pc_jin_skeleton_drop_query_contract.ps1'
```

Expected: exit code `0`；八项均为 PASS；汇总为 `TOTAL PASS 8 FAIL 0`。

- [ ] **Step 7: Release/AnyCPU 重建 PC 客户端**

Run:

```powershell
& 'C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\MSBuild\Current\Bin\MSBuild.exe' `
  'D:\相聚假人\Source\145Client\145Client.csproj' `
  /t:Rebuild /m /v:minimal /p:Configuration=Release /p:Platform=AnyCPU
```

Expected: MSBuild exit code `0` and `D:\Client\Mir3.exe` exists. Record all warnings exactly; do not call a warning pre-existing unless current baseline evidence supports that classification.

- [ ] **Step 8: 复核范围与受保护文件未变化**

Run:

```powershell
$allowed = @(
    'D:\相聚假人\Source\.diagnostics\test_pc_jin_skeleton_drop_query_contract.ps1',
    'D:\相聚假人\Source\145Client\Models\MonsterObject.cs',
    'D:\相聚假人\Source\145Client\Scenes\Views\MainPanel.Korean.cs',
    'D:\相聚假人\Source\145Client\Scenes\Views\RateQueryDiglog.cs',
    'D:\相聚假人\Source\docs\superpowers\specs\2026-08-24-pc-jin-skeleton-drop-query-design.md',
    'D:\相聚假人\Source\docs\superpowers\plans\2026-08-24-pc-jin-skeleton-drop-query.md'
)
Get-Item -LiteralPath $allowed | Select-Object FullName, Length, LastWriteTime

$protected = @(
    'D:\Debug\4月18日更新\Client\Mir3.exe',
    'D:\Debug\4月18日更新\Client\Data\ClientSystem.db',
    'D:\Debug\4月18日更新\Client\Data\Mon-6.Zl',
    'D:\Debug\4月18日更新\Client\Data\Mon-26.Zl'
)
Get-FileHash -Algorithm SHA256 -LiteralPath $protected | Format-Table Path, Hash -AutoSize
Get-FileHash -Algorithm SHA256 -LiteralPath 'D:\Client\Mir3.exe' | Format-Table Path, Hash -AutoSize
```

Expected: four protected-file hashes exactly match Step 1；only the three approved production sources plus the contract/design/plan documents are attributable to this task；`D:\Client\Mir3.exe` has a recorded post-build hash. Because this is a non-Git tree, do not claim whole-tree diff completeness beyond explicit owned-path inspection and protected-file hashes.

- [ ] **Step 9: 记录尚未执行的运行时验收**

Final report must state that automated evidence does not cover Direct3D runtime behavior. Required manual acceptance remains:

1. Taoist summons the super skeleton and sees the model while standing.
2. The model remains visible during movement, attack, struck, and death animations, with expected `WhiteBone` sounds.
3. The Korean main menu shows “掉落查询” and opens the existing rate-query window.
4. The window title also shows “掉落查询”.

Do not deploy, start the game client, or claim these four checks passed unless the user separately authorizes and observes them.
