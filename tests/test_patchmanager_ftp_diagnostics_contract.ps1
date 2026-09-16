$ErrorActionPreference = 'Stop'

function Assert-Contract {
    param(
        [bool]$Condition,
        [string]$Message
    )

    if (-not $Condition) {
        throw "CONTRACT FAILURE: $Message"
    }
}

function Get-PrivateMethod {
    param(
        [Type]$Type,
        [string]$Name,
        [int]$ParameterCount
    )

    $method = @($Type.GetMethods([System.Reflection.BindingFlags]::Instance -bor [System.Reflection.BindingFlags]::Static -bor [System.Reflection.BindingFlags]::Public -bor [System.Reflection.BindingFlags]::NonPublic) |
        Where-Object { $_.Name -eq $Name -and $_.GetParameters().Count -eq $ParameterCount }) | Select-Object -First 1

    Assert-Contract ($null -ne $method) "missing method $Name with $ParameterCount parameters"
    return $method
}

function Get-InternalPropertyValue {
    param(
        [object]$Instance,
        [string]$Name
    )

    $property = $Instance.GetType().GetProperty($Name, [System.Reflection.BindingFlags]::Instance -bor [System.Reflection.BindingFlags]::Static -bor [System.Reflection.BindingFlags]::Public -bor [System.Reflection.BindingFlags]::NonPublic)
    Assert-Contract ($null -ne $property) "missing property $Name on $($Instance.GetType().FullName)"
    return $property.GetValue($Instance, $null)
}

function Get-InternalStaticPropertyValue {
    param(
        [Type]$Type,
        [string]$Name
    )

    $property = $Type.GetProperty($Name, [System.Reflection.BindingFlags]::Static -bor [System.Reflection.BindingFlags]::Public -bor [System.Reflection.BindingFlags]::NonPublic)
    Assert-Contract ($null -ne $property) "missing static property $Name on $($Type.FullName)"
    return $property.GetValue($null, $null)
}

function Set-StaticPropertyValue {
    param(
        [Type]$Type,
        [string]$Name,
        [object]$Value
    )

    $property = $Type.GetProperty($Name, [System.Reflection.BindingFlags]::Static -bor [System.Reflection.BindingFlags]::Public -bor [System.Reflection.BindingFlags]::NonPublic)
    Assert-Contract ($null -ne $property) "missing static property $Name on $($Type.FullName)"
    $property.SetValue($null, $Value, $null)
}

function Find-Control {
    param(
        [System.Windows.Forms.Control]$Root,
        [string]$Name
    )

    foreach ($control in $Root.Controls) {
        if ($control.Name -eq $Name) {
            return $control
        }

        $nested = Find-Control -Root $control -Name $Name
        if ($null -ne $nested) {
            return $nested
        }
    }

    return $null
}

function Get-ControlVisibleState {
    param(
        [System.Windows.Forms.Control]$Control
    )

    $getState = [System.Windows.Forms.Control].GetMethod('GetState', [System.Reflection.BindingFlags]::Instance -bor [System.Reflection.BindingFlags]::NonPublic)
    Assert-Contract ($null -ne $getState) 'cannot inspect WinForms visible state'
    return [bool]$getState.Invoke($Control, [object[]]@(2))
}

function Test-MethodReferencesToken {
    param(
        [System.Reflection.MethodBase]$Method,
        [int]$MetadataToken
    )

    $methods = @($Method)
    $asyncAttribute = @($Method.GetCustomAttributes($false) |
        Where-Object { $_ -is [System.Runtime.CompilerServices.AsyncStateMachineAttribute] }) | Select-Object -First 1
    if ($null -ne $asyncAttribute) {
        $moveNext = $asyncAttribute.StateMachineType.GetMethod('MoveNext', [System.Reflection.BindingFlags]::Instance -bor [System.Reflection.BindingFlags]::NonPublic)
        if ($null -ne $moveNext) {
            $methods += $moveNext
        }
    }

    foreach ($candidate in $methods) {
        $body = $candidate.GetMethodBody()
        if ($null -eq $body) {
            continue
        }

        $bytes = $body.GetILAsByteArray()
        for ($index = 0; $index -le $bytes.Length - 4; $index++) {
            if ([BitConverter]::ToInt32($bytes, $index) -eq $MetadataToken) {
                return $true
            }
        }
    }

    return $false
}

function Get-ClickHandlerNames {
    param(
        [System.Windows.Forms.Control]$Control
    )

    $controlType = $Control.GetType()
    $eventClickField = $null
    while ($null -ne $controlType -and $null -eq $eventClickField) {
        $eventClickField = $controlType.GetField('EventClick', [System.Reflection.BindingFlags]::Static -bor [System.Reflection.BindingFlags]::NonPublic)
        $controlType = $controlType.BaseType
    }

    Assert-Contract ($null -ne $eventClickField) "cannot inspect Click event key for $($Control.Name)"
    $eventKey = $eventClickField.GetValue($null)
    $eventsProperty = [System.ComponentModel.Component].GetProperty('Events', [System.Reflection.BindingFlags]::Instance -bor [System.Reflection.BindingFlags]::NonPublic)
    Assert-Contract ($null -ne $eventsProperty) 'cannot inspect WinForms event list'
    $handler = $eventsProperty.GetValue($Control, $null)[$eventKey]
    if ($null -eq $handler) {
        return @()
    }

    return @($handler.GetInvocationList() | ForEach-Object { $_.Method.Name })
}

function Close-TestMessageBoxes {
    [ContractWindowCloser]::CloseCurrentProcessWindows()
}

Add-Type @'
using System;
using System.Reflection;
using System.Threading;

public sealed class ContractInvocation
{
    private readonly Thread thread;
    private object value;
    private Exception error;

    internal ContractInvocation(MethodInfo method, object target, object[] arguments, int timeoutMilliseconds)
    {
        thread = new Thread(() =>
        {
            try
            {
                value = method.Invoke(target, arguments);
            }
            catch (Exception exception)
            {
                error = exception;
            }
        });
        thread.IsBackground = true;
        thread.Start();
    }

    public bool IsCompleted { get { return !thread.IsAlive; } }
    public object Value { get { return value; } }
    public Exception Error { get { return error; } }

    public bool Wait(int timeoutMilliseconds)
    {
        return thread.Join(timeoutMilliseconds);
    }
}

public static class ContractReflectionRunner
{
    public static ContractInvocation Start(MethodInfo method, object target, object[] arguments, int timeoutMilliseconds)
    {
        return new ContractInvocation(method, target, arguments, timeoutMilliseconds);
    }
}
'@

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$projectPath = Join-Path $repoRoot 'PatchManager\PatchManager.csproj'
$msbuildPath = 'C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\MSBuild\Current\Bin\MSBuild.exe'
Assert-Contract (Test-Path -LiteralPath $msbuildPath) "MSBuild not found at $msbuildPath"

$caseRoot = Join-Path ([System.IO.Path]::GetTempPath()) ('PatchManager-ftp-contract-' + [Guid]::NewGuid().ToString('N'))
$outputRoot = Join-Path $caseRoot 'out'
$intermediateRoot = Join-Path $caseRoot 'obj'
$intermediateOutput = Join-Path $intermediateRoot 'Release'
$patchRoot = Join-Path $caseRoot 'Patch'
$failedPatchPath = Join-Path $patchRoot 'contract.bin.gz'
$logPath = Join-Path $outputRoot 'PatchManager.log'
$sentinelPassword = 'SECRET-PASSWORD-MUST-NOT-APPEAR'
$failureUri = 'http://127.0.0.1:1/'

New-Item -ItemType Directory -Path $patchRoot -Force | Out-Null
New-Item -ItemType Directory -Path $outputRoot -Force | Out-Null
New-Item -ItemType Directory -Path $intermediateOutput -Force | Out-Null
[System.IO.File]::WriteAllBytes($failedPatchPath, [byte[]](0x50, 0x41, 0x54, 0x43, 0x48, 0x2D, 0x52, 0x45, 0x44))

try {
    $buildArguments = @(
        $projectPath,
        '/t:Rebuild',
        '/p:Configuration=Release',
        '/p:Platform=AnyCPU',
        ('/p:OutputPath=' + $outputRoot + '\'),
        ('/p:BaseIntermediateOutputPath=' + $intermediateRoot + '\'),
        ('/p:IntermediateOutputPath=' + $intermediateOutput + '\'),
        '/nologo',
        '/verbosity:minimal'
    )
    & $msbuildPath @buildArguments
    if ($LASTEXITCODE -ne 0) {
        throw "CONTRACT SETUP FAILURE: isolated build exited $LASTEXITCODE"
    }

    $assemblyPath = Join-Path $outputRoot 'PatchManager.exe'
    Assert-Contract (Test-Path -LiteralPath $assemblyPath) "isolated assembly missing at $assemblyPath"
    $assembly = [System.Reflection.Assembly]::LoadFrom($assemblyPath)
    $pMainType = $assembly.GetType('PatchManager.PMain', $true)
    $configType = $assembly.GetType('PatchManager.Config', $true)
    $patchInfoType = $assembly.GetType('PatchManager.PatchInformation', $true)
    Assert-Contract ($null -ne $pMainType) 'PatchManager.PMain type missing'
    Assert-Contract ($null -ne $configType) 'PatchManager.Config type missing'
    Assert-Contract ($null -ne $patchInfoType) 'PatchManager.PatchInformation type missing'

    $form = [Activator]::CreateInstance($pMainType)
    $expectedWindowTitle = -join ([char[]](0x8865, 0x4E01, 0x7BA1, 0x7406, 0x5668))
    $actualWindowTitle = [string]$form.Text
    if ($actualWindowTitle -ne $expectedWindowTitle) {
        Write-Output ('RED exact symptom reproduced: PMain title is ' + $actualWindowTitle)
    }
    Assert-Contract ($actualWindowTitle -eq $expectedWindowTitle) ('unexpected PMain title: ' + $actualWindowTitle)
    Write-Output ('PASS: PMain title is exactly ' + $expectedWindowTitle)
    [System.Net.WebRequest]::DefaultWebProxy = $null
    Set-StaticPropertyValue -Type $configType -Name 'PcFtpHost' -Value $failureUri
    Set-StaticPropertyValue -Type $configType -Name 'PcFtpUseLogin' -Value $true
    Set-StaticPropertyValue -Type $configType -Name 'PcUsername' -Value 'contract-user'
    Set-StaticPropertyValue -Type $configType -Name 'PcPassword' -Value $sentinelPassword

    $patchInfo = [Activator]::CreateInstance($patchInfoType)
    $patchInfoType.GetProperty('FileName').SetValue($patchInfo, 'contract.bin', $null)
    $patchInfoType.GetProperty('FullFileName').SetValue($patchInfo, $failedPatchPath, $null)
    $patchInfoType.GetProperty('CompressedLength').SetValue($patchInfo, [long]9, $null)

    $progressType = [System.Progress[string]]
    $progress = [Activator]::CreateInstance($progressType)
    $previousDirectory = [Environment]::CurrentDirectory
    Push-Location $caseRoot
    try {
        [Environment]::CurrentDirectory = $caseRoot
        $uploadMethod = Get-PrivateMethod -Type $pMainType -Name 'Upload' -ParameterCount 3
        $uploadArguments = [object[]]@($patchInfo, $progress, $false)
        $uploadInvocation = [ContractReflectionRunner]::Start($uploadMethod, $form, $uploadArguments, 10000)
        $uploadDeadline = [DateTime]::UtcNow.AddSeconds(10)
        while (-not $uploadInvocation.IsCompleted -and [DateTime]::UtcNow -lt $uploadDeadline) {
            Start-Sleep -Milliseconds 50
        }
        Assert-Contract $uploadInvocation.IsCompleted 'Upload did not finish on the refused URI'
        $uploadOutcome = $uploadInvocation.Value
        $uploadException = $uploadInvocation.Error
        $uploadResult = if ($null -eq $uploadException) { [bool]$uploadOutcome } else { $false }

        if ($uploadResult -and -not (Test-Path -LiteralPath $failedPatchPath)) {
            Write-Output "RED exact symptom reproduced: failed Upload returned true and deleted $failedPatchPath"

            $listType = [System.Collections.Generic.List``1].MakeGenericType(@($patchInfoType))
            $versionList = [Activator]::CreateInstance($listType)
            $saveMethod = @($pMainType.GetMethods([System.Reflection.BindingFlags]::Instance -bor [System.Reflection.BindingFlags]::NonPublic) |
                Where-Object { $_.Name -eq 'SaveVersion' }) | Select-Object -First 1
            Assert-Contract ($null -ne $saveMethod) 'current SaveVersion method missing during RED'
            $saveArguments = if ($saveMethod.GetParameters().Count -eq 2) {
                [object[]]@($versionList, $false)
            }
            else {
                [object[]]@($versionList, $progress, $false)
            }

            try {
                $saveResult = $saveMethod.Invoke($form, $saveArguments)
                Write-Output 'RED companion evidence: SaveVersion did not throw on the refused URI'
            }
            catch {
                Write-Output "RED companion evidence: SaveVersion propagated $($_.Exception.GetType().FullName) on the refused URI"
            }

            exit 1
        }

        Assert-Contract ($null -eq $uploadException) 'Upload threw before returning a result'
        Assert-Contract (-not $uploadResult) 'failed Upload must return false after implementation'
        Assert-Contract (Test-Path -LiteralPath $failedPatchPath) 'failed local temporary patch must survive after implementation'
        $errorField = $pMainType.GetField('Error', [System.Reflection.BindingFlags]::Instance -bor [System.Reflection.BindingFlags]::Public)
        Assert-Contract ($null -ne $errorField -and [bool]$errorField.GetValue($form)) 'failed Upload did not set Error'
        Write-Output 'PASS: failed Upload returned false and preserved the local temporary patch'

        $diagnosticsType = $assembly.GetType('PatchManager.FtpDiagnostics', $true)
        $probeType = $assembly.GetType('PatchManager.FtpConnectionProbe', $true)
        Assert-Contract ($null -ne $diagnosticsType) 'FtpDiagnostics type missing'
        Assert-Contract ($null -ne $probeType) 'FtpConnectionProbe type missing'

        if (Test-Path -LiteralPath $logPath) {
            Remove-Item -LiteralPath $logPath -Force
        }

        $recordFailure = Get-PrivateMethod -Type $diagnosticsType -Name 'RecordFailure' -ParameterCount 5
        $webException = [System.Net.WebException]::new(('refused ' + $sentinelPassword), [System.Net.WebExceptionStatus]::ConnectFailure)
        $failureTarget = [Uri]('ftp://contract-user:' + $sentinelPassword + '@127.0.0.1:1/PList.Bin')
        $failureReport = $recordFailure.Invoke($null, [object[]]@('端游', '上传 PList.Bin', $failureTarget, $webException, $sentinelPassword))
        $failureUserMessage = [string](Get-InternalPropertyValue -Instance $failureReport -Name 'UserMessage')
        $failureLogPath = [string](Get-InternalPropertyValue -Instance $failureReport -Name 'LogPath')
        Assert-Contract ($failureUserMessage.Contains('端游')) 'failure summary missing mode'
        Assert-Contract ($failureUserMessage.Contains('上传 PList.Bin')) 'failure summary missing stage'
        Assert-Contract ($failureUserMessage.Contains('ConnectFailure')) 'failure summary missing WebExceptionStatus'
        Assert-Contract ($failureUserMessage.Contains($failureLogPath)) 'failure summary missing log path'
        Assert-Contract (-not $failureUserMessage.Contains($sentinelPassword)) 'failure summary leaked the password sentinel'
        Assert-Contract (Test-Path -LiteralPath $failureLogPath) 'diagnostic log was not created'
        $failureLog = Get-Content -Raw -Encoding UTF8 -LiteralPath $failureLogPath
        Assert-Contract (-not $failureLog.Contains($sentinelPassword)) 'diagnostic log leaked the password sentinel'
        Write-Output 'PASS: failure summary and UTF-8 log include mode/stage/Web status without the password sentinel'

        $recordConnectionStep = Get-PrivateMethod -Type $diagnosticsType -Name 'RecordConnectionStep' -ParameterCount 5
        $stepMode = 'connection-step-mode'
        $stepStage = 'connection-step-stage'
        $stepFileName = 'step-test.tmp'
        $stepDetail = 'step-detail'
        $stepTarget = [Uri]('ftp://step-user:' + $sentinelPassword + '@probe.example/' + $stepFileName)
        $stepException = $null
        try {
            $recordConnectionStep.Invoke($null, [object[]]@($stepMode, $stepStage, $stepTarget, $stepDetail, $sentinelPassword)) | Out-Null
        }
        catch {
            $stepException = $_.Exception
        }
        if ($null -ne $stepException) {
            $rootStepException = $stepException
            while ($null -ne $rootStepException.InnerException) {
                $rootStepException = $rootStepException.InnerException
            }
            $rootStepType = $rootStepException.GetType().FullName
            if ($rootStepType -like '*FormatException') {
                Write-Output "RED exact symptom reproduced: RecordConnectionStep threw $rootStepType before logging"
                throw "CONTRACT FAILURE: RecordConnectionStep threw $rootStepType"
            }
            throw "CONTRACT SETUP FAILURE: RecordConnectionStep threw $rootStepType"
        }
        $stepLog = Get-Content -Raw -Encoding UTF8 -LiteralPath $failureLogPath
        Assert-Contract $stepLog.Contains($stepMode) 'connection-step log missing mode'
        Assert-Contract $stepLog.Contains($stepStage) 'connection-step log missing stage'
        Assert-Contract $stepLog.Contains($stepFileName) 'connection-step log missing test file name'
        Assert-Contract $stepLog.Contains('Result=') 'connection-step log missing Result'
        Assert-Contract (-not $stepLog.Contains($sentinelPassword)) 'connection-step log leaked the password sentinel'
        Write-Output 'PASS: RecordConnectionStep writes step details without the password sentinel'

        $createRemoteFileName = Get-PrivateMethod -Type $probeType -Name 'CreateRemoteFileName' -ParameterCount 0
        $remoteFileName1 = [string]$createRemoteFileName.Invoke($null, [object[]]@())
        $remoteFileName2 = [string]$createRemoteFileName.Invoke($null, [object[]]@())
        Assert-Contract ($remoteFileName1 -ne $remoteFileName2) 'connection test names were not unique'
        Assert-Contract ($remoteFileName1 -match '^\.patchmanager-test-[0-9a-fA-F]+\.tmp$') "invalid first connection test name: $remoteFileName1"
        Assert-Contract ($remoteFileName2 -match '^\.patchmanager-test-[0-9a-fA-F]+\.tmp$') "invalid second connection test name: $remoteFileName2"

        $executeProbe = Get-PrivateMethod -Type $probeType -Name 'Execute' -ParameterCount 5
        $expectedBytes = [byte[]](0x10, 0x20, 0x30, 0x40)
        $successCalls = New-Object 'System.Collections.Generic.List[string]'
        $uploadAction = [Action[Uri, byte[]]]{
            param([Uri]$Target, [byte[]]$Bytes)
            $successCalls.Add('Upload')
        }
        $downloadFunc = [Func[Uri, byte[]]]{
            param([Uri]$Target)
            $successCalls.Add('Download')
            return $expectedBytes
        }
        $deleteAction = [Action[Uri]]{
            param([Uri]$Target)
            $successCalls.Add('Delete')
        }
        $successProbe = $executeProbe.Invoke($null, [object[]]@([Uri]'ftp://probe.example/root/', $expectedBytes, $uploadAction, $downloadFunc, $deleteAction))
        Assert-Contract ([bool](Get-InternalPropertyValue -Instance $successProbe -Name 'Success')) 'successful probe reported failure'
        Assert-Contract (($successCalls -join ',') -eq 'Upload,Download,Delete') "probe order was $($successCalls -join ',')"
        Write-Output 'PASS: successful probe order is Upload, Download, Delete'

        $mismatchCalls = New-Object 'System.Collections.Generic.List[string]'
        $mismatchUpload = [Action[Uri, byte[]]]{
            param([Uri]$Target, [byte[]]$Bytes)
            $mismatchCalls.Add('Upload')
        }
        $mismatchDownload = [Func[Uri, byte[]]]{
            param([Uri]$Target)
            $mismatchCalls.Add('Download')
            return [byte[]](0x10, 0x20, 0x30, 0x41)
        }
        $mismatchDelete = [Action[Uri]]{
            param([Uri]$Target)
            $mismatchCalls.Add('Delete')
        }
        $mismatchProbe = $executeProbe.Invoke($null, [object[]]@([Uri]'ftp://probe.example/root/', $expectedBytes, $mismatchUpload, $mismatchDownload, $mismatchDelete))
        $mismatchStage = [string](Get-InternalPropertyValue -Instance $mismatchProbe -Name 'FailedStage')
        $readbackStage = ([char[]](0x56DE, 0x8BFB, 0x6821, 0x9A8C)) -join ''
        Assert-Contract (-not [bool](Get-InternalPropertyValue -Instance $mismatchProbe -Name 'Success')) 'mismatched probe reported success'
        Assert-Contract ($mismatchStage.Contains($readbackStage)) "mismatch stage was $mismatchStage"
        Assert-Contract (($mismatchCalls -join ',') -eq 'Upload,Download,Delete') "mismatch cleanup order was $($mismatchCalls -join ',')"
        Write-Output 'PASS: mismatched readback failed at the readback-verification stage and still deleted the remote test file'

        $uploadResponseCalls = New-Object 'System.Collections.Generic.List[string]'
        $uploadResponseUpload = [Action[Uri, byte[]]]{
            param([Uri]$Target, [byte[]]$Bytes)
            $uploadResponseCalls.Add('Upload')
            throw [InvalidOperationException]::new('upload completion response failed')
        }
        $uploadResponseDownload = [Func[Uri, byte[]]]{
            param([Uri]$Target)
            $uploadResponseCalls.Add('Download')
            return $expectedBytes
        }
        $uploadResponseDelete = [Action[Uri]]{
            param([Uri]$Target)
            $uploadResponseCalls.Add('Delete')
        }
        $uploadResponseProbe = $executeProbe.Invoke($null, [object[]]@([Uri]'ftp://probe.example/root/', $expectedBytes, $uploadResponseUpload, $uploadResponseDownload, $uploadResponseDelete))
        if (($uploadResponseCalls -join ',') -ne 'Upload,Delete') {
            Write-Output "RED exact symptom reproduced: upload completion-response failure skipped Delete; CALLS=$($uploadResponseCalls -join ',')"
            throw "CONTRACT FAILURE: upload completion-response failure cleanup order was $($uploadResponseCalls -join ',')"
        }
        $uploadResponseError = Get-InternalPropertyValue -Instance $uploadResponseProbe -Name 'Error'
        Assert-Contract (-not [bool](Get-InternalPropertyValue -Instance $uploadResponseProbe -Name 'Success')) 'upload completion-response failure reported success'
        Assert-Contract (-not [bool](Get-InternalPropertyValue -Instance $uploadResponseProbe -Name 'RemoteFileMayRemain')) 'upload failure with successful cleanup reported possible residue'
        Assert-Contract ($uploadResponseError.Message -eq 'upload completion response failed') 'upload completion-response error was not preserved as the primary error'

        $uploadAndDeleteFailureCalls = New-Object 'System.Collections.Generic.List[string]'
        $uploadAndDeleteFailureUpload = [Action[Uri, byte[]]]{
            param([Uri]$Target, [byte[]]$Bytes)
            $uploadAndDeleteFailureCalls.Add('Upload')
            throw [InvalidOperationException]::new('upload completion response failed')
        }
        $uploadAndDeleteFailureDownload = [Func[Uri, byte[]]]{
            param([Uri]$Target)
            $uploadAndDeleteFailureCalls.Add('Download')
            return $expectedBytes
        }
        $uploadAndDeleteFailureDelete = [Action[Uri]]{
            param([Uri]$Target)
            $uploadAndDeleteFailureCalls.Add('Delete')
            throw [InvalidOperationException]::new('delete after upload failure failed')
        }
        $uploadAndDeleteFailureProbe = $executeProbe.Invoke($null, [object[]]@([Uri]'ftp://probe.example/root/', $expectedBytes, $uploadAndDeleteFailureUpload, $uploadAndDeleteFailureDownload, $uploadAndDeleteFailureDelete))
        $uploadAndDeleteFailureError = Get-InternalPropertyValue -Instance $uploadAndDeleteFailureProbe -Name 'Error'
        $uploadAndDeleteFailureRemoteName = [string](Get-InternalPropertyValue -Instance $uploadAndDeleteFailureProbe -Name 'RemoteFileName')
        Assert-Contract (($uploadAndDeleteFailureCalls -join ',') -eq 'Upload,Delete') "upload/delete failure cleanup order was $($uploadAndDeleteFailureCalls -join ',')"
        Assert-Contract (-not [bool](Get-InternalPropertyValue -Instance $uploadAndDeleteFailureProbe -Name 'Success')) 'combined upload/delete failure reported success'
        Assert-Contract ([bool](Get-InternalPropertyValue -Instance $uploadAndDeleteFailureProbe -Name 'RemoteFileMayRemain')) 'combined upload/delete failure did not report possible residue'
        Assert-Contract ($uploadAndDeleteFailureError.ToString().Contains('upload completion response failed')) 'combined error lost the upload failure'
        Assert-Contract ($uploadAndDeleteFailureError.ToString().Contains('delete after upload failure failed')) 'combined error lost the delete failure'
        Assert-Contract ($uploadAndDeleteFailureError.ToString().Contains($uploadAndDeleteFailureRemoteName)) 'combined error did not report the residual remote name'
        Write-Output 'PASS: upload completion-response failures trigger cleanup, preserve the primary error, and report residue when cleanup fails'

        $deleteFailureUpload = [Action[Uri, byte[]]]{
            param([Uri]$Target, [byte[]]$Bytes)
        }
        $deleteFailureDownload = [Func[Uri, byte[]]]{
            param([Uri]$Target)
            return $expectedBytes
        }
        $deleteFailureDelete = [Action[Uri]]{
            param([Uri]$Target)
            throw [InvalidOperationException]::new('delete blocked')
        }
        $deleteFailureProbe = $executeProbe.Invoke($null, [object[]]@([Uri]'ftp://probe.example/root/', $expectedBytes, $deleteFailureUpload, $deleteFailureDownload, $deleteFailureDelete))
        $deleteFailureError = Get-InternalPropertyValue -Instance $deleteFailureProbe -Name 'Error'
        $deleteFailureRemoteName = [string](Get-InternalPropertyValue -Instance $deleteFailureProbe -Name 'RemoteFileName')
        Assert-Contract (-not [bool](Get-InternalPropertyValue -Instance $deleteFailureProbe -Name 'Success')) 'delete failure reported success'
        Assert-Contract ([bool](Get-InternalPropertyValue -Instance $deleteFailureProbe -Name 'RemoteFileMayRemain')) 'delete failure did not report possible remote residue'
        Assert-Contract ($deleteFailureRemoteName -match '^\.patchmanager-test-[0-9a-fA-F]+\.tmp$') 'delete failure did not expose the remote test name'
        Assert-Contract ($deleteFailureError.ToString().Contains($deleteFailureRemoteName)) 'delete failure did not report the residual remote name'
        Write-Output 'PASS: delete failure reports the unique possible remote residual name'

        Add-Type @'
using System;
using System.Diagnostics;
using System.Runtime.InteropServices;
using System.Text;

public static class ContractWindowCloser
{
    private delegate bool EnumWindowsProc(IntPtr handle, IntPtr state);

    [DllImport("user32.dll")]
    private static extern bool EnumWindows(EnumWindowsProc callback, IntPtr state);

    [DllImport("user32.dll")]
    private static extern bool IsWindowVisible(IntPtr handle);

    [DllImport("user32.dll")]
    private static extern uint GetWindowThreadProcessId(IntPtr handle, out uint processId);

    [DllImport("user32.dll", CharSet = CharSet.Unicode)]
    private static extern int GetWindowText(IntPtr handle, StringBuilder text, int capacity);

    [DllImport("user32.dll")]
    private static extern bool PostMessage(IntPtr handle, uint message, IntPtr wParam, IntPtr lParam);

    public static void CloseCurrentProcessWindows()
    {
        uint currentProcessId = (uint)Process.GetCurrentProcess().Id;
        EnumWindows((handle, state) =>
        {
            if (!IsWindowVisible(handle))
                return true;

            uint processId;
            GetWindowThreadProcessId(handle, out processId);
            if (processId == currentProcessId)
                PostMessage(handle, 0x0010, IntPtr.Zero, IntPtr.Zero);

            return true;
        }, IntPtr.Zero);
    }
}
'@

        $listType = [System.Collections.Generic.List``1].MakeGenericType(@($patchInfoType))
        $versionList = [Activator]::CreateInstance($listType)
        $saveMethod = @($pMainType.GetMethods([System.Reflection.BindingFlags]::Instance -bor [System.Reflection.BindingFlags]::NonPublic) |
            Where-Object { $_.Name -eq 'SaveVersion' }) | Select-Object -First 1
        Assert-Contract ($null -ne $saveMethod) 'SaveVersion method missing after implementation'
        $saveArguments = if ($saveMethod.GetParameters().Count -eq 3) {
            [object[]]@($versionList, $progress, $false)
        }
        else {
            throw "SaveVersion has unexpected parameter count $($saveMethod.GetParameters().Count)"
        }

        $saveInvocation = [ContractReflectionRunner]::Start($saveMethod, $form, $saveArguments, 10000)
        $deadline = [DateTime]::UtcNow.AddSeconds(10)
        while (-not $saveInvocation.IsCompleted -and [DateTime]::UtcNow -lt $deadline) {
            Close-TestMessageBoxes
            Start-Sleep -Milliseconds 50
        }
        Close-TestMessageBoxes
        Assert-Contract $saveInvocation.IsCompleted 'SaveVersion did not finish after the refused URI'
        $saveOutcome = $saveInvocation.Value
        Assert-Contract ($null -eq $saveInvocation.Error) 'SaveVersion escaped an exception instead of returning false'
        Assert-Contract (-not [bool]$saveOutcome) 'SaveVersion returned success for a refused URI'
        Assert-Contract ((Get-Content -Raw -Encoding UTF8 -LiteralPath $failureLogPath).Contains('PList.Bin')) 'SaveVersion failure log did not identify PList.Bin'
        Write-Output 'PASS: SaveVersion converted PList.Bin failure into a controlled false result'

        $pcButton = Find-Control -Root $form -Name 'pcTestFtpButton'
        $mobButton = Find-Control -Root $form -Name 'mobTestFtpButton'
        $mobUploadButton = Find-Control -Root $form -Name 'mobUploadPatchButton'
        Assert-Contract ($null -ne $pcButton) 'pcTestFtpButton missing'
        Assert-Contract ($null -ne $mobButton) 'mobTestFtpButton missing'
        Assert-Contract ($null -ne $mobUploadButton) 'mobUploadPatchButton missing'
        $pcButtonText = (([char[]](0x6D4B, 0x8BD5, 0x7AEF, 0x6E38, 0x20)) -join '') + 'FTP'
        $mobButtonText = (([char[]](0x6D4B, 0x8BD5, 0x624B, 0x6E38, 0x20)) -join '') + 'FTP'
        Assert-Contract ($pcButton.Text -eq $pcButtonText) "unexpected pcTestFtpButton text: $($pcButton.Text)"
        Assert-Contract ($mobButton.Text -eq $mobButtonText) "unexpected mobTestFtpButton text: $($mobButton.Text)"
        Assert-Contract ((Get-ClickHandlerNames -Control $pcButton) -contains 'pcTestFtpButton_Click') 'pc test button is not bound to its independent handler'
        Assert-Contract ((Get-ClickHandlerNames -Control $mobButton) -contains 'mobTestFtpButton_Click') 'mob test button is not bound to its independent handler'
        Write-Output 'PASS: both independent FTP test buttons exist with the requested text and handlers'

        $mobileUploadVisibleBeforeLoad = Get-ControlVisibleState -Control $mobUploadButton
        Assert-Contract $mobileUploadVisibleBeforeLoad 'mobUploadPatchButton was not visible before PMain_Load'
        $loadMethod = Get-PrivateMethod -Type $pMainType -Name 'PMain_Load' -ParameterCount 2
        $loadMethod.Invoke($form, [object[]]@($null, [EventArgs]::Empty)) | Out-Null
        $mobileUploadVisible = Get-ControlVisibleState -Control $mobUploadButton
        if (-not $mobileUploadVisible) {
            Write-Output 'RED exact symptom reproduced: Release PMain_Load hides mobUploadPatchButton'
        }
        Assert-Contract $mobileUploadVisible 'Release PMain_Load hid mobUploadPatchButton'
        Assert-Contract (Get-ControlVisibleState -Control $mobButton) 'Release PMain_Load hid mobTestFtpButton'
        Write-Output 'PASS: Release PMain_Load keeps both mobile FTP controls visible'

        $testMethod = Get-PrivateMethod -Type $pMainType -Name 'TestFtpConnectionAsync' -ParameterCount 5
        $parameterNames = @($testMethod.GetParameters() | ForEach-Object { $_.Name })
        Assert-Contract (($parameterNames -join ',') -eq 'mode,host,useLogin,username,password') "unexpected shared test method parameters: $($parameterNames -join ',')"
        $isMobField = $pMainType.GetField('IsMobPath', [System.Reflection.BindingFlags]::Instance -bor [System.Reflection.BindingFlags]::NonPublic)
        Assert-Contract ($null -ne $isMobField) 'IsMobPath field missing while checking configuration isolation'
        Assert-Contract (-not (Test-MethodReferencesToken -Method $testMethod -MetadataToken $isMobField.MetadataToken)) 'shared FTP test method directly reads or writes IsMobPath'

        $pcHandler = Get-PrivateMethod -Type $pMainType -Name 'pcTestFtpButton_Click' -ParameterCount 2
        $mobHandler = Get-PrivateMethod -Type $pMainType -Name 'mobTestFtpButton_Click' -ParameterCount 2
        $pcHostGetterToken = $configType.GetProperty('PcFtpHost').GetGetMethod().MetadataToken
        $pcLoginGetterToken = $configType.GetProperty('PcFtpUseLogin').GetGetMethod().MetadataToken
        $pcUserGetterToken = $configType.GetProperty('PcUsername').GetGetMethod().MetadataToken
        $pcPasswordGetterToken = $configType.GetProperty('PcPassword').GetGetMethod().MetadataToken
        $mobHostGetterToken = $configType.GetProperty('MobFtpHost').GetGetMethod().MetadataToken
        $mobLoginGetterToken = $configType.GetProperty('MobFtpUseLogin').GetGetMethod().MetadataToken
        $mobUserGetterToken = $configType.GetProperty('MobUsername').GetGetMethod().MetadataToken
        $mobPasswordGetterToken = $configType.GetProperty('MobPassword').GetGetMethod().MetadataToken
        foreach ($token in @($pcHostGetterToken, $pcLoginGetterToken, $pcUserGetterToken, $pcPasswordGetterToken)) {
            Assert-Contract (Test-MethodReferencesToken -Method $pcHandler -MetadataToken $token) 'pc test handler did not pass all PC configuration values'
        }
        foreach ($token in @($mobHostGetterToken, $mobLoginGetterToken, $mobUserGetterToken, $mobPasswordGetterToken)) {
            Assert-Contract (Test-MethodReferencesToken -Method $mobHandler -MetadataToken $token) 'mob test handler did not pass all mobile configuration values'
        }
        foreach ($token in @($mobHostGetterToken, $mobLoginGetterToken, $mobUserGetterToken, $mobPasswordGetterToken)) {
            Assert-Contract (-not (Test-MethodReferencesToken -Method $pcHandler -MetadataToken $token)) 'pc test handler mixed in mobile configuration'
        }
        foreach ($token in @($pcHostGetterToken, $pcLoginGetterToken, $pcUserGetterToken, $pcPasswordGetterToken)) {
            Assert-Contract (-not (Test-MethodReferencesToken -Method $mobHandler -MetadataToken $token)) 'mob test handler mixed in PC configuration'
        }
        Write-Output 'PASS: shared test method receives a configuration snapshot and PC/mobile handlers stay isolated'
    }
    finally {
        [Environment]::CurrentDirectory = $previousDirectory
        Pop-Location
    }
}
finally {
    if ($null -ne $form) {
        $form.Dispose()
    }

    if (Test-Path -LiteralPath $patchRoot) {
        Remove-Item -LiteralPath $patchRoot -Recurse -Force -ErrorAction SilentlyContinue
    }

    if (Test-Path -LiteralPath $logPath) {
        Remove-Item -LiteralPath $logPath -Force -ErrorAction SilentlyContinue
    }
}
