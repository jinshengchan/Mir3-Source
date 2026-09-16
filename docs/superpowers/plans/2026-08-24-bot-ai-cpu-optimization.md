# Bot AI CPU Optimization Implementation Plan

> **Execution:** Continue the existing GPT-5.6 Luna / Max task. Work in the shared non-Git tree and preserve unrelated edits. The primary task must inspect the actual files, rerun all verification, and accept the result.

**Goal:** Reduce the avoidable non-combat CPU and allocation cost of 15 server bots without slowing combat or potion response, and add a strict below-5%-HP single-bot home recall safety net.

**Architecture:** Keep the existing 200 ms potion monitor, four-slice main loop, approximately 800 ms combat cadence, and main-thread execution model. Add per-bot next-run gates around existing maintenance methods, eliminate avoidable potion candidate allocations/duplicate validation, and reuse the existing home-map teleport and recall-recovery state for critical HP. Do not add threads, timers, configuration, Python, database changes, or deployment logic.

**Tech Stack:** C#, .NET/MSBuild, Windows PowerShell 5.1 static contracts, SHA-256 evidence.

**Authorized production files:**

- `Server/BotManager.cs`
- `Server/BotManager.Support.cs`
- `Server/BotManager.Combat.cs`
- `Server/BotManager.Chat.cs`

**Authorized diagnostics/docs:**

- `.diagnostics/bot-ai-cpu-optimization-contract.ps1` (new)
- Existing bot-AI contracts named below (verification only unless a production rename makes a minimal assertion update unavoidable)
- This plan and the approved design spec

**Out of scope:** Deployment, restart, backup, Git/PR, client changes, database/resource/script changes, new scheduler threads, combat/potion cadence changes, and unrelated cleanup.

---

## Task 1: Lock the optimization contract RED

**Files:**

- Create: `.diagnostics/bot-ai-cpu-optimization-contract.ps1`
- Read: `Server/BotManager.cs`
- Read: `Server/BotManager.Support.cs`
- Read: `Server/BotManager.Combat.cs`
- Read: `Server/BotManager.Chat.cs`

### Step 1: Recheck ownership baselines

Run:

```powershell
Get-FileHash -Algorithm SHA256 `
  'Server\BotManager.cs', `
  'Server\BotManager.Support.cs', `
  'Server\BotManager.Combat.cs', `
  '.diagnostics\bot-ai-cpu-profiling-contract.ps1', `
  '.diagnostics\bot-ai-cpu-potion-contract.ps1', `
  '.diagnostics\bot-ai-phase1-contract.ps1', `
  '.diagnostics\bot-ai-level40-assassin-contract.ps1', `
  '.diagnostics\bot-ai-taoist-wizard-combat-priority-contract.ps1'
```

Expected production baselines before editing:

- `BotManager.cs`: `377327CB2FF8C5148F020CF279A500342641FE884688150904B59017B75DE3B0`
- `BotManager.Support.cs`: `77FE39E636BD4ECFDBF610397D897D669B62F2ADBF135CD31D4F1523E288468B`
- `BotManager.Combat.cs`: `7D81FBD026DF6CD9AFECCC66A80FE38DD5ED4750F22E0B258FA297294E6BB698`

If an owned production hash differs, inspect the current content and preserve concurrent work; do not overwrite from an old snapshot.

### Step 2: Write one focused structural contract

The contract must read UTF-8 explicitly under Windows PowerShell 5.1 and fail unless all these requirements are present:

```powershell
$utf8 = New-Object System.Text.UTF8Encoding($false)
$manager = [System.IO.File]::ReadAllText((Join-Path $PSScriptRoot '..\Server\BotManager.cs'), $utf8)
$support = [System.IO.File]::ReadAllText((Join-Path $PSScriptRoot '..\Server\BotManager.Support.cs'), $utf8)
$combat = [System.IO.File]::ReadAllText((Join-Path $PSScriptRoot '..\Server\BotManager.Combat.cs'), $utf8)
$chat = [System.IO.File]::ReadAllText((Join-Path $PSScriptRoot '..\Server\BotManager.Chat.cs'), $utf8)

Assert-Match $manager 'BotEquipmentMaintenanceIntervalSeconds\s*=\s*30'
Assert-Match $manager 'BotConsumableMaintenanceIntervalSeconds\s*=\s*20'
Assert-Match $manager 'BotInventoryMaintenanceIntervalSeconds\s*=\s*60'
Assert-Match $manager 'BotClassSupportIntervalSeconds\s*=\s*10'
Assert-Match $manager 'BotHighBossMaintenanceIntervalSeconds\s*=\s*180'
Assert-Match $combat 'BotMapEvalInterval\s*=\s*120'
Assert-Match $chat 'BotSocialMinIntervalSeconds\s*=\s*30'
Assert-Match $chat 'BotSocialMaxIntervalSeconds\s*=\s*60'
Assert-Match $chat 'BotSocialInitialDelayMinSeconds\s*=\s*30'
Assert-Match $chat 'BotSocialInitialDelayMaxSeconds\s*=\s*60'
Assert-Match $combat 'BotCriticalRecallHpPct\s*=\s*5'
Assert-Match $combat 'CurrentHP\s*\*\s*100L\s*/\s*maxHP\s*<\s*BotCriticalRecallHpPct'
Assert-NotMatch ($manager + $support + $combat + $chat) 'new\s+(Thread|Timer)\s*\('
```

Also assert structurally that:

- equipment, consumable, inventory, class-support, and high-boss work are each behind the intended per-bot gate;
- skill learning and normal resupply retain their existing 30-second behavior;
- trade constants remain 120/180;
- inventory cleanup has no full-bag bypass;
- the leader gate occurs before `TryGetBotHighBossGroupTarget`;
- support gates do not wrap PK, pickup, or combat calls;
- new dictionaries are cleared in global stop/reset and removed in per-bot/account cleanup;
- `HashSet<int>` is created only after the first potion-use attempt fails;
- recall is single-bot and does not call `RecallAllBots`;
- exact 5% does not recall, and teleport failure falls through.

### Step 3: Run RED

Run:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File '.diagnostics\bot-ai-cpu-optimization-contract.ps1'
```

Expected: FAIL because the new intervals/guards and strict critical recall are not implemented. Record the failing assertion. Do not edit production before this genuine RED.

---

## Task 2: Gate non-combat maintenance at the approved frequencies

**Files:**

- Modify: `Server/BotManager.cs`
- Modify: `Server/BotManager.Support.cs`
- Modify: `Server/BotManager.Combat.cs`
- Modify: `Server/BotManager.Chat.cs`
- Test: `.diagnostics/bot-ai-cpu-optimization-contract.ps1`

### Step 1: Add minimal per-bot schedules

Use ordinary dictionaries because all calls remain on the existing main action queue:

```csharp
private const int BotEquipmentMaintenanceIntervalSeconds = 30;
private const int BotConsumableMaintenanceIntervalSeconds = 20;
private const int BotInventoryMaintenanceIntervalSeconds = 60;
private const int BotClassSupportIntervalSeconds = 10;
private const int BotHighBossMaintenanceIntervalSeconds = 180;

private static readonly Dictionary<uint, DateTime> _botEquipmentMaintenanceTime = new Dictionary<uint, DateTime>();
private static readonly Dictionary<uint, DateTime> _botConsumableMaintenanceTime = new Dictionary<uint, DateTime>();
private static readonly Dictionary<uint, DateTime> _botInventoryMaintenanceTime = new Dictionary<uint, DateTime>();
private static readonly Dictionary<uint, DateTime> _botClassSupportTime = new Dictionary<uint, DateTime>();
private static readonly Dictionary<uint, DateTime> _botHighBossMaintenanceTime = new Dictionary<uint, DateTime>();

private static bool ShouldRunBotMaintenance(Dictionary<uint, DateTime> schedule, uint objectId, int intervalSeconds)
{
    DateTime now = SEnvir.Now;
    if (schedule.TryGetValue(objectId, out DateTime next) && now < next)
        return false;

    schedule[objectId] = now.AddSeconds(intervalSeconds);
    return true;
}
```

Match the current class field style and naming if equivalent existing helpers are found; do not create a second abstraction.

### Step 2: Gate common maintenance without reordering behavior

In `ProcessBotCommonModules`:

- keep `EquipStarterWeapon(player)` on its current immediate path;
- run auto-equip/buy/repair behind the 30-second equipment gate;
- run ordinary consumable maintenance behind the 20-second gate;
- leave skill-learning and normal-resupply methods on their existing 30-second internal schedules;
- run sell-inventory and game-gold item scanning behind the 60-second inventory gate;
- keep the existing operation order and a single `FlushBotGoldState` path;
- do not add an urgent/full-bag bypass.

### Step 3: Gate class support only

For Wizard, Taoist, and Assassin, place only support/summon/buff maintenance behind one 10-second per-bot gate. Warrior needs no empty gate. PK checks, pickup, targeting, movement, and combat must remain outside this gate.

### Step 4: Gate high-BOSS scans at the leader boundary

Return followers first, then gate the leader by `ObjectID` for 180 seconds before calling `TryGetBotHighBossGroupTarget`. Preserve the existing group/preparation semantics and its internal state.

### Step 5: Update approved slow intervals

- Change normal map evaluation from 60 to 120 seconds.
- Change social regular and initial ranges to 30–60 seconds.
- Leave trade intervals at 120/180 seconds.

### Step 6: Clean schedule state

Clear every new dictionary in the global stop/reset block and remove the bot key in all existing dead/logout/account cleanup paths that clear the neighboring bot state dictionaries.

### Step 7: Run focused GREEN checkpoint

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File '.diagnostics\bot-ai-cpu-optimization-contract.ps1'
```

Expected: maintenance assertions pass; later potion/recall assertions may still fail until Tasks 3–4.

---

## Task 3: Remove avoidable potion hot-path allocation and duplicate checks

**Files:**

- Modify: `Server/BotManager.Combat.cs`
- Test: `.diagnostics/bot-ai-cpu-optimization-contract.ps1`
- Test: `.diagnostics/bot-ai-cpu-potion-contract.ps1`

### Step 1: Preserve potion behavior and cadence

Do not change:

- `BotPotionMonitorIntervalMs = 200`
- HP normal threshold 50%
- MP threshold 50%
- HP emergency threshold 15%
- the existing cooldown/retry semantics

### Step 2: Lazily allocate exclusions

Reshape `TryUseBestBotPotion` so the normal first-success path allocates no `HashSet<int>`:

```csharp
HashSet<int> excludedSlots = null;

while (true)
{
    int potionSlot = FindBestBotPotionSlot(player, restoreHealth, restoreMana, excludedSlots, out potionCooldownMs);
    if (potionSlot < 0)
        return false;

    if (TryUseBotPotion(player, potionSlot, out potionCooldownMs))
        return true;

    if (excludedSlots == null)
        excludedSlots = new HashSet<int>();

    excludedSlots.Add(potionSlot);
    if (excludedSlots.Count >= player.Inventory.Length)
        return false;
}
```

Adapt only parameter order/names to the current signature.

### Step 3: Remove only the proven duplicate validation

`TryUseBotPotion` is private and called only from the selector that has already validated the candidate. Remove its second `CanBotActuallyUsePotionNow` call while retaining basic null/slot/item guards and the existing consume/cooldown behavior. If current call-site inspection shows another caller, preserve validation there instead of broadening behavior.

### Step 4: Verify focused contracts

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File '.diagnostics\bot-ai-cpu-optimization-contract.ps1'
powershell.exe -NoProfile -ExecutionPolicy Bypass -File '.diagnostics\bot-ai-cpu-potion-contract.ps1'
```

Expected: potion allocation/order assertions and existing potion behavior are GREEN.

---

## Task 4: Add strict below-5%-HP single-bot recall

**Files:**

- Modify: `Server/BotManager.Combat.cs`
- Modify only if existing helper ownership requires it: `Server/BotManager.Support.cs`
- Test: `.diagnostics/bot-ai-cpu-optimization-contract.ps1`
- Test: `.diagnostics/bot-ai-phase1-contract.ps1`

### Step 1: Add the strict integer-safe predicate

```csharp
private const int BotCriticalRecallHpPct = 5;

private static bool ShouldRecallBotForCriticalHealth(PlayerObject player)
{
    int maxHP = player?.Stats?[Stat.Health] ?? 0;
    return maxHP > 0 && player.CurrentHP * 100L / maxHP < BotCriticalRecallHpPct;
}
```

Use the actual health-stat access type from current source. The comparison must remain strict `< 5`; exactly 5% must not recall.

### Step 2: Reuse the existing recall recovery flow for one bot

Insert the check in `ProcessBotCombat` after the existing recall freeze/recovery block and before new target/combat/telemetry work:

```csharp
if (ShouldRecallBotForCriticalHealth(player) && TryRecallBotForCriticalHealth(player))
    return;
```

`TryRecallBotForCriticalHealth` must:

- resolve existing `BotHomeMapIndex` and `BotHomePoint`;
- attempt `Teleport` for only this player;
- never call `RecallAllBots` or alter other bots;
- only after successful teleport set the successful recovery state;
- reuse `BotRecallRestSeconds = 60` and permit the existing full-HP early recovery exit;
- clear target lock, pending combat actions, pickup target/waiting, kite, roam/path/movement samples, and other matching state already cleared by recall helpers;
- delay map evaluation until recovery ends and record the map switch;
- on missing map/destination or teleport failure, return `false` without setting recovery and let the same tick continue through existing potion, retreat, and combat fallback.

### Step 3: Run recall GREEN

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File '.diagnostics\bot-ai-cpu-optimization-contract.ps1'
powershell.exe -NoProfile -ExecutionPolicy Bypass -File '.diagnostics\bot-ai-phase1-contract.ps1'
```

Expected: strict threshold, one-bot scope, success cleanup, recovery ordering, and failure fall-through are GREEN.

---

## Task 5: Full regression, Debug/AnyCPU artifact, and evidence

**Files:**

- Verify all authorized production/diagnostic files
- Output only: `.build-check/bot-ai-cpu-optimization-debug-anycpu/`
- Output only: `.build-check/bot-ai-cpu-optimization-debug-anycpu-obj/`

### Step 1: Run the complete focused regression set

```powershell
$contracts = @(
  '.diagnostics\bot-ai-cpu-optimization-contract.ps1',
  '.diagnostics\bot-ai-cpu-profiling-contract.ps1',
  '.diagnostics\bot-ai-cpu-potion-contract.ps1',
  '.diagnostics\bot-ai-phase1-contract.ps1',
  '.diagnostics\bot-ai-level40-assassin-contract.ps1',
  '.diagnostics\bot-ai-assassin-positioning-contract.ps1',
  '.diagnostics\bot-ai-taoist-wizard-combat-priority-contract.ps1',
  '.diagnostics\bot-ai-taoist-consumable-supply-contract.ps1',
  '.diagnostics\bot-ai-taoist-auto-skill-contract.ps1'
)

foreach ($contract in $contracts) {
    powershell.exe -NoProfile -ExecutionPolicy Bypass -File $contract
    if ($LASTEXITCODE -ne 0) { throw "Contract failed: $contract" }
}
```

If one listed historical contract does not exist, report that exact gap and run every existing listed contract; do not manufacture unrelated coverage.

### Step 2: Compile the server library first

```powershell
dotnet build 'ServerLibrary\ServerLibrary.csproj' -c Debug --no-restore
```

Expected: 0 errors.

### Step 3: Rebuild Debug / AnyCPU to an isolated artifact directory

```powershell
$output = 'D:\相聚假人\Source\.build-check\bot-ai-cpu-optimization-debug-anycpu\'
$obj = 'D:\相聚假人\Source\.build-check\bot-ai-cpu-optimization-debug-anycpu-obj\'
New-Item -ItemType Directory -Force -Path $output, $obj | Out-Null
$msbuild = 'C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\MSBuild\Current\Bin\MSBuild.exe'
& $msbuild 'Server\Server.csproj' /t:Rebuild /m /v:minimal /p:Configuration=Debug /p:Platform=AnyCPU "/p:OutputPath=$output" "/p:BaseIntermediateOutputPath=$obj"
if ($LASTEXITCODE -ne 0) { throw 'Debug/AnyCPU rebuild failed.' }
```

Expected: 0 errors. Existing `MSB3277` warnings may be reported but are not silently described as new failures.

### Step 4: Record final evidence

```powershell
Get-FileHash -Algorithm SHA256 `
  'Server\BotManager.cs', `
  'Server\BotManager.Support.cs', `
  'Server\BotManager.Combat.cs', `
  'Server\BotManager.Chat.cs', `
  '.diagnostics\bot-ai-cpu-optimization-contract.ps1', `
  'docs\superpowers\specs\2026-08-24-bot-ai-cpu-optimization-design.md', `
  'docs\superpowers\plans\2026-08-24-bot-ai-cpu-optimization.md', `
  '.build-check\bot-ai-cpu-optimization-debug-anycpu\Server.exe'

Get-Item '.build-check\bot-ai-cpu-optimization-debug-anycpu\Server.exe' |
  Select-Object FullName, Length, LastWriteTime
```

Also compare all modified files against the recorded baselines/current pre-edit copies and state every actual changed file. Do not deploy or copy the artifact to `D:\Debug\4月18日更新\Server`.

### Step 5: Report the remaining runtime gap

Static contracts and a successful Debug/AnyCPU rebuild do not prove the live CPU reduction. Report that acceptance still requires a manual run with the same 15-bot workload and a comparable 10-minute sampling window. The previous observed reference was approximately 4–9% for the newer build versus 1–4% for the older build, but do not claim improvement until measured on the new artifact.
