# Bot AI Taoist and Wizard Combat Priority Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:test-driven-development to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make Taoist bots use offensive talisman and melee skills before basic attacks, and make Wizard bots select area attacks when at least three attackable monsters are nearby.

**Architecture:** Keep execution in the existing server C# combat pipeline. Pass the real nearby-monster count into the existing skill selector, reuse its readiness/damage/MP checks, and adjust only the Wizard/Taoist close-range fallback so a failed reposition does not cancel an otherwise legal cast.

**Tech Stack:** C# 7.2, .NET Framework 4.8, PowerShell 5.1 static contracts, MSBuild 17 / Debug / AnyCPU (project target x64).

## Global Constraints

- Work in the shared non-Git tree `D:\相聚假人\Source`; preserve concurrent and unrelated edits.
- Production ownership is limited to `Server\BotSkillSelector.cs` and `Server\BotManager.Combat.cs`.
- Test ownership is limited to the new `.diagnostics\bot-ai-taoist-wizard-combat-priority-contract.ps1`.
- Do not modify existing contracts, skill learning, supplies, potion logic, maps, economy, other professions, clients, databases, Python strategy files, or changelog.
- Do not deploy, overwrite, stop, start, or otherwise touch the user's currently running old `Server.exe`.
- Use a three-monster threshold. Fewer than three attackable monsters remains single-target behavior.
- No production edit is allowed until the new focused contract has been run and failed for the expected missing behavior.
- Current production base hashes before this task:
  - `Server\BotSkillSelector.cs`: `7539FC83A3CEDC4D947EA84C343CEABB9D249C051D881B400C9F7B76165F3AB3`
  - `Server\BotManager.Combat.cs`: `E8E03CDFF296468FF045E78656F6AD94D80A4A69C834B8DCACB1A67D9614FA21`

---

### Task 1: Add the focused RED contract

**Files:**
- Create: `.diagnostics\bot-ai-taoist-wizard-combat-priority-contract.ps1`
- Read: `Server\BotSkillSelector.cs`
- Read: `Server\BotManager.Combat.cs`

**Interfaces:**
- Consumes: the existing method names `GetWizardRangedMagic`, `GetTaoistRangedMagic`, `SelectTalismanAttack`, `ProcessBotWizardCombatAction`, `ProcessBotTaoistCombatAction`, and `TryProcessBotRangedCombatAction`.
- Produces: a deterministic PowerShell contract whose process exit code is 1 before implementation and 0 after implementation.

- [ ] **Step 1: Create the contract using the existing brace-balanced `Get-MethodBlock` and `Assert-Contract` helpers**

The assertions must directly encode these behaviors:

```powershell
Assert-Contract ($wizardSelector -match 'int\s+nearbyMobCount') 'Wizard selector consumes nearby monster count'
Assert-Contract ($wizardSelector -match 'nearbyMobCount\s*>=\s*3') 'Wizard enables area selection at three monsters'
Assert-Contract ($wizardSelector -notmatch 'false\s*,\s*1\s*\)') 'Wizard damage selection does not hard-code single target'
Assert-Contract ($wizardCombat -match 'CountNearbyAttackableMonsters[\s\S]*?GetWizardRangedMagic\s*\([^\)]*nearbyMobCount') 'Wizard combat forwards nearby monster count'

Assert-Contract ($talismanSelector -match 'int\s+nearbyMobCount') 'Talisman selector consumes nearby monster count'
Assert-Contract ($talismanSelector -notmatch 'false\s*,\s*1\s*\)') 'Talisman damage selection does not hard-code single target'
Assert-Contract ($taoistCombat -match 'GetTaoistMeleeAttackMagic\s*\([^\)]*nearbyMobCount') 'Taoist uses melee magic before basic fallback'
Assert-Contract ($selectorSource -match 'GetTaoistMeleeAttackMagic[\s\S]*?TaoistMeleePriority') 'Taoist melee priority is connected'

Assert-Contract ($rangedAction -match 'TryRepositionBotForPreferredRange[\s\S]*?TryCastBotMagic') 'Failed preferred-range reposition can continue to casting'
Assert-Contract ($rangedAction -notmatch 'TryRepositionBotForPreferredRange[\s\S]*?return\s+false;[\s\S]*?TryCastBotMagic') 'Failed reposition does not force premature physical fallback'
```

Also assert that the threshold remains exactly three, the Assassin exclusion in the shared ranged branch remains, and the Taoist order in `ProcessBotTaoistCombatAction` is ranged attempt → melee selector → `ProcessBotMeleeCombatAction`.

- [ ] **Step 2: Run the contract and verify genuine RED**

Run:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File ".\.diagnostics\bot-ai-taoist-wizard-combat-priority-contract.ps1"
```

Expected: exit code 1. Failures must specifically include the current Wizard hard-coded single-target path and the missing Taoist melee connection. A parse error, missing file, or unrelated hash failure is not an acceptable RED.

- [ ] **Step 3: Record RED output before touching production files**

Record the exact assertion totals and failed assertion names in the Luna handoff. Do not edit either production file until this evidence exists.

---

### Task 2: Implement the minimum selector and combat changes

**Files:**
- Modify: `Server\BotSkillSelector.cs:112-219,424-653`
- Modify: `Server\BotManager.Combat.cs:2380-2422,3016-3048`
- Test: `.diagnostics\bot-ai-taoist-wizard-combat-priority-contract.ps1`

**Interfaces:**
- Produces: `GetWizardRangedMagic(PlayerObject player, MapObject target, int nearbyMobCount)`.
- Produces: `SelectTalismanAttack(PlayerObject player, MapObject target, int nearbyMobCount)`.
- Produces: `GetTaoistMeleeAttackMagic(PlayerObject player, MapObject target, int nearbyMobCount)`.
- Preserves: `TryProcessBotRangedCombatAction(PlayerObject, MapObject, int, MirDirection, MagicType)` and all external combat dispatch signatures.

- [ ] **Step 1: Make Wizard selection count-aware**

In `GetWizardRangedMagic`, derive the mode once and pass the real count through existing damage selection:

```csharp
bool isAreaAttack = nearbyMobCount >= 3;
IEnumerable<MagicType> candidates = isAreaAttack ? WizardAdaptiveFallback : WizardRangedPriority;
MagicType bestSkill = SelectHighestDamageSkill(player, target, candidates, isAreaAttack, nearbyMobCount);
```

Keep the existing monster-resistance fallback. Set its area filter to `!isAreaAttack`; use the existing single-target rotating fallback below three monsters and an existing all-ready rotating path for the area candidate list at three or more. Do not invent a new scheduler, cache, timer, or skill list.

- [ ] **Step 2: Pass Wizard's real nearby count from combat**

At the beginning of `ProcessBotWizardCombatAction`, compute:

```csharp
int nearbyMobCount = BotSkillSelector.CountNearbyAttackableMonsters(player, player.CurrentLocation, 2);
```

Pass it to `GetWizardRangedMagic(player, target, nearbyMobCount)`. Preserve the current final ordinary-attack fallback when no spell is usable.

- [ ] **Step 3: Make Taoist talisman selection count-aware**

Change every `SelectTalismanAttack(player, target)` call in the Taoist attack selectors to pass `nearbyMobCount`. Inside `SelectTalismanAttack`, use `nearbyMobCount >= 3` as the area flag and pass the real count to `SelectHighestDamageSkill`; choose from the existing Taoist offensive candidates so the already-defined group talisman skills are eligible only in area mode. Preserve amulet availability, readiness, MP, and resistance checks.

- [ ] **Step 4: Connect Taoist melee skill selection**

Add `GetTaoistMeleeAttackMagic(PlayerObject player, MapObject target, int nearbyMobCount)`. It must use the existing `TaoistMeleePriority`, filter area magic below three monsters through `SelectHighestDamageSkill`, and return `MagicType.None` when no learned/ready/affordable melee skill exists.

In `ProcessBotTaoistCombatAction`, after the ranged attempt returns false, call this melee selector regardless of `forcePhysicalFallback`, then pass its result to `ProcessBotMeleeCombatAction`. `MagicType.None` remains the final basic-attack signal.

- [ ] **Step 5: Preserve casting when preferred reposition fails**

In `TryProcessBotRangedCombatAction`, keep the initial reposition attempt for non-Assassins. If reposition succeeds, return true as today. If it fails, continue through the existing distance/facing/cast checks instead of returning false immediately. Keep `player.Class != MirClass.Assassin` unchanged and do not change maximum range calculations.

- [ ] **Step 6: Run the focused contract and verify GREEN**

Run:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File ".\.diagnostics\bot-ai-taoist-wizard-combat-priority-contract.ps1"
```

Expected: exit code 0 and every focused assertion reports PASS.

---

### Task 3: Regression checks, build, and evidence

**Files:**
- Read only: all existing `.diagnostics\bot-ai-*.ps1` contracts
- Build output only: `.build-check\server-taoist-wizard-debug-anycpu\`

**Interfaces:**
- Consumes: the production result of Task 2.
- Produces: regression outputs, isolated `Server.exe`, final hashes, and a manual runtime gap statement.

- [ ] **Step 1: Run all existing bot-AI contracts without modifying them**

Run each command separately and require exit code 0:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File ".\.diagnostics\bot-ai-taoist-auto-skill-contract.ps1"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File ".\.diagnostics\bot-ai-taoist-consumable-supply-contract.ps1"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File ".\.diagnostics\bot-ai-phase1-contract.ps1"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File ".\.diagnostics\bot-ai-level40-assassin-contract.ps1"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File ".\.diagnostics\bot-ai-cpu-potion-contract.ps1"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File ".\.diagnostics\bot-ai-assassin-positioning-contract.ps1"
```

Expected: every script reports `RESULT: PASS`. If an existing protected-hash assertion fails only because this authorized task changed `BotManager.Combat.cs`, do not edit that old contract; report the stale protection as a blocker to the primary.

- [ ] **Step 2: Rebuild Debug / AnyCPU into an isolated directory**

Run:

```powershell
& 'C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\MSBuild\Current\Bin\MSBuild.exe' '.\Zircon Server.sln' /t:Rebuild /m /p:Configuration=Debug /p:Platform=AnyCPU /p:OutDir='D:\相聚假人\Source\.build-check\server-taoist-wizard-debug-anycpu\' /v:minimal
```

Expected: exit code 0 and zero compile errors. Do not copy the output elsewhere.

- [ ] **Step 3: Verify artifact and scope**

Run:

```powershell
Get-Item -LiteralPath '.\.build-check\server-taoist-wizard-debug-anycpu\Server.exe' | Select-Object FullName,Length,LastWriteTime
Get-FileHash -Algorithm SHA256 -LiteralPath 'Server\BotSkillSelector.cs','Server\BotManager.Combat.cs','.diagnostics\bot-ai-taoist-wizard-combat-priority-contract.ps1','.build-check\server-taoist-wizard-debug-anycpu\Server.exe'
```

Expected: all four paths exist and have SHA-256 values. Report the exact changed-file list from an allowed-path scan; this is a non-Git tree, so do not run Git or claim a Git diff.

- [ ] **Step 4: Return structured evidence**

Report RED assertion failures, GREEN assertion total, each regression result, build error/warning counts, output path, file size, hashes, and the unchanged runtime gap. Explicitly state that no deployment or live in-game observation was performed and that the user's old running `Server.exe` was not touched.
