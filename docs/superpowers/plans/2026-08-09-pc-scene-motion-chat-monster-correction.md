# PC Scene Motion, Chat Boundary, and Monster Info Correction Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Correct diagonal scenery-shadow flicker, Korean chat/input overlap, and monster-info movement/visual behavior with four surgical PC-client edits.

**Architecture:** Preserve existing render and UI composition. Adjust only the diagonal camera-offset invariant, Korean chat absolute spacing, and the existing monster-window update gate and visual constants.

**Tech Stack:** C#/.NET Framework, SharpDX Direct3D9, PowerShell static contracts, Visual Studio 2022 MSBuild.

## Global Constraints

- Modify only the four approved PC source files plus `CHANGELOG.md` after verification.
- Do not modify resources, `Mir3.ini`, server code, or mobile code.
- Do not create repeated backups before formal visual acceptance.
- Preserve 145-interface behavior and unrelated Korean-interface behavior.
- The source tree is non-Git; do not initialize Git or claim commits.

---

### Task 1: Add the RED/GREEN correction contract

**Files:**
- Create: `C:/Users/chen/Documents/Codex/2026-08-08/mir3-pc-dual-ui-luna/work/pc-scene-motion-chat-monster-contract.ps1`

**Interfaces:**
- Consumes: the four approved source files.
- Produces: one exit-code contract that identifies every requested invariant.

- [ ] **Step 1: Write assertions for the target source invariants**

Assert that diagonal movement is not excluded from even-pixel alignment, both Korean chat placement paths subtract 8px, movement gates monster assignment, content opacity is `0.7F`, and information fonts use `9F`.

- [ ] **Step 2: Run the contract before implementation**

Run:

```powershell
& 'C:\Users\chen\Documents\Codex\2026-08-08\mir3-pc-dual-ui-luna\work\pc-scene-motion-chat-monster-contract.ps1'
```

Expected: non-zero exit with failures for the not-yet-implemented invariants.

### Task 2: Correct diagonal scene offset

**Files:**
- Modify: `145Client/Models/UserObject.cs:1476-1500`

**Interfaces:**
- Consumes: calculated `x` and `y` movement offsets.
- Produces: even-valued `MovingOffSet.X/Y` for every movement direction.

- [ ] **Step 1: Replace the direction-limited parity switch**

Use the existing project expression for both coordinates:

```csharp
x -= x % 2;
y -= y % 2;
```

Keep the existing Mir2 correction and all frame/reversal logic unchanged.

- [ ] **Step 2: Run the focused contract**

Expected: the diagonal-offset assertion passes; unrelated assertions may remain RED until their tasks are complete.

### Task 3: Separate Korean chat history from the input composite

**Files:**
- Modify: `145Client/Scenes/GameScene.cs:1579`
- Modify: `145Client/Scenes/Views/ChatDialog.Korean.cs:210-212`

**Interfaces:**
- Consumes: `ChatTextBox.Location.Y`, current chat height.
- Produces: chat history top position with an exact 8px separation from the input control boundary.

- [ ] **Step 1: Adjust default Korean placement**

Set the default Y position to `ChatTextBox.Location.Y - ChatBox.Size.Height - 8`.

- [ ] **Step 2: Adjust resize-cycle placement**

Set the dynamic Y position to `ChatTextBox.Location.Y - height - 8`.

- [ ] **Step 3: Run the focused contract**

Expected: both chat-placement assertions pass and the existing resize-cycle contract remains GREEN.

### Task 4: Apply monster movement and visual rules

**Files:**
- Modify: `145Client/Scenes/GameScene.cs:2036-2071`
- Modify: `145Client/Scenes/Views/MonsterDialog.cs:95-105,191-247`

**Interfaces:**
- Consumes: `User.CurrentAction`, existing mouse/focus monster selection.
- Produces: hidden window while moving/pushed; original refresh behavior when stationary; 70% content background and 9F information fonts.

- [ ] **Step 1: Gate the existing monster assignment block**

When `User.CurrentAction` is `MirAction.Moving` or `MirAction.Pushed`, set `MonsterBox.Visible = false` and skip the existing assignment block for that frame. Otherwise run the existing selection block unchanged and ensure a valid current monster makes the window visible through its existing refresh path.

- [ ] **Step 2: Change only the requested visual constants**

Change the content background control from `Opacity = 0.85F` to `Opacity = 0.7F`. Change the three information-font factory uses from `CEnvir.FontSize(8F)` to `CEnvir.FontSize(9F)`. Keep the triangle button at 9F.

- [ ] **Step 3: Run the complete new contract**

Expected: exit code 0 and all new assertions GREEN.

### Task 5: Regression, build, and delivery evidence

**Files:**
- Modify after GREEN: `CHANGELOG.md`
- Build output: `145Client/bin/Release/Mir3.exe`
- Deploy after verification: `D:/Debug/4月18日更新/Client/Mir3.exe`

**Interfaces:**
- Consumes: completed source changes.
- Produces: verified Release client and traceable log entry.

- [ ] **Step 1: Run all existing UI contracts plus the new contract**

Expected: 10/10 scripts exit 0.

- [ ] **Step 2: Rebuild Release/AnyCPU**

```powershell
& 'C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\MSBuild\Current\Bin\MSBuild.exe' `
  'D:\相聚假人\Source\145Client\145Client.csproj' /t:Rebuild /m /v:minimal `
  /p:Configuration=Release /p:Platform=AnyCPU
```

Expected: 0 errors; record warnings, timestamp, size, and SHA-256.

- [ ] **Step 3: Inspect the actual four-file delta**

Verify every changed source line maps to the approved requirements and no resource/server/mobile/deployed config file changed.

- [ ] **Step 4: Update `CHANGELOG.md`**

Record source files, behavior, contract/build evidence, deployment hash, and the remaining Direct3D manual validation requirement.

- [ ] **Step 5: Deploy the verified executable without creating another backup**

Copy only the verified `Mir3.exe` over `D:/Debug/4月18日更新/Client/Mir3.exe`; do not touch `Mir3.ini`.

