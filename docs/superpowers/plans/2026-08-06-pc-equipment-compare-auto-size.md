# PC 装备比较框自动宽度与等高实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 让右侧属性比较框按内容自动定宽，并与自动高度的左侧共同框上下完全对齐。

**Architecture:** 保留现有逐标签扩展宽度机制，去掉固定初始宽度；比较框先生成内容，外观共同框随后以三方最大高度作为最终高度，最后把比较框同步到该高度。

**Tech Stack:** C#、.NET Framework、SharpDX、MSBuild、PowerShell 源码契约检查。

## Global Constraints

- 只修改 `145Client/Scenes/GameScene.cs` 和 `CHANGELOG.md`。
- 不改属性计算、差值颜色、文字、窗口定位、网格入口、服务端、安卓端或资源文件。
- 覆盖前备份源码、日志和目标 `Mir3.exe`；不新建客户端目录。
- 工程不是 Git 仓库，以单文件备份代替提交。

---

### Task 1: 失败检查与备份

- [ ] **Step 1: 运行失败契约**

检查右框初始宽度为零、最终高度包含右框内容、右框同步最终高度；修改前应三项失败。

- [ ] **Step 2: 创建覆盖前备份**

以 `20260806-equipment-compare-auto-size` 后缀备份 `GameScene.cs`、`CHANGELOG.md` 和目标 `Mir3.exe`。

### Task 2: 实现自动宽度与等高

**Files:**
- Modify: `145Client/Scenes/GameScene.cs:3883-3892,4060-4090`

- [ ] **Step 1: 去掉固定右框宽度**

把 `EquipmentCompareLabel` 初始尺寸改为 `new Size(0, 4)`；继续由 `AddEquipmentCompareLabel()` 的现有最大宽度计算扩展。

- [ ] **Step 2: 计算左框最终高度**

`alignedHeight` 取外观高度、物品属性高度和有效右框内容高度的最大值。

- [ ] **Step 3: 同步右框高度**

共同外框生成后，在右框存在且未销毁时只更新其高度为 `alignedHeight`，保留已计算宽度。

- [ ] **Step 4: 运行绿色契约与阶段编译**

确认三项新规则和宠物背包、角色装备栏、普通道具、人物边界、未装备规则全部存在，随后编译客户端项目。

### Task 3: 交付与日志

- [ ] **Step 1: 更新日志**

记录尺寸根因、最终规则、验证结果、哈希和备份路径。

- [ ] **Step 2: 最终独立验证**

重新编译并运行完整源码契约，确认目标客户端未运行后覆盖，核对编译产物与交付文件 SHA256 一致。

- [ ] **Step 3: 人工验证说明**

要求游戏内检查短属性、长属性、未装备、宠物背包装备和角色装备栏悬停框。
