# PC Equipment Compare Panel Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the vertically appended PC inventory equipment comparison with a separate right-hand panel whose equipped-stat rows show their difference inline.

**Architecture:** Keep the existing `ItemLabel` as the left tooltip and add one top-level `EquipmentCompareLabel` managed by `GameScene`. Reuse existing slot resolution and stat aggregation, but render each equipped stat and its signed difference as two labels on the same row.

**Tech Stack:** C#, .NET Framework/MSBuild, existing `DXControl`/`DXLabel` UI framework, PowerShell contract test.

## Global Constraints

- Modify only the PC client comparison implementation in `145Client\Scenes\GameScene.cs` plus diagnostics and changelog.
- Do not change the server, packets, Android client, resources, or existing item dragging/selection behavior.
- Rings and bracelets compare both left and right slots.
- Back up only the executable that will be overwritten; do not create a new delivery directory.

---

### Task 1: Contract for an independent inline-difference panel

**Files:**
- Modify: `.diagnostics/test_pc_equipment_compare_contract.ps1`
- Test: `.diagnostics/test_pc_equipment_compare_contract.ps1`

**Interfaces:**
- Consumes: `GameScene.CreateEquipmentCompareInfo()` and the existing comparison helpers.
- Produces: checks for `EquipmentCompareLabel`, independent creation/drawing/disposal, and inline stat-row rendering.

- [ ] **Step 1: Update the contract test**

Require the source to contain `EquipmentCompareLabel`, `CreateEquipmentCompareStatRow`, `EquipmentCompareLabel.Draw()`, and same-row difference positioning; reject the old `Parent = ItemLabel` comparison helper.

- [ ] **Step 2: Run the contract test and verify RED**

Run: `powershell.exe -NoProfile -ExecutionPolicy Bypass -File .diagnostics\test_pc_equipment_compare_contract.ps1`

Expected: failure because the current implementation appends comparison labels to `ItemLabel`.

### Task 2: Implement the right-hand comparison panel

**Files:**
- Modify: `145Client/Scenes/GameScene.cs`

**Interfaces:**
- Consumes: `Functions.CorrectSlot(ItemType, EquipmentSlot)`, `GetEquipmentStats(ClientUserItem)`, `Stats.GetDisplay(Stat)`.
- Produces: `EquipmentCompareLabel`, `CreateEquipmentCompareStatRow(Stats, Stats, ItemInfo)`, and `GetEquipmentDifferenceText(Stats, Stat)`.

- [ ] **Step 1: Add lifecycle handling**

Declare `EquipmentCompareLabel` beside `ItemLabel`; dispose it when the hovered item changes, a cell is selected, or the scene is disposed.

- [ ] **Step 2: Render an independent panel**

Create `EquipmentCompareLabel` with the same background/border palette as the existing tooltip. Add the slot heading, equipped item name, `属性`/`属性差值` columns, and one row per visible stat.

- [ ] **Step 3: Render differences inline**

For each visible equipped-stat row, place the signed difference label to its right. Use green for positive, red for negative, yellow for mixed range changes, and omit zero differences.

- [ ] **Step 4: Position and draw both panels as a group**

Clamp the combined width and maximum height to the game scene; place `EquipmentCompareLabel` immediately to the right of `ItemLabel` and draw both top-level controls.

- [ ] **Step 5: Run the contract test and verify GREEN**

Run: `powershell.exe -NoProfile -ExecutionPolicy Bypass -File .diagnostics\test_pc_equipment_compare_contract.ps1`

Expected: `PC equipment comparison contract passed`.

### Task 3: Build, deliver, and document

**Files:**
- Modify: `CHANGELOG.md`
- Generate: `D:\相聚假人\客户端\Mir3.exe`
- Back up/replace: `D:\Debug\4月18日更新\Client\Mir3.exe`

**Interfaces:**
- Consumes: completed PC client source.
- Produces: verified PC executable and rollback backup.

- [ ] **Step 1: Compile PC Debug**

Run MSBuild for `145Client\145Client.csproj` with `Configuration=Debug` and `Platform=AnyCPU`.

Expected: exit code `0`; only the pre-existing `ChkLockMonEffect` warning may remain.

- [ ] **Step 2: Back up and replace the executable**

Copy the current target executable to a timestamped `.bak-20260806-equipment-compare-panel` file, then copy the new `Mir3.exe` into the existing Client directory.

- [ ] **Step 3: Verify the delivery hash**

Compute SHA-256 for the build output and delivered executable; require exact equality.

- [ ] **Step 4: Update the changelog**

Record the independent right panel, inline difference layout, modified files, build result, executable hash, and backup path.

- [ ] **Step 5: Manual acceptance**

Launch the PC client, open the inventory, hover ordinary equipment and ring/bracelet items, then confirm the two-column layout and correct green/red/yellow values.

Repository note: `D:\相聚假人\Source` is not a Git repository, so commit steps are intentionally omitted.
