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
$settingsPath = Join-Path $root 'Server\BotManagementSettings.cs'
$configPath = Join-Path $root 'ServerLibrary\Envir\Config.cs'
$projectPath = Join-Path $root 'Server\Server.csproj'
$settings = if (Test-Path -LiteralPath $settingsPath) { Get-Content -Raw -LiteralPath $settingsPath } else { '' }
$config = Get-Content -Raw -LiteralPath $configPath
$project = Get-Content -Raw -LiteralPath $projectPath

Assert-Contains $settings 'public sealed class BotManagementSettings' 'typed management settings model exists'
foreach ($property in @(
    'AggressionPercent','ActivityPercent','GroupTendencyPercent','ChatFrequencyPercent',
    'PercentRecoveryEnabled','FixedRecoveryEnabled','PercentRecoveryPerSecond','FixedRecoveryPerSecond',
    'ProactivePvpMinLevel','AutoRebirthLevel','AutoRebirthMaxCount','MainActionsPerFrame','PotionActionsPerFrame',
    'FromConfig\s*\(', 'TryValidate\s*\(out string error\)', 'WriteToConfig\s*\('
)) {
    Assert-Contains $settings $property "settings interface/property $property exists"
}

foreach ($property in @(
    'BotEnableChat','BotAutoLevel','BotAutoPickup','BotAutoSellTrash','BotAutoPotionSupply','BotAutoEquip',
    'BotAutoLearnSkill','BotAutoGroup','BotAutoTrade','BotGuildSystem','BotParticipateConquest','BotPvpRetaliation',
    'BotAutoMapSwitch','BotSkipPickupWhenGroupedWithHuman','BotAutoRebirth','BotPercentRecoveryEnabled',
    'BotFixedRecoveryEnabled','BotAutoSpecialRepair','BotProactivePvpMinLevel','BotAutoRebirthLevel',
    'BotAutoRebirthMaxCount','BotDefenseLevelInterval','BotDefenseBonusPerTier','BotStrongElementStartLevel',
    'BotStrongElementLevelInterval','BotStrongElementTypeCount','BotPercentRecoveryPerSecond',
    'BotFixedRecoveryPerSecond','BotGlobalChatIntervalSeconds','BotSpecialRepairThresholdPercent',
    'BotRecallBatchIntervalMs','BotRecallBatchSize','BotAggressionPercent','BotActivityPercent',
    'BotGroupTendencyPercent','BotChatFrequencyPercent','BotInitialGoldFloor','BotGoldFarmThreshold',
    'BotMinHealthPotionCount','BotMinManaPotionCount','BotTickDispatchLimit','BotMainLoopIntervalMs',
    'BotMaxOnline','BotPotionMonitorIntervalMs','BotFullHealthThresholdPercent','BotAttackAttemptIntervalMs',
    'BotPickupAttemptIntervalMs','BotPickupRadius','BotMapPoolBonus','BotMapSwitchScoreGapMax',
    'BotPeriodicGroupSeconds','BotMainActionsPerFrame','BotPotionActionsPerFrame','BotLogDirectory'
)) {
    Assert-Contains $config "public static [^\r\n]+ $property\s*\{" "Config property $property exists"
}

foreach ($default in @(
    'BotAggressionPercent[^\r\n]*= 50','BotActivityPercent[^\r\n]*= 50','BotGroupTendencyPercent[^\r\n]*= 50',
    'BotChatFrequencyPercent[^\r\n]*= 50','BotInitialGoldFloor[^\r\n]*= 100000',
    'BotMinHealthPotionCount[^\r\n]*= 80','BotMinManaPotionCount[^\r\n]*= 80',
    'BotMainLoopIntervalMs[^\r\n]*= 200','BotPotionMonitorIntervalMs[^\r\n]*= 200',
    'BotSpecialRepairThresholdPercent[^\r\n]*= 50','BotMainActionsPerFrame[^\r\n]*= 200'
)) {
    Assert-Contains $config $default "compatibility default $default"
}

Assert-Contains $settings 'PercentRecoveryEnabled\s*&&\s*FixedRecoveryEnabled' 'recovery modes are mutually exclusive'
Assert-Contains $settings '0\s*[-<]\s*100|Math\.Min\(100|Math\.Max\(0|>=\s*0\s*&&\s*value\s*<=\s*100' 'percentage bounds are validated'
Assert-Contains $settings '60000' 'interval upper bound is validated'
Assert-Contains $settings '10000' 'quantity or queue upper bound is validated'
Assert-Contains $settings 'AutoRebirthMaxCount[^\r\n]*>\s*0' 'rebirth cap requires a nonzero level'
Assert-Contains $settings 'Config\.Bot' 'settings map to Config'
Assert-Contains $settings 'TryValidate\(out string error\)' 'write path exposes validation result'
Assert-Contains $settings 'WriteToConfig' 'settings can persist into Config'
Assert-Contains $project '<Compile Include="BotManagementSettings\.cs"\s*/>' 'new settings file is compiled'

Write-Host "RESULT: PASS ($script:Assertions assertions)"
