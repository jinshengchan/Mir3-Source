# PC 韩版聊天复合素材去重、按钮定位与动态提示 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 只调整韩版聊天组合层，让顶部和底部各只显示一套控件，关闭按钮完整靠右且可点击，底部三角提示随缩小、隐藏和展开状态变化。

**Architecture:** 保留现有 `GameInter` 复合素材和全部聊天业务。通过 `FixedSize` 裁掉 `3500` 从 `Y=27` 开始的重复控制区，让现有独立滚动条接管该位置；把独立 `3542/3552` 精确覆盖到 `3503` 内嵌按钮坐标；仅韩版 `ChatDialog` 关闭通用窗口纹理层并重新置顶关闭按钮。

**Tech Stack:** C#、.NET Framework 4.8、WinForms、SharpDX Direct3D9、GameInter.ZL、PowerShell 源码契约、Visual Studio 2022 Build Tools MSBuild。

## Global Constraints

- 设计依据：`docs\superpowers\specs\2026-08-09-pc-korean-chat-composite-control-dedup-design.md`。
- 生产源码只允许修改 `145Client\Scenes\Views\ChatDialog.Korean.cs` 和 `145Client\Scenes\Views\ChatTextBox.cs`。
- 不修改 `DXButton`、`DXWindow`、`DXVScrollBar` 的通用实现；复用已存在且默认开启的 `DXWindow.DrawWindowTexture`。
- 不修改四级高度 `268、218、168、118`、可见行数 `14、11、7、4`、频道过滤、输入发送、物品链接、滚轮、拖动和轨道点击。
- 不修改 145 界面、经验悬停、小地图、主面板、服务端、移动端、`Mir3.ini` 或任何 `.ZL` 资源。
- 修改源码前创建唯一 sibling 备份，首选后缀 `.bak-20260809-pc-korean-chat-composite-control-dedup-01`；存在时使用 `-02`，禁止覆盖旧备份，并记录 SHA-256。
- 源树不是 Git 仓库；不要初始化 Git，不创建 commit、branch 或 PR。
- Luna 任务只修改源码、外部契约和隔离构建目录；不部署客户端，不修改 `CHANGELOG.md`。

---

### Task 1: 建立能够捕获本次真实视觉结构的 RED 契约

**Files:**
- Create: `C:\Users\chen\Documents\Codex\2026-08-08\mir3-pc-dual-ui-luna\work\pc-korean-chat-composite-control-dedup-contract.ps1`
- Read: `145Client\Scenes\Views\ChatDialog.Korean.cs`
- Read: `145Client\Scenes\Views\ChatTextBox.cs`

**Interfaces:**
- Consumes: 环境变量 `PC_DUAL_SOURCE`；缺失时回退到 `D:\相聚假人\Source`。
- Produces: 退出码 `1` 和 `RED:` 缺口列表，或退出码 `0` 和 `GREEN: Korean composite chat control dedup contract passed.`。

- [ ] **Step 1: 写入聚焦契约**

契约读取两个生产源码文件并逐项要求：

```powershell
# ChatDialog.Korean.cs
# BuildKoreanInterface() 设置 DrawWindowTexture = false。
# ChatPanel 仍使用 GameInter/3500，但 Size = new Size(380, 27) 且 FixedSize = true。
# KoreanTextBackground 使用 Y=27，并在 ApplyKoreanChatSize() 中使用 height - 27。
# TextPanel 使用 Y=31，并在 ApplyKoreanChatSize() 中使用 height - 32。
# ScrollBar 使用 Y=27，并在 ApplyKoreanChatSize() 中使用 height - 27。
# 每次 ApplyKoreanChatSize() 后 CloseButton.Location = new Point(364, 5)，随后 CloseButton.BringToFront()。
# SyncKoreanTriangle() 保持可见 3552、隐藏 3542，并分别产生“缩小聊天框”“隐藏聊天框”“展开聊天框”。

# ChatTextBox.cs
# ChangeButton 仍调用 CycleKoreanChatSize()。
# ChangeButton.Location = new Point(356, 8)，完成定位后调用 ChangeButton.BringToFront()。
# 初始 Hint 不再是“切换聊天框”，而是“缩小聊天框”。
# Background 仍使用 GameInter/3503、Size 380x25、FixedSize=true、ImageOpacity=0.7F。
```

契约同时要求四级高度数组、滚动条 `3561/3562/3560`、`DXWindow.DrawWindowTexture` 默认 `true` 保持不变。

- [ ] **Step 2: 运行契约并确认 RED**

Run:

```powershell
$env:PC_DUAL_SOURCE = 'D:\相聚假人\Source'
powershell.exe -NoProfile -ExecutionPolicy Bypass -File 'C:\Users\chen\Documents\Codex\2026-08-08\mir3-pc-dual-ui-luna\work\pc-korean-chat-composite-control-dedup-contract.ps1'
```

Expected: exit `1`，至少报告未裁切 3500、ChatDialog 未关闭通用窗口层、底部按钮坐标不匹配、动态提示缺失、关闭按钮未置顶；不得因脚本语法或路径错误而失败。

---

### Task 2: 修正韩版 ChatDialog 顶部复合下段、窗口层和关闭按钮

**Files:**
- Modify: `145Client\Scenes\Views\ChatDialog.Korean.cs:18-235`
- Backup: `145Client\Scenes\Views\ChatDialog.Korean.cs.bak-20260809-pc-korean-chat-composite-control-dedup-01`
- Test: `C:\Users\chen\Documents\Codex\2026-08-08\mir3-pc-dual-ui-luna\work\pc-korean-chat-composite-control-dedup-contract.ps1`

**Interfaces:**
- Consumes: 已有 `DXWindow.DrawWindowTexture`、`DXControl.BringToFront()`、`CycleKoreanChatSize()` 和 `SyncKoreanTriangle()`。
- Produces: 韩版 27 像素标题层、从 Y=27 开始的唯一滚动区、固定右上关闭按钮和状态相关提示。

- [ ] **Step 1: 创建并校验源码备份**

若 `-01` 不存在则复制当前文件到 `-01`，否则使用 `-02`。复制前记录当前 SHA-256，复制后要求备份哈希完全相同；不允许覆盖。

- [ ] **Step 2: 关闭韩版 ChatDialog 的通用窗口纹理层**

在 `BuildKoreanInterface()` 的韩版初始化路径设置：

```csharp
DrawWindowTexture = false;
```

不改变 `DXWindow.DrawWindowTexture` 的默认值或 145 构造路径。

- [ ] **Step 3: 将顶部复合素材限制为唯一标题层**

保留 `LibraryFile.GameInter` 和 `Index = 3500`，将 `ChatPanel` 初始化改为：

```csharp
Size = new Size(380, 27),
FixedSize = true,
```

`FixedSize = true` 是必须条件；否则 `DXImageControl.Size` 会继续返回素材原始 `380×48`。

- [ ] **Step 4: 把消息背景、文字区和滚动条上移到标题下方**

初始化值与 `ApplyKoreanChatSize()` 的动态值必须一致：

```csharp
KoreanTextBackground.Location = new Point(0, 27);
KoreanTextBackground.Size = new Size(380, height - 27);

TextPanel.Location = new Point(8, 31);
TextPanel.Size = new Size(350, height - 32);

ScrollBar.Location = new Point(360, 27);
ScrollBar.Size = new Size(16, height - 27);
```

保留 `ScrollBar.UpButton.Location = new Point(0, 2)`、素材 `3561/3562/3560`、位置条偏移 2、轨道扣减 40 和可见行数数组 `14/11/7/4`。

- [ ] **Step 5: 每次布局后固定并置顶关闭按钮**

在 `ApplyKoreanChatSize()` 完成尺寸和子控件布局后执行：

```csharp
CloseButton.Location = new Point(364, 5);
CloseButton.BringToFront();
```

这样可抵消 `DXWindow.OnSizeChanged()` 的通用坐标重置，并避免后创建素材遮挡。

- [ ] **Step 6: 动态更新底部三角提示**

在 `SyncKoreanTriangle()` 中用现有高度/级别状态统一更新索引和提示：

```csharp
DXButton changeButton = GameScene.Game?.ChatTextBox?.ChangeButton;
if (changeButton == null) return;

bool hidden = height == 0;
changeButton.Index = hidden ? 3542 : 3552;
changeButton.Hint = hidden
    ? "展开聊天框".Lang()
    : KoreanChatResizeLevel == KoreanChatHeights.Length - 1
        ? "隐藏聊天框".Lang()
        : "缩小聊天框".Lang();
```

局部变量只引用当前实际字段 `GameScene.Game.ChatTextBox.ChangeButton`，不要引入新的持久状态字段。

---

### Task 3: 将底部独立按钮精确覆盖 3503 内嵌按钮

**Files:**
- Modify: `145Client\Scenes\Views\ChatTextBox.cs:175-235`
- Backup: `145Client\Scenes\Views\ChatTextBox.cs.bak-20260809-pc-korean-chat-composite-control-dedup-01`
- Test: `C:\Users\chen\Documents\Codex\2026-08-08\mir3-pc-dual-ui-luna\work\pc-korean-chat-composite-control-dedup-contract.ps1`

**Interfaces:**
- Consumes: `GameInter/3503` 内嵌按钮像素坐标 `(356,8)`；独立 `3542/3552` 尺寸 `20×18`。
- Produces: 一个完整可点击、可动态换向且始终位于最上层的底部三角按钮。

- [ ] **Step 1: 创建并校验源码备份**

按 Task 2 相同规则创建唯一 sibling 备份并完成修改前/备份 SHA-256 配对校验。

- [ ] **Step 2: 修正初始提示**

把韩版 `ChangeButton` 的初始化提示由：

```csharp
Hint = "切换聊天框".Lang(),
```

改为：

```csharp
Hint = "缩小聊天框".Lang(),
```

- [ ] **Step 3: 使用素材内嵌按钮的精确位置并置顶**

韩版子控件完成定位后，不再使用基于 `ClientArea` 的旧按钮坐标，改为：

```csharp
ChangeButton.Location = new Point(356, 8);
ChangeButton.BringToFront();
```

保留 `Background` 的 `GameInter/3503`、`380×25`、`FixedSize = true` 和 `ImageOpacity = 0.7F`；保留点击调用 `CycleKoreanChatSize()`。

- [ ] **Step 4: 运行聚焦契约并确认 GREEN**

Run: Task 1 的相同命令。

Expected: exit `0`，输出 `GREEN: Korean composite chat control dedup contract passed.`。

---

### Task 4: 回归契约、差异审计和 Luna Release 构建

**Files:**
- Read: 两个本轮源码及其唯一备份
- Build output: `D:\相聚假人\Source\.build-check\pc-korean-chat-composite-control-dedup-luna\`

**Interfaces:**
- Consumes: Tasks 1-3 的 GREEN 源码状态。
- Produces: 完整契约结果、两文件精确 diff、Release `Mir3.exe` 及 SHA-256。

- [ ] **Step 1: 重跑全部八项契约**

依次运行：

```text
pc-korean-chat-composite-control-dedup-contract.ps1
pc-korean-chat-freeze-opacity-single-input-contract.ps1
pc-korean-chat-single-layer-scroll-contract.ps1
pc-korean-experience-hover-contract.ps1
pc-korean-chat-resize-cycle-contract.ps1
pc-korean-original-ui-contract.ps1
korean-core-hud-contract.ps1
pc-dual-ui-contract.ps1
```

Expected: 八项均退出 `0` 并输出 GREEN。若旧契约因本次已批准的 `Y=27` 新布局而失败，只允许最小更新该外部契约的对应旧坐标断言，并必须先说明冲突；不得放宽四级高度、索引、交互或 145 保护断言。

- [ ] **Step 2: 执行 Release Rebuild**

Run:

```powershell
& 'C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\MSBuild\Current\Bin\MSBuild.exe' `
  'D:\相聚假人\Source\145Client\145Client.csproj' `
  /t:Rebuild /m /v:minimal `
  /p:Configuration=Release /p:Platform=AnyCPU `
  /p:OutDir='D:\相聚假人\Source\.build-check\pc-korean-chat-composite-control-dedup-luna\'
```

Expected: exit `0`，0 errors；允许保留一个既有 `BigPatchConfig.ChkLockMonEffect` `CS0649` warning。报告 `Mir3.exe` 的路径、字节数、时间和 SHA-256。

- [ ] **Step 3: 审计实际差异和保护范围**

使用 `git diff --no-index`（源树本身非 Git）分别比较两个源码与本轮备份。只允许出现：韩版窗口层关闭、3500 固定 27 高、Y=27/31 布局、关闭按钮坐标/置顶、动态提示、底部 `(356,8)`/置顶。报告未修改 `DXButton.cs`、`DXWindow.cs`、`DXVScrollBar.cs`、145 分支、资源、配置、服务端、移动端、部署目录和 `CHANGELOG.md`。

---

### Task 5: 主任务独立验收、备份部署与日志

**Owner:** Primary task only; Luna must not perform this task.

**Files:**
- Build output: 新的主任务隔离目录，不复用 Luna 输出目录
- Deploy: `D:\Debug\4月18日更新\Client\Mir3.exe`
- Preserve: `D:\Debug\4月18日更新\Client\Mir3.ini`
- Modify: `CHANGELOG.md`

- [ ] **Step 1: 主任务检查 Luna 实际 diff 并重跑八项契约**

必须读取同一 Luna 任务最终交接，逐文件相对备份检查实际差异，并在主任务重新运行全部八项契约。

- [ ] **Step 2: 主任务使用新目录独立 Release Rebuild**

使用与 Task 4 相同的 MSBuild 参数，但输出到新的、此前不存在的 parent 目录。要求退出 `0`、0 errors，并记录产物 SHA-256。

- [ ] **Step 3: 备份并部署**

确认目标路径的 `Mir3.exe` 进程未运行。为当前部署文件和 `CHANGELOG.md` 创建唯一且 SHA 配对一致的覆盖前备份，再复制主任务构建产物覆盖 `D:\Debug\4月18日更新\Client\Mir3.exe`。部署后要求目标 SHA-256 与主任务产物完全一致。

- [ ] **Step 4: 更新日志并完成部署后验证**

使用 `apply_patch` 向 `CHANGELOG.md` 追加本轮根因、两文件改动、源码/部署备份、八项契约、构建、目标哈希和人工验证缺口。再次确认 `Mir3.ini` SHA-256 与部署前一致。

- [ ] **Step 5: 用户 Direct3D 实机验收**

验证：顶部无复合下段双层，仅一个滚动条上箭头；底部仅一个三角按钮；四级缩小/隐藏/恢复正常；关闭按钮完整靠右且可点击；提示依次为“缩小聊天框”“隐藏聊天框”“展开聊天框”；客户端不再产生新的逐帧按钮异常。
