# 假人道士可选施毒与连续输出 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 让假人道士优先逐一实际尝试灵魂火符、月魂断玉、月魂灵波，三招均未成功时才把施毒作为补空档技能。

**Architecture:** 在 `BotSkillSelector` 中把“已就绪攻击候选”和“可选施毒选择”分开，避免施毒状态控制攻击选择。在 `ProcessBotTaoistCombatAction` 中按固定顺序逐个调用现有实际施法链，全部未成功后再执行一次可选施毒，不新增计时器、缓存或持久化状态。

**Tech Stack:** C# 7.2、.NET Framework 4.8、Mir3 Server、PowerShell 5.1 静态契约、MSBuild 17、Debug / AnyCPU。

## Global Constraints

- 只修改 `Server/BotSkillSelector.cs`、`Server/BotManager.Combat.cs`、`.diagnostics/bot-ai-taoist-wizard-combat-priority-contract.ps1`。
- 固定攻击顺序为 `ExplosiveTalisman`、`EvilSlayer`、`GreaterEvilSlayer`，不得混入其他攻击技能。
- 施毒不是门闩，只能在全部攻击候选均未成功后尝试一次。
- 保留贴身撤退、十级以上不普攻、自动装备护身符、法师现有行为。
- 不修改寻路、喝药、补给、自动学习、刺客、数据库、部署目录和现有运行进程。
- 不新增配置项、线程、计时器、高频轮询、缓存或持久化状态。
- 当前目录不是 Git 工作树；所有“提交”检查点改为记录相关文件 SHA-256。

---

### Task 1: 用专项契约锁定攻击优先和可选施毒

**Files:**
- Modify: `.diagnostics/bot-ai-taoist-wizard-combat-priority-contract.ps1`
- Test: `.diagnostics/bot-ai-taoist-wizard-combat-priority-contract.ps1`

**Interfaces:**
- Consumes: 现有 `Get-MethodBlock`、`Assert-Contract` 和 61 条专项断言。
- Produces: 对 `GetTaoistReadyDirectAttacks(PlayerObject)`、`GetTaoistOptionalPoisonMagic(PlayerObject, MapObject, int)` 以及 `ProcessBotTaoistCombatAction(...)` 新数据流的静态契约。

- [ ] **Step 1: 扩展契约的文件和方法块清单**

在 `$methodSpecs` 增加：

```powershell
'GetTaoistReadyDirectAttacks' = @{ Source = $selectorSource; Name = 'GetTaoistReadyDirectAttacks' }
'GetTaoistOptionalPoisonMagic' = @{ Source = $selectorSource; Name = 'GetTaoistOptionalPoisonMagic' }
```

保存对应 `$blocks`，供后续断言使用。

- [ ] **Step 2: 写入会因当前强制施毒链而失败的断言**

契约必须验证以下结构：

```powershell
Assert-Contract ($readyDirect -match 'foreach\s*\(\s*MagicType\s+magicType\s+in\s+TaoistDirectAttackPriority\s*\)') 'Taoist enumerates direct attacks in the requested priority order'
Assert-Contract ($readyDirect -match 'IsMagicReady\s*\(\s*player\s*,\s*magicType\s*\)[\s\S]*?yield\s+return\s+magicType') 'Taoist direct candidates contain only ready attacks'
Assert-Contract ($optionalPoison -notmatch 'SelectTalismanAttack|TaoistDirectAttackPriority|_botTaoistLastPoisonCast') 'Optional poison selection neither selects nor gates direct attacks'
Assert-Contract ($taoistCombat -match 'foreach\s*\(\s*MagicType\s+directMagic\s+in\s+BotSkillSelector\.GetTaoistReadyDirectAttacks') 'Taoist combat iterates ready direct attacks'
Assert-Contract ($taoistCombat -match 'TryProcessBotRangedCombatAction\s*\([^;]*directMagic[^;]*\)[\s\S]*?return;') 'Taoist stops after a successful direct attack or reposition'
Assert-Contract ($taoistCombat -match 'GetTaoistReadyDirectAttacks[\s\S]*?GetTaoistOptionalPoisonMagic') 'Taoist attempts optional poison only after all direct candidates'
Assert-Contract ($taoistCombat -notmatch 'GetTaoistRangedMagic\s*\(') 'Taoist combat no longer collapses direct and poison selection into one candidate'
```

同时删除或改写现有“施毒后必须先打一符才解除”的断言，改为断言三个选择方法均不读取 `_botTaoistLastPoisonCast`。

- [ ] **Step 3: 运行专项契约并确认真实 RED**

Run:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .diagnostics\bot-ai-taoist-wizard-combat-priority-contract.ps1
```

Expected: exit code `1`；新增方法块和攻击优先于可选施毒的断言失败，既有法师、贴身撤退、十级分界和护身符断言继续通过。

- [ ] **Step 4: 记录 RED 时的文件哈希**

Run:

```powershell
Get-FileHash -Algorithm SHA256 Server\BotSkillSelector.cs,Server\BotManager.Combat.cs,.diagnostics\bot-ai-taoist-wizard-combat-priority-contract.ps1
```

Expected: 输出三个明确 SHA-256；不创建 Git 提交。

---

### Task 2: 分离攻击候选与可选施毒选择

**Files:**
- Modify: `Server/BotSkillSelector.cs`
- Test: `.diagnostics/bot-ai-taoist-wizard-combat-priority-contract.ps1`

**Interfaces:**
- Consumes: `TaoistDirectAttackPriority`、`IsMagicReady(PlayerObject, MagicType)`、`GetMonsterVisualState(MapObject)`。
- Produces: `internal static IEnumerable<MagicType> GetTaoistReadyDirectAttacks(PlayerObject player)` 和 `internal static MagicType GetTaoistOptionalPoisonMagic(PlayerObject player, MapObject target, int nearbyMobCount = 0)`。

- [ ] **Step 1: 增加按固定顺序产出已就绪攻击候选的方法**

在 `SelectTalismanAttack` 附近加入：

```csharp
internal static IEnumerable<MagicType> GetTaoistReadyDirectAttacks(PlayerObject player)
{
    if (player == null || player.Dead)
        yield break;

    foreach (MagicType magicType in TaoistDirectAttackPriority)
    {
        if (IsMagicReady(player, magicType))
            yield return magicType;
    }
}
```

该方法只做就绪候选枚举，不检查施毒记录，不实际施法。

- [ ] **Step 2: 提取只负责施毒的选择方法**

把现有红毒、绿毒、药粉形状和群毒阈值判断放入：

```csharp
internal static MagicType GetTaoistOptionalPoisonMagic(PlayerObject player, MapObject target, int nearbyMobCount = 0)
```

方法规则：玩家或目标无效返回 `MagicType.None`；根据目标毒状态决定所需药粉；药粉不匹配或毒技能未就绪时返回 `MagicType.None`；群怪数量至少 3 且群毒就绪时可返回 `GreaterPoisonDust`，否则返回就绪的 `PoisonDust`。该方法不得调用 `SelectTalismanAttack`，不得读取 `_botTaoistLastPoisonCast`。

- [ ] **Step 3: 让兼容选择入口也遵守攻击优先**

将 `GetTaoistRangedMagic` 和未被战斗入口调用的 `GetTaoistAttackMagic` 收敛为相同行为：先取 `GetTaoistReadyDirectAttacks(player).FirstOrDefault()`；找到攻击技能立即返回；没有攻击候选才返回 `GetTaoistOptionalPoisonMagic(player, target, nearbyMobCount)`。不得使用数据库或共享技能缓存。

- [ ] **Step 4: 运行专项契约，确认选择器断言转绿而战斗数据流仍保持 RED**

Run:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .diagnostics\bot-ai-taoist-wizard-combat-priority-contract.ps1
```

Expected: `GetTaoistReadyDirectAttacks`、`GetTaoistOptionalPoisonMagic` 方法块和选择器断言通过；`ProcessBotTaoistCombatAction` 尚未逐个尝试攻击候选，因此整体仍 exit code `1`。

- [ ] **Step 5: 记录选择器哈希**

Run:

```powershell
Get-FileHash -Algorithm SHA256 Server\BotSkillSelector.cs
```

Expected: 输出新哈希；不创建 Git 提交。

---

### Task 3: 战斗入口逐一实际尝试攻击技能后再施毒

**Files:**
- Modify: `Server/BotManager.Combat.cs`
- Test: `.diagnostics/bot-ai-taoist-wizard-combat-priority-contract.ps1`

**Interfaces:**
- Consumes: `BotSkillSelector.GetTaoistReadyDirectAttacks(PlayerObject)`、`BotSkillSelector.GetTaoistOptionalPoisonMagic(PlayerObject, MapObject, int)`、`TryProcessBotRangedCombatAction(...)`。
- Produces: 攻击技能实际尝试顺序和可选施毒数据流。

- [ ] **Step 1: 保留贴身撤退并先逐一尝试攻击技能**

在 `ProcessBotTaoistCombatAction` 中计算 `nearbyMobCount` 后加入：

```csharp
foreach (MagicType directMagic in BotSkillSelector.GetTaoistReadyDirectAttacks(player))
{
    if (TryProcessBotRangedCombatAction(player, target, dist, dir, directMagic))
        return;
}
```

`TryRepositionBotFromImmediateRangedThreat` 必须继续位于候选循环之前。第一招实际施法返回 `false` 时自然继续下一候选。

- [ ] **Step 2: 把毒药装备和施毒移动到攻击候选之后**

保留现有目标毒状态与 `TryEquipBotTaoistPoisonForShape` 逻辑，但位置必须在攻击候选循环之后。随后只调用一次：

```csharp
MagicType optionalPoison = BotSkillSelector.GetTaoistOptionalPoisonMagic(player, target, nearbyMobCount);
if (TryProcessBotRangedCombatAction(player, target, dist, dir, optionalPoison))
    return;
```

最后保留 `ProcessBotRangedNoMagicFallback(player, target, dist, dir)`。

- [ ] **Step 3: 删除施毒门闩的解除分支**

从 `TryCastBotMagic` 删除成功释放三种攻击技能后 `_botTaoistLastPoisonCast.Remove(player.ObjectID)` 的 `else if` 分支。保留成功施毒时的次数和最近施毒记录，不让该记录参与选择或战斗控制。

- [ ] **Step 4: 运行专项契约并确认 GREEN**

Run:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .diagnostics\bot-ai-taoist-wizard-combat-priority-contract.ps1
```

Expected: exit code `0`；全部断言通过。

- [ ] **Step 5: 检查没有新增高频状态或跨范围修改**

Run:

```powershell
rg -n "Timer|Task\.Run|Thread|_botTaoistLastPoisonCast" Server\BotSkillSelector.cs Server\BotManager.Combat.cs
Get-FileHash -Algorithm SHA256 Server\BotSkillSelector.cs,Server\BotManager.Combat.cs,.diagnostics\bot-ai-taoist-wizard-combat-priority-contract.ps1
```

Expected: 不出现新计时器、线程或任务；选择器和战斗入口不读取最近施毒记录；只记录三个最终哈希。

---

### Task 4: 回归验证与 Debug / AnyCPU 独立重建

**Files:**
- Verify: `.diagnostics/bot-ai-taoist-wizard-combat-priority-contract.ps1`
- Verify: `.diagnostics/bot-ai-phase1-contract.ps1`
- Verify: `.diagnostics/bot-ai-level40-assassin-contract.ps1`
- Verify: `.diagnostics/bot-ai-cpu-potion-contract.ps1`
- Build output: `.build-check/server-taoist-optional-poison-debug-anycpu/Server.exe`

**Interfaces:**
- Consumes: Tasks 1–3 的最终源码和契约。
- Produces: GREEN 契约结果、Debug / AnyCPU 服务端产物、版本/大小/SHA-256，以及明确的未部署运行验收缺口。

- [ ] **Step 1: 并行运行核心回归契约**

Run:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .diagnostics\bot-ai-taoist-wizard-combat-priority-contract.ps1
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .diagnostics\bot-ai-phase1-contract.ps1
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .diagnostics\bot-ai-level40-assassin-contract.ps1
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .diagnostics\bot-ai-cpu-potion-contract.ps1
```

Expected: 四个命令均 exit code `0`。历史保护哈希契约不在本任务中修改或放宽。

- [ ] **Step 2: 构建 Debug ServerLibrary**

Run:

```powershell
dotnet build ServerLibrary\ServerLibrary.csproj -c Debug --no-restore
```

Expected: 0 errors。

- [ ] **Step 3: 独立重建 Debug / AnyCPU Server**

Run:

```powershell
$msbuild = 'C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\MSBuild\Current\Bin\MSBuild.exe'
$output = 'D:\相聚假人\Source\.build-check\server-taoist-optional-poison-debug-anycpu\'
$obj = 'D:\相聚假人\Source\.build-check\server-taoist-optional-poison-debug-anycpu-obj\'
New-Item -ItemType Directory -Force -Path $output,$obj | Out-Null
& $msbuild Server\Server.csproj /t:Rebuild /m /v:minimal /p:Configuration=Debug /p:Platform=AnyCPU "/p:OutputPath=$output" "/p:BaseIntermediateOutputPath=$obj"
```

Expected: exit code `0`、0 errors；仅允许报告项目既有 `MSB3277` 程序集版本冲突警告。

- [ ] **Step 4: 构建后重新运行专项契约并记录产物**

Run:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .diagnostics\bot-ai-taoist-wizard-combat-priority-contract.ps1
$artifact = '.build-check\server-taoist-optional-poison-debug-anycpu\Server.exe'
Get-Item -LiteralPath $artifact | Select-Object FullName,Length,LastWriteTime,@{Name='Version';Expression={$_.VersionInfo.FileVersion}}
Get-FileHash -Algorithm SHA256 -LiteralPath $artifact
```

Expected: 专项契约仍为 GREEN；产物存在并输出版本、大小和 SHA-256。

- [ ] **Step 5: 确认未部署并记录人工验收项**

Run:

```powershell
Get-FileHash -Algorithm SHA256 -LiteralPath 'D:\Debug\4月18日更新\Server\Server.exe'
Get-Process -Name Server -ErrorAction SilentlyContinue | Select-Object Id,StartTime
```

Expected: 本任务不覆盖部署路径、不停止或重启运行进程。最终报告人工验收缺口：观察至少一个已学会三种攻击技能的道士连续战斗，确认攻击技能优先、第一招失败会尝试后两招、施毒仅补空档且不再持续发呆。
