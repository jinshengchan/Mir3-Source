# Taoist Combat and Auto-Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (- [ ]) syntax for tracking. Execute in the same GPT-5.6 Luna/Max task and the shared non-Git tree; preserve unrelated edits and do not create a worktree.

**Goal:** Make Taoist monster combat selectors return attack skills only, so a valid adjacent target can fall through to physical melee when attack magic is unavailable, and make bot auto-learning grant every class-matching skill whose NeedLevel1 is at most the current player level and at most 35 directly while leaving NeedLevel1 36 and above on the existing skill-book path.

**Architecture:** Keep bot orchestration, target retention, retreat, movement, support actions, and melee fallback in BotManager. Restrict only the Taoist monster-attack selector outputs in BotSkillSelector. Keep the existing 30-second ProcessBotLearnSkill scan in BotManager.Support, changing only its class/current-level/35-boundary decision order. Dedicated Taoist summon, defence, and support modules continue to own their actions and ActionTime delays.

**Tech Stack:** C# bot source in the existing Server/ServerLibrary solution, PowerShell brace-depth source contracts, .NET Debug build, and Visual Studio 2022 MSBuild Debug/AnyCPU rebuild to an isolated output directory.

## Global Constraints

- This is a shared non-Git tree at D:\相聚假人\Source. Do not run Git commands, create a worktree, commit, push, open a pull request, merge, deploy, back up, or replace the running old Server.exe.
- The only implementation-owned paths are Server\BotSkillSelector.cs, Server\BotManager.Support.cs, .diagnostics\bot-ai-taoist-auto-skill-contract.ps1, and the current 2026-08-20 bot-AI area of CHANGELOG.md. The focused contract is created before production edits; the changelog is updated only after contracts and builds pass.
- Server\BotManager.cs, Server\BotManager.Combat.cs, every existing bot-AI contract, the approved design specification, ServerLibrary\Models\Player\Helpers.cs, and ServerLibrary\Models\Player\PlayerItem.cs are read-only.
- Preserve the public signatures of GetTaoistRangedMagic, GetTaoistAttackMagic, ProcessBotTaoistCombatAction, ProcessBotLearnSkill, and ProcessBotSkillModule.
- Preserve Taoist poison/talisman/attack priorities, the existing ranged-to-melee fallback order, emergency potion behavior, low-HP retreat, target ownership, group behavior, level-40 map switching, map/Boss/safety filters, all non-Taoist classes, and the CPU/potion optimization.
- Do not refactor the dedicated Taoist support queue or its normal ActionTime/CanAttack delay. This plan fixes direct combat selector routing only.
- Do not add a movement state, skill-learning dictionary, cooldown, thread, random movement, Action filter, School filter, login hook, or high-frequency learning scan.
- The inclusive learning boundary is NeedLevel1 35 for direct auto-learning and NeedLevel1 36 for the existing book acquisition/use path. NeedLevel1 must be no greater than player.Level before either path is considered. NeedLevel2 and NeedLevel3 remain outside this change.
- Build only Debug. The Server rebuild must use Platform=AnyCPU and output to D:\相聚假人\Source\.build-check\bot-ai-taoist-auto-skill-debug\Server\.
- Static contracts and builds do not prove live pathing, skill use, support coexistence, or CPU/potion improvement. Report the manual runtime gaps explicitly.

---

## File map and ownership

| Path | Planned action | Responsibility and boundary |
| --- | --- | --- |
| Server\BotSkillSelector.cs | Minimal production edit | Remove the two defence-first blocks from GetTaoistRangedMagic and GetTaoistAttackMagic only. Keep GetTaoistQuickDefenseMagic and all attack priorities/fallbacks. |
| Server\BotManager.Support.cs | Minimal production edit | Add BotAutoLearnMaxNeedLevel = 35 near the existing _botSkillLearnTime timing table and restructure ProcessBotLearnSkill. Keep every existing book helper and direct UserMagic notification sequence. |
| .diagnostics\bot-ai-taoist-auto-skill-contract.ps1 | Create before production edits | Extract complete method blocks by brace depth and enforce the Taoist selector, fallback, learning-boundary, preservation, and protected-hash assertions. |
| CHANGELOG.md | Append/update only after GREEN and builds | Record the symptom, source-supported cause, exact fix, RED/GREEN results, Debug/AnyCPU evidence, and manual runtime gaps in the current 2026-08-20 bot-AI area. |
| Server\BotManager.cs | Read-only | Preserve ProcessBotSkillModule, the shared scheduler, BotSkillActionRetrySeconds, and non-Taoist routing. |
| Server\BotManager.Combat.cs | Read-only | Preserve ProcessBotTaoistCombatAction, retreat, target retention, ranged-to-melee fallback, assassin behavior, and CPU/potion changes. |
| ServerLibrary\Models\Player\Helpers.cs | Read-only | Preserve non-bot/player learning helpers; final SHA-256 must match the baseline below. |
| ServerLibrary\Models\Player\PlayerItem.cs | Read-only | Preserve non-bot/player ItemUse behavior; final SHA-256 must match the baseline below. |
| Existing .diagnostics\bot-ai-*-contract.ps1 files | Read-only | Run phase1, level40-assassin, cpu-potion, and assassin-positioning regressions without changing them. |
| docs\superpowers\specs\2026-08-20-bot-ai-taoist-auto-skill-design.md | Read-only | Implement the approved semantics exactly; do not rewrite the design. |

## Approved behavior and current source evidence

### Combat decision boundary

The existing pipeline is ProcessBotBehaviorPipeline -> ProcessBotSkillModule -> ProcessBotTaoistModules -> PK/pickup -> ProcessBotCombat -> target validation -> ProcessBotCombatEngagement -> low-HP retreat -> ProcessBotTaoistCombatAction.

ProcessBotTaoistCombatAction currently calls TryProcessBotRangedCombatAction with GetTaoistRangedMagic, returns when that action succeeds, then obtains GetTaoistAttackMagic and calls ProcessBotMeleeCombatAction. The final implementation must preserve that order and the existing forcePhysicalFallback behavior.

The direct defect is in the two selector methods at the current BotSkillSelector.cs locations around lines 459 and 577: both call GetTaoistQuickDefenseMagic before attack selection. A ready defence result can be handed to generic ranged combat, which consumes the combat decision without an attack result and prevents the same tick from reaching melee. Removing those two selector-local blocks leaves support ownership intact and keeps the existing poison, talisman, adaptive, and rotating attack selection.

ProcessBotTaoistSummon, ProcessBotTaoistDefenceBuff, and ProcessBotTaoistSupportBuff remain in BotManager.Support.cs. Their normal support ActionTime delay is a separate queue behavior and is not changed by this plan.

### Learning decision boundary

ProcessBotSkillModule in Server\BotManager.cs continues to call ProcessBotLearnSkill. ProcessBotLearnSkill keeps its existing ObjectID timing table and 30-second normal scan. Inside the existing MagicInfoList.Binding loop, the final order is:

1. Skip null entries and entries whose MagicInfo.Class does not equal player.Class.
2. Skip entries already present in player.Magics.
3. Skip entries whose NeedLevel1 is greater than player.Level.
4. For NeedLevel1 at most BotAutoLearnMaxNeedLevel (35), create the existing UserMagic and perform the existing Character, Info, player.Magics, S.NewMagic, and RefreshStats sequence.
5. For NeedLevel1 36 or above, fall through to the current ready-book, appraisal, refine, page composition, book composition, item-parts, and shop-purchase helpers without changing their order or retry behavior.

There is no Action or School filter. Every MagicInfo entry for the matching class is eligible subject to duplicate, current-level, and 35/36 boundary checks. Because the old level-at-most-20 outer branch is removed, a level-above-35 bot fills missing class skills at most 35 during its existing 30-second scan without a new login or combat-tick scan.

The current source is expected to fail the focused contract before implementation because both selectors contain GetTaoistQuickDefenseMagic, ProcessBotLearnSkill still has the level-at-most-20/direct-at-most-20 structure, and it has no unified current-level gate before the book path.

## Task 1: Capture the baseline and create the focused RED contract

Files: .diagnostics\bot-ai-taoist-auto-skill-contract.ps1 is the only file created in this task. Do not edit either production file until the RED command has produced the expected source-specific failures.

- [ ] From D:\相聚假人\Source, capture the protected baseline hashes and confirm every listed file exists:

~~~powershell
$baselinePaths = @(
    'docs\superpowers\specs\2026-08-20-bot-ai-taoist-auto-skill-design.md',
    'Server\BotManager.cs',
    'Server\BotManager.Combat.cs',
    'Server\BotManager.Support.cs',
    'Server\BotSkillSelector.cs',
    'ServerLibrary\Models\Player\Helpers.cs',
    'ServerLibrary\Models\Player\PlayerItem.cs',
    '.diagnostics\bot-ai-phase1-contract.ps1',
    '.diagnostics\bot-ai-level40-assassin-contract.ps1',
    '.diagnostics\bot-ai-cpu-potion-contract.ps1',
    '.diagnostics\bot-ai-assassin-positioning-contract.ps1',
    'CHANGELOG.md'
)
$missing = $baselinePaths | Where-Object { -not (Test-Path -LiteralPath $_ -PathType Leaf) }
if ($missing) { $missing | ForEach-Object { Write-Error "Missing baseline path: $_" }; exit 2 }
$baselinePaths | ForEach-Object { Get-FileHash -Algorithm SHA256 -LiteralPath $_ | Select-Object Path,Hash }
~~~

  Expected protected values are:

  - design spec: 0040924D7FD6FF588E34515A7951C1D74AFE568BA0B33D8B89E8B84D4CF7ABD0
  - Server\BotManager.cs: DD57CE15664A5228B9A6670541E0C92FEBE001E25CC2B9B225CC28E41E03ACEF
  - Server\BotManager.Combat.cs: 7A4C3F853D85701EB4D197F7903D7C8834E06A296D6C937DD01DF22DB6DA0866
  - Server\BotManager.Support.cs: F71C4EFE90ABC9843A19E9802F94C09AA5B4615FDE084D7BF5ED5C4CA702130F
  - Server\BotSkillSelector.cs: E7DB5333E855C9610F5D26DDB19D3483E0466E46ABED36353576E7D3D418898A
  - ServerLibrary\Models\Player\Helpers.cs: E5ACF232C8EBA330160805AA77923FF4D87B37D514FB75C206AF630221347C61
  - ServerLibrary\Models\Player\PlayerItem.cs: BA35461EC9840FDB7638CA642406047AE89FDAD17F9165EE26AEEBF65F2AC235
  - .diagnostics\bot-ai-phase1-contract.ps1: BB272684407A9C3B786237DA9049E927DFE38A1D7FBCB9BAE8F8FD18CD2F5AD9
  - .diagnostics\bot-ai-level40-assassin-contract.ps1: 14009340E7F3CED0F71A59E06D279599C9885E3ECAD265104CEC979C26F70137
  - .diagnostics\bot-ai-cpu-potion-contract.ps1: C4C0B509223B7E512B36BE8046283B44928AA3EEC8DDB71453A1EF57817950BE
  - .diagnostics\bot-ai-assassin-positioning-contract.ps1: 63B69A5662339BF07A5F256A95642074416A1A99225992C686A284EFECEAE44C
  - CHANGELOG.md: C509E6AC25BD11B3964621B7C2A3F5F0885672C19E04B07D97EEC11AF013EF47

- [ ] Record the old deployed binary without touching it. If D:\Debug\4月18日更新\Server\Server.exe exists, print its SHA-256 and size; otherwise print an explicit absent result. Also inspect PID 10224 and any Server process metadata read-only, without stopping or replacing a process:

~~~powershell
$oldServerPath = 'D:\Debug\4月18日更新\Server\Server.exe'
if (Test-Path -LiteralPath $oldServerPath -PathType Leaf) {
    Get-Item -LiteralPath $oldServerPath | Select-Object FullName,Length,LastWriteTimeUtc
    Get-FileHash -Algorithm SHA256 -LiteralPath $oldServerPath
} else {
    Write-Host "OLD DEPLOYED SERVER ABSENT: $oldServerPath"
}
Get-Process -Id 10224 -ErrorAction SilentlyContinue |
    Select-Object Id,ProcessName,StartTime,Path,WorkingSet64,PrivateMemorySize64,Handles,Threads
Get-Process -Name Server -ErrorAction SilentlyContinue |
    Select-Object Id,ProcessName,StartTime,Path,WorkingSet64,PrivateMemorySize64,Handles,Threads
~~~

  Expected result: metadata only; no process control, deployment, copy, or binary change.

## Task 1 contract continuation

- [ ] Create .diagnostics\bot-ai-taoist-auto-skill-contract.ps1 with strict failure handling, complete-method extraction, and a fixed 36-assertion inventory. The contract must derive the source root from PSScriptRoot, use exit code 2 for missing paths, and reserve exit code 1 for source assertion failures.

- [ ] Implement the complete-method extractor below or an equivalent brace-depth implementation. It must locate the method signature, find its first opening brace, count every opening and closing brace until depth returns to zero, and return the full signature/body block. A regex that stops at the first closing brace is not sufficient.

~~~powershell
function Get-MethodBlock {
    param(
        [Parameter(Mandatory = $true)][string]$Source,
        [Parameter(Mandatory = $true)][string]$MethodName
    )

    $escapedName = [regex]::Escape($MethodName)
    $signaturePattern = '(?ms)^\s*(?:public|private|protected|internal)\s+' +
        '(?:(?:static|async|virtual|override|sealed)\s+)*' +
        '(?:[\w<>,\[\]\.\?]+\s+)*' + $escapedName + '\s*\('
    $signature = [regex]::Match($Source, $signaturePattern)
    if (-not $signature.Success) { return $null }

    $openBrace = $Source.IndexOf('{', $signature.Index)
    if ($openBrace -lt 0) { return $null }

    $depth = 0
    for ($index = $openBrace; $index -lt $Source.Length; $index++) {
        if ($Source[$index] -eq '{') {
            $depth++
        } elseif ($Source[$index] -eq '}') {
            $depth--
            if ($depth -eq 0) {
                return $Source.Substring($signature.Index, $index - $signature.Index + 1)
            }
        }
    }

    return $null
}
~~~

- [ ] Load exactly Server\BotSkillSelector.cs, Server\BotManager.Combat.cs, Server\BotManager.Support.cs, and Server\BotManager.cs for method extraction. Extract these nine complete blocks and assert each is nonempty: GetTaoistRangedMagic, GetTaoistAttackMagic, GetTaoistQuickDefenseMagic, ProcessBotTaoistCombatAction, ProcessBotTaoistDefenceBuff, ProcessBotTaoistSupportBuff, ProcessBotTaoistSummon, ProcessBotLearnSkill, and ProcessBotSkillModule. The extraction source must be tied to each method name so an unrelated call site cannot satisfy an assertion.

- [ ] Implement the contract path guard and assertion counter in this exact shape:

~~~powershell
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$requiredPaths = @(
    'Server\BotSkillSelector.cs',
    'Server\BotManager.Combat.cs',
    'Server\BotManager.Support.cs',
    'Server\BotManager.cs',
    'ServerLibrary\Models\Player\Helpers.cs',
    'ServerLibrary\Models\Player\PlayerItem.cs',
    'docs\superpowers\specs\2026-08-20-bot-ai-taoist-auto-skill-design.md',
    '.diagnostics\bot-ai-phase1-contract.ps1',
    '.diagnostics\bot-ai-level40-assassin-contract.ps1',
    '.diagnostics\bot-ai-cpu-potion-contract.ps1',
    '.diagnostics\bot-ai-assassin-positioning-contract.ps1'
)
foreach ($relativePath in $requiredPaths) {
    if (-not (Test-Path -LiteralPath (Join-Path $root $relativePath) -PathType Leaf)) {
        Write-Error "Missing contract path: $relativePath"
        exit 2
    }
}

$passed = 0
$failures = @()
function Assert-Contract {
    param([bool]$Condition, [string]$Name)
    if ($Condition) {
        $script:passed++
        Write-Host "PASS: $Name"
    } else {
        $script:failures += $Name
        Write-Host "FAIL: $Name"
    }
}
~~~

- [ ] Add the focused assertions below. Keep the labels stable. The first 27 assertions are source-structure checks; the final 9 are protected SHA-256 checks.

~~~powershell
$selectorPath = Join-Path $root 'Server\BotSkillSelector.cs'
$combatPath = Join-Path $root 'Server\BotManager.Combat.cs'
$supportPath = Join-Path $root 'Server\BotManager.Support.cs'
$managerPath = Join-Path $root 'Server\BotManager.cs'
$selectorSource = Get-Content -LiteralPath $selectorPath -Raw
$combatSource = Get-Content -LiteralPath $combatPath -Raw
$supportSource = Get-Content -LiteralPath $supportPath -Raw
$managerSource = Get-Content -LiteralPath $managerPath -Raw

$methodSpecs = [ordered]@{
    'GetTaoistRangedMagic' = @{ Source = $selectorSource; Name = 'GetTaoistRangedMagic' }
    'GetTaoistAttackMagic' = @{ Source = $selectorSource; Name = 'GetTaoistAttackMagic' }
    'GetTaoistQuickDefenseMagic' = @{ Source = $selectorSource; Name = 'GetTaoistQuickDefenseMagic' }
    'ProcessBotTaoistCombatAction' = @{ Source = $combatSource; Name = 'ProcessBotTaoistCombatAction' }
    'ProcessBotTaoistDefenceBuff' = @{ Source = $supportSource; Name = 'ProcessBotTaoistDefenceBuff' }
    'ProcessBotTaoistSupportBuff' = @{ Source = $supportSource; Name = 'ProcessBotTaoistSupportBuff' }
    'ProcessBotTaoistSummon' = @{ Source = $supportSource; Name = 'ProcessBotTaoistSummon' }
    'ProcessBotLearnSkill' = @{ Source = $supportSource; Name = 'ProcessBotLearnSkill' }
    'ProcessBotSkillModule' = @{ Source = $managerSource; Name = 'ProcessBotSkillModule' }
}

$blocks = @{}
foreach ($methodName in $methodSpecs.Keys) {
    $spec = $methodSpecs[$methodName]
    $blocks[$methodName] = Get-MethodBlock -Source $spec.Source -MethodName $spec.Name
    Assert-Contract (-not [string]::IsNullOrWhiteSpace($blocks[$methodName])) "complete method block: $methodName"
}

Assert-Contract ($blocks['GetTaoistRangedMagic'] -notmatch '\bGetTaoistQuickDefenseMagic\s*\(') 'ranged Taoist selector excludes quick defence'
Assert-Contract ($blocks['GetTaoistAttackMagic'] -notmatch '\bGetTaoistQuickDefenseMagic\s*\(') 'attack Taoist selector excludes quick defence'

Assert-Contract (
    $blocks['GetTaoistRangedMagic'] -match '\bSelectTalismanAttack\s*\(' -and
    $blocks['GetTaoistRangedMagic'] -match '\bSelectRotatingReadySingleTargetMagic\s*\('
) 'ranged Taoist attack priorities remain'
Assert-Contract (
    $blocks['GetTaoistAttackMagic'] -match '\bSelectTalismanAttack\s*\(' -and
    $blocks['GetTaoistAttackMagic'] -match '\bSelectRotatingReadySingleTargetMagic\s*\('
) 'attack Taoist attack priorities remain'

$combat = $blocks['ProcessBotTaoistCombatAction']
$rangedCall = $combat.IndexOf('TryProcessBotRangedCombatAction')
$attackSelectorCall = $combat.IndexOf('GetTaoistAttackMagic')
$meleeCall = $combat.IndexOf('ProcessBotMeleeCombatAction')
Assert-Contract (
    $rangedCall -ge 0 -and $attackSelectorCall -gt $rangedCall -and
    $meleeCall -gt $attackSelectorCall -and
    $combat -match 'if\s*\(\s*TryProcessBotRangedCombatAction[\s\S]*?\)\s*\r?\n\s*return;'
) 'Taoist ranged action then attack selector then melee fallback'

Assert-Contract ($blocks['ProcessBotTaoistDefenceBuff'] -match 'MagicType|CanAttack|ActionTime') 'dedicated Taoist defence support remains'
Assert-Contract ($blocks['ProcessBotTaoistSupportBuff'] -match 'MagicType|CanAttack|ActionTime') 'dedicated Taoist support buff remains'
Assert-Contract ($blocks['ProcessBotTaoistSummon'] -match 'MagicType|CanAttack|ActionTime') 'dedicated Taoist summon remains'

$constantMatches = [regex]::Matches($supportSource, 'private\s+const\s+int\s+BotAutoLearnMaxNeedLevel\s*=\s*35\s*;')
Assert-Contract ($constantMatches.Count -eq 1) 'single BotAutoLearnMaxNeedLevel constant equals 35'

$learn = $blocks['ProcessBotLearnSkill']
Assert-Contract ($learn -match 'magic\.Class\s*!=\s*cls') 'auto-learning keeps exact MagicInfo.Class guard'
Assert-Contract ($learn -match 'player\.Magics\.ContainsKey\s*\(\s*magic\.Magic\s*\)') 'auto-learning keeps duplicate UserMagic guard'

$levelGatePattern = 'if\s*\(\s*magic\.NeedLevel1\s*>\s*level\s*\)\s*\{\s*continue;\s*\}'
$directThresholdPattern = 'if\s*\(\s*magic\.NeedLevel1\s*<=\s*BotAutoLearnMaxNeedLevel\s*\)'
$levelGatePosition = $learn.IndexOf('magic.NeedLevel1 > level')
$bookPosition = $learn.IndexOf('FindBotReadySkillBookSlot')
Assert-Contract (
    $learn -match $levelGatePattern -and
    $learn -match $directThresholdPattern -and
    $levelGatePosition -ge 0 -and
    $bookPosition -gt $levelGatePosition
) 'current-level gate precedes the 35 direct branch and book path'

Assert-Contract (
    $learn -notmatch 'if\s*\(\s*level\s*<=\s*20\s*\)' -and
    $learn -notmatch 'magic\.NeedLevel1\s*>\s*20'
) 'old level-20 learning branch is removed'

Assert-Contract (
    $learn -match 'UserMagic\s+userMagic\s*=\s*SEnv\.UserMagicList\.CreateNewObject' -and
    $learn -match 'userMagic\.Character\s*=\s*player\.Character' -and
    $learn -match 'userMagic\.Info\s*=\s*magic' -and
    $learn -match 'player\.Magics\s*\[\s*magic\.Magic\s*\]\s*=\s*userMagic' -and
    $learn -match 'player\.Enqueue\s*\(\s*new\s+S\.NewMagic' -and
    $learn -match 'player\.RefreshStats\s*\(\s*\)'
) 'direct UserMagic creation notification and RefreshStats sequence remains'

Assert-Contract (
    $bookPosition -ge 0 -and
    $learn -match 'FindBotReadySkillBookSlot' -and
    $learn -match 'TryBotAppraiseRecipeSkillBook' -and
    $learn -match 'TryBotRefineInventorySkillBooks' -and
    $learn -match 'TryBotComposeRecipeSkillBookFromPages' -and
    $learn -match 'TryBotComposeRecipeSkillBook' -and
    $learn -match 'TryBotComposeSkillBookFromItemParts' -and
    $learn -match 'TryBotBuySkillBook'
) 'existing NeedLevel1-at-least-36 book helpers remain'
Assert-Contract ($learn -notmatch '\bmagic\.(Action|School)\b') 'auto-learning has no Action or School filter'
Assert-Contract ($learn -match '_botSkillLearnTime' -and $learn -match 'AddSeconds\s*\(\s*30\s*\)') 'existing 30-second normal learning scan remains'
Assert-Contract ($learn -notmatch '\b(?:Dictionary|ConcurrentDictionary)\s*<' -and $learn -match '_botSkillLearnTime') 'no new high-frequency learner state is introduced'

$protectedHashes = [ordered]@{
    'docs\superpowers\specs\2026-08-20-bot-ai-taoist-auto-skill-design.md' = '0040924D7FD6FF588E34515A7951C1D74AFE568BA0B33D8B89E8B84D4CF7ABD0'
    'Server\BotManager.cs' = 'DD57CE15664A5228B9A6670541E0C92FEBE001E25CC2B9B225CC28E41E03ACEF'
    'Server\BotManager.Combat.cs' = '7A4C3F853D85701EB4D197F7903D7C8834E06A296D6C937DD01DF22DB6DA0866'
    'ServerLibrary\Models\Player\Helpers.cs' = 'E5ACF232C8EBA330160805AA77923FF4D87B37D514FB75C206AF630221347C61'
    'ServerLibrary\Models\Player\PlayerItem.cs' = 'BA35461EC9840FDB7638CA642406047AE89FDAD17F9165EE26AEEBF65F2AC235'
    '.diagnostics\bot-ai-phase1-contract.ps1' = 'BB272684407A9C3B786237DA9049E927DFE38A1D7FBCB9BAE8F8FD18CD2F5AD9'
    '.diagnostics\bot-ai-level40-assassin-contract.ps1' = '14009340E7F3CED0F71A59E06D279599C9885E3ECAD265104CEC979C26F70137'
    '.diagnostics\bot-ai-cpu-potion-contract.ps1' = 'C4C0B509223B7E512B36BE8046283B44928AA3EEC8DDB71453A1EF57817950BE'
    '.diagnostics\bot-ai-assassin-positioning-contract.ps1' = '63B69A5662339BF07A5F256A95642074416A1A99225992C686A284EFECEAE44C'
}
foreach ($relativePath in $protectedHashes.Keys) {
    $actualHash = (Get-FileHash -Algorithm SHA256 -LiteralPath (Join-Path $root $relativePath)).Hash
    Assert-Contract ($actualHash -eq $protectedHashes[$relativePath]) "protected hash: $relativePath"
}

if ($failures.Count -gt 0) {
    Write-Host "RESULT: FAIL ($passed passed; $($failures.Count) failed)"
    $failures | ForEach-Object { Write-Host "FAILED ASSERTION: $_" }
    exit 1
}
Write-Host "RESULT: PASS (36 assertions)"
exit 0
~~~

- [ ] Run the focused contract before any production edit:

~~~powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .diagnostics\bot-ai-taoist-auto-skill-contract.ps1
~~~

  Expected RED: exit code 1 with RESULT: FAIL (31 passed; 5 failed). The five named failures must be the two selector defence exclusions, the missing BotAutoLearnMaxNeedLevel=35, the missing unified NeedLevel1/current-level-to-direct/book ordering, and the old level-at-most-20/direct-at-most-20 branch. A path, method-extraction, PowerShell parse, or protected-hash failure is not an acceptable RED.

## Task 2: Remove only defence-first outputs from the two Taoist attack selectors

File: Server\BotSkillSelector.cs only.

- [ ] Re-read the complete GetTaoistRangedMagic and GetTaoistAttackMagic blocks extracted by the focused contract and identify the two identical defence-first regions.

- [ ] Apply the smallest production edit: remove the local defenseMagic declaration, GetTaoistQuickDefenseMagic call, and immediate non-None return from both attack-selector methods. Remove or update only the comments that describe those deleted selector-local regions.

- [ ] Do not change GetTaoistQuickDefenseMagic, any support caller, selector signatures, poison/talisman/adaptive/rotating priorities, area-attack filtering, cooldown/MP/item checks, or the combat caller.

- [ ] Run the focused contract immediately after this selector edit:

~~~powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .diagnostics\bot-ai-taoist-auto-skill-contract.ps1
~~~

  Expected intermediate result: exit code 1 with the two selector failures resolved and exactly the three learning failures still present. Do not proceed if any combat order, support-preservation, extraction, or protected-hash assertion fails.

## Task 3: Unify the bot learning gate and preserve the existing book path

File: Server\BotManager.Support.cs only.

- [ ] Add exactly one declaration immediately beside the existing skill-learning timing table around _botSkillLearnTime:

~~~csharp
private const int BotAutoLearnMaxNeedLevel = 35;
~~~

  Do not modify the read-only BotSkillActionRetrySeconds declaration in Server\BotManager.cs and do not add another timing table or learning-state map.

- [ ] Update the ProcessBotLearnSkill summary comment so it states the approved 35 direct / 36-and-above book boundary. This is a comment correction for the changed condition, not a behavior expansion.

- [ ] Restructure only the decision order inside the existing MagicInfoList.Binding loop to the following sequence:

~~~csharp
if (magic == null || magic.Class != cls) continue;
if (player.Magics.ContainsKey(magic.Magic)) continue;
if (magic.NeedLevel1 > level) continue;

if (magic.NeedLevel1 <= BotAutoLearnMaxNeedLevel)
{
    // Keep the existing UserMagic creation, Character/Info assignment,
    // player.Magics insertion, S.NewMagic notification, RefreshStats,
    // exception handling, and continue behavior unchanged.
    continue;
}

// Keep the complete existing ready-book/appraisal/refine/compose/purchase
// chain and its UseItemTime/retry/return behavior unchanged.
~~~

  Move the current direct UserMagic body into the at-most-35 branch, remove the outer level-at-most-20 condition and its NeedLevel1-at-most-20 check, and leave the existing book chain as the fall-through for NeedLevel1 36 and above. Keep the reqClass calculation because the book helpers use it.

- [ ] Preserve the class guard and duplicate guard before the current-level gate. Do not add an Action or School predicate, and do not use NeedLevel2 or NeedLevel3 for initial acquisition. Every MagicInfo entry whose MagicInfo.Class matches the bot remains eligible subject only to duplicate, current-level, and 35/36 boundary checks.

- [ ] Preserve the existing 30-second _botSkillLearnTime scan and every existing book helper in its current order: FindBotReadySkillBookSlot, TryBotAppraiseRecipeSkillBook, TryBotRefineInventorySkillBooks, TryBotComposeRecipeSkillBookFromPages, TryBotComposeRecipeSkillBook, TryBotComposeSkillBookFromItemParts, and TryBotBuySkillBook. Preserve UseItemTime checks, BotSkillActionRetrySeconds scheduling, return behavior, item quantities, and gold values.

- [ ] Preserve the direct sequence exactly: SEnv.UserMagicList.CreateNewObject, Character assignment, MagicInfo assignment, player.Magics insertion under magic.Magic, S.NewMagic enqueue, RefreshStats, exception handling, and the existing loop continuation. The duplicate guard must remain the only protection against a second UserMagic for the same MagicInfo.

- [ ] Do not edit Server\BotManager.cs, Server\BotManager.Combat.cs, ServerLibrary\Models\Player\Helpers.cs, ServerLibrary\Models\Player\PlayerItem.cs, BotSkillSelector.cs in this task, any existing contract, or CHANGELOG.md.

- [ ] Run the focused contract for GREEN after the Support.cs edit:

~~~powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .diagnostics\bot-ai-taoist-auto-skill-contract.ps1
~~~

  Expected GREEN: exit code 0 and RESULT: PASS (36 assertions). The output must include passing assertions for no selector defence calls, the single 35 constant, the current-level gate before both acquisition paths, direct UserMagic sequencing, all existing book helpers, no Action/School filter, the 30-second scan, dedicated support methods, melee fallback order, and all protected hashes.

## Task 4: Run the complete static regression suite and isolated Debug build

- [ ] Run the focused contract once more after both production edits, without changing the contract:

~~~powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .diagnostics\bot-ai-taoist-auto-skill-contract.ps1
~~~

  Expected output: exit code 0 and RESULT: PASS (36 assertions).

- [ ] Run the phase-1 regression contract from D:\相聚假人\Source:

~~~powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .diagnostics\bot-ai-phase1-contract.ps1
~~~

  Expected output: exit code 0 and 21 assertions PASS. This protects the four-slice 200ms scheduler, approximately 800ms bot main behavior, emergency potion behavior, support routing, and existing fallback contracts.

- [ ] Run the level-40/Assassin regression contract:

~~~powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .diagnostics\bot-ai-level40-assassin-contract.ps1
~~~

  Expected output: exit code 0 and 6 assertions PASS. This protects level-40 map switching, Assassin skill behavior, map thresholds, and safety filters.

- [ ] Run the CPU/potion regression contract:

~~~powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .diagnostics\bot-ai-cpu-potion-contract.ps1
~~~

  Expected output: exit code 0 with every reported assertion PASS. This protects duplicate normal-potion-call removal, the independent 200ms potion timer, the 800ms non-emergency retry reservation, emergency HP behavior, and economy values.

- [ ] Run the Assassin-positioning regression contract:

~~~powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .diagnostics\bot-ai-assassin-positioning-contract.ps1
~~~

  Expected output: exit code 0 with every reported assertion PASS. This protects the approved Assassin melee-distance guard and keeps Wizard/Taoist preferred-range repositioning unchanged.

- [ ] Stop before any build if any of the four existing contracts or the focused contract fails. Inspect the named failure; do not alter a protected contract or weaken an assertion to obtain PASS.

- [ ] Build ServerLibrary in Debug from D:\相聚假人\Source:

~~~powershell
& 'C:\Program Files\dotnet\dotnet.exe' build 'ServerLibrary\ServerLibrary.csproj' -c Debug --nologo
~~~

  Expected acceptance: process exit code 0 and zero compile errors. Record the exact warning count printed by the build. No Release build is permitted.

- [ ] Rebuild Server in Debug/AnyCPU to the isolated output directory:

~~~powershell
& 'C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\MSBuild\Current\Bin\MSBuild.exe' 'Server\Server.csproj' /t:Rebuild /m /v:minimal /p:Configuration=Debug /p:Platform=AnyCPU '/p:OutputPath=D:\相聚假人\Source\.build-check\bot-ai-taoist-auto-skill-debug\Server\'
~~~

  Expected acceptance: process exit code 0, zero compile errors, actual warning count recorded, and D:\相聚假人\Source\.build-check\bot-ai-taoist-auto-skill-debug\Server\Server.exe exists. Report its byte size and SHA-256 in the final handoff. The isolated output must not be copied to any deployment directory.

- [ ] If the app layer reports a build timeout, inspect completion state and artifact existence before retrying:

~~~powershell
Get-Process -Name dotnet,MSBuild -ErrorAction SilentlyContinue |
    Select-Object Id,ProcessName,StartTime,HasExited
$isolatedServer = 'D:\相聚假人\Source\.build-check\bot-ai-taoist-auto-skill-debug\Server\Server.exe'
Test-Path -LiteralPath $isolatedServer -PathType Leaf
if (Test-Path -LiteralPath $isolatedServer -PathType Leaf) {
    Get-Item -LiteralPath $isolatedServer | Select-Object FullName,Length,LastWriteTimeUtc
}
~~~

  An already completed build is evidence to inspect, not permission to stop the old Server.exe, deploy, copy, back up, or replace any binary.

## Task 5: Record verified results, audit scope, and close the implementation boundary

- [ ] After the focused contract, all four existing regression contracts, and both Debug builds pass, update only the current 2026-08-20 bot-AI area of CHANGELOG.md. Use apply_patch and append one adjacent dated entry. The entry must state:

  - the confirmed symptom: a level-10 Taoist with a valid adjacent monster target could stand idle instead of retaliating;
  - the direct routing cause: GetTaoistRangedMagic and GetTaoistAttackMagic returned ready defence skills before attack selection, allowing the generic ranged path to consume the combat decision;
  - the exact fix: the two selector-local defence-first blocks were removed, while ProcessBotTaoistDefenceBuff, ProcessBotTaoistSupportBuff, ProcessBotTaoistSummon, the ranged-to-melee fallback, and normal support ActionTime behavior remain;
  - the learning rule: exact MagicInfo.Class match, duplicate guard, NeedLevel1 at most player.Level, direct auto-learning through 35, and the existing book acquisition/use path from 36;
  - actual focused RED and GREEN results, all four regression results, both Debug build exit results, exact warning/error counts, and the isolated Server.exe path, byte size, and SHA-256;
  - explicit no-deployment status and the remaining manual runtime checks from this task.

- [ ] Do not change any older CHANGELOG entry, approved design text, plan text before this Task 5 section, production source outside the two approved files, existing contract, ServerLibrary player learning file, build output outside the isolated directory, database, configuration, resource, client, deployed binary, or process.

- [ ] Re-run the focused contract after the changelog update:

~~~powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .diagnostics\bot-ai-taoist-auto-skill-contract.ps1
~~~

  Expected output: exit code 0 and RESULT: PASS (36 assertions).

- [ ] Re-run phase1 after the changelog update:

~~~powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .diagnostics\bot-ai-phase1-contract.ps1
~~~

  Expected output: exit code 0 and 21 assertions PASS.

- [ ] Re-run the level-40/Assassin contract after the changelog update:

~~~powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .diagnostics\bot-ai-level40-assassin-contract.ps1
~~~

  Expected output: exit code 0 and 6 assertions PASS.

- [ ] Re-run the CPU/potion contract after the changelog update:

~~~powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .diagnostics\bot-ai-cpu-potion-contract.ps1
~~~

  Expected output: exit code 0 and every reported assertion PASS.

- [ ] Re-run the Assassin-positioning contract after the changelog update:

~~~powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .diagnostics\bot-ai-assassin-positioning-contract.ps1
~~~

  Expected output: exit code 0 and every reported assertion PASS.

- [ ] Confirm the successful Debug/AnyCPU build evidence is still available. If either Task 4 build did not finish with exit code 0 and zero compile errors, rerun exactly the two Task 4 Debug commands before finalizing; do not run Release and do not deploy:

~~~powershell
& 'C:\Program Files\dotnet\dotnet.exe' build 'ServerLibrary\ServerLibrary.csproj' -c Debug --nologo
& 'C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\MSBuild\Current\Bin\MSBuild.exe' 'Server\Server.csproj' /t:Rebuild /m /v:minimal /p:Configuration=Debug /p:Platform=AnyCPU '/p:OutputPath=D:\相聚假人\Source\.build-check\bot-ai-taoist-auto-skill-debug\Server\'
~~~

  Expected acceptance: both commands exit 0, both report zero compile errors, actual warning counts are recorded, and the isolated Server.exe exists.

- [ ] Print final SHA-256 and byte size for every owned file and the isolated artifact:

~~~powershell
$ownedFinal = @(
    'Server\BotSkillSelector.cs',
    'Server\BotManager.Support.cs',
    '.diagnostics\bot-ai-taoist-auto-skill-contract.ps1',
    'CHANGELOG.md',
    '.build-check\bot-ai-taoist-auto-skill-debug\Server\Server.exe'
)
foreach ($relativePath in $ownedFinal) {
    $fullPath = Join-Path (Get-Location) $relativePath
    if (-not (Test-Path -LiteralPath $fullPath -PathType Leaf)) {
        Write-Error "Missing final owned artifact: $relativePath"
        continue
    }
    Get-Item -LiteralPath $fullPath | Select-Object FullName,Length,LastWriteTimeUtc
    Get-FileHash -Algorithm SHA256 -LiteralPath $fullPath
}
~~~

  Expected output: one actual final hash and size for each of the four owned files plus the isolated Server.exe. Report all five values verbatim in the handoff.

- [ ] Recompute the protected hashes and require exact equality with the Task 1 baseline:

~~~powershell
$protected = [ordered]@{
    'docs\superpowers\specs\2026-08-20-bot-ai-taoist-auto-skill-design.md' = '0040924D7FD6FF588E34515A7951C1D74AFE568BA0B33D8B89E8B84D4CF7ABD0'
    'Server\BotManager.cs' = 'DD57CE15664A5228B9A6670541E0C92FEBE001E25CC2B9B225CC28E41E03ACEF'
    'Server\BotManager.Combat.cs' = '7A4C3F853D85701EB4D197F7903D7C8834E06A296D6C937DD01DF22DB6DA0866'
    'ServerLibrary\Models\Player\Helpers.cs' = 'E5ACF232C8EBA330160805AA77923FF4D87B37D514FB75C206AF630221347C61'
    'ServerLibrary\Models\Player\PlayerItem.cs' = 'BA35461EC9840FDB7638CA642406047AE89FDAD17F9165EE26AEEBF65F2AC235'
    '.diagnostics\bot-ai-phase1-contract.ps1' = 'BB272684407A9C3B786237DA9049E927DFE38A1D7FBCB9BAE8F8FD18CD2F5AD9'
    '.diagnostics\bot-ai-level40-assassin-contract.ps1' = '14009340E7F3CED0F71A59E06D279599C9885E3ECAD265104CEC979C26F70137'
    '.diagnostics\bot-ai-cpu-potion-contract.ps1' = 'C4C0B509223B7E512B36BE8046283B44928AA3EEC8DDB71453A1EF57817950BE'
    '.diagnostics\bot-ai-assassin-positioning-contract.ps1' = '63B69A5662339BF07A5F256A95642074416A1A99225992C686A284EFECEAE44C'
}
foreach ($relativePath in $protected.Keys) {
    $actual = (Get-FileHash -Algorithm SHA256 -LiteralPath $relativePath).Hash
    if ($actual -ne $protected[$relativePath]) {
        Write-Error "Protected hash changed: $relativePath expected $($protected[$relativePath]) actual $actual"
    } else {
        Write-Host "PROTECTED HASH PASS: $relativePath"
    }
}
~~~

  Expected output: all nine protected entries pass. BotSkillSelector.cs, BotManager.Support.cs, the new focused contract, and CHANGELOG.md are intentional owned-file changes and must be reported with their actual final hashes rather than compared with the old values.

- [ ] Perform the non-Git allowed-path audit using the Task 1 file listing and the final listing. The only changed or newly created source/document/diagnostic paths may be Server\BotSkillSelector.cs, Server\BotManager.Support.cs, .diagnostics\bot-ai-taoist-auto-skill-contract.ps1, and CHANGELOG.md. The only allowed generated-output roots are normal bin/obj directories and D:\相聚假人\Source\.build-check\bot-ai-taoist-auto-skill-debug\.

~~~powershell
$allowedOwned = @(
    'Server\BotSkillSelector.cs',
    'Server\BotManager.Support.cs',
    '.diagnostics\bot-ai-taoist-auto-skill-contract.ps1',
    'CHANGELOG.md'
)
$allowedGeneratedRoots = @(
    'bin\',
    'obj\',
    '.build-check\bot-ai-taoist-auto-skill-debug\'
)
Write-Host 'ALLOWED OWNED PATHS:'
$allowedOwned
Write-Host 'ALLOWED GENERATED ROOTS:'
$allowedGeneratedRoots
Write-Host 'FINAL PROJECT FILES OUTSIDE GENERATED ROOTS:'
Get-ChildItem -Path Server,ServerLibrary,.diagnostics,docs -Recurse -File |
    Select-Object -ExpandProperty FullName
~~~

  Compare this output with the Task 1 listing in the task transcript. Report any path outside the four owned paths, protected paths, or generated roots as a scope failure. Do not use Git status or Git diff because this project is non-Git.

- [ ] Inspect the final complete method blocks and changed regions for instrumentation or unrelated edits. The production-side search below must produce no newly introduced match; PowerShell contract Write-Host output is not production instrumentation:

~~~powershell
rg -n 'Console\.WriteLine|Debug\.WriteLine|Trace\.WriteLine|File\.AppendAllText|File\.WriteAllText|Stopwatch' Server\BotSkillSelector.cs Server\BotManager.Support.cs
~~~

  Also inspect that no new movement state, skill-learning map, cooldown, thread, random movement, Action filter, School filter, or high-frequency scan was introduced.

- [ ] Re-hash D:\Debug\4月18日更新\Server\Server.exe and capture the read-only process snapshot again:

~~~powershell
$oldServerPath = 'D:\Debug\4月18日更新\Server\Server.exe'
if (Test-Path -LiteralPath $oldServerPath -PathType Leaf) {
    Get-Item -LiteralPath $oldServerPath | Select-Object FullName,Length,LastWriteTimeUtc
    Get-FileHash -Algorithm SHA256 -LiteralPath $oldServerPath
} else {
    Write-Host "OLD DEPLOYED SERVER ABSENT: $oldServerPath"
}
Get-Process -Id 10224 -ErrorAction SilentlyContinue |
    Select-Object Id,ProcessName,StartTime,Path,WorkingSet64,PrivateMemorySize64,Handles,Threads
Get-Process -Name Server -ErrorAction SilentlyContinue |
    Select-Object Id,ProcessName,StartTime,Path,WorkingSet64,PrivateMemorySize64,Handles,Threads
~~~

  Compare old Server.exe hash and size with Task 1. Expected result: unchanged if present, or explicitly absent in both snapshots. The process snapshot is read-only; do not stop, restart, replace, deploy, copy, or back up the old process or binary.

### Manual runtime acceptance still required

- [ ] Test a level-10 Taoist with no queued support action, a valid adjacent monster target, and no immediately usable attack magic. Expected behavior: the bot attempts ordinary physical melee in the same combat decision instead of standing idle.

- [ ] Test a level-10 Taoist with a valid adjacent monster target and a usable Taoist attack spell. Expected behavior: the Taoist releases the attack spell when its normal cooldown, MP, item, target, and ActionTime gates permit it; if the cast path returns false, the existing melee fallback remains available.

- [ ] Test support coexistence with summon, defence buff, and support heal/invisibility actions. Expected behavior: dedicated support actions still run with their existing ActionTime delay, and the target-acquired Taoist does not remain idle after a transient support action.

- [ ] Test the inclusive learning boundary with matching-class missing skills: NeedLevel1 35 is directly created and notified through the existing UserMagic path, while NeedLevel1 36 uses the existing skill-book acquisition/use path.

- [ ] Test an existing bot above level 35 with missing matching-class NeedLevel1-at-most-35 skills. Expected behavior: the normal 30-second learning scan backfills them without a login-only dependency and without a combat-tick learning scan.

- [ ] Run an old/new same-load runtime A/B for CPU, private bytes, working set, managed/native memory evidence, potion-monitor attempts, potion inventory scans, and potion use. Include the new Assassin/Taoist workload and record the sample method. Static contracts and builds cannot prove the CPU, memory, or drinking-potion result.

## Plan closure and implementation handoff

- [ ] Re-read docs\superpowers\specs\2026-08-20-bot-ai-taoist-auto-skill-design.md and this plan side by side. Confirm every approved behavior, non-goal, file boundary, threshold, preserved helper, regression command, build boundary, and manual gap is represented.

- [ ] Verify type and signature consistency: MagicInfo.Class is compared with MirClass, NeedLevel1 is compared with player.Level, the direct branch creates one UserMagic per duplicate-guarded entry, the book helpers still receive magic and reqClass, and no caller signature changed.

- [ ] Verify the plan has no unresolved marker, vague implementation step, extra production scope, Release build, Git/PR operation, deployment operation, backup operation, or process-control operation.

The implementation handoff must report STATUS, TASK ID, baseline hashes, exact RED output, file-by-file changes, focused GREEN, all four regression results, both Debug build commands with warning/error counts, isolated Server.exe path/size/hash, final owned/protected hashes, allowed-path audit, old deployed Server.exe comparison, read-only process snapshot, GIT=non-Git/no commits, PR=not authorized, DEPLOY=none, judgment calls, and the six manual runtime checks above. It must not claim that Taoist live retaliation, skill release, learning backfill, CPU, memory, or potion performance is accepted until the corresponding manual checks are run.
