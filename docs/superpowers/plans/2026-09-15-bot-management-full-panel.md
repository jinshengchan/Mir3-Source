# Bot Management Full Panel Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the simplified bot-management view with the approved screenshot-matched two-column panel and connect every displayed control to persisted, thread-safe server behavior.

**Architecture:** Keep the existing `BotManager` partial-class system and add focused management/settings/reward partials rather than expanding the already-large core files. Persist scalar settings through `Config`/`Server.ini`, persist per-bot reward progress through `BotAccountInfo`, and expose immutable snapshots to the UI. Main-AI and potion work remain main-thread-only but receive independent queues/budgets.

**Tech Stack:** C# 7.2/8, .NET Framework 4.8 WinForms + DevExpress 23.2, .NET Standard 2.0 `ServerLibrary`, MirDB, PowerShell contract tests, MSBuild/dotnet build.

## Global Constraints

- Work only in `D:\相聚假人\Source`; do not deploy, restart, replace runtime binaries, edit clients, or change scripts.
- `Server\Server.csproj` references `ServerLibrary\bin\$(Configuration)\netstandard2.0\Library.dll`; modify `ServerLibrary`, not the unused `ServerLibrary7878` mirror.
- Preserve existing `CanAttackTarget` safety-zone, safe-map, team, guild, bot, pet, and pet-owner protections.
- At 50%, all four behavior-strength settings must preserve current behavior.
- Any role/map/inventory/database mutation must execute on the server main thread.
- Use atomic validation: an invalid form value must leave both `Config` and runtime settings unchanged.
- This workspace is not a Git repository. Replace commit steps with named verification checkpoints; do not initialize Git.
- Static contracts and isolated builds do not prove live gameplay acceptance.

---

## File Structure

- Create `Server/BotManagementSettings.cs`: typed form/config model, defaults, bounds, validation, and `Config` mapping.
- Create `Server/BotManager.Management.cs`: apply/sync API, pause state, statistics/log snapshots, initial-gold refill, recovery and runtime controls.
- Create `Server/BotManager.Rewards.cs`: idempotent defense/strong-element reward calculation, audit and backfill.
- Modify `Server/Server.csproj`: compile the three new server files.
- Modify `ServerLibrary/Envir/Config.cs`: persisted scalar properties only.
- Modify `ServerLibrary/Envir/SEnvir.cs`: separate potion action queue and independent per-frame drains in both loop variants.
- Modify `ServerLibrary/DBModels/BotAccountInfo.cs`: persisted reward tiers and `Stats` reward payload.
- Modify `Server/BotManager.cs`, `.Combat.cs`, `.Support.cs`, `.Chat.cs`, `.Siege.cs`: narrow gates and configurable constants at their existing owners.
- Modify `Server/Views/BotConfigView.cs`: approved two-column panel, binding, refresh, logs and commands.
- Do not modify `Server/Views/BotConfigView.Designer.cs`; it is not compiled by `Server.csproj`, and the live view owns `InitializeComponent()` in `BotConfigView.cs`.
- Modify `Server/SMain.cs`: restore guarded auto-start.
- Create five focused PowerShell contracts under `tests/`.

Every contract uses this exact harness; each task supplies its own file paths and literal/regex assertions:

```powershell
$ErrorActionPreference = 'Stop'
$script:Assertions = 0
function Assert-Contains([string]$Text, [string]$Pattern, [string]$Message) {
    $script:Assertions++
    if ($Text -notmatch $Pattern) { throw "FAIL: $Message`nPattern: $Pattern" }
}
function Assert-NotContains([string]$Text, [string]$Pattern, [string]$Message) {
    $script:Assertions++
    if ($Text -match $Pattern) { throw "FAIL: $Message`nForbidden: $Pattern" }
}
Write-Host "RESULT: PASS ($script:Assertions assertions)"
```

---

### Task 1: Persisted settings and atomic validation

**Files:**
- Create: `Server/BotManagementSettings.cs`
- Modify: `ServerLibrary/Envir/Config.cs`
- Modify: `Server/Server.csproj`
- Test: `tests/test_bot_management_config_contract.ps1`

**Interfaces:**
- Produces: `BotManagementSettings.FromConfig()`, `TryValidate(out string error)`, `WriteToConfig()`.
- Produces: all `Config.Bot*` properties consumed by Tasks 2-7.

- [ ] **Step 1: Write the failing config contract**

Create a PowerShell test that reads the three files and asserts exact property/model names, the 50% defaults, current-compatible constants, validation bounds, and the new `<Compile Include="BotManagementSettings.cs" />`. Include a `Assert-Contains` helper and end with `RESULT: PASS (<n> assertions)`.

Run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\tests\test_bot_management_config_contract.ps1
```

Expected: FAIL because `BotManagementSettings.cs` and the new properties do not exist.

- [ ] **Step 2: Add the exact settings model**

Define `public sealed class BotManagementSettings` in namespace `Server` with fields/properties for every approved control. Use these exact groups and names:

```csharp
public int AggressionPercent { get; set; }
public int ActivityPercent { get; set; }
public int GroupTendencyPercent { get; set; }
public int ChatFrequencyPercent { get; set; }
public bool PercentRecoveryEnabled { get; set; }
public bool FixedRecoveryEnabled { get; set; }
public int PercentRecoveryPerSecond { get; set; }
public int FixedRecoveryPerSecond { get; set; }
public int ProactivePvpMinLevel { get; set; }
public int AutoRebirthLevel { get; set; }
public int AutoRebirthMaxCount { get; set; }
public int MainActionsPerFrame { get; set; }
public int PotionActionsPerFrame { get; set; }
```

Use direct counterparts for this complete persisted set:

```csharp
BotEnableChat, BotAutoLevel, BotAutoPickup, BotAutoSellTrash,
BotAutoPotionSupply, BotAutoEquip, BotAutoLearnSkill, BotAutoGroup,
BotAutoTrade, BotGuildSystem, BotParticipateConquest, BotPvpRetaliation,
BotAutoMapSwitch, BotSkipPickupWhenGroupedWithHuman, BotAutoRebirth,
BotPercentRecoveryEnabled, BotFixedRecoveryEnabled, BotAutoSpecialRepair,
BotProactivePvpMinLevel, BotAutoRebirthLevel, BotAutoRebirthMaxCount,
BotDefenseLevelInterval, BotDefenseBonusPerTier, BotStrongElementStartLevel,
BotStrongElementLevelInterval, BotStrongElementTypeCount,
BotPercentRecoveryPerSecond, BotFixedRecoveryPerSecond,
BotGlobalChatIntervalSeconds, BotSpecialRepairThresholdPercent,
BotRecallBatchIntervalMs, BotRecallBatchSize, BotAggressionPercent,
BotActivityPercent, BotGroupTendencyPercent, BotChatFrequencyPercent,
BotInitialGoldFloor, BotGoldFarmThreshold, BotMinHealthPotionCount,
BotMinManaPotionCount, BotTickDispatchLimit, BotMainLoopIntervalMs,
BotMaxOnline, BotPotionMonitorIntervalMs, BotFullHealthThresholdPercent,
BotAttackAttemptIntervalMs, BotPickupAttemptIntervalMs, BotPickupRadius,
BotMapPoolBonus, BotMapSwitchScoreGapMax, BotPeriodicGroupSeconds,
BotMainActionsPerFrame, BotPotionActionsPerFrame, BotLogDirectory
```

`TryValidate` must reject simultaneous recovery modes, values outside the design bounds, and `AutoRebirthMaxCount > 0` with `AutoRebirthLevel == 0`. `WriteToConfig` must be called only after successful validation.

- [ ] **Step 3: Add compatible `Config` defaults**

Add one contiguous `#region 假人管理完整配置` beside the existing bot settings. Preserve existing defaults: gold threshold 500000, potion minima 80, main/potion timers 200ms, repair threshold 50, main frame budget 200, behavior sliders 50. New behavior that does not currently exist defaults off.

- [ ] **Step 4: Run RED/GREEN config verification**

Run the config contract, then:

```powershell
dotnet build .\ServerLibrary\ServerLibrary.csproj -c Debug --no-restore
```

Expected: contract PASS; library build 0 errors.

Checkpoint: record changed files and test/build output; do not commit.

---

### Task 2: Independent runtime scheduling and safe application

**Files:**
- Create: `Server/BotManager.Management.cs`
- Modify: `Server/BotManager.cs`
- Modify: `ServerLibrary/Envir/SEnvir.cs`
- Modify: `Server/Server.csproj`
- Test: `tests/test_bot_management_runtime_contract.ps1`

**Interfaces:**
- Produces: `public static bool TryApplyManagementSettings(BotManagementSettings settings, bool persist, out string error)`.
- Produces: `public static void SetPaused(bool paused)`, `public static bool IsPaused`.
- Produces: `SEnvir.BotPotionActionQueue` and independent queue drains.

- [ ] **Step 1: Write a failing scheduling contract**

Assert that potion callbacks enqueue only to `BotPotionActionQueue`, both server loop variants consume `BotActionQueue` with `Config.BotMainActionsPerFrame`, both consume `BotPotionActionQueue` with `Config.BotPotionActionsPerFrame`, and neither Timer callback executes player logic directly.

- [ ] **Step 2: Split the queue budgets**

Add:

```csharp
public static ConcurrentQueue<Action> BotPotionActionQueue = new ConcurrentQueue<Action>();
```

In both SEnvir loop variants, drain main actions and potion actions separately using validated config budgets. Keep per-action exception isolation and existing log wording differentiated as `BotAction` versus `BotPotionAction`.

- [ ] **Step 3: Make timers configurable**

Replace `BotMainSliceIntervalMs`, `BotMainSliceCount`, `BotPotionMonitorIntervalMs` scheduling constants at their use sites with the validated runtime snapshot. Enforce “每Tick处理” as a dispatch budget in `BotTick`; preserve `_botQueued`/`_botPotionQueued` anti-backlog guards.

- [ ] **Step 4: Add atomic apply and pause**

`TryApplyManagementSettings` must validate first, save old settings, write config, optionally call `ConfigReader.Save()`, reset timers only after success, and enqueue online synchronization. On failure restore the old settings and return an actionable error. `SetPaused(true)` blocks ordinary AI decisions while preserving connection maintenance, dead-player handling and emergency potion processing.

- [ ] **Step 5: Verify scheduling**

Run the runtime and config contracts plus the library build. Expected: all PASS and 0 build errors.

Checkpoint: inspect that only the named files changed.

---

### Task 3: Gate automatic behavior and apply strength/economy controls

**Files:**
- Modify: `Server/BotManager.cs`
- Modify: `Server/BotManager.Combat.cs`
- Modify: `Server/BotManager.Support.cs`
- Modify: `Server/BotManager.Chat.cs`
- Modify: `Server/BotManager.Siege.cs`
- Extend test: `tests/test_bot_management_runtime_contract.ps1`

**Interfaces:**
- Consumes: validated `Config.Bot*` fields and `BotManager.IsPaused`.
- Produces: `ApplyInitialGoldFloor(PlayerObject player)`, `ProcessConfiguredRecovery(PlayerObject player)`, `ShouldTriggerScaledBehavior(int percent, uint stableKey, long window)`.

- [ ] **Step 1: Add failing gate assertions**

Cover each approved switch at its owning module, separate PVP retaliation from proactive PVP level, and assert that proactive human targets still end in `CanAttackTarget`.

- [ ] **Step 2: Gate existing modules narrowly**

Add early guards only around the corresponding existing calls: leveling/combat, pickup, trash sale, potion supply, equip, skill learning, grouping, trading, guild, conquest, retaliation and auto-map. Do not reorder the existing pipeline or alter adjacent human-player behavior.

- [ ] **Step 3: Implement 50%-baseline scaling**

Use a deterministic per-window roll so 0 disables non-emergency proactive triggers, 50 executes exactly the legacy cadence, and 100 permits at most two attempts in the same legacy interval. Apply it only to proactive target search, non-emergency movement/map switching, ordinary group participation and proactive chat.

- [ ] **Step 4: Add economy/recovery controls**

Call `ApplyInitialGoldFloor` only on first creation, login and explicit synchronization. Top up only the difference. Parameterize the existing gold/potion/repair thresholds. Implement the mutually exclusive once-per-second HP+MP recovery on the main thread and cap at max HP/MP.

- [ ] **Step 5: Add configurable PK/rebirth behavior**

Retaliation ignores the proactive level threshold but retains legality. Proactive PVP requires `Level >= ProactivePvpMinLevel` unless threshold is 0. Auto-rebirth invokes the existing `NPCRebirth()` path only when enabled, level reached and `Character.Rebirth` is below the configured cap.

- [ ] **Step 6: Verify all gates**

Run both contracts and build `ServerLibrary`. Expected: PASS and 0 errors.

Checkpoint: manually inspect every gate to confirm it encloses only its own module.

---

### Task 4: Idempotent level rewards, audit and backfill

**Files:**
- Modify: `ServerLibrary/DBModels/BotAccountInfo.cs`
- Modify: `ServerLibrary/Models/Player/Refresh.cs`
- Create: `Server/BotManager.Rewards.cs`
- Modify: `Server/Server.csproj`
- Test: `tests/test_bot_management_rewards_contract.ps1`

**Interfaces:**
- Produces DB properties: `DefenseRewardTier`, `StrongElementRewardTier`, `Stats LevelRewardStats`.
- Produces: `GetMissingBotRewardReport()`, `BackfillMissingBotRewards()`.

- [ ] **Step 1: Write failing reward scenarios**

The contract must cover first grant, same-level repeat, re-login repeat, interval disabled by 0, multi-tier catch-up, fixed persisted random element results, audit without mutation and backfill with mutation.

- [ ] **Step 2: Add minimal persisted state**

Persist completed tiers and the actual reward `Stats` on `BotAccountInfo`. Never alter general `CharacterInfo.HermitStats`; bot rewards remain bot-owned and auditable.

- [ ] **Step 3: Calculate and apply rewards**

Defense tiers add equal values to `MinAC`, `MaxAC`, `MinMR`, and `MaxMR`. Strong-element tiers choose distinct entries per tier from the seven attack elements (`FireAttack` through `PhantomAttack`), add one point to each selected element, persist immediately, and call `RefreshStats()` once after a changed batch.

- [ ] **Step 4: Integrate reward stats into refresh**

In `PlayerObject.RefreshStats()`, after base and character stats are assembled and before final derived-stat notifications, resolve the player's `BotAccountInfo`; when present, add its `LevelRewardStats` once to the current refresh accumulator. Assert non-bot characters never receive it.

- [ ] **Step 5: Verify rewards**

Run reward/config/runtime contracts and build `ServerLibrary`. Expected: PASS, 0 errors, and audit code contains no assignment to reward progress.

Checkpoint: review the DB-model delta for backward-compatible default values.

---

### Task 5: Map/group tuning, management commands, snapshots and logs

**Files:**
- Modify: `Server/BotManager.Management.cs`
- Modify: `Server/BotManager.Support.cs`
- Modify: `Server/BotManager.cs`
- Test: `tests/test_bot_management_operations_contract.ps1`

**Interfaces:**
- Produces: `BotManagementSnapshot GetManagementSnapshot()`.
- Produces: `BotBatchResult SyncOnlineBots()`, `SetTargetOnlineCount(int)`, existing recall/switch APIs with result counts.
- Produces: `RecordManagementLog(BotLogKind kind, string message)` and bounded activity/operation snapshots.

- [ ] **Step 1: Write failing operation/snapshot assertions**

Cover statistics definitions, map-score bonus/difference pool, periodic grouping 0-disable behavior, pause status, bounded logs and batch result counts.

- [ ] **Step 2: Parameterize map selection and grouping**

Add `BotMapPoolBonus` to level-appropriate candidates. Build the random pool from candidates where `bestScore - score <= BotMapSwitchScoreGapMax`. Keep every existing block reason. Trigger ordinary periodic regrouping at `BotPeriodicGroupSeconds`; preserve forced/high-boss regroup behavior.

- [ ] **Step 3: Implement immutable UI snapshots**

Return copied rows/log lines, never live collections. Define statistics exactly as the design: session kills/deaths, distinct current maps, online-gold sum and online average level. Reset counters at `Start`, retain them after `Stop`.

- [ ] **Step 4: Add bounded logging and batch results**

Use separate bounded activity and GM-operation buffers, write to the configured bot-log directory, and return success/failure/protected/timeout counts from batch operations. Do not log every normal Tick.

- [ ] **Step 5: Verify operations**

Run all four contracts and both relevant builds. Expected: PASS and 0 errors.

Checkpoint: confirm snapshot/log APIs expose copies only.

---

### Task 6: Build the screenshot-matched management UI

**Files:**
- Modify: `Server/Views/BotConfigView.cs`
- Test: `tests/test_bot_management_ui_contract.ps1`

**Interfaces:**
- Consumes: `BotManagementSettings`, `TryApplyManagementSettings`, `GetManagementSnapshot`, reward and batch APIs.

- [ ] **Step 1: Write the failing UI contract**

Assert every approved Chinese label, four 0-100 sliders defaulting to 50, numeric up/down controls for economic/performance/new-feature values, one-second UI timer, save/apply handlers, mutual recovery checkbox handlers, dangerous confirmations and disposal cleanup.

- [ ] **Step 2: Rebuild the form in screenshot order**

Use the current MDI form entry and project-native WinForms/DevExpress controls. Create the two columns and exact groups from the design. Match screenshot button colors and ordering; use scroll support only when host DPI cannot fit the full content.

The UI contract must find these corrected visible labels verbatim:

```text
自动特修装备
按比例每秒给假人回血蓝
按数值每秒给假人回血蓝
增加双防
随机增加几种强元素
查看奖励漏发
覆盖地图
新增功能配置
地图池加成
切图分差上限
主AI每帧上限
药水每帧上限
周期组队（秒）
达到
级以上与玩家PK
自动转生
```

- [ ] **Step 3: Bind without partial saves**

`LoadBotSettings` uses `BotManagementSettings.FromConfig()`. `TryReadFormSettings` builds a detached model and validates it. Only then call the manager apply API. Reflect right-side quick changes into the formal values before save/sync.

- [ ] **Step 4: Wire commands and refresh**

Every button invokes a real manager API. A one-second WinForms timer refreshes status, bot rows, statistics and copied logs. Stop the timer and unsubscribe on form disposal; closing the form must not stop bots.

- [ ] **Step 5: Verify UI and compile**

Run the UI contract and all prior contracts. Build Server to an isolated directory:

```powershell
$out = Join-Path (Resolve-Path .) '.artifacts\bot-management-full-panel-debug'
& msbuild .\Server\Server.csproj /t:Rebuild /p:Configuration=Debug /p:Platform=AnyCPU /p:OutDir="$out\"
```

Expected: all contracts PASS; Server build 0 errors. Existing dependency warnings must be reported, not hidden.

Checkpoint: compare the running form visually with the approved screenshot and corrected labels.

---

### Task 7: Guarded auto-start and full regression acceptance

**Files:**
- Modify: `Server/SMain.cs`
- Extend test: `tests/test_bot_management_operations_contract.ps1`

**Interfaces:**
- Consumes: validated config and existing `BotManager.Initialize/Start`.

- [ ] **Step 1: Add failing auto-start assertions**

Require initialize-first ordering, enabled flag, non-empty existing file, validated settings, one start call, and logged non-fatal failure.

- [ ] **Step 2: Restore guarded auto-start**

Replace the commented call with a single guarded startup after environment initialization. Invalid configuration or missing file logs the reason and leaves the server UI running.

- [ ] **Step 3: Run the complete verification matrix**

```powershell
$tests = @(
  '.\tests\test_bot_management_config_contract.ps1',
  '.\tests\test_bot_management_runtime_contract.ps1',
  '.\tests\test_bot_management_rewards_contract.ps1',
  '.\tests\test_bot_management_operations_contract.ps1',
  '.\tests\test_bot_management_ui_contract.ps1'
)
foreach ($test in $tests) {
  powershell -NoProfile -ExecutionPolicy Bypass -File $test
  if ($LASTEXITCODE -ne 0) { throw "Contract failed: $test" }
}
dotnet build .\ServerLibrary\ServerLibrary.csproj -c Debug --no-restore
```

Then rebuild Server with the isolated `OutDir` from Task 6 and calculate SHA-256 for the isolated `Server.exe`.

- [ ] **Step 4: Inspect the complete change set**

Because there is no Git metadata, record before/after SHA-256 hashes for every owned production file, list newly created files, and verify `ServerLibrary7878`, client, deployment and script trees are untouched.

- [ ] **Step 5: Manual acceptance checklist**

Open the isolated Server build against a copied test database/config only. Verify DPI/layout, arrows and sliders, save/reload, 50% baseline, live sync, pause/continue, gold top-up timing, reward audit/backfill, map/group controls, queue limits, statistics/logs and all confirmations. Do not point this build at production data without separate authorization.

Final checkpoint: report static contracts, build output, artifact path/hash, changed-file hashes, and clearly separate unperformed live production acceptance.
