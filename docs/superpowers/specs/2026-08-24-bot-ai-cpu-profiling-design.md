# 假人 AI CPU 回归低开销诊断设计

## 目标

在保持 15 个假人当前行为不变的前提下，定位新版 `Server.exe` 从旧版约 1%–4% 上升到约 4%–9% 的 CPU 时间落点，为后续单点优化提供可重复证据。

当前已确认：

- 部署版本为 Debug / AnyCPU `1.0.9732.1203`，运行目标 `BotCount=15`。
- 前 15 个假人为战士 6、法师 4、道士 3、刺客 2。
- 每个假人仍约 800ms 驱动一次，独立喝药仍为 200ms。
- 旧版 `1.0.9732.302` 与新版的方法体比较显示，`BotTick`、`BotPotionTick`、喝药模块和 A* 实现未变化；变化集中在道士选择和实际施法链。
- 新版道士候选枚举每次战斗帧分配一个迭代器，但 3 个道士合计仅约每秒 3.75 次，不能单独解释数个百分点的 CPU 上升。

## 诊断方案

增加临时、低开销的聚合计时。每个测量点只调用两次 `Stopwatch.GetTimestamp()`，并用 `Interlocked` 累计总 ticks 和调用次数；不得创建计时对象、闭包、任务或新线程。

测量六个相互嵌套的桶：

1. `TickDispatch`：`BotTick` 的快照、分片和入队成本。
2. `AiPipeline`：主线程实际执行单个假人行为管线的总耗时。
3. `Potion`：主线程实际执行单个假人喝药模块的总耗时。
4. `Combat`：完整 `ProcessBotCombat` 耗时。
5. `TaoistCombat`：道士职业战斗入口耗时，用于验证最近改动是否为热点。
6. `PathCompute`：仅统计 A* 重新计算和缓存路径，不统计消费已有路径。

这些桶是包含关系，不得相加当作总 CPU。例如 `TaoistCombat` 属于 `Combat`，`Combat` 属于 `AiPipeline`。

## 汇总输出

- 使用一个原子控制的 60 秒窗口。
- 每个窗口最多输出一条以 `[BotPerf]` 开头的日志。
- 每个桶输出调用次数、累计毫秒和平均毫秒。
- 日志不得包含角色名、账号、密码、地图对象列表或逐次调用明细。
- 汇总后用 `Interlocked.Exchange` 清零当前窗口计数。
- 假人系统未运行时不输出诊断日志。

## 修改边界

只允许修改：

- `Server/BotManager.cs`：计数器、汇总输出、`BotTick`、`ProcessBotBehaviorPipeline`、`ProcessBotPotionModule`。
- `Server/BotManager.Combat.cs`：`ProcessBotCombat` 和 `ProcessBotTaoistCombatAction` 测量。
- `Server/BotPathFinder.cs`：`ComputeAndCache` 测量。
- `.diagnostics/bot-ai-cpu-profiling-contract.ps1`：专项静态契约。
- 本设计文档和后续实施计划。

不得修改 `BotMainSliceIntervalMs=200`、`BotMainSliceCount=4`、`BotPotionMonitorIntervalMs=200`、技能顺序、喝药阈值、寻路策略、数据库、配置文件或部署目录。

## 测试与验证

1. 先创建专项契约并取得真实 RED，要求六个桶、60秒单条汇总、`Stopwatch.GetTimestamp`、`Interlocked`、无新线程/定时器且三个周期常量不变。
2. 实施诊断后取得专项 GREEN。
3. 重跑既有 CPU/喝药、阶段一、40级/刺客、道士/法师战斗契约。
4. 独立构建 Debug / AnyCPU 到新的 `.build-check` 目录，0 errors。
5. 本阶段只生成诊断版，不自动覆盖部署目录、不停止或重启当前服务。

## 运行验收

用户部署诊断版后，在相同的 15 个假人和尽量相同的地图/战斗状态下运行至少 10 分钟，同时记录：

- 任务管理器中 Server CPU 的稳定区间。
- 至少 10 条连续 `[BotPerf]` 汇总。
- 是否存在地图切换、集中死亡复活、补货或大量 A* 重算等负载变化。

根据累计毫秒占比选择后续唯一优化点；完成优化后删除全部临时诊断代码和 `[BotPerf]` 日志，再用相同负载复测。若六个桶均不足以解释 CPU 上升，则停止猜测并升级到具有管理员权限的采样分析，而不是调整行为频率。
