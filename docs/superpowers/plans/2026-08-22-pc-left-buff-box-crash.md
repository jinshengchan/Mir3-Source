# PC LeftBuffBox Crash Fix Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Prevent Taoist observer clients from terminating when `LeftBuffBox.Process()` formats a Buff stat name whose calculated display width exceeds 20.

**Architecture:** Keep the correction entirely in the PC client presentation layer. Clamp only the padding width passed to `String.PadLeft`; preserve Buff selection, localized text, stat values, countdowns, server behavior, and observer packets.

**Tech Stack:** C#/.NET Framework 4.8 WinForms/SharpDX client, Windows PowerShell 5.1 static contracts, Visual Studio 2022 Build Tools MSBuild.

## Global Constraints

- Work in the shared non-Git tree `D:\相聚假人\Source`; preserve unrelated and concurrent edits.
- Modify only `145Client\Scenes\Views\LeftBuffBox.cs`, `.diagnostics\test_pc_left_buff_box_padding_contract.ps1`, and the existing related Taoist entry in `CHANGELOG.md`.
- Do not modify `Server\BotManager*.cs`, databases, NPC files, language resources, observer protocol, configuration, or deployment directories.
- Build Debug/AnyCPU only into an isolated `.build-check` directory.
- Do not copy binaries, restart processes, back up files, use Git, create a PR, or deploy.
- Static/build evidence is not Direct3D runtime acceptance; report the manual observation gap.

---

### Task 1: Add a red-capable focused padding contract

**Files:**
- Create: `.diagnostics\test_pc_left_buff_box_padding_contract.ps1`
- Inspect: `145Client\Scenes\Views\LeftBuffBox.cs:39-77`

**Interfaces:**
- Consumes: `LeftBuffBox.Process()` and its existing `len` calculation.
- Produces: a focused source contract whose exit code is nonzero for the unsafe implementation and zero for the clamped implementation.

- [ ] **Step 1: Record the pre-edit SHA-256 hashes**

Run:

```powershell
Get-FileHash -Algorithm SHA256 -LiteralPath `
  '145Client\Scenes\Views\LeftBuffBox.cs', `
  'CHANGELOG.md'
```

Expected: both files exist; record complete hashes before any edit.

- [ ] **Step 2: Create the focused contract**

Use this behavior in `.diagnostics\test_pc_left_buff_box_padding_contract.ps1`:

```powershell
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$sourcePath = Join-Path $root '145Client\Scenes\Views\LeftBuffBox.cs'
if (-not (Test-Path -LiteralPath $sourcePath)) { Write-Error "Missing $sourcePath"; exit 2 }

$source = Get-Content -LiteralPath $sourcePath -Raw -Encoding UTF8
$pass = 0
$fail = 0
function Assert-Source([string]$name, [bool]$condition) {
    if ($condition) { Write-Host "PASS $name"; $script:pass++ }
    else { Write-Host "FAIL $name"; $script:fail++ }
}

Assert-Source 'keeps-four-taoist-buff-types' (
    $source -match 'case\s+BuffType\.BloodLust' -and
    $source -match 'case\s+BuffType\.ElementalSuperiority' -and
    $source -match 'case\s+BuffType\.Resilience' -and
    $source -match 'case\s+BuffType\.MagicResistance'
)
Assert-Source 'keeps-language-aware-length' (
    $source -match 'type\s*==\s*Language\.SimplifiedChinese\s*\?\s*temp\.Length\s*\*\s*2\s*:\s*temp\.Length'
)
Assert-Source 'clamps-padding-width-to-nonnegative' (
    $source -match 'PadLeft\s*\(\s*Math\.Max\s*\(\s*0\s*,\s*20\s*-\s*len\s*\)\s*\)'
)
Assert-Source 'removes-unsafe-direct-padding' (
    $source -notmatch 'PadLeft\s*\(\s*20\s*-\s*len\s*\)'
)
Assert-Source 'keeps-buff-countdown' (
    $source -match '\(int\)buff\.RemainingTime\.TotalSeconds'
)
Assert-Source 'does-not-swallow-format-errors' (
    $source -notmatch '(?s)public\s+override\s+void\s+Process\s*\(\s*\).*?catch\s*\('
)

$knownText = 'PhysicalResistance'
$knownLength = $knownText.Length * 2
$knownPadding = [Math]::Max(0, 20 - $knownLength)
Assert-Source 'known-crash-input-produces-zero-padding' ($knownLength -eq 36 -and $knownPadding -eq 0)

Write-Host "TOTAL PASS $pass FAIL $fail"
if ($fail -gt 0) { exit 1 }
exit 0
```

- [ ] **Step 3: Run the contract and verify genuine RED**

Run:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .diagnostics\test_pc_left_buff_box_padding_contract.ps1
```

Expected before production edit: exit `1`; only `clamps-padding-width-to-nonnegative` and `removes-unsafe-direct-padding` fail. The four Buff types, language-aware length, countdown, no-catch, and known crash input assertions pass.

### Task 2: Clamp only the display padding width

**Files:**
- Modify: `145Client\Scenes\Views\LeftBuffBox.cs:68-70`
- Test: `.diagnostics\test_pc_left_buff_box_padding_contract.ps1`

**Interfaces:**
- Consumes: existing local integer `len`.
- Produces: the same `temp` text plus zero or more spaces, without a negative `PadLeft` width.

- [ ] **Step 1: Apply the minimal production edit**

Replace:

```csharp
temp = temp + "".PadLeft(20 - len);
```

with:

```csharp
temp = temp + "".PadLeft(Math.Max(0, 20 - len));
```

Do not reformat surrounding code, add exception handling, change Buff cases, or alter text/countdown behavior.

- [ ] **Step 2: Run focused GREEN**

Run:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .diagnostics\test_pc_left_buff_box_padding_contract.ps1
```

Expected: exit `0`, `7 PASS / 0 FAIL`.

- [ ] **Step 3: Inspect the exact production delta**

Run:

```powershell
rg -n -C 4 'Math\.Max\(0, 20 - len\)|PadLeft' 145Client\Scenes\Views\LeftBuffBox.cs
```

Expected: exactly one `PadLeft` call in `LeftBuffBox.Process`, guarded by `Math.Max(0, 20 - len)`.

### Task 3: Document and verify the PC client correction

**Files:**
- Modify: existing related Taoist entry in `CHANGELOG.md`
- Verify: `145Client\145Client.csproj`

**Interfaces:**
- Consumes: completed focused fix and contract.
- Produces: isolated Debug client artifact and evidence for primary review.

- [ ] **Step 1: Update only the existing related CHANGELOG entry**

Append a concise sentence stating that observer clients no longer pass negative padding widths to `LeftBuffBox.Process`, while Taoist Buff content and countdown behavior remain unchanged. State that Direct3D observation is still required; do not claim online acceptance.

- [ ] **Step 2: Run focused and existing PC regression contracts**

Run:

```powershell
$tests = @(
  '.diagnostics\test_pc_left_buff_box_padding_contract.ps1',
  '.diagnostics\test_pc_big_map_world_view_contract.ps1',
  '.diagnostics\test_pc_korean_magic_list_contract.ps1',
  '.diagnostics\test_pc_equipment_compare_contract.ps1',
  '.diagnostics\test_pc_pig_companion_contract.ps1'
)
foreach ($test in $tests) {
  & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $test
  if ($LASTEXITCODE -ne 0) { throw "$test failed with $LASTEXITCODE" }
}
```

Expected: focused contract `7 PASS / 0 FAIL`; each existing PC contract exits `0`. If an existing fixed-hash assertion alone is stale, report it exactly and do not edit that contract outside ownership.

- [ ] **Step 3: Rebuild Debug/AnyCPU into an isolated directory**

Run:

```powershell
$msbuild = 'C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\MSBuild\Current\Bin\MSBuild.exe'
$out = 'D:\相聚假人\Source\.build-check\pc-left-buff-box-debug\'
& $msbuild '145Client\145Client.csproj' /t:Rebuild /p:Configuration=Debug /p:Platform=AnyCPU "/p:OutputPath=$out" /nologo /v:minimal
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
```

Expected: exit `0`, zero compile errors, and an isolated `Mir3.exe` under `.build-check\pc-left-buff-box-debug`.

- [ ] **Step 4: Record final scope and artifact evidence**

Run:

```powershell
Get-FileHash -Algorithm SHA256 -LiteralPath `
  '145Client\Scenes\Views\LeftBuffBox.cs', `
  '.diagnostics\test_pc_left_buff_box_padding_contract.ps1', `
  'CHANGELOG.md', `
  '.build-check\pc-left-buff-box-debug\Mir3.exe'
Get-Item -LiteralPath '.build-check\pc-left-buff-box-debug\Mir3.exe' |
  Select-Object FullName, Length, LastWriteTime
```

Expected: only the three owned source/contract/changelog files changed; report complete hashes, artifact size, warning/error counts, and no deployment.

- [ ] **Step 5: Report the manual acceptance gap**

Manual acceptance after separately authorized deployment:

1. Observe 华佗 for at least 60 seconds while Taoist Buffs are active.
2. Observe 唐EV for at least 60 seconds while Taoist Buffs are active.
3. Observe one non-Taoist bot for at least 60 seconds.
4. Confirm Buff text/countdowns render and Windows Application log has no new `.NET Runtime` event whose frame is `LeftBuffBox.Process()`.

Do not perform these deployment/runtime actions without separate authorization.
