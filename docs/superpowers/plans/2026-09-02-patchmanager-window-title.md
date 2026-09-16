# PatchManager Window Title Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将 PatchManager 正式版主窗口标题精确设置为“补丁管理器”。

**Architecture:** 保留现有 WinForms 结构，只修改 Designer 生成的 `PMain.Text` 值，并用现有程序集行为契约锁定精确标题。

**Tech Stack:** C#、.NET Framework 4.8、Windows Forms、PowerShell 5.1、MSBuild 2022。

## Global Constraints

- 只修改 `PatchManager/PMain.Designer.cs` 和 `tests/test_patchmanager_ftp_diagnostics_contract.ps1`。
- 不修改程序名、版本、布局、按钮、FTP 或日志行为。
- 先 RED 后 GREEN。
- 不连接真实 FTP。
- Release 构建输出和中间目录全部进入唯一 Temp 根目录。
- 非 Git；正式目标路径未知时不部署或覆盖。

---

### Task 1: Set the exact production window title

**Files:**

- Modify: `PatchManager/PMain.Designer.cs:507`
- Test: `tests/test_patchmanager_ftp_diagnostics_contract.ps1`

**Interfaces:**

- Preserves: `PMain` 类型和所有控件/事件。
- Produces: 新建 `PMain` 后 `Text == "补丁管理器"`。

- [ ] **Step 1: Add the failing title assertion**

在现有契约创建 `$form` 后断言精确标题；使用 Unicode 码点构造中文，兼容 PowerShell 5.1：

```powershell
$expectedWindowTitle = ([char[]](0x8865, 0x4E01, 0x7BA1, 0x7406, 0x5668)) -join ''
if ($form.Text -ne $expectedWindowTitle) {
    Write-Output "RED exact symptom reproduced: unexpected window title '$($form.Text)'"
}
Assert-Contract ($form.Text -eq $expectedWindowTitle) 'PatchManager window title is not the approved production title'
```

- [ ] **Step 2: Run RED**

Run:

```powershell
powershell.exe -STA -NoProfile -ExecutionPolicy Bypass -File .\tests\test_patchmanager_ftp_diagnostics_contract.ps1
```

Expected: exit nonzero，输出旧标题 `补丁管理器 qq715590` 的精确 RED；生产源码尚未修改。

- [ ] **Step 3: Apply the one-line Designer change**

```csharp
this.Text = "补丁管理器";
```

不得修改其他 Designer 属性。

- [ ] **Step 4: Run GREEN and isolated Release build**

复跑完整契约，Expected: exit 0。随后以 Release/AnyCPU 构建，并同时将 `OutputPath`、`BaseIntermediateOutputPath`、`IntermediateOutputPath` 指向唯一 Temp 根目录。

- [ ] **Step 5: Audit scope**

确认只有两个 owned 文件改变，保护文件和源码树 `PatchManager/obj/Release` 未被本轮触碰。记录正式 Release EXE 路径、大小和 SHA-256；不覆盖未知正式路径。

