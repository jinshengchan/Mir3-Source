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
$managementPath = Join-Path $root 'Server\BotManager.Management.cs'
$rewardsPath = Join-Path $root 'Server\BotManager.Rewards.cs'
$combatPath = Join-Path $root 'Server\BotManager.Combat.cs'
$supportPath = Join-Path $root 'Server\BotManager.Support.cs'
$mainPath = Join-Path $root 'Server\SMain.cs'
$management = if (Test-Path -LiteralPath $managementPath) { Get-Content -Raw -LiteralPath $managementPath } else { '' }
$rewards = if (Test-Path -LiteralPath $rewardsPath) { Get-Content -Raw -LiteralPath $rewardsPath } else { '' }
$combat = Get-Content -Raw -LiteralPath $combatPath
$support = Get-Content -Raw -LiteralPath $supportPath
$main = Get-Content -Raw -LiteralPath $mainPath

foreach ($symbol in @(
    'class BotManagementSnapshot','class BotBatchResult','GetManagementSnapshot\s*\(',
    'SyncOnlineBots\s*\(', 'SetTargetOnlineCount\s*\(', 'RecordManagementLog\s*\(',
    'GetMissingBotRewardReport\s*\(', 'BackfillMissingBotRewards\s*\(',
    'ActivityLogs|OperationLogs|activity|operation', 'MaxLog|Bounded|Take\('
)) {
    Assert-Contains ($management + "`n" + $rewards) $symbol "management operation symbol $symbol exists"
}
Assert-Contains $management 'OnlineBotCount' 'snapshot includes online bot count'
Assert-Contains $management 'TotalKills' 'snapshot includes session kills'
Assert-Contains $management 'TotalDeaths' 'snapshot includes session deaths'
Assert-Contains $management 'HashSet' 'snapshot uses a distinct-map set'
Assert-Contains $management 'map' 'snapshot includes map coverage data'
Assert-Contains $management 'TotalGold' 'snapshot sums online gold'
Assert-Contains $management 'AverageLevel' 'snapshot computes average level'
Assert-Contains $management 'ToArray' 'snapshot returns copied collections'
Assert-Contains $management 'Protected' 'batch result separates protected outcomes'
Assert-Contains $management 'BotMapPoolBonus' 'map score uses configurable pool bonus'
Assert-Contains $combat 'BotMapSwitchScoreGapMax' 'map candidate pool honors score gap'
Assert-Contains $support 'BotPeriodicGroupSeconds' 'periodic group setting is consumed'
Assert-Contains $support 'GetBotManualMapSwitchBlockReason' 'existing group/map protections remain'
Assert-Contains $management 'IsPaused' 'snapshot exposes pause status'
Assert-Contains $management 'Interlocked' 'management state is thread safe'
Assert-Contains $management 'enum BotRuntimeQuickTuningTarget' 'quick tuning target enum exists'
Assert-Contains $management 'class BotRuntimeQuickTuningSnapshot' 'quick tuning snapshot exists'
foreach ($property in @(
    'bool Active', 'bool Changed', 'int AggressionPercent', 'int ActivityPercent',
    'int MinHealthPotionCount', 'int MinManaPotionCount', 'string Message'
)) {
    Assert-Contains $management $property "quick tuning snapshot exposes $property"
}
Assert-Contains $management 'AdjustRuntimeQuickTuning\s*\(\s*BotRuntimeQuickTuningTarget target, int delta\)' 'quick tuning adjust API exists'
Assert-Contains $management 'GetRuntimeQuickTuningSnapshot\s*\(' 'quick tuning snapshot API exists'
Assert-Contains $management 'ResetRuntimeQuickTuning\s*\(string reason\)' 'quick tuning reset API exists'
Assert-Contains $management 'CommitRuntimeQuickTuningBaseline\s*\(' 'quick tuning commit API exists'
Assert-Contains $management '_managementSync' 'quick tuning uses the management lock'
Assert-Contains $management 'Config\.BotAggressionPercent' 'quick tuning changes aggression runtime config'
Assert-Contains $management 'Config\.BotActivityPercent' 'quick tuning changes activity runtime config'
Assert-Contains $management 'Config\.BotMinHealthPotionCount' 'quick tuning changes health potion runtime config'
Assert-Contains $management 'Config\.BotMinManaPotionCount' 'quick tuning changes mana potion runtime config'
$adjustStart = $management.IndexOf('AdjustRuntimeQuickTuning')
$adjustEnd = $management.IndexOf('GetRuntimeQuickTuningSnapshot', $adjustStart)
$adjustBody = if ($adjustStart -ge 0 -and $adjustEnd -gt $adjustStart) { $management.Substring($adjustStart, $adjustEnd - $adjustStart) } else { '' }
$lockStart = $adjustBody.IndexOf('lock (_managementSync)')
$onlineSnapshotStart = $adjustBody.IndexOf('SnapshotBotPlayers()')
$lockEnd = if ($lockStart -ge 0) { $adjustBody.IndexOf("`n            }", $lockStart) } else { -1 }
$script:Assertions++
if ($lockStart -lt 0 -or $onlineSnapshotStart -lt $lockStart -or $lockEnd -lt 0 -or $onlineSnapshotStart -gt $lockEnd) {
    throw 'FAIL: online bot snapshot must be taken inside the _managementSync lock'
}
Assert-NotContains $adjustBody 'ConfigReader\.Save\(\)' 'temporary quick tuning never saves config'
Assert-Contains $management '当前没有在线假人，快捷调整未执行' 'quick tuning has the no-online guard message'
Assert-Contains $management 'RecordManagementLog\(BotLogKind\.Operation' 'quick tuning records operation logs'
Assert-Contains $main 'BotManager\.Initialize\(\)' 'auto-start follows initialization'
Assert-Contains $main 'Config\.EnableBotSystem' 'auto-start checks enabled flag'
Assert-Contains $main 'File\.Exists\(Config\.BotFilePath\)' 'auto-start checks bot file existence'
Assert-Contains $main 'BotManagementSettings\.FromConfig' 'auto-start validates settings'
Assert-Contains $main 'BotManager.Start' 'auto-start calls start once'
Assert-Contains $main 'catch' 'auto-start failure is logged'

$artifactRoot = Join-Path $root '.artifacts'
$libraryPath = Join-Path $root 'ServerLibrary\bin\Debug\netstandard2.0\Library.dll'
$artifact = Get-ChildItem -LiteralPath $artifactRoot -Directory -Filter 'bot-management-*' -ErrorAction SilentlyContinue |
    ForEach-Object { Get-Item -LiteralPath (Join-Path $_.FullName 'Server.exe') -ErrorAction SilentlyContinue } |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 1
$script:Assertions++
if ($null -eq $artifact) { throw 'FAIL: no bot management Server.exe artifact found for quick tuning reflection' }

$reflectionScript = @"
`$ErrorActionPreference = 'Stop'
`$artifactPath = '$($artifact.FullName)'
`$libraryPath = '$libraryPath'
`$artifactDirectory = Split-Path -Parent `$artifactPath
`$resolver = [System.ResolveEventHandler]{
    param(`$sender, `$resolveArgs)
    `$assemblyName = (`$resolveArgs.Name.Split(',')[0] + '.dll')
    `$candidate = Join-Path `$artifactDirectory `$assemblyName
    if (Test-Path -LiteralPath `$candidate) { return [System.Reflection.Assembly]::LoadFrom(`$candidate) }
    if (`$assemblyName -eq 'Library.dll' -and (Test-Path -LiteralPath `$libraryPath)) { return [System.Reflection.Assembly]::LoadFrom(`$libraryPath) }
    return `$null
}
[System.AppDomain]::CurrentDomain.add_AssemblyResolve(`$resolver)
`$assembly = [System.Reflection.Assembly]::LoadFrom(`$artifactPath)
`$libraryAssembly = [System.Reflection.Assembly]::LoadFrom(`$libraryPath)
`$flags = [System.Reflection.BindingFlags]::Static -bor [System.Reflection.BindingFlags]::Public -bor [System.Reflection.BindingFlags]::NonPublic
`$configType = `$libraryAssembly.GetType('Server.Envir.Config')
`$managerType = `$assembly.GetType('Server.Envir.BotManager')
`$targetType = `$assembly.GetType('Server.Envir.BotRuntimeQuickTuningTarget')
`$snapshotType = `$assembly.GetType('Server.Envir.BotRuntimeQuickTuningSnapshot')
if (`$null -eq `$configType -or `$null -eq `$managerType -or `$null -eq `$targetType -or `$null -eq `$snapshotType) { throw 'Required quick tuning types not found' }
`$tempLogDirectory = Join-Path ([System.IO.Path]::GetTempPath()) ('bot-management-contract-' + [Guid]::NewGuid().ToString('N'))
`$configType.GetProperty('BotLogDirectory').SetValue(`$null, `$tempLogDirectory, `$null)
`$configType.GetProperty('BotAggressionPercent').SetValue(`$null, 50, `$null)
`$configType.GetProperty('BotActivityPercent').SetValue(`$null, 50, `$null)
`$configType.GetProperty('BotMinHealthPotionCount').SetValue(`$null, 80, `$null)
`$configType.GetProperty('BotMinManaPotionCount').SetValue(`$null, 80, `$null)
`$managerType.GetMethod('CommitRuntimeQuickTuningBaseline', `$flags).Invoke(`$null, `$null) | Out-Null
`$playersField = `$managerType.GetField('botPlayers', `$flags)
`$players = `$playersField.GetValue(`$null)
`$playerType = `$libraryAssembly.GetType('Server.Models.PlayerObject')
`$fakePlayer = [System.Runtime.Serialization.FormatterServices]::GetUninitializedObject(`$playerType)
`$nodeField = `$playerType.GetField('Node')
`$nodeField.SetValue(`$fakePlayer, [System.Runtime.Serialization.FormatterServices]::GetUninitializedObject(`$nodeField.FieldType))
`$players.Add(`$fakePlayer)
`$adjust = `$managerType.GetMethod('AdjustRuntimeQuickTuning', `$flags)
`$getSnapshot = `$managerType.GetMethod('GetRuntimeQuickTuningSnapshot', `$flags)
`$reset = `$managerType.GetMethod('ResetRuntimeQuickTuning', `$flags)
`$commit = `$managerType.GetMethod('CommitRuntimeQuickTuningBaseline', `$flags)
`$aggression = [Enum]::Parse(`$targetType, 'Aggression')
`$activity = [Enum]::Parse(`$targetType, 'Activity')
`$potion = [Enum]::Parse(`$targetType, 'PotionMinimums')
`$adjust.Invoke(`$null, @(`$aggression, 10)) | Out-Null
`$adjust.Invoke(`$null, @(`$activity, -10)) | Out-Null
`$adjust.Invoke(`$null, @(`$potion, 5)) | Out-Null
`$snapshot = `$getSnapshot.Invoke(`$null, `$null)
'ADJUST={0},{1},{2},{3};ACTIVE={4};CHANGED={5}' -f `$snapshot.AggressionPercent, `$snapshot.ActivityPercent, `$snapshot.MinHealthPotionCount, `$snapshot.MinManaPotionCount, `$snapshot.Active, `$snapshot.Changed
`$resetResult = `$reset.Invoke(`$null, @('contract reset'))
`$snapshot = `$getSnapshot.Invoke(`$null, `$null)
'RESET={0};VALUES={1},{2},{3},{4};ACTIVE={5}' -f `$resetResult, `$snapshot.AggressionPercent, `$snapshot.ActivityPercent, `$snapshot.MinHealthPotionCount, `$snapshot.MinManaPotionCount, `$snapshot.Active
`$secondReset = `$reset.Invoke(`$null, @('contract idempotent reset'))
'SECOND_RESET={0}' -f `$secondReset
`$adjust.Invoke(`$null, @(`$aggression, 10)) | Out-Null
`$commit.Invoke(`$null, `$null) | Out-Null
`$snapshot = `$getSnapshot.Invoke(`$null, `$null)
`$afterCommitReset = `$reset.Invoke(`$null, @('contract committed baseline'))
`$afterCommit = `$getSnapshot.Invoke(`$null, `$null)
'COMMIT={0},{1};RESET_AFTER_COMMIT={2};VALUE_AFTER_RESET={3}' -f `$snapshot.AggressionPercent, `$snapshot.Active, `$afterCommitReset, `$afterCommit.AggressionPercent
`$configType.GetProperty('BotAggressionPercent').SetValue(`$null, 100, `$null)
`$configType.GetProperty('BotActivityPercent').SetValue(`$null, 0, `$null)
`$cases = @(
    @{ Label = 'POTION_UPPER'; Health = 10000; Mana = 5000; Delta = 5 },
    @{ Label = 'POTION_LOWER'; Health = 0; Mana = 5000; Delta = -5 }
)
foreach (`$case in `$cases) {
    `$configType.GetProperty('BotMinHealthPotionCount').SetValue(`$null, `$case.Health, `$null)
    `$configType.GetProperty('BotMinManaPotionCount').SetValue(`$null, `$case.Mana, `$null)
    `$commit.Invoke(`$null, `$null) | Out-Null
    `$potionSnapshot = `$adjust.Invoke(`$null, @(`$potion, `$case.Delta))
    '{0}={1},{2};CHANGED={3};MESSAGE={4}' -f `$case.Label, `$potionSnapshot.MinHealthPotionCount, `$potionSnapshot.MinManaPotionCount, `$potionSnapshot.Changed, `$potionSnapshot.Message
    `$reset.Invoke(`$null, @('contract potion case reset')) | Out-Null
}
`$players.Remove(`$fakePlayer) | Out-Null
`$configType.GetProperty('BotAggressionPercent').SetValue(`$null, 50, `$null)
`$configType.GetProperty('BotActivityPercent').SetValue(`$null, 50, `$null)
`$configType.GetProperty('BotMinHealthPotionCount').SetValue(`$null, 80, `$null)
`$configType.GetProperty('BotMinManaPotionCount').SetValue(`$null, 80, `$null)
`$commit.Invoke(`$null, `$null) | Out-Null
`$noOnlineSnapshot = `$adjust.Invoke(`$null, @(`$aggression, 10))
'NO_ONLINE={0},{1},{2},{3};ACTIVE={4};MESSAGE={5}' -f `$noOnlineSnapshot.AggressionPercent, `$noOnlineSnapshot.ActivityPercent, `$noOnlineSnapshot.MinHealthPotionCount, `$noOnlineSnapshot.MinManaPotionCount, `$noOnlineSnapshot.Active, `$noOnlineSnapshot.Message
if (Test-Path -LiteralPath `$tempLogDirectory) { Remove-Item -LiteralPath `$tempLogDirectory -Recurse -Force }
"@
$windowsPowerShell = Join-Path $env:WINDIR 'System32\WindowsPowerShell\v1.0\powershell.exe'
$reflectionOutput = & $windowsPowerShell -NoProfile -STA -ExecutionPolicy Bypass -Command $reflectionScript 2>&1
$reflectionExitCode = $LASTEXITCODE
$script:Assertions++
if ($reflectionExitCode -ne 0) { throw "FAIL: quick tuning reflection process failed`n$reflectionOutput" }
foreach ($expected in @(
    '^ADJUST=60,40,85,85;ACTIVE=True;CHANGED=True$',
    '^RESET=True;VALUES=50,50,80,80;ACTIVE=False$',
    '^SECOND_RESET=False$',
    '^COMMIT=60,False;RESET_AFTER_COMMIT=False;VALUE_AFTER_RESET=60$',
    '^NO_ONLINE=50,50,80,80;ACTIVE=False;MESSAGE=\u5f53\u524d\u6ca1\u6709\u5728\u7ebf\u5047\u4eba\uff0c\u5feb\u6377\u8c03\u6574\u672a\u6267\u884c$'
)) {
    $script:Assertions++
    if (($reflectionOutput | Where-Object { $_ -match $expected } | Select-Object -Last 1) -eq $null) {
        throw "FAIL: quick tuning reflection did not match $expected`n$reflectionOutput"
    }
}
foreach ($expectation in @(
    @{ Label = 'POTION_UPPER'; Health = 10000; Mana = 5005; Forbidden = '\u5df2\u8fbe\u5230\u4e0a\u9650' },
    @{ Label = 'POTION_LOWER'; Health = 0; Mana = 4995; Forbidden = '\u5df2\u8fbe\u5230\u4e0b\u9650' }
)) {
    $pattern = '^{0}={1},{2};CHANGED=True;MESSAGE=' -f $expectation.Label, $expectation.Health, $expectation.Mana
    $line = $reflectionOutput | Where-Object { $_ -match $pattern } | Select-Object -Last 1
    $script:Assertions++
    if ($null -eq $line) { throw "FAIL: potion case did not apply the expected HP/MP values: $pattern`n$reflectionOutput" }
    $script:Assertions++
    if ($line -match $expectation.Forbidden) { throw "FAIL: potion case reported a boundary without applying the changed value: $line" }
    $script:Assertions++
    if ($line -notmatch 'HP' -or $line -notmatch 'MP' -or $line -notmatch ([string]$expectation.Mana)) {
        throw "FAIL: potion case message did not report the actual HP/MP result: $line"
    }
}

Write-Host "RESULT: PASS ($script:Assertions assertions)"
