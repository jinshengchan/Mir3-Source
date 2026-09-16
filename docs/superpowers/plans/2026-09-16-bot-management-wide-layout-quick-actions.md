# 假人管理 800px 双栏布局与临时快捷操作 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将假人管理左栏固定为 800px，优化左右栏多列排版，并让六个快捷增减按钮即时生效、可见提示且在全员下线后恢复基础值。

**Architecture:** 保留现有 `BotConfigView`、`SplitContainer` 和 `Config` 消费路径，只增加可复用的宽栏/双列布局辅助方法。快捷操作由 `BotManager.Management` 管理四个运行期值及其基础快照，直接更新现有 `Config` 运行值而不保存；停止假人或最后一名假人下线时恢复基础值，明确保存时将当前值升级为新基础值。

**Tech Stack:** C# 7.2、.NET Framework 4.8 WinForms、PowerShell 契约测试、MSBuild 17、Fody。

## Global Constraints

- 以 `docs/superpowers/specs/2026-09-16-bot-management-wide-layout-quick-actions-design.md` 为唯一功能规格。
- 左栏目标宽度为 800px；1380px 客户区下右栏不得小于约 520px。
- 快捷操作只改运行值，不自动写入 `Server.ini`；明确点击“保存配置”才持久化。
- 停止假人或最后一名假人下线时恢复快捷操作前的基础值；单个假人下线且仍有其他在线假人时不得重置。
- 不改变战斗目标选择、PK 安全区/队伍/行会/假人/宠物保护、药水购买与使用算法。
- 不修改数据库、客户端、部署目录、正式配置或正式进程。
- 此目录不是 Git 仓库，不执行 commit、PR、worktree 或部署。

---

### Task 1: 建立 800px 左栏与左右栏排版回归契约

**Files:**
- Modify: `tests/test_bot_management_ui_contract.ps1`
- Modify: `Server/Views/BotConfigView.cs`

**Interfaces:**
- Consumes: `BotConfigView.InitializeComponent()`、`BuildLeftColumn()`、`BuildRightColumn()`。
- Produces: `LeftPanelWidth = 800`、宽栏双列流、右栏双列流和整行控件布局。

- [ ] **Step 1: 将运行时分栏断言改为新规格**

把 UI 契约中的旧断言：

```powershell
if ($panel1Width -lt 500 -or $panel1Width -gt 600) { ... }
if ($panel2Width -lt 700) { ... }
```

替换为：

```powershell
if ($panel1Width -lt 790 -or $panel1Width -gt 810) {
    throw "FAIL: expected Panel1 width 790-810, got $panel1Width"
}
if ($panel2Width -lt 520) {
    throw "FAIL: expected Panel2 width >=520, got $panel2Width"
}
```

在反射脚本中递归按 `Name` 或 `Text` 查找控件并输出坐标，增加以下确定性断言：

```powershell
# 左栏自动行为前两项同一行、不同列
Assert-SameRowDifferentColumn 'BotAutoLevelCheckEdit' 'BotAutoPickupCheckEdit'
# 右栏经济控制前两项同一行、不同列
Assert-SameRowDifferentColumn 'BotInitialGoldFloorEdit' 'BotGoldFarmThresholdEdit'
# 快捷操作为两列
Assert-SameRowDifferentColumnByText '攻击性 +10' '攻击性 -10'
# 等级切图第一行四项
Assert-SameRowDifferentColumnByText '1-9级' '30-39级'
```

同时断言源码包含 `LeftPanelWidth = 800`、左栏双列辅助方法、右栏双列辅助方法、完整宽度状态行和禁止横向滚动的配置。

- [ ] **Step 2: 运行 UI 契约确认 RED**

Run:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\tests\test_bot_management_ui_contract.ps1
```

Expected: FAIL；当前反射值仍为 `P1=530`，且自动行为、经济控制和等级切图不是指定网格。

- [ ] **Step 3: 实现外层 800px 分栏**

在 `BotConfigView` 增加并统一使用以下常量：

```csharp
private const int LeftPanelWidth = 800;
private const int LeftGroupWidth = 775;
private const int RightPanelMinWidth = 520;
private const int HalfRowWidth = 365;
private const int FullRowWidth = 745;
```

初始化 `SplitContainer` 时设置：

```csharp
split.Panel1MinSize = LeftPanelWidth;
split.Panel2MinSize = RightPanelMinWidth;
ClientSize = new Size(1380, 820);
MinimumSize = new Size(1340, 650);
```

在控件加入窗体并完成布局后，以及尺寸变化时，使用同一计算：

```csharp
split.SplitterDistance = Math.Min(LeftPanelWidth,
    Math.Max(split.Panel1MinSize, split.ClientSize.Width - split.Panel2MinSize));
```

- [ ] **Step 4: 实现确定性的单双列布局辅助方法**

保留现有控件与事件，仅增加宽度参数和两列布局辅助方法：

```csharp
private static FlowLayoutPanel GetGroupFlow(GroupBox group, bool twoColumn, int contentWidth)
private static void AddField(FlowLayoutPanel flow, string labelText, Control control, int rowWidth)
private static void AddCheck(FlowLayoutPanel flow, CheckBox check, int rowWidth)
private static void AddFullWidthControl(FlowLayoutPanel flow, Control control, int rowWidth)
private static void ResizeRightColumnGroups(FlowLayoutPanel column)
```

两列流必须使用：

```csharp
FlowDirection = FlowDirection.LeftToRight;
WrapContents = true;
Width = contentWidth;
AutoSize = true;
AutoSizeMode = AutoSizeMode.GrowAndShrink;
```

左栏短字段/复选框使用 `HalfRowWidth`，路径、状态、按钮、地图操作、列表和日志使用 `FullRowWidth`。右栏状态和滑块使用整行；经济、性能、新增功能配置使用两列；快捷操作按两列三行；等级切图按四列两行。右栏列容器设置 `AutoScroll = true`，并在 `ClientSizeChanged` 中调用 `ResizeRightColumnGroups`，用 `column.ClientSize.Width - column.Padding.Horizontal - SystemInformation.VerticalScrollBarWidth - 2` 计算组框宽度，保证没有水平滚动条。

- [ ] **Step 5: 构建隔离产物并验证 UI GREEN**

先正常 Fody 重建到：

```text
D:\相聚假人\Source\.artifacts\bot-management-wide-layout-ready\
```

再运行 UI 契约。Expected: `P1=790–810`、`P2>=520`，四组位置断言均 PASS，状态标签不使用省略号截断。

---

### Task 2: 建立运行期临时快捷参数 API

**Files:**
- Modify: `tests/test_bot_management_operations_contract.ps1`
- Modify: `Server/BotManager.Management.cs`

**Interfaces:**
- Produces: `BotRuntimeQuickTuningTarget`、`BotRuntimeQuickTuningSnapshot`、`BotManager.AdjustRuntimeQuickTuning(BotRuntimeQuickTuningTarget target, int delta)`、`BotManager.GetRuntimeQuickTuningSnapshot()`、`BotManager.ResetRuntimeQuickTuning(string reason)`、`BotManager.CommitRuntimeQuickTuningBaseline()`。
- Consumes: 现有 `Config.BotAggressionPercent`、`Config.BotActivityPercent`、`Config.BotMinHealthPotionCount`、`Config.BotMinManaPotionCount` 和 `_managementSync`。

- [ ] **Step 1: 写运行期临时参数失败契约**

在 operations 契约中断言存在以下精确接口：

```powershell
Assert-Contains $management 'enum BotRuntimeQuickTuningTarget' 'quick tuning target enum exists'
Assert-Contains $management 'class BotRuntimeQuickTuningSnapshot' 'quick tuning snapshot exists'
Assert-Contains $management 'AdjustRuntimeQuickTuning\s*\(BotRuntimeQuickTuningTarget target, int delta\)' 'quick tuning adjust API exists'
Assert-Contains $management 'GetRuntimeQuickTuningSnapshot\s*\(' 'quick tuning snapshot API exists'
Assert-Contains $management 'ResetRuntimeQuickTuning\s*\(string reason\)' 'quick tuning reset API exists'
Assert-Contains $management 'CommitRuntimeQuickTuningBaseline\s*\(' 'quick tuning commit API exists'
```

增加反射测试：初始四项设为 `50/50/80/80`，依次调用攻击性 `+10`、活跃度 `-10`、药水 `+5`，断言运行值为 `60/40/85/85` 且 `Active=True`；调用 reset 后断言恢复 `50/50/80/80` 且 `Active=False`。再执行一次 reset，值不得变化。

- [ ] **Step 2: 运行 operations 契约确认 RED**

Run:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\tests\test_bot_management_operations_contract.ps1
```

Expected: FAIL，接口不存在。

- [ ] **Step 3: 定义目标枚举和只读快照**

在 `Server.Envir` 命名空间增加：

```csharp
public enum BotRuntimeQuickTuningTarget
{
    Aggression,
    Activity,
    PotionMinimums
}

public sealed class BotRuntimeQuickTuningSnapshot
{
    public bool Active { get; internal set; }
    public bool Changed { get; internal set; }
    public int AggressionPercent { get; internal set; }
    public int ActivityPercent { get; internal set; }
    public int MinHealthPotionCount { get; internal set; }
    public int MinManaPotionCount { get; internal set; }
    public string Message { get; internal set; }
}
```

- [ ] **Step 4: 实现捕获、调整、恢复和提交**

在 `BotManager` 内用 `_managementSync` 保护：

```csharp
private static bool _runtimeQuickTuningActive;
private static int _runtimeQuickBaseAggression;
private static int _runtimeQuickBaseActivity;
private static int _runtimeQuickBaseHealthPotions;
private static int _runtimeQuickBaseManaPotions;
```

实现精确签名：

```csharp
public static BotRuntimeQuickTuningSnapshot AdjustRuntimeQuickTuning(
    BotRuntimeQuickTuningTarget target, int delta)
public static BotRuntimeQuickTuningSnapshot GetRuntimeQuickTuningSnapshot()
public static bool ResetRuntimeQuickTuning(string reason)
public static void CommitRuntimeQuickTuningBaseline()
```

`AdjustRuntimeQuickTuning` 第一次调用时捕获基础值；攻击性/活跃度限制在 `0..100`，药水限制在 `0..10000`。只修改这四个运行期 `Config` 属性，不调用 `ConfigReader.Save()`。返回包含最终四项值和中文提示的快照，并写入 `RecordManagementLog(BotLogKind.Operation, message)`。到达边界时 `Changed=false`，提示明确写“已达到上限/下限”。`GetRuntimeQuickTuningSnapshot()` 在锁内返回复制值，不暴露可变内部状态。

`ResetRuntimeQuickTuning(reason)` 仅在 active 时恢复四项基础值、清除 active 并记录原因；重复调用返回 `false` 且不再次改变值。`CommitRuntimeQuickTuningBaseline()` 将当前四项视为新基础并清除 active，不回退值。

- [ ] **Step 5: 让明确保存升级基础值**

在 `TryApplyManagementSettings` 的 `settings.WriteToConfig()` 与成功持久化之后，仅当 `persist == true` 时调用内部无重复加锁版本的 commit。保存失败走现有回滚，不得清除临时基础快照。

- [ ] **Step 6: 运行 operations 契约确认 GREEN**

重新构建隔离产物并运行 operations 契约。Expected: 运行调整、边界、幂等恢复和保存升级基础值全部 PASS；契约同时断言临时调整方法体不含 `ConfigReader.Save()`。

---

### Task 3: 连接快捷按钮、日志和非阻塞面板提示

**Files:**
- Modify: `tests/test_bot_management_ui_contract.ps1`
- Modify: `Server/Views/BotConfigView.cs`

**Interfaces:**
- Consumes: Task 2 的 `AdjustRuntimeQuickTuning` 和 `BotRuntimeQuickTuningSnapshot`。
- Produces: `BotQuickActionStatusLabel`、`ApplyRuntimeQuickTuning(...)`、`RefreshRuntimeQuickTuningControls(...)`。

- [ ] **Step 1: 写快捷按钮失败契约**

增加源码与反射断言：六个按钮必须调用 `ApplyRuntimeQuickTuning`，方法体必须调用 `BotManager.AdjustRuntimeQuickTuning`，不得调用 `MessageBox.Show`，并必须更新 `BotQuickActionStatusLabel`。反射点击“攻击性 +10”后断言滑块和运行配置同时从 50 变为 60，提示包含 `60%`；点击“药水补给 +5”后 HP/MP 控件和运行配置同时变为 85。

- [ ] **Step 2: 运行 UI 契约确认 RED**

Run:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\tests\test_bot_management_ui_contract.ps1
```

Expected: FAIL；当前按钮委托仍只调用 `AdjustSlider`/`AdjustPotionMinimum`。

- [ ] **Step 3: 替换六个按钮委托**

按钮委托改为：

```csharp
delegate { ApplyRuntimeQuickTuning(BotRuntimeQuickTuningTarget.Aggression, 10); }
delegate { ApplyRuntimeQuickTuning(BotRuntimeQuickTuningTarget.Aggression, -10); }
delegate { ApplyRuntimeQuickTuning(BotRuntimeQuickTuningTarget.Activity, 10); }
delegate { ApplyRuntimeQuickTuning(BotRuntimeQuickTuningTarget.Activity, -10); }
delegate { ApplyRuntimeQuickTuning(BotRuntimeQuickTuningTarget.PotionMinimums, 5); }
delegate { ApplyRuntimeQuickTuning(BotRuntimeQuickTuningTarget.PotionMinimums, -5); }
```

`ApplyRuntimeQuickTuning` 调用 manager API，根据返回快照统一更新两个滑块、两个百分比标签、HP/MP 数值框和非阻塞状态标签。提示标签放在快捷操作组底部并占整行；成功、边界和失败均显示明确中文，不弹阻塞框。

调用 manager API 前读取 `GetManagementSnapshot().OnlineBotCount`；为 0 时不修改运行值，提示“当前没有在线假人，快捷调整未执行”，并写一条操作日志。这样系统停止时点击按钮不会留下无法自动清理的临时值。

- [ ] **Step 4: 同步外部恢复状态**

在现有一秒刷新中读取 `BotManager.GetRuntimeQuickTuningSnapshot()`。当 active 时显示“临时调整生效”；当 UI 观察到从 active 变为 inactive 时，仅刷新四个快捷相关控件和提示，不覆盖其他尚未保存的表单字段。

- [ ] **Step 5: 运行 UI 契约确认 GREEN**

重建后运行 UI 契约。Expected: 六个点击路径、即时运行值、无 MessageBox、日志/提示和四项控件同步全部 PASS。

---

### Task 4: 在停止和最后一名假人下线时清除临时值

**Files:**
- Modify: `tests/test_bot_management_runtime_contract.ps1`
- Modify: `Server/BotManager.cs`
- Modify: `Server/BotManager.Support.cs`

**Interfaces:**
- Consumes: Task 2 的 `ResetRuntimeQuickTuning(string reason)`。
- Produces: 两个生命周期重置调用点。

- [ ] **Step 1: 写生命周期失败契约**

提取 `BotManager.Stop` 和 `RemoveBotConnection` 方法块，断言：

```powershell
Assert-Contains $stopMethod 'ResetRuntimeQuickTuning\s*\(' 'Stop resets temporary quick tuning'
Assert-Contains $removeMethod 'botPlayers\.Count\s*==\s*0' 'disconnect checks last online bot'
Assert-Contains $removeMethod 'ResetRuntimeQuickTuning\s*\(' 'last disconnect resets temporary quick tuning'
```

并断言 reset 位于 `Stop` 设置 `isRunning=false` 后、异步下线清理前；`RemoveBotConnection` 只在移除玩家后且剩余数量为 0 时调用，不能在每个单独断线时无条件调用。

- [ ] **Step 2: 运行 runtime 契约确认 RED**

Run:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\tests\test_bot_management_runtime_contract.ps1
```

Expected: FAIL，两个生命周期调用点不存在。

- [ ] **Step 3: 增加两个最小重置调用点**

在 `Stop()` 将 `isRunning` 设为 false 后调用：

```csharp
ResetRuntimeQuickTuning("停止假人");
```

在 `RemoveBotConnection` 成功移除当前玩家、完成 `RemoveBotPlayer(player)` 后检查线程安全快照：

```csharp
if (SnapshotBotPlayers().Length == 0)
    ResetRuntimeQuickTuning("最后一名假人已下线");
```

不要在仍有在线假人时重置，不要改变现有断线清理顺序。

- [ ] **Step 4: 运行 runtime 与 operations 契约确认 GREEN**

Expected: 生命周期顺序、单人断线不重置、最后一人断线重置、重复重置幂等均 PASS。

---

### Task 5: 全量构建、运行验收与交付

**Files:**
- Verify: `tests/test_bot_management_*_contract.ps1`
- Create: `.artifacts/bot-management-wide-layout-ready/`

**Interfaces:**
- Consumes: Tasks 1–4 的最终源码。
- Produces: 正常 Fody 构建、运行证据和 SHA-256。

- [ ] **Step 1: 独立运行五组契约**

每个脚本必须使用独立 `powershell.exe`，因为脚本会设置进程退出码：

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\tests\test_bot_management_config_contract.ps1
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\tests\test_bot_management_runtime_contract.ps1
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\tests\test_bot_management_rewards_contract.ps1
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\tests\test_bot_management_operations_contract.ps1
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\tests\test_bot_management_ui_contract.ps1
```

Expected: 五组均退出码 0。

- [ ] **Step 2: 构建 ServerLibrary**

```powershell
dotnet build .\ServerLibrary\ServerLibrary.csproj -c Debug --no-restore
```

Expected: 0 errors。

- [ ] **Step 3: 正常 Fody 重建 Server**

```powershell
& 'C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\MSBuild\Current\Bin\MSBuild.exe' `
  '.\Server\Server.csproj' /t:Rebuild /p:Configuration=Debug /p:Platform=AnyCPU `
  "/p:OutDir=D:\相聚假人\Source\.artifacts\bot-management-wide-layout-ready\" /m /v:minimal
```

Expected: 0 errors；只允许现有 `MSB3277 System.Runtime.InteropServices.RuntimeInformation` 版本冲突警告。

- [ ] **Step 4: 运行时布局与点击验收**

使用 STA PowerShell 从新产物反射实例化 `BotConfigView`，将客户区设为 `1380x780`，确认：

```text
P1=790..810
P2>=520
左栏自动行为两列
右栏经济控制两列
快捷操作两列三行
等级切图四列两行
```

反射点击六个快捷按钮，确认运行值即时改变、提示更新、无阻塞弹窗；调用 reset 后恢复基础值；模拟 commit 后 reset 不回退。

- [ ] **Step 5: 短暂启动新产物**

从新输出目录隐藏启动 `Server.exe`，15 秒内确认进程未退出、窗口标题为“Z3服务端”且 `Responding=True`，随后仅停止该测试 PID，并确认没有残留 `Server` 进程。

- [ ] **Step 6: 交付报告**

报告：修改文件、RED/GREEN 证据、五组断言数、构建警告/错误数、反射布局尺寸、六个按钮运行值与恢复结果、窗口标题/响应状态、产物绝对路径与 SHA-256。明确未部署、未修改正式配置或正式进程；真实多假人在线下线顺序仍作为测试服 E2E 边界单独说明。
