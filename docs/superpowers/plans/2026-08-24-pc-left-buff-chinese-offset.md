# PC Left BUFF Chinese Display and Offset Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the PC client's Taoist left-side BUFF display use “体质” instead of `StrongElement.PhysicalResistance`, while moving the entire `LeftBuffBox` down exactly 10 pixels.

**Architecture:** Keep the correction local to the two presentation points that own the behavior. `LeftBuffBox.Process()` will special-case only `Stat.PhysicalResistance` and retain the existing display path for every other stat; `GameScene` will add 10 to the existing box-level Y expression so child spacing and relative layout remain unchanged.

**Tech Stack:** C# legacy PC client, PowerShell 5.1 focused source contract, Visual Studio 2022 Build Tools/MSBuild, SHA-256 verification.

## Global Constraints

- Modify production code only in `145Client/Scenes/Views/LeftBuffBox.cs` and `145Client/Scenes/GameScene.cs`.
- Modify test code only in `.diagnostics/test_pc_left_buff_box_padding_contract.ps1`.
- Preserve the four existing Taoist BUFF cases, the `buff.RemainingTime.TotalSeconds` suffix, language-aware width calculation, `PadLeft(Math.Max(0, 20 - len))` guard, colors, dimensions, line spacing, and relative child layout.
- Do not modify `ClientSystem.db`, `145Client/Extentions/StatEx.cs`, `Library/Enum.cs`, any `.Zl` resource, server code, or mobile code.
- Build to the configured Release output `D:\Client\`; do not copy or deploy the result into `D:\Debug\4月18日更新\Client`.
- This workspace has no Git metadata. Replace commit steps with source hashes and explicit verification checkpoints; do not initialize a repository.

---

### Task 1: Localize PhysicalResistance Only in LeftBuffBox

**Files:**
- Modify: `.diagnostics/test_pc_left_buff_box_padding_contract.ps1:3-42`
- Modify: `145Client/Scenes/Views/LeftBuffBox.cs:61-70`

**Interfaces:**
- Consumes: `Stat.PhysicalResistance`, `StatEx.Lang(this Stat stat)`, and the existing `Stats.GetShortDisplay(Stat stat)` fallback.
- Produces: `temp` as “体质” for `Stat.PhysicalResistance`; every other stat still uses `stats.GetShortDisplay(pair.Key)`.

- [ ] **Step 1: Add focused localization assertions to the existing contract**

Insert these assertions after `keeps-language-aware-length` and before the padding assertions:

```powershell
Assert-Source 'physical-resistance-uses-enum-localization' (
    $source -match 'pair\.Key\s*==\s*Stat\.PhysicalResistance\s*\?\s*pair\.Key\.Lang\s*\(\s*\)'
)
Assert-Source 'other-stats-keep-short-display' (
    $source -match '\?\s*pair\.Key\.Lang\s*\(\s*\)\s*:\s*stats\.GetShortDisplay\s*\(\s*pair\.Key\s*\)'
)
```

- [ ] **Step 2: Run the expanded contract and confirm RED**

Run:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\.diagnostics\test_pc_left_buff_box_padding_contract.ps1
```

Expected: exit code `1`, the two new localization assertions report `FAIL`, and the existing seven assertions remain `PASS`, ending with `TOTAL PASS 7 FAIL 2`.

- [ ] **Step 3: Apply the minimal LeftBuffBox localization branch**

Replace:

```csharp
string temp = stats.GetShortDisplay(pair.Key);
```

with:

```csharp
string temp = pair.Key == Stat.PhysicalResistance ? pair.Key.Lang() : stats.GetShortDisplay(pair.Key);
```

Do not change the surrounding null guard, display-width calculation, padding, newline, or countdown code.

- [ ] **Step 4: Re-run the focused contract and confirm GREEN**

Run:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\.diagnostics\test_pc_left_buff_box_padding_contract.ps1
```

Expected: exit code `0`, ending with `TOTAL PASS 9 FAIL 0`.

- [ ] **Step 5: Record the first verification checkpoint**

Run:

```powershell
Get-FileHash -Algorithm SHA256 -LiteralPath `
    '.\145Client\Scenes\Views\LeftBuffBox.cs', `
    '.\.diagnostics\test_pc_left_buff_box_padding_contract.ps1'
```

Expected: two SHA-256 values are printed for the only files changed in this task.

---

### Task 2: Move the Entire LeftBuffBox Down 10 Pixels

**Files:**
- Modify: `.diagnostics/test_pc_left_buff_box_padding_contract.ps1:3-42`
- Modify: `145Client/Scenes/GameScene.cs:1616`

**Interfaces:**
- Consumes: `GameScene.Size`, `LeftBuffBox.Size`, and the existing `LeftBuffBox.Location` assignment.
- Produces: one box-level location assignment with `X = 0` and `Y = (Size.Height - LeftBuffBox.Size.Height) / 2 + 10`.

- [ ] **Step 1: Extend the contract to inspect GameScene and assert the exact location expression**

After the existing `$sourcePath` declaration and existence check, add:

```powershell
$scenePath = Join-Path $root '145Client\Scenes\GameScene.cs'
if (-not (Test-Path -LiteralPath $scenePath)) { Write-Error "Missing $scenePath"; exit 2 }
```

After loading `$source`, add:

```powershell
$scene = Get-Content -LiteralPath $scenePath -Raw -Encoding UTF8
```

Before the final `TOTAL` output, add:

```powershell
Assert-Source 'moves-entire-left-buff-box-down-ten-pixels' (
    ([regex]::Matches($scene, 'LeftBuffBox\.Location\s*=')).Count -eq 1 -and
    $scene -match 'LeftBuffBox\.Location\s*=\s*new\s+Point\s*\(\s*0\s*,\s*\(\s*Size\.Height\s*-\s*LeftBuffBox\.Size\.Height\s*\)\s*/\s*2\s*\+\s*10\s*\)\s*;'
)
```

- [ ] **Step 2: Run the contract and confirm the offset assertion is RED**

Run:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\.diagnostics\test_pc_left_buff_box_padding_contract.ps1
```

Expected: exit code `1`; the nine earlier assertions report `PASS`, the new location assertion reports `FAIL`, and the result is `TOTAL PASS 9 FAIL 1`.

- [ ] **Step 3: Add 10 pixels to the existing box-level Y expression**

Replace:

```csharp
LeftBuffBox.Location = new Point(0, (Size.Height - LeftBuffBox.Size.Height) / 2);
```

with:

```csharp
LeftBuffBox.Location = new Point(0, (Size.Height - LeftBuffBox.Size.Height) / 2 + 10);
```

Do not change the X coordinate, `LeftBuffBox.Size`, `BuffInfo`, or any neighboring UI location.

- [ ] **Step 4: Re-run the focused contract and confirm GREEN**

Run:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\.diagnostics\test_pc_left_buff_box_padding_contract.ps1
```

Expected: exit code `0`, ending with `TOTAL PASS 10 FAIL 0`.

- [ ] **Step 5: Record the second verification checkpoint**

Run:

```powershell
Get-FileHash -Algorithm SHA256 -LiteralPath `
    '.\145Client\Scenes\GameScene.cs', `
    '.\.diagnostics\test_pc_left_buff_box_padding_contract.ps1'
```

Expected: two SHA-256 values are printed for the only files changed in this task.

---

### Task 3: Run Regression, Release Build, and Protected-File Checks

**Files:**
- Verify: `.diagnostics/test_pc_left_buff_box_padding_contract.ps1`
- Verify: `145Client/Scenes/Views/LeftBuffBox.cs`
- Verify: `145Client/Scenes/GameScene.cs`
- Build: `145Client/145Client.csproj`
- Verify unchanged: `145Client/Extentions/StatEx.cs`
- Verify unchanged: `Library/Enum.cs`
- Verify unchanged: `D:\Debug\4月18日更新\Client\Mir3.exe`
- Verify unchanged: `D:\Debug\4月18日更新\Client\Data\ClientSystem.db`
- Verify unchanged: all `*.Zl` files under `D:\Debug\4月18日更新\Client`

**Interfaces:**
- Consumes: the two completed source edits and the focused PowerShell contract.
- Produces: a Release/AnyCPU `D:\Client\Mir3.exe`, final source hashes, unchanged protected-file evidence, and a clearly stated manual Direct3D acceptance gap.

- [ ] **Step 1: Run the final focused regression contract**

Run:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\.diagnostics\test_pc_left_buff_box_padding_contract.ps1
```

Expected: exit code `0`, all ten assertions pass, ending with `TOTAL PASS 10 FAIL 0`.

- [ ] **Step 2: Verify protected baselines, build Release/AnyCPU, and prove the active client tree stayed unchanged**

Run this as one PowerShell block so the `.Zl` before/after manifests remain in memory:

```powershell
$expectedProtected = @{
    'D:\相聚假人\Source\145Client\Extentions\StatEx.cs' = '741B097508A2121E5AA049B85C64EC75077D60B3F248A2EAFA2341410E65741C'
    'D:\相聚假人\Source\Library\Enum.cs' = 'D1DE8ABDA382E18DEFF7B93EDD4A8A7E45DDF90F9B40D28C3D39848AF913BFB5'
    'D:\Debug\4月18日更新\Client\Mir3.exe' = '34C84FEABF0B39C3104187092C8E192B25A7CFACB54ECE646905F2ACBD134BBB'
    'D:\Debug\4月18日更新\Client\Data\ClientSystem.db' = 'D8B5AC3C03C0E0333572FA1325167083DA5A8EF6A31D2167063596292CEFF1CD'
}

foreach ($entry in $expectedProtected.GetEnumerator()) {
    $actual = (Get-FileHash -Algorithm SHA256 -LiteralPath $entry.Key).Hash
    if ($actual -ne $entry.Value) { throw "Protected baseline mismatch: $($entry.Key)" }
}

$activeClientRoot = 'D:\Debug\4月18日更新\Client'
$zlBefore = Get-ChildItem -LiteralPath $activeClientRoot -Filter '*.Zl' -Recurse -File |
    Sort-Object FullName |
    ForEach-Object { "$($_.FullName)|$((Get-FileHash -Algorithm SHA256 -LiteralPath $_.FullName).Hash)" }

& 'C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\MSBuild\Current\Bin\MSBuild.exe' `
    'D:\相聚假人\Source\145Client\145Client.csproj' `
    /t:Rebuild /p:Configuration=Release /p:Platform=AnyCPU /m
if ($LASTEXITCODE -ne 0) { throw "MSBuild failed with exit code $LASTEXITCODE" }

foreach ($entry in $expectedProtected.GetEnumerator()) {
    $actual = (Get-FileHash -Algorithm SHA256 -LiteralPath $entry.Key).Hash
    if ($actual -ne $entry.Value) { throw "Protected file changed: $($entry.Key)" }
}

$zlAfter = Get-ChildItem -LiteralPath $activeClientRoot -Filter '*.Zl' -Recurse -File |
    Sort-Object FullName |
    ForEach-Object { "$($_.FullName)|$((Get-FileHash -Algorithm SHA256 -LiteralPath $_.FullName).Hash)" }
$zlDifference = Compare-Object -ReferenceObject $zlBefore -DifferenceObject $zlAfter
if ($zlDifference) { $zlDifference | Format-Table -AutoSize; throw 'Active .Zl resources changed' }

Get-FileHash -Algorithm SHA256 -LiteralPath 'D:\Client\Mir3.exe'
```

Expected: every protected baseline matches before and after the build; MSBuild exits `0`; any warnings are retained in the evidence; no `.Zl` differences are printed; the newly built `D:\Client\Mir3.exe` SHA-256 is printed. The build output is not copied to the active client tree.

- [ ] **Step 3: Record final hashes for all authorized implementation files**

Run:

```powershell
Get-FileHash -Algorithm SHA256 -LiteralPath `
    '.\145Client\Scenes\Views\LeftBuffBox.cs', `
    '.\145Client\Scenes\GameScene.cs', `
    '.\.diagnostics\test_pc_left_buff_box_padding_contract.ps1', `
    '.\docs\superpowers\specs\2026-08-24-pc-left-buff-chinese-offset-design.md', `
    '.\docs\superpowers\plans\2026-08-24-pc-left-buff-chinese-offset.md'
```

Expected: five SHA-256 values are recorded; no production source outside the two approved C# files is included.

- [ ] **Step 4: Hand off the remaining Direct3D acceptance check**

Report the static evidence separately from runtime acceptance. The manual in-game checklist is exactly:

1. Summon or activate the Taoist BUFF that supplies `PhysicalResistance` and confirm the label is “体质”, not `StrongElement.PhysicalResistance`.
2. Confirm the remaining-seconds number still appears after the BUFF text and continues updating.
3. Compare the left BUFF group with the previous position and confirm the whole group is 10 pixels lower.
4. Confirm all visible BUFF rows retain their spacing and are not clipped or obscured.

Do not claim these four Direct3D checks passed until they are performed in the running client.
