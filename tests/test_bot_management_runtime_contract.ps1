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

$root = Split-Path -Parent $PSScriptRoot
$managerPath = Join-Path $root 'Server\BotManager.cs'
$sMainPath = Join-Path $root 'Server\SMain.cs'
$uiPath = Join-Path $root 'Server\Views\BotConfigView.cs'
$managementPath = Join-Path $root 'Server\BotManager.Management.cs'
$combatPath = Join-Path $root 'Server\BotManager.Combat.cs'
$supportPath = Join-Path $root 'Server\BotManager.Support.cs'
$seEnvirPath = Join-Path $root 'ServerLibrary\Envir\SEnvir.cs'
$manager = Get-Content -Raw -Encoding UTF8 -LiteralPath $managerPath
$sMain = Get-Content -Raw -Encoding UTF8 -LiteralPath $sMainPath
$ui = Get-Content -Raw -Encoding UTF8 -LiteralPath $uiPath
$management = if (Test-Path -LiteralPath $managementPath) { Get-Content -Raw -Encoding UTF8 -LiteralPath $managementPath } else { '' }
$combat = Get-Content -Raw -Encoding UTF8 -LiteralPath $combatPath
$support = Get-Content -Raw -Encoding UTF8 -LiteralPath $supportPath
$seEnvir = Get-Content -Raw -Encoding UTF8 -LiteralPath $seEnvirPath

$processBotCombat = [regex]::Match($combat, '(?s)private static void ProcessBotCombat\s*\(.*?(?=\r?\n\s*(?:private|public|protected|internal)\s+[^;\r\n]+\()').Value
$step1Block = [regex]::Match($processBotCombat, '(?s)//[^\r\n]*Step 1\b[^\r\n]*\r?\n.*?(?=\r?\n\s*//[^\r\n]*Step 1b\b)').Value
Assert-Contains $step1Block 'if\s*\(\s*player\.InSafeZone\s*&&\s*Config\.BotAutoLevel\s*&&\s*Config\.BotAutoMapSwitch\s*\)' 'safe-zone exit branch requires the player to be in a safe zone and both bot movement settings'
$step1Branch = [regex]::Match($step1Block, '(?s)if\s*\(\s*player\.InSafeZone\s*&&\s*Config\.BotAutoLevel\s*&&\s*Config\.BotAutoMapSwitch\s*\)\s*\{.*?return;\s*\}').Value
$script:Assertions++
if ([string]::IsNullOrWhiteSpace($step1Branch)) { throw 'FAIL: safe-zone exit branch must contain its guarded exit logic and return' }
Assert-Contains $step1Branch 'FindNearestNonSafeCell\s*\(' 'safe-zone exit branch still finds the nearest non-safe cell'
Assert-Contains $step1Branch 'if\s*\(\s*exit\s*!=\s*Point\.Empty\s*\)\s*player\.Teleport\s*\(\s*player\.CurrentMap\s*,\s*exit\s*\)' 'safe-zone exit still teleports when an exit exists'
$step1Returns = [regex]::Matches($step1Block, '\breturn\s*;')
$script:Assertions++
if ($step1Returns.Count -ne 1) { throw "FAIL: Step 1 must keep exactly one return inside the safe-zone exit branch (got $($step1Returns.Count))" }
$step1bBlock = [regex]::Match($processBotCombat, '(?s)//[^\r\n]*Step 1b\b[^\r\n]*\r?\n.*?(?=\r?\n\s*//[^\r\n]*Step 1c\b)').Value
Assert-Contains $step1bBlock 'stuckTooLong' 'out-of-safe-zone path can continue into Step 1b stuck detection'
$step1BranchIndex = $processBotCombat.IndexOf($step1Branch)
$step1bIndex = $processBotCombat.IndexOf('Step 1b')
$script:Assertions++
if ($step1BranchIndex -lt 0 -or $step1bIndex -le ($step1BranchIndex + $step1Branch.Length)) {
    throw 'FAIL: Step 1b must remain after the guarded safe-zone branch so out-of-safe-zone bots can reach it'
}

$sMainLoadBlock = [regex]::Match($sMain, '(?s)private void SMain_Load\(.*?(?=\r?\n\s*private void )').Value
Assert-NotContains $sMainLoadBlock 'BotManager\.Start\(' 'SMain_Load does not start bots before the server/database lifecycle is ready'
Assert-Contains $sMain 'TryAutoStartBotSystem' 'SMain has deferred bot auto-start helper'
Assert-Contains $sMain 'SEnvir\.Started' 'deferred auto-start checks server started state'
Assert-Contains $sMain 'SEnvir\.AccountInfoList' 'deferred auto-start checks account database collection'
Assert-Contains $sMain 'SEnvir\.CharacterInfoList' 'deferred auto-start checks character database collection'
Assert-Contains $sMain 'SEnvir\.BotAccountInfoList' 'deferred auto-start checks bot database collection'
Assert-Contains $manager '\u5047\u4eba\u7cfb\u7edf\u542f\u52a8\u5ef6\u540e\uff1a\u670d\u52a1\u5668\u6570\u636e\u5e93\u5c1a\u672a\u5c31\u7eea' 'BotManager.Start reports database-not-ready protection'
Assert-Contains $manager 'SEnvir\.Started' 'BotManager.Start protects against a stopped server'
Assert-Contains $manager 'AccountInfoList\?\.Binding' 'BotManager.Start protects account collection readiness'
Assert-Contains $manager 'CharacterInfoList\?\.Binding' 'BotManager.Start protects character collection readiness'
Assert-Contains $manager 'BotAccountInfoList\?\.Binding' 'BotManager.Start protects bot collection readiness'

$tryAutoStartMethod = [regex]::Match($sMain, '(?s)private void TryAutoStartBotSystem\s*\(.*?(?=\r?\n\s*(?:public|private|protected|internal)\s+[^;\r\n]+\()').Value
Assert-Contains $tryAutoStartMethod 'private void TryAutoStartBotSystem' 'deferred auto-start method block is extracted'
Assert-Contains $tryAutoStartMethod 'SEnvir\.Started' 'auto-start method checks server started state locally'
Assert-Contains $tryAutoStartMethod 'SEnvir\.AccountInfoList\?\.Binding' 'auto-start method checks account binding locally'
Assert-Contains $tryAutoStartMethod 'SEnvir\.CharacterInfoList\?\.Binding' 'auto-start method checks character binding locally'
Assert-Contains $tryAutoStartMethod 'SEnvir\.BotAccountInfoList\?\.Binding' 'auto-start method checks bot binding locally'
$autoStartCallMatches = [regex]::Matches($tryAutoStartMethod, 'BotManager\.Start\s*\(')
$autoStartAttemptMatch = [regex]::Match($tryAutoStartMethod, '_botAutoStartAttempted\s*=\s*true\s*;')
$script:Assertions++
if ($autoStartCallMatches.Count -ne 1) { throw "FAIL: deferred auto-start must call BotManager.Start exactly once inside its method block (got $($autoStartCallMatches.Count))" }
$script:Assertions++
if (!$autoStartAttemptMatch.Success -or $autoStartAttemptMatch.Index -ge $autoStartCallMatches[0].Index) {
    throw 'FAIL: _botAutoStartAttempted must be set before the unique deferred BotManager.Start call'
}

$botStartMethod = [regex]::Match($manager, '(?s)public static void Start\s*\(.*?(?=\r?\n\s*(?:public|private|protected|internal)\s+[^;\r\n]+\()').Value
Assert-Contains $botStartMethod 'public static void Start' 'BotManager.Start method block is extracted'
$databaseGuardMatch = [regex]::Match($botStartMethod, '(?s)if\s*\(\s*!SEnvir\.Started.*?return;')
$script:Assertions++
if (!$databaseGuardMatch.Success) { throw 'FAIL: BotManager.Start database guard block is missing' }
foreach ($bindingPattern in @(
    'SEnvir\.AccountInfoList\?\.Binding',
    'SEnvir\.CharacterInfoList\?\.Binding',
    'SEnvir\.BotAccountInfoList\?\.Binding'
)) {
    Assert-Contains $databaseGuardMatch.Value $bindingPattern "BotManager.Start guard contains $bindingPattern"
}
foreach ($statePattern in @('botFilePath\s*=', 'botCount\s*=', 'ResetManagementCounters\s*\(')) {
    $stateMatch = [regex]::Match($botStartMethod, $statePattern)
    $script:Assertions++
    if (!$stateMatch.Success -or $databaseGuardMatch.Index + $databaseGuardMatch.Length -gt $stateMatch.Index) {
        throw "FAIL: BotManager.Start database guard must finish before state change $statePattern"
    }
}

$botStartButtonMethod = [regex]::Match($ui, '(?s)private void BotStartButton_Click\s*\(.*?(?=\r?\n\s*private void )').Value
Assert-Contains $botStartButtonMethod 'private void BotStartButton_Click' 'bot start button method block is extracted'
$buttonStartMatch = [regex]::Match($botStartButtonMethod, 'BotManager\.Start\s*\(')
$script:Assertions++
if (!$buttonStartMatch.Success) { throw 'FAIL: bot start button must call BotManager.Start' }
$buttonAfterStart = $botStartButtonMethod.Substring($buttonStartMatch.Index + $buttonStartMatch.Length)
Assert-Contains $buttonAfterStart '(?s)if\s*\(\s*BotManager\.IsRunning\s*\).*?MessageBox\.Show\s*\(\s*"\u5047\u4eba\u7cfb\u7edf\u5df2\u542f\u52a8' 'success message is conditional on IsRunning after Start'
Assert-Contains $botStartButtonMethod '\u670d\u52a1\u5668\u6570\u636e\u5e93\u5c1a\u672a\u5c31\u7eea\uff0c\u542f\u52a8\u5df2\u5ef6\u540e\uff0c\u8bf7\u5148\u542f\u52a8\u670d\u52a1\u5668\u3002' 'failed bot start reports database-not-ready guidance'

Assert-Contains $seEnvir 'ConcurrentQueue<Action>\s+BotActionQueue' 'main bot action queue exists'
Assert-Contains $seEnvir 'ConcurrentQueue<Action>\s+BotPotionActionQueue' 'independent potion action queue exists'
Assert-Contains $management 'TryApplyManagementSettings\s*\(BotManagementSettings settings, bool persist, out string error\)' 'atomic apply API exists'
Assert-Contains $management 'SetPaused\s*\(bool paused\)' 'pause API exists'
Assert-Contains $management 'bool IsPaused' 'pause state is exposed'
Assert-Contains $management 'GetManagementSnapshot\s*\(' 'management snapshot API exists'
Assert-Contains $management 'SyncOnlineBots\s*\(' 'explicit online synchronization exists'

$potionTick = [regex]::Match($manager, '(?s)private static void BotPotionTick\(object state\).*?(?=\r?\n\s*private static void |\z)').Value
Assert-Contains $potionTick 'BotPotionActionQueue\.Enqueue' 'potion timer uses only potion queue'
Assert-NotContains $potionTick 'BotActionQueue\.Enqueue' 'potion timer does not consume main AI queue budget'
Assert-Contains $manager 'BotActionQueue\.Enqueue' 'main timer still dispatches main actions'
Assert-Contains $seEnvir 'Config\.BotMainActionsPerFrame' 'original loop uses configured main frame budget'
Assert-Contains $seEnvir 'Config\.BotPotionActionsPerFrame' 'original loop uses configured potion frame budget'
Assert-Contains $seEnvir 'BotPotionActionQueue\.TryDequeue' 'original loop drains potion queue independently'
Assert-Contains $seEnvir 'BotActionQueue\.TryDequeue' 'original loop drains main queue'
Assert-Contains $seEnvir 'BotAction' 'main queue exceptions stay isolated'
Assert-Contains $seEnvir 'BotPotionAction' 'potion queue exceptions stay isolated'
Assert-Contains $seEnvir 'int botConsumeLimit2?\s*=\s*(Math\.Max\([^;]*,\s*)?Config\.BotMainActionsPerFrame' 'second loop uses configured main budget'
Assert-Contains $seEnvir 'int botPotionConsumeLimit2?\s*=\s*(Math\.Max\([^;]*,\s*)?Config\.BotPotionActionsPerFrame' 'second loop uses configured potion budget'
Assert-NotContains $seEnvir 'int botConsumeLimit\s*=\s*200|int botConsumeLimit2\s*=\s*200' 'queue budgets are not hardcoded'
Assert-Contains $manager 'botTimer\.Change\(0,\s*(Math\.Max\([^;]*,\s*)?Config\.BotMainLoopIntervalMs' 'main timer interval is configurable'
Assert-Contains $manager 'botPotionTimer\.Change\(0,\s*(Math\.Max\([^;]*,\s*)?Config\.BotPotionMonitorIntervalMs' 'potion timer interval is configurable'
Assert-Contains $manager '_botQueued' 'main anti-backlog guard remains'
Assert-Contains $manager '_botPotionQueued' 'potion anti-backlog guard remains'
Assert-Contains $manager 'IsPaused' 'pause state is consulted by runtime'
Assert-Contains $manager 'ProcessBotPotionModule' 'potion logic remains on a queued main-thread action'
Assert-Contains $management 'ConfigReader\.Save\(\)' 'persisted apply saves config'
Assert-Contains $management 'TryValidate' 'apply validates before mutation'

$stopMethod = [regex]::Match($manager, '(?s)public static void Stop\s*\(.*?(?=\r?\n\s*(?:public|private|protected|internal)\s+[^;\r\n]+\()').Value
Assert-Contains $stopMethod 'public static void Stop' 'stop method block is extracted'
Assert-Contains $stopMethod 'ResetRuntimeQuickTuning\s*\(\s*"\u505c\u6b62\u5047\u4eba"\s*\)' 'stop resets runtime quick tuning'
$stopRunningIndex = $stopMethod.IndexOf('isRunning = false')
$stopResetIndex = $stopMethod.IndexOf('ResetRuntimeQuickTuning')
$script:Assertions++
if ($stopRunningIndex -lt 0 -or $stopResetIndex -lt 0 -or $stopResetIndex -le $stopRunningIndex) {
    throw 'FAIL: stop resets quick tuning only after marking the manager stopped'
}

$removeConnectionMethod = [regex]::Match($support, '(?s)public static void RemoveBotConnection\s*\(.*?(?=\r?\n\s*(?:public|private|protected|internal)\s+[^;\r\n]+\()').Value
Assert-Contains $removeConnectionMethod 'public static void RemoveBotConnection' 'remove connection method block is extracted'
Assert-Contains $removeConnectionMethod 'SnapshotBotPlayers\(\)\.Length\s*==\s*0' 'last bot detection uses a snapshot after removal'
Assert-Contains $removeConnectionMethod 'ResetRuntimeQuickTuning\s*\(\s*"\u6700\u540e\u4e00\u540d\u5047\u4eba\u5df2\u4e0b\u7ebf"\s*\)' 'last bot disconnect resets runtime quick tuning'
$playerRemoveIndex = $removeConnectionMethod.LastIndexOf('SEnvir.Players.Remove(player)')
$connectionResetIndex = $removeConnectionMethod.IndexOf('ResetRuntimeQuickTuning')
$script:Assertions++
if ($playerRemoveIndex -lt 0 -or $connectionResetIndex -le $playerRemoveIndex) {
    throw 'FAIL: disconnect reset must run after removing the player from the server collection'
}

Write-Host "RESULT: PASS ($script:Assertions assertions)"
