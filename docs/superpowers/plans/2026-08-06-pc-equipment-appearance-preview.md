# PC Equipment Appearance Preview Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在 PC 端人物包裹中，鼠标悬停衣服或时装时显示基础人物穿戴该物品的效果，悬停其他装备时仅显示装备自身外观。

**Architecture:** 沿用 `GameScene` 现有悬停说明和装备比较面板的生命周期，新增一个独立、不可交互的外观预览面板。衣服/时装复用角色内观使用的 `ProgUse`、`Equip` 与幻化索引；其他装备复用背包格子的 `Inventory` 图像索引。功能仅由 `GridType.Inventory` 触发，不改服务端、封包和资源。

**Tech Stack:** C# 8.0、.NET Framework 4.8、SharpDX、项目现有 DXControl/MirLibrary 绘制系统。

## Global Constraints

- 只影响 PC 客户端人物包裹。
- 普通衣服和时装显示基础人物穿上鼠标所指物品的效果。
- 其他装备只显示鼠标所指装备自身外观。
- 保留现有装备属性说明与身上装备属性差值。
- 最小改动；覆盖源码前仅备份被修改文件。
- 不修改服务端、封包或资源文件。

---

### Task 1: 外观预览分类与生命周期

**Files:**
- Modify: `145Client/Scenes/GameScene.cs`
- Test: 临时 PowerShell 反射验证（不写入项目）

**Interfaces:**
- Consumes: `MouseItem`、`MouseControl as DXItemCell`、`GridType.Inventory`、`ItemType`
- Produces: `UsesCharacterAppearancePreview(ItemType)` 和 `EquipmentAppearanceLabel`

- [ ] **Step 1: 建立失败验证**

  先编译当前客户端，再通过反射检查 `GameScene.UsesCharacterAppearancePreview(ItemType)`；预期因方法不存在而失败。

- [ ] **Step 2: 增加最小分类逻辑**

  仅让 `ItemType.Armour` 和 `ItemType.Fashion` 返回人物穿戴预览，其余装备返回物品外观预览。

- [ ] **Step 3: 接入创建、销毁与位置计算**

  `CreateItemLabel()` 创建前清理旧面板；选中物品或移开鼠标时一并销毁；位置按 `[外观][物品说明][装备比较]` 计算并限制在游戏窗口内。

- [ ] **Step 4: 运行反射验证**

  验证 `Armour=True`、`Fashion=True`、`Weapon=False`、`Helmet=False`。

### Task 2: 绘制人物穿衣与装备外观

**Files:**
- Modify: `145Client/Scenes/GameScene.cs`

**Interfaces:**
- Consumes: `MapObject.User` 的职业、性别、发型，`CEnvir.GetItemIllusionItemInfo`，`LibraryFile.ProgUse`、`LibraryFile.Equip`、`LibraryFile.Inventory`
- Produces: `DrawEquipmentAppearancePreview()`

- [ ] **Step 1: 衣服和时装人物预览**

  绘制当前角色基础身体和发型，仅叠加悬停衣服/时装；不读取或绘制当前已穿戴武器、头盔、盾牌和其他装备。衣服使用幻化图像索引并叠加物品颜色。

- [ ] **Step 2: 其他装备外观预览**

  使用与 `DXItemCell` 一致的 ItemPart、幻化图像索引规则，从 `LibraryFile.Inventory` 以原始比例居中绘制装备图像。

- [ ] **Step 3: 绘制顺序验证**

  在 `OnAfterDraw()` 中先画外观面板，再画原物品说明和装备比较，确保三者均显示且不接收鼠标点击。

### Task 3: 编译、产物与更新日志

**Files:**
- Modify: `CHANGELOG.md`
- Backup: `145Client/Scenes/GameScene.cs.bak-20260806-equipment-appearance-preview`

**Interfaces:**
- Consumes: `145Client/145Client.csproj`
- Produces: 可运行的 PC 客户端编译产物和可回溯记录

- [ ] **Step 1: 编译 PC 客户端**

  使用项目配置编译 `145Client.csproj`，要求退出码为 0。

- [ ] **Step 2: 检查改动范围**

  确认源码改动仅涉及 `GameScene.cs`，并确认备份存在。

- [ ] **Step 3: 更新日志**

  记录日期、需求、修改文件、备份文件、行为范围及编译结果。

- [ ] **Step 4: 人工验收清单**

  在 PC 客户端人物包裹中分别悬停普通衣服、时装、武器、头盔、首饰；确认衣服/时装仅显示基础人物穿戴效果，其他装备只显示自身外观，并检查屏幕四边的面板位置。
