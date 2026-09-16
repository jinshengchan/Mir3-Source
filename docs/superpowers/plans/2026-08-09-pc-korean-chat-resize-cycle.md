# PC Korean Chat Resize Cycle Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the Korean chat input triangle exclusively cycle through three progressively smaller visible chat heights, then hide the chat, then restore the maximum height, while keeping the scrollbar proportional and the chat background about 30% opaque.

**Architecture:** Keep the current shared chat model, history, filtering, input, links and scrolling. Add one Korean-only resize level and one centralized layout method in `ChatDialog.Korean.cs`; route the existing bottom `ChatTextBox.ChangeButton` to that method and leave the shared 145 branch untouched.

**Tech Stack:** C#/.NET Framework, existing `DXControl`/`DXImageControl`/`DXVScrollBar`, PowerShell source contracts, VS 2022 MSBuild.

## Global Constraints

- Visible state sequence is exactly: height 268 → 218 → 168 → 118 → hidden.
- The bottom triangle is `GameInter/3552` (down) for every visible state and `GameInter/3542` (up) while hidden.
- Clicking the up triangle while hidden restores height 268 and changes it back to down.
- The input bar stays visible while the chat history window is hidden.
- The top duplicate expand/shrink controls are not visible or clickable in Korean mode.
- The right scrollbar height and visible-row count change at every visible level; its current message range and scroll behavior remain shared.
- Only backgrounds are about 30% opaque; text, tabs, borders, buttons and scrollbar remain fully legible.
- Do not modify the 145 branch, minimap, server, mobile projects, `Mir3.ini`, deployed files or `.ZL` resources.
- The source tree is non-Git. Do not initialize Git, commit, push or create a PR.

---

### Task 1: Korean chat four-level resize cycle

**Files:**
- Modify: `145Client/Scenes/Views/ChatDialog.Korean.cs`
- Modify: `145Client/Scenes/Views/ChatTextBox.cs`
- Test: `C:/Users/chen/Documents/Codex/2026-08-08/mir3-pc-dual-ui-luna/work/pc-korean-chat-resize-cycle-contract.ps1`
- Verify: `C:/Users/chen/Documents/Codex/2026-08-08/mir3-pc-dual-ui-luna/work/pc-korean-original-ui-contract.ps1`
- Verify: `C:/Users/chen/Documents/Codex/2026-08-08/mir3-pc-dual-ui-luna/work/korean-core-hud-contract.ps1`
- Verify: `C:/Users/chen/Documents/Codex/2026-08-08/mir3-pc-dual-ui-luna/work/pc-dual-ui-contract.ps1`

**Interfaces:**
- Consumes: `ChatDialog.TextPanel`, `ScrollBar`, `ChatPanel`, `KoreanInputPanel`, `ChatTextBox.ChangeButton`, `ChatDialog.Update()`.
- Produces: `public void CycleKoreanChatSize()` as the sole Korean size/hide entry point.
- Produces: a Korean-only `ApplyKoreanChatSize()` method that updates size, bottom anchoring, content background, scroll track, visible rows and triangle direction together.

- [ ] **Step 1: Back up both production source files**

Create unique sibling backups before either edit:

```text
ChatDialog.Korean.cs.bak-20260809-pc-korean-chat-resize-cycle-01
ChatTextBox.cs.bak-20260809-pc-korean-chat-resize-cycle-01
```

Verify each backup SHA-256 equals its source before modification. Do not overwrite an existing backup.

- [ ] **Step 2: Write the failing source contract**

Create the external PowerShell contract with assertions that fail against the current duplicate two-button implementation and require all of the following:

```powershell
# Required source-level contract facts:
# - ChatTextBox.ChangeButton calls CycleKoreanChatSize().
# - Korean visible heights are exactly 268, 218, 168, 118.
# - the next state hides ChatDialog; hidden-click restores level 0.
# - visible states use index 3552; hidden uses 3542.
# - ExpendButton and ShrinkButton are hidden in Korean construction and have no Korean MouseClick resize handlers.
# - TextPanel, scrollbar and background heights derive from the same selected height.
# - background controls use 0.3F opacity; the parent ChatDialog and message labels do not.
# - no 145 constructor branch is changed by this contract fix.
```

- [ ] **Step 3: Run the contract and capture RED**

Run:

```powershell
$env:PC_DUAL_SOURCE='D:\相聚假人\Source'
powershell.exe -NoProfile -ExecutionPolicy Bypass -File 'C:\Users\chen\Documents\Codex\2026-08-08\mir3-pc-dual-ui-luna\work\pc-korean-chat-resize-cycle-contract.ps1'
```

Expected: exit `1`, specifically reporting the duplicated expand/shrink route and missing four-level/hidden state cycle.

- [ ] **Step 4: Add the minimal Korean-only state and centralized layout**

In `ChatDialog.Korean.cs`, add a resize level with exact visible heights and a content background field. Use one method shaped like this, adapted to the existing control API without changing shared message behavior:

```csharp
private static readonly int[] KoreanChatHeights = { 268, 218, 168, 118 };
private int KoreanChatResizeLevel;
private DXControl KoreanTextBackground;

public void CycleKoreanChatSize()
{
    if (!Visible || KoreanChatResizeLevel >= KoreanChatHeights.Length)
    {
        KoreanChatResizeLevel = 0;
        Visible = true;
    }
    else
    {
        KoreanChatResizeLevel++;
        if (KoreanChatResizeLevel >= KoreanChatHeights.Length)
        {
            Visible = false;
            SyncKoreanTriangle();
            return;
        }
    }

    ApplyKoreanChatSize();
}
```

`ApplyKoreanChatSize()` must use the selected height as the single source of truth:

```csharp
int height = KoreanChatHeights[KoreanChatResizeLevel];
Size = new Size(380, height);
KoreanInputPanel.Location = new Point(0, height - 20);
KoreanTextBackground.Location = new Point(0, 48);
KoreanTextBackground.Size = new Size(380, height - 68);
TextPanel.Location = new Point(8, 52);
TextPanel.Size = new Size(350, height - 73);
ScrollBar.Location = new Point(360, 50);
ScrollBar.Size = new Size(16, height - 72);
LineCount = Math.Max(1, TextPanel.Size.Height / 15);
ScrollBar.VisibleSize = LineCount;
Location = new Point(GameScene.Game.ChatTextBox.Location.X,
    GameScene.Game.ChatTextBox.Location.Y - height);
```

After layout changes, clamp through the existing `Update()` path so messages and the scrollbar remain usable. Keep `ExpendButton` and `ShrinkButton` instantiated only if shared disposal/field compatibility requires them, but set them hidden and do not attach Korean resize click handlers.

- [ ] **Step 5: Route the bottom triangle and synchronize close/hide state**

In the Korean branch of `ChatTextBox.cs`, replace the current `ChangeButton` handler that invokes `ExpendButton`/`ShrinkButton` with:

```csharp
ChangeButton.MouseClick += (o, e) => GameScene.Game.ChatBox.CycleKoreanChatSize();
```

For Korean mode, visible chat states use `ChangeButton.Index = 3552`; hidden chat uses `3542`. Closing the chat with its existing X must also put the state into hidden/up-triangle mode, while showing it again through the bottom triangle restores the maximum height.

- [ ] **Step 6: Apply background-only 30% opacity**

Set `ImageOpacity = 0.3F` on Korean background images (`ChatPanel`, `KoreanInputPanel`, and any retained image background). Use a black `DXControl` behind the message area with `Opacity = 0.3F`. Do not set the containing `ChatDialog` opacity to `0.3F`, and do not change label/button/scrollbar opacity.

- [ ] **Step 7: Run focused GREEN and regression contracts**

Run the new contract and then all three existing contracts with `PC_DUAL_SOURCE=D:\相聚假人\Source`.

Expected:

```text
GREEN: Korean chat resize cycle contract passed.
GREEN: Korean original UI contract passed.
GREEN: Korean core HUD/chat contract passed.
GREEN: PC dual-interface source contract passed.
```

- [ ] **Step 8: Release rebuild**

Run:

```powershell
& 'C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\MSBuild\Current\Bin\MSBuild.exe' `
  'D:\相聚假人\Source\145Client\145Client.csproj' `
  /t:Rebuild /m:1 /nr:false /v:minimal `
  /p:Configuration=Release /p:Platform=AnyCPU `
  /p:OutputPath='D:\相聚假人\Source\.build-check\pc-korean-chat-resize-cycle-luna\' `
  /p:RestorePackages=false
```

Expected: exit `0`, 0 errors. Report warning count, output size and SHA-256.

- [ ] **Step 9: Scope and backup audit**

Compare both changed source files against their new backups. Confirm no 145-only construction, minimap, server/mobile, resource archive, deployed client, `Mir3.ini` or `CHANGELOG.md` was modified. Return runtime Direct3D appearance and click behavior as an explicit manual verification gap.
