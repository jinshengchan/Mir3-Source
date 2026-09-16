# Taoist Consumable Supply Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox syntax for tracking. This is a shared non-Git tree; use SHA-256 checkpoints instead of commits.

**Goal:** 修复道士药粉候选购买、集中 60 秒补给边界，并让普通护身符与 Shape 0 灵魂护身符只在当前技能实际需要且库存不足时从背包换装，同时保持现有战斗 fallback、施毒记录、调度频率和低等级启动补给。

**Architecture:** 将购买、直接购买价筛选、已学道士 UseAmulet 需求和仅库存换装集中在 Server\BotManager.Support.cs；Server\BotManager.Combat.cs 只保留目标毒状态判断、必要的背包换粉、按技能换符和原有技能/近战顺序。通过 brace-depth 源结构 contract 先 RED、再 GREEN，最后执行既有回归、Debug/AnyCPU 隔离构建和人工 A/B。

**Tech Stack:** C# legacy Server/ServerLibrary；PowerShell 只读/源结构 contracts；SHA-256 文件核对；.NET Debug build；Visual Studio 2022 BuildTools MSBuild Debug/AnyCPU。

## Global Constraints

- 工作根目录固定为 D:\相聚假人\Source；项目是共享本地非 Git 树，不创建 worktree、commit、PR、备份，不执行 Git mutation。
- 本计划执行阶段的可写 ownership 仅为 Server\BotManager.Support.cs、必要的 Server\BotManager.Combat.cs、新建 .diagnostics\bot-ai-taoist-consumable-supply-contract.ps1，以及所有 focused/regression/build 通过后的 CHANGELOG.md 当前 bot-AI 相邻记录。
- 保护 D:\相聚假人\Source\Server\BotManager.cs、Server\BotSkillSelector.cs、ServerLibrary\Models\Player\PlayerItem.cs、ServerLibrary\Models\Player\Aciton.cs、所有既有 bot-ai contracts/specs/plans、数据库、资源、客户端、部署树和 D:\Debug\4月18日更新\Server\Server.exe。
- 保留 BotPotionMonitorIntervalMs=200、BotPotionRetryIntervalMs=800、BotMainSliceIntervalMs=200、四 slice 200ms 调度、约 800ms 每 bot 主行为、现有 60 秒 _botTaoistBuyTime 门控、经济价格和批量目标。
- 购买只允许发生在 ProcessBotTaoistSupply 的 60 秒门控中；战斗方法不得直接购买、枚举商店或 NPC 商品，不新增每 tick 商店扫描、线程、计时器、缓存字典、轮换状态或日志。
- 普通护身符只选择 ItemType.Amulet、Shape 1..8 的最低成功直接购买价；Resurrection 只选择 Shape 0。候选通过 ItemType/Shape 与 TryGetBotDirectBuyCost 可购买性选择，不依赖硬编码 ItemName→Shape 映射；运行时数据库内容需手工验收。
- 药粉 Shape 1 和 Shape 0 独立统计，池低于 100 时按现有约 500 补货；金币不足时按可负担数量购买；等级 <=7 的现有启动补给保持，等级 >7 不免费发放。
- 所有实际调用 UseAmulet 的已学道士技能由一个统一 requirement helper 覆盖；普通技能按 Shape 1..8，Resurrection 按 Shape 0；EvilSlayer 系列的 HolyAffinity 条件、实际消耗数量和技能选择逻辑不改变。
- 装备切换只在当前 Shape 不匹配或数量不足时扫描一次背包；当前有效装备不扫描、不切换、不购买。移除独立于目标状态的旧 20 次药粉自动轮换，但保留施毒使用计数和 _botTaoistLastPoisonCast 记录。
- 严格 TDD：生产编辑前 focused contract 必须以源行为失败 exit 1；路径/方法抽取错误使用独立的 contract error exit，不得伪装成 RED。每个生产任务后重跑 focused intermediate，最终 focused GREEN。
- 只构建 Debug；Server Debug/AnyCPU 输出固定到 D:\相聚假人\Source\.build-check\bot-ai-taoist-consumable-supply-debug\Server\。不复制、不部署、不停止、不替换旧 Server.exe。
- 执行前必须核对以下当前基线；任一受保护文件或已批准 spec 漂移，先停止并报告 baseline drift，不写入任何实现文件：
  - approved spec docs\superpowers\specs\2026-08-21-bot-ai-taoist-consumable-supply-design.md：0FBE1287251468469E7C216E5AF1A8FE6BAFCC97030DA4B040DC197E79361B15。
  - Server\BotManager.Support.cs：5827F22CAB44060E8CA45E11563873A3228EBC06E1512B582D89857690F167E1。
  - Server\BotManager.Combat.cs：7A4C3F853D85701EB4D197F7903D7C8834E06A296D6C937DD01DF22DB6DA0866。
  - Server\BotSkillSelector.cs：7539FC83A3CEDC4D947EA84C343CEABB9D249C051D881B400C9F7B76165F3AB3。
  - Server\BotManager.cs：DD57CE15664A5228B9A6670541E0C92FEBE001E25CC2B9B225CC28E41E03ACEF。
  - ServerLibrary\Models\Player\PlayerItem.cs：BA35461EC9840FDB7638CA642406047AE89FDAD17F9165EE26AEEBF65F2AC235。
  - ServerLibrary\Models\Player\Aciton.cs：C78212CB3AC0932134233A1221813600F1EFB0F31E80901B7095AEF8670FDC5A。
  - CHANGELOG.md：9BD2738D2288C4532EDDCA81FF13375409C1DB617C38B989258BE8B83291B1DA。
  - .diagnostics\bot-ai-phase1-contract.ps1：BB272684407A9C3B786237DA9049E927DFE38A1D7FBCB9BAE8F8FD18CD2F5AD9。
  - .diagnostics\bot-ai-level40-assassin-contract.ps1：14009340E7F3CED0F71A59E06D279599C9885E3ECAD265104CEC979C26F70137。
  - .diagnostics\bot-ai-cpu-potion-contract.ps1：C4C0B509223B7E512B36BE8046283B44928AA3EEC8DDB71453A1EF57817950BE。
  - .diagnostics\bot-ai-assassin-positioning-contract.ps1：63B69A5662339BF07A5F256A95642074416A1A99225992C686A284EFECEAE44C。
  - .diagnostics\bot-ai-taoist-auto-skill-contract.ps1：AA84C0C23F0C7C401AA4B03BD53BC5AFE621EAD6C4DAADBF5773478A5CCF7A03。
  - 当前旧部署 Server.exe 只读基线：83,103,744 bytes，SHA-256 D47BC3C8FEFA067DF68309D667E579F3EC5418E2E955B41E87A4BEB5F8267477；执行前和最终均需重新核对。

## File Map

| 文件 | 状态 | 唯一职责 |
| --- | --- | --- |
| Server\BotManager.Support.cs | 允许修改 | 修复 BotBuyPoisonByShape；扩展按 Shape 的直接购买；新增统一 TryGetBotTaoistAmuletRequirement(MagicType magicType, out int requiredCount, out bool requiresSoulAmulet)；驱动已学技能普通/灵魂库存池；提供仅库存换装并保留 <=7 启动补给。 |
| Server\BotManager.Combat.cs | 必要时允许修改 | 删除 ProcessBotTaoistCombatAction 内库存统计/购买/商店路径；按目标毒状态调用仅背包换粉；在 TryCastBotMagic 与 TryCastBotMagicWithPredicton 中按 magicType 换符；保留红→绿、施毒计数/记录、ranged→melee fallback。 |
| .diagnostics\bot-ai-taoist-consumable-supply-contract.ps1 | 新建 | 用 brace-depth 提取完整方法块，验证候选购买、60 秒唯一边界、统一 UseAmulet 集合/数量/Shape、mismatch-only 换装、fallback、调度常量和保护哈希。 |
| CHANGELOG.md | 最后才允许修改 | 仅在 focused/regression/build 完成后，在当前 2026-08-20 bot-AI 区域增加实际证据、assassin-positioning stale hash exception、产物和人工缺口；不得声称全部回归全绿或运行时已接受。 |
| Server\BotManager.cs | 只读保护 | 200ms/四 slice/约 800ms pipeline 和 Taoist 模块顺序。 |
| Server\BotSkillSelector.cs | 只读保护 | 道士目标毒状态、攻击技能和护身符选择；本需求不改选择器。 |
| ServerLibrary\Models\Player\PlayerItem.cs | 只读保护 | PutOnEquip 交换、RefreshStats、UsePoison 和 UseAmulet 的实际装备/消耗语义。 |
| ServerLibrary\Models\Player\Aciton.cs | 只读保护 | 所有实际 UseAmulet 技能 case、消耗数量和 Resurrection Shape 0 事实来源。 |
| 既有 contracts/specs/plans、数据库、资源、客户端、部署树、旧 Server.exe | 只读保护 | 回归证据、设计基线和已部署运行时；不得改动。 |

### Task 1: Baseline and protected-hash gate

**Files:**
- Read only: approved spec, owned source files, protected source files, all existing bot-ai contracts, CHANGELOG.md, and D:\Debug\4月18日更新\Server\Server.exe.
- Write: none.

**Interfaces:**
- Consumes: the exact baseline values in Global Constraints.
- Produces: a terminal-only baseline report; a nonzero result blocks every later task before the new contract is created.

- [ ] **Step 1: Capture every baseline hash and size before any implementation write**

Run from D:\相聚假人\Source:

~~~powershell
$root = 'D:\相聚假人\Source'
$expected = [ordered]@{
  "$root\docs\superpowers\specs\2026-08-21-bot-ai-taoist-consumable-supply-design.md" = '0FBE1287251468469E7C216E5AF1A8FE6BAFCC97030DA4B040DC197E79361B15'
  "$root\Server\BotManager.Support.cs" = '5827F22CAB44060E8CA45E11563873A3228EBC06E1512B582D89857690F167E1'
  "$root\Server\BotManager.Combat.cs" = '7A4C3F853D85701EB4D197F7903D7C8834E06A296D6C937DD01DF22DB6DA0866'
  "$root\Server\BotSkillSelector.cs" = '7539FC83A3CEDC4D947EA84C343CEABB9D249C051D881B400C9F7B76165F3AB3'
  "$root\Server\BotManager.cs" = 'DD57CE15664A5228B9A6670541E0C92FEBE001E25CC2B9B225CC28E41E03ACEF'
  "$root\ServerLibrary\Models\Player\PlayerItem.cs" = 'BA35461EC9840FDB7638CA642406047AE89FDAD17F9165EE26AEEBF65F2AC235'
  "$root\ServerLibrary\Models\Player\Aciton.cs" = 'C78212CB3AC0932134233A1221813600F1EFB0F31E80901B7095AEF8670FDC5A'
  "$root\CHANGELOG.md" = '9BD2738D2288C4532EDDCA81FF13375409C1DB617C38B989258BE8B83291B1DA'
  "$root\.diagnostics\bot-ai-phase1-contract.ps1" = 'BB272684407A9C3B786237DA9049E927DFE38A1D7FBCB9BAE8F8FD18CD2F5AD9'
  "$root\.diagnostics\bot-ai-level40-assassin-contract.ps1" = '14009340E7F3CED0F71A59E06D279599C9885E3ECAD265104CEC979C26F70137'
  "$root\.diagnostics\bot-ai-cpu-potion-contract.ps1" = 'C4C0B509223B7E512B36BE8046283B44928AA3EEC8DDB71453A1EF57817950BE'
  "$root\.diagnostics\bot-ai-assassin-positioning-contract.ps1" = '63B69A5662339BF07A5F256A95642074416A1A99225992C686A284EFECEAE44C'
  "$root\.diagnostics\bot-ai-taoist-auto-skill-contract.ps1" = 'AA84C0C23F0C7C401AA4B03BD53BC5AFE621EAD6C4DAADBF5773478A5CCF7A03'
}
$failed = $false
foreach ($path in $expected.Keys) {
  if (-not (Test-Path -LiteralPath $path)) {
    Write-Host "MISSING $path"
    $failed = $true
    continue
  }
  $item = Get-Item -LiteralPath $path
  $actual = (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash
  Write-Host ("BASELINE {0} {1} bytes {2}" -f $path, $item.Length, $actual)
  if ($actual -ne $expected[$path]) {
    Write-Host ("DRIFT {0} expected {1} actual {2}" -f $path, $expected[$path], $actual)
    $failed = $true
  }
}
$oldServer = 'D:\Debug\4月18日更新\Server\Server.exe'
if (-not (Test-Path -LiteralPath $oldServer)) {
  Write-Host "MISSING $oldServer"
  $failed = $true
} else {
  $oldItem = Get-Item -LiteralPath $oldServer
  $oldHash = (Get-FileHash -LiteralPath $oldServer -Algorithm SHA256).Hash
  Write-Host ("OLD_SERVER {0} bytes {1}" -f $oldItem.Length, $oldHash)
  if ($oldItem.Length -ne 83103744 -or $oldHash -ne 'D47BC3C8FEFA067DF68309D667E579F3EC5418E2E955B41E87A4BEB5F8267477') {
    Write-Host "DRIFT old deployed Server.exe"
    $failed = $true
  }
}
if ($failed) { exit 21 }
Write-Host 'BASELINE_GATE PASS'
exit 0
~~~

Expected: exit 0, every listed hash matches, and the old deployed binary is exactly 83,103,744 bytes with SHA-256 D47BC3C8FEFA067DF68309D667E579F3EC5418E2E955B41E87A4BEB5F8267477. A mismatch is baseline drift and requires stopping before any write; do not normalize or overwrite the drift.

- [ ] **Step 2: Capture a read-only Server process snapshot without controlling the process**

Run:

~~~powershell
$snapshot = Get-Process -Name Server -ErrorAction SilentlyContinue |
  Select-Object Id, ProcessName, StartTime, CPU, WorkingSet64, PrivateMemorySize64, Threads, Handles
if ($null -eq $snapshot) {
  Write-Host 'NO_RUNNING_SERVER_PROCESS'
} else {
  $snapshot | Format-List
}
~~~

Expected: either a metadata-only snapshot or NO_RUNNING_SERVER_PROCESS. Do not stop, start, attach to, replace, or deploy a process. The snapshot is evidence only and does not change the baseline gate.

### Task 2: Create the focused brace-depth contract and obtain genuine RED

**Files:**
- Create: D:\相聚假人\Source\.diagnostics\bot-ai-taoist-consumable-supply-contract.ps1
- Read only: Server\BotManager.Support.cs, Server\BotManager.Combat.cs, protected source files, existing contracts, and the approved spec.
- Write: no production source, no existing contract, no CHANGELOG, no plan/spec other than this plan.

**Interfaces:**
- Consumes: the exact source method names and protected hashes from Task 1.
- Produces: exit 1 for the current source-behavior RED; exit 0 only after the approved Support/Combat implementation satisfies every focused assertion; exit 2 for path, extraction, or protected-baseline errors.

- [ ] **Step 1: Create the contract with a complete brace-depth method extractor**

The new PowerShell contract must load only the two owned source files and use a complete method-block extractor. The extractor must locate a method signature, find its first opening brace, count every opening and closing brace until depth returns to zero, and return the entire block. It must not use a regex that stops at the first nested brace or spans an unrelated caller.

Use this executable helper shape in the contract:

~~~powershell
$root = Split-Path -Parent $PSScriptRoot
$supportPath = Join-Path $root 'Server\BotManager.Support.cs'
$combatPath = Join-Path $root 'Server\BotManager.Combat.cs'
$support = Get-Content -LiteralPath $supportPath -Raw
$combat = Get-Content -LiteralPath $combatPath -Raw

function Get-MethodBlock {
  param(
    [Parameter(Mandatory = $true)][string]$Text,
    [Parameter(Mandatory = $true)][string]$MethodName
  )
  $escaped = [regex]::Escape($MethodName)
  $signature = [regex]::Match(
    $Text,
    '(?ms)(?:^|\r?\n)\s*(?:private|internal|public|protected)\s+(?:static\s+)?[^{;\r\n]+\b' + $escaped + '\s*\('
  )
  if (-not $signature.Success) { return $null }
  $open = $Text.IndexOf('{', $signature.Index)
  if ($open -lt 0) { return $null }
  $depth = 0
  for ($i = $open; $i -lt $Text.Length; $i++) {
    if ($Text[$i] -eq '{') { $depth++ }
    elseif ($Text[$i] -eq '}') {
      $depth--
      if ($depth -eq 0) {
        return $Text.Substring($signature.Index, $i - $signature.Index + 1)
      }
    }
  }
  return $null
}

function Get-ActiveText {
  param([Parameter(Mandatory = $true)][string]$Text)
  return (($Text -split '\r?\n' | ForEach-Object {
    if ($_ -match '^\s*//') { '' } else { $_ -replace '//.*$', '' }
  }) -join ([Environment]::NewLine))
}

$blocks = @{
  BotBuyPoisonByShape = Get-MethodBlock $support 'BotBuyPoisonByShape'
  BotBuyConsumable = Get-MethodBlock $support 'BotBuyConsumable'
  ProcessBotTaoistSupply = Get-MethodBlock $support 'ProcessBotTaoistSupply'
  ProcessBotTaoistEquipSupply = Get-MethodBlock $support 'ProcessBotTaoistEquipSupply'
  TryGrantTaoistStarterConsumable = Get-MethodBlock $support 'TryGrantTaoistStarterConsumable'
  ProcessBotTaoistCombatAction = Get-MethodBlock $combat 'ProcessBotTaoistCombatAction'
  TryCastBotMagic = Get-MethodBlock $combat 'TryCastBotMagic'
  TryCastBotMagicWithPredicton = Get-MethodBlock $combat 'TryCastBotMagicWithPredicton'
}
if ($blocks.Values | Where-Object { $null -eq $_ }) {
  Write-Error 'CONTRACT_ERROR: required method block extraction failed'
  exit 2
}
~~~

Expected: all eight current method blocks are extracted completely. A missing block, malformed brace depth, or missing source file is exit 2 and is not a valid RED.

- [ ] **Step 2: Add the named assertion runner and protected-file checks**

Use a counter-based runner so every assertion has a stable failure name:

~~~powershell
$pass = 0
$fail = 0
function Assert-Source {
  param([string]$Name, [bool]$Condition)
  if ($Condition) {
    $script:pass++
    Write-Host "PASS $Name"
  } else {
    $script:fail++
    Write-Host "FAIL $Name"
  }
}
function Active-Has {
  param([string]$Block, [string]$Pattern)
  return [bool]([regex]::IsMatch((Get-ActiveText $Block), $Pattern))
}
function Active-NotHas {
  param([string]$Block, [string]$Pattern)
  return -not (Active-Has $Block $Pattern)
}
~~~

The contract must hash-check the protected BotManager.cs, BotSkillSelector.cs, PlayerItem.cs, Aciton.cs, approved spec, and all five existing bot-ai contracts against Task 1 values. A protected hash mismatch prints PROTECTED_HASH_FAIL and exits 2 after reporting assertions; it must not be counted as a source RED. Do not fixed-hash Support.cs, Combat.cs, or CHANGELOG.md because those are later owned outputs.

- [ ] **Step 3: Add the initial RED assertion inventory**

The contract must contain these individually named source assertions. Current source is expected to fail only the behavior assertions listed as RED below; the existing target/fallback/recording/protection assertions are expected to pass.

1. Poison candidate:
   - BotBuyPoisonByShape has an active if (!TryGetBotDirectBuyCost(info, out long directCost)) continue.
   - BotBuyPoisonByShape has active assignments bestPrice = directCost; and bestInfo = info; inside the lower-price branch.
   - Its filter retains ItemType.Poison and exact requested Shape.
2. Shape-bounded amulet purchase:
   - BotBuyConsumable exposes minShape/maxShape bounds and filters ItemType.Amulet candidates by those bounds.
   - It accepts only successful TryGetBotDirectBuyCost results and keeps the existing affordable-count, CanGainItems, ChangeBotGoldSilently, CreateFreshItem, GainItem and rollback sequence.
3. Unified requirement:
   - Server\BotManager.Support.cs contains the exact helper signature TryGetBotTaoistAmuletRequirement(MagicType magicType, out int requiredCount, out bool requiresSoulAmulet).
   - The helper covers every current UseAmulet skill from the approved spec: ExplosiveTalisman, ImprovedExplosiveTalisman, EvilSlayer, GreaterEvilSlayer, GreaterHolyStrike, MagicResistance, ElementalSuperiority, SummonSkeleton, Neutralize, Resilience, BloodLust, LifeSteal, TrapOctagon, SummonJinSkeleton, Invisibility, MassTransparency, MassInvisibility, Purification, SummonShinsu, StrengthOfFaith, Transparency, CelestialLight, DemonExplosion, SummonDemonicCreature, and Resurrection.
   - The requirement counts are 1/2/5/10/20/25 as specified; Resurrection alone returns requiresSoulAmulet=true and Shape 0 is represented by that mode.
4. Supply boundary:
   - ProcessBotTaoistSupply retains the _botTaoistBuyTime 60-second gate and independent <100 checks for powder Shape 1 and Shape 0.
   - It iterates learned player.Magics through the unified helper instead of a five-skill literal list.
   - It buys ordinary amulets only in Shape 1..8 and soul amulets only in Shape 0, without a fixed rotation or eight-shape stockpile.
   - TryGrantTaoistStarterConsumable still guards player.Level > 7, requires an inventory null slot, and keeps the existing count-50 path.
5. Equipment boundary:
   - A context-aware inventory-only amulet helper exists and is used for the exact magic type; it accepts Shape 1..8 for ordinary skills and Shape 0 for Resurrection.
   - A valid nonempty Shape 0 equipped item is not replaced by contextless ProcessBotTaoistEquipSupply.
   - Inventory scanning occurs only after current Shape/count mismatch; no purchase helper is called by an equipment helper.
   - The old independent 20-use poison flip is absent; the existing poison count and last-cast record remain.
6. Combat:
   - ProcessBotTaoistCombatAction contains no BotBuyPoisonByShape, BotBuyConsumable, TryGetBotDirectBuyCost, SEnvir.ItemInfoList, NPC-good enumeration, or direct purchase call.
   - It retains target-state ordering if (!hasRedPoison) targetShape = 1 before else if (!hasGreenPoison) targetShape = 0.
   - It retains the ranged selector call and ProcessBotMeleeCombatAction fallback.
   - TryCastBotMagic and TryCastBotMagicWithPredicton use the unified requirement and inventory-only amulet helper before casting.
   - TryCastBotMagic retains _botTaoistPoisonUseCount increment and _botTaoistLastPoisonCast recording.
7. Frequency/protection:
   - BotPotionMonitorIntervalMs=200 and BotPotionRetryIntervalMs=800 remain in Combat.cs and BotManager.cs protected hashes remain unchanged.
   - No new Taoist Dictionary, thread, timer, rotation state, cache, or log call is introduced in the owned source.

The current genuine RED must include the current commented poison assignments and missing failed-cost continue, the absent shape-bounded purchase, the five-skill supply trigger, the absent unified helper/Shape 0 route, the combat purchase calls, the unconditional Shape 0 replacement risk, the 20-use flip, and the missing context-aware cast calls. It must not fail because a method block was not extracted or because a path was misspelled.

- [ ] **Step 4: Run the new contract before any production edit**

Run from D:\相聚假人\Source:

~~~powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .diagnostics\bot-ai-taoist-consumable-supply-contract.ps1
~~~

Expected: exit 1; output contains PASS/FAIL counts and only the named initial source-behavior failures. There must be no CONTRACT_ERROR, PROTECTED_HASH_FAIL, command-not-found error, or parser error. Preserve the complete output in the task record. If exit is 0, the contract is not genuine RED and production edits are forbidden until the contract is corrected. If exit is 2 or any failure is outside the inventory above, stop and report BLOCKED without modifying source.

- [ ] **Step 5: Record a non-Git hash checkpoint after RED**

Run:

~~~powershell
Get-FileHash -LiteralPath '.diagnostics\bot-ai-taoist-consumable-supply-contract.ps1' -Algorithm SHA256
~~~

Expected: the new contract has a recorded SHA-256; all Task 1 protected hashes still match. Do not commit, push, create a PR, or modify any file other than the new focused contract in this task.

### Task 3: Support-layer purchase, requirement, supply, and inventory-only equipment

**Files:**
- Modify only: D:\相聚假人\Source\Server\BotManager.Support.cs
- Test: D:\相聚假人\Source\.diagnostics\bot-ai-taoist-consumable-supply-contract.ps1
- Protect: Server\BotManager.Combat.cs, BotManager.cs, BotSkillSelector.cs, PlayerItem.cs, Aciton.cs, existing contracts, CHANGELOG.md, specs, plans, binaries, and deployment files.

**Interfaces:**
- Consumes: Task 2 RED assertions and the existing TryGetBotDirectBuyCost, ChangeBotGoldSilently, CanGainItems, CreateFreshItem, GainItem, FindEmptyInventorySlot, PutOnEquip, _botTaoistBuyTime, _botTaoistPoisonUseCount, and _botTaoistLastPoisonCast symbols.
- Produces: a Support implementation that owns all purchasing and exposes inventory-only shape-aware equipment behavior for the later Combat task.
- Required signatures:
  - private static bool TryGetBotTaoistAmuletRequirement(MagicType magicType, out int requiredCount, out bool requiresSoulAmulet)
  - private static int GetBotTaoistConsumableCount(PlayerObject player, ItemType type, int minShape, int maxShape)
  - private static void BotBuyConsumable(PlayerObject player, ItemType type, int minShape, int maxShape, int count, bool allowStarterSupply)
  - private static bool TryEquipBotTaoistPoisonForShape(PlayerObject player, int targetShape)
  - private static bool TryEquipBotTaoistAmuletForMagic(PlayerObject player, MagicType magicType)
  - existing private static void BotBuyPoisonByShape(PlayerObject player, int shape, int count)
  - existing private static void ProcessBotTaoistSupply(PlayerObject player)
  - existing private static void ProcessBotTaoistEquipSupply(PlayerObject player)

- [ ] **Step 1: Fix only the active poison candidate selection**

Use apply_patch in BotManager.Support.cs inside BotBuyPoisonByShape. Keep the ItemType.Poison filter, exact shape filter, existing batch/count calculation, affordability reduction, CanGainItems loop, gold deduction, CreateFreshItem, GainItem, exception rollback, and <=7 starter fallback. Replace the commented candidate behavior with this active structure:

~~~csharp
if (!TryGetBotDirectBuyCost(info, out long directCost))
    continue;
if (directCost <= 0)
    continue;

if (directCost < bestPrice)
{
    bestPrice = directCost;
    bestInfo = info;
}
~~~

Do not add an item-name check, change a fallback price, change the requested count, or move this method into the combat path. The method must return safely when bestInfo is null or bestPrice is not positive before multiplying or dereferencing either value.

- [ ] **Step 2: Run the focused contract at the first Support checkpoint**

Run from D:\相聚假人\Source:

~~~powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .diagnostics\bot-ai-taoist-consumable-supply-contract.ps1
~~~

Expected: exit 1, with the poison successful-cost continue and active bestPrice/bestInfo assertions PASS. The remaining failures must be limited to the not-yet-implemented shape-bounded amulet purchase, unified requirement, supply expansion, context-aware equipment, and Combat purchase-removal assertions. Any extraction, parser, protection-hash, or unexpected behavior failure blocks the next edit.

- [ ] **Step 3: Add one shape-range purchase implementation without changing the transaction semantics**

Change the Support-only BotBuyConsumable signature to:

~~~csharp
private static void BotBuyConsumable(
    PlayerObject player,
    ItemType type,
    int minShape,
    int maxShape,
    int count,
    bool allowStarterSupply)
~~~

Keep the current candidate loop and transaction order, adding only the shape range and the explicit direct-cost success gate:

~~~csharp
foreach (ItemInfo info in SEnvir.ItemInfoList.Binding)
{
    if (info == null || info.ItemType != type)
        continue;
    if (info.Shape < minShape || info.Shape > maxShape)
        continue;
    if (!TryGetBotDirectBuyCost(info, out long directCost))
        continue;
    if (directCost <= 0 || directCost >= bestPrice)
        continue;

    bestPrice = directCost;
    bestInfo = info;
}
~~~

After candidate selection retain, in order, bestInfo/bestPrice guard, total cost calculation, affordable-count reduction, CanGainItems decrement loop, ChangeBotGoldSilently, CreateFreshItem, GainItem, and exception gold rollback. Invoke TryGrantTaoistStarterConsumable only when allowStarterSupply is true and the existing <=7 conditions are met. The ordinary Shape 1..8 call passes true to preserve the existing starter semantics; the Shape 0 soul-amulet call passes false so a missing soul amulet never becomes a new free-item path. Do not alter item prices, NPC/fallback rates, stack sizes, or gold support.

- [ ] **Step 4: Run the focused contract at the shape-purchase checkpoint**

Run the same focused command.

Expected: exit 1; poison assertions and shape-bounded direct-cost candidate assertions PASS. The existing five-skill trigger, unified helper, Shape 0 equipment, contextless Shape 0 protection, and Combat purchase assertions remain the only relevant failures. No failure may mention the transaction order, affordable count, rollback, or starter level guard.

- [ ] **Step 5: Add the single source of truth for every actual UseAmulet skill**

Replace the count-only Taoist amulet switch with the required helper. Initialize both out parameters before the switch and return false for non-UseAmulet magic. Use these exact groups and values:

~~~csharp
private static bool TryGetBotTaoistAmuletRequirement(
    MagicType magicType,
    out int requiredCount,
    out bool requiresSoulAmulet)
{
    requiredCount = 0;
    requiresSoulAmulet = false;

    switch (magicType)
    {
        case MagicType.ExplosiveTalisman:
        case MagicType.ImprovedExplosiveTalisman:
        case MagicType.EvilSlayer:
        case MagicType.GreaterEvilSlayer:
        case MagicType.GreaterHolyStrike:
        case MagicType.MagicResistance:
        case MagicType.ElementalSuperiority:
        case MagicType.SummonSkeleton:
        case MagicType.Neutralize:
            requiredCount = 1;
            return true;

        case MagicType.Resilience:
        case MagicType.BloodLust:
        case MagicType.LifeSteal:
        case MagicType.TrapOctagon:
        case MagicType.SummonJinSkeleton:
        case MagicType.Invisibility:
        case MagicType.MassTransparency:
        case MagicType.MassInvisibility:
        case MagicType.Purification:
            requiredCount = 2;
            return true;

        case MagicType.SummonShinsu:
        case MagicType.StrengthOfFaith:
            requiredCount = 5;
            return true;

        case MagicType.Transparency:
        case MagicType.CelestialLight:
            requiredCount = 10;
            return true;

        case MagicType.DemonExplosion:
            requiredCount = 20;
            return true;

        case MagicType.SummonDemonicCreature:
            requiredCount = 25;
            return true;

        case MagicType.Resurrection:
            requiredCount = 1;
            requiresSoulAmulet = true;
            return true;

        default:
            return false;
    }
}
~~~

Keep the Aciton.cs HolyAffinity condition in the actual spell path; this helper only declares the source-verified UseAmulet requirement and does not make an EvilSlayer-family spell consume an amulet when Aciton.cs would not. Do not add Action, School, NeedLevel, database-name, or resistance filters.

- [ ] **Step 6: Add one non-cached pool counter and update the 60-second supply method**

Implement GetBotTaoistConsumableCount as a one-call count of equipped plus inventory items whose ItemType matches and whose Shape is within the inclusive range. For the equipment slot, include the current equipped Poison for ItemType.Poison or Amulet for ItemType.Amulet; for the inventory, sum only non-null items with positive Count. Do not create a cache or dictionary.

Keep the existing ProcessBotTaoistSupply null/dead/class guards, set _botTaoistBuyTime to SEnvir.Now.AddSeconds(60) at the existing gate, and preserve independent powder checks. Replace only the five-skill amulet literal with this flow:

~~~csharp
bool needsNormalAmulet = false;
bool needsSoulAmulet = false;
foreach (MagicType magicType in player.Magics.Keys)
{
    if (!TryGetBotTaoistAmuletRequirement(
            magicType,
            out int requiredCount,
            out bool requiresSoulAmulet))
        continue;

    if (requiresSoulAmulet)
        needsSoulAmulet = true;
    else
        needsNormalAmulet = true;
}

if (needsNormalAmulet
    && GetBotTaoistConsumableCount(player, ItemType.Amulet, 1, 8) < BotTaoistSupplyMinCount)
{
    BotBuyConsumable(
        player,
        ItemType.Amulet,
        1,
        8,
        BotTaoistSupplyBuyCount,
        true);
}

if (needsSoulAmulet
    && GetBotTaoistConsumableCount(player, ItemType.Amulet, 0, 0) < BotTaoistSupplyMinCount)
{
    BotBuyConsumable(
        player,
        ItemType.Amulet,
        0,
        0,
        BotTaoistSupplyBuyCount,
        false);
}
~~~

The powder part remains two independent total-count checks: Shape 1 below 100 calls BotBuyPoisonByShape(player, 1, BotTaoistSupplyBuyCount), and Shape 0 below 100 calls BotBuyPoisonByShape(player, 0, BotTaoistSupplyBuyCount). The ordinary and soul amulet pools are separate; no eight-shape rotation or monster-resistance selection is introduced. The existing TryGrantTaoistStarterConsumable remains level <=7, requires at least one null inventory slot, requires zero current/inventory count for its type, creates 50, GainItem calls ProcessBotTaoistEquipSupply, and catches failure. No free path is allowed for level >7 or for the Shape 0 supply call.

- [ ] **Step 7: Run the focused contract at the unified-supply checkpoint**

Run the same focused command.

Expected: exit 1 until Combat is changed, but the unified helper signature, complete skill list, count groups, Resurrection soul mode, learned-magic iteration, normal/soul pool ranges, independent 100 thresholds, 500 purchase count, 60-second gate, and starter assertions PASS. Any failure in Support purchase safety or supply semantics blocks the equipment edit.

- [ ] **Step 8: Add inventory-only mismatch helpers and make contextless equipment Shape 0 safe**

Implement TryEquipBotTaoistPoisonForShape with this behavior:

~~~csharp
private static bool TryEquipBotTaoistPoisonForShape(PlayerObject player, int targetShape)
{
    if (player == null || player.Dead || player.Class != MirClass.Taoist)
        return false;

    UserItem equipped = player.Equipment[(int)EquipmentSlot.Poison];
    if (equipped?.Info?.ItemType == ItemType.Poison
        && equipped.Count > 0
        && equipped.Info.Shape == targetShape)
        return true;

    for (int i = 0; i < player.Inventory.Length; i++)
    {
        UserItem candidate = player.Inventory[i];
        if (candidate?.Info?.ItemType != ItemType.Poison
            || candidate.Count <= 0
            || candidate.Info.Shape != targetShape)
            continue;
        if (equipped != null && FindEmptyInventorySlot(player) < 0)
            return false;
        try
        {
            player.PutOnEquip(candidate, (int)EquipmentSlot.Poison);
            return player.Equipment[(int)EquipmentSlot.Poison]?.Info?.Shape == targetShape
                   && player.Equipment[(int)EquipmentSlot.Poison].Count > 0;
        }
        catch (Exception)
        {
            return false;
        }
    }
    return false;
}
~~~

Implement TryEquipBotTaoistAmuletForMagic so it calls the unified requirement, accepts Shape 0 only when requiresSoulAmulet is true, accepts Shape 1..8 otherwise, returns true without scanning when the equipped item has the required ItemType, range, and requiredCount, and otherwise scans the inventory once for a matching positive-count item. If an existing equipped item must be exchanged and FindEmptyInventorySlot returns -1, return false before mutation. Use PutOnEquip in the try block and verify the resulting equipment slot; never call BotBuyPoisonByShape, BotBuyConsumable, TryGetBotDirectBuyCost, or any NPC/shop enumeration from either helper.

Change ProcessBotTaoistEquipSupply so a nonempty Shape 0 amulet is not treated as invalid merely because the method lacks a magic context. It may equip an amulet only when the slot is null or Count <= 0, and the context-aware helper owns all ordinary-versus-soul decisions. Preserve its existing empty-poison recovery, but remove the block that tests _botTaoistPoisonUseCount against BotTaoistPoisonSwitchThreshold and flips to the opposite Shape after 20 casts. Remove the now-unused threshold constant and its stale switching comment; keep _botTaoistPoisonUseCount and _botTaoistLastPoisonCast declarations and the TryCastBotMagic recording path unchanged for the later Combat task.

- [ ] **Step 9: Run the focused contract at the completed Support checkpoint**

Run the same focused command.

Expected: exit 1 because ProcessBotTaoistCombatAction still contains its pre-existing direct purchase calls and TryCastBotMagic/TryCastBotMagicWithPredicton still use the old count-only/contextless path. All Support assertions PASS, including active poison selection, shape-bounded purchase with affordability/rollback, complete requirement map, 60-second supply, <=7 starter semantics, mismatch-only inventory scans, safe Shape 0 preservation, removal of the 20-use flip, and retention of poison count/record symbols. Stop if any other failure appears; do not edit Combat or the contract to hide a failure.

### Task 4: Remove Combat purchase paths and connect inventory-only context

**Files:**
- Modify only: D:\相聚假人\Source\Server\BotManager.Combat.cs
- Test: D:\相聚假人\Source\.diagnostics\bot-ai-taoist-consumable-supply-contract.ps1
- Protect: BotManager.Support.cs after Task 3, BotManager.cs, BotSkillSelector.cs, PlayerItem.cs, Aciton.cs, existing contracts, CHANGELOG.md, specs, plans, binaries, and deployment files.

**Interfaces:**
- Consumes: TryEquipBotTaoistPoisonForShape(PlayerObject player, int targetShape), TryGetBotTaoistAmuletRequirement(MagicType magicType, out int requiredCount, out bool requiresSoulAmulet), and TryEquipBotTaoistAmuletForMagic(PlayerObject player, MagicType magicType) from Support.
- Produces: a Combat path with no purchase/shop calls, target-driven red-then-green poison switching, context-correct amulet switching in both cast paths, preserved poison records, and preserved ranged-to-melee fallback.

- [ ] **Step 1: Replace the high-frequency Combat powder purchase block**

In ProcessBotTaoistCombatAction(PlayerObject player, MapObject target, int dist, MirDirection dir, bool forcePhysicalFallback), remove the block that counts equipped/inventory powders and calls BotBuyPoisonByShape when Gold >= 100. Do not replace it with another inventory-wide count on every tick.

Keep the target state logic and call the Support inventory-only helper only when a target Shape is required:

~~~csharp
int targetShape = -1;
if (!hasRedPoison)
    targetShape = 1;
else if (!hasGreenPoison)
    targetShape = 0;

if (targetShape >= 0)
    TryEquipBotTaoistPoisonForShape(player, targetShape);
~~~

The helper must perform its own current-equipment fast path and one inventory scan only on mismatch or shortage. ProcessBotTaoistCombatAction must contain no BotBuyPoisonByShape, BotBuyConsumable, TryGetBotDirectBuyCost, SEnvir.ItemInfoList, NPC-good enumeration, direct gold deduction, or purchase fallback. It must not clear a valid target or return before the existing ranged selector, attack selector, and ProcessBotMeleeCombatAction fallback.

- [ ] **Step 2: Run the focused contract after removing Combat powder purchase**

Run:

~~~powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .diagnostics\bot-ai-taoist-consumable-supply-contract.ps1
~~~

Expected: exit 1 only because the two cast paths still use the old GetBotRequiredTaoistAmuletCount/ProcessBotTaoistEquipSupply route. The Combat no-purchase, red-before-green, ranged-to-melee, and poison-record assertions must PASS. Any remaining Combat purchase or target-order failure blocks the cast-path edit.

- [ ] **Step 3: Connect TryCastBotMagic to the unified magic-type amulet helper**

In TryCastBotMagic(PlayerObject player, MirDirection dir, MagicType magicType, MapObject target = null, Point? location = null), replace only the old count-only/contextless amulet precheck with:

~~~csharp
if (TryGetBotTaoistAmuletRequirement(
        magicType,
        out int requiredAmuletCount,
        out bool requiresSoulAmulet))
{
    if (!TryEquipBotTaoistAmuletForMagic(player, magicType))
        return false;

    UserItem equippedAmulet = player.Equipment[(int)EquipmentSlot.Amulet];
    int requiredShapeMin = requiresSoulAmulet ? 0 : 1;
    int requiredShapeMax = requiresSoulAmulet ? 0 : 8;
    if (equippedAmulet?.Info?.ItemType != ItemType.Amulet
        || equippedAmulet.Count < requiredAmuletCount
        || equippedAmulet.Info.Shape < requiredShapeMin
        || equippedAmulet.Info.Shape > requiredShapeMax)
        return false;
}
~~~

The helper itself remains the only inventory scan and does not buy. Keep all existing CanCast, PacketWaiting, ActionList, learned-level, cooldown, MP, direction, Magic call, cooldown-success, and RecordBotMagicCastResult behavior. Keep the isPoisonSkill block that increments _botTaoistPoisonUseCount and records _botTaoistLastPoisonCast with target ID, SEnvir.Now, and equipped Shape.

- [ ] **Step 4: Apply the same context connection to the predicted cast path**

In TryCastBotMagicWithPredicton(PlayerObject player, MirDirection dir, MagicType magicType, MapObject target, Point predictedLocation), make the identical requirement/helper change. Keep its predicted location, target validation, cooldown, MP, Magic call, and existing return behavior unchanged. Do not add a second requirement switch or a second purchase path.

- [ ] **Step 5: Run the focused contract for GREEN**

Run:

~~~powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .diagnostics\bot-ai-taoist-consumable-supply-contract.ps1
~~~

Expected: exit 0. Every focused assertion passes, including:

- successful direct-cost-only cheapest candidate selection for powder and Shape-bounded amulet purchase;
- independent Shape 1/Shape 0 powder pools and ordinary Shape 1..8/Resurrection Shape 0 amulet pools under the one 60-second gate;
- complete UseAmulet skill/count/Shape requirement map;
- <=7 starter semantics and no >7 free item path;
- mismatch-only inventory scans and no contextless replacement of valid Shape 0;
- no Combat purchase/shop enumeration;
- red-before-green target switching, poison counter/last-cast record, and ranged-to-melee fallback;
- unchanged 200ms/800ms scheduler/potion constants and protected hashes.

If exit is not 0, stop before regression or build work. Do not weaken an assertion, fixed hash, or existing contract to obtain GREEN.

### Task 5: Run focused and existing regressions, then build isolated Debug/AnyCPU artifacts

**Files:**
- Read only: all owned/protected source, all contracts, and build output.
- Write: no source, contract, spec, plan, CHANGELOG, deployment file, or binary outside the permitted isolated build output.

**Interfaces:**
- Consumes: Task 4 focused GREEN.
- Produces: regression output, warning/error counts, isolated Server.exe evidence, and no deployment action.

- [ ] **Step 1: Re-run the focused contract and the five existing bot-AI contracts in fixed order**

Run from D:\相聚假人\Source:

~~~powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .diagnostics\bot-ai-taoist-consumable-supply-contract.ps1
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .diagnostics\bot-ai-taoist-auto-skill-contract.ps1
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .diagnostics\bot-ai-phase1-contract.ps1
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .diagnostics\bot-ai-level40-assassin-contract.ps1
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .diagnostics\bot-ai-cpu-potion-contract.ps1
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .diagnostics\bot-ai-assassin-positioning-contract.ps1
~~~

Expected:

- New focused contract: exit 0, all assertions PASS.
- bot-ai-taoist-auto-skill: 36 PASS.
- bot-ai-phase1: 21 PASS.
- bot-ai-level40-assassin: 6 PASS.
- bot-ai-cpu-potion: 21 PASS.
- bot-ai-assassin-positioning: 11/12, with exactly one explained failure from its stale fixed BotManager.Support.cs ownership hash; all 11 behavior/protection assertions pass. Do not modify or weaken that contract and do not describe this result as all regressions green.

Any new assertion failure, parser failure, path error, or protected hash failure stops the task before building.

- [ ] **Step 2: Build ServerLibrary in Debug and record exact warning/error counts**

Run:

~~~powershell
& 'C:\Program Files\dotnet\dotnet.exe' build 'ServerLibrary\ServerLibrary.csproj' -c Debug --nologo
~~~

Expected: exit 0 and 0 compile errors. Record the exact warning count and the full command result. Do not use Release and do not publish or copy the output.

- [ ] **Step 3: Rebuild Server Debug/AnyCPU into the isolated directory**

Run:

~~~powershell
& 'C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\MSBuild\Current\Bin\MSBuild.exe' 'Server\Server.csproj' /t:Rebuild /m /v:minimal /p:Configuration=Debug /p:Platform=AnyCPU '/p:OutputPath=D:\相聚假人\Source\.build-check\bot-ai-taoist-consumable-supply-debug\Server\'
~~~

Expected: exit 0, 0 compile errors, and the exact warning count recorded. If the app layer times out, inspect only the build process and isolated artifact with Get-Process/Get-Item before considering a retry; do not blindly rerun. A real compiler failure stops the task.

- [ ] **Step 4: Verify the isolated artifact without deployment**

Run:

~~~powershell
$artifact = 'D:\相聚假人\Source\.build-check\bot-ai-taoist-consumable-supply-debug\Server\Server.exe'
if (-not (Test-Path -LiteralPath $artifact)) { exit 31 }
$item = Get-Item -LiteralPath $artifact
$hash = (Get-FileHash -LiteralPath $artifact -Algorithm SHA256).Hash
Write-Host ("ARTIFACT {0} bytes {1}" -f $item.Length, $hash)
~~~

Expected: Server.exe exists in the exact isolated path; report its actual bytes and SHA-256. Do not copy it to D:\Debug\4月18日更新\Server, do not stop or replace the old process, and do not call any deployment or backup command.

### Task 6: Update CHANGELOG only after all static/build gates, then close with hashes and manual gaps

**Files:**
- Modify only after Task 5 succeeds: D:\相聚假人\Source\CHANGELOG.md, current 2026-08-20 bot-AI area.
- Read only for final audit: all owned/protected files, old deployed Server.exe, isolated artifact, and process metadata.

**Interfaces:**
- Consumes: focused/regression/build outputs and actual artifact/hash values.
- Produces: an accurate changelog entry and a final non-Git handoff; no deployment.

- [ ] **Step 1: Append one adjacent current bot-AI CHANGELOG entry with measured facts**

Use apply_patch only after all prior commands pass. The entry must state:

- direct cause and fix: commented BotBuyPoisonByShape candidate assignments and failed direct-cost candidates are corrected;
- purchase boundary: ProcessBotTaoistSupply only, 60 seconds, independent powder Shape 1/0 pools below 100 with approximately 500 batch and affordable-count reduction;
- ordinary Shape 1..8 and Resurrection Shape 0 on-demand amulet selection driven by every source-verified UseAmulet skill, with no hardcoded ItemName-to-Shape mapping;
- Combat has no direct purchase/shop enumeration, uses inventory-only mismatch switching, keeps red-before-green, poison count/last-cast record, and melee fallback;
- focused result and exact existing contract results: 36, 21, 6, 21, plus assassin-positioning 11/12 with the one stale Support fixed-hash exception;
- both Debug build exit codes, exact warning/error counts, isolated artifact path/bytes/SHA-256;
- no deployment and the remaining manual gaps. Do not claim all regressions green, runtime acceptance, CPU improvement, memory improvement, or database item mapping without measurements.

- [ ] **Step 2: Re-run focused and all existing contracts after the CHANGELOG edit**

Run the six commands from Task 5 Step 1 again. Expected: the same results; the new focused contract remains exit 0, the four numerical regressions remain 36/21/6/21, and assassin-positioning remains 11/12 only for the known stale Support hash. A new failure stops the final handoff.

- [ ] **Step 3: Reconfirm owned and protected SHA-256 values and the isolated artifact**

Run a terminal-only hash report:

~~~powershell
$root = 'D:\相聚假人\Source'
$owned = @(
  "$root\Server\BotManager.Support.cs",
  "$root\Server\BotManager.Combat.cs",
  "$root\.diagnostics\bot-ai-taoist-consumable-supply-contract.ps1",
  "$root\CHANGELOG.md",
  "$root\docs\superpowers\plans\2026-08-21-bot-ai-taoist-consumable-supply.md"
)
$protected = @(
  "$root\Server\BotManager.cs",
  "$root\Server\BotSkillSelector.cs",
  "$root\ServerLibrary\Models\Player\PlayerItem.cs",
  "$root\ServerLibrary\Models\Player\Aciton.cs",
  "$root\docs\superpowers\specs\2026-08-21-bot-ai-taoist-consumable-supply-design.md",
  "$root\.diagnostics\bot-ai-taoist-auto-skill-contract.ps1",
  "$root\.diagnostics\bot-ai-phase1-contract.ps1",
  "$root\.diagnostics\bot-ai-level40-assassin-contract.ps1",
  "$root\.diagnostics\bot-ai-cpu-potion-contract.ps1",
  "$root\.diagnostics\bot-ai-assassin-positioning-contract.ps1"
)
foreach ($path in ($owned + $protected)) {
  $item = Get-Item -LiteralPath $path
  $hash = (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash
  Write-Host ("HASH {0} {1} bytes {2}" -f $path, $item.Length, $hash)
}
$artifact = "$root\.build-check\bot-ai-taoist-consumable-supply-debug\Server\Server.exe"
$artifactItem = Get-Item -LiteralPath $artifact
$artifactHash = (Get-FileHash -LiteralPath $artifact -Algorithm SHA256).Hash
Write-Host ("ARTIFACT {0} {1} bytes {2}" -f $artifact, $artifactItem.Length, $artifactHash)
~~~

Expected: every owned file is listed with its final measured hash; every protected file is listed and unchanged from Task 1; the plan/spec/protected contracts are not rewritten. Report the actual new hashes rather than copying a prior artifact hash.

- [ ] **Step 4: Audit allowed paths, instrumentation, and new state**

Check the final change scope with terminal-only commands:

~~~powershell
rg -n "Console\.Write|Debug\.Write|SEnvir\.Log|new Thread|System\.Threading\.Timer|new Dictionary|Rotation|Cache" Server\BotManager.Support.cs Server\BotManager.Combat.cs .diagnostics\bot-ai-taoist-consumable-supply-contract.ps1
rg -n "BotBuyPoisonByShape|BotBuyConsumable|TryGetBotDirectBuyCost|ItemInfoList|NPC" Server\BotManager.Combat.cs
~~~

Expected: no newly introduced diagnostic logging, thread/timer, per-bot cache, rotation state, or purchase/shop symbol in ProcessBotTaoistCombatAction; the existing poison count/last-cast dictionaries are explicitly preserved and are not counted as new state. Inspect the complete owned methods and report any existing matches separately from new lines. The only intentional changed paths are Support.cs, Combat.cs, the new focused contract, CHANGELOG.md, and this plan; normal bin/obj and the isolated .build-check output are the only permitted generated paths.

- [ ] **Step 5: Recheck old deployed Server.exe and process metadata without control**

Run:

~~~powershell
$oldServer = 'D:\Debug\4月18日更新\Server\Server.exe'
$oldItem = Get-Item -LiteralPath $oldServer
$oldHash = (Get-FileHash -LiteralPath $oldServer -Algorithm SHA256).Hash
Write-Host ("OLD_SERVER {0} bytes {1}" -f $oldItem.Length, $oldHash)
Get-Process -Name Server -ErrorAction SilentlyContinue |
  Select-Object Id, ProcessName, StartTime, CPU, WorkingSet64, PrivateMemorySize64, Threads, Handles |
  Format-List
~~~

Expected: old Server.exe remains 83,103,744 bytes and SHA-256 D47BC3C8FEFA067DF68309D667E579F3EC5418E2E955B41E87A4BEB5F8267477, or any changed value is reported as a deployment-boundary failure. Process output is metadata only; no process is stopped, started, replaced, or deployed.

- [ ] **Step 6: Record manual runtime and A/B gaps explicitly**

The static and build gates do not close these runtime checks:

1. Runtime database validation that yellow Shape 1 and gray Shape 0 powders, ordinary Shape 1..8 amulets, and soul Shape 0 amulets have the expected ItemType, direct price, shop availability, stack behavior, and actual Shape; the implementation must not infer this from names.
2. Two powder purchase cases at the 60-second boundary, including each pool below 100, cheapest successful direct cost, approximately 500 batch, gold-short affordability, full inventory, no product, and no combat-tick shop enumeration.
3. Real combat red-then-green powder switching with 500ms poison effect timing, _botTaoistPoisonUseCount, _botTaoistLastPoisonCast, and no 20-use oscillating rotation.
4. Ordinary UseAmulet skills switch among Shape 1..8 only on mismatch/shortage, do not stock all eight, and do not rotate on monster resistance.
5. Resurrection switches to Shape 0 before casting and later switches back to an ordinary Shape 1..8 item only when a normal skill actually needs it; test no inventory slot, no gold, no soul product, failed PutOnEquip, and preserved current equipment.
6. Level <=7 starter supply still uses one empty inventory slot and zero type count, while level >7 never receives a free item; melee fallback remains reachable after any supply/equip failure.
7. Same-load old-versus-isolated-five-minute A/B for CPU per logical processor, working set, private bytes, managed heap, native/address-space evidence, shop-enumeration frequency, and equipment-scan frequency. The 4.9GB private-memory observation cannot be labeled a leak without managed/native profiling.

- [ ] **Step 7: Apply the completion gate**

Mark the plan complete only when all of the following are recorded: Task 1 baseline gate passed; genuine RED was exit 1 with only named behavior failures; Support intermediate assertions passed; focused GREEN is exit 0; auto-skill is 36 PASS; phase1 is 21 PASS; level40-assassin is 6 PASS; cpu-potion is 21 PASS; assassin-positioning is 11/12 with only the known stale Support fixed-hash exception; both Debug builds exit 0 with 0 errors and exact warnings recorded; isolated artifact path/size/hash is recorded; CHANGELOG contains measured facts; owned/protected hashes and allowed-path audit are complete; old deployed Server.exe is unchanged; no deployment/process control occurred; and all seven manual gaps remain clearly labeled if not performed. If any gate is missing, report partial rather than claiming runtime completion.

## Plan close

This plan deliberately ends without Git, deployment, backup, process control, or a runtime-success claim. The only implementation path is the bounded Support/Combat change described above, with source-structure RED/GREEN, protected regression evidence, isolated Debug/AnyCPU build evidence, and manual database/combat/performance acceptance still required.
