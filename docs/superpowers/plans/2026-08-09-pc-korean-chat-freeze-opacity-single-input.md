# PC 韩版聊天卡死、背景透明度与输入框单层修正 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 以最小改动让韩版聊天背景按约 30% 透明真实绘制、输入框只绘制一套素材，并阻止无效按钮图片引发逐帧异常和客户端假死。

**Architecture:** 保留现有韩版聊天和滚动条结构。给 `DXWindow` 增加默认开启的窗口纹理绘制开关，仅韩版 `ChatTextBox` 关闭；给 `DXButton` 补齐与 `DXImageControl` 一致的空图片防护；显式启用韩版内容背景纹理绘制。

**Tech Stack:** C#、.NET Framework 4.8、WinForms、SharpDX Direct3D9、PowerShell 源码契约、Visual Studio 2022 Build Tools MSBuild。

## Global Constraints

- 仅修改 `145Client\Controls\DXButton.cs`、`145Client\Controls\DXWindow.cs`、`145Client\Scenes\Views\ChatDialog.Korean.cs`、`145Client\Scenes\Views\ChatTextBox.cs`。
- 不修改 145 界面、经验悬停、小地图、服务端、移动端、`Mir3.ini`、`.ZL` 资源、部署客户端或 `CHANGELOG.md`。
- `DXWindow` 新开关默认必须保持所有现有窗口继续绘制；仅韩版聊天输入框关闭。
- 韩版内容背景保持 `BackColour = Color.Black`、`Opacity = 0.7F`；四级高度、滚动条素材和交互不变。
- 生产源码修改前，在同目录创建后缀 `.bak-20260809-pc-korean-chat-freeze-opacity-single-input-01` 的精确备份并记录 SHA-256；若目标已存在则使用 `-02`，不得覆盖旧备份。
- 源树不是 Git 仓库，不创建 commit、branch 或 PR。

---

### Task 1: 建立失败契约并实施三项根因修正

**Files:**
- Create: `C:\Users\chen\Documents\Codex\2026-08-08\mir3-pc-dual-ui-luna\work\pc-korean-chat-freeze-opacity-single-input-contract.ps1`
- Modify: `145Client\Controls\DXButton.cs`
- Modify: `145Client\Controls\DXWindow.cs`
- Modify: `145Client\Scenes\Views\ChatDialog.Korean.cs`
- Modify: `145Client\Scenes\Views\ChatTextBox.cs`

**Interfaces:**
- Consumes: `MirLibrary.CreateImage(int, ImageType)` may return `null`; `DXWindow.DrawWindow()` is the standard window frame path; `GameScene.Game.KoreanInterface` identifies the Korean branch.
- Produces: `DXWindow.DrawWindowTexture` as a `bool` defaulting to `true`; Korean `ChatTextBox` sets it to `false`; `DXButton.DrawMirTexture()` safely returns on `image?.Image == null`.

- [ ] **Step 1: Write the focused failing contract**

Create a PowerShell contract that reads the four owned source files from `$env:PC_DUAL_SOURCE` and fails unless all of these source requirements exist:

```powershell
$window -match 'public\s+bool\s+DrawWindowTexture\s*=\s*true'
$window -match 'if\s*\(\s*!DrawWindowTexture\s*\|\|\s*InterfaceLibrary\s*==\s*null\s*\)\s*return'
$chatText -match 'DrawWindowTexture\s*=\s*false'
$chat -match 'KoreanTextBackground[\s\S]{0,300}DrawTexture\s*=\s*true[\s\S]{0,180}Opacity\s*=\s*0\.7F'
$button -match 'MirImage\s+image\s*=\s*Library\.CreateImage\(Index,\s*ImageType\.Image\);[\s\S]{0,100}if\s*\(\s*image\?\.Image\s*==\s*null\s*\)\s*return;[\s\S]{0,100}texture\s*=\s*image\.Image;'
```

The contract must also fail if Korean `ChatTextBox` removes `GameInter/3503`, changes its opacity away from `0.7F`, or changes `DXWindow.DrawWindowTexture` default away from `true`.

- [ ] **Step 2: Run the focused contract and verify RED**

Run:

```powershell
$env:PC_DUAL_SOURCE = 'D:\相聚假人\Source'
powershell.exe -NoProfile -ExecutionPolicy Bypass -File 'C:\Users\chen\Documents\Codex\2026-08-08\mir3-pc-dual-ui-luna\work\pc-korean-chat-freeze-opacity-single-input-contract.ps1'
```

Expected: exit code `1`, with failures for the missing background draw flag, Korean window-layer opt-out, and `DXButton` null-image guard.

- [ ] **Step 3: Back up the four production files**

Create exact same-directory backups before edits and verify each original/backup SHA-256 pair matches. Do not overwrite an existing backup.

- [ ] **Step 4: Add the minimal `DXButton` null-image guard**

In the existing library-backed branch of `DXButton.DrawMirTexture()`, use:

```csharp
MirImage image = Library.CreateImage(Index, ImageType.Image);
if (image?.Image == null) return;

texture = image.Image;
image.ExpireTime = CEnvir.Now + Config.CacheDuration;
```

Do not change button indices, input events, enabled state or drawing state restoration.

- [ ] **Step 5: Add the default-preserving `DXWindow` draw switch**

Add one public field alongside the window properties:

```csharp
public bool DrawWindowTexture = true;
```

Change only the first guard of `DrawWindow()`:

```csharp
if (!DrawWindowTexture || InterfaceLibrary == null) return;
```

Do not change `Draw()`, `DrawEdges()` or existing window layout logic.

- [ ] **Step 6: Apply the Korean-only single-layer and background fixes**

In `ChatDialog.Korean.cs`, add exactly `DrawTexture = true` to `KoreanTextBackground`, retaining black and `0.7F`.

In the Korean branch of the `ChatTextBox` constructor, set:

```csharp
DrawWindowTexture = false;
```

Retain `Background` as the only `GameInter/3503` input backdrop and retain its `ImageOpacity = 0.7F`.

- [ ] **Step 7: Run focused GREEN and all regressions**

Run the new focused contract, then these existing contracts with the same `PC_DUAL_SOURCE` environment variable:

```powershell
pc-korean-chat-single-layer-scroll-contract.ps1
pc-korean-experience-hover-contract.ps1
pc-korean-chat-resize-cycle-contract.ps1
pc-korean-original-ui-contract.ps1
korean-core-hud-contract.ps1
pc-dual-ui-contract.ps1
```

Expected: all seven contracts exit `0` and print GREEN/PASS.

- [ ] **Step 8: Perform an isolated Release rebuild**

Run:

```powershell
& 'C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\MSBuild\Current\Bin\MSBuild.exe' `
  'D:\相聚假人\Source\145Client\145Client.csproj' `
  /t:Rebuild /m:1 /nr:false /v:minimal `
  /p:Configuration=Release /p:Platform=AnyCPU `
  /p:OutputPath='D:\相聚假人\Source\.build-check\pc-korean-chat-freeze-opacity-single-input-luna\' `
  /p:RestorePackages=false
```

Expected: exit `0`, 0 errors; only the existing `BigPatchConfig.cs` `CS0649` warning may remain. Report output path, byte length and SHA-256.

- [ ] **Step 9: Report without deployment**

Return exact changed files, concise diff summary, RED/GREEN outputs, backup paths and hashes, build output/hash, unchanged scope, and the remaining Direct3D manual checks. Do not deploy or modify `CHANGELOG.md`.
