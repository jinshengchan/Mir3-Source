# PC Equipment Appearance Frame Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将 PC 人物包裹装备外观框收紧到素材实际宽度，并让外观框与物品属性框上下边框完全对齐。

**Architecture:** 在 `GameScene` 现有外观预览创建流程中读取 `MirLibrary.GetSize/GetOffSet`，合并基础人物、衣服和发型的水平范围，计算面板最小宽度及绘制锚点。创建完成后把外观框和物品属性框高度统一为两者原高度的较大值，不改变绘制内容、属性文字和装备比较面板。

**Tech Stack:** C# 8.0、.NET Framework 4.8、SharpDX、项目现有 DXControl/MirLibrary 绘制系统。

## Global Constraints

- 仅影响 PC 端人物包裹装备悬停预览。
- 人物和装备素材不缩放、不裁切。
- 左右内容各保留 `6` 像素水平边距。
- 外观框与物品属性框顶部、底部完全对齐。
- 不修改服务端、封包、安卓端、资源素材和右侧文字排版。
- 仅备份将覆盖的源码、客户端和更新日志文件。

---

### Task 1: 水平素材范围与等高规则

**Files:**
- Modify: `145Client/Scenes/GameScene.cs`
- Test: 临时 PowerShell 反射验证（不写入运行项目）

**Interfaces:**
- Consumes: `Rectangle[]` 素材范围、外观原始高度、属性框原始高度
- Produces: `GetAppearanceHorizontalBounds(Rectangle[])`、`GetAlignedAppearanceHeight(int, int)`

- [ ] **Step 1: 运行失败验证**

  反射检查上述两个方法；预期因方法尚不存在而失败。

- [ ] **Step 2: 实现最小纯计算逻辑**

  合并所有有效矩形的最小 `Left` 与最大 `Right`；等高函数返回两个高度中的较大值。

- [ ] **Step 3: 运行行为验证**

  使用 `[-20, 30]`、`[10, 40]` 两个范围验证合并结果为 `Left=-20`、`Right=50`，并验证 `240/135` 与 `120/260` 两组高度均取较大值。

### Task 2: 动态最小宽度与人物居中

**Files:**
- Modify: `145Client/Scenes/GameScene.cs`

**Interfaces:**
- Consumes: `LibraryFile.ProgUse`、`LibraryFile.Equip`、`LibraryFile.Inventory` 的尺寸与偏移
- Produces: 动态 `EquipmentAppearanceLabel.Size` 与人物绘制锚点

- [ ] **Step 1: 收集人物绘制层范围**

  按当前实际绘制条件加入基础身体、刺客女长辫、衣服/时装和发型的水平矩形；衣服继续使用幻化后的图像索引。

- [ ] **Step 2: 设置人物外观框宽度**

  面板宽度设为合并范围宽度加 `12` 像素，人物锚点设为 `6 - bounds.Left`，使可见模型左右各保留 `6` 像素。

- [ ] **Step 3: 设置其他装备外观框宽度**

  面板宽度设为背包图像实际宽度加 `12` 像素；图像继续在等高后的面板内水平、垂直居中。

- [ ] **Step 4: 对齐左右高度**

  人物外观原始高度保留 `240`；其他装备使用图像高度加 `12`。外观框与 `ItemLabel` 同时设置为两者原高度较大值，文字子控件位置不变。

### Task 3: 编译产物与更新记录

**Files:**
- Modify: `CHANGELOG.md`
- Backup: `145Client/Scenes/GameScene.cs.bak-20260806-equipment-appearance-frame`
- Backup: `D:/Debug/4月18日更新/Client/Mir3.exe.bak-20260806-equipment-appearance-frame`

**Interfaces:**
- Consumes: `145Client/145Client.csproj`
- Produces: 更新后的 PC `Mir3.exe` 与可回滚记录

- [ ] **Step 1: Rebuild 客户端**

  使用 Debug/AnyCPU 配置完整重建，要求退出码为 `0`。

- [ ] **Step 2: 覆盖目标客户端**

  先备份目标 `Mir3.exe`，再复制最终编译产物到 `D:/Debug/4月18日更新/Client/Mir3.exe`。

- [ ] **Step 3: 更新日志与哈希**

  记录需求、唯一源码改动、备份路径、验证结果和最终 SHA-256。

- [ ] **Step 4: 人工验收**

  分别悬停普通衣服、时装、宽体衣服、武器和首饰，确认宽度紧贴素材且左右边框上下完全对齐。
