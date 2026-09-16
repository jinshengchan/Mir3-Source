# PatchManager FTP 测试步骤日志格式修复设计

日期：2026-09-02

## 已确认问题

真实 FTP 测试提示上传失败，但日志中的异常不是网络异常，而是：

```text
System.FormatException: 索引(从零开始)必须大于或等于零，且小于参数列表的大小。
```

堆栈定位到 `FtpDiagnostics.RecordConnectionStep`。该方法的格式字符串使用 `{0}` 至 `{5}` 六个占位符，实际只提供五个参数，因此在上传委托调用 FTP 之前就抛出异常；清理委托也在发出删除请求前因同一日志错误失败。`WebExceptionStatus` 和 FTP 状态均为“无”，进一步证明失败发生在本地日志格式化阶段。

## 决策

保留现有格式字符串和日志布局，补上缺失的第六个 `Environment.NewLine` 参数。该参数既满足 `{5}`，又让每条步骤日志以换行结束，避免后续记录粘连。

不采用：

- 删除 `{5}`：虽然不再抛异常，但会让相邻日志记录粘连。
- 捕获并吞掉格式异常：会隐藏日志实现错误，无法保证要求的步骤记录实际写入。

## 修改范围

允许修改：

- `PatchManager/FtpDiagnostics.cs`：仅为 `RecordConnectionStep` 补充缺失参数。
- `tests/test_patchmanager_ftp_diagnostics_contract.ps1`：直接调用步骤日志方法并验证行为。

禁止修改：

- `PatchManager/PMain.cs`
- `PatchManager/PMain.Designer.cs`
- `PatchManager/PatchManager.csproj`
- FTP 地址、账号、权限、上传/下载/删除逻辑
- 服务器文件和发布目录程序

## 回归契约

契约使用虚拟 FTP URI，直接反射调用 `RecordConnectionStep`，不进行网络访问。断言：

1. 方法不抛异常。
2. `PatchManager.log` 包含模式、步骤、目标与结果。
3. 日志不包含密码哨兵。
4. 原有上传失败、清单失败、探测清理、按钮可见性和配置隔离断言继续通过。

## 验收标准

- 修复前同一契约因 `FormatException` 精确 RED。
- 修复后完整契约 exit 0。
- Release/AnyCPU 隔离构建 exit 0。
- 不连接真实 FTP，不部署、不重启。

