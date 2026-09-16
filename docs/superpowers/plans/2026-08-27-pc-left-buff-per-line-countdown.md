# PC Left BUFF Per-Line Countdown Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make every visible attribute line emitted by a supported Taoist BUFF display that BUFF's same remaining-seconds value.

**Architecture:** Keep the correction inside `LeftBuffBox.Process()`, where one `ClientBuffInfo` is expanded into visible stat lines. Append the shared `buff.RemainingTime.TotalSeconds` value while each visible line is produced, and remove the former single append after the stat loop.

**Tech Stack:** C# legacy PC client, PowerShell 5.1 focused source contract, Visual Studio 2022 Build Tools/MSBuild, SHA-256 verification.

## Global Constraints

- Modify production code only in `145Client/Scenes/Views/LeftBuffBox.cs`.
- Modify test code only in `.diagnostics/test_pc_left_buff_box_padding_contract.ps1`.
- Each visible stat line from one supported BUFF must display the same `(int)buff.RemainingTime.TotalSeconds` value.
- Preserve the four existing Taoist BUFF cases, `Stat.Duration` skipping, “体质” localization, the `GetShortDisplay()` fallback, language-aware width calculation, `PadLeft(Math.Max(0, 20 - len))`, colors, dimensions, line spacing, and the approved `LeftBuffBox` Y offset of `+ 10`.
- Do not modify `145Client/Scenes/GameScene.cs`, `145Client/Extentions/StatEx.cs`, `Library/Enum.cs`, `ServerLibrary/Models/Player/TaoistMagic.cs`, mobile or server behavior, `ClientSystem.db`, or any `.Zl` resource.
- Build to the configured Release output `D:\Client\`; do not copy or deploy the result into `D:\Debug\4月18日更新\Client`.
- This is a non-Git source tree. Do not initialize Git or create commits, branches, worktrees, tags, pushes, or PRs.
- Execute through the explicitly authorized Sol Advisor user-visible Luna task lane with model `gpt-5.6-luna` and reasoning `max`; the primary task owns monitoring, diff inspection, verification reruns, and acceptance.

---

### Task 1: Append the Shared Countdown to Every Visible Stat Line

**Files:**
- Modify: `.diagnostics/test_pc_left_buff_box_padding_contract.ps1:17-56`
- Modify: `145Client/Scenes/Views/LeftBuffBox.cs:61-75`

**Interfaces:**
- Consumes: `ClientBuffInfo.RemainingTime`, `Stats.Values`, `Stat.PhysicalResistance`, `StatEx.Lang(Stat)`, and `Stats.GetShortDisplay(Stat)`.
- Produces: one rendered line per non-null visible stat, formatted as `\n{padded stat text}{remaining whole seconds}`.

- [ ] **Step 1: Add one exact per-line countdown assertion to the existing focused contract**

Insert this assertion after `keeps-buff-countdown` and before `does-not-swallow-format-errors`:

```powershell
Assert-Source 'appends-countdown-to-each-visible-stat-line' (
    $source -match 'text\s*\+=\s*\$"\\n\{temp\}\{\(int\)buff\.RemainingTime\.TotalSeconds\}"\s*;' -and
    $source -notmatch 'text\s*\+=\s*\$"\{\(int\)buff\.RemainingTime\.TotalSeconds\}"\s*;'
)
```

This asserts both parts of the approved behavior: the countdown is joined to every emitted visible stat line, and the former standalone post-loop append no longer exists.

- [ ] **Step 2: Run the expanded contract and confirm genuine RED before changing production code**

Run:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\.diagnostics\test_pc_left_buff_box_padding_contract.ps1
```

Expected: exit code `1`; the existing ten assertions remain `PASS`; `appends-countdown-to-each-visible-stat-line` reports `FAIL`; final output is `TOTAL PASS 10 FAIL 1`.

- [ ] **Step 3: Apply the single minimal production behavior change**

Replace the current line inside the stat loop:

```csharp
text += $"\n{temp}";
```

with:

```csharp
text += $"\n{temp}{(int)buff.RemainingTime.TotalSeconds}";
```

Then delete the standalone append after the loop:

```csharp
text += $"{(int)buff.RemainingTime.TotalSeconds}";
```

Do not change any surrounding condition, padding, localization, iteration order, switch case, or layout code.

- [ ] **Step 4: Re-run the focused contract and confirm GREEN**

Run:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\.diagnostics\test_pc_left_buff_box_padding_contract.ps1
```

Expected: exit code `0`; all eleven assertions report `PASS`; final output is `TOTAL PASS 11 FAIL 0`.

- [ ] **Step 5: Record the implementation checkpoint hashes**

Run:

```powershell
Get-FileHash -Algorithm SHA256 -LiteralPath `
    '.\145Client\Scenes\Views\LeftBuffBox.cs', `
    '.\.diagnostics\test_pc_left_buff_box_padding_contract.ps1'
```

Expected: two SHA-256 values are printed for the only implementation files owned by this plan.

---

### Task 2: Rebuild Release and Verify the Protected Boundary

**Files:**
- Verify: `145Client/Scenes/Views/LeftBuffBox.cs`
- Verify: `.diagnostics/test_pc_left_buff_box_padding_contract.ps1`
- Build: `145Client/145Client.csproj`
- Verify unchanged: `145Client/Scenes/GameScene.cs`
- Verify unchanged: `145Client/Extentions/StatEx.cs`
- Verify unchanged: `Library/Enum.cs`
- Verify unchanged: `ServerLibrary/Models/Player/TaoistMagic.cs`
- Verify unchanged: `D:\Debug\4月18日更新\Client\Mir3.exe`
- Verify unchanged: `D:\Debug\4月18日更新\Client\Data\ClientSystem.db`
- Verify unchanged: all 401 current `*.Zl` files under `D:\Debug\4月18日更新\Client`

**Interfaces:**
- Consumes: the completed Task 1 source and contract changes.
- Produces: a Release/AnyCPU `D:\Client\Mir3.exe`, final owned-file hashes, protected-boundary evidence, and an explicit manual Direct3D acceptance gap.

- [ ] **Step 1: Run the final focused contract immediately before the build**

Run:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\.diagnostics\test_pc_left_buff_box_padding_contract.ps1
```

Expected: exit code `0`, ending with `TOTAL PASS 11 FAIL 0`.

- [ ] **Step 2: Verify protected baselines, rebuild Release/AnyCPU, and compare all active resources in one PowerShell session**

Run:

```powershell
$ErrorActionPreference = 'Stop'
$activeClientRoot = 'D:\Debug\4月18日更新\Client'
$expectedProtected = [ordered]@{
    'D:\相聚假人\Source\145Client\Scenes\GameScene.cs' = 'F05DE4BB0128D62F1E494B7DCBF6AC6C5B783A2F9D96B95302D5D252407FCECD'
    'D:\相聚假人\Source\145Client\Extentions\StatEx.cs' = '741B097508A2121E5AA049B85C64EC75077D60B3F248A2EAFA2341410E65741C'
    'D:\相聚假人\Source\Library\Enum.cs' = 'D1DE8ABDA382E18DEFF7B93EDD4A8A7E45DDF90F9B40D28C3D39848AF913BFB5'
    'D:\相聚假人\Source\ServerLibrary\Models\Player\TaoistMagic.cs' = '36987FDFB77278EA977281D43F23D25654B81D61A3FED19CC3BC651E660F6761'
    'D:\Debug\4月18日更新\Client\Mir3.exe' = 'DAA68527F755A208AE03908319072D688B9FEA148AE3AC005E6D89D9347C9333'
    'D:\Debug\4月18日更新\Client\Data\ClientSystem.db' = 'D8B5AC3C03C0E0333572FA1325167083DA5A8EF6A31D2167063596292CEFF1CD'
}

foreach ($entry in $expectedProtected.GetEnumerator()) {
    $actual = (Get-FileHash -Algorithm SHA256 -LiteralPath $entry.Key).Hash
    if ($actual -ne $entry.Value) { throw "Protected baseline mismatch: $($entry.Key)" }
}

$zlBefore = Get-ChildItem -LiteralPath $activeClientRoot -Filter '*.Zl' -Recurse -File |
    Sort-Object FullName |
    ForEach-Object { "$($_.FullName)|$((Get-FileHash -Algorithm SHA256 -LiteralPath $_.FullName).Hash)" }
if ($zlBefore.Count -ne 401) { throw "Unexpected active .Zl baseline count: $($zlBefore.Count)" }

& 'C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\MSBuild\Current\Bin\MSBuild.exe' `
    'D:\相聚假人\Source\145Client\145Client.csproj' `
    /t:Rebuild /p:Configuration=Release /p:Platform=AnyCPU /m /v:minimal
if ($LASTEXITCODE -ne 0) { throw "MSBuild failed with exit code $LASTEXITCODE" }

foreach ($entry in $expectedProtected.GetEnumerator()) {
    $actual = (Get-FileHash -Algorithm SHA256 -LiteralPath $entry.Key).Hash
    if ($actual -ne $entry.Value) { throw "Protected file changed: $($entry.Key)" }
}

$zlAfter = Get-ChildItem -LiteralPath $activeClientRoot -Filter '*.Zl' -Recurse -File |
    Sort-Object FullName |
    ForEach-Object { "$($_.FullName)|$((Get-FileHash -Algorithm SHA256 -LiteralPath $_.FullName).Hash)" }
$zlDifference = @(Compare-Object -ReferenceObject $zlBefore -DifferenceObject $zlAfter)
if ($zlAfter.Count -ne 401 -or $zlDifference.Count -ne 0) {
    $zlDifference | Format-Table -AutoSize
    throw "Active .Zl resources changed: after=$($zlAfter.Count), diff=$($zlDifference.Count)"
}

Get-FileHash -Algorithm SHA256 -LiteralPath `
    'D:\相聚假人\Source\145Client\Scenes\Views\LeftBuffBox.cs', `
    'D:\相聚假人\Source\.diagnostics\test_pc_left_buff_box_padding_contract.ps1', `
    'D:\Client\Mir3.exe'
```

Expected: all protected hashes match before and after; MSBuild exits `0`; warnings are recorded verbatim; the `.Zl` comparison remains `401 → 401` with difference count `0`; hashes for the two owned files and latest `D:\Client\Mir3.exe` are printed; no artifact is copied to the active client tree.

- [ ] **Step 3: Inspect the exact final implementation scope**

Run:

```powershell
Select-String -LiteralPath '.\145Client\Scenes\Views\LeftBuffBox.cs' `
    -Pattern 'text \+=|RemainingTime|PadLeft|PhysicalResistance' |
    ForEach-Object { "$($_.LineNumber):$($_.Line)" }

Select-String -LiteralPath '.\.diagnostics\test_pc_left_buff_box_padding_contract.ps1' `
    -Pattern 'appends-countdown-to-each-visible-stat-line|RemainingTime' |
    ForEach-Object { "$($_.LineNumber):$($_.Line)" }
```

Expected: the production source has one combined per-line countdown append and no standalone countdown append; the contract contains the exact new assertion; no additional behavior or file is introduced.

- [ ] **Step 4: Hand off the remaining Direct3D acceptance check**

Report static evidence separately from runtime acceptance. The manual in-game checklist is exactly:

1. Apply a `Resilience` BUFF with `PhysicalResistanceSwitch` enabled.
2. Confirm both “物理防御” and “体质” show the same remaining whole seconds.
3. Confirm both numbers update together until the BUFF expires.
4. Confirm single-line Taoist BUFFs, the existing 10-pixel lower position, line spacing, and clipping remain normal.

Do not claim these Direct3D checks passed until they are performed in the running client.
