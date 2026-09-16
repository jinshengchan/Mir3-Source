# Bot Death, Revive, and Safe-Zone Recovery Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make server bots retain equipped items on death, revive in town at full HP/MP, and refill missing HP/MP once on the next existing bot AI tick while in a safe zone.

**Architecture:** Keep all behavior on existing server paths. Gate only the equipped-item death-drop candidate loops in `PlayerObject.Die`, select a bot-specific revive rate in `TownRevive`, and reuse the existing per-bot main action queue for safe-zone refill without adding timers, threads, map scans, database work, or repeated state updates when already full.

**Tech Stack:** C# / .NET Framework 4.8, PowerShell 5.1 focused contract, Visual Studio 2022 Build Tools MSBuild.

## Global Constraints

- Only `PlayerObject.IsBot == true` behavior changes.
- Equipped items are protected; inventory and companion-inventory death drops remain unchanged.
- Existing bind-point and war revive-location selection remains unchanged.
- Human players retain 30% town-revive HP/MP and existing safe-zone regeneration behavior.
- Bot safe-zone refill reuses the current bot main tick and does not add a timer, thread, map scan, database query, or configuration option.
- Do not deploy, restart the server, modify databases, initialize Git, or edit files outside the ownership list.
- This is a non-Git workspace; do not run commit, checkout, reset, clean, or branch operations.

## File Map and Ownership

- Create: `.diagnostics/test_bot_death_revive_safezone_recovery_contract.ps1` — focused RED/GREEN source contract for the three requested behavior branches.
- Modify: `ServerLibrary/Models/Player/Combat.cs` — prevent bots from entering both equipped-item drop candidate paths.
- Modify: `ServerLibrary/Models/Player/Initialize.cs` — restore bots to 100% HP/MP during existing town revive while retaining 30% for humans.
- Modify: `Server/BotManager.cs` — refill a live bot once when safe-zone HP/MP is below its current stat maximum.
- Reference only: `docs/superpowers/specs/2026-09-05-bot-death-revive-safezone-recovery-design.md`.
- Do not modify project files, configuration, deployment outputs, inventory-drop code, companion-inventory-drop code, safe-zone detection, tick cadence, or client code.

---

### Task 1: Add the focused failing contract

**Files:**
- Create: `.diagnostics/test_bot_death_revive_safezone_recovery_contract.ps1`
- Read only: `ServerLibrary/Models/Player/Combat.cs`
- Read only: `ServerLibrary/Models/Player/Initialize.cs`
- Read only: `Server/BotManager.cs`

**Interfaces:**
- Consumes: UTF-8 C# source files and the existing PowerShell contract convention.
- Produces: one executable PowerShell 5.1 contract that exits `0` only when all three bot-only behavior boundaries and the no-extra-scheduler constraint are present.

- [ ] **Step 1: Create the contract before production edits**

Use the repository's existing `Assert-Contract` pattern. The script must load the three owned C# files with `Get-Content -Encoding UTF8 -Raw`, slice `PlayerObject.Die` from `public override void Die()` to the following method, slice `TownRevive`, and slice the queued bot lambda around the existing `ProcessBotBehaviorPipeline(capturedPlayer)` call. It must assert all of these independently:

```powershell
Assert-Contract ($dieBody -match 'if\s*\(\s*!IsBot\s*&&\s*\(Stats\[Stat\.PKPoint\]') 'red-name equipped drop path excludes bots'
Assert-Contract ($equipmentDropBody -match 'if\s*\(\s*!IsBot\s*\)\s*\r?\n\s*for\s*\(int i = 0; i < Equipment\.Length; i\+\+\)') 'general equipped drop candidate loop excludes bots'
Assert-Contract ($townReviveBody -match 'int\s+reviveRate\s*=\s*IsBot\s*\?\s*100\s*:\s*30\s*;') 'town revive selects full rate only for bots'
Assert-Contract ($townReviveBody -match 'SetHP\s*\(\s*Stats\[Stat\.Health\]\s*\*\s*reviveRate\s*/\s*100\s*\)') 'town revive applies selected HP rate'
Assert-Contract ($townReviveBody -match 'SetMP\s*\(\s*Stats\[Stat\.Mana\]\s*\*\s*reviveRate\s*/\s*100\s*\)') 'town revive applies selected MP rate'
Assert-Contract ($botTickBody -match 'if\s*\(\s*capturedPlayer\.InSafeZone\s*\)') 'existing bot tick gates refill by safe zone'
Assert-Contract ($botTickBody -match 'capturedPlayer\.CurrentHP\s*<\s*capturedPlayer\.Stats\[Stat\.Health\][\s\S]*?capturedPlayer\.SetHP\s*\(\s*capturedPlayer\.Stats\[Stat\.Health\]\s*\)') 'safe-zone bot HP refills only when below maximum'
Assert-Contract ($botTickBody -match 'capturedPlayer\.CurrentMP\s*<\s*capturedPlayer\.Stats\[Stat\.Mana\][\s\S]*?capturedPlayer\.SetMP\s*\(\s*capturedPlayer\.Stats\[Stat\.Mana\]\s*\)') 'safe-zone bot MP refills only when below maximum'
Assert-Contract ($botTickBody -notmatch 'new\s+(System\.Threading\.)?Timer|Task\.Run|new\s+Thread') 'safe-zone refill adds no scheduler or thread'
```

The script must print `RESULT: PASS (<n> assertions)` on success and `RESULT: FAIL (<passed> passed; <failed> failed)` plus every failed assertion on failure.

- [ ] **Step 2: Run the contract and verify RED**

Run:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File 'D:\相聚假人\Source\.diagnostics\test_bot_death_revive_safezone_recovery_contract.ps1'
```

Expected: exit code `1`; failures must specifically show the missing bot equipment-drop exclusion, 100% bot revive rate, and safe-zone one-shot refill. A parse error, missing file, or unrelated failure is not an acceptable RED.

---

### Task 2: Protect equipped items and make bot town revive full

**Files:**
- Modify: `ServerLibrary/Models/Player/Combat.cs:2819-3464`
- Modify: `ServerLibrary/Models/Player/Initialize.cs:729-778`
- Test: `.diagnostics/test_bot_death_revive_safezone_recovery_contract.ps1`

**Interfaces:**
- Consumes: `PlayerObject.IsBot`, `Stats[Stat.PKPoint]`, `Equipment`, `SetHP(int)`, `SetMP(int)`.
- Produces: bot-only exclusion from both worn-equipment candidate paths and bot-only 100% town-revive HP/MP.

- [ ] **Step 1: Exclude bots from both equipped-item candidate paths**

In `Combat.cs`, change only the two entry conditions inside `#region 死亡身上装备掉落`:

```csharp
if (!IsBot && (Stats[Stat.PKPoint] >= Config.RedPoint) && SEnvir.Random.Next(Config.DieRedRandomChance) == 0)
```

and immediately before the general `for (int i = 0; i < Equipment.Length; i++)` loop:

```csharp
if (!IsBot)
    for (int i = 0; i < Equipment.Length; i++)
```

Do not alter either loop body, inventory drops, companion-inventory drops, final `RefreshWeight()`/`RefreshStats()`, random rates, or human behavior.

- [ ] **Step 2: Select the existing revive percentage by bot status**

In `Initialize.cs`, after `Dead = false;` and before the HP/MP setters, use exactly one local rate:

```csharp
int reviveRate = IsBot ? 100 : 30;
SetHP(Stats[Stat.Health] * reviveRate / 100);
SetMP(Stats[Stat.Mana] * reviveRate / 100);
```

Do not alter the location-selection branches, object removal/addition, revive broadcast, or human percentage.

- [ ] **Step 3: Run the focused contract for an intermediate check**

Run the Task 1 command. Expected: equipment and town-revive assertions pass; safe-zone refill assertions remain failed, so the script still exits `1` for the expected remaining feature only.

---

### Task 3: Refill living bots on the existing safe-zone tick

**Files:**
- Modify: `Server/BotManager.cs:1124-1212`
- Test: `.diagnostics/test_bot_death_revive_safezone_recovery_contract.ps1`

**Interfaces:**
- Consumes: the existing queued `capturedPlayer`, `InSafeZone`, `CurrentHP`, `CurrentMP`, `Stats`, `SetHP(int)`, `SetMP(int)` and current main bot tick.
- Produces: no new public API; missing HP/MP is restored no later than the next existing bot main tick while safe, with no setter call when already full.

- [ ] **Step 1: Add the safe-zone refill after dead/node guards**

Immediately after `if (capturedPlayer.Node == null) return;` and before the normal AI `try`, add:

```csharp
if (capturedPlayer.InSafeZone)
{
    if (capturedPlayer.CurrentHP < capturedPlayer.Stats[Stat.Health])
        capturedPlayer.SetHP(capturedPlayer.Stats[Stat.Health]);

    if (capturedPlayer.CurrentMP < capturedPlayer.Stats[Stat.Mana])
        capturedPlayer.SetMP(capturedPlayer.Stats[Stat.Mana]);
}
```

Do not add a helper, timer, thread, task, configuration switch, map scan, database access, logging, or early return from normal AI.

- [ ] **Step 2: Run the focused contract and verify GREEN**

Run the Task 1 command. Expected: exit code `0`, every assertion prints `PASS`, and the final line reports `RESULT: PASS`.

---

### Task 4: Build and scope-audit the server change

**Files:**
- Verify: `Server/Server.csproj`
- Verify: all six owned/reference files listed in the File Map and final hash list.

**Interfaces:**
- Consumes: Visual Studio 2022 Build Tools MSBuild and the current local dependency set.
- Produces: isolated compile evidence only; no deployment or live-runtime claim.

- [ ] **Step 1: Build to an isolated output directory**

Run:

```powershell
& 'C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\MSBuild\Current\Bin\MSBuild.exe' 'D:\相聚假人\Source\Server\Server.csproj' /t:Build /p:Configuration=Release /p:Platform=AnyCPU /p:OutputPath='D:\相聚假人\Source\.artifacts\bot-death-revive-safezone-recovery\' /m
```

Expected: exit code `0` and `0 Error(s)`. Record warnings separately; do not call warnings newly introduced unless shown by a baseline comparison.

- [ ] **Step 2: Re-run the focused contract after the build**

Run the Task 1 command again. Expected: exit code `0` and `RESULT: PASS`.

- [ ] **Step 3: Inspect exact changed-file scope without Git**

Report the SHA-256 hashes and last-write times for:

```text
ServerLibrary/Models/Player/Combat.cs
ServerLibrary/Models/Player/Initialize.cs
Server/BotManager.cs
.diagnostics/test_bot_death_revive_safezone_recovery_contract.ps1
docs/superpowers/specs/2026-09-05-bot-death-revive-safezone-recovery-design.md
docs/superpowers/plans/2026-09-05-bot-death-revive-safezone-recovery.md
```

Inspect bounded excerpts around each edited production location and the complete new contract. Confirm no deployment, process restart, database modification, project-file edit, or output replacement occurred.

- [ ] **Step 4: State the remaining live acceptance explicitly**

Do not claim runtime completion. Record these unperformed acceptance checks for the user:

```text
1. Kill a bot whose worn item is eligible for death drop and verify every equipped slot remains populated.
2. Verify the dead bot revives at the existing bind/war revive point with HP and MP both at their stat maximum.
3. Damage/drain a live bot, move it into a safe zone, and verify HP/MP reach maximum no later than the next bot main tick.
4. Confirm a human player still town-revives at 30% HP/MP and retains current death-drop behavior.
```
