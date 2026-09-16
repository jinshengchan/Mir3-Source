# 假人 AI 道士攻击选择与自动学技能设计

## 状态

本规格已获批准，当前阶段只完成设计文档，不修改生产源码、契约、变更日志、构建产物或部署目录。

## 背景与已确认现象

用户观察到：10 级道士已经锁定同图、相邻且可攻击的怪物，但没有进行反击。目标不是无目标漫游，也不是目标死亡后的拾取等待。

当前行为管线为：

```text
ProcessBotBehaviorPipeline
  → ProcessBotSkillModule
  → ProcessBotTaoistModules
      → 召唤 / 防御 Buff / 支援治疗
      → PK / 拾取
      → ProcessBotCombat
          → 目标保持或获取
          → ProcessBotCombatEngagement
              → 低血保命
              → ProcessBotTaoistCombatAction
```

### 源码支持的两个机制

第一，`ProcessBotTaoistModules` 在战斗前执行召唤、防御和支援动作，但这些方法只返回各自的方法调用，不会把“本 Tick 已经有支持动作”传递给父模块。成功的召唤或 Buff 会在 `ActionList` 中留下延迟动作，并更新 `ActionTime`/`MagicTime`。同一 Tick 继续进入战斗时，施法、移动和物理攻击可能都被当前动作状态拒绝。这是支持动作队列造成的独立、通常短暂的阻塞机制。

第二，Taoist 的 `GetTaoistRangedMagic` 与 `GetTaoistAttackMagic` 当前都先返回可用的防御技能。`ProcessBotTaoistCombatAction` 把该返回值当作怪物攻击技能交给通用远程入口；只要施法冷却推进，远程入口就会提前返回，战斗 Tick 不会进入物理兜底。防御、治疗和召唤不应由怪物攻击选择器拥有，这是本设计要修正的直接路由缺陷。

相关当前路径：

- `Server/BotManager.cs:1991-2002`：道士支持模块之后仍继续进入战斗。
- `Server/BotManager.Support.cs:3723-3785`：召唤；成功动作有约 8 秒召唤门控。
- `Server/BotManager.Support.cs:4010-4115`：防御 Buff；成功动作有约 5 秒 Buff 门控。
- `Server/BotManager.Support.cs:4126-4260`：隐身和治疗支援。
- `Server/BotManager.Combat.cs:2393-2508`：道士毒药装备、远程选择和近战兜底。
- `Server/BotSkillSelector.cs:459-666`：道士远程/攻击选择器当前包含防御优先分支。
- `Server/BotManager.Combat.cs:2571-2633`：通用施法门控和施法成功判断。
- `Server/BotManager.Combat.cs:3139-3175`：相邻目标的物理攻击以及距离较远时的追击。

支持动作队列是独立机制。它不被本设计伪装成已修复；实现后必须单独验证支持 Buff 与相邻反击的共存行为。

## 批准行为

### 道士怪物战斗

1. 对有效、存活、可攻击的怪物目标，道士战斗选择器只返回攻击技能，包括施毒、符咒、道士攻击技能以及需要时的近战攻击技能。
2. 防御、治疗、隐身和召唤技能继续由 `ProcessBotTaoistDefenceBuff`、`ProcessBotTaoistSupportBuff`、`ProcessBotTaoistSummon` 等专用支持模块拥有；它们不再作为怪物攻击选择器的输出。
3. 当没有满足当前等级、冷却、魔力、毒药、护身符或目标条件的攻击魔法时，保留同一个有效怪物目标并进入现有物理兜底调用。目标相邻且当前动作门控允许攻击时必须尝试物理攻击；目标较远时继续使用现有追击逻辑。支持模块已经排队的 `ActionTime`/`CanAttack` 延迟仍属于独立的支持动作队列验收项，不在本设计中重构。
4. 不添加新的 Taoist 状态字典、攻击冷却、随机移动或滞回逻辑。
5. 保持低血逃跑、紧急喝药、目标所有权、组队协战、地图安全/Boss 过滤、40 级换图、Wizard、Warrior、Assassin 和 CPU/药水优化语义不变。

这里的“攻击魔法不可用”包括选择器返回 `None`、技能未学习、`NeedLevel1` 未满足、冷却未到、魔力不足、必需毒药或护身符不可用，以及通用施法入口拒绝当前动作。上述情况都必须最终保留目标并走已有物理兜底，而不是清除目标或转入无目标漫游。

### 自动学技能边界

对 `SEnvir.MagicInfoList.Binding` 中的每一条技能记录，按照以下顺序处理：

```text
magic.Class != player.Class
    → 跳过

player.Magics 已包含 magic.Magic
    → 跳过

magic.NeedLevel1 > player.Level
    → 任何路径都不学习、不消耗书

magic.NeedLevel1 <= 35
    → 直接创建 UserMagic

magic.NeedLevel1 >= 36
    → 只进入现有技能书获取/使用链路
```

边界是包含式的：`NeedLevel1 == 35` 直接自动学习；`NeedLevel1 == 36` 只能走技能书路径。`NeedLevel2` 和 `NeedLevel3` 是同一技能后续等级的等级要求，不改变初次学习边界。

“所有 class-appropriate skills”定义为 `MagicInfo.Class` 与 bot 的 `MirClass` 完全匹配。按批准语义，不能再按 `MagicInfo.Action` 或 `MagicInfo.School` 排除条目；被该职业标记的主动、被动、转换和各技能树条目均纳入扫描。

### 高等级 bot 回填

现有 `_botSkillLearnTime` 继续使用 30 秒学习扫描门控。等级大于 35 且已经在线的 bot，不新增专用登录扫描，也不在每个高频战斗 Tick 扫描；它们在下一次正常 30 秒学习扫描中补齐所有缺失且 `NeedLevel1 <=35` 的本职业技能。

登录流程不直接调用 `ProcessBotLearnSkill`，因此“回填”定义为正常学习扫描的最终一致性，而不是登录瞬间完成。

## 架构与数据流

### 战斗职责

- `BotManager` 继续拥有 bot 行为编排、目标保留、支持模块调用和战斗兜底。
- `BotSkillSelector` 的 Taoist 战斗入口只负责攻击技能选择；防御/治疗/召唤选择仍由支持模块调用相应逻辑。
- `TryProcessBotRangedCombatAction` 继续负责距离、施法和追击；它不接收支持类魔法作为怪物攻击输入。
- `ProcessBotMeleeCombatAction` 继续负责相邻目标的物理攻击和较远目标的现有追击，不改变其移动辅助函数或目标状态。
- 低血逃跑与独立 200ms 药水定时器不属于本设计的攻击选择修复范围。

### 学习职责

- `ProcessBotSkillModule` → `ProcessBotLearnSkill` 仍是唯一 bot 自动学习入口，保留现有 30 秒门控。
- 直接学习沿用当前 `UserMagicList.CreateNewObject()` → 设置 `Character`/`Info` → 写入 `player.Magics` → 发送 `S.NewMagic` → `RefreshStats()` 的顺序。
- 技能书路径继续由 `FindBotReadySkillBookSlot`、鉴定/合成/残页/购买辅助方法以及 `player.ItemUse` 驱动；不改变书籍消耗、成功率、数量或经济值。
- `PlayerObject.Magics` 仍以 `MagicType` 为键，现有 `ContainsKey` 检查是重复学习保护。
- `PlayerObject.LearnSkill` 与 `PlayerItem.ItemUse` 的普通玩家路径保持原样；本设计只规定 bot 管理器的选择分支。

### 现有技能书消费者

技能书保留和打书地图评分会读取缺失技能列表。实现时必须确认 `NeedLevel1 <=35` 的自动学习分支先于这些消费者运行；不得把低于或等于 35 级的技能重新当成 bot 的技能书必需目标。除非验证证明需要，不能扩大到地图评分、掉落评分或经济策略的重构。

## 明确不在范围内

- 不修改 `ServerLibrary` 的普通玩家学习、技能书使用、技能数据定义或数据库记录。
- 不修改 Warrior、Wizard、Assassin 的技能选择或攻击顺序。
- 不修改 Taoist 的低血逃跑、紧急喝药、毒药购买数量、护身符经济、组队支援规则或目标保留。
- 不修改 `BotMainSliceIntervalMs=200`、四片调度、约 800ms 主行为、独立 200ms 药水定时器、CPU/药水优化、地图评分、40 级换图和 Boss/安全过滤。
- 不增加新状态字典、冷却缓存、线程、后台循环或随机移动。
- 不修改客户端、脚本、资源、配置、数据库、部署目录、运行中的旧版 `Server.exe` 或备份。
- 不在本阶段实现代码、创建契约、更新 `CHANGELOG.md`、构建或部署。

## TDD 与验收设计

实现阶段必须先创建并运行聚焦源码契约，生产源码修改前必须得到真实 RED。契约必须用括号深度提取完整方法块，不能用会命中无关调用点的局部正则替代。

聚焦契约至少提取：

- `ProcessBotTaoistCombatAction`
- `GetTaoistRangedMagic`
- `GetTaoistAttackMagic`
- `ProcessBotTaoistDefenceBuff`
- `ProcessBotTaoistSupportBuff`
- `ProcessBotTaoistSummon`
- `ProcessBotLearnSkill`
- `ProcessBotSkillModule`

生产修改前的 RED 必须来自当前行为缺失，而不是路径、语法或提取失败：

1. 当前 Taoist 战斗选择器会返回防御类技能；契约应明确失败。
2. 当前 `ProcessBotTaoistCombatAction` 尚未证明“攻击魔法不可用后仍调用同目标物理兜底”；契约应明确失败。
3. 当前学习器只直接处理旧的 20 级边界；契约应因缺少 `NeedLevel1 <=35` 直接学习而失败。
4. 当前大于 20 级的书链没有统一的 `NeedLevel1 <= player.Level` 前置门控；契约应因缺少“所有路径先检查当前等级”而失败。

修改后 GREEN 必须断言：

- Taoist 攻击选择器只会向怪物战斗返回攻击技能。
- 防御、治疗、召唤仍由专用支持模块保留且可达。
- 有效相邻怪物在攻击魔法不可用时进入现有物理兜底调用；没有支持动作门控时应到达 `player.Attack`，有支持动作门控时只验证目标保留和既有动作状态语义。
- `NeedLevel1 <= player.Level` 在直接学习和技能书路径之前统一生效。
- `NeedLevel1 <=35` 直接创建 `UserMagic`；`NeedLevel1 >=36` 不直接创建，只进入现有书链。
- `MagicInfo.Class` 精确匹配，且不按 `Action`/`School` 过滤。
- 已有 `player.Magics.ContainsKey` 防重复和完整通知/刷新顺序不变。
- 30 秒 `_botSkillLearnTime` 门控仍存在，支持等级大于 35 bot 在正常学习扫描中回填。
- 现有 phase1、level40/Assassin、CPU/potion 契约继续通过。
- 非 bot/player 的 `LearnSkill` 与 `PlayerItem.ItemUse` 内容未被修改。

静态契约不能证明真实游戏对象的动作队列、攻击事件或路径移动。因此 GREEN 和 Debug 构建都不能替代人工运行验收。

## 构建边界

实现获批后只使用 Debug/AnyCPU，并输出到隔离目录：

```powershell
& 'C:\Program Files\dotnet\dotnet.exe' build 'ServerLibrary\ServerLibrary.csproj' -c Debug --nologo

& 'C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\MSBuild\Current\Bin\MSBuild.exe' `
    'Server\Server.csproj' /t:Rebuild /m /v:minimal `
    /p:Configuration=Debug /p:Platform=AnyCPU `
    '/p:OutputPath=D:\相聚假人\Source\.build-check\bot-ai-taoist-auto-skill-debug\Server\'
```

构建产物只能留在该隔离目录。没有单独部署授权时不得停止、替换或启动正式服务端。

## 人工运行验收缺口

实现和 Debug 验证完成后，仍需人工确认：

1. 在没有支持动作排队的 Tick 中，10 级道士与相邻有效怪物接触时，在攻击魔法不可用的情况下会在同一目标上物理反击。
2. 防御 Buff、治疗和召唤仍能正常执行；其延迟动作只造成可解释的短暂动作门控，不形成持续站桩。
3. 35 级技能在 `NeedLevel1=35` 时直接学习；`NeedLevel1=36` 在等级 35 时不学习、不消耗书，在等级 36 时只走技能书路径。
4. 已在线且等级大于 35、缺失低阶本职业技能的 bot，会在正常 30 秒学习扫描中补齐，不触发高频战斗扫描。
5. 同等目标、地图、职业比例和负载下，之前已完成的 CPU/药水、地图换图和 Assassin 行为没有运行时回归。

## 风险与缓解

| 风险 | 缓解 |
| --- | --- |
| 删除攻击选择器中的防御输出后，Taoist 可能少一次防御机会 | 保留专用防御/支援模块，并在契约中确认其调用链仍存在 |
| 支持动作队列仍可能让同一 Tick 的攻击门控失败 | 将其作为独立运行时验收项，不用攻击选择器修复掩盖或重构动作队列 |
| `Action`/`School` 不过滤可能纳入被动或转换技能 | 这是已批准的“所有 class 条目”语义；用 `MagicInfo.Class` 作为唯一职业过滤条件 |
| 书链在角色等级不足时提前消耗高阶书 | 所有学习路径先执行 `NeedLevel1 <= player.Level`，等级不足直接跳过 |
| 回填扫描增加单次学习工作量 | 沿用现有 30 秒门控和主 AI 正常学习入口，不加入每 Tick 或独立线程扫描 |
| 重复创建 `UserMagic` 造成持久化或通知异常 | 保留现有 `ContainsKey` 检查和创建、入字典、通知、刷新顺序 |
