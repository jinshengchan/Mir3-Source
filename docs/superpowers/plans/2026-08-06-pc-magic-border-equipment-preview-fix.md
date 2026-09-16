# PC 魔法窗口边框与装备预览修复实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 用最小源码改动修复魔法窗口右侧空栏、人物预览越框和未装备仍显示属性差值，并重新编译交付 PC 客户端。

**Architecture:** 魔法窗口恢复素材原生宽度，不再拼接整幅背景；人物预览用现有图层矩形同时计算横纵边界；装备比较在未装备分支提前结束属性行生成。所有改动限制在两个现有界面文件内。

**Tech Stack:** C#、.NET Framework、SharpDX、MSBuild、PowerShell 源码契约检查。

## Global Constraints

- 不修改 `UI1.Zl`；该资源已只读检查为所需素材 42/42 完整。
- 只修改 `145Client/Scenes/Views/MagicDialog.cs`、`145Client/Scenes/GameScene.cs` 和 `CHANGELOG.md`。
- 覆盖前备份两个源码文件、更新日志和目标 `Mir3.exe`；不新建客户端目录。
- 不改动 11 个分类按钮、11 个技能页面的素材索引及切换逻辑。
- 工程不是 Git 仓库，以带时间和用途后缀的文件备份代替提交。

---

### Task 1: 修复魔法窗口右侧空栏和重复边框

**Files:**
- Modify: `145Client/Scenes/Views/MagicDialog.cs:91-147`
- Test: PowerShell 源码契约 + `145Client.csproj` 编译

**Interfaces:**
- Consumes: `UI1Library.GetSize(1620)` 返回的原生窗口尺寸。
- Produces: 原生宽度的 `MagicDialog`，滚动条和关闭按钮使用原位置；11 个分类按钮保持不变。

- [ ] **Step 1: 运行失败契约**

检查当前源码不应包含 `extraWidth`、`magicExtension`、`317 + extraWidth`；当前应失败，以证明能捕获空栏实现。

- [ ] **Step 2: 写入最小实现**

将窗口恢复为 `Size = s;`，删除 `extraWidth` 和 `magicExtension`，关闭按钮恢复 `new Point(317, 400)`。滚动条现有 `Size.Width - 42` 自动恢复到原位置。

- [ ] **Step 3: 运行绿色契约与编译**

确认加宽与拼接代码不存在，同时 `CombatButton`、`AssassinationButton`、`AssassinatieButton` 及 `1711–1743` 页面仍存在；编译 `145Client.csproj`。

### Task 2: 修复人物外观预览越框

**Files:**
- Modify: `145Client/Scenes/GameScene.cs:192-195,3926-4140`
- Test: PowerShell 源码契约 + `145Client.csproj` 编译

**Interfaces:**
- Consumes: 每个角色绘制图层的 `Rectangle`（偏移和尺寸）。
- Produces: `GetAppearanceBounds(Rectangle[] layers)` 完整边界及 `EquipmentAppearanceDrawOffsetY` 绘制基准。

- [ ] **Step 1: 运行失败契约**

检查源码应包含纵向绘制偏移，并且不再存在 `appearanceHeight = 240`、`drawY = ... + 220`；当前应失败。

- [ ] **Step 2: 写入最小实现**

把仅计算左右边界的辅助方法改为计算 `left/top/right/bottom`；人物预览宽高均使用边界尺寸加 12 像素，X/Y 绘制偏移均使用 `6 - bounds.Left/Top`。

- [ ] **Step 3: 运行绿色契约与编译**

确认固定高度和固定基准已删除、横纵边界均参与尺寸和位置计算，然后编译客户端项目。

### Task 3: 未装备时隐藏属性差值

**Files:**
- Modify: `145Client/Scenes/GameScene.cs:3891-3916`
- Test: PowerShell 源码契约 + `145Client.csproj` 编译

**Interfaces:**
- Consumes: `Equipment[(int)slot]`。
- Produces: 未装备槽位只有部位标题和“未装备”，已装备槽位继续调用 `AppendEquipmentCompareStatRows`。

- [ ] **Step 1: 运行失败契约**

检查 `equippedItem == null` 分支必须在“属性差值”标签和 `AppendEquipmentCompareStatRows` 之前提前继续；当前应失败。

- [ ] **Step 2: 写入最小实现**

输出部位标题和名称后，若 `equippedItem == null`，设置 `firstSlot = false` 并 `continue`；不创建属性标题与差值行。

- [ ] **Step 3: 运行绿色契约与编译**

确认未装备分支位于属性标题之前，且已装备比较代码保持不变，然后编译客户端项目。

### Task 4: 交付与记录

**Files:**
- Modify: `CHANGELOG.md`
- Replace: `D:/Debug/4月18日更新/Client/Mir3.exe`

- [ ] **Step 1: 完整编译**

使用 MSBuild 构建 `145Client/145Client.csproj` 的 `Debug|AnyCPU`，要求退出码为 0。

- [ ] **Step 2: 最终源码契约**

一次检查三项修复及 11 个按钮/页面保留情况，要求全部为 True。

- [ ] **Step 3: 覆盖交付并核对哈希**

把 `D:/相聚假人/客户端/Mir3.exe` 复制到目标客户端，并确认两者 SHA256 一致。

- [ ] **Step 4: 更新日志**

记录根因、改动文件、资源完整性检查、编译结果、哈希和备份路径。

- [ ] **Step 5: 人工验证说明**

交付时明确要求进入游戏检查：魔法窗口右栏、11 个分类切换、衣服/时装人物边界、未装备与已装备两种比较状态。
