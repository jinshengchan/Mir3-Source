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
$uiPath = Join-Path $root 'Server\Views\BotConfigView.cs'
$mainPath = Join-Path $root 'Server\SMain.cs'
$ui = Get-Content -Raw -Encoding UTF8 -LiteralPath $uiPath
$main = Get-Content -Raw -Encoding UTF8 -LiteralPath $mainPath

$splitControlsPosition = $ui.IndexOf('Controls.Add(split)')
$splitDistanceMatches = [regex]::Matches($ui, 'split\.SplitterDistance\s*=')
$splitDistancePosition = if ($splitDistanceMatches.Count -eq 0) { -1 } else { $splitDistanceMatches[$splitDistanceMatches.Count - 1].Index }
$script:Assertions++
if ($splitControlsPosition -lt 0 -or $splitDistancePosition -lt 0 -or $splitControlsPosition -ge $splitDistancePosition) {
    throw 'FAIL: split splitter distance must be assigned after the split container is added to the form'
}
Assert-Contains $ui 'LeftPanelWidth\s*=\s*800' 'left panel target width is 800'
Assert-Contains $ui 'LeftGroupWidth\s*=\s*775' 'left group width uses the wide layout'
Assert-Contains $ui 'RightPanelMinWidth\s*=\s*520' 'right panel keeps its minimum width'
Assert-Contains $ui 'HalfRowWidth\s*=\s*365' 'half-width rows use the wide layout'
Assert-Contains $ui 'FullRowWidth\s*=\s*745' 'full-width rows use the wide layout'
Assert-Contains $ui 'GetGroupFlow\s*\(GroupBox group, bool twoColumn, int contentWidth\)' 'group flow helper supports columns'
Assert-Contains $ui 'AddFullWidthControl\s*\(' 'full-width layout helper exists'
Assert-Contains $ui 'LeftOperationButtonMaxWidth\s*=\s*180' 'left operation buttons have a compact maximum width'
Assert-Contains $ui 'RightQuickButtonMaxWidth\s*=\s*220' 'right quick-action buttons have a compact maximum width'
Assert-Contains $ui 'MapButtonMaxWidth\s*=\s*150' 'quick-map buttons have a compact maximum width'
Assert-Contains $ui 'AddButtonRow\s*\(FlowLayoutPanel flow, int rowWidth, int maxButtonWidth, params Button\[\] buttons\)' 'button rows expose a maximum-width overload'
Assert-Contains $ui 'ResizeRightColumnGroups\s*\(' 'right column resize helper exists'
Assert-Contains $ui 'HorizontalScroll\.Enabled\s*=\s*false' 'horizontal scrolling is disabled'
Assert-Contains $ui 'BotQuickActionStatusLabel' 'quick tuning has a nonblocking status label'
Assert-Contains $ui 'ApplyRuntimeQuickTuning\s*\(' 'quick tuning buttons use one UI handler'
Assert-Contains $ui 'BotManager\.AdjustRuntimeQuickTuning' 'quick tuning delegates to the runtime manager API'
$quickHandlerStart = $ui.IndexOf('private void ApplyRuntimeQuickTuning')
$quickHandlerEnd = $ui.IndexOf('private void RefreshRuntimeQuickTuningControls', $quickHandlerStart)
$quickHandlerBody = if ($quickHandlerStart -ge 0 -and $quickHandlerEnd -gt $quickHandlerStart) { $ui.Substring($quickHandlerStart, $quickHandlerEnd - $quickHandlerStart) } else { '' }
Assert-NotContains $quickHandlerBody 'MessageBox\.Show' 'quick tuning does not show blocking message boxes'
Assert-Contains $quickHandlerBody 'RefreshRuntimeQuickTuningControls' 'quick tuning refreshes controls and status'
Assert-Contains $ui 'BotQuickActionStatusLabel\.Text' 'quick tuning updates the status label'

$artifactRoot = Join-Path $root '.artifacts'
$libraryPath = Join-Path $root 'ServerLibrary\bin\Debug\netstandard2.0\Library.dll'
$artifact = Get-ChildItem -LiteralPath $artifactRoot -Directory -Filter 'bot-management-*' -ErrorAction SilentlyContinue |
    ForEach-Object { Get-Item -LiteralPath (Join-Path $_.FullName 'Server.exe') -ErrorAction SilentlyContinue } |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 1
$script:Assertions++
if ($null -eq $artifact) { throw 'FAIL: no bot management Server.exe artifact found for layout reflection' }

$reflectionScript = @"
`$ErrorActionPreference = 'Stop'
`$artifactPath = '$($artifact.FullName)'
`$libraryPath = '$libraryPath'
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
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
`$configType = `$libraryAssembly.GetType('Server.Envir.Config')
`$tempLogDirectory = Join-Path ([System.IO.Path]::GetTempPath()) ('bot-ui-contract-' + [Guid]::NewGuid().ToString('N'))
`$configType.GetProperty('BotLogDirectory').SetValue(`$null, `$tempLogDirectory, `$null)
`$form = [Activator]::CreateInstance(`$assembly.GetType('Server.Views.BotConfigView'))
`$form.ClientSize = New-Object System.Drawing.Size(1380, 780)
`$form.PerformLayout()
`$form.ShowInTaskbar = `$false
`$form.Show()
[System.Windows.Forms.Application]::DoEvents()
`$split = `$form.Controls | Where-Object { `$_.GetType().FullName -eq 'System.Windows.Forms.SplitContainer' } | Select-Object -First 1
if (`$null -eq `$split) { throw 'SplitContainer not found' }
`$split.PerformLayout()
function Get-Descendants(`$control) {
    foreach (`$child in `$control.Controls) {
        `$child
        Get-Descendants `$child
    }
}
function Find-ByName(`$root, [string]`$name) {
    if (`$root.Name -eq `$name) { return `$root }
    foreach (`$child in Get-Descendants `$root) {
        if (`$child.Name -eq `$name) { return `$child }
    }
    return `$null
}
function Get-AbsolutePoint(`$control) {
    `$x = `$control.Left
    `$y = `$control.Top
    `$parent = `$control.Parent
    while (`$null -ne `$parent) {
        `$x += `$parent.Left
        `$y += `$parent.Top
        `$parent = `$parent.Parent
    }
    return [pscustomobject]@{ X = `$x; Y = `$y }
}
function Get-FormPoint(`$control) {
    `$x = `$control.Left
    `$y = `$control.Top
    `$parent = `$control.Parent
    while (`$null -ne `$parent -and `$parent -ne `$form) {
        `$x += `$parent.Left
        `$y += `$parent.Top
        `$parent = `$parent.Parent
    }
    return [pscustomobject]@{ X = `$x; Y = `$y }
}
function Find-Group(`$root, [string]`$pattern) {
    foreach (`$candidate in Get-Descendants `$root) {
        if (`$candidate.GetType().FullName -eq 'System.Windows.Forms.GroupBox' -and `$candidate.Text -match `$pattern) {
            return `$candidate
        }
    }
    return `$null
}
function Get-Buttons(`$root) {
    @(Get-Descendants `$root | Where-Object { `$_.GetType().FullName -eq 'System.Windows.Forms.Button' })
}
function Get-RowCounts(`$controls) {
    `$groups = @{}
    foreach (`$control in `$controls) {
        `$point = Get-AbsolutePoint `$control
        `$key = [int]`$point.Y
        if (`$groups.ContainsKey(`$key)) { `$groups[`$key]++ } else { `$groups[`$key] = 1 }
    }
    return @(`$groups.Values | Sort-Object)
}
function Get-UniqueButtonRows(`$buttons) {
    `$rows = New-Object System.Collections.ArrayList
    foreach (`$button in @(`$buttons)) {
        `$found = `$false
        foreach (`$row in @(`$rows)) {
            if ([object]::ReferenceEquals(`$row, `$button.Parent)) {
                `$found = `$true
                break
            }
        }
        if (-not `$found) { [void]`$rows.Add(`$button.Parent) }
    }
    return @(`$rows)
}
function Get-ButtonLayoutMetrics(`$buttons) {
    `$buttons = @(`$buttons)
    if (`$buttons.Count -eq 0) { throw 'No buttons supplied for compact layout metrics' }
    `$rows = @(Get-UniqueButtonRows `$buttons)
    `$maxWidth = (`$buttons | Measure-Object -Property Width -Maximum).Maximum
    `$minWidth = (`$buttons | Measure-Object -Property Width -Minimum).Minimum
    `$minHeight = (`$buttons | Measure-Object -Property Height -Minimum).Minimum
    `$overflow = 0
    `$centerFailures = 0
    foreach (`$row in `$rows) {
        `$rowButtons = @(`$buttons | Where-Object { [object]::ReferenceEquals(`$_.Parent, `$row) })
        `$left = (`$rowButtons | Measure-Object -Property Left -Minimum).Minimum
        `$right = ((`$rowButtons | ForEach-Object { `$_.Left + `$_.Width }) | Measure-Object -Maximum).Maximum
        if ([Math]::Abs(`$left - (`$row.ClientSize.Width - `$right)) -gt 1) { `$centerFailures++ }
        foreach (`$button in `$rowButtons) {
            if (`$button.Left -lt 0 -or (`$button.Left + `$button.Width) -gt `$row.ClientSize.Width) { `$overflow++ }
        }
    }
    return [pscustomobject]@{
        MaxWidth = [int]`$maxWidth
        MinWidth = [int]`$minWidth
        MinHeight = [int]`$minHeight
        AllVisible = (@(`$buttons | Where-Object { -not `$_.Visible }).Count -eq 0)
        Details = (@(`$buttons | ForEach-Object { '{0}={1}x{2};Visible={3}' -f `$_.Text, `$_.Width, `$_.Height, `$_.Visible }) -join '|')
        Centered = (`$centerFailures -eq 0)
        Overflow = [int]`$overflow
        RowCount = [int]`$rows.Count
    }
}
function Get-CompactLayoutSnapshot([int]`$width, [int]`$height) {
    `$probeForm = [Activator]::CreateInstance(`$assembly.GetType('Server.Views.BotConfigView'))
    `$probeForm.ClientSize = New-Object System.Drawing.Size(`$width, `$height)
    `$probeForm.PerformLayout()
    `$probeForm.ShowInTaskbar = `$false
    `$probeForm.Show()
    [System.Windows.Forms.Application]::DoEvents()
    `$probeForm.PerformLayout()
    `$probeQuickGroup = Find-Group `$probeForm '\u5feb\u6377\u64cd\u4f5c'
    `$probeMapGroup = Find-Group `$probeForm '\u6309\u6863\u5feb\u901f\u5207\u56fe'
    if (`$null -eq `$probeQuickGroup -or `$null -eq `$probeMapGroup) { throw 'Compact layout groups not found' }
    `$probeInstanceFlags = [System.Reflection.BindingFlags]::Instance -bor [System.Reflection.BindingFlags]::NonPublic
    `$probeViewType = `$probeForm.GetType()
    `$probeLeftButtons = @('BotStartButton','BotStopButton','BotRecallButton','BotPauseButton','BotSaveButton','BotRefreshButton') |
        ForEach-Object { `$probeViewType.GetField(`$_, `$probeInstanceFlags).GetValue(`$probeForm) }
    `$probeQuickButtons = @(Get-Buttons `$probeQuickGroup)
    `$probeMapButtons = @(Get-Buttons `$probeMapGroup)
    `$snapshot = [pscustomobject]@{
        Size = '{0}x{1}' -f `$width, `$height
        Left = Get-ButtonLayoutMetrics `$probeLeftButtons
        Quick = Get-ButtonLayoutMetrics `$probeQuickButtons
        Map = Get-ButtonLayoutMetrics `$probeMapButtons
    }
    `$probeForm.Close()
    `$probeForm.Dispose()
    return `$snapshot
}
function Write-CompactLayoutSnapshot(`$snapshot) {
    'COMPACT_BUTTONS=Size={0};LeftMax={1};QuickMax={2};MapMax={3};Caps=Left<=180;Quick<=220;Map<=150' -f `$snapshot.Size, `$snapshot.Left.MaxWidth, `$snapshot.Quick.MaxWidth, `$snapshot.Map.MaxWidth
    'BUTTON_WIDTHS=Size={0};LeftMin={1};QuickMin={2};MapMin={3}' -f `$snapshot.Size, `$snapshot.Left.MinWidth, `$snapshot.Quick.MinWidth, `$snapshot.Map.MinWidth
    'BUTTON_STATE=Size={0};LeftMinHeight={1};QuickMinHeight={2};MapMinHeight={3};LeftVisible={4};QuickVisible={5};MapVisible={6}' -f `$snapshot.Size, `$snapshot.Left.MinHeight, `$snapshot.Quick.MinHeight, `$snapshot.Map.MinHeight, `$snapshot.Left.AllVisible, `$snapshot.Quick.AllVisible, `$snapshot.Map.AllVisible
    'BUTTON_DETAILS=Size={0};Left={1};Quick={2};Map={3}' -f `$snapshot.Size, `$snapshot.Left.Details, `$snapshot.Quick.Details, `$snapshot.Map.Details
    'CENTERING=Size={0};Left={1};Quick={2};Map={3}' -f `$snapshot.Size, `$snapshot.Left.Centered, `$snapshot.Quick.Centered, `$snapshot.Map.Centered
    'BUTTON_OVERFLOW=Size={0};Count={1}' -f `$snapshot.Size, (`$snapshot.Left.Overflow + `$snapshot.Quick.Overflow + `$snapshot.Map.Overflow)
}
`$autoLevel = Find-ByName `$form 'BotAutoLevelCheckEdit'
`$autoPickup = Find-ByName `$form 'BotAutoPickupCheckEdit'
`$goldFloor = Find-ByName `$form 'BotInitialGoldFloorEdit'
`$goldThreshold = Find-ByName `$form 'BotGoldFarmThresholdEdit'
`$quickGroup = Find-Group `$form '\u5feb\u6377\u64cd\u4f5c'
`$mapGroup = Find-Group `$form '\u6309\u6863\u5feb\u901f\u5207\u56fe'
if (`$null -eq `$autoLevel -or `$null -eq `$autoPickup -or `$null -eq `$goldFloor -or `$null -eq `$goldThreshold -or `$null -eq `$quickGroup -or `$null -eq `$mapGroup) { throw 'Required layout controls or groups not found' }
`$autoPoint = Get-AbsolutePoint `$autoLevel
`$pickupPoint = Get-AbsolutePoint `$autoPickup
`$goldPoint = Get-AbsolutePoint `$goldFloor
`$thresholdPoint = Get-AbsolutePoint `$goldThreshold
`$quickButtons = Get-Buttons `$quickGroup | Where-Object { `$_.Text -match '^\u653b\u51fb\u6027|^\u6d3b\u8dc3\u5ea6|^\u836f\u6c34\u8865\u7ed9' }
`$instanceFlags = [System.Reflection.BindingFlags]::Instance -bor [System.Reflection.BindingFlags]::NonPublic
`$viewType = `$form.GetType()
`$leftOperationButtons = @('BotStartButton','BotStopButton','BotRecallButton','BotPauseButton','BotSaveButton','BotRefreshButton') |
    ForEach-Object { `$viewType.GetField(`$_, `$instanceFlags).GetValue(`$form) }
`$rightQuickButtons = @(Get-Buttons `$quickGroup)
`$mapButtons = Get-Buttons `$mapGroup
`$quickRows = Get-RowCounts `$quickButtons
`$mapRows = Get-RowCounts `$mapButtons
`$leftColumn = `$split.Panel1.Controls | Where-Object { `$_.GetType().FullName -eq 'System.Windows.Forms.FlowLayoutPanel' } | Select-Object -First 1
`$rightColumn = `$split.Panel2.Controls | Where-Object { `$_.GetType().FullName -eq 'System.Windows.Forms.FlowLayoutPanel' } | Select-Object -First 1
if (`$null -eq `$leftColumn -or `$null -eq `$rightColumn) { throw 'Layout columns not found' }
`$groupHeightDetails = @()
`$groupHeightFailures = @()
foreach (`$columnInfo in @(
    @{ Name = 'LEFT'; Column = `$leftColumn },
    @{ Name = 'RIGHT'; Column = `$rightColumn }
)) {
    foreach (`$group in @(`$columnInfo.Column.Controls | Where-Object {
        `$_.GetType().FullName -eq 'System.Windows.Forms.GroupBox' -and `$_.Visible
    })) {
        `$flow = `$group.Controls | Where-Object {
            `$_.GetType().FullName -eq 'System.Windows.Forms.FlowLayoutPanel'
        } | Select-Object -First 1
        `$flowBottom = if (`$null -eq `$flow) { 0 } else { `$flow.Bottom }
        `$requiredHeight = `$flowBottom + `$group.Padding.Bottom
        `$heightOk = `$requiredHeight -le `$group.ClientSize.Height
        `$detail = '{0}:{1}=group={2};client={3};flowBottom={4};required={5};ok={6}' -f `$columnInfo.Name, `$group.Text, `$group.Height, `$group.ClientSize.Height, `$flowBottom, `$requiredHeight, `$heightOk
        `$groupHeightDetails += `$detail
        if (-not `$heightOk) { `$groupHeightFailures += `$detail }
    }
}
function Get-ColumnOverlaps(`$column, [string]`$name) {
    `$groups = @(`$column.Controls | Where-Object {
        `$_.GetType().FullName -eq 'System.Windows.Forms.GroupBox' -and `$_.Visible
    } | ForEach-Object {
        `$point = Get-FormPoint `$_
        [pscustomobject]@{ Name = `$_.Text; Top = `$point.Y; Bottom = `$point.Y + `$_.Height }
    } | Sort-Object Top)
    `$overlaps = @()
    for (`$index = 1; `$index -lt `$groups.Count; `$index++) {
        if (`$groups[`$index].Top -lt `$groups[`$index - 1].Bottom) {
            `$overlaps += '{0}>{1}' -f `$groups[`$index - 1].Name, `$groups[`$index].Name
        }
    }
    [pscustomobject]@{ Name = `$name; Count = `$overlaps.Count; Details = (`$overlaps -join ',') }
}
`$leftOverlap = Get-ColumnOverlaps `$leftColumn 'LEFT'
`$rightOverlap = Get-ColumnOverlaps `$rightColumn 'RIGHT'
`$quickControls = @(
    [pscustomobject]@{ Name = 'BotQuickRecallButton'; Control = `$viewType.GetField('BotQuickRecallButton', `$instanceFlags).GetValue(`$form) },
    [pscustomobject]@{ Name = 'BotQuickPauseButton'; Control = `$viewType.GetField('BotQuickPauseButton', `$instanceFlags).GetValue(`$form) },
    [pscustomobject]@{ Name = 'BotQuickSyncButton'; Control = `$viewType.GetField('BotQuickSyncButton', `$instanceFlags).GetValue(`$form) }
)
function Test-IsDescendantOf(`$control, `$root) {
    while (`$null -ne `$control) {
        if (`$control -eq `$root) { return `$true }
        `$control = `$control.Parent
    }
    return `$false
}
`$leftQuickNames = @(`$quickControls | Where-Object { `$_.Control.Visible -and (Test-IsDescendantOf `$_.Control `$split.Panel1) } | Select-Object -ExpandProperty Name)
`$rightQuickNames = @(`$quickControls | Where-Object { `$_.Control.Visible -and (Test-IsDescendantOf `$_.Control `$quickGroup) } | Select-Object -ExpandProperty Name | Sort-Object)
`$syncVisibleButtons = @(Get-Buttons `$form | Where-Object { `$_.Visible -and `$_.Text -match '^\u540c\u6b65\u5230\u5de6\u4fa7$' })
`$panel2Point = Get-FormPoint `$split.Panel2
`$panel2Right = `$panel2Point.X + `$split.Panel2.ClientSize.Width
`$allRightBounds = @(Get-Descendants `$split.Panel2 | Where-Object { `$_.Visible -and `$_.Width -gt 0 } | ForEach-Object {
    `$point = Get-FormPoint `$_
    [pscustomobject]@{ Name = if ([string]::IsNullOrWhiteSpace(`$_.Name)) { `$_.GetType().Name } else { `$_.Name }; Right = `$point.X + `$_.Width }
})
`$economySecond = Find-ByName `$form 'BotGoldFarmThresholdEdit'
`$performanceSecond = Find-ByName `$form 'BotMainLoopIntervalMsEdit'
`$featuresSecond = Find-ByName `$form 'BotPickupAttemptIntervalMsEdit'
`$economySecondRight = (Get-FormPoint `$economySecond).X + `$economySecond.Width
`$performanceSecondRight = (Get-FormPoint `$performanceSecond).X + `$performanceSecond.Width
`$featuresSecondRight = (Get-FormPoint `$featuresSecond).X + `$featuresSecond.Width
`$quickMaxRight = ((`$quickButtons | ForEach-Object { `$point = Get-FormPoint `$_; `$point.X + `$_.Width }) | Measure-Object -Maximum).Maximum
`$mapMaxRight = ((`$mapButtons | ForEach-Object { `$point = Get-FormPoint `$_; `$point.X + `$_.Width }) | Measure-Object -Maximum).Maximum
`$maxRight = (`$allRightBounds | Measure-Object -Property Right -Maximum).Maximum
`$overflowCount = @(`$allRightBounds | Where-Object { `$_.Right -gt `$panel2Right }).Count
'P1={0};P2={1};Form={2}x{3}' -f `$split.Panel1.Width, `$split.Panel2.Width, `$form.ClientSize.Width, `$form.ClientSize.Height
'AUTO={0},{1};{2},{3}' -f `$autoPoint.X, `$autoPoint.Y, `$pickupPoint.X, `$pickupPoint.Y
'ECONOMY={0},{1};{2},{3}' -f `$goldPoint.X, `$goldPoint.Y, `$thresholdPoint.X, `$thresholdPoint.Y
'QUICK={0};ROWS={1};COUNTS={2}' -f `$quickButtons.Count, `$quickRows.Count, (`$quickRows -join ',')
'MAPS={0};ROWS={1};COUNTS={2}' -f `$mapButtons.Count, `$mapRows.Count, (`$mapRows -join ',')
'GROUP_HEIGHTS={0}' -f (`$groupHeightDetails -join '|')
'OVERLAP=Left={0};Right={1};Details={2}' -f `$leftOverlap.Count, `$rightOverlap.Count, ((@(`$leftOverlap.Details, `$rightOverlap.Details) | Where-Object { `$_ }) -join '|')
'BUTTON_LOCATIONS=LeftQuick={0};RightQuick={1};SyncVisible={2};RightQuickNames={3}' -f (`$leftQuickNames -join ','), (`$rightQuickNames -join ','), `$syncVisibleButtons.Count, (`$rightQuickNames -join ',')
'RIGHT_BOUNDS=Panel2Right={0};MaxRight={1};EconomySecondRight={2};PerformanceSecondRight={3};FeaturesSecondRight={4};QuickMaxRight={5};MapMaxRight={6};Overflow={7}' -f `$panel2Right, `$maxRight, `$economySecondRight, `$performanceSecondRight, `$featuresSecondRight, `$quickMaxRight, `$mapMaxRight, `$overflowCount
`$compact1380 = [pscustomobject]@{
    Size = '1380x780'
    Left = Get-ButtonLayoutMetrics `$leftOperationButtons
    Quick = Get-ButtonLayoutMetrics `$rightQuickButtons
    Map = Get-ButtonLayoutMetrics `$mapButtons
}
Write-CompactLayoutSnapshot `$compact1380
Write-CompactLayoutSnapshot (Get-CompactLayoutSnapshot 1740 780)
Write-CompactLayoutSnapshot (Get-CompactLayoutSnapshot 1000 700)
if (`$groupHeightFailures.Count -gt 0 -or `$leftOverlap.Count -gt 0 -or `$rightOverlap.Count -gt 0) {
    Write-Output 'FAIL: GroupBox height or column overlap contract failed'
    Write-Output ('GROUP_HEIGHTS=' + (`$groupHeightDetails -join '|'))
    Write-Output ('OVERLAP=Left=' + `$leftOverlap.Count + ';Right=' + `$rightOverlap.Count)
    exit 1
}
if (`$leftQuickNames.Count -gt 0 -or `$rightQuickNames.Count -ne 3 -or (`$rightQuickNames -join ',') -ne 'BotQuickPauseButton,BotQuickRecallButton,BotQuickSyncButton' -or `$syncVisibleButtons.Count -ne 1) {
    Write-Output 'FAIL: Quick control placement or sync button uniqueness contract failed'
    Write-Output ('BUTTON_LOCATIONS=LeftQuick=' + (`$leftQuickNames -join ',') + ';RightQuick=' + (`$rightQuickNames -join ',') + ';SyncVisible=' + `$syncVisibleButtons.Count)
    exit 1
}
if (`$overflowCount -gt 0 -or `$economySecondRight -gt `$panel2Right -or `$performanceSecondRight -gt `$panel2Right -or `$featuresSecondRight -gt `$panel2Right -or `$quickMaxRight -gt `$panel2Right -or `$mapMaxRight -gt `$panel2Right) { throw 'Right column contains a visible control beyond Panel2 right boundary' }
`$quickStatus = Find-ByName `$form 'BotQuickActionStatusLabel'
`$attackPlus = `$quickButtons | Where-Object { `$_.Text -match '^\u653b\u51fb\u6027 \+10$' } | Select-Object -First 1
if (`$null -eq `$quickStatus -or `$null -eq `$attackPlus) { throw 'Quick tuning status or attack button not found' }
`$attackPlus.PerformClick()
'QUICK_STATUS={0}' -f `$quickStatus.Text
`$form.Close()
`$form.Dispose()
if (Test-Path -LiteralPath `$tempLogDirectory) { Remove-Item -LiteralPath `$tempLogDirectory -Recurse -Force }
"@
$windowsPowerShell = Join-Path $env:WINDIR 'System32\WindowsPowerShell\v1.0\powershell.exe'
$reflectionOutput = & $windowsPowerShell -NoProfile -STA -ExecutionPolicy Bypass -Command $reflectionScript 2>&1
$reflectionExitCode = $LASTEXITCODE
$script:Assertions++
if ($reflectionExitCode -ne 0) {
    $reflectionOutput | Where-Object { $_ -match '^(GROUP_HEIGHTS|OVERLAP|BUTTON_LOCATIONS)=' } | ForEach-Object { Write-Host $_ }
    throw "FAIL: layout reflection process failed`n$reflectionOutput"
}
$compactLines = @($reflectionOutput | Where-Object { [string]$_ -match '^COMPACT_BUTTONS=' } | ForEach-Object { [string]$_ })
$widthLines = @($reflectionOutput | Where-Object { [string]$_ -match '^BUTTON_WIDTHS=' } | ForEach-Object { [string]$_ })
$stateLines = @($reflectionOutput | Where-Object { [string]$_ -match '^BUTTON_STATE=' } | ForEach-Object { [string]$_ })
$detailsLines = @($reflectionOutput | Where-Object { [string]$_ -match '^BUTTON_DETAILS=' } | ForEach-Object { [string]$_ })
$centeringLines = @($reflectionOutput | Where-Object { [string]$_ -match '^CENTERING=' } | ForEach-Object { [string]$_ })
$buttonOverflowLines = @($reflectionOutput | Where-Object { [string]$_ -match '^BUTTON_OVERFLOW=' } | ForEach-Object { [string]$_ })
$script:Assertions++
if ($compactLines.Count -ne 3 -or $widthLines.Count -ne 3 -or $stateLines.Count -ne 3 -or $detailsLines.Count -ne 3 -or $centeringLines.Count -ne 3 -or $buttonOverflowLines.Count -ne 3) {
    throw "FAIL: compact layout reflection did not return all three size snapshots`n$reflectionOutput"
}
foreach ($size in @('1380x780', '1740x780', '1000x700')) {
    $compactLine = $compactLines | Where-Object { $_ -match ('^COMPACT_BUTTONS=Size={0};' -f [regex]::Escape($size)) } | Select-Object -First 1
    $widthLine = $widthLines | Where-Object { $_ -match ('^BUTTON_WIDTHS=Size={0};' -f [regex]::Escape($size)) } | Select-Object -First 1
    $stateLine = $stateLines | Where-Object { $_ -match ('^BUTTON_STATE=Size={0};' -f [regex]::Escape($size)) } | Select-Object -First 1
    $detailsLine = $detailsLines | Where-Object { $_ -match ('^BUTTON_DETAILS=Size={0};' -f [regex]::Escape($size)) } | Select-Object -First 1
    $centeringLine = $centeringLines | Where-Object { $_ -match ('^CENTERING=Size={0};' -f [regex]::Escape($size)) } | Select-Object -First 1
    $buttonOverflowLine = $buttonOverflowLines | Where-Object { $_ -match ('^BUTTON_OVERFLOW=Size={0};' -f [regex]::Escape($size)) } | Select-Object -First 1
    Write-Host $compactLine
    Write-Host $widthLine
    Write-Host $stateLine
    Write-Host $detailsLine
    Write-Host $centeringLine
    Write-Host $buttonOverflowLine
    $script:Assertions++
    if ([string]::IsNullOrWhiteSpace([string]$compactLine) -or [string]::IsNullOrWhiteSpace([string]$widthLine) -or [string]::IsNullOrWhiteSpace([string]$stateLine) -or [string]::IsNullOrWhiteSpace([string]$detailsLine) -or [string]::IsNullOrWhiteSpace([string]$centeringLine) -or [string]::IsNullOrWhiteSpace([string]$buttonOverflowLine)) {
        throw "FAIL: compact layout snapshot missing for $size`n$reflectionOutput"
    }
    $compactMatch = [regex]::Match([string]$compactLine, '^COMPACT_BUTTONS=Size=(?<size>[^;]+);LeftMax=(?<left>\d+);QuickMax=(?<quick>\d+);MapMax=(?<map>\d+);')
    $script:Assertions++
    if (!$compactMatch.Success -or [int]$compactMatch.Groups['left'].Value -gt 180 -or [int]$compactMatch.Groups['quick'].Value -gt 220 -or [int]$compactMatch.Groups['map'].Value -gt 150) {
        throw "FAIL: compact button maximum-width contract failed for $size`n$reflectionOutput"
    }
    $stateMatch = [regex]::Match([string]$stateLine, '^BUTTON_STATE=Size=[^;]+;LeftMinHeight=(?<leftHeight>\d+);QuickMinHeight=(?<quickHeight>\d+);MapMinHeight=(?<mapHeight>\d+);LeftVisible=(?<leftVisible>True|False);QuickVisible=(?<quickVisible>True|False);MapVisible=(?<mapVisible>True|False)$')
    $script:Assertions++
    if (!$stateMatch.Success -or [int]$stateMatch.Groups['leftHeight'].Value -le 0 -or [int]$stateMatch.Groups['quickHeight'].Value -le 0 -or [int]$stateMatch.Groups['mapHeight'].Value -le 0 -or $stateMatch.Groups['leftVisible'].Value -ne 'True' -or $stateMatch.Groups['quickVisible'].Value -ne 'True' -or $stateMatch.Groups['mapVisible'].Value -ne 'True') {
        throw "FAIL: compact button height/visibility contract failed for $size`n$reflectionOutput"
    }
    $centeringMatch = [regex]::Match([string]$centeringLine, '^CENTERING=Size=[^;]+;Left=(?<left>True|False);Quick=(?<quick>True|False);Map=(?<map>True|False)$')
    $script:Assertions++
    if (!$centeringMatch.Success -or $centeringMatch.Groups['left'].Value -ne 'True' -or $centeringMatch.Groups['quick'].Value -ne 'True' -or $centeringMatch.Groups['map'].Value -ne 'True') {
        throw "FAIL: compact button centering contract failed for $size`n$reflectionOutput"
    }
    $overflowMatch = [regex]::Match([string]$buttonOverflowLine, '^BUTTON_OVERFLOW=Size=[^;]+;Count=(?<count>\d+)$')
    $script:Assertions++
    if (!$overflowMatch.Success -or [int]$overflowMatch.Groups['count'].Value -ne 0) {
        throw "FAIL: compact button row overflow contract failed for $size`n$reflectionOutput"
    }
    if ($size -eq '1000x700') {
        $widthMatch = [regex]::Match([string]$widthLine, '^BUTTON_WIDTHS=Size=[^;]+;LeftMin=(?<left>\d+);QuickMin=(?<quick>\d+);MapMin=(?<map>\d+)$')
        $script:Assertions++
        if (!$widthMatch.Success -or ([int]$widthMatch.Groups['left'].Value -ge 180 -and [int]$widthMatch.Groups['quick'].Value -ge 220 -and [int]$widthMatch.Groups['map'].Value -ge 150)) {
            throw "FAIL: narrow compact button rows did not shrink below their maximum widths`n$reflectionOutput"
        }
    }
}
$layoutLine = $reflectionOutput | Where-Object { $_ -match '^P1=\d+;P2=\d+;Form=\d+x\d+$' } | Select-Object -Last 1
$layoutMatch = [regex]::Match([string]$layoutLine, '^P1=(\d+);P2=(\d+);Form=(\d+)x(\d+)$')
$script:Assertions++
if (!$layoutMatch.Success) { throw "FAIL: layout reflection did not return panel widths`n$reflectionOutput" }
$panel1Width = [int]$layoutMatch.Groups[1].Value
$panel2Width = [int]$layoutMatch.Groups[2].Value
$script:Assertions++
if ($panel1Width -lt 790 -or $panel1Width -gt 810) { throw "FAIL: expected Panel1 width 790-810, got $panel1Width" }
$script:Assertions++
if ($panel2Width -lt 520) { throw "FAIL: expected Panel2 width >=520, got $panel2Width" }
$script:Assertions++
if ([int]$layoutMatch.Groups[3].Value -ne 1380 -or [int]$layoutMatch.Groups[4].Value -ne 780) { throw 'FAIL: reflection form size is not 1380x780' }
$autoLine = $reflectionOutput | Where-Object { $_ -match '^AUTO=' } | Select-Object -Last 1
$autoMatch = [regex]::Match([string]$autoLine, '^AUTO=(\d+),(\d+);(\d+),(\d+)$')
$script:Assertions++
if (!$autoMatch.Success -or $autoMatch.Groups[2].Value -ne $autoMatch.Groups[4].Value -or $autoMatch.Groups[1].Value -eq $autoMatch.Groups[3].Value) { throw "FAIL: automatic behavior controls are not on the same row in different columns`n$reflectionOutput" }
$economyLine = $reflectionOutput | Where-Object { $_ -match '^ECONOMY=' } | Select-Object -Last 1
$economyMatch = [regex]::Match([string]$economyLine, '^ECONOMY=(\d+),(\d+);(\d+),(\d+)$')
$script:Assertions++
if (!$economyMatch.Success -or $economyMatch.Groups[2].Value -ne $economyMatch.Groups[4].Value -or $economyMatch.Groups[1].Value -eq $economyMatch.Groups[3].Value) { throw "FAIL: economy controls are not on the same row in different columns`n$reflectionOutput" }
$quickLine = $reflectionOutput | Where-Object { $_ -match '^QUICK=' } | Select-Object -Last 1
$script:Assertions++
if ([string]$quickLine -notmatch '^QUICK=6;ROWS=3;COUNTS=2,2,2$') { throw "FAIL: quick actions are not a 2x3 grid`n$reflectionOutput" }
$mapLine = $reflectionOutput | Where-Object { $_ -match '^MAPS=' } | Select-Object -Last 1
$script:Assertions++
if ([string]$mapLine -notmatch '^MAPS=8;ROWS=2;COUNTS=4,4$') { throw "FAIL: map ranges are not a 4x2 grid`n$reflectionOutput" }
$rightBoundsLine = $reflectionOutput | Where-Object { $_ -match '^RIGHT_BOUNDS=' } | Select-Object -Last 1
$script:Assertions++
if ([string]::IsNullOrWhiteSpace([string]$rightBoundsLine)) { throw "FAIL: reflection did not return RIGHT_BOUNDS evidence`n$reflectionOutput" }
Write-Host $rightBoundsLine
foreach ($evidencePattern in @('^GROUP_HEIGHTS=', '^OVERLAP=', '^BUTTON_LOCATIONS=')) {
    $evidenceLine = $reflectionOutput | Where-Object { $_ -match $evidencePattern } | Select-Object -Last 1
    $script:Assertions++
    if ([string]::IsNullOrWhiteSpace([string]$evidenceLine)) { throw "FAIL: reflection did not return $evidencePattern evidence`n$reflectionOutput" }
    Write-Host $evidenceLine
}
$quickStatusLine = $reflectionOutput | Where-Object { $_ -match '^QUICK_STATUS=' } | Select-Object -Last 1
$script:Assertions++
if ([string]$quickStatusLine -notmatch '^QUICK_STATUS=\u5f53\u524d\u6ca1\u6709\u5728\u7ebf\u5047\u4eba\uff0c\u5feb\u6377\u8c03\u6574\u672a\u6267\u884c$') { throw "FAIL: no-online quick tuning status is not nonblocking and explicit`n$reflectionOutput" }

foreach ($label in @(
    '\u81ea\u52a8\u7279\u4fee\u88c5\u5907','\u6309\u6bd4\u4f8b\u6bcf\u79d2\u7ed9\u5047\u4eba\u56de\u8840\u84dd',
    '\u6309\u6570\u503c\u6bcf\u79d2\u7ed9\u5047\u4eba\u56de\u8840\u84dd','\u589e\u52a0\u53cc\u9632',
    '\u968f\u673a\u589e\u52a0\u51e0\u79cd\u5f3a\u5143\u7d20','\u67e5\u770b\u5956\u52b1\u6f0f\u53d1',
    '\u8986\u76d6\u5730\u56fe','\u65b0\u589e\u529f\u80fd\u914d\u7f6e','\u5730\u56fe\u6c60\u52a0\u6210',
    '\u5207\u56fe\u5206\u5dee\u4e0a\u9650','\u4e3bAI\u6bcf\u5e27\u4e0a\u9650','\u836f\u6c34\u6bcf\u5e27\u4e0a\u9650',
    '\u5468\u671f\u7ec4\u961f\uff08\u79d2\uff09','\u8fbe\u5230','\u7ea7\u4ee5\u4e0a\u4e0e\u73a9\u5bb6PK',
    '\u81ea\u52a8\u8f6c\u751f','\u542f\u52a8\u5047\u4eba','\u505c\u6b62\u5047\u4eba',
    '\u6240\u6709\u5047\u4eba\u56de\u57ce','\u6682\u505c','\u7ee7\u7eed','\u4fdd\u5b58\u914d\u7f6e',
    '\u5237\u65b0','\u5b9e\u65f6\u6d3b\u52a8\u65e5\u5fd7','\u64cd\u4f5c\u65e5\u5fd7'
)) {
    Assert-Contains $ui $label "visible label $label exists"
}
Assert-Contains $ui 'Panel|TableLayoutPanel|SplitContainer|\u5de6\u680f|\u53f3\u680f|TwoColumn|Column' 'UI creates a two-column layout'
Assert-Contains $ui 'TrackBar|TrackBarControl' 'behavior strengths use sliders'
Assert-Contains $ui 'Minimum\s*=\s*0|EditValue.*0' 'sliders have zero lower bound'
Assert-Contains $ui 'Maximum\s*=\s*100|EditValue.*100' 'sliders have 100 upper bound'
Assert-Contains $ui 'AggressionPercent[^\r\n]*50|Value\s*=\s*50' 'behavior strength defaults include 50'
Assert-Contains $ui 'NumericUpDown|SpinEdit|CalcEdit' 'numeric controls support arrows'
Assert-Contains $ui 'BotInitialGoldFloor|BotGoldFarmThreshold|BotMinHealthPotionCount|BotMinManaPotionCount' 'economic values are bound'
Assert-Contains $ui 'BotMainLoopIntervalMs|BotPotionMonitorIntervalMs|BotMainActionsPerFrame|BotPotionActionsPerFrame' 'performance values are bound'
Assert-Contains $ui 'BotAttackAttemptIntervalMs|BotPickupAttemptIntervalMs|BotPickupRadius|BotMapPoolBonus|BotMapSwitchScoreGapMax|BotPeriodicGroupSeconds' 'new feature values are bound'
Assert-Contains $ui 'Timer' 'UI has a refresh timer'
Assert-Contains $ui 'Interval\s*=\s*1000|new Timer\(1000\)' 'UI refresh timer is one second'
Assert-Contains $ui 'LoadBotSettings|FromConfig' 'UI loads detached settings from Config'
Assert-Contains $ui 'TryReadFormSettings' 'UI reads a detached form model'
Assert-Contains $ui 'TryApplyManagementSettings' 'UI uses atomic manager apply'
Assert-Contains $ui 'CheckedChanged|PercentRecovery|FixedRecovery' 'recovery checkboxes are mutually handled'
Assert-Contains $ui 'MessageBoxButtons\.YesNo|XtraMessageBox.*YesNo' 'dangerous actions require confirmation'
Assert-Contains $ui 'GetManagementSnapshot|SyncOnlineBots|BackfillMissingBotRewards|GetMissingBotRewardReport' 'buttons call real manager APIs'
Assert-Contains $ui 'Dispose|OnFormClosed|FormClosed' 'UI cleanup hook exists'
Assert-Contains $ui 'Stop\(\)|Enabled\s*=\s*false' 'UI timer is stopped during cleanup'
Assert-Contains $main 'ShowView\(typeof\(BotConfigView\)\)' 'existing MDI entry remains'

Write-Host "RESULT: PASS ($script:Assertions assertions)"
