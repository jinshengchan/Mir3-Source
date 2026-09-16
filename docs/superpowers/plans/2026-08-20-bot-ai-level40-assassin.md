# Bot AI Level 40 Progression and Assassin Skills Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 让 40 级以上假人在普通练级时采用明显更高分的安全地图，并让刺客对怪物使用现有 AOE、突进、点名和近战技能链。

**Architecture:** 保留当前地图评分、安全过滤、打金和组队跟随机制，只补上普通练级采纳更高分候选图的缺失分支。刺客继续复用 `BotSkillSelector` 与 `TryCastBotMagic`，移除只对刺客造成技能短路的物理回退参数。

**Tech Stack:** C# 7.2、.NET Framework 4.8、PowerShell 源码契约、VS 2022 Build Tools MSBuild。

## Global Constraints

- 仅修改 `Server/BotManager.Combat.cs`、新增专项契约、更新 `CHANGELOG.md`。
- 不修改技能优先级、技能学习、金币模式、地图安全过滤、Boss 过滤、组队跟随或服务端数据库。
- 不部署，不覆盖 `D:\Debug\4月18日更新\Server\Server.exe`；Release 构建输出到隔离 `.build-check` 目录。
- 非 Git 工作区，以基线/最终 SHA-256 和明确文件清单证明范围。

---

### Task 1: 建立两项失败契约

**Files:**
- Create: `.diagnostics/bot-ai-level40-assassin-contract.ps1`
- Read: `Server/BotManager.Combat.cs`

**Interfaces:**
- Consumes: `ProcessBotAutoCombat` 的地图评估分支和 `ProcessBotAssassinCombatAction`。
- Produces: 两项可重复源码契约，分别捕获普通练级忽略高分地图、刺客怪物战斗被物理回退短路。

- [ ] **Step 1:** 新契约读取 `Server/BotManager.Combat.cs`，检查 40 级以上、非打金、`bestScore > currentScore + switchMargin` 时设置 `shouldSwitchMap = true`。
- [ ] **Step 2:** 新契约检查刺客战斗调用不再接收 `forcePhysicalFallback`，且 AOE、突进和 `GetAssassinMeleeAttackMagic` 不再被该标志挡住。
- [ ] **Step 3:** 运行 `powershell.exe -NoProfile -ExecutionPolicy Bypass -File .diagnostics\bot-ai-level40-assassin-contract.ps1`；预期两项因当前缺陷失败并退出 `1`。

### Task 2: 最小生产修复

**Files:**
- Modify: `Server/BotManager.Combat.cs`

**Interfaces:**
- Preserves: `GetBotMapScore`、`FindSuitableMapForBot`、金币模式分差、安全/Boss 过滤、组队跟随。
- Preserves: `BotSkillSelector` 的刺客技能优先级、冷却、蓝量和目标条件。

- [ ] **Step 1:** 在现有地图评估中增加：`!goldFarmMode && player.Level >= 40 && bestScore > currentScore + switchMargin` 时切图。
- [ ] **Step 2:** 删除 `ProcessBotAssassinCombatAction` 的 `forcePhysicalFallback` 参数及三处技能短路，继续使用现有技能选择器。
- [ ] **Step 3:** 重跑专项契约；预期全部 PASS、退出 `0`。
- [ ] **Step 4:** 运行现有 `.diagnostics\bot-ai-phase1-contract.ps1`；预期保持 `21 assertions PASS`。

### Task 3: 记录与隔离验证

**Files:**
- Modify: `CHANGELOG.md`

**Interfaces:**
- Produces: 本轮行为、RED/GREEN、隔离构建和未在线验证边界。

- [ ] **Step 1:** 在当前日期条目记录两个根因与最小修复，不宣称已在线验证。
- [ ] **Step 2:** Release 编译 `ServerLibrary` 与 `Server` 到 `.build-check\bot-ai-level40-assassin-release`，不得覆盖运行目录。
- [ ] **Step 3:** 重跑两份契约，核对仅计划文件、专项契约、生产源码和 `CHANGELOG.md` 发生变化。
- [ ] **Step 4:** 输出最终 SHA-256，并明确真实在线换图节奏与刺客施法仍需运行服务端验收。
