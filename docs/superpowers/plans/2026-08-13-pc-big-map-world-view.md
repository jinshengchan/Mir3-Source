# PC Big Map World View Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make both the Korean and 145 PC interfaces use the Korean-style large-map window, opening on the current map and switching to the built-in world map on demand.

**Architecture:** Extend the existing shared `BigMapDialog` with two display states rather than creating interface-specific dialogs. Reuse `WorldMap.Zl` for the world image, keep the current `MiniMap.Zl` rendering and pathfinding untouched, and resolve map-name searches against the existing `Globals.MapInfoList` data.

**Tech Stack:** .NET Framework 4.8, WinForms/SharpDX custom controls, PowerShell contract tests, MSBuild Release build.

## Global Constraints

- Both Korean and 145 interfaces must use the same behavior and layout.
- Opening the large map defaults to the current map and preserves existing click pathfinding.
- `全部地图` switches to the Korean world map; `当前位置` switches back to the current map.
- Search input is a map name; a unique/first matching map switches to that map's current-map view.
- Reuse the existing `Data/WorldMap.Zl`; do not copy or modify resource packages.
- Do not change the minimap, server, map database, or unrelated dual-interface code.
- Update `CHANGELOG.md`; do not deploy or create repeated backups before visual acceptance.

---

### Task 1: Lock the big-map behavior contract

**Files:**
- Create: `.diagnostics/test_pc_big_map_world_view_contract.ps1`

**Interfaces:**
- Consumes: `145Client/Scenes/Views/BigMapDialog.cs`
- Produces: a focused RED/GREEN contract for the shared two-state map window

- [ ] **Step 1: Write the failing contract test**

Assert that the source contains a world-map state, `WorldMap` index usage, `全部地图` and `当前位置` buttons, map-name matching through `Globals.MapInfoList`, and retains the existing `InitCurrentPath` call.

- [ ] **Step 2: Run the test to verify RED**

Run: `powershell -ExecutionPolicy Bypass -File .diagnostics/test_pc_big_map_world_view_contract.ps1`

Expected: FAIL because the current dialog has no world-map state, buttons, or map-name search.

### Task 2: Implement the shared Korean-style large-map window

**Files:**
- Modify: `145Client/Scenes/Views/BigMapDialog.cs`

**Interfaces:**
- Consumes: `MapInfo.MiniMap`, `Globals.MapInfoList`, `LibraryFile.WorldMap`, existing `Image_MouseClick`
- Produces: `ShowCurrentMap()`, `ShowWorldMap()`, and map-name search behavior inside the shared dialog

- [ ] **Step 1: Add the minimum controls and state**

Add one world-map image control, one search text box, one search button, and the two mode buttons. Keep controls in the existing dialog so both UI modes instantiate the same implementation.

- [ ] **Step 2: Preserve current-map behavior**

Opening and `当前位置` must set `SelectedInfo` to `GameScene.Game.MapControl.MapInfo`, restore existing markers, scaling, and click pathfinding.

- [ ] **Step 3: Add world-map mode**

`全部地图` must hide current-map overlays and show the built-in 770x415 world map without modifying `SelectedInfo` pathfinding rules.

- [ ] **Step 4: Add map-name search**

Trim the entered text, match `MapInfo.Description` case-insensitively, prefer exact match before partial match, and switch to the matched map view. Empty or unmatched text must not corrupt the current display state.

- [ ] **Step 5: Run the contract to verify GREEN**

Run: `powershell -ExecutionPolicy Bypass -File .diagnostics/test_pc_big_map_world_view_contract.ps1`

Expected: PASS.

### Task 3: Build and document

**Files:**
- Modify: `CHANGELOG.md`

**Interfaces:**
- Consumes: completed source and contract test
- Produces: a Release-buildable client change with traceable history

- [ ] **Step 1: Rebuild the PC client**

Run: `& 'C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\MSBuild\Current\Bin\MSBuild.exe' 'D:\相聚假人\Source\145Client\145Client.csproj' /t:Rebuild /m /v:minimal /p:Configuration=Release /p:Platform=AnyCPU`

Expected: exit code 0 and no errors.

- [ ] **Step 2: Re-run the focused contract**

Run: `powershell -ExecutionPolicy Bypass -File .diagnostics/test_pc_big_map_world_view_contract.ps1`

Expected: PASS after the Release build.

- [ ] **Step 3: Update the changelog**

Record the shared Korean/145 large-map layout, default current-map behavior, world-map switching, map-name search, resource reuse, and verification result.

## Self-Review

- Spec coverage: both UI modes, default current map, original pathfinding, world-map switch, return button, and map-name search are all assigned to Task 2.
- Scope: only one production source file is modified; no resource, minimap, server, or database change is planned.
- Acceptance gap: automated contract and Release build cannot prove final Direct3D placement; an in-game screenshot remains required before deployment.
