# PC Korean Chat Input Bottom Alignment Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Move the Korean chat composite down by 18 pixels and move its text-entry background right so it begins after the chat-mode button.

**Architecture:** Preserve the existing Korean composite and resize state machine. Change only the Korean placement formulas in `GameScene.cs` and `ChatTextBox.cs`, plus the Korean-local `TextBox` X coordinate; keep all 145 branches untouched.

**Tech Stack:** C#/.NET Framework 4.8, WinForms/SharpDX client, PowerShell source contracts, VS 2022 MSBuild.

## Global Constraints

- Minimal source-only geometry change; no resource edits and no unrelated formatting.
- Korean composite vertical offset is exactly `+18px` from its current main-panel anchor.
- Korean text-entry local position is exactly `(60,8)`; size remains `295x20`.
- Do not change the 145 interface, resize cycle, Enter behavior, triangle assets, or `Mir3.ini`.
- The workspace is non-Git; do not create commits, branches, or PRs.
- Do not create another backup before formal runtime acceptance.

---

### Task 1: Add a focused geometry contract

**Files:**
- Create: `C:\Users\chen\Documents\Codex\2026-08-08\mir3-pc-dual-ui-luna\work\pc-korean-chat-input-bottom-align-contract.ps1`
- Inspect: `D:\相聚假人\Source\145Client\Scenes\GameScene.cs`
- Inspect: `D:\相聚假人\Source\145Client\Scenes\Views\ChatTextBox.cs`

**Interfaces:**
- Consumes: `GameScene.SetSceneSize`, `ChatTextBox.OnParentChanged`, and the Korean constructor branch.
- Produces: a source contract that rejects missing `+18` Korean placement, missing `(60,8)`, changes to `295x20`, or removal of the existing non-Korean paths.

- [ ] **Step 1: Write the focused PowerShell contract**

Assert the Korean layout contains the exact main-panel anchor plus `18`, the parent-change anchor plus `18`, and `TextBox.Location = new Point(60, 8)`. Also assert the existing `295x20` input size and the non-Korean placement branch remain present.

- [ ] **Step 2: Run the focused contract before production edits**

Run with process-scoped execution-policy bypass and `PC_DUAL_SOURCE=D:\相聚假人\Source`.

Expected: nonzero exit with RED findings for the absent `+18` placement and `(60,8)` coordinate.

### Task 2: Apply the minimum Korean-only geometry change

**Files:**
- Modify: `D:\相聚假人\Source\145Client\Scenes\GameScene.cs` in the Korean layout branch.
- Modify: `D:\相聚假人\Source\145Client\Scenes\Views\ChatTextBox.cs` in the Korean constructor branch and `OnParentChanged` Korean guard.

**Interfaces:**
- Consumes: `MainPanel.Location`, `MainPanel.DisplayArea.Top`, and `ChatTextBox.Size.Height`.
- Produces: stable Korean chat placement at the current anchor plus `18px`; text entry at `(60,8)`.

- [ ] **Step 1: Change only the Korean scene layout formula**

Use `MainPanel.Location.Y - ChatTextBox.Size.Height + 18` while retaining the existing X coordinate and subsequent `ChatBox` anchoring.

- [ ] **Step 2: Change the Korean initial parent-placement formula**

Use `MainPanel.DisplayArea.Top - Size.Height + 18` inside the existing Korean-only guard.

- [ ] **Step 3: Move only the Korean text-entry control right**

Change `TextBox.Location` from `new Point(2, 8)` to `new Point(60, 8)`. Do not move `ChatModeButton` or `ChangeButton` locally and do not change sizes.

- [ ] **Step 4: Run the focused contract**

Expected: exit zero and GREEN.

### Task 3: Synchronize stale contracts and verify the client

**Files:**
- Modify only stale coordinate assertions under `C:\Users\chen\Documents\Codex\2026-08-08\mir3-pc-dual-ui-luna\work\*.ps1` when they directly conflict with the new approved geometry.
- Modify: `D:\相聚假人\Source\CHANGELOG.md` after parent acceptance and deployment.

**Interfaces:**
- Consumes: all PC dual-interface source contracts and `config-reader-contract.ps1`.
- Produces: verified Release `Mir3.exe` without modifying `Mir3.ini`.

- [ ] **Step 1: Run all PC dual-interface source contracts**

Expected: every source contract exits successfully; no old `(2,8)` Korean input assertion remains.

- [ ] **Step 2: Rebuild Release/AnyCPU**

Run VS 2022 Build Tools MSBuild against `D:\相聚假人\Source\145Client\145Client.csproj` with `/t:Rebuild /p:Configuration=Release /p:Platform=AnyCPU`.

Expected: zero errors; report any warnings without hiding them.

- [ ] **Step 3: Run the configuration round-trip contract**

Set `PC_DUAL_OUTPUT=D:\Client` and run `config-reader-contract.ps1`.

Expected: GREEN with `GameInterface=Korean` preserved and no derived property persisted.

- [ ] **Step 4: Return evidence to the primary task**

Report exact changed files, before/after source snippets, focused RED/GREEN output, full-contract count, build output path, file size and SHA-256. Do not deploy, edit `CHANGELOG.md`, create a backup, or touch `Mir3.ini`; those remain primary-owned.

