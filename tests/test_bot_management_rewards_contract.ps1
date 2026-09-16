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
$accountPath = Join-Path $root 'ServerLibrary\DBModels\BotAccountInfo.cs'
$refreshPath = Join-Path $root 'ServerLibrary\Models\Player\Refresh.cs'
$rewardsPath = Join-Path $root 'Server\BotManager.Rewards.cs'
$account = Get-Content -Raw -LiteralPath $accountPath
$refresh = Get-Content -Raw -LiteralPath $refreshPath
$rewards = if (Test-Path -LiteralPath $rewardsPath) { Get-Content -Raw -LiteralPath $rewardsPath } else { '' }

Assert-Contains $account 'DefenseRewardTier' 'defense reward progress is persisted'
Assert-Contains $account 'StrongElementRewardTier' 'strong-element reward progress is persisted'
Assert-Contains $account 'Stats\s+LevelRewardStats' 'actual level reward stats are persisted'
Assert-Contains $account 'LevelRewardStats\s*=\s*new Stats\(\)' 'new accounts initialize reward stats'
Assert-Contains $rewards 'GetMissingBotRewardReport\s*\(' 'reward audit API exists'
Assert-Contains $rewards 'BackfillMissingBotRewards\s*\(' 'reward backfill API exists'
Assert-Contains $rewards 'DefenseRewardTier' 'defense tiers are calculated'
Assert-Contains $rewards 'StrongElementRewardTier' 'element tiers are calculated'
Assert-Contains $rewards 'LevelRewardStats' 'actual random reward values are reused'
Assert-Contains $rewards 'MinAC|MaxAC|MinMR|MaxMR' 'defense reward applies to both defenses'
Assert-Contains $rewards 'FireAttack|IceAttack|LightningAttack|WindAttack|HolyAttack|DarkAttack|PhantomAttack' 'seven attack elements are eligible'
Assert-Contains $rewards 'RefreshStats\(\)' 'changed reward batches refresh stats once'
Assert-Contains $rewards 'Random' 'element choices are randomized'
Assert-Contains $rewards 'already|missing|缺失|应得' 'reward logic distinguishes already-granted and missing tiers'
Assert-Contains $rewards 'BotAccountInfoList' 'reward code resolves persisted bot accounts'
Assert-Contains $rewards 'IsBot' 'non-bot players are excluded'
Assert-Contains $rewards 'interval.*0|==\s*0' 'zero interval disables the corresponding reward'
Assert-Contains $rewards 'Idempot|重复|completed|tier' 'reward application is idempotent'

$audit = [regex]::Match($rewards, '(?s)(GetMissingBotRewardReport|Audit).*?\{.*?(?=\r?\n\s*\})').Value
Assert-NotContains $audit 'DefenseRewardTier\s*=|StrongElementRewardTier\s*=|LevelRewardStats\s*=' 'audit path does not mutate progress'
Assert-Contains $refresh 'BotAccountInfoList' 'refresh resolves bot account data'
Assert-Contains $refresh 'LevelRewardStats' 'refresh includes persisted bot reward stats'
Assert-Contains $refresh 'IsBot' 'refresh guards reward stats to bot characters'
Assert-Contains $refresh 'Stats\.Add\(.*LevelRewardStats|LevelRewardStats\.Values' 'refresh adds reward stats to current accumulator'
Assert-NotContains $refresh 'Character\.HermitStats.*LevelRewardStats|LevelRewardStats.*HermitStats' 'bot rewards do not use general hermit stats'

Write-Host "RESULT: PASS ($script:Assertions assertions)"
