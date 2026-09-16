# PC Korean Chat Single-Layer Opacity and Scrollbar Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remove the duplicate Korean chat footer shadow, make chat backgrounds 70% opaque, and reproduce the original Korean 3561/3562/3560 scrollbar geometry without changing shared 145 behavior.

**Architecture:** Keep the current `DXVScrollBar` value/events interface used by shared chat code. Add two opt-in geometry properties whose defaults preserve every existing scrollbar, enable them only in the Korean chat constructor, and make the existing four-level layout update the single message region and scrollbar from the same selected height.

**Tech Stack:** C#/.NET Framework, existing DX controls and GameInter assets, PowerShell contracts, VS 2022 MSBuild.

## Global Constraints

- Remove the Korean `GameInter/3502` internal footer; retain `ChatTextBox` `GameInter/3503` as the only bottom input background.
- Backgrounds use `0.7F` opacity; text, tabs, borders, buttons and scrollbar remain fully legible.
- Korean scrollbar art is exactly GameInter 3561 up, 3562 down and 3560 circular position bar.
- Korean scrollbar geometry uses position-bar X offset 2 and scroll-height padding 40, matching `DXMirScrollBar`.
- `DXVScrollBar` defaults remain X offset 0 and padding 50 so existing consumers are unchanged.
- Visible chat heights remain exactly 268, 218, 168 and 118, followed by hidden and restore-to-268.
- Preserve chat history, filtering, links, input, wheel, drag, arrows, four-level resize and experience-hover behavior.
- Do not modify 145 construction, minimap, server/mobile code, `Mir3.ini`, deployed files, `CHANGELOG.md` or `.ZL` resources in the Luna task.
- The source tree is non-Git; do not initialize Git, commit, push or create a PR.

---

### Task 1: Opt-in original Korean scrollbar geometry

**Files:**
- Modify: `145Client/Controls/DXVScrollBar.cs`
- Test: `C:/Users/chen/Documents/Codex/2026-08-08/mir3-pc-dual-ui-luna/work/pc-korean-chat-single-layer-scroll-contract.ps1`

**Interfaces:**
- Produces: `public int PositionBarOffsetX` with default `0`.
- Produces: `public int ScrollHeightPadding` with default `50`.
- Preserves: existing `Value`, `MaxValue`, `MinValue`, `VisibleSize`, `Change`, `SetSkin()` and events.

- [ ] **Step 1: Back up the control source**

Create `DXVScrollBar.cs.bak-20260809-pc-korean-chat-single-layer-scroll-01` beside the source and verify its SHA-256 equals the unmodified file. If it exists, use suffix `-02`; never overwrite.

- [ ] **Step 2: Write the failing control contract and capture RED**

The external contract must require explicit opt-in properties with unchanged defaults, require every position-bar X calculation to use the offset, and require the effective scroll height to use the configurable padding. It must fail current source with exit `1`.

- [ ] **Step 3: Add only the two geometry parameters**

Use the following public defaults near the existing `Change` field:

```csharp
public int PositionBarOffsetX;
public int ScrollHeightPadding = 50;
```

Change the private calculation to:

```csharp
private int ScrollHeight => Size.Height - ScrollHeightPadding;
```

In `UpdateScrollBar()` and `PositionBar_Moving()`, use:

```csharp
new Point(UpButton.Location.X + PositionBarOffsetX, calculatedY)
```

Do not alter default button images, enabling rules, value clamping, mouse-wheel behavior or other controls.

- [ ] **Step 4: Run the control portion of the focused contract GREEN**

Expected: offset/padding/default-preservation assertions pass before changing Korean chat construction.

---

### Task 2: Single-layer Korean chat background and original scrollbar skin

**Files:**
- Modify: `145Client/Scenes/Views/ChatDialog.Korean.cs`
- Modify: `145Client/Scenes/Views/ChatTextBox.cs`
- Test: `C:/Users/chen/Documents/Codex/2026-08-08/mir3-pc-dual-ui-luna/work/pc-korean-chat-single-layer-scroll-contract.ps1`

**Interfaces:**
- Consumes: `DXVScrollBar.PositionBarOffsetX`, `DXVScrollBar.ScrollHeightPadding` from Task 1.
- Preserves: `CycleKoreanChatSize()` and visible heights 268/218/168/118.
- Produces: one visible Korean footer/input background, `ChatTextBox.Background` at GameInter/3503.

- [ ] **Step 1: Back up both Korean chat source files**

Create SHA-verified siblings using suffix `.bak-20260809-pc-korean-chat-single-layer-scroll-01`; if present use `-02`. Never overwrite.

- [ ] **Step 2: Extend the focused contract and capture Korean RED**

Require all of the following before production edits:

```powershell
# ChatDialog.Korean.cs has no KoreanInputPanel field/construction/reference.
# ChatDialog.Korean.cs does not construct GameInter index 3502.
# ChatTextBox retains GameInter index 3503 as the sole input background.
# ChatPanel.ImageOpacity, KoreanTextBackground.Opacity and ChatTextBox Background.ImageOpacity are 0.7F.
# ScrollBar SetSkin remains GameInter/-1/3561/3562/3560.
# Korean ScrollBar sets PositionBarOffsetX=2 and ScrollHeightPadding=40.
# Four visible heights remain 268/218/168/118.
# Per-level TextPanel and ScrollBar extend to the chat bottom instead of reserving 20 pixels for the removed footer.
```

Expected current source: exit `1` for duplicate 3502, `0.3F` opacity, missing original geometry options and reserved footer space.

- [ ] **Step 3: Remove the internal 3502 footer**

Delete the Korean-only `KoreanInputPanel` field, construction and all visibility/location references. Do not remove `BigChatPanel`/`BigChatPanelBackground` compatibility fields unless independently proven unused by shared disposal; keep them hidden as before.

- [ ] **Step 4: Set 70% background opacity only**

Use:

```csharp
ChatPanel.ImageOpacity = 0.7F;
KoreanTextBackground.Opacity = 0.7F;
Background.ImageOpacity = 0.7F; // Korean ChatTextBox branch
```

Do not change parent window opacity or message/control opacity.

- [ ] **Step 5: Configure the exact Korean scrollbar style**

Keep:

```csharp
ScrollBar.SetSkin(LibraryFile.GameInter, -1, 3561, 3562, 3560);
```

Then configure only this instance:

```csharp
ScrollBar.PositionBarOffsetX = 2;
ScrollBar.ScrollHeightPadding = 40;
ScrollBar.UpButton.Location = new Point(0, 2);
```

Ensure the current `OnSizeChanged()` continues to place the down arrow at the bottom and all position-bar updates retain X offset 2.

- [ ] **Step 6: Extend content and scrollbar to the bottom**

In the centralized Korean layout, derive all dimensions from `height`:

```csharp
KoreanTextBackground.Location = new Point(0, 48);
KoreanTextBackground.Size = new Size(380, height - 48);
TextPanel.Location = new Point(8, 52);
TextPanel.Size = new Size(350, height - 53);
ScrollBar.Location = new Point(360, 48);
ScrollBar.Size = new Size(16, height - 49);
LineCount = Math.Max(1, TextPanel.Size.Height / 15);
ScrollBar.VisibleSize = LineCount;
```

This yields visible rows 14, 11, 7 and 4 for heights 268, 218, 168 and 118. Preserve bottom anchoring and hidden/up-triangle synchronization.

- [ ] **Step 7: Run the complete focused contract GREEN**

Expected: `GREEN: Korean single-layer opacity/scrollbar contract passed.`

- [ ] **Step 8: Run all regression contracts**

Run with `PC_DUAL_SOURCE=D:\相聚假人\Source`:

```text
pc-korean-chat-single-layer-scroll-contract.ps1
pc-korean-experience-hover-contract.ps1
pc-korean-chat-resize-cycle-contract.ps1
pc-korean-original-ui-contract.ps1
korean-core-hud-contract.ps1
pc-dual-ui-contract.ps1
```

Expected: all GREEN, exit `0`. Update obsolete test expectations only where the approved single-layer geometry intentionally changes them; retain all existing coverage.

- [ ] **Step 9: Release rebuild**

Run:

```powershell
& 'C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\MSBuild\Current\Bin\MSBuild.exe' `
  'D:\相聚假人\Source\145Client\145Client.csproj' `
  /t:Rebuild /m:1 /nr:false /v:minimal `
  /p:Configuration=Release /p:Platform=AnyCPU `
  /p:OutputPath='D:\相聚假人\Source\.build-check\pc-korean-chat-single-layer-scroll-luna\' `
  /p:RestorePackages=false
```

Expected: exit `0`, 0 errors. Report warnings, artifact size and SHA-256.

- [ ] **Step 10: Scope and backup audit**

Compare the three changed source files against their new backups. Confirm the default `DXVScrollBar` path is unchanged and no 145 construction, experience-hover source, minimap, server/mobile, resource archive, deployed client, `Mir3.ini` or `CHANGELOG.md` changed. Report real Direct3D shadow, opacity and drag behavior as manual verification gaps.
