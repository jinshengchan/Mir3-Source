# Bot AI CPU and Potion Scan Optimization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remove duplicate low-MP potion scans from combat casting and throttle failed non-emergency potion scans without weakening emergency healing.

**Architecture:** Keep the independent 200ms potion timer as the sole normal low-HP/low-MP trigger. Reuse `_botPotionCooldownTime` as an 800ms pre-scan reservation for non-emergency checks, then overwrite it with the actual item cooldown after successful use. Preserve HP<=15% emergency bypass and all map/skill semantics.

**Tech Stack:** C# 7.2, .NET Framework 4.8, PowerShell focused source contracts, VS 2022 Build Tools.

## Global Constraints

- Shared non-Git tree: preserve unrelated edits and compare SHA-256 hashes.
- Use the same GPT-5.6 Luna / Max task for implementation.
- RED must run before production edits; GREEN and regressions run afterward.
- Build Debug/AnyCPU only to `.build-check/bot-ai-cpu-potion-debug/Server/`.
- Do not deploy, back up, edit databases/configuration, or modify ServerLibrary source.
- Do not change the level-40 map threshold, assassin skill priority, 200ms potion timer, emergency HP<=15% bypass, potion scoring, buying quantities, or economy support.

---

### Task 1: Add the focused failing contract

**Files:**
- Create: `.diagnostics/bot-ai-cpu-potion-contract.ps1`
- Inspect: `Server/BotManager.Support.cs`
- Inspect: `Server/BotManager.Combat.cs`

**Interfaces:**
- Consumes: `ProcessBotPotionMonitor(PlayerObject, bool)` and both generic combat casting helpers.
- Produces: one focused command whose output states assertion counts and exits nonzero on either regression.

- [ ] **Step 1: Write assertions for the approved behavior**

The contract must extract complete method blocks and prove:

```text
ProcessBotPotionMonitor defines an 800ms non-emergency retry interval.
The non-emergency cooldown reservation occurs before TryUseBestBotPotion.
HP<=BotPotionEmergencyHpPct bypasses the reservation/cooldown gate.
Successful potion use still overwrites _botPotionCooldownTime with potionCooldownMs.
TryCastBotMagic does not call ProcessBotPotionMonitor when MP is insufficient.
TryCastBotMagicWithPredicton does not call ProcessBotPotionMonitor when MP is insufficient.
TryProcessBotRangedCombatAction contains no direct potion-monitor call.
BotPotionTick still calls ProcessBotPotionModule and the timer remains 200ms.
The level-40 map switch and four assassin selectors remain present.
```

- [ ] **Step 2: Run RED before any production edit**

Run:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .diagnostics\bot-ai-cpu-potion-contract.ps1
```

Expected: nonzero exit with failures naming the missing 800ms pre-scan reservation and the two generic casting helpers that still invoke `ProcessBotPotionMonitor`.

### Task 2: Implement the non-emergency scan reservation

**Files:**
- Modify: `Server/BotManager.Support.cs:68-117`

**Interfaces:**
- Consumes: existing `_botPotionCooldownTime`, `BotPotionEmergencyHpPct`, and successful-use `potionCooldownMs`.
- Produces: `private const int BotPotionRetryIntervalMs = 800` and a pre-scan reservation for non-emergency checks.

- [ ] **Step 1: Add the single constant next to potion timing constants**

```csharp
private const int BotPotionRetryIntervalMs = 800;
```

- [ ] **Step 2: Reserve the next non-emergency check before inventory work**

After the existing non-emergency cooldown check and before `TryUseBestBotPotion`, set:

```csharp
_botPotionCooldownTime[pid] = now.AddMilliseconds(BotPotionRetryIntervalMs);
```

Do not execute this reservation for HP<=15% emergency checks. Keep the successful-use assignment based on `potionCooldownMs` unchanged.

### Task 3: Remove duplicate low-MP potion calls from generic casting

**Files:**
- Modify: `Server/BotManager.Combat.cs:2570-2584`
- Modify: the complete `TryCastBotMagicWithPredicton` method around `Server/BotManager.Combat.cs:2930-2942`

**Interfaces:**
- Consumes: independent `BotPotionTick` normal potion monitoring.
- Produces: both helpers return `false` immediately when `magic.Cost > player.CurrentMP`.

- [ ] **Step 1: Simplify both low-MP branches**

Use the minimal behavior:

```csharp
if (magic.Cost > player.CurrentMP)
    return false;
```

Do not change other call sites, emergency potion calls, target handling, cooldowns, action queues, or skill selection.

### Task 4: Verify, document, and build Debug

**Files:**
- Modify: `CHANGELOG.md`
- Verify only: `.diagnostics/bot-ai-phase1-contract.ps1`
- Verify only: `.diagnostics/bot-ai-level40-assassin-contract.ps1`

**Interfaces:**
- Produces: contract evidence, isolated Debug binaries, SHA-256 hashes, and explicit runtime gap.

- [ ] **Step 1: Run focused GREEN**

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .diagnostics\bot-ai-cpu-potion-contract.ps1
```

Expected: all focused assertions pass.

- [ ] **Step 2: Run both regressions**

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .diagnostics\bot-ai-phase1-contract.ps1
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .diagnostics\bot-ai-level40-assassin-contract.ps1
```

Expected: `21 assertions` and `6 assertions` pass.

- [ ] **Step 3: Build Debug/AnyCPU in isolation**

```powershell
dotnet build ServerLibrary\ServerLibrary.csproj -c Debug --nologo
& 'C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\MSBuild\Current\Bin\MSBuild.exe' Server\Server.csproj /t:Rebuild /m /v:minimal /p:Configuration=Debug /p:Platform=AnyCPU '/p:OutputPath=D:\相聚假人\Source\.build-check\bot-ai-cpu-potion-debug\Server\'
```

Expected: both commands exit 0; report warnings exactly and never copy the output to a deployment directory.

- [ ] **Step 4: Update changelog and final evidence**

Record RED/GREEN counts, regression counts, Debug build result, isolated artifact path/hash, unchanged deployed old Server.exe hash, and the remaining same-load five-minute A/B runtime check.

- [ ] **Step 5: Non-Git scope and placeholder review**

Compare owned-file hashes, confirm existing regression-contract hashes are unchanged, run the standard placeholder scan over the plan/spec, and report no commit/PR/deploy.
