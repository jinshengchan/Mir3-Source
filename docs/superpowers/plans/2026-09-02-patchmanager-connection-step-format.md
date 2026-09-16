# PatchManager FTP Connection Step Format Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 修复 FTP 测试在实际网络调用前被步骤日志 `FormatException` 错误中断的问题。

**Architecture:** 保留现有 `FtpDiagnostics.RecordConnectionStep` 接口、格式字符串和 FTP 探测流程，只补齐缺失的格式参数。现有程序集行为契约直接调用该方法，验证日志确实写入且密码脱敏。

**Tech Stack:** C#、.NET Framework 4.8、PowerShell 5.1、MSBuild 2022。

## Global Constraints

- 只修改 `PatchManager/FtpDiagnostics.cs` 和 `tests/test_patchmanager_ftp_diagnostics_contract.ps1`。
- 不修改 FTP 配置、上传/下载/删除逻辑、UI 或服务器。
- 必须先得到由 `RecordConnectionStep` 本身触发的精确 RED。
- 自动化不得连接真实 FTP。
- 构建输出和中间目录必须全部位于唯一 Temp 根目录。
- 非 Git 工作区：不提交、不部署、不重启。

---

## File Structure

- Modify: `PatchManager/FtpDiagnostics.cs` — 补齐 `string.Format` 的第六个参数。
- Modify: `tests/test_patchmanager_ftp_diagnostics_contract.ps1` — 增加无网络步骤日志行为契约。

### Task 1: Prevent connection-step logging from aborting the FTP probe

**Files:**

- Modify: `PatchManager/FtpDiagnostics.cs:84-102`
- Test: `tests/test_patchmanager_ftp_diagnostics_contract.ps1`

**Interfaces:**

- Preserves: `internal static void RecordConnectionStep(string mode, string stage, Uri target, string detail, string password)`。
- Produces: 格式化成功、UTF-8 追加记录、现有密码脱敏行为保持不变。

- [ ] **Step 1: Add the failing behavior contract**

在现有程序集加载和日志路径初始化后，反射调用真实方法：

```powershell
$recordConnectionStep = Get-PrivateMethod -Type $diagnosticsType -Name 'RecordConnectionStep' -ParameterCount 5
try {
    $recordConnectionStep.Invoke($null, [object[]]@(
        '端游',
        '开始上传测试文件',
        [Uri]('ftp://contract-user:' + $sentinelPassword + '@probe.example/.patchmanager-test-contract.tmp'),
        '开始',
        $sentinelPassword)) | Out-Null
}
catch {
    $actualError = if ($null -ne $_.Exception.InnerException) { $_.Exception.InnerException } else { $_.Exception }
    if ($actualError -is [FormatException]) {
        Write-Output 'RED exact symptom reproduced: RecordConnectionStep threw FormatException before FTP'
    }
    throw
}
```

若调用成功，读取日志并断言包含 `Mode=端游`、`Stage=开始上传测试文件`、测试文件名和 `Result=开始`，且不包含 `$sentinelPassword`。

- [ ] **Step 2: Run RED**

Run:

```powershell
powershell.exe -STA -NoProfile -ExecutionPolicy Bypass -File .\tests\test_patchmanager_ftp_diagnostics_contract.ps1
```

Expected: exit nonzero，并精确打印 `RED exact symptom reproduced: RecordConnectionStep threw FormatException before FTP`。生产源码哈希必须仍为起始值。

- [ ] **Step 3: Apply the one-line production fix**

把当前最后一个参数：

```csharp
Environment.NewLine + "  Result=" + Redact(detail, password));
```

改为：

```csharp
Environment.NewLine + "  Result=" + Redact(detail, password),
Environment.NewLine);
```

不得改动格式字符串、方法签名或 FTP 委托。

- [ ] **Step 4: Run GREEN**

Run the same full contract command.

Expected: exit 0；新步骤日志断言和所有现有 FTP/UI 回归断言通过。

- [ ] **Step 5: Build Release/AnyCPU in isolation**

使用唯一 Temp 根目录，并同时设置：

```text
/p:OutputPath=<temp>\out\
/p:BaseIntermediateOutputPath=<temp>\obj\
/p:IntermediateOutputPath=<temp>\obj\Release\
```

Expected: exit 0。记录 `PatchManager.exe` 的绝对路径、大小和 SHA-256。

- [ ] **Step 6: Audit scope and protected hashes**

确认只有两个 owned 文件变化；`PMain.cs`、Designer、csproj、已批准文档和 `PatchManager/obj/Release` 均未被本轮修改。报告真实 FTP 复测仍未执行。

