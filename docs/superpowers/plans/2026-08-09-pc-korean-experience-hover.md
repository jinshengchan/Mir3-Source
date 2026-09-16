# PC Korean Experience Hover Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the Korean thin experience bar show `[经验] xx%` only while hovered, without adding permanent experience text or changing the 145 UI.

**Architecture:** Keep the existing `GameInter/51` frame and `/56` fill. Make only the Korean experience control mouse-addressable and branch the existing experience hint update by the scene's locked interface mode.

**Tech Stack:** C#/.NET Framework, existing DX controls, PowerShell source contracts, VS 2022 MSBuild.

## Global Constraints

- Modify only `MainPanel.Korean.cs` and the minimum Korean branch in `GameScene.ExperienceChanged()`.
- Keep `ExperienceLabel` hidden and keep `GameInter/51` plus `/56` unchanged.
- Korean hover text is exactly `[经验] {clamped percentage:0%}`; no-next-level fallback is 100%.
- Preserve the 145 experience hint statement and behavior exactly.
- No deployment, `Mir3.ini`, `.ZL`, server/mobile, minimap or unrelated HUD changes in the Luna task.
- Non-Git source tree: no commit, push or PR.

---

### Task 1: Korean experience hover target and percentage hint

**Files:**
- Modify: `145Client/Scenes/Views/MainPanel.Korean.cs`
- Modify: `145Client/Scenes/GameScene.cs`
- Test: `C:/Users/chen/Documents/Codex/2026-08-08/mir3-pc-dual-ui-luna/work/pc-korean-experience-hover-contract.ps1`

**Interfaces:**
- Consumes: `MainPanel.ExperienceBar`, `GameScene.KoreanInterface`, `User.Experience`, `User.MaxExperience`.
- Produces: Korean `ExperienceBar.Hint` text in exact `[经验] xx%` format.

- [ ] **Step 1: Create SHA-verified sibling backups**

Use unique suffix `.bak-20260809-pc-korean-experience-hover-01` for both owned source files; never overwrite an existing backup.

- [ ] **Step 2: Write and run a failing focused contract**

The contract must fail against the current source because the Korean experience bar is pass-through and because `ExperienceChanged()` has no Korean percentage branch. It must also assert that `ExperienceLabel` stays hidden and the 145 hint path remains present.

Run with `PC_DUAL_SOURCE=D:\相聚假人\Source`; expected RED exit `1`.

- [ ] **Step 3: Make the Korean experience bar hoverable**

In `BuildKoreanInterface()`, remove the experience bar's `PassThrough = true` assignment or set it to `false`. Do not change the background panel or other pass-through controls.

- [ ] **Step 4: Add the Korean-only percentage hint**

In `GameScene.ExperienceChanged()`, retain the existing 145 statement in its non-Korean branch. For Korean mode, calculate a clamped decimal percentage, using 100% when `User.MaxExperience <= 0`, and set:

```csharp
MainPanel.ExperienceBar.Hint = $"[经验] {percent:0%}";
```

Do not assign `MainPanel.ExperienceLabel.Text` and do not make that label visible.

- [ ] **Step 5: Run focused and regression contracts**

Expected GREEN for:

```text
pc-korean-experience-hover-contract.ps1
pc-korean-chat-resize-cycle-contract.ps1
pc-korean-original-ui-contract.ps1
korean-core-hud-contract.ps1
pc-dual-ui-contract.ps1
```

- [ ] **Step 6: Release rebuild and scope audit**

Rebuild `145Client/145Client.csproj` in Release with `/m:1 /nr:false /p:RestorePackages=false` to `D:\相聚假人\Source\.build-check\pc-korean-experience-hover-luna\`. Require 0 errors, report warnings, artifact size/hash, backup hashes and exact diff. Do not deploy or update `CHANGELOG.md`.
