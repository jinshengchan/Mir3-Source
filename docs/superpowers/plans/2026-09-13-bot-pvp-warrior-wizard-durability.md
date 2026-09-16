# 假人主动攻击、职业技能与装备耐久 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在服务端增加默认关闭的假人主动攻击真人设置，保持怪物优先，同时禁用战士野蛮冲撞、恢复战士三种蓄力攻击、让法师轮换攻击技能，并阻止假人普通装备战斗磨损。

**Architecture:** 保留现有 `ProcessBotCombat`、`BotSkillSelector`、`PlayerObject.CanAttackTarget` 和 `DamageItem` 主链，只在各自权威入口增加假人专属窄分支。主动寻人不并入受击威胁策略；技能仍通过现有 `Magic`/`Attack` 入口；持久豁免集中在统一扣减入口。

**Tech Stack:** C# 7.x、.NET Framework 4.8 WinForms 服务端、PowerShell 聚焦契约、MSBuild 2022 BuildTools。

## Global Constraints

- `Config.BotAttackPlayers` 默认必须为 `false`。
- 受击反击、攻城战、低血逃跑优先级不变；怪物始终优先于主动攻击的真人。
- 真人候选排除假人、同队、同行会和安全区目标，并继续经过 `CanAttackTarget`。
- 战士不得主动调用 `MagicType.ShoulderDash`，也不增加替代冲撞。
- 只恢复烈火剑法、莲月剑法、屠龙斩；翔空剑法及其他未点名技能保持现状。
- 法师单怪不用群攻，三只及以上优先轮换可用群攻，无群攻再轮换单攻。
- 假人药品、毒粉、护身符、火把、钓鱼装备及背包次数型物品仍正常消耗。
- 只修改规格列出的服务端与诊断文件；不修改客户端、数据库、技能数据或部署目录。
- 共享目录不是 Git 工作树：不创建分支、不提交、不复制产物到活动目录、不启动或停止服务。
- 每个生产改动前必须先运行对应新增契约并观察到目标原因的 RED。

---

## File Map

- `.diagnostics/bot-ai-pvp-warrior-wizard-durability-contract.ps1`：按 `ConfigPvp`、`Warrior`、`Wizard`、`Durability` 四个 section 检查本次行为。
- `ServerLibrary/Envir/Config.cs`：持久化默认关闭的主动攻击配置。
- `Server/Views/BotConfigView.cs`：显示、读取和保存复选框。
- `Server/BotManager.Combat.cs`：怪物优先的人类目标接入、主动攻击模式、战士蓄力与野蛮移除。
- `Server/BotSkillSelector.cs`：战士蓄力/已蓄力选择和法师轮换。
- `ServerLibrary/Models/Player/Combat.cs`：主动模式下保护假人、队友、同行会成员及其宠物。
- `ServerLibrary/Models/Player/PlayerItem.cs`：假人普通装备免战斗磨损。

## Task 1: 主动攻击配置、UI 与怪物优先目标选择

**Files:**

- Create: `.diagnostics/bot-ai-pvp-warrior-wizard-durability-contract.ps1`
- Modify: `ServerLibrary/Envir/Config.cs:2172-2197`
- Modify: `Server/Views/BotConfigView.cs:31-48,59-77,112-130,205-232,272-281,675-684`
- Modify: `Server/BotManager.Combat.cs:1055-1118,1914-2025,2095-2155`
- Modify: `ServerLibrary/Models/Player/Combat.cs:2089-2182`

**Interfaces:**

- Produces: `public static bool Config.BotAttackPlayers { get; set; } = false`
- Produces: `private static PlayerObject FindNearestBotProactiveHumanTarget(PlayerObject player)`
- Produces: `private static bool IsValidBotProactiveHumanTarget(PlayerObject player, PlayerObject target)`
- Consumes: `FindBestBotVisibleMonsterTarget`, `Functions.InRange`, `PlayerObject.InGroup`, `PlayerObject.InGuild`, `PlayerObject.CanAttackTarget`

- [ ] **Step 1: Create the focused contract harness and Config/PvP assertions**

Create a PowerShell script with `param([ValidateSet('All','ConfigPvp','Warrior','Wizard','Durability')] [string]$Section = 'All')`, the existing repository pattern for `Get-MethodBlock`, and an `Assert-Contract` collector. Load the six production files listed in File Map. Under `ConfigPvp`, assert these exact structural requirements:

```powershell
Assert-Contract ($configSource -match 'public\s+static\s+bool\s+BotAttackPlayers\s*\{\s*get;\s*set;\s*\}\s*=\s*false') 'BotAttackPlayers defaults off'
Assert-Contract ($viewSource -match 'BotAttackPlayersCheckEdit') 'Bot config view declares proactive PvP checkbox'
Assert-Contract ($viewSource -match 'BotAttackPlayersCheckEdit\.Checked\s*=\s*Config\.BotAttackPlayers') 'Bot config view loads proactive PvP setting'
Assert-Contract ($viewSource -match 'Config\.BotAttackPlayers\s*=\s*BotAttackPlayersCheckEdit\.Checked') 'Bot config view saves proactive PvP setting'
Assert-Contract ($combatSource -match 'FindNearestBotProactiveHumanTarget') 'Combat can find proactive human target'
Assert-Contract ($combatSource -match 'FindBestBotVisibleMonsterTarget[\s\S]*?FindNearestBotProactiveHumanTarget') 'Monster acquisition precedes proactive human acquisition'
Assert-Contract ($combatSource -match 'lockedTarget\.Race\s*==\s*ObjectType\.Player[\s\S]*?FindBestBotVisibleMonsterTarget') 'Visible monster can preempt proactive human target'
Assert-Contract ($combatSource -match '!target\.IsBot') 'Proactive targeting excludes bots'
Assert-Contract ($combatSource -match '!player\.InGroup\(target\)') 'Proactive targeting excludes group members'
Assert-Contract ($combatSource -match '!player\.InGuild\(target\)') 'Proactive targeting excludes guild members'
Assert-Contract ($playerCombatSource -match 'IsBot\s*&&\s*Config\.BotAttackPlayers') 'Player attack authority has bot proactive guard'
Assert-Contract ($playerCombatSource -match 'player\.IsBot[\s\S]*?InGroup\(player\)[\s\S]*?InGuild\(player\)') 'Bot proactive attack authority protects bots group and guild'
```

- [ ] **Step 2: Run Config/PvP contract and verify RED**

Run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\.diagnostics\bot-ai-pvp-warrior-wizard-durability-contract.ps1 -Section ConfigPvp
```

Expected: exit `1`; failures name the missing default config, checkbox bindings, proactive finder, monster-preemption ordering, and attack-authority protections. A syntax error or missing-file error is not an acceptable RED.

- [ ] **Step 3: Add the default-off config and checkbox binding**

In `Config.cs`, add next to `BotAllowGroup`:

```csharp
/// <summary>
/// 假人是否在没有怪物目标时主动攻击视野内的真人。
/// </summary>
public static bool BotAttackPlayers { get; set; } = false;
```

In `BotConfigView`, add `BotAttackPlayersCheckEdit`, place it on the existing settings row without moving unrelated controls, set text to `主动攻击真人`, add it to `Controls`, and bind it in both methods:

```csharp
BotAttackPlayersCheckEdit.Checked = Config.BotAttackPlayers;
```

```csharp
Config.BotAttackPlayers = BotAttackPlayersCheckEdit.Checked;
```

Do not add a restart handler: the behavior reads `Config.BotAttackPlayers` each Tick.

- [ ] **Step 4: Add narrow proactive-human eligibility and nearest-target selection**

In `BotManager.Combat.cs`, implement the two declared helpers. `IsValidBotProactiveHumanTarget` must reject null/dead/unspawned/invisible/different-map/out-of-range/self/bot/safe-map/safe-zone/group/guild candidates. `FindNearestBotProactiveHumanTarget` must scan `SEnvir.Players`, call the predicate, and choose the lowest Chebyshev distance, using `ObjectID` as the deterministic tie-breaker.

Do not call `CanAttackTarget` while the bot is still in `AttackMode.Peace`; that would incorrectly reject every proactive candidate. `CanAttackTarget` remains the final authority after the selected target causes `UpdateBotAttackMode` to choose `AttackMode.All`.

- [ ] **Step 5: Insert the target in the existing combat order**

In `ProcessBotCombat`:

```csharp
if (lockedTarget?.Race == ObjectType.Player && Config.BotAttackPlayers)
{
    MonsterObject monster = FindBestBotVisibleMonsterTarget(player, Config.MaxViewRange, true);
    if (monster != null)
    {
        lockedTarget = monster;
        _botTargets[player.ObjectID] = monster;
        _botTargetSwitchTime[player.ObjectID] = SEnvir.Now.AddSeconds(BotTargetSwitchTimeout);
    }
}
```

Place proactive human acquisition only after both existing nearby/full-view monster acquisition paths and before recovery/roam fallback:

```csharp
if (lockedTarget == null && Config.BotAttackPlayers)
{
    PlayerObject human = FindNearestBotProactiveHumanTarget(player);
    if (human != null)
    {
        lockedTarget = human;
        _botTargets[player.ObjectID] = human;
        _botTargetSwitchTime[player.ObjectID] = SEnvir.Now.AddSeconds(BotTargetSwitchTimeout);
        _botRoamTime.Remove(player.ObjectID);
    }
}
```

When the switch is turned off, invalidate a locked human only if no active `BotPvPStrategy` threat exists; this preserves retaliation.

- [ ] **Step 6: Make actual attacks legal without weakening relationship protection**

In `UpdateBotAttackMode`, after the conquest branch and before reactive-attacker handling, select `AttackMode.All` only when the tracked target is a `PlayerObject`, `Config.BotAttackPlayers` is true, and the target passes proactive eligibility.

In `PlayerObject.CanAttackTarget`, add an `IsBot && Config.BotAttackPlayers` guard inside both player-owned-pet and player branches. It must reject bot owners/players, `InGroup(...)`, and `InGuild(...)` before the normal `AttackMode` switch. Do not alter真人 logic or safe-zone/map checks.

- [ ] **Step 7: Run Config/PvP contract and focused existing PvP-sensitive checks**

Run the Config/PvP section again; expected `RESULT: PASS`. Then run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\.diagnostics\bot-ai-cpu-optimization-contract.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\.diagnostics\bot-ai-phase1-contract.ps1
```

Expected: both existing contracts exit `0`. Record exact assertion totals; do not normalize changed totals.

## Task 2: 禁用野蛮并恢复烈火、莲月、屠龙斩

**Files:**

- Modify: `.diagnostics/bot-ai-pvp-warrior-wizard-durability-contract.ps1`
- Modify: `Server/BotSkillSelector.cs:59-117,388-427,1144-1174`
- Modify: `Server/BotManager.Combat.cs:2390-2427,2558-2620`

**Interfaces:**

- Produces: `public static MagicType GetWarriorChargeMagic(PlayerObject player)`
- Produces: `private static bool IsWarriorChargeMagicReady(PlayerObject player, MagicType magicType)`
- Produces: `private static bool TryPrepareBotWarriorChargedAttack(PlayerObject player, MapObject target, MirDirection dir)`
- Consumes: `TryCastBotMagic`, `PlayerObject.Magic`, `PlayerObject.Attack`, `CanFlamingSword`, `CanBladeStorm`, `CanMaelstromBlade`

- [ ] **Step 1: Add Warrior assertions and verify RED**

Add assertions under `Warrior` that require: no `MagicType.ShoulderDash` in `BotSkillSelector.cs` or the warrior combat methods; dedicated ordered `WarriorChargedAttackPriority` containing exactly `FlamingSword`, `BladeStorm`, `MaelstromBlade`; readiness mapped to all three `Can...` flags; a charge selector using learned/level/cooldown/MP checks; and `ProcessBotWarriorCombatAction` calling `TryPrepareBotWarriorChargedAttack` before normal chase/attack.

Run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\.diagnostics\bot-ai-pvp-warrior-wizard-durability-contract.ps1 -Section Warrior
```

Expected: exit `1` for existing ShoulderDash and missing charge/selection paths.

- [ ] **Step 2: Remove the ShoulderDash path**

Delete `GetWarriorGapCloserMagic`, `TryProcessBotWarriorGapClose`, and their only call. Update only the adjacent comments so they no longer claim the bot uses野蛮. Do not remove `MagicType.ShoulderDash` from shared enums or真人 skill handlers.

- [ ] **Step 3: Add exact charged-attack selection**

Add:

```csharp
private static readonly MagicType[] WarriorChargedAttackPriority =
{
    MagicType.FlamingSword,
    MagicType.BladeStorm,
    MagicType.MaelstromBlade,
};
```

`IsMagicReady` must require the matching `CanFlamingSword`, `CanBladeStorm`, or `CanMaelstromBlade`. `GetWarriorMeleeAttackMagic` must first return a rotating ready charged attack; only when none is charged may it use the existing non-charge damage/adaptive/fallback candidates. Remove duplicate charged skills from those later candidate arrays so one decision path owns them.

- [ ] **Step 4: Add charge preparation through the existing Magic entry**

`IsWarriorChargeMagicReady` must require learned magic, `NeedLevel1`, cooldown complete, enough MP, and the corresponding `Can...` flag currently false. `GetWarriorChargeMagic` rotates only those chargeable candidates.

In `ProcessBotWarriorCombatAction`, before chasing or attacking, call `TryPrepareBotWarriorChargedAttack`. The helper returns false if any of the three charged flags is already true; otherwise it gets one charge magic and invokes `TryCastBotMagic(player, dir, magic, player, player.CurrentLocation)`. A successful charge consumes the Tick; the next eligible melee attack consumes the charged flag through existing `Attack` logic.

- [ ] **Step 5: Run Warrior section and regressions**

Expected: Warrior section passes and exact search below prints no bot-side ShoulderDash call:

```powershell
rg -n "MagicType\.ShoulderDash|GetWarriorGapCloserMagic|TryProcessBotWarriorGapClose" Server\BotSkillSelector.cs Server\BotManager.Combat.cs
```

`rg` exit `1` is expected. Then run `bot-ai-level40-assassin-contract.ps1` and `bot-ai-equipment-gold-skill-contract.ps1`; both must exit `0`.

## Task 3: 法师按单体/群体场景轮换攻击技能

**Files:**

- Modify: `.diagnostics/bot-ai-pvp-warrior-wizard-durability-contract.ps1`
- Modify: `Server/BotSkillSelector.cs:119-183,429-468,1411-1498`

**Interfaces:**

- Keeps: `public static MagicType GetWizardRangedMagic(PlayerObject player, MapObject target, int nearbyMobCount)`
- Consumes: `SelectRotatingReadyMagic`, `SelectRotatingReadySingleTargetMagic`, `IsAreaAttackMagic`

- [ ] **Step 1: Add Wizard assertions and verify RED**

Require `GetWizardRangedMagic` to contain no `SelectHighestDamageSkill` and no wizard cache lookup; require `< 3` to call `SelectRotatingReadySingleTargetMagic`; require `>= 3` to first select from area-only candidates and then fall back to single-target rotation. Keep assertions that `ProcessBotWizardCombatAction` forwards the real radius-two monster count.

Run the Wizard section. Expected: exit `1` because the current method still calls `SelectHighestDamageSkill` and does not enforce group-first rotation.

- [ ] **Step 2: Implement minimal scene-aware rotation**

Keep the current supported spell arrays. Rewrite only `GetWizardRangedMagic`:

```csharp
if (nearbyMobCount >= 3)
{
    MagicType areaMagic = SelectRotatingReadyMagic(
        player,
        WizardAdaptiveFallback.Where(IsAreaAttackMagic));
    if (areaMagic != MagicType.None)
        return areaMagic;
}

return SelectRotatingReadySingleTargetMagic(player, WizardRangedPriority);
```

Do not modify shared damage estimation because other professions still consume it. Do not add unsupported control, movement, firewall or support spells.

- [ ] **Step 3: Run Wizard and prior Taoist/Wizard contracts**

Run the new Wizard section and `.diagnostics/bot-ai-taoist-wizard-combat-priority-contract.ps1`. If the older contract asserts the superseded highest-damage policy, update only those wizard assertions to the newly approved rotation contract; preserve every Taoist, movement and fallback assertion unchanged. Observe RED for changed assertions before editing that existing contract, then rerun to GREEN.

## Task 4: 假人普通装备免战斗磨损

**Files:**

- Modify: `.diagnostics/bot-ai-pvp-warrior-wizard-durability-contract.ps1`
- Modify: `ServerLibrary/Models/Player/PlayerItem.cs:6081-6141`

**Interfaces:**

- Keeps: `public bool DamageItem(GridType grid, int slot, int rate = 1, bool delayStats = false)`
- Produces: an early return only for bot ordinary equipment slots

- [ ] **Step 1: Add Durability assertions and verify RED**

Require the complete `DamageItem` block to contain an early `IsBot && grid == GridType.Equipment` guard; require explicit exceptions for `Medicament`, `Poison`, `Amulet`, and `Torch`; require fishing equipment not to be included in the exemption. Run the Durability section and observe exit `1` because no exemption exists.

- [ ] **Step 2: Add the narrow early return**

Immediately after grid/slot resolution and before random strength/durability calculations, add:

```csharp
if (IsBot && grid == GridType.Equipment
    && slot != (int)EquipmentSlot.Medicament
    && slot != (int)EquipmentSlot.Poison
    && slot != (int)EquipmentSlot.Amulet
    && slot != (int)EquipmentSlot.Torch)
    return false;
```

Do not change `ReflushDurability`, `DamageMedicament`, amulet consumption, torch timing, fishing, NPC repair, or真人 branches.

- [ ] **Step 3: Run Durability section and equipment regression**

Run the new Durability section, then `.diagnostics/bot-ai-equipment-gold-skill-contract.ps1`. Both must exit `0`.

## Task 5: Full verification and handoff

**Files:**

- Verify only; no planned production edits

**Interfaces:**

- Consumes all four completed contract sections
- Produces exact static/build evidence and a clearly stated runtime gap

- [ ] **Step 1: Run the complete new contract**

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\.diagnostics\bot-ai-pvp-warrior-wizard-durability-contract.ps1 -Section All
```

Expected: `RESULT: PASS` and exit `0`.

- [ ] **Step 2: Run the complete existing focused regression set**

Run every command separately and record exact totals:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\.diagnostics\bot-ai-cpu-optimization-contract.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\.diagnostics\bot-ai-cpu-potion-contract.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\.diagnostics\bot-ai-phase1-contract.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\.diagnostics\bot-ai-level40-assassin-contract.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\.diagnostics\bot-ai-taoist-wizard-combat-priority-contract.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\.diagnostics\bot-ai-equipment-gold-skill-contract.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\.diagnostics\test_bot_death_revive_safezone_recovery_contract.ps1
```

Expected: every command exits `0`.

- [ ] **Step 3: Build ServerLibrary**

```powershell
dotnet build .\ServerLibrary\ServerLibrary.csproj -c Debug --no-restore
```

Expected: exit `0`, zero errors. Record warnings exactly rather than calling them new or existing without diff evidence.

- [ ] **Step 4: Build Server into isolated output/intermediate directories**

```powershell
$msbuild = 'C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\MSBuild\Current\Bin\MSBuild.exe'
& $msbuild .\Server\Server.csproj /t:Rebuild /p:Configuration=Debug /p:Platform=AnyCPU /p:OutputPath="$PWD\.build-check\bot-pvp-warrior-wizard-durability\Server\" /p:BaseIntermediateOutputPath="$PWD\.build-check\bot-pvp-warrior-wizard-durability\obj\" /m
```

Expected: exit `0`, zero compile errors, and no write to `D:\mir3\Server` or any active deployment directory.

- [ ] **Step 5: Inspect scope and temporary instrumentation**

Because the tree is non-Git, compare the recorded pre-change file metadata/hashes with post-change values and list every changed file. Confirm the list is limited to File Map plus the already approved spec/plan. Run:

```powershell
rg -n "\[DEBUG-|BotPerf|Stopwatch\.GetTimestamp" Server\BotManager.Combat.cs Server\BotSkillSelector.cs ServerLibrary\Models\Player\Combat.cs ServerLibrary\Models\Player\PlayerItem.cs
```

Any new temporary marker must be removed; pre-existing matches must be reported with evidence and left untouched.

- [ ] **Step 6: Report static completion separately from live acceptance**

Report exact contract totals, build errors/warnings, changed files, and isolated output path. State that no deployment or server restart occurred and that the six runtime scenarios listed in the approved design remain manual acceptance items.
