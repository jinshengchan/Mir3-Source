# PatchManager Mobile Upload Button Visibility Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 让 Release/AnyCPU 版本加载后继续显示“上传手游补丁”按钮。

**Architecture:** 保留现有 WinForms Designer 布局和事件绑定，只移除 `PMain_Load` 中 Release 专用的隐藏逻辑。现有 PowerShell 行为契约通过反射执行真实 Release `PMain_Load` 并检查控件自身 Visible 状态，锁定用户截图中的回归。

**Tech Stack:** C#、.NET Framework 4.8、Windows Forms、PowerShell 5.1、MSBuild 2022。

## Global Constraints

- 只修改 `PatchManager/PMain.cs` 和 `tests/test_patchmanager_ftp_diagnostics_contract.ps1`。
- 不修改 Designer、FTP 上传/测试/日志逻辑和服务器配置。
- 必须先得到精确 RED，再修改生产源码。
- 非 Git 工作区：不提交、不部署、不重启、不连接真实 FTP。
- `OutputPath`、`BaseIntermediateOutputPath`、`IntermediateOutputPath` 必须全部进入唯一 Temp 目录。

---

## File Structure

- Modify: `PatchManager/PMain.cs` — 删除 Release 专用的手游上传按钮隐藏分支。
- Modify: `tests/test_patchmanager_ftp_diagnostics_contract.ps1` — 增加 Release 加载后的按钮可见性回归断言。

### Task 1: Restore the mobile upload button in Release

**Files:**

- Modify: `PatchManager/PMain.cs:531-539`
- Test: `tests/test_patchmanager_ftp_diagnostics_contract.ps1`

**Interfaces:**

- Consumes: 现有私有 `void PMain_Load(object, EventArgs)` 与 WinForms `Control.GetState(int)`。
- Preserves: `mobUploadPatchButton_Click(object, EventArgs)`、Designer 位置与事件绑定。
- Produces: Release 加载后 `mobUploadPatchButton` 自身 Visible 状态为 `true`。

- [ ] **Step 1: Write the failing Release visibility assertion**

在现有契约创建并找到 `mobUploadPatchButton` 后，通过反射调用真实加载事件并读取控件自身 Visible 状态，避免未显示父窗体导致公开 `Visible` 属性返回假阴性：

```powershell
$loadMethod = Get-PrivateMethod -Type $pMainType -Name 'PMain_Load' -ParameterCount 2
$getState = [System.Windows.Forms.Control].GetMethod(
    'GetState',
    [System.Reflection.BindingFlags]::Instance -bor [System.Reflection.BindingFlags]::NonPublic)
Assert-Contract ($null -ne $getState) 'cannot inspect WinForms visible state'
$loadMethod.Invoke($form, [object[]]@($null, [EventArgs]::Empty)) | Out-Null
$mobileUploadVisible = [bool]$getState.Invoke($mobButton, [object[]]@(2))
if (-not $mobileUploadVisible) {
    Write-Output 'RED exact symptom reproduced: Release PMain_Load hides mobUploadPatchButton'
}
Assert-Contract $mobileUploadVisible 'Release PMain_Load hid mobUploadPatchButton'
```

- [ ] **Step 2: Run RED**

Run:

```powershell
powershell.exe -STA -NoProfile -ExecutionPolicy Bypass -File .\tests\test_patchmanager_ftp_diagnostics_contract.ps1
```

Expected: exit nonzero with `RED exact symptom reproduced: Release PMain_Load hides mobUploadPatchButton`; all setup and earlier assertions must have reached the visibility check.

- [ ] **Step 3: Apply the minimal production fix**

Delete only this block from `PMain_Load`:

```csharp
#if !DEBUG
            mobUploadPatchButton.Enabled = false;
            mobUploadPatchButton.Visible = false;
#endif
```

Do not add a replacement flag or change Designer coordinates.

- [ ] **Step 4: Run GREEN**

Run the same contract command.

Expected: exit 0; the new Release visibility assertion and every existing FTP diagnostic assertion pass.

- [ ] **Step 5: Build Release/AnyCPU in isolation**

Use a unique Temp root and pass all three properties:

```text
/p:OutputPath=<temp>\out\
/p:BaseIntermediateOutputPath=<temp>\obj\
/p:IntermediateOutputPath=<temp>\obj\Release\
```

Expected: exit 0 and `PatchManager.exe` exists only in the isolated output. Record path, byte length and SHA-256.

- [ ] **Step 6: Scope and hash audit**

Confirm only the two owned files changed, both approved documents remain unchanged, and no build touched `PatchManager/obj/Release` during this correction. Return full before/after SHA-256 and explicitly leave real UI/FTP/deployment acceptance open.

