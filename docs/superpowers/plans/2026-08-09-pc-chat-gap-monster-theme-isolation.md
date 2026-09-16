# PC Chat Gap and Monster Theme Isolation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remove the Korean chat gap and restore the original 145 monster window without changing the accepted Korean monster window.

**Architecture:** Keep the existing public `MonsterDialog` API and select one layout at construction from the game scene's locked interface mode. Share monster data/refresh methods, but isolate layout, positioning, and hover/movement visibility behavior by theme.

**Tech Stack:** C#/.NET Framework, SlimDX Direct3D controls, PowerShell source contracts, Visual Studio 2022 MSBuild.

## Global Constraints

- Source root is the non-Git tree `D:\相聚假人\Source`.
- Original 145 source baseline is `D:\相聚\145Client` and is read-only.
- Do not create another source backup before user visual acceptance.
- Do not change mobile, server, ZL resources, `Mir3.ini`, or unrelated UI.
- Use `apply_patch` for production source edits.
- Primary task owns build, deployment, `CHANGELOG.md`, actual-diff inspection, and final acceptance.
- Deployment may overwrite only `D:\Debug\4月18日更新\Client\Mir3.exe`; its `Mir3.ini` hash must remain unchanged.

---

### Task 1: Create the focused RED contract

**Files:**
- Create: `C:\Users\chen\Documents\Codex\2026-08-08\mir3-pc-dual-ui-luna\work\pc-chat-gap-monster-theme-isolation-contract.ps1`
- Read: `D:\相聚假人\Source\145Client\Scenes\GameScene.cs`
- Read: `D:\相聚假人\Source\145Client\Scenes\Views\ChatDialog.Korean.cs`
- Read: `D:\相聚假人\Source\145Client\Scenes\Views\MonsterDialog.cs`
- Read: `D:\相聚\145Client\Scenes\Views\MonsterDialog.cs`
- Read: `D:\相聚\145Client\Scenes\GameScene.cs`

**Interfaces:**
- Consumes: current production source and read-only original 145 source.
- Produces: a PowerShell contract that distinguishes both themes and the two chat placement paths.

- [ ] **Step 1: Write exact source assertions**

The contract must assert all of these, using `Get-Content -Raw` and regex/substring checks:

```powershell
# Chat outer boundaries abut in both placement paths.
Require-Match 'Korean default chat abuts input' $gameScene 'ChatTextBox\.Location\.Y\s*-\s*ChatBox\.Size\.Height\s*\)'
Forbid-Match 'Korean default chat has legacy gap' $gameScene 'ChatTextBox\.Location\.Y\s*-\s*ChatBox\.Size\.Height\s*-\s*8'
Require-Match 'Korean dynamic chat abuts input' $koreanChat 'ChatTextBox\.Location\.Y\s*-\s*height\s*\)'
Forbid-Match 'Korean dynamic chat has legacy gap' $koreanChat 'ChatTextBox\.Location\.Y\s*-\s*height\s*-\s*8'

# One public type, two construction paths.
Require-Match 'Monster layout uses locked theme' $monster 'KoreanInterface[\s\S]{0,300}?(Build145|BuildKorean)'
Require-Match '145 original size' $monster 'new Size\(240,\s*120\)'
Require-Match '145 original portrait' $monster 'LibraryFile\.MonImg'
Require-Match 'Korean size retained' $monster 'new Size\(200,\s*160\)'
Require-Match 'Korean remains movable' $monster 'Movable\s*=\s*true'
Require-Match 'Korean content remains 70 percent' $monster 'Opacity\s*=\s*0\.7F'

# Theme-specific visibility behavior.
Require-Match 'Movement hide is Korean only' $gameScene 'KoreanInterface[\s\S]{0,220}?MirAction\.Moving[\s\S]{0,120}?MonsterBox\.Visible\s*=\s*false'
Require-Match '145 mouse-out clears monster' $gameScene '!KoreanInterface[\s\S]{0,500}?MonsterBox\.Monster\s*=\s*null'
```

- [ ] **Step 2: Run the focused contract before editing**

Run:

```powershell
$env:PC_DUAL_SOURCE = 'D:\相聚假人\Source'
powershell.exe -NoProfile -ExecutionPolicy Bypass -File 'C:\Users\chen\Documents\Codex\2026-08-08\mir3-pc-dual-ui-luna\work\pc-chat-gap-monster-theme-isolation-contract.ps1'
```

Expected: exit 1, identifying both `-8` gaps, missing 145 construction path, and unguarded Korean visibility behavior.

### Task 2: Remove only the Korean chat gap

**Files:**
- Modify: `D:\相聚假人\Source\145Client\Scenes\GameScene.cs`
- Modify: `D:\相聚假人\Source\145Client\Scenes\Views\ChatDialog.Korean.cs`
- Modify: `D:\相聚假人\Source\145Client\Scenes\Views\ChatTextBox.cs`

**Interfaces:**
- Consumes: existing `ChatBox`, `ChatTextBox`, and `ApplyKoreanChatSize()`.
- Produces: history bottom equals gold skin top; actual text input follows the skin; combined input layout remains immediately above MainPanel.

- [ ] **Step 1: Patch the two positions**

```csharp
// GameScene.SetDefaultLocations(), Korean branch
ChatBox.Location = new Point(MainPanel.Location.X,
    ChatTextBox.Location.Y - ChatBox.Size.Height);

// ChatDialog.Korean.ApplyKoreanChatSize()
Location = new Point(GameScene.Game.MainPanel.Location.X,
    GameScene.Game.ChatTextBox.Location.Y - height);
```

Do not change height arrays, row counts, opacity, scrollbar geometry, button indices, or hints.

- [ ] **Step 2: Apply the user-confirmed Korean input composition**

After the existing `SetClientSize(...)`, set only the Korean layout to:

```csharp
Size = new Size(400, 58);
Background.Location = Point.Empty;
ChatModeButton.Location = Point.Empty;
TextBox.Location = new Point(0, 38);
ChangeButton.Location = new Point(356, 0);
```

Keep `Background.Size = new Size(380, 38)` and `TextBox.Size = new Size(295, 20)`. `OnParentChanged()` continues to use `MainPanel.DisplayArea.Top - Size.Height`, so the 58px composition ends at the main panel top. Do not alter the 145 branch.

Set `Background.Sort = true` before the existing `Background.SendToBack()` so the skin is actually moved behind controls by `DXControl.SendToBack()`.

- [ ] **Step 3: Remove the internal two-pixel visual gap**

For each Korean chat height, extend the three internal regions exactly to the window bottom:

```csharp
KoreanTextBackground.Size = new Size(380, height - 27);
TextPanel.Size = new Size(350, height - 31);
ScrollBar.Size = new Size(16, height - 27);
```

Update their largest-state constructor sizes to 241, 237, and 241 respectively. Keep Y locations 27, 31, and 27 and preserve line-count arrays.

- [ ] **Step 4: Run the focused contract**

Run the Task 1 command. Expected: chat assertions pass; monster assertions remain RED.

### Task 3: Restore original 145 monster construction and isolate Korean construction

**Files:**
- Modify: `D:\相聚假人\Source\145Client\Scenes\Views\MonsterDialog.cs`
- Reference only: `D:\相聚\145Client\Scenes\Views\MonsterDialog.cs`

**Interfaces:**
- Consumes: `GameScene.Game.KoreanInterface`, `MonsterObject`, `BigPatchConfig.ChkMonsterInfo`, existing public labels and refresh methods.
- Produces: unchanged public class `MonsterDialog`, property `Monster`, and methods `RefreshHealth()` / `RefreshStats()`.

- [ ] **Step 1: Add a locked theme field and split layout construction**

```csharp
private readonly bool KoreanInterface;

public MonsterDialog()
{
    KoreanInterface = GameScene.Game.KoreanInterface;

    if (KoreanInterface)
        BuildKoreanInterface();
    else
        Build145Interface();
}
```

Move the current constructor body unchanged into `BuildKoreanInterface()`.

Within `BuildKoreanInterface()`, keep `DrawWindowTexture=false` and the gold `Border=true`, but set the outer `DrawTexture=false`; the existing 70%-opacity child content remains the single dark background layer.

- [ ] **Step 2: Restore the 145 layout from the read-only baseline**

Create `Build145Interface()` by transplanting the original constructor layout from `D:\相聚\145Client\Scenes\Views\MonsterDialog.cs:75` through the end of that constructor. Preserve its exact controls, resources, coordinates, sizes, opacity, `Movable=false`, portrait rendering and resistance layout. Adapt only direct compile differences caused by the current public field set; do not redesign or restyle it.

The required invariant begins with:

```csharp
HasTitle = false;
HasFooter = false;
HasTopBorder = false;
TitleLabel.Visible = false;
CloseButton.Visible = false;
Opacity = 0F;
Border = false;
Movable = false;
Size = new Size(240, 120);
```

- [ ] **Step 3: Isolate monster-change positioning**

```csharp
if (KoreanInterface)
{
    if (!MonsterLocationInitialized)
    {
        Location = new Point((GameScene.Game.Size.Width - Size.Width) / 2, 10);
        MonsterLocationInitialized = true;
    }
}
else
{
    Location = new Point(GameScene.Game.ChatBox.Photo.DisplayArea.Location.X,
        GameScene.Game.ChatBox.Photo.DisplayArea.Location.Y - 5);
}
```

For 145, keep the original name handling and do not require the Korean-only level display if the original control is absent/hidden. Guard only members that are genuinely absent in one layout.

- [ ] **Step 4: Preserve shared refresh semantics**

Ensure `RefreshHealth()` and `RefreshStats()` work with both layouts. `UpdateHealthBar()` may remain a no-op when the Korean `HealthTrack` is absent only if the 145 original `panel.AfterDraw` health rendering is retained. Do not change stat values, element selection, resistance formatting, or packet handling.

- [ ] **Step 5: Run the focused contract**

Run the Task 1 command. Expected: monster layout assertions pass; GameScene behavior assertion may remain RED until Task 4.

### Task 4: Restore 145 visibility behavior and retain Korean behavior

**Files:**
- Modify: `D:\相聚假人\Source\145Client\Scenes\GameScene.cs`
- Reference only: `D:\相聚\145Client\Scenes\GameScene.cs:1974-1983`

**Interfaces:**
- Consumes: `KoreanInterface`, `mob`, `FocusObject`, `MonsterBox`.
- Produces: explicit mutually exclusive behavior branches.

- [ ] **Step 1: Branch the existing block by locked theme**

```csharp
if (KoreanInterface)
{
    // Retain current Korean behavior exactly:
    // Moving/Pushed hides; stationary mouse/focus monster restores;
    // mouse-out does not clear Monster.
}
else if (mob != null && mob.CompanionObject == null)
{
    MonsterBox.Monster = mob;
}
else
{
    mob = FocusObject as MonsterObject;
    MonsterBox.Monster = null;
}
```

The Korean branch must retain the explicit same-instance visibility restore. The 145 branch must not use movement hiding or mouse-out persistence.

- [ ] **Step 2: Run the focused and existing source contracts**

Run the focused contract, then every existing `*.ps1` source contract in the work directory except `config-reader-contract.ps1`. Expected: all exit 0. If an old contract encodes the superseded shared behavior, update only its assertion to require Korean guarding; do not weaken unrelated checks.

### Task 5: Primary verification, Release build, deploy, and log

**Files:**
- Modify after acceptance: `D:\相聚假人\Source\CHANGELOG.md`
- Build output: `D:\Client\Mir3.exe`
- Deploy: `D:\Debug\4月18日更新\Client\Mir3.exe`

**Interfaces:**
- Consumes: Luna implementation result.
- Produces: independently verified Release executable and update record.

- [ ] **Step 1: Inspect actual source differences**

Compare the three production source files against the state recorded before delegation. Confirm no unrelated formatting or behavior changed.

- [ ] **Step 2: Run all source contracts**

```powershell
$env:PC_DUAL_SOURCE = 'D:\相聚假人\Source'
Get-ChildItem 'C:\Users\chen\Documents\Codex\2026-08-08\mir3-pc-dual-ui-luna\work' -Filter '*.ps1' |
    Where-Object Name -ne 'config-reader-contract.ps1' |
    ForEach-Object { powershell.exe -NoProfile -ExecutionPolicy Bypass -File $_.FullName; if ($LASTEXITCODE) { throw $_.Name } }
```

Expected: every contract exits 0.

- [ ] **Step 3: Release Rebuild**

```powershell
& 'C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\MSBuild\Current\Bin\MSBuild.exe' `
  'D:\相聚假人\Source\145Client\145Client.csproj' /t:Rebuild /m /v:minimal `
  /p:Configuration=Release /p:Platform=AnyCPU
```

Expected: 0 errors; report all warnings and SHA-256 of `D:\Client\Mir3.exe`.

- [ ] **Step 4: Verify config reader against build output**

```powershell
$env:PC_DUAL_OUTPUT = 'D:\Client'
powershell.exe -NoProfile -ExecutionPolicy Bypass -File 'C:\Users\chen\Documents\Codex\2026-08-08\mir3-pc-dual-ui-luna\work\config-reader-contract.ps1'
```

Expected: exit 0.

- [ ] **Step 5: Deploy only the executable**

Record target `Mir3.ini` SHA-256, verify no running `Mir3` process, copy `D:\Client\Mir3.exe` over the deployed executable without creating another backup, then verify executable hashes match and `Mir3.ini` hash is unchanged.

- [ ] **Step 6: Update the changelog**

Add one entry describing the two corrections, exact changed source files, Release evidence, deployment hash, and the remaining Direct3D manual validation gap.
