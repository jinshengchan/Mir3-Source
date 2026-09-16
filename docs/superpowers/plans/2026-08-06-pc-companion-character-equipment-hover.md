# PC 宠物背包与角色装备栏悬停展示实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 复用现有人物背包装备悬停逻辑到宠物背包和角色装备栏，并恢复普通道具独立说明框绘制。

**Architecture:** 不复制提示框代码，只扩展 `CreateEquipmentCompareInfo()` 与 `CreateEquipmentAppearanceInfo()` 的网格入口；独立说明框在 `OnAfterDraw()` 中显式处理外观框为空或已销毁的状态。

**Tech Stack:** C#、.NET Framework、SharpDX、MSBuild、PowerShell 源码契约检查。

## Global Constraints

- 只修改 `145Client/Scenes/GameScene.cs` 和 `CHANGELOG.md`。
- 不修改宠物自身装备栏、服务端、封包、安卓端和资源文件。
- 覆盖前备份源码、日志和目标 `Mir3.exe`；不新建客户端目录。
- 工程不是 Git 仓库，以单文件备份代替提交。

---

### Task 1: 建立失败检查并备份

**Files:**
- Test: `145Client/Scenes/GameScene.cs` 源码契约
- Backup: `GameScene.cs`、`CHANGELOG.md`、目标 `Mir3.exe`

- [ ] **Step 1: 运行失败契约**

断言比较入口包含 `Inventory` 和 `CompanionInventory`；外观入口包含 `Inventory`、`CompanionInventory` 和 `Equipment`；独立说明绘制先处理外观框为空或已销毁。修改前应失败。

- [ ] **Step 2: 创建覆盖前备份**

以 `20260806-companion-character-hover` 后缀备份三个将覆盖文件，不覆盖已有备份。

### Task 2: 扩展宠物背包和角色装备栏入口

**Files:**
- Modify: `145Client/Scenes/GameScene.cs:3862-3866,3959-3963`

**Interfaces:**
- Consumes: `DXItemCell.GridType`。
- Produces: 比较入口 `Inventory|CompanionInventory`；外观入口 `Inventory|CompanionInventory|Equipment`。

- [ ] **Step 1: 写入最小入口判断**

比较方法允许人物背包和宠物背包；外观方法额外允许角色装备栏。保持 `CompanionEquipment` 被排除。

- [ ] **Step 2: 运行入口绿色契约**

检查三个目标入口为真、宠物自身装备栏未加入，并确认未装备提前结束差值仍存在。

### Task 3: 恢复普通道具说明绘制

**Files:**
- Modify: `145Client/Scenes/GameScene.cs:5500-5504`

**Interfaces:**
- Consumes: `ItemLabel.Parent` 和 `EquipmentAppearanceLabel` 生命周期。
- Produces: 无外观框时绘制独立说明；已嵌入共同外框时不重复绘制。

- [ ] **Step 1: 写入最小绘制条件**

条件改为：`EquipmentAppearanceLabel == null || EquipmentAppearanceLabel.IsDisposed || ItemLabel.Parent != EquipmentAppearanceLabel`。

- [ ] **Step 2: 运行绘制绿色契约**

确认空外观框和已销毁外观框均能进入手动绘制，同时保留父级不等判断。

### Task 4: 编译、交付与日志

**Files:**
- Modify: `CHANGELOG.md`
- Replace: `D:/Debug/4月18日更新/Client/Mir3.exe`

- [ ] **Step 1: 编译 PC 客户端项目**

构建 `145Client/145Client.csproj` 的 `Debug|AnyCPU`，要求退出码为 0。

- [ ] **Step 2: 更新日志**

记录普通道具根因、三个网格行为、验证结果、哈希和备份路径。

- [ ] **Step 3: 最终验证与交付**

重新编译，运行全部源码契约，确认目标客户端未运行后覆盖，并核对编译产物与交付文件 SHA256 一致。

- [ ] **Step 4: 人工验证说明**

要求游戏内检查人物背包、宠物背包、角色装备栏的装备和普通道具两类悬停行为。
