# PatchManager FTP Upload Diagnostics Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 让端游、手游普通补丁和手游 APK 的 FTP 失败变为可定位的受控错误，并增加独立的端游/手游完整读写连接测试。

**Architecture:** 保留现有 WinForms 和 `WebClient` 上传协议，在一个小型 `FtpDiagnostics.cs` 中集中异常格式化、脱敏日志和可测试的上传—回读—删除探测编排。`PMain` 仍负责 UI、配置快照和真实 FTP 调用；现有上传改用可传播异常的 Task API，所有失败统一写日志并停止发布。

**Tech Stack:** C#、.NET Framework 4.8、Windows Forms、`WebClient`/`FtpWebRequest`、PowerShell 5.1 行为契约、MSBuild 2022。

## Global Constraints

- 端游、手游普通补丁和手游 APK 必须共用同一套错误处理，不复制三套上传实现。
- 日志固定为 `PatchManager.exe` 所在目录的 `PatchManager.log`，UTF-8 追加写入。
- 日志和弹窗不得泄露 FTP 密码；目标 URI 中的 user-info 和异常文本中的实际密码都必须脱敏。
- 不修改 FTP 主机、端口、账号、密码、服务器配置、补丁格式、`PList.Bin` 或 `APKVersion.bin` 协议。
- 测试连接只能操作唯一的 `.patchmanager-test-{Guid}.tmp`，不得读取、覆盖或删除正式文件。
- 非 Git 工作区：禁止 Git、提交、PR、部署、服务重启和真实补丁上传。
- 构建输出必须进入唯一隔离目录，不能覆盖桌面或 `工具\PatchManager` 中的现有程序。

---

## File Structure

- Create: `PatchManager/FtpDiagnostics.cs` — FTP 失败报告、密码脱敏、日志追加、连接探测结果和可测试的上传—回读—删除编排。
- Modify: `PatchManager/PMain.cs` — 接入受控上传失败、版本清单失败、连接测试事件及 UI 状态恢复。
- Modify: `PatchManager/PMain.Designer.cs` — 增加 `pcTestFtpButton`、`mobTestFtpButton` 和事件绑定。
- Modify: `PatchManager/PatchManager.csproj` — 仅登记 `FtpDiagnostics.cs` 编译项。
- Create: `tests/test_patchmanager_ftp_diagnostics_contract.ps1` — 在隔离目录构建并执行真实程序集行为契约，不连接外部 FTP。

### Task 1: 建立现有误报与未处理异常的 RED 契约

**Files:**
- Create: `tests/test_patchmanager_ftp_diagnostics_contract.ps1`
- Read: `PatchManager/PMain.cs:122`
- Read: `PatchManager/PMain.cs:376`
- Read: `PatchManager/PMain.cs:496`
- Read: `PatchManager/PMain.cs:593`

**Interfaces:**
- Consumes: 现有私有 `bool Upload(PatchInformation, IProgress<string>, bool)`。
- Produces: 单一 PowerShell 入口，后续所有任务反复运行。

- [ ] **Step 1: 编写失败上传行为场景**

契约必须在 `-STA` PowerShell 中：

```powershell
$failureUri = 'http://127.0.0.1:1/'
$sentinelPassword = 'SECRET-PASSWORD-MUST-NOT-APPEAR'
$patchFile = Join-Path $caseRoot 'Patch\contract.bin.gz'
# 构造 PMain 和 PatchInformation，通过反射调用 Upload。
# 手工期望：返回 $false，且 $patchFile 仍存在。
```

当前生产代码应稳定复现：`UploadFileCompleted` 忽略 `e.Error`，连接失败后 `Upload` 返回成功并删除 `$patchFile`。契约打印 `RED exact symptom reproduced` 后以非零退出。

- [ ] **Step 2: 编写版本清单异常场景**

契约以同一拒绝连接地址调用 `SaveVersion`，手工期望为：方法返回 `false`、不向调用者抛出 `TargetInvocationException`、日志包含 `PList.Bin` 和失败阶段。

- [ ] **Step 3: 编写脱敏和连接探测行为断言**

契约必须在生产类型出现后执行以下行为断言；类型尚不存在时属于预期 RED：

```text
FtpDiagnostics: 用户摘要包含模式/阶段/Web状态/日志路径；日志不含 sentinel password
FtpConnectionProbe success: 调用顺序严格为 Upload, Download, Delete
FtpConnectionProbe mismatch: 返回“回读校验”失败并仍调用 Delete
FtpConnectionProbe delete failure: 返回失败并报告唯一远端残留文件名
CreateRemoteFileName twice: 两次不同，均匹配 .patchmanager-test-*.tmp
```

- [ ] **Step 4: 运行 RED**

Run:

```powershell
powershell.exe -STA -NoProfile -ExecutionPolicy Bypass -File .\tests\test_patchmanager_ftp_diagnostics_contract.ps1
```

Expected: 非零退出，并明确打印 `RED exact symptom reproduced`；失败原因必须是上传失败仍返回成功/删除临时文件，而不是构建、依赖或脚本语法错误。

### Task 2: 实现可测试的诊断与连接探测核心

**Files:**
- Create: `PatchManager/FtpDiagnostics.cs`
- Modify: `PatchManager/PatchManager.csproj`
- Test: `tests/test_patchmanager_ftp_diagnostics_contract.ps1`

**Interfaces:**
- Produces:

```csharp
internal sealed class FtpFailureReport
{
    internal string UserMessage { get; }
    internal string LogPath { get; }
    internal string LogWriteError { get; }
}

internal static class FtpDiagnostics
{
    internal static string LogPath { get; }
    internal static FtpFailureReport RecordFailure(
        string mode, string stage, Uri target, Exception error, string password);
    internal static void RecordConnectionStep(
        string mode, string stage, Uri target, string detail, string password);
}

internal sealed class FtpProbeResult
{
    internal bool Success { get; }
    internal string FailedStage { get; }
    internal Exception Error { get; }
    internal string RemoteFileName { get; }
    internal bool RemoteFileMayRemain { get; }
}

internal static class FtpConnectionProbe
{
    internal static string CreateRemoteFileName();
    internal static FtpProbeResult Execute(
        Uri target,
        byte[] expected,
        Action<Uri, byte[]> upload,
        Func<Uri, byte[]> download,
        Action<Uri> delete);
}
```

- [ ] **Step 1: 确认 RED 失败点仍为缺失行为**

Run: Task 1 的契约命令。

Expected: `RED exact symptom reproduced`，且没有生产源码改动。

- [ ] **Step 2: 实现最小诊断格式化与日志**

实现要求：

```text
LogPath = Path.Combine(Path.GetDirectoryName(typeof(FtpDiagnostics).Assembly.Location), "PatchManager.log")
RecordFailure = 中文短摘要 + WebExceptionStatus + FtpWebResponse 状态 + ex.ToString() 日志
Redaction = URI user-info 去除，并将非空 password 在摘要、状态说明、异常链中替换为 ***
Log I/O failure = 返回 LogWriteError，不覆盖原始 FTP 错误，也不再次抛出
Append = UTF-8，静态锁保护并发追加
```

- [ ] **Step 3: 实现最小连接探测状态机**

`Execute` 必须严格执行：上传 → 下载 → `SequenceEqual(expected)` → 删除。上传成功后无论回读是否匹配都尝试删除；删除失败时 `RemoteFileMayRemain=true`。若主失败和删除失败同时存在，用可读的组合异常保留两者，不覆盖主失败。

- [ ] **Step 4: 登记编译文件并运行局部行为契约**

Run: Task 1 的契约命令。

Expected: 诊断格式、脱敏、唯一文件名和纯探测编排断言通过；现有 `Upload`/`SaveVersion` 场景仍为 RED。

### Task 3: 修复端游/手游共用上传与版本发布失败处理

**Files:**
- Modify: `PatchManager/PMain.cs:122`
- Modify: `PatchManager/PMain.cs:376`
- Modify: `PatchManager/PMain.cs:496`
- Modify: `PatchManager/PMain.cs:593`
- Test: `tests/test_patchmanager_ftp_diagnostics_contract.ps1`

**Interfaces:**
- Consumes: `FtpDiagnostics.RecordFailure`。
- Preserves: `Upload(PatchInformation, IProgress<string>, bool)` 返回 `bool`。
- Changes: `SaveVersion` 返回 `bool` 并接收 `IProgress<string>`。

```csharp
private bool SaveVersion(
    List<PatchInformation> current,
    IProgress<string> progress,
    bool isAPKinfo = false);
```

- [ ] **Step 1: 运行并保存现有 RED 证据**

Run: Task 1 的契约命令。

Expected: 上传失败仍被误报成功，或 `SaveVersion` 异常越界。

- [ ] **Step 2: 让异步上传异常同步传播**

在现有后台 `UploadPatch` 线程内使用：

```csharp
client.UploadFileTaskAsync(targetUri, localPath).GetAwaiter().GetResult();
```

保留 `UploadProgressChanged`。只有 Task 成功后才增加 `TotalProgress` 并删除普通补丁临时文件；失败调用统一诊断、向状态栏报告并返回 `false`。

- [ ] **Step 3: 收拢发布失败边界**

`SaveVersion` 捕获 `UploadData` 异常，按端游/手游与 `PList.Bin`/`APKVersion.bin` 写日志、显示详细提示并返回 `false`。`CreatePatch` 必须：

```text
普通上传失败 -> Error=true，不上传版本清单，不删除失败临时文件
版本清单失败 -> Error=true，不进入后续手游 APK 发布
任何退出路径 -> finally 恢复 InterfaceLock(true)
```

现有 `Patch` 目录删除必须位于确认没有上传错误的分支，不能清除失败文件。

- [ ] **Step 4: 运行 GREEN 契约**

Run: Task 1 的契约命令。

Expected: 上传失败返回 `false`、临时文件保留、`SaveVersion` 返回 `false`、日志包含阶段和 `PList.Bin`、日志不含 sentinel password。

### Task 4: 增加端游与手游完整 FTP 连接测试按钮

**Files:**
- Modify: `PatchManager/PMain.Designer.cs:165`
- Modify: `PatchManager/PMain.Designer.cs:400`
- Modify: `PatchManager/PMain.Designer.cs:438`
- Modify: `PatchManager/PMain.cs:184`
- Modify: `PatchManager/PMain.cs`（新增两个事件处理器和一个共享异步方法）
- Test: `tests/test_patchmanager_ftp_diagnostics_contract.ps1`

**Interfaces:**
- Consumes: `FtpConnectionProbe`、`FtpDiagnostics`。
- Produces:

```csharp
private async void pcTestFtpButton_Click(object sender, EventArgs e);
private async void mobTestFtpButton_Click(object sender, EventArgs e);
private async Task TestFtpConnectionAsync(
    string mode,
    string host,
    bool useLogin,
    string username,
    string password);
```

- [ ] **Step 1: 扩展契约的 UI 和配置隔离断言**

实例化窗体并按控件 `Name` 查找：

```text
pcTestFtpButton.Text == 测试端游 FTP
mobTestFtpButton.Text == 测试手游 FTP
两个按钮均绑定独立事件；共享方法接收配置快照，不读写 IsMobPath
```

Run: Task 1 的契约命令。

Expected: 当前因按钮不存在而 RED。

- [ ] **Step 2: 增加两个按钮**

在两个上传按钮上方使用现有列宽：

```text
pcTestFtpButton: Location(100, 246), Size(233, 27), Text="测试端游 FTP"
mobTestFtpButton: Location(429, 246), Size(233, 27), Text="测试手游 FTP"
```

将两按钮纳入 `InterfaceLock`，连接测试期间禁止同时上传或修改配置。

- [ ] **Step 3: 实现真实 FTP 操作闭包**

共享异步方法先验证绝对 FTP URI，再生成唯一名称和 UTF-8 随机标记内容。在 `Task.Run` 内给 `FtpConnectionProbe.Execute` 传入：

```text
upload: 新 WebClient + 配置快照凭据 + UploadData
download: 新 WebClient + 配置快照凭据 + DownloadData
delete: FtpWebRequest(Method=DeleteFile, Credentials=配置快照, KeepAlive=false)
```

每个开始/成功阶段调用 `RecordConnectionStep`。完整成功显示“连接及读写测试成功”；失败使用统一详细弹窗。删除失败必须显示 `RemoteFileName` 并说明可能残留。

- [ ] **Step 4: 运行 GREEN 契约**

Run: Task 1 的契约命令。

Expected: 两个按钮存在；端游/手游配置独立；探测调用顺序、回读不匹配清理、删除失败残留提示全部通过。

### Task 5: 完整验证与隔离构建

**Files:**
- Verify only: `PatchManager/FtpDiagnostics.cs`
- Verify only: `PatchManager/PMain.cs`
- Verify only: `PatchManager/PMain.Designer.cs`
- Verify only: `PatchManager/PatchManager.csproj`
- Verify only: `tests/test_patchmanager_ftp_diagnostics_contract.ps1`

**Interfaces:**
- Produces: 主任务可复跑的测试输出、隔离 `PatchManager.exe` 和 SHA-256。

- [ ] **Step 1: 运行完整契约**

Run:

```powershell
powershell.exe -STA -NoProfile -ExecutionPolicy Bypass -File .\tests\test_patchmanager_ftp_diagnostics_contract.ps1
```

Expected: exit 0；输出上传失败受控、临时文件保留、版本清单失败受控、脱敏、连接探测顺序、两个按钮配置隔离全部 PASS。

- [ ] **Step 2: 隔离 Release 构建**

Run:

```powershell
$verifyRoot = Join-Path $env:TEMP ('PatchManager-upload-diagnostics-' + [Guid]::NewGuid().ToString('N'))
$verifyOut = Join-Path $verifyRoot 'out'
New-Item -ItemType Directory -Path $verifyOut -Force | Out-Null
& 'C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\MSBuild\Current\Bin\MSBuild.exe' `
  '.\PatchManager\PatchManager.csproj' /t:Rebuild /p:Configuration=Release /p:Platform=AnyCPU `
  "/p:OutputPath=$verifyOut\" /nologo /verbosity:minimal
```

Expected: exit 0，`$verifyOut\PatchManager.exe` 存在；没有写入 `工具\PatchManager` 或桌面程序目录。

- [ ] **Step 3: 记录产物与范围证据**

Run:

```powershell
Get-Item -LiteralPath (Join-Path $verifyOut 'PatchManager.exe') | Select-Object FullName,Length,LastWriteTime
Get-FileHash -Algorithm SHA256 -LiteralPath (Join-Path $verifyOut 'PatchManager.exe')
```

Expected: 返回唯一隔离路径、非零大小和 SHA-256。报告真实 FTP 测试、服务器落盘、部署和重启均未执行，等待用户运行新按钮验收。
