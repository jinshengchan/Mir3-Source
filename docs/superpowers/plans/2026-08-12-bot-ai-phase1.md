# Bot AI Phase 1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 接通假人自卫受击链，修正已确认的 PK 与装备评分错误，并把 30 个假人的主 AI 均匀分布在四个 200ms 调度片中。

**Architecture:** `ServerLibrary` 只发布通用的假人 PvP 受击事件，避免反向依赖 `Server`；`BotManager` 继续作为威胁和行为状态唯一拥有者。调度采用固定四片轮转，不新增后台工作线程，所有游戏动作继续由 `SEnvir.BotActionQueue` 在主循环执行。

**Tech Stack:** C# 7.2、.NET Framework 4.8、MSBuild、PowerShell 源码契约检查。

## Global Constraints

- 最小改动，不重构现有大文件。
- 普通地图只自卫，不增加主动 PK。
- 不调整现有经济扶持数值。
- 不覆盖运行服务端，构建输出必须隔离到 `.build-check`。

---

### Task 1: 建立失败的回归契约

**Files:**
- Create: `.diagnostics/bot-ai-phase1-contract.ps1`

**Interfaces:**
- Consumes: 当前五个生产源码文件。
- Produces: 对受击通知、PK过滤、职业评分和四片调度的静态契约。

- [ ] **Step 1:** 编写契约脚本，逐项检查设计要求对应的源码结构。
- [ ] **Step 2:** 运行脚本并确认旧源码因缺少受击事件、错峰调度和统一评分而失败。

### Task 2: 接通自卫受击链并修正 PK 决策

**Files:**
- Modify: `ServerLibrary/Models/Player/PlayerObjectBase.cs`
- Modify: `ServerLibrary/Models/Player/Combat.cs`
- Modify: `Server/BotManager.cs`
- Modify: `Server/BotManager.Combat.cs`
- Modify: `Server/BotPvPStrategy.cs`

**Interfaces:**
- Produces: `PlayerObject.BotPvPDamaged(PlayerObject bot, PlayerObject attacker, int damage)` 事件。
- Consumes: `BotManager.RecordBotAttacker` 与现有 `BotPvPStrategy`。

- [ ] **Step 1:** 在 `PlayerObject` 声明静态事件，只在 `IsBot` 且攻击来源为真人或其宠物主人时发布最终有效伤害。
- [ ] **Step 2:** `BotManager.Initialize` 幂等订阅事件，处理器仅在系统运行且对象仍是假人时记录威胁。
- [ ] **Step 3:** 修正同行会自检、风筝布尔判断、队友威胁编号、同图/视野/合法性过滤、逃跑方向和 10 格停止条件。
- [ ] **Step 4:** 运行契约脚本，确认本任务对应断言通过。

### Task 3: 统一装备评分

**Files:**
- Modify: `Server/BotManager.Support.cs`

**Interfaces:**
- Produces: `CalculateWeightedItemScore(UserItem item, MirClass playerClass)`，同时计算基础与附加属性。

- [ ] **Step 1:** 自动换装和双槽排序改用职业加权的 `UserItem` 评分。
- [ ] **Step 2:** 基础与附加属性计算移除绝对值，保留负属性扣分。
- [ ] **Step 3:** 双槽当前装备比较改用同一职业评分。
- [ ] **Step 4:** 运行契约脚本，确认装备评分断言通过。

### Task 4: 四片错峰和重复喝药清理

**Files:**
- Modify: `Server/BotManager.cs`
- Modify: `Server/BotManager.Combat.cs`

**Interfaces:**
- Produces: 4 个稳定调度槽，每槽 200ms，每名假人约 800ms 执行一次主 AI。

- [ ] **Step 1:** 增加 200ms/4片常量和轮转索引，只有第0片执行登录、记忆和组队维护。
- [ ] **Step 2:** 在线假人按 `ObjectID % 4` 进入对应片，游戏动作仍投递主线程队列。
- [ ] **Step 3:** 对两个防积压 `HashSet` 的跨线程 Add/Remove 加最小锁保护。
- [ ] **Step 4:** 删除 `ProcessBotBehaviorPipeline` 内重复的药水模块调用，保留独立 200ms 监控和战斗紧急喝药。
- [ ] **Step 5:** 运行完整契约脚本并确认通过。

### Task 5: 构建、差异和日志验证

**Files:**
- Modify: `CHANGELOG.md`

**Interfaces:**
- Produces: 隔离 Release 构建、哈希与变更清单。

- [ ] **Step 1:** 编译 `ServerLibrary/ServerLibrary.csproj` Release 到隔离目录。
- [ ] **Step 2:** 使用隔离的 `Library.dll` 编译 `Server/Server.csproj` Release 到隔离目录。
- [ ] **Step 3:** 再次运行完整契约，记录退出码和断言数量。
- [ ] **Step 4:** 更新 `CHANGELOG.md`，列明源码文件、行为变化、构建证据和尚需在线验证的项目。
- [ ] **Step 5:** 输出修改文件 SHA256，确认未覆盖运行服务端。

