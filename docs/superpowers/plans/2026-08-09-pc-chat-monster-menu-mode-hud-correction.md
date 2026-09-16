# PC Chat, Monster, Menu, and Mode HUD Correction Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use the approved Sol Advisor Luna task lane to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remove the remaining Korean chat-input shadow, add the chat-mode tooltip, rebuild the monster hover panel in the approved compact movable style, complete the Korean main menu, and show attack/pet modes on the Korean `IP` row.

**Architecture:** Keep every existing business entry point and network/data flow. Apply view-only changes in the three existing PC view files, use one external source contract for RED/GREEN, and update only obsolete assertions in two existing external contracts. Do not add a skin framework, resource file, configuration key, or server/mobile code.

**Tech Stack:** C# / .NET Framework 4.8, WinForms, SharpDX Direct3D9, existing `DXWindow`/`DXControl`/`DXButton` controls, VS 2022 Build Tools MSBuild, PowerShell source contracts.

## Global Constraints

- Approved design: `docs/superpowers/specs/2026-08-09-pc-chat-monster-menu-mode-hud-correction-design.md` with SHA-256 `39AAAC995E2F1FB2FC74409728393534B571F029ABEDD0101C22E88F41647473`.
- Production edits are limited to `ChatTextBox.cs`, `MonsterDialog.cs`, and `MainPanel.Korean.cs`, unless the Release build proves one direct caller requires a compile-only adaptation.
- Do not modify `.ZL`, `Mir3.ini`, server, mobile, network configuration, shared controls, the 145 main-interface layout, or unrelated formatting.
- Preserve current chat cycle, target/hover assignment, health/stat data flow, mode-change packets, observer guards, and existing window instances.
- Per the user's latest instruction, do not create another source, deployed executable, or `CHANGELOG.md` backup before Direct3D acceptance. Preserve all existing backups.
- The Luna worker must not deploy or edit `CHANGELOG.md`; the primary task owns independent verification, deployment, log update, and acceptance.
- The source tree is non-Git. Do not initialize Git, create commits, branches, or PRs.

---

### Task 1: Establish the focused RED contract

**Files:**
- Create: `C:/Users/chen/Documents/Codex/2026-08-08/mir3-pc-dual-ui-luna/work/pc-chat-monster-menu-mode-hud-correction-contract.ps1`
- Read: `145Client/Scenes/Views/ChatTextBox.cs`
- Read: `145Client/Scenes/Views/MonsterDialog.cs`
- Read: `145Client/Scenes/Views/MainPanel.Korean.cs`

**Interfaces:**
- Consumes: `PC_DUAL_SOURCE` environment variable, falling back to `D:\相聚假人\Source`.
- Produces: exit `1` with named missing requirements before production edits; exit `0` and one `GREEN:` line after all four UI corrections exist.

- [ ] **Step 1: Write the contract before any production edit**

The contract must read the three production files and independently require these exact behaviors:

```powershell
Require-Match 'Korean 3503 is shifted up eight pixels' $chatText 'Background\.Location\s*=\s*new\s+Point\(0,\s*-8\)'
Require-Match '3503 keeps its full source height for clipping' $chatText 'Index\s*=\s*3503[\s\S]{0,220}?Size\s*=\s*new\s+Size\(380,\s*38\)'
Require-Match 'Triangle follows cropped row' $chatText 'ChangeButton\.Location\s*=\s*new\s+Point\(356,\s*0\)'
Require-Match 'Chat mode tooltip' $chatText 'ChatModeButton\.Hint\s*=\s*"切换聊天"\.Lang\(\)'

Require-Match 'Compact monster size' $monster 'Size\s*=\s*new\s+Size\(200,\s*160\)'
Require-Match 'Monster remains movable' $monster 'Movable\s*=\s*true'
Require-Match 'Monster position initializes once' $monster 'bool\s+MonsterLocationInitialized[\s\S]*?if\s*\(\s*!MonsterLocationInitialized\s*\)'
Require-Match 'Monster level is displayed' $monster 'Monster\.MonsterInfo\.Level'
Require-Match 'Four combat ranges are populated' $monster 'GetFormat\(Stat\.MaxAC\)[\s\S]*GetFormat\(Stat\.MaxMR\)[\s\S]*GetFormat\(Stat\.MaxDC\)[\s\S]*GetFormat\(Stat\.MaxMC\)'
Require-Match 'Eight resistances remain populated' $monster 'PhysicalResistance[\s\S]*FireResistance[\s\S]*IceResistance[\s\S]*LightningResistance[\s\S]*WindResistance[\s\S]*HolyResistance[\s\S]*DarkResistance[\s\S]*PhantomResistance'

Require-Match 'Menu title' $mainPanel 'Text\s*=\s*"主菜单"\.Lang\(\)'
Require-Match 'Rate query action' $mainPanel 'RateQueryShowCheck[\s\S]*RateQueryBox\.Visible'
Require-Match 'Assistant action' $mainPanel 'BigPatchBox\.Visible'
Require-Absent 'Mentor menu is removed' $mainPanel '"师徒信息"'
Require-MenuLabels $mainPanel @('环境设置','队伍信息','爆率查询','玛法排行榜','宠物状态','辅助设置','结束游戏')
Require-Match 'Korean attack mode label is visible' $mainPanel 'AttackModeLabel\s*=\s*CreateKoreanLabel\(new\s+Point\(35,\s*46\),\s*new\s+Size\(115,\s*16\)\)'
Require-Match 'Korean pet mode label is visible' $mainPanel 'PetModeLabel\s*=\s*CreateKoreanLabel\(new\s+Point\(150,\s*46\),\s*new\s+Size\(105,\s*16\)\)'
```

`Require-MenuLabels` must search each exact quoted string separately; it must not pass merely because seven calls exist.

- [ ] **Step 2: Run RED**

```powershell
$env:PC_DUAL_SOURCE = 'D:\相聚假人\Source'
powershell.exe -NoProfile -ExecutionPolicy Bypass -File 'C:\Users\chen\Documents\Codex\2026-08-08\mir3-pc-dual-ui-luna\work\pc-chat-monster-menu-mode-hud-correction-contract.ps1'
```

Expected: exit `1`. The output must name the current top-crop/y=8 chat layout, missing tooltip, 310×85 monster layout with unconditional recentering, missing runtime menu labels/actions, and hidden Korean mode labels. A parser or missing-file error is not an acceptable RED.

---

### Task 2: Correct the Korean input crop and chat-mode tooltip

**Files:**
- Modify: `145Client/Scenes/Views/ChatTextBox.cs:151-236`
- Test: `C:/Users/chen/Documents/Codex/2026-08-08/mir3-pc-dual-ui-luna/work/pc-chat-monster-menu-mode-hud-correction-contract.ps1`

**Interfaces:**
- Consumes: existing `GameInter/3503` 380×38 input asset, `GameInter/3542` and `3552` triangle assets, and `CycleKoreanChatSize()`.
- Produces: one clipped Korean input layer, an aligned independent triangle button, and the exact shared chat-mode tooltip.

- [ ] **Step 1: Add the shared tooltip**

In the existing `ChatModeButton` initializer add only:

```csharp
Hint = "切换聊天".Lang(),
```

Keep the existing click handler that advances `ChatMode`; do not add a second handler.

- [ ] **Step 2: Use the full 3503 texture as a clipped child**

Change the Korean `Background` geometry to:

```csharp
Size = new Size(380, 38),
FixedSize = true,
```

After layout, set:

```csharp
Background.Location = new Point(0, -8);
ChangeButton.Location = new Point(356, 0);
ChangeButton.BringToFront();
```

The parent control supplies clipping. Preserve `LibraryFile.GameInter`, `Index=3503`, `ImageOpacity=0.7F`, `DrawWindowTexture=false`, the existing `TextBox`, and the triangle click handler.

- [ ] **Step 3: Run the focused contract**

Run the Task 1 command. Expected: chat requirements pass; the overall contract remains RED only for monster/menu/mode-label requirements.

---

### Task 3: Recompose `MonsterDialog` as the compact movable panel

**Files:**
- Modify: `145Client/Scenes/Views/MonsterDialog.cs`
- Test: focused contract from Task 1

**Interfaces:**
- Consumes: existing `Monster` property, `GameScene.Game.DataDictionary`, `MonsterInfo.Stats`, `Stats.GetFormat`, `PopulateLabel`, `RefreshHealth`, `RefreshStats`, and `GameInter/1517,1520-1526` icons.
- Produces: the same `MonsterDialog` instance and public refresh methods with a 200×160 compact view and session-persistent dragged location.

- [ ] **Step 1: Make location initialization one-shot**

Add a private field:

```csharp
private bool MonsterLocationInitialized;
```

Replace unconditional recentering in `OnMonsterChanged` with:

```csharp
if (!MonsterLocationInitialized)
{
    Location = new Point((GameScene.Game.Size.Width - Size.Width) / 2, 10);
    MonsterLocationInitialized = true;
}
```

Keep `Movable=true`. Do not save this position to configuration.

- [ ] **Step 2: Build only the approved compact visual hierarchy**

Set the root size to `new Size(200, 160)`. The visible panel must use a dark, approximately 80%-opaque background, gold/brown border, and pass mouse input to the movable window. Do not draw the old portrait or its four auxiliary status glyphs.

Create or reuse controls at these bounded regions:

```text
Level:        x=6..30,   y=4..21
Name:         x=34..190, y=4..21
Affinity:     x=8..28,   y=30..50
HP border:    x=38..188, y=31..47
Combat rows:  y=58 and y=78, two columns
Resists:      four cells at y=104 and four cells at y=130
```

Each resistance cell consists of its existing icon plus a short numeric label. Use the current font, white values, gold captions, and red HP fill. No close button or portrait is required.

- [ ] **Step 3: Populate all approved data from one selected `Stats` source**

In `RefreshStats()` select data once:

```csharp
ClientObjectData data;
GameScene.Game.DataDictionary.TryGetValue(Monster.ObjectID, out data);
Stats stats = data?.Stats ?? Monster.MonsterInfo.Stats;

LevelLabel.Text = Monster.MonsterInfo.Level.ToString();
HealthLabel.Text = data == null ? string.Empty : $"{Math.Max(0, data.Health)} / {data.MaxHealth}";
ACLabel.Text = stats.GetFormat(Stat.MaxAC);
MRLabel.Text = stats.GetFormat(Stat.MaxMR);
DCLabel.Text = stats.GetFormat(Stat.MaxDC);
MCLabel.Text = stats.GetFormat(Stat.MaxMC);
```

Call `PopulateLabel` for `PhysicalResistance`, `FireResistance`, `IceResistance`, `LightningResistance`, `WindResistance`, `HolyResistance`, `DarkResistance`, and `PhantomResistance`. Retain the existing affinity switch, but make it use the selected `stats` object.

- [ ] **Step 4: Keep health rendering live**

The red HP fill must recompute from `DataDictionary` during drawing and clamp the fraction to `[0,1]`, so `RefreshHealth()` text updates and ordinary health packets continue to work without a new timer or network request.

- [ ] **Step 5: Dispose only newly owned references**

Add cleanup for newly introduced `MCLabel`, health controls, or persistent panel references using the file's existing `IsDisposed` pattern. Do not alter unrelated disposal paths.

- [ ] **Step 6: Run the focused contract**

Expected: chat and monster requirements pass; the contract remains RED only for the Korean main-menu and mode-label requirements.

---

### Task 4: Complete the Korean main menu and `IP` mode row

**Files:**
- Modify: `145Client/Scenes/Views/MainPanel.Korean.cs:91-117,301-351`
- Test: focused contract from Task 1

**Interfaces:**
- Consumes: `GameScene.Game.ConfigBox`, `GroupBox`, `RateQueryBox`, `RankingBox`, `CompanionBox`, `BigPatchBox`, `ShowExitDialog()`, `CEnvir.ClientControl.RateQueryShowCheck`, and existing `AttackModeChanged()`/`PetModeChanged()` assignments.
- Produces: two visible mode labels and one seven-button Korean menu with existing business actions.

- [ ] **Step 1: Expose attack and pet mode labels on the `IP` row**

Replace the two hidden empty labels with:

```csharp
AttackModeLabel = CreateKoreanLabel(new Point(35, 46), new Size(115, 16));
PetModeLabel = CreateKoreanLabel(new Point(150, 46), new Size(105, 16));
AttackModeLabel.ForeColour = Color.Cyan;
PetModeLabel.ForeColour = Color.Cyan;
```

Do not add click handlers. Existing `GameScene.AttackModeChanged()` and `PetModeChanged()` remain the sole text update path.

- [ ] **Step 2: Add the menu title and resize only as needed**

Use a centered `DXLabel` with exact text `"主菜单".Lang()`, gold foreground, bold current UI font, and black outline. Keep the existing Korean close-button asset and place it frontmost at the right edge. Increase the menu height only enough for title plus seven 26-pixel buttons and margins; the existing GameScene anchor will continue to place it above the main panel.

- [ ] **Step 3: Replace baked-text menu assets with uniform runtime-label buttons**

Change `CreateMenuButton` to create a standard `ButtonType.Default` button with size `100×26`, `Label.Visible=true`, centered label text, and the existing `Hint`. Create seven calls at 29-pixel vertical intervals below the title:

```csharp
CreateMenuButton(y0 + 0 * 29, "环境设置", ...);
CreateMenuButton(y0 + 1 * 29, "队伍信息", ...);
CreateMenuButton(y0 + 2 * 29, "爆率查询", ...);
CreateMenuButton(y0 + 3 * 29, "玛法排行榜", ...);
CreateMenuButton(y0 + 4 * 29, "宠物状态", ...);
CreateMenuButton(y0 + 5 * 29, "辅助设置", ...);
CreateMenuButton(y0 + 6 * 29, "结束游戏", ...);
```

Do not retain `"师徒信息"` or its mentor-chat click handler.

- [ ] **Step 4: Wire only existing actions**

Use these exact action rules:

```csharp
// 爆率查询
if (CEnvir.ClientControl.RateQueryShowCheck)
    GameScene.Game.RateQueryBox.Visible = !GameScene.Game.RateQueryBox.Visible;

// 辅助设置
if (!GameScene.Game.Observer && GameScene.Game.BigPatchBox != null)
    GameScene.Game.BigPatchBox.Visible = !GameScene.Game.BigPatchBox.Visible;
```

Preserve the existing actions and guards for environment, group, ranking, companion, and exit.

- [ ] **Step 5: Run focused GREEN**

Run the Task 1 command. Expected: exit `0` and `GREEN: PC chat/monster/menu/mode HUD correction contract passed.`

---

### Task 5: Reconcile and rerun regression contracts

**Files:**
- Modify only obsolete assertions in: `C:/Users/chen/Documents/Codex/2026-08-08/mir3-pc-dual-ui-luna/work/pc-korean-chat-composite-control-dedup-contract.ps1`
- Modify only obsolete assertions in: `C:/Users/chen/Documents/Codex/2026-08-08/mir3-pc-dual-ui-luna/work/pc-korean-original-ui-contract.ps1`
- Test: all listed PowerShell contracts

**Interfaces:**
- Consumes: the approved new 3503 crop geometry and runtime-label Korean menu.
- Produces: regression contracts that reject the old shadow/menu behavior without weakening unrelated 145, HUD, chat, experience, and resource assertions.

- [ ] **Step 1: Update only the two obsolete assertions**

- In `pc-korean-chat-composite-control-dedup-contract.ps1`, replace the old `Size(380,25)` / `(356,8)` expectation with `Size(380,38)`, background `(0,-8)`, and triangle `(356,0)` while retaining the `3503`, `0.7F`, single-button, frontmost, dynamic-index, and hint assertions.
- In `pc-korean-original-ui-contract.ps1`, replace the requirement for menu indices `460,465,470,475,480,485` with exact assertions for the title, seven runtime labels, `RateQueryBox`, `BigPatchBox`, and absence of `师徒信息`. Keep all other asset, HUD, chat, 145 compatibility, minimap, and hero-item assertions unchanged.

- [ ] **Step 2: Run the full regression set**

```powershell
$env:PC_DUAL_SOURCE = 'D:\相聚假人\Source'
$work = 'C:\Users\chen\Documents\Codex\2026-08-08\mir3-pc-dual-ui-luna\work'
$tests = @(
  'pc-chat-monster-menu-mode-hud-correction-contract.ps1',
  'pc-korean-chat-composite-control-dedup-contract.ps1',
  'pc-korean-chat-freeze-opacity-single-input-contract.ps1',
  'pc-korean-chat-single-layer-scroll-contract.ps1',
  'pc-korean-experience-hover-contract.ps1',
  'pc-korean-chat-resize-cycle-contract.ps1',
  'pc-korean-original-ui-contract.ps1',
  'korean-core-hud-contract.ps1',
  'pc-dual-ui-contract.ps1'
)
foreach ($test in $tests) {
  & powershell.exe -NoProfile -ExecutionPolicy Bypass -File (Join-Path $work $test)
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}
```

Expected: all nine contracts exit `0` and print `GREEN`.

---

### Task 6: Release build and Luna handoff

**Files:**
- Build input: `145Client/145Client.csproj`
- Build output: `.build-check/pc-chat-monster-menu-mode-hud-correction-luna/`
- Do not modify: `CHANGELOG.md`, deployed client, or `Mir3.ini`

**Interfaces:**
- Consumes: accepted production source and nine GREEN contracts.
- Produces: a Release `Mir3.exe` plus exact diff, build, and remaining manual-test evidence for the primary task.

- [ ] **Step 1: Run Release Rebuild**

```powershell
& 'C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\MSBuild\Current\Bin\MSBuild.exe' `
  'D:\相聚假人\Source\145Client\145Client.csproj' `
  /t:Rebuild /m /v:minimal /p:Configuration=Release /p:Platform=AnyCPU `
  /p:OutDir='D:\相聚假人\Source\.build-check\pc-chat-monster-menu-mode-hud-correction-luna\'
```

Expected: exit `0`, 0 errors. Report all warnings; the existing `CS0649 BigPatchConfig.ChkLockMonEffect` warning is allowed.

- [ ] **Step 2: Rerun all nine contracts after the build**

Run Task 5 Step 2 again. Expected: all GREEN after the final production state.

- [ ] **Step 3: Return structured evidence**

Return:

- Actual changed production files and concise behavior-level diff.
- RED command and named expected failures from before edits.
- Nine final GREEN results.
- Exact MSBuild command, exit code, warnings, artifact path, byte size, last-write time, and SHA-256.
- Confirmation that no new backups were created and existing backups were not changed.
- Confirmation that `.ZL`, `Mir3.ini`, `CHANGELOG.md`, deployed client, server, mobile, and unrelated sources were not written.
- Explicit Direct3D gaps: chat shadow/tooltip, monster appearance/drag retention, seven menu actions/title, and both `IP` mode labels.

Do not deploy, update the changelog, start/stop the client, or claim visual acceptance.

---

## Primary-task acceptance and deployment

After Luna completes, the primary task must:

1. Inspect complete diffs of the three production files and external contract changes.
2. Confirm no other production source or resource changed.
3. Independently rerun all nine contracts.
4. Independently Release Rebuild to a new parent output directory.
5. Check whether the deployed `Mir3.exe` is running; do not terminate it without permission.
6. Per the user's current instruction, do not create another deployment or changelog backup before visual acceptance.
7. Deploy only the independently built `Mir3.exe`, verify source/target SHA-256 equality, and verify `Mir3.ini` hash is unchanged.
8. Append a `CHANGELOG.md` entry with root causes, exact files, tests, build/deploy hash, no-repeat-backup decision, and pending Direct3D validation.
9. Ask the user to verify all four visual/interactive behaviors before marking the correction fully complete.
