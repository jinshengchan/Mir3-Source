# PatchManager 正式版窗口标题设计

日期：2026-09-02

## 目标

将主窗口标题从 `补丁管理器 qq715590` 精确改为 `补丁管理器`。

## 范围

- 只修改 `PatchManager/PMain.Designer.cs` 中 `PMain.Text`。
- 在现有 `tests/test_patchmanager_ftp_diagnostics_contract.ps1` 中增加程序集级标题断言。
- 不修改程序文件名、程序集版本、按钮文字、FTP 行为或布局。
- 构建 Release/AnyCPU 正式产物；在正式部署路径未确认前不覆盖现有工具。

## 验证

- 修复前契约因窗口标题仍含 QQ 文本而 RED。
- 修复后完整契约 exit 0，主窗口 `Text` 精确等于 `补丁管理器`。
- Release/AnyCPU 使用唯一 Temp 输出和中间目录构建。

