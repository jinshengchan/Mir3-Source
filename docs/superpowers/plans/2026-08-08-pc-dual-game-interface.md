# PC Dual Game Interface Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use Sol Advisor's explicitly authorized GPT-5.6 Luna / Max task lane to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a login-time “145界面／韩版界面” selection, persist it to `Mir3.ini`, and construct exactly one matching PC in-game interface, with the Korean theme using the same built-in artwork and 1024×768 composition shown in the approved reference image.

**Architecture:** Keep all network, model, command, hotkey, drag/drop, and inventory logic shared. Add one persisted theme value and a small theme-query seam; each affected view chooses a 145 or Korean construction path before creating child controls. Use existing `GameInter.Zl`, `GameInter2.Zl`, `Interface.Zl`, and only visually verified matching entries from other built-in libraries; never globally remap `UI1.Zl` to `UI2.Zl`.

**Tech Stack:** C#/.NET Framework 4.8, WinForms, SharpDX Direct3D9, MirLibrary `.Zl` resources, VS 2022 Build Tools MSBuild.

## Global Constraints

- The current 145 interface is the compatibility baseline and must remain unchanged when the new setting is absent or invalid.
- Korean 1024×768 layout and artwork must match `C:\Users\chen\AppData\Local\Temp\codex-clipboard-c5add74c-87c1-4962-96fc-d2a1dd310d41.png`.
- Select only at login; apply on the next `GameScene` construction. No in-game hot swapping.
- Reuse existing business logic and event handlers. Theme code owns only resources, control construction, sizes, positions, anchors, and visibility composition.
- Do not modify the server or Android clients.
- Before changing an existing source or deployment file, create a sibling timestamped `.bak-20260808-pc-dual-ui` backup. Do not overwrite existing backups.
- The checkout is not a Git repository. Replace commit steps with changed-file manifests, SHA-256 evidence, and saved before/after diffs.
- Update root `CHANGELOG.md` after source, resources, build, and deployment are verified.

---

### Task 1: Persisted theme value and login selector

**Files:**
- Modify: `145Client/Envir/Config.cs`
- Modify: `145Client/Scenes/LoginScene.cs`
- Reference: `Library/ConfigReader.cs`

**Interfaces:**
- Produces: `Config.GameInterface` with canonical values `145` and `Korean`.
- Produces: two mutually exclusive login controls labelled `145界面` and `韩版界面`.
- Consumes: existing `ConfigReader.Load()` and `ConfigReader.Save()`.

- [ ] **Step 1: Back up both owned source files**

```powershell
Copy-Item -LiteralPath '145Client\Envir\Config.cs' -Destination '145Client\Envir\Config.cs.bak-20260808-pc-dual-ui'
Copy-Item -LiteralPath '145Client\Scenes\LoginScene.cs' -Destination '145Client\Scenes\LoginScene.cs.bak-20260808-pc-dual-ui'
```

Expected: both backups exist and have the same SHA-256 as their originals before editing.

- [ ] **Step 2: Add the minimal persisted setting**

Add one property under `[ConfigSection("Graphics")]`:

```csharp
public static string GameInterface { get; set; } = "145";

public static bool KoreanInterface => string.Equals(GameInterface, "Korean", StringComparison.OrdinalIgnoreCase);
```

Normalize any missing, empty, or unknown value to `145` before the game scene is created.

- [ ] **Step 3: Add login selector controls**

Create two mutually exclusive buttons in `LoginScene`, using already loaded login/common button artwork. Their labels are exactly `145界面` and `韩版界面`. Clicking a button must:

```csharp
Config.GameInterface = korean ? "Korean" : "145";
ConfigReader.Save();
RefreshInterfaceSelection();
```

The selected state must be visibly distinct without introducing a new external asset.

- [ ] **Step 4: Verify persistence without entering the game**

Run the client from a copied test directory, select each option, close normally, and inspect `Mir3.ini`.

Expected: only the chosen interface value changes; IP, port, resolution, and other settings retain their prior values.

---

### Task 2: Theme seam and built-in asset manifest

**Files:**
- Create: `145Client/Scenes/Views/GameInterfaceTheme.cs`
- Create: `docs/ui/pc-korean-interface-assets.md`
- Modify: `145Client/145Client.csproj`
- Reference: `Library/Libraries.cs`
- Reference assets: deployed `Data/GameInter.Zl`, `Data/GameInter2.Zl`, `Data/Interface.Zl`, `Data/UI1.Zl`, `Data/UI2.Zl`

**Interfaces:**
- Produces: `GameInterfaceTheme.IsKorean` and narrowly scoped helpers for selecting verified library/index pairs.
- Produces: an auditable resource manifest mapping each Korean visual role to library, index, size, and screenshot location.
- Consumes: `Config.KoreanInterface`.

- [ ] **Step 1: Back up the project file**

```powershell
Copy-Item -LiteralPath '145Client\145Client.csproj' -Destination '145Client\145Client.csproj.bak-20260808-pc-dual-ui'
```

- [ ] **Step 2: Build the asset manifest from actual library metadata and image inspection**

Use the existing `LibraryEditor`/`MirLibrary` reader to inspect candidate indices. Record one row per required role with these mandatory columns: visual role, exact `LibraryFile` value, exact numeric index, measured pixel width/height, consuming class, and a short statement of how it matches the approved screenshot.

Required roles: bottom status panel, HP/MP bars, experience/weight bars, chat frame/tabs/input, belt frame/cells, right menu background/buttons, minimap frame, character frame/tabs/equipment slots, inventory frame/grid/currency/buttons, common Korean window border/close button/tab/button.

Success: every source index is opened and visually matched to the approved screenshot; no row uses an assumed same-number mapping from `UI1.Zl` to `UI2.Zl`.

- [ ] **Step 3: Add the theme seam**

Implement a static, read-only theme query whose state comes from normalized config. Add only helpers that remove repeated conditionals for verified library/index pairs; do not introduce a general skin engine.

- [ ] **Step 4: Compile-check the new file inclusion**

Run:

```powershell
& 'C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\MSBuild\Current\Bin\MSBuild.exe' '145Client\145Client.csproj' /t:Build /m /v:minimal /p:Configuration=Debug /p:Platform=AnyCPU
```

Expected: 0 errors. Existing warnings may remain; no new warning may originate from `GameInterfaceTheme.cs`.

---

### Task 3: Korean core HUD, chat, belt, menu, and minimap layout

**Files:**
- Modify: `145Client/Scenes/Views/MainPanel.cs`
- Create: `145Client/Scenes/Views/MainPanel.Korean.cs`
- Modify: `145Client/Scenes/Views/ChatDialog.cs`
- Create: `145Client/Scenes/Views/ChatDialog.Korean.cs`
- Modify: `145Client/Scenes/Views/ChatTextBox.cs`
- Modify: `145Client/Scenes/Views/BeltDialog.cs`
- Modify: `145Client/Scenes/Views/MiniMapDialog.cs`
- Modify: `145Client/Scenes/GameScene.cs`
- Modify: `145Client/145Client.csproj`

**Interfaces:**
- Keeps: existing `GameScene.MainPanel`, `ChatBox`, `ChatTextBox`, `BeltBox`, and `MiniMapBox` field types and event consumers.
- Consumes: `GameInterfaceTheme.IsKorean` and the verified asset manifest.
- Produces: Korean 1024×768 HUD composition without constructing hidden 145 duplicates.

- [ ] **Step 1: Back up every existing owned source file before its first edit**

Use the exact `.bak-20260808-pc-dual-ui` suffix and verify hashes before editing.

- [ ] **Step 2: Split construction paths without duplicating business logic**

Convert only the affected view classes to `partial` where needed. Their constructors must select one build path before creating children:

```csharp
if (GameInterfaceTheme.IsKorean)
    BuildKoreanInterface();
else
    Build145Interface();
```

Move existing construction statements unchanged into the 145 path. Keep event bodies, data updates, hotkeys, drag/drop, and packet actions shared.

- [ ] **Step 3: Construct Korean HUD from verified artwork**

At 1024×768 match the reference composition: full-width bottom status panel, left chat/belt stack, right vertical menu, and top-right minimap. Preserve all current command targets, including inventory, character, magic, settings, group, guild, ranking, companion, mount, exit, and any currently exposed custom feature.

- [ ] **Step 4: Add resolution anchoring**

In `GameScene.SetDefaultLocations()`, branch only the coordinates and anchors. Korean bottom components anchor to `Size.Height`; right components anchor to `Size.Width`; artwork is not scaled. The existing 145 coordinate block remains behaviorally unchanged.

- [ ] **Step 5: Focused interaction test**

At 1024×768, verify every visible Korean menu button, chat tab/input/scroll, belt cell, and minimap button has a matching hitbox and triggers its existing behavior. Repeat the same checks in 145 mode to detect regression.

---

### Task 4: Korean character, inventory, and common window skin

**Files:**
- Modify: `145Client/Scenes/Views/CharacterDialog.cs`
- Create: `145Client/Scenes/Views/CharacterDialog.Korean.cs`
- Modify: `145Client/Scenes/Views/InventoryDialog.cs`
- Create: `145Client/Scenes/Views/InventoryDialog.Korean.cs`
- Modify: `145Client/Controls/DXWindow.cs`
- Modify: `145Client/145Client.csproj`

**Interfaces:**
- Keeps: existing `CharacterDialog` and `InventoryDialog` public fields/events consumed by `GameScene` and item logic.
- Keeps: 8×8 inventory, real scrollbar behavior, search/refresh controls, item tooltips, appearance preview, and equipment comparison.
- Produces: Korean window artwork and coordinates matching the reference.

- [ ] **Step 1: Back up all existing owned files**

Create and hash-check sibling `.bak-20260808-pc-dual-ui` copies.

- [ ] **Step 2: Add Korean character construction path**

Use the verified Korean frame, tabs, equipment-slot artwork, and model viewport positions. Bind the same cells and tab commands as the 145 view. Do not copy equipment/stat calculation code.

- [ ] **Step 3: Add Korean inventory construction path**

Use the verified Korean frame, 8×8 grid, scrollbar, weight/currency labels, close/refresh/search controls and hitboxes. Bind existing item cells and interactions; do not change inventory capacity or server data.

- [ ] **Step 4: Theme the shared window chrome narrowly**

In `DXWindow`, select Korean common border/close/tab/button artwork only when a window opts into the Korean common skin. Do not force fixed dimensions over custom windows and do not change 145 defaults.

- [ ] **Step 5: Regression test item and window behaviors**

In each theme verify: equip/unequip, item hover text, equipped-item comparison, appearance preview, inventory scrolling, search/refresh, drag/drop, closing/reopening, and window bounds at 1024×768.

---

### Task 5: Construction lock, fallback, and lifecycle verification

**Files:**
- Modify: `145Client/Scenes/LoadScene.cs`
- Modify: `145Client/Scenes/GameScene.cs`
- Modify: `145Client/Envir/CEnvir.cs` only if its existing logger is required for fallback reporting

**Interfaces:**
- Consumes: normalized `Config.GameInterface`.
- Produces: one immutable theme decision per `GameScene` instance.
- Produces: pre-construction fallback to 145 when required Korean assets are unavailable.

- [ ] **Step 1: Back up each file actually changed**

Use the required sibling backup suffix and hash verification.

- [ ] **Step 2: Validate Korean resources before `new GameScene(Config.GameSize)`**

At the start of `LoadScene.CreateGame()`, validate the exact manifest entries required by Korean core controls. If any required file/index/size is unavailable, set the normalized selection to 145 for that construction and write one diagnostic entry. Do not construct a partial Korean scene.

- [ ] **Step 3: Lock the theme for the scene lifetime**

Pass or snapshot the normalized value when constructing `GameScene`; all child constructors in that scene read the snapshot, not a mutable login control.

- [ ] **Step 4: Lifecycle tests**

For both themes: login, enter a character, exit to character selection, enter again, then close normally. Success: no black screen, duplicate controls, disposed-control access, stale hitbox, or missing texture error.

---

### Task 6: Build, deploy with backups, and changelog

**Files:**
- Modify: `CHANGELOG.md`
- Deploy: `D:\Debug\4月18日更新\Client\Mir3.exe`
- Deploy: any new Korean `.Zl` resource only if Task 2 proves an independent composed pack is necessary

**Interfaces:**
- Produces: a runnable PC client containing both interface choices.

- [ ] **Step 1: Capture source-change evidence**

Generate a list of changed source/resource files, compare each against its backup, and record before/after SHA-256 values. Exclude unrelated pre-existing changes.

- [ ] **Step 2: Rebuild the PC client**

```powershell
& 'C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\MSBuild\Current\Bin\MSBuild.exe' '145Client\145Client.csproj' /t:Rebuild /m /v:minimal /p:Configuration=Debug /p:Platform=AnyCPU
```

Expected: `Build succeeded`, 0 errors, and a newly timestamped `Mir3.exe`.

- [ ] **Step 3: Back up deployment targets**

Before replacing `Mir3.exe` or any existing resource, copy each target to a timestamped backup in the same client directory. Back up `Mir3.ini` before smoke tests because a normal client exit rewrites it.

- [ ] **Step 4: Deploy and smoke-test both modes**

Copy the verified build and any required new resource. Test 145 mode and Korean mode at 1024×768 using the same deployed directory. Compare Korean composition against the approved reference image and capture screenshots.

- [ ] **Step 5: Update the changelog**

Back up `CHANGELOG.md`, then record date/time, design and plan paths, every changed source/resource/deployment file, backups, build command/result, both-mode test results, and any known limitation. Do not claim pixel/interaction parity without actual runtime evidence.

- [ ] **Step 6: Final acceptance evidence**

Report: changed-file list, backup list, build summary, deployed artifact SHA-256, `Mir3.ini` keys for both selections, 145 regression result, Korean screenshot comparison, and unresolved gaps.
