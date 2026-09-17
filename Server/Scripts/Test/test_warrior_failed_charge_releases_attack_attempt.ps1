$ErrorActionPreference = 'Stop'

$sourcePath = Join-Path $PSScriptRoot '..\..\BotManager.Combat.cs'
$source = Get-Content -LiteralPath $sourcePath -Raw

$method = [regex]::Match(
    $source,
    'private static bool TryPrepareBotWarriorChargedAttack\([\s\S]*?\n        \}',
    [System.Text.RegularExpressions.RegexOptions]::Singleline)

if (-not $method.Success) {
    throw '找不到 TryPrepareBotWarriorChargedAttack。'
}

if ($method.Value -notmatch '_botNextAttackAttemptTime\.TryGetValue') {
    throw '战士蓄力前未保存原攻击节流状态。'
}

if ($method.Value -notmatch 'if \(!castSucceeded\)') {
    throw '战士蓄力失败后未进入节流恢复分支。'
}

if ($method.Value -notmatch '_botNextAttackAttemptTime\.Remove') {
    throw '战士蓄力失败且原无节流时未释放本次占用。'
}

Write-Host 'PASS: failed warrior charge releases attack attempt'
