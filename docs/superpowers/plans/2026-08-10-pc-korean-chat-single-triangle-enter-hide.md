# PC 韩版聊天单三角与回车隐藏 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 韩版聊天只保留输入框右侧三角，按 `218px（▼）→ 166px（▼）→ 118px（▼）→ 隐藏（▲）→ 218px（▼）` 循环，并让输入框第二次回车后隐藏且不再绘制 `3503` 阴影层。

**Architecture:** 继续复用现有 `KoreanChatResizeLevel` 状态机，只缩减可见高度数组并移除韩版重复按钮实例；`ChatTextBox.ChangeButton` 成为鼠标和聊天窗口快捷键的唯一入口。回车显示由 `GameScene` 处理，第二次回车后的隐藏由 `ChatTextBox` 处理，所有新行为均受 `KoreanInterface` 保护。

**Tech Stack:** C# / .NET Framework / DirectX UI，PowerShell 静态契约，VS 2022 MSBuild。

## Global Constraints

- 仅修改 PC 韩版分支；145 界面行为和布局保持原样。
- 高度循环必须严格为 `218（▼）→ 166（▼）→ 118（▼）→ 隐藏（▲）→ 218（▼）`。
- 第一次回车显示并聚焦输入框，第二次回车沿用发送逻辑后隐藏输入框；空文本也隐藏。
- 不修改 `GameInter.Zl`，通过不绘制 `GameInter:3503` 背景层去除阴影。
- 不重复创建备份；部署只覆盖 `Mir3.exe`，不改 `Mir3.ini`。
- 项目不是 Git 仓库，不创建提交或 PR。

---

### Task 1: 建立韩版聊天行为失败契约

**Files:**
- Create: `C:\Users\chen\Documents\Codex\2026-08-08\mir3-pc-dual-ui-luna\work\pc-korean-chat-single-triangle-enter-hide-contract.ps1`
- Read: `145Client\Scenes\Views\ChatDialog.Korean.cs`
- Read: `145Client\Scenes\Views\ChatTextBox.cs`
- Read: `145Client\Scenes\GameScene.cs`

**Interfaces:**
- Consumes: `KoreanChatHeights`, `KoreanChatResizeLevel`, `CycleKoreanChatSize()`, `SyncKoreanTriangle()`, `ChatTextBox.ChangeButton`。
- Produces: 一个只读源码契约，覆盖三档状态、单三角、回车隐藏、回车恢复和阴影关闭。

- [ ] **Step 1: 写入失败契约**

契约必须读取上述三份源码并检查：

```powershell
Require-Match 'three visible heights' $chat 'KoreanChatHeights\s*=\s*\{\s*218,\s*166,\s*118\s*\}'
Require-Match 'initial level is maximum' $chat 'KoreanChatResizeLevel\s*=\s*0\s*;'
Forbid-Match 'no duplicate Korean triangles' $chat 'ExpendButton\s*=\s*CreateKoreanChatWindowButton|ShrinkButton\s*=\s*CreateKoreanChatWindowButton'
Require-Match 'down while visible and up while hidden' $chat 'changeButton\.Index\s*=\s*hidden\s*\?\s*3542\s*:\s*3552'
Require-Match '3503 layer is not drawn' $chatText 'Index\s*=\s*3503[\s\S]{0,260}?Visible\s*=\s*false'
Require-Match 'second Enter hides Korean input' $chatText 'DXTextBox\.ActiveTextBox\s*=\s*null;[\s\S]{0,220}?KoreanInterface[\s\S]{0,100}?Visible\s*=\s*false'
Require-Match 'hidden Korean input reopens on Enter' $gameScene 'e\.KeyCode\s*==\s*Keys\.Enter\s*&&\s*KoreanInterface\s*&&\s*!ChatTextBox\.Visible[\s\S]{0,180}?ChatTextBox\.Visible\s*=\s*true[\s\S]{0,120}?ChatTextBox\.OpenChat'
Require-Match 'Korean hotkey uses sole triangle' $gameScene 'case\s+KeyBindAction\.ChatWindow:[\s\S]{0,220}?KoreanInterface[\s\S]{0,120}?ChatTextBox\.ChangeButton\.InvokeMouseClick'
Require-Match '145 hotkey path retained' $gameScene 'else[\s\S]{0,220}?ChatBox\.ShrinkButton\.Visible[\s\S]{0,260}?ChatBox\.ExpendButton\.InvokeMouseClick'
```

- [ ] **Step 2: 运行契约确认 RED**

Run:

```powershell
$env:PC_DUAL_SOURCE='D:\相聚假人\Source'
powershell.exe -NoProfile -ExecutionPolicy Bypass -File 'C:\Users\chen\Documents\Codex\2026-08-08\mir3-pc-dual-ui-luna\work\pc-korean-chat-single-triangle-enter-hide-contract.ps1'
```

Expected: exit `1`，失败项至少包含三档高度、重复三角、回车隐藏/恢复和 3503 不绘制。

---

### Task 2: 最小实现单一三角与回车状态流

**Files:**
- Modify: `145Client\Scenes\Views\ChatDialog.Korean.cs`
- Modify: `145Client\Scenes\Views\ChatTextBox.cs`
- Modify: `145Client\Scenes\GameScene.cs`
- Test: `C:\Users\chen\Documents\Codex\2026-08-08\mir3-pc-dual-ui-luna\work\pc-korean-chat-single-triangle-enter-hide-contract.ps1`

**Interfaces:**
- Consumes: 现有 `ChangeButton.MouseClick → CycleKoreanChatSize()` 调用链。
- Produces: `ChangeButton` 唯一控制三档/隐藏状态；韩版回车显示/隐藏闭环；145 原路径保留。

- [ ] **Step 1: 修改韩版聊天记录状态机**

在 `ChatDialog.Korean.cs` 使用：

```csharp
private static readonly int[] KoreanChatHeights = { 218, 166, 118 };
private static readonly int[] KoreanChatLineCounts = { 11, 7, 4 };
private int KoreanChatResizeLevel = 0;
```

删除韩版 `ExpendButton/ShrinkButton` 的创建块和已不再使用的 `CreateKoreanChatWindowButton()`。保留现有 `CycleKoreanChatSize()` 的越界隐藏、隐藏后索引归零恢复，以及 `3542/3552` 方向同步。

- [ ] **Step 2: 去掉输入阴影并在第二次回车隐藏韩版输入框**

在 `ChatTextBox.cs` 的韩版 `Background` 初始化中加入：

```csharp
Visible = false,
```

把 Enter 结束输入后的可见性规则改为：

```csharp
DXTextBox.ActiveTextBox = null;
if (GameScene.Game?.KoreanInterface == true)
{
    Visible = false;
}
else if (!GameScene.Game.ChatBox.Visible)
{
    Visible = false;
}
```

发送、清空、私聊记录和 145 条件不改。

- [ ] **Step 3: 接通隐藏输入框的回车恢复和聊天窗口快捷键**

在 `GameScene.cs` 的 Enter 分支中，于原 `else if (!ChatBox.Visible)` 之前加入：

```csharp
else if (e.KeyCode == Keys.Enter && KoreanInterface && !ChatTextBox.Visible)
{
    ChatTextBox.Visible = true;
    ChatTextBox.OpenChat();
}
```

在 `KeyBindAction.ChatWindow` 中使用：

```csharp
if (KoreanInterface)
{
    ChatTextBox.ChangeButton.InvokeMouseClick();
}
else if (ChatBox.ShrinkButton.Visible == false)
{
    ChatBox.ExpendButton.InvokeMouseClick();
}
else
{
    ChatBox.ShrinkButton.InvokeMouseClick();
}
```

- [ ] **Step 4: 运行聚焦契约确认 GREEN**

Run: Task 1 Step 2 的命令。

Expected: exit `0`，输出 `GREEN`。

- [ ] **Step 5: 更新被新规格取代的旧契约**

只把旧契约中的 `{268,218,166,118}`、默认索引 `2`、韩版重复三角存在和 `3503` 必须可见等断言更新为本规格；不得删除 145 隔离、滚动条、透明度、位置和怪物窗口断言。

- [ ] **Step 6: 运行全部源码契约**

Run:

```powershell
$work='C:\Users\chen\Documents\Codex\2026-08-08\mir3-pc-dual-ui-luna\work'
$env:PC_DUAL_SOURCE='D:\相聚假人\Source'
Get-ChildItem $work -Filter '*.ps1' |
  Where-Object { $_.Name -notmatch 'config-reader-contract\.ps1$' } |
  ForEach-Object { & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $_.FullName; if ($LASTEXITCODE) { throw $_.Name } }
```

Expected: 每个源码契约 exit `0`。

---

### Task 3: 构建、部署与记录

**Files:**
- Build output: `D:\Client\Mir3.exe`
- Deploy: `D:\Debug\4月18日更新\Client\Mir3.exe`
- Preserve: `D:\Debug\4月18日更新\Client\Mir3.ini`
- Modify: `CHANGELOG.md`

**Interfaces:**
- Consumes: Task 2 全绿源码状态。
- Produces: 可手动验证的正式 PC 客户端和可回溯更新记录。

- [ ] **Step 1: Release 重编译**

Run:

```powershell
& 'C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\MSBuild\Current\Bin\MSBuild.exe' `
  'D:\相聚假人\Source\145Client\145Client.csproj' /t:Rebuild /m /v:minimal `
  /p:Configuration=Release /p:Platform=AnyCPU
```

Expected: exit `0`、0 errors；仅允许现有 `BigPatchConfig.ChkLockMonEffect` CS0649 warning。

- [ ] **Step 2: 运行配置产物契约**

```powershell
$env:PC_DUAL_OUTPUT='D:\Client'
powershell.exe -NoProfile -ExecutionPolicy Bypass -File 'C:\Users\chen\Documents\Codex\2026-08-08\mir3-pc-dual-ui-luna\work\config-reader-contract.ps1'
```

Expected: exit `0`，输出 `GREEN`。

- [ ] **Step 3: 覆盖正式客户端**

确认没有 `Mir3` 进程；记录正式 `Mir3.ini` 哈希；只把 `D:\Client\Mir3.exe` 覆盖到正式目录；确认源/目标 exe 哈希相同且 ini 前后哈希相同。不创建备份。

- [ ] **Step 4: 更新并验证 CHANGELOG**

记录三档循环、单三角、两次回车、3503 阴影关闭、修改文件、契约结果、构建结果、部署哈希和 ini 前后哈希。使用 UTF-8 读取检查新条目位于顶部。

- [ ] **Step 5: 实机交接**

要求用户验证：`218 → 166 → 118 → 隐藏 → 218`、按钮方向、第一次/第二次回车、阴影消失，以及 145 界面未变。
