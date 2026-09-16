# 道士药粉与护身符自动补给设计

## 状态与范围

本文是已批准设计的实现前规格，不是实现结果。当前阶段只记录现状、边界、数据流、验收和人工缺口；不得据此推断源码已经改变或新行为已经部署。

项目位于 D:\相聚假人\Source，是共享的本地非 Git 树。后续实现只允许触及本设计指定的最小所有权文件，必须使用 Debug/AnyCPU 隔离输出，不能停止、替换或部署旧的 Server.exe。

本设计解决两个相互关联的问题：

1. 道士药粉补给方法 BotBuyPoisonByShape 中选择候选物品的赋值语句被注释，导致黄色药粉和灰色药粉都无法形成有效购买候选。
2. 道士战斗过程在高频路径中直接购买药粉，且护身符补给只覆盖少数技能；需要把购买集中到低频补给边界，并按当前施法需要从背包即时换装。

目标行为是：药粉按 Shape 1/0 低库存补货，护身符按实际 UseAmulet 技能集合、Shape 1..8 普通消耗和 Shape 0 回生术按需补给与换装，同时保留现有战斗、施毒顺序、技能计数、近战 fallback、调度频率和低等级启动补给。

## 已核验的现状证据

### 调度和模块顺序

- D:\相聚假人\Source\Server\BotManager.cs:453-456 保留 200ms 主计时器和 200ms 药水计时器。
- D:\相聚假人\Source\Server\BotManager.cs:1015-1083 的 BotTick 使用四个 slice，每 200ms 处理一个 slice；现有注释和队列行为约等于每个假人 800ms 执行一次主行为。
- D:\相聚假人\Source\Server\BotManager.cs:1389-1491 先执行公共模块、装备和通用补给，再按职业进入职业模块。
- D:\相聚假人\Source\Server\BotManager.cs:1991-2001 的道士顺序是 ProcessBotTaoistSupply、ProcessBotTaoistEquipSupply、召唤、专用防御 buff、专用支持 buff、PK、拾取、战斗。购买边界应留在 Supply，不应由战斗模块另行购买。

### 当前道士补给和购买

- D:\相聚假人\Source\Server\BotManager.Support.cs:2926-2957 已有 _botTaoistBuyTime、BotTaoistSupplyMinCount=100、BotTaoistSupplyBuyCount=500、BotTaoistStarterSupplyCount=50 和 60 秒补给门控相关常量。
- D:\相聚假人\Source\Server\BotManager.Support.cs:2972-2985 的 IsBotUsableTaoistAmuletInfo 目前只承认 ItemType.Amulet 且 Shape 1..8；Shape 0 的灵魂护身符不能通过这一普通护身符判定。
- D:\相聚假人\Source\Server\BotManager.Support.cs:2987-3013 的 GetBotRequiredTaoistAmuletCount 已有按技能消耗数量分组的入口，但补给触发范围仍不是 Aciton.cs 中所有实际调用 UseAmulet 的已学技能。
- D:\相聚假人\Source\Server\BotManager.Support.cs:3016-3082 的 ProcessBotTaoistSupply 是当前 60 秒购买门控。它按 Shape 1 和 Shape 0 统计药粉并在总数低于 100 时请求 500 个；护身符触发目前只检查 ExplosiveTalisman、ImprovedExplosiveTalisman、SummonSkeleton、SummonJinSkeleton、SummonShinsu 五种技能。
- D:\相聚假人\Source\Server\BotManager.Support.cs:3087-3129 的 TryGrantTaoistStarterConsumable 是现有低等级启动补给：仅道士、等级 <=7、背包至少有一个空位且该物品类型总数为零时免费给予 50 个并尝试装备。该路径必须保持，且绝不扩展到等级 >7。
- D:\相聚假人\Source\Server\BotManager.Support.cs:3131-3191 的 BotBuyConsumable 会从 ItemInfoList.Binding 按 ItemType 选候选，调用 TryGetBotDirectBuyCost，按最低直接购买价购买，并在金币不足时降低数量；失败时有金币回滚路径。它当前没有把普通护身符 Shape 1..8、灵魂护身符 Shape 0 分成按需池。
- D:\相聚假人\Source\Server\BotManager.Support.cs:3193-3271 的 BotBuyPoisonByShape 已过滤 ItemType.Poison 和目标 Shape，但 TryGetBotDirectBuyCost 成功后的 bestPrice/bestInfo 赋值在当前源码中被注释，且失败候选没有形成严格的 continue。因此 bestInfo 可能一直为 null，黄色和灰色药粉不能可靠购买。
- D:\相聚假人\Source\Server\BotManager.Support.cs:3620-3710 的 ProcessBotTaoistEquipSupply 现在主要处理装备中的药粉形状切换和普通 Shape 1..8 护身符；它没有 Shape 0 回生术上下文，也没有统一区分“普通技能”和“回生术”的按需换装。
- D:\相聚假人\Source\Server\BotManager.Support.cs:1713-1789 的 BotFallbackDirectBuyRates 包含黄色/灰色药粉小中大变体和多种护身符名称；D:\相聚假人\Source\Server\BotManager.Support.cs:1791-1850 的 TryGetBotDirectBuyCost 会先扫描安全区 NPC 商品，再使用允许的 fallback 价格；D:\相聚假人\Source\Server\BotManager.Support.cs:4619-4631 计算 NPC 商品单价。名称和 Shape 的实际数据库映射不能由 fallback 名称猜测，候选必须以 ItemInfo.Shape 和 TryGetBotDirectBuyCost 的实际成功结果为准。

### 当前高频战斗路径

- D:\相聚假人\Source\Server\BotManager.Combat.cs:2393-2508 的 ProcessBotTaoistCombatAction 每个道士战斗动作都会统计装备和背包中的两种药粉；当前缺粉且金币达到 100 时会直接调用 BotBuyPoisonByShape。该调用违反“购买只在 60 秒补给边界”的目标，必须移除。
- 同一方法 2441-2501 根据目标是否已有红毒/绿毒，按红后绿的顺序确定目标 Shape；装备不匹配时先把旧装备放回空背包位，再从背包找目标 Shape 并 PutOnEquip。这个即时背包换装和红→绿顺序必须保留，但战斗方法不能枚举商店或购买。
- 同一方法 2503-2508 先走 Taoist ranged magic，随后走 Taoist attack magic，最后进入 ProcessBotMeleeCombatAction。补给失败或没有合适技能时不能阻断这条近战 fallback。
- D:\相聚假人\Source\Server\BotManager.Combat.cs:2571-2633 的 TryCastBotMagic 在施法前会按技能需要调用 ProcessBotTaoistEquipSupply，然后检查护身符；成功施毒时会更新 _botTaoistPoisonUseCount 和 _botTaoistLastPoisonCast。D:\相聚假人\Source\Server\BotManager.Combat.cs:2926-2969 的预测施法也有同类护身符检查。计数和记录必须原样保留。
- D:\相聚假人\Source\Server\BotManager.Combat.cs:94、99、135-136 已有药水补货、短缺购买、200ms 监视和 800ms 重试边界；本设计不改变这些常量、四片调度或约 800ms 主行为。

### ItemInfo、装备槽和实际消耗

- D:\相聚假人\Source\Library\SystemModels\ItemInfo.cs:34-47 定义 ItemType，:136-149 定义 Shape，:204-217 定义 Price，:238-251 定义 StackSize。
- D:\相聚假人\Source\Library\Enum.cs:2161-2210 定义 EquipmentSlot.Poison=10、EquipmentSlot.Amulet=11；:3097-3158 定义 ItemType.Poison 和 ItemType.Amulet。
- D:\相聚假人\Source\ServerLibrary\Models\Player\PlayerItem.cs:556-590 的 PutOnEquip 负责库存物品与当前装备交换、入队和 RefreshStats；:6192-6219 的 UsePoison 要求已装备药粉并按 Shape 消耗；:6227-6288 的 UseAmulet 要求已装备护身符并按精确 Shape 消耗。
- D:\相聚假人\Source\ServerLibrary\Models\Player\Aciton.cs:2693-2744、2765-2820、2845-2884、2900-2920、2929-2941、2951-3030、3039-3069、3078-3118、3129-3143、3188-3241、3260-3349、3370-3380、3406-3448 是当前道士实际 UseAmulet 调用块。源码核验出的技能集合为：
  - 普通 Shape 1..8、消耗 1：ExplosiveTalisman、ImprovedExplosiveTalisman、EvilSlayer、GreaterEvilSlayer、GreaterHolyStrike、MagicResistance、ElementalSuperiority、SummonSkeleton、Neutralize。
  - 普通 Shape 1..8、消耗 2：Resilience、BloodLust、LifeSteal、TrapOctagon、SummonJinSkeleton、Invisibility、MassTransparency、MassInvisibility、Purification。
  - 普通 Shape 1..8、消耗 5：SummonShinsu、StrengthOfFaith。
  - 普通 Shape 1..8、消耗 10：Transparency、CelestialLight。
  - 普通 Shape 1..8、消耗 20：DemonExplosion。
  - 普通 Shape 1..8、消耗 25：SummonDemonicCreature。
  - Shape 0、消耗 1：Resurrection。Aciton.cs:3348 明确调用 UseAmulet(1, 0)，并带有灵魂护身符注释。

其中 EvilSlayer、GreaterEvilSlayer、GreaterHolyStrike 的源码块只有在装备满足 HolyAffinity 条件时消耗护身符；该条件必须保留。上面的集合是当前源码的 UseAmulet 事实集合，不是数据库名称推断。后续 focused contract 必须从完整 brace-depth 方法块检查这些分组 case，不能只用最后一个 case 标签或只保留当前五项。

## 目标行为与固定规则

### 药粉

1. BotBuyPoisonByShape 只接受同时满足 ItemType.Poison、目标 Shape、TryGetBotDirectBuyCost 成功的候选。对每个成功候选使用实际直接购买价，选择最便宜候选；未成功的直接购买价不能参与 bestPrice/bestInfo 比较。
2. 选择候选与计算可购买数量分开：先选最便宜且有直接购买价的 ItemInfo，再沿用现有批量约 500、金币不足时按可负担数量缩减、CanGainItems 检查、扣金、创建物品、GainItem 和异常回滚顺序。不能把“买不起整批”误判成候选不存在。
3. ProcessBotTaoistSupply 是唯一购买边界，并继续使用现有约 60 秒 _botTaoistBuyTime 门控。只有在黄色药粉 Shape 1 的装备加背包总数低于 100 时补约 500；灰色药粉 Shape 0 同样独立判断、独立补货。两个 Shape 不能合并为一个库存池。
4. 金币不足时购买当前金币能负担的数量；若数量为零则安全返回并保留装备与金币。不得在战斗 tick 中为凑够最低金币而购买，也不得发放等级 >7 的免费药粉。
5. 现有等级 <=7 启动补给 TryGrantTaoistStarterConsumable 保持原条件、数量、GainItem 和装备尝试；它不是普通战斗购买的替代路径。

### 护身符

1. 购买触发由一个统一的、基于 MagicType 的 eligibility/消耗量/Shape 模式 helper 提供。该 helper 是所有实际 UseAmulet 技能的唯一来源：返回普通 Shape 1..8 或 Shape 0 回生模式，以及对应的现有每次消耗量；非 UseAmulet 技能返回不适用。不得再在 ProcessBotTaoistSupply 中复制五个技能的 if 分支。
2. 只对已学习的道士技能评估补给。若已学集合中存在至少一个使用普通护身符的技能，统计装备加背包的普通护身符池（Shape 1..8）；池总数低于 100 时，在 60 秒补给边界购买约 500 个最便宜、ItemType.Amulet、Shape 1..8 且 TryGetBotDirectBuyCost 成功的候选。无需囤齐八种 Shape，不做固定轮换。
3. 若已学习 Resurrection，独立统计 Shape 0 灵魂护身符池；池总数低于 100 时在同一 60 秒边界购买约 500 个最便宜、ItemType.Amulet、Shape 0 且 TryGetBotDirectBuyCost 成功的候选。当前 Aciton.cs 只有 Resurrection 明确使用 Shape 0；不得把普通 Shape 1..8 误当作灵魂护身符。
4. 普通技能施法只使用当前可购买且可装备的 Shape 1..8 护身符。当前装备仍是有效 Shape 1..8 且数量足够时不切换；当前装备为空、Shape 不在 1..8 或数量不足时，只扫描一次背包并换入可用的 Shape 1..8。没有固定 Shape 轮换，也不依据怪物抗性频繁切换护身符。
5. Resurrection 施法前使用同一个按需换装 helper：当前不是 Shape 0 或数量不足时，只扫描背包并换入 Shape 0；无 Shape 0 时安全失败。回生施法结束后，下一次普通技能需要时再按 mismatch 规则换回 Shape 1..8，不为恢复普通形状增加每 tick 扫描。
6. 所有实际 UseAmulet 技能都进入统一 eligibility。对于 EvilSlayer 系列，保留 Aciton.cs 中 HolyAffinity 条件；对于其它技能保留对应消耗数量、目标和技能选择逻辑。不得通过猜测数据库中文名、ItemInfo 名称或 Shape 映射扩大集合。
7. 护身符不足、无商品、无金币、无空背包位、PutOnEquip 失败或装备交换异常时安全返回；旧装备仍在装备槽或已成功交换到背包时都必须保持可恢复，不扣除未成功交易的金币，不发放免费物品，不阻断同一 tick 的普通物理攻击 fallback。

### 战斗边界

- ProcessBotTaoistCombatAction 不得调用 BotBuyPoisonByShape、BotBuyConsumable、任何直接商店购买 helper，也不得扫描 SEnvir.ItemInfoList 或 NPC 商品。它只负责目标毒状态判断、必要的背包即时换装、技能选择、施毒顺序、计数/记录和原有 melee fallback。
- TryCastBotMagic 及预测施法只可调用不购买的装备检查/背包换装 helper；当技能所需护身符不能满足时返回原有失败结果，由外层继续既有 fallback。
- 目标已有毒状态的顺序保持：没有红毒先使用 Shape 1；已有红毒但没有绿毒再使用 Shape 0。不得因为护身符优化改变这一顺序。

## 数据流和职责

实现后的最小数据流如下：

1. 200ms BotTick 经过四片调度，约每 800ms 进入一次假人主行为；BotManager 不增加新的调度器或线程。
2. 道士进入 ProcessBotTaoistSupply 时先执行现有死亡、职业和 60 秒 gate。gate 未到期立即返回。gate 到期后，使用统一的已学技能 eligibility 分别评估 Shape 1/0 药粉和普通/灵魂护身符池。
3. Supply 仅在池低于 100 时调用按 Shape 的购买 helper。购买 helper 只查直接购买价、选择最低价候选、按金币缩减数量并完成现有交易/回滚。
4. 后续 ProcessBotTaoistEquipSupply 或施法前装备检查只处理当前装备与目标技能所需 Shape 的 mismatch/数量不足；它只读背包并调用 PutOnEquip，不触发购买，不扫描商店。
5. ProcessBotTaoistCombatAction 根据目标毒状态进行药粉 mismatch 换装，保留红→绿；TryCastBotMagic 根据 UseAmulet 需求进行普通或 Shape 0 护身符换装。换装成功才进入原有施法调用。
6. 若施法技能不能完成，原有技能选择和 ProcessBotMeleeCombatAction 路径继续生效；补给失败不能把目标清空或把近战 fallback 变成购买循环。

支持代码的职责边界固定为：

- BotManager.Support.cs：60 秒补给门控、按 Shape 的药粉/护身符候选购买、统一 UseAmulet eligibility、库存统计、仅背包换装和低等级启动补给。
- BotManager.Combat.cs：移除战斗内直接购买，调用仅换装的支持 helper，保留目标毒状态、施法计数/记录和 ranged-to-melee 顺序。
- BotSkillSelector.cs：本需求只读保护；不调整道士攻击技能、毒/符优先级或自适应选择。
- BotManager.cs：本需求只读保护；不调整 200ms/四片/约 800ms 行为。
- ServerLibrary 的 PlayerItem.cs、Aciton.cs：本需求只读保护；它们是装备交换和实际消耗的事实来源。

## 明确非目标

- 不囤满八种普通护身符，不固定轮换 Shape，不按怪物抗性频繁切换护身符。
- 不在战斗路径购买任何药粉或护身符，不增加每 tick 商店枚举，不增加线程、计时器、缓存字典或诊断日志。
- 不改变 BotPotionMonitorIntervalMs=200、BotPotionRetryIntervalMs=800、BotMainSliceIntervalMs=200、现有 60 秒道士购买 gate、药粉/护身符经济价格、批量目标、技能优先级、目标所有权、地图安全或 Boss 过滤。
- 不改变玩家/非假人学习或购买逻辑，不改变通用药水 monitor、应急喝药和金币支持。
- 不修改 BotManager.cs、BotSkillSelector.cs、PlayerItem.cs、Aciton.cs、数据库、资源、客户端、部署树或旧 Server.exe。
- 不把数据库中的中文物品名、fallback 名称或 Shape 编号关系作为未经源码和 ItemInfo 核验的事实。

## 失败语义和安全性

按以下顺序处理失败：

1. TryGetBotDirectBuyCost 失败、候选 ItemType/Shape 不匹配或没有合格候选：不改金币、不改装备、不创建物品，返回失败。
2. 金币少于整批：以当前实际单价计算可负担数量；数量为零则返回失败。不能通过负数、免费发放或跳过扣金制造物品。
3. CanGainItems 失败或背包没有交换空位：保持当前装备和库存，返回失败。
4. 扣金、CreateFreshItem、GainItem 或回滚路径抛出异常：沿用现有 BotBuyConsumable 的回滚语义，确保交易失败不留下已扣金币的假成功。
5. PutOnEquip 失败或交换异常：不清空装备槽，不把战斗变成重复购买；TryCastBotMagic 返回原有失败，外层按原顺序允许物理近战 fallback。
6. 等级 >7 的假人永远不走免费启动补给；等级 <=7 只保留现有空背包、零库存启动条件。

## 性能边界

- 购买只发生在 ProcessBotTaoistSupply 的现有 60 秒 gate 内；200ms potion timer、200ms BotTick、四片调度和每个 bot 约 800ms 主行为不变。
- 商店/NPC 商品枚举只由低频购买 helper 经由 TryGetBotDirectBuyCost 触发；战斗路径零商店枚举。
- 装备不匹配或数量不足才触发一次背包扫描；装备已经满足当前技能 Shape 时不扫描、不换装、不买货。
- 不新增 per-bot cache dictionary、轮换状态、后台线程、计时器或日志。复用现有 _botTaoistBuyTime、库存和装备模型。
- 静态 contract 和 Debug build 只能证明源结构、编译和隔离产物，不能证明 CPU、私有字节、托管堆或本机分配下降。CPU/内存结论必须通过同负载人工 A/B。

## 最小所有权与保护

后续实现的最小可写范围：

- D:\相聚假人\Source\Server\BotManager.Support.cs：购买候选、60 秒补给、统一技能 eligibility、库存统计和仅库存换装。
- D:\相聚假人\Source\Server\BotManager.Combat.cs：删除战斗内购买，接入仅换装路径，保持施毒和 melee fallback。
- D:\相聚假人\Source\.diagnostics\bot-ai-taoist-consumable-supply-contract.ps1：新增 brace-depth focused contract。
- D:\相聚假人\Source\CHANGELOG.md：focused/regression/build 通过后追加当前 bot-AI 区域记录。

必须保护且不得由本需求改动：

- D:\相聚假人\Source\Server\BotManager.cs
- D:\相聚假人\Source\Server\BotSkillSelector.cs
- D:\相聚假人\Source\ServerLibrary\Models\Player\PlayerItem.cs
- D:\相聚假人\Source\ServerLibrary\Models\Player\Aciton.cs
- 所有既有 bot-ai contracts、approved specs/plans、数据库、资源、客户端、部署文件和旧 D:\Debug\4月18日更新\Server\Server.exe。

项目非 Git；不创建 commit、PR、备份，不执行 Git mutation，不部署。

## TDD 和静态验收

### Focused contract

生产修改前必须先创建并运行 D:\相聚假人\Source\.diagnostics\bot-ai-taoist-consumable-supply-contract.ps1。contract 必须用 brace-depth 提取完整方法块，而不是用跨方法正则匹配。至少提取并独立断言：

- BotBuyPoisonByShape
- BotBuyConsumable 或其按 Shape 的购买实现
- ProcessBotTaoistSupply
- ProcessBotTaoistEquipSupply
- ProcessBotTaoistCombatAction
- TryCastBotMagic
- TryCastBotMagicWithPredicton
- 统一的 Taoist UseAmulet eligibility helper
- TryGrantTaoistStarterConsumable

RED 必须是源行为失败而不是路径、解析或语法失败，至少包括：

1. BotBuyPoisonByShape 当前 bestPrice/bestInfo 赋值仍被注释，或失败的 TryGetBotDirectBuyCost 候选仍可参与选择。
2. ProcessBotTaoistCombatAction 当前仍包含战斗内 BotBuyPoisonByShape/直接购买路径。
3. ProcessBotTaoistSupply 当前只用五项护身符技能触发，而非从所有实际 UseAmulet 技能的已学集合驱动。
4. 当前 source path 尚未把 Resurrection 的 Shape 0 和普通 Shape 1..8 放入统一 eligibility/换装规则。
5. 当前护身符购买/换装路径尚未证明“只在 mismatch/不足时扫描背包、战斗不枚举商店、失败不阻断 melee fallback”。

RED 输出必须列出每个失败断言；focused contract 若因方法抽取错误、路径错误或不计数而失败，必须先修复 contract，不得修改生产源码。

GREEN 必须证明：

- 只接受成功的 TryGetBotDirectBuyCost，并按 Shape 选择最低直接价候选；黄色 Shape 1、灰色 Shape 0 分开。
- ProcessBotTaoistSupply 保留 60 秒 gate、100 阈值、约 500 批量、金币缩减和 <=7 启动补给。
- 所有实际 UseAmulet 技能均由单一 eligibility 来源覆盖；普通技能只允许 Shape 1..8，Resurrection 只允许 Shape 0。
- 战斗方法没有购买或商店枚举，只做目标毒状态和必要背包换装；TryCastBotMagic 仍保留施法计数/记录，melee fallback 仍可达。
- 200ms/800ms 常量、BotManager 调度、技能选择和受保护文件未被改动。

### 既有回归和构建

focused GREEN 后依次运行现有只读契约：

- powershell.exe -NoProfile -ExecutionPolicy Bypass -File .diagnostics\bot-ai-phase1-contract.ps1：21 项 PASS。
- powershell.exe -NoProfile -ExecutionPolicy Bypass -File .diagnostics\bot-ai-level40-assassin-contract.ps1：6 项 PASS。
- powershell.exe -NoProfile -ExecutionPolicy Bypass -File .diagnostics\bot-ai-cpu-potion-contract.ps1：21 项 PASS。
- powershell.exe -NoProfile -ExecutionPolicy Bypass -File .diagnostics\bot-ai-assassin-positioning-contract.ps1：行为断言应通过；其对 BotManager.Support.cs 的旧固定 ownership hash 因本需求继续授权 Support.cs 修改，必须记录为 11/12，唯一已解释的 stale ownership hash exception，不能声称四项回归全绿，也不得修改或弱化该旧 contract。

构建命令固定为 Debug：

    & 'C:\Program Files\dotnet\dotnet.exe' build 'ServerLibrary\ServerLibrary.csproj' -c Debug --nologo

    & 'C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\MSBuild\Current\Bin\MSBuild.exe' 'Server\Server.csproj' /t:Rebuild /m /v:minimal /p:Configuration=Debug /p:Platform=AnyCPU '/p:OutputPath=D:\相聚假人\Source\.build-check\bot-ai-taoist-consumable-supply-debug\Server\'

验收要求是两个命令 exit 0、0 compile errors，并记录 warnings；Server.exe 必须存在于 D:\相聚假人\Source\.build-check\bot-ai-taoist-consumable-supply-debug\Server\。不得复制隔离产物到旧部署目录，不得启动或替换旧进程。最终报告应列出 owned/protected 文件 SHA-256、产物路径/大小/SHA-256、允许路径审计和无 instrumentation/额外状态的检查结果。

已有前序实现的基线证据是 focused 36 PASS、phase1 21 PASS、level40 6 PASS、cpu-potion 21 PASS；assassin-positioning 只有上述 Support 固定 hash exception。前序 Debug 构建为 ServerLibrary 0 warnings/0 errors、Server Debug/AnyCPU 16 MSB3277 warnings/0 errors，隔离 Server.exe 为 83,103,744 bytes、SHA-256 D47BC3C8FEFA067DF68309D667E579F3EC5418E2E955B41E87A4BEB5F8267477。旧部署 D:\Debug\4月18日更新\Server\Server.exe 当时为 83,103,744 bytes、SHA-256 6992C33D892CDD67794D9E59CA41B33541843270509165F453346EF584BB5E4D；后续实现必须重新只读核验，不得把隔离产物当作已部署。

## 人工运行验收缺口

静态 contract 和构建完成后，仍必须在不替换当前旧 Server.exe 的前提下，用隔离 Debug/AnyCPU 版本做同负载人工验收：

1. 两种药粉：道士分别缺少黄色 Shape 1 和灰色 Shape 0 时，观察 60 秒补给是否按各自低于 100 触发、选择可购最低价、批量约 500；金币不足时数量是否正确缩减，战斗 tick 是否没有商店枚举或即时购买。
2. 药粉即时换装：目标无红毒时装备 Shape 1，已有红毒无绿毒时装备 Shape 0；确认红→绿、施法次数和 _botTaoistLastPoisonCast 记录不变。
3. 普通护身符：逐一使用实际普通 UseAmulet 技能，确认 Shape 1..8 中已有合适库存时只在空、Shape 不合格或数量不足时换装，不囤满八种，不按怪物抗性轮换。
4. Shape 0：等级和技能条件允许的道士施放 Resurrection 时，确认能按需购买/保有灵魂护身符、施法前切到 Shape 0；之后普通技能需要时能换回 Shape 1..8，且不在每个 tick 重复扫描。
5. 技能覆盖：逐项覆盖当前 Aciton.cs 的 UseAmulet 集合，特别是分组 case、EvilSlayer 的 HolyAffinity 条件、MassTransparency/MassInvisibility、Purification、DemonExplosion、Neutralize，确认购买触发不再只限五项。
6. 边界失败：无商品、无金币、背包满、旧装备无法交换、PutOnEquip 失败时，确认金币和装备安全、无等级 >7 免费物品、当前目标仍能走物理近战 fallback。
7. 性能与内存：旧版与新隔离版在相同 bot 数、地图、目标、补给和战斗负载下各运行至少五分钟，分别记录总 CPU/每逻辑处理器 CPU、working set、private bytes、managed heap 和必要的 native/address-space 指标；确认商店枚举只在 60 秒边界、装备扫描只在 mismatch/不足时触发。4.9GB private bytes 不能单凭数值判定泄漏。

最终人工结果必须分别记录成功或失败；未完成这些项目时，只能报告静态/build 完成，不能声称运行时已接受，也不能声称 CPU、内存或喝药优化已经得到实测证明。

## 风险与缓解

- 风险：候选 ItemInfo 名称与 NPC 商品名不一致。缓解：只用 ItemInfo.ItemType/Shape 和 TryGetBotDirectBuyCost 成功结果，不写死数据库名称映射。
- 风险：Shape 0 被普通护身符过滤器拒绝。缓解：按技能上下文使用统一 requirement，普通和 Resurrection 使用不同 Shape 模式。
- 风险：把购买逻辑留在战斗路径造成 CPU 回归。缓解：focused contract 对 Combat 完整方法块断言无购买/商店枚举，购买只允许位于 Supply 的 60 秒 gate。
- 风险：背包换装失败清空装备或阻断攻击。缓解：沿用 PutOnEquip 的交换语义，失败安全返回，保留原目标、技能选择和 melee fallback。
- 风险：只覆盖当前五项护身符技能。缓解：以 Aciton.cs 所有实际 UseAmulet case 为 source of truth，并在 contract 中检查完整分组。
- 风险：静态检查通过但运行时经济或性能不正确。缓解：保留旧 Server.exe 不变，隔离 Debug/AnyCPU，执行同负载五分钟 A/B 和边界人工验收。

这份设计到此闭合：实现范围、购买边界、Shape 规则、错误语义、性能约束、所有权、测试和人工验收均已固定；当前没有生产源码或运行时行为变更。
