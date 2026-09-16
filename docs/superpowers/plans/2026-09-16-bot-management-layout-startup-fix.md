# 假人管理分栏与启动时序修复 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 修复假人管理左栏异常占宽和数据库未就绪时提前加载假人导致逐行空引用的问题。

**Architecture:** 保留现有 WinForms 双栏结构，只把分隔位置设置推迟到控件获得真实尺寸之后。自动启动改为由 `SMain` 在服务器环境及三张数据库集合就绪后触发，`BotManager.Start` 同时保留入口级保护，避免其他调用者绕过时序。

**Tech Stack:** C# 7.2、.NET Framework 4.8 WinForms、DevExpress MDI、PowerShell 契约测试、MSBuild 17。

## Global Constraints

- 只修改 `Server/Views/BotConfigView.cs`、`Server/SMain.cs`、`Server/BotManager.cs` 和对应两个现有契约脚本。
- 不修改 `假人.txt`、数据库、客户端、部署目录、正式配置或正式进程。
- 不改变假人行为、配置字段和 PVP 合法性保护。
- 此目录不是 Git 仓库，不执行提交、PR 或部署。

---

### Task 1: 建立分栏布局回归契约

**Files:**
- Modify: `tests/test_bot_management_ui_contract.ps1`
- Modify: `Server/Views/BotConfigView.cs`

**Interfaces:**
- Consumes: `BotConfigView.InitializeComponent()` 和其顶层 `SplitContainer`。
- Produces: 真实尺寸下左栏约 530px、右栏不少于 700px 的布局。

- [ ] **Step 1: 写失败契约**

在 UI 契约中增加源码顺序断言：`Controls.Add(split)` 必须早于最终 `split.SplitterDistance = 530`；再用 STA PowerShell 反射实例化最新完整构建，将 `ClientSize` 设为 `1380×780`，断言 `Panel1.Width` 在 500–600、`Panel2.Width >= 700`。

- [ ] **Step 2: 验证 RED**

Run: `powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\tests\test_bot_management_ui_contract.ps1`

Expected: FAIL，当前运行时值为 `P1=1113, P2=263`。

- [ ] **Step 3: 最小实现**

从 `SplitContainer` 对象初始化器移除 `SplitterDistance = 530`，在 `ClientSize` 设置且 `Controls.Add(split)` 完成后执行：

```csharp
PerformLayout();
split.SplitterDistance = Math.Min(530, Math.Max(split.Panel1MinSize, split.ClientSize.Width - split.Panel2MinSize));
```

不得改写组框、控件或业务事件。

- [ ] **Step 4: 验证 GREEN**

重新构建完整 Server，再运行 UI 契约和反射布局检查，预期右栏不少于 700px。

---

### Task 2: 建立启动时序回归契约

**Files:**
- Modify: `tests/test_bot_management_runtime_contract.ps1`
- Modify: `Server/SMain.cs`
- Modify: `Server/BotManager.cs`

**Interfaces:**
- Consumes: `SEnvir.Started`、`SEnvir.AccountInfoList`、`SEnvir.CharacterInfoList`、`SEnvir.BotAccountInfoList`。
- Produces: `SMain.TryAutoStartBotSystem()`；`BotManager.Start()` 的数据库就绪入口保护。

- [ ] **Step 1: 写失败契约**

增加以下源码契约：

```powershell
Assert-NotContains $sMainLoadBlock 'BotManager.Start('
Assert-Contains $sMain 'TryAutoStartBotSystem'
Assert-Contains $sMain 'SEnvir.Started'
Assert-Contains $sMain 'SEnvir.BotAccountInfoList'
Assert-Contains $botManager '假人系统启动延后：服务器数据库尚未就绪'
```

- [ ] **Step 2: 验证 RED**

Run: `powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\tests\test_bot_management_runtime_contract.ps1`

Expected: FAIL，因为 `SMain_Load` 当前直接调用 `BotManager.Start`，且入口无数据库保护。

- [ ] **Step 3: 最小实现**

在 `SMain` 增加 `_botAutoStartAttempted` 和 `TryAutoStartBotSystem()`：仅当 `SEnvir.Started` 且三个集合及其 `Binding` 非空时置为已尝试并校验配置、调用 `BotManager.Start`；在服务器未启动时重置该标记。删除 `SMain_Load` 中现有自动启动块，并在 `InterfaceTimer_Tick` 调用该方法。

在 `BotManager.Start` 的文件与数量检查之后、修改任何运行状态之前增加：

```csharp
if (!SEnvir.Started
    || SEnvir.AccountInfoList?.Binding == null
    || SEnvir.CharacterInfoList?.Binding == null
    || SEnvir.BotAccountInfoList?.Binding == null)
{
    SEnvir.Log("假人系统启动延后：服务器数据库尚未就绪");
    return;
}
```

- [ ] **Step 4: 验证 GREEN**

运行 runtime 契约；预期通过且不再允许数据库未就绪时进入逐行解析。

---

### Task 3: 全量验证与可运行产物

**Files:**
- Verify: `tests/test_bot_management_*_contract.ps1`
- Create: `.artifacts/bot-management-layout-startup-ready/`

**Interfaces:**
- Consumes: Tasks 1–2 的最终源码。
- Produces: 可运行的完整 Fody 构建与 SHA-256。

- [ ] **Step 1: 运行五组独立契约**

逐个以独立 `powershell.exe` 进程运行 config、runtime、rewards、operations、ui 契约；任何非零退出码立即失败。

- [ ] **Step 2: 构建 ServerLibrary**

Run: `dotnet build .\ServerLibrary\ServerLibrary.csproj -c Debug --no-restore`

Expected: 0 errors。

- [ ] **Step 3: 完整重建 Server**

使用 MSBuild `Rebuild`、`Configuration=Debug`、`Platform=AnyCPU`，不设置 `DisableFody`，输出到 `.artifacts/bot-management-layout-startup-ready\`。

Expected: 0 errors；只允许已知 `MSB3277 System.Runtime.InteropServices.RuntimeInformation` 版本冲突警告。

- [ ] **Step 4: 运行时验收**

从新输出目录启动 `Server.exe`，15 秒内确认进程未退出、窗口标题为“Z3服务端”且 `Responding=True`，随后仅停止该测试 PID。再次反射实例化 `BotConfigView`，确认 `P1=500–600`、`P2>=700`。

- [ ] **Step 5: 交付报告**

报告两个根因、契约断言数、构建警告/错误数、运行时分栏尺寸、产物绝对路径和 SHA-256；明确未部署、未修改正式配置及正式进程。
