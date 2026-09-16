# PC Korean Chat Input Area Size Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Expand the Korean text-entry background to `(48,5), 308x28` without moving its surrounding buttons or changing 145 UI behavior.

**Architecture:** Change only the Korean `inputSize` and Korean-local `TextBox.Location` expressions in `ChatTextBox.cs`. Protect the exact geometry and unchanged 145 branch with a focused PowerShell source contract.

**Tech Stack:** C#/.NET Framework 4.8, WinForms/SharpDX client, PowerShell source contracts, VS 2022 MSBuild.

## Global Constraints

- Korean `TextBox`: exact local location `(48,5)`, exact size `308x28`.
- Keep `ChatTextBox` at `400x38`, `ChatModeButton` at `(0,0)`, and `ChangeButton` at `(356,0)`.
- Keep the 145 input size `560x20` and non-Korean placement unchanged.
- Do not modify Fody, csproj, dependencies, debug symbols, resources, or Mir3.ini.
- Do not create backups before runtime acceptance; non-Git workspace, no commit or PR.

---

### Task 1: Focused input-area geometry contract

**Files:**
- Create: `C:\Users\chen\Documents\Codex\2026-08-08\mir3-pc-dual-ui-luna\work\pc-korean-chat-input-area-size-contract.ps1`
- Inspect: `D:\相聚假人\Source\145Client\Scenes\Views\ChatTextBox.cs`

**Interfaces:**
- Consumes: Korean constructor geometry and existing non-Korean branch.
- Produces: exact assertions for `(48,5)`, `308x28`, unchanged `400x38`, `(0,0)`, `(356,0)`, and `560x20`.

- [ ] **Step 1: Write and run the focused contract before code changes**

Expected: RED only because the source still contains Korean `(60,8)` and `295x20`.

### Task 2: Minimum Korean-only source change

**Files:**
- Modify: `D:\相聚假人\Source\145Client\Scenes\Views\ChatTextBox.cs`

**Interfaces:**
- Produces: Korean input size `new Size(308, 28)` and local position `new Point(48, 5)`.

- [ ] **Step 1: Change the conditional Korean input size**

Replace only the Korean side of `korean ? new Size(295, 20) : new Size(560, 20)` with `new Size(308, 28)`.

- [ ] **Step 2: Change the Korean-local input position**

Replace only `TextBox.Location = new Point(60, 8)` with `TextBox.Location = new Point(48, 5)`.

- [ ] **Step 3: Run focused and complete source contracts**

Expected: focused GREEN and every non-`config-reader-contract.ps1` contract GREEN. Update only stale assertions directly superseded by the new input geometry.

- [ ] **Step 4: Return parent evidence**

Report exact changed files/lines, RED and GREEN evidence, complete contract count, and SHA-256. Do not build, deploy, edit CHANGELOG, back up files, or touch Fody/csproj/Mir3.ini.

