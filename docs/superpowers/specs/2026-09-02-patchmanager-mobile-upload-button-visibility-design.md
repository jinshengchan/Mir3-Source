# PatchManager 手游上传按钮 Release 可见性设计

日期：2026-09-02

## 问题与证据

Release/AnyCPU 构建中，“测试手游 FTP”可见，但“上传手游补丁”不可见。对当前 Release 程序集执行真实 `PMain_Load` 后，`mobUploadPatchButton` 仍存在于控件树中，位置也未与测试按钮重叠，但自身可见状态由 `true` 变为 `false`；`mobTestFtpButton` 仍为 `true`。

根因是 `PMain_Load` 内的 `#if !DEBUG` 分支在 Release 构建中主动执行：

```csharp
mobUploadPatchButton.Enabled = false;
mobUploadPatchButton.Visible = false;
```

## 决策

删除这段 Release 专用隐藏逻辑。端游与手游上传按钮、两个 FTP 测试按钮在 Release 中都保持 Designer 定义的可见状态；不增加配置开关，不改变位置、文字、事件绑定或上传行为。

## 修改范围

允许修改：

- `PatchManager/PMain.cs`：仅删除 Release 隐藏手游上传按钮的条件分支。
- `tests/test_patchmanager_ftp_diagnostics_contract.ps1`：增加 Release 加载后手游上传按钮仍可见的行为断言。

禁止修改：

- `PatchManager/PMain.Designer.cs`
- `PatchManager/FtpDiagnostics.cs`
- `PatchManager/PatchManager.csproj`
- FTP 配置、上传协议、日志格式和服务器文件
- 发布目录中的现有 `PatchManager.exe`

## 验证

1. 先让当前 Release 源码因 `PMain_Load` 后 `mobUploadPatchButton` 不可见而 RED。
2. 删除条件隐藏逻辑后，同一契约必须 GREEN。
3. 原有 FTP 诊断、失败文件保留、探测清理和端游/手游配置隔离断言必须继续通过。
4. Release/AnyCPU 构建的输出和中间目录都放入唯一 Temp 目录。
5. 自动化不连接真实 FTP，不部署、不重启。

## 验收标准

- Release 版本加载后，“上传手游补丁”和“测试手游 FTP”同时可见且不重叠。
- 只删除 Release 隐藏逻辑，不改变手游上传功能本身。
- 完整契约 exit 0，隔离 Release/AnyCPU 构建 exit 0。

