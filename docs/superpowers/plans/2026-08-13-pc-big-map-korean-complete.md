# PC 大地图韩版完整窗口 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在共享 PC `BigMapDialog` 中完整还原韩版大地图外框、NPC 列表、世界区域动画和原版底栏交互。

**Architecture:** 保持一个共享 `BigMapDialog` 状态机：世界总览与地图详细页互斥。详细页复用现有 `MapInfo`/NPC/寻路数据流；世界页只增加素材驱动的悬停层和目标映射，不复制地图或寻路系统。

**Tech Stack:** C#、.NET Framework 4.8、WinForms/SharpDX、自定义 DXControls、BlackDragon `.Zl` 素材。

## Global Constraints

- 仅修改 `145Client/Scenes/Views/BigMapDialog.cs`、`.diagnostics/test_pc_big_map_world_view_contract.ps1` 和现有 `CHANGELOG.md` 条目。
- 不修改 `.Zl`、地图/NPC 数据、寻路算法、服务器、移动端及其他 UI。
- 保持145与韩版界面共享实现。
- 不部署或覆盖现有客户端。

---

### Task 1: 素材与现有接口核对

**Files:**
- Inspect: `145Client/Data/UI1.Zl`
- Inspect: `145Client/Data/WorldMap.Zl`
- Inspect: `145Client/Scenes/Views/BigMapDialog.cs`

- [ ] 确认完整外框、标题、关闭按钮、NPC区、滚动条、搜索按钮、输入框和两个底栏按钮的确切素材序号。
- [ ] 确认世界总览底图、区域命中范围、目标地图和动画帧组的映射；优先复用源码已有映射或资源内连续帧，不猜测序号。
- [ ] 若素材或映射不足以实现参考效果，停止并报告具体缺口，不用临时绘制替代。

### Task 2: 扩展 RED 契约

**Files:**
- Modify: `.diagnostics/test_pc_big_map_world_view_contract.ps1`

- [ ] 新增完整边框、标题、关闭按钮、NPC列表/滚动条、世界页隐藏列表、悬停动画、点击目标、原版底栏素材和现有寻路入口断言。
- [ ] 运行 `powershell.exe -NoProfile -ExecutionPolicy Bypass -File .diagnostics/test_pc_big_map_world_view_contract.ps1`。
- [ ] 确认当前实现因缺少上述结构而失败，并记录失败项。

### Task 3: 最小实现完整窗口

**Files:**
- Modify: `145Client/Scenes/Views/BigMapDialog.cs`

- [ ] 用已核实素材建立完整外框、标题、关闭按钮、内容区、NPC区和原版底栏控件。
- [ ] 详细地图刷新时从 `Globals.NPCInfoList.Binding` 过滤当前 `SelectedInfo`，刷新可滚动列表。
- [ ] NPC点击只在 `SelectedInfo == GameScene.Game.MapControl.MapInfo` 时调用现有寻路入口。
- [ ] 世界页隐藏 NPC 区；建立区域命中控件，悬停时按帧切换高亮动画和标题，离开恢复，点击调用现有详细地图切换。
- [ ] 当前地图点击寻路、路径绘制和右键传送逻辑保持原样。

### Task 4: 验证和记录

**Files:**
- Modify: `CHANGELOG.md`（更新现有 2026-08-13 大地图条目，不新增重复条目）

- [ ] 重跑 focused contract，要求全部 PASS。
- [ ] 运行 `MSBuild.exe 145Client/145Client.csproj /t:Rebuild /m /v:minimal /p:Configuration=Release /p:Platform=AnyCPU`，要求退出码 0。
- [ ] 报告完整差异、文件哈希、编译产物路径和尚需实机验证的像素/动画项；不部署。
