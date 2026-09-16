# 假人管理紧凑按钮布局 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 为假人管理窗口的三类按钮增加最大宽度和居中布局，使宽窗口中的按钮保持紧凑、窄窗口中仍能自动缩小且不越界。

**Architecture:** 继续复用 `BotConfigView` 现有 `AddButtonRow` / `ResizeButtonRow` 布局通道，通过按钮的 `MaximumSize.Width` 传递每类最大宽度。`ResizeButtonRow` 先按可用宽度等分，再应用最大宽度并计算整行居中起点，不改变按钮事件或业务逻辑。

**Tech Stack:** C# 7.2、.NET Framework 4.8 WinForms、PowerShell 反射契约、MSBuild 17、Fody。

## Global Constraints

- 左栏操作按钮最大宽度为 180 像素。
- 右栏行为快捷按钮最大宽度为 220 像素。
- 右栏按档快速切图按钮最大宽度为 150 像素。
- 窄窗口中按钮必须缩小到所属行以内，禁止横向滚动或裁剪。
- 按钮行整体水平居中；输入框、状态、列表和日志继续随栏宽伸缩。
- 不修改按钮文字、点击事件、运行时调节逻辑、配置、数据库、客户端或部署目录。
- 保持左右分组无重叠、右栏横向溢出为零、`同步到左侧` 仅在右栏显示一次。
- 当前目录不是 Git 仓库；不得初始化 Git、提交、推送或创建 PR。

---

### Task 1: 为按钮行增加最大宽度和居中布局

**Files:**
- Modify: `tests/test_bot_management_ui_contract.ps1`
- Modify: `Server/Views/BotConfigView.cs`

**Interfaces:**
- Consumes: `AddButtonRow(FlowLayoutPanel, int, params Button[])`、`ResizeButtonRow(Panel)`、现有左右栏构建方法。
- Produces: `AddButtonRow(FlowLayoutPanel flow, int rowWidth, int maxButtonWidth, params Button[] buttons)` 重载；按钮通过 `MaximumSize.Width` 表达宽度上限。

- [ ] **Step 1: 先写宽窗口与窄窗口的失败契约**

在 `test_bot_management_ui_contract.ps1` 的 STA 反射脚本中，按 `Name`/所属组收集以下按钮：

```powershell
$leftOperationButtons = @('BotStartButton','BotStopButton','BotRecallButton','BotPauseButton','BotSaveButton','BotRefreshButton')
$rightQuickButtons = @(Get-Buttons $quickGroup)
$mapButtons = @(Get-Buttons $mapGroup)
```

对 `1380x780` 和 `1740x780` 两种客户区分别输出并断言：

```text
COMPACT_BUTTONS=LeftMax<=180;QuickMax<=220;MapMax<=150
CENTERING=Left=True;Quick=True;Map=True
BUTTON_OVERFLOW=0
```

居中判定使用按钮行左右剩余空间之差不超过 1 像素；越界判定使用每个按钮的窗体相对 `Left/Right` 与所属行边界比较。随后把客户区缩到 `1000x700`，断言按钮宽度可以低于最大值且 `BUTTON_OVERFLOW=0`。

- [ ] **Step 2: 运行 UI 契约并确认 RED**

Run:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\tests\test_bot_management_ui_contract.ps1
```

Expected: FAIL；当前 `ResizeButtonRow` 会把按钮始终等分填满整行，宽窗口下超过 180/220/150，单按钮“刷新”也会占满整行。

- [ ] **Step 3: 增加按钮宽度常量和带上限的按钮行重载**

在 `BotConfigView` 常量区加入：

```csharp
private const int LeftOperationButtonMaxWidth = 180;
private const int RightQuickButtonMaxWidth = 220;
private const int MapButtonMaxWidth = 150;
```

保留现有无上限入口，并加入重载：

```csharp
private static void AddButtonRow(FlowLayoutPanel flow, int rowWidth, params Button[] buttons)
{
    AddButtonRow(flow, rowWidth, 0, buttons);
}

private static void AddButtonRow(FlowLayoutPanel flow, int rowWidth, int maxButtonWidth, params Button[] buttons)
{
    Panel row = CreateRow(rowWidth, 35);
    row.Tag = "button";
    foreach (Button button in buttons)
    {
        if (maxButtonWidth > 0)
            button.MaximumSize = new Size(maxButtonWidth, 0);
        row.Controls.Add(button);
    }
    row.Resize += delegate { ResizeButtonRow(row); };
    ResizeButtonRow(row);
    flow.Controls.Add(row);
}
```

- [ ] **Step 4: 将三类目标按钮行绑定对应最大宽度**

左栏“假人操作”所有按钮行使用 `LeftOperationButtonMaxWidth`，并把单独的刷新按钮改为单按钮行：

```csharp
AddButtonRow(operationsFlow, FullRowWidth, LeftOperationButtonMaxWidth, BotStartButton, BotStopButton, BotRecallButton);
AddButtonRow(operationsFlow, FullRowWidth, LeftOperationButtonMaxWidth, BotPauseButton, BotSaveButton);
AddButtonRow(operationsFlow, FullRowWidth, LeftOperationButtonMaxWidth, BotRefreshButton);
```

右栏“快捷操作”每行使用 `RightQuickButtonMaxWidth`；“按档快速切图”每行使用 `MapButtonMaxWidth`。按钮对象和点击处理程序保持原样。

- [ ] **Step 5: 修改 `ResizeButtonRow`，先等分、再限宽并居中**

最小实现：

```csharp
private static void ResizeButtonRow(Panel row)
{
    if (row == null || row.Controls.Count == 0) return;
    Button[] buttons = row.Controls.OfType<Button>().ToArray();
    if (buttons.Length == 0) return;

    int gaps = 5 * (buttons.Length - 1);
    int availableButtonWidth = Math.Max(1, row.ClientSize.Width - gaps);
    int width = Math.Max(1, availableButtonWidth / buttons.Length);
    int configuredMaximum = buttons
        .Where(button => button.MaximumSize.Width > 0)
        .Select(button => button.MaximumSize.Width)
        .DefaultIfEmpty(width)
        .Min();
    width = Math.Min(width, configuredMaximum);

    int totalWidth = width * buttons.Length + gaps;
    int x = Math.Max(0, (row.ClientSize.Width - totalWidth) / 2);
    foreach (Button button in buttons)
    {
        button.Location = new Point(x, 2);
        button.Width = width;
        x += width + 5;
    }
}
```

- [ ] **Step 6: 运行 UI 契约并确认 GREEN**

Run:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\tests\test_bot_management_ui_contract.ps1
```

Expected: PASS；输出三类最大宽度、三类居中结果和宽/窄窗口 `BUTTON_OVERFLOW=0`，同时保留现有 `RIGHT_BOUNDS Overflow=0`、`OVERLAP Left=0;Right=0` 和按钮归属断言。

---

### Task 2: 独立回归、构建和产物验收

**Files:**
- Verify: `tests/test_bot_management_config_contract.ps1`
- Verify: `tests/test_bot_management_runtime_contract.ps1`
- Verify: `tests/test_bot_management_rewards_contract.ps1`
- Verify: `tests/test_bot_management_operations_contract.ps1`
- Verify: `tests/test_bot_management_ui_contract.ps1`
- Build output: `.artifacts/bot-management-compact-buttons-ready/`

**Interfaces:**
- Consumes: Task 1 的最终源码和 UI 契约。
- Produces: 正常 Fody `Server.exe`、SHA-256、短启动证据。

- [ ] **Step 1: 分别运行五组契约**

每个脚本使用独立 Windows PowerShell 进程：

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\tests\test_bot_management_config_contract.ps1
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\tests\test_bot_management_runtime_contract.ps1
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\tests\test_bot_management_rewards_contract.ps1
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\tests\test_bot_management_operations_contract.ps1
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\tests\test_bot_management_ui_contract.ps1
```

Expected: 五组退出码均为 0，并记录断言总数。

- [ ] **Step 2: 构建 ServerLibrary**

```powershell
dotnet build .\ServerLibrary\ServerLibrary.csproj -c Debug --no-restore
```

Expected: 0 errors。

- [ ] **Step 3: 正常 Fody 重建 Server**

```powershell
& 'C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\MSBuild\Current\Bin\MSBuild.exe' `
  '.\Server\Server.csproj' /t:Rebuild /p:Configuration=Debug /p:Platform=AnyCPU `
  "/p:OutDir=D:\相聚假人\Source\.artifacts\bot-management-compact-buttons-ready\" /m /v:minimal
```

Expected: 0 errors；只允许既有 `MSB3277 System.Runtime.InteropServices.RuntimeInformation` 版本冲突警告。

- [ ] **Step 4: 短启动新产物并只清理测试 PID**

在确认启动前 `Server.exe` PID 列表后，从新产物目录隐藏启动。15 秒内确认：

```text
MainWindowTitle=Z3服务端
Responding=True
```

只结束本次创建的确切 PID；等待 1 秒后确认没有新增残留 PID，不操作启动前已存在的任何进程。

- [ ] **Step 5: 生成交付证据**

报告：两处实际修改文件、RED/GREEN、三类按钮宽度与居中值、宽/窄窗口溢出数、五组断言数、构建错误/警告、短启动 PID/标题/响应、产物绝对路径和 SHA-256。明确未部署、未改正式配置和正式进程。
