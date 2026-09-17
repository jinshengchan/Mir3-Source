# 更新日志

## 2026-09-17 - 战士假人不攻击修复

- 修复战士假人先尝试蓄力技能失败后仍占用攻击节流，导致普通攻击分支在每个 AI 周期都被跳过的问题。
- 蓄力失败时恢复原有攻击尝试状态；不改变选怪、走位、技能选择和其他职业逻辑。
- 清理战士专项临时诊断日志与异常输出，保留正式回归契约 `test_warrior_failed_charge_releases_attack_attempt.ps1`。
- 实机验证：战士假人已恢复攻击；回归契约通过；服务端 Debug/AnyCPU Rebuild 为 `0` 错误，仅保留项目原有 `MSB3277` 程序集版本冲突警告。

## 2026-08-20 - 假人 AI 40级练级换图与刺客技能修正（源码完成，待在线验证）

- 普通练级原先虽然计算更优地图，但不会采纳候选；现在仅让 `40` 级以上、非打金且非组队跟随的假人在候选评分高于当前地图至少 `25` 分时换图，原有安全、Boss、打金和组队规则保持不变。
- 怪物战斗不再强制刺客进入纯物理回退，复用现有范围、目标、突进和近战技能选择链；战士、法师与道士逻辑未改。
- 聚焦契约完成 RED（`4 passed / 2 failed`）到 GREEN（`6 assertions`），一期回归契约 `21 assertions` 通过；`ServerLibrary` Release 为 `0` 警告、`0` 错误，`Server` Release 为 `0` 错误，仅保留项目原有 `System.Runtime.InteropServices.RuntimeInformation` 版本冲突警告。隔离产物为 `.build-check/bot-ai-level40-assassin-release/Server/Server.exe`，未覆盖或部署正式服务端。
- 待在线验证：40级以上假人是否在明显更优地图出现时换图，以及刺客对怪时是否按学习状态、距离、冷却和魔力正常施放技能。

## 2026-08-20 - 假人 AI 低蓝药水重复扫描优化（源码完成，待在线验证）

- 通用 `TryCastBotMagic` 与 `TryCastBotMagicWithPredicton` 在魔力不足时直接返回失败，不再在独立药水定时器之外同步调用普通药水监控；其他紧急/支援药水入口、刺客技能、40级换图和 200ms 调度保持不变。
- 非紧急 `ProcessBotPotionMonitor` 在现有 `_botPotionCooldownTime` 检查后预留 `800ms` 再次检查时间；成功用药仍以真实药品冷却覆盖该预留，HP `<=15%` 继续绕过预留执行紧急追药。
- 聚焦契约先按预期 RED（`15 passed / 6 failed`），修改后 GREEN（`21 assertions`）；一期回归契约 `21 assertions`、40级/刺客契约 `6 assertions` 均通过。契约为完整私有方法块的源码结构检查，不能替代运行时性能测量。
- `ServerLibrary` Debug 构建为 `0` 警告、`0` 错误；`Server` Debug/AnyCPU 重建退出码 `0`、`0` 错误，仅输出既有 `MSB3277 System.Runtime.InteropServices.RuntimeInformation` 版本冲突诊断。主任务最终隔离重建产物为 `.build-check/bot-ai-cpu-potion-debug/Server/Server.exe`，大小 `83,103,744` 字节，SHA-256 `4792F0274A74CDC0B9352ACFBD593DBC2E1179F387936B0AC2206416B0D672BA`。
- 未停止或替换当前旧版 `Server.exe`，未部署；待相同假人数量、职业比例和地图负载下完成旧版/新版至少 5 分钟 CPU/药水 A/B，并另行采集 managed/native 内存证据。

## 2026-08-20 - 假人 AI 刺客近距离重定位振荡修正（源码完成，待在线验证）

- 根因：刺客在距离 `1` 且目标魔法可选时沿用首选距离 `2` 的重定位分支，先后退；目标魔法未能施放时，同一 tick 继续进入突进/近战回退，下一 tick 又重新接近同一目标，形成近/远振荡。
- 修复：`TryProcessBotRangedCombatAction` 的首选距离重定位仅适用于非刺客；刺客仍按原目标魔法、突进和近战顺序处理，法师与道士的首选距离行为不变，未增加状态或冷却。
- 聚焦契约先按预期 RED（`11 passed / 1 failed`，唯一失败为缺少 `MirClass.Assassin` 排除），修改后 GREEN（`12 assertions`）；一期、40级/刺客和 CPU/药水回归契约分别为 `21`、`6`、`21 assertions PASS`。
- `ServerLibrary` Debug 构建为 `0` 警告、`0` 错误；`Server` Debug/AnyCPU 隔离重建退出码 `0`、`0` 错误，保留 `12` 条既有 `MSB3277` 程序集版本冲突警告，未覆盖或部署正式服务端。
- 待在线验证：在相同目标、地图、职业和负载下确认刺客不再因目标魔法可用而从距离 `1` 后退，并完成旧版/新版 CPU、药水与 managed/native 内存 A/B；静态契约和构建不能替代实机验收。

## 2026-08-20 - 假人 AI 道士攻击选择与自动学技能（源码完成，待在线验证）

- 症状：10级道士取得有效相邻怪物目标后可能发呆不反击；直接原因是 GetTaoistRangedMagic 与 GetTaoistAttackMagic 在攻击选择前优先返回可用防御技能，使通用远程路径消耗战斗决策。
- 修复：仅删除两个攻击 selector 内的防御优先说明、defenseMagic 调用和 immediate return 块；专用 ProcessBotTaoistDefenceBuff、ProcessBotTaoistSupportBuff、ProcessBotTaoistSummon、原有 ActionTime 延迟以及 range→melee fallback 保持不变，未修改 GetTaoistQuickDefenseMagic 或 Combat。
- 自动学技能：保持 class match 与 duplicate guard，先要求 NeedLevel1 <= player.Level；NeedLevel1 <= 35 直接按原 UserMagic/通知/刷新属性序列学习，NeedLevel1 >= 36 自然进入原 ready-book、鉴定、精炼、合成、购买链；未增加 Action、School、NeedLevel2/3 过滤，保留30秒扫描。
- TDD/回归：focused contract RED 31 passed / 5 failed，selector 中间 RED 33 passed / 3 failed，最终 GREEN 36 assertions；phase1 21、level40/Assassin 6、CPU/potion 21 assertions 通过。bot-ai-assassin-positioning-contract.ps1 为 11/12，唯一失败是旧固定 BotManager.Support.cs 基线哈希 F71C4EFE90ABC9843A19E9802F94C09AA5B4615FDE084D7BF5ED5C4CA702130F 与本次授权修改冲突，行为断言和其他保护断言通过，契约未修改。
- 构建：ServerLibrary Debug 为 0 警告、0 错误；Server Debug/AnyCPU 重建退出码 0、16 条既有 MSB3277 警告、0 错误。隔离产物 .build-check/bot-ai-taoist-auto-skill-debug/Server/Server.exe 大小 83,103,744 字节，SHA-256 D47BC3C8FEFA067DF68309D667E579F3EC5418E2E955B41E87A4BEB5F8267477。
- 未部署、未停止或替换旧版 Server.exe。待在线验证：①无支援动作且无可用道术时10级道士相邻怪普攻；②有可用道术时技能释放及施法失败后的近战回退；③召唤/防御/支援动作与 ActionTime 共存；④NeedLevel1 35/36边界；⑤35级以上各职业假人在30秒扫描中的技能回填；⑥旧版/新版同负载 CPU、私有字节/工作集、managed/native 内存和喝药 A/B。

## 2026-08-21 - 假人 AI 道士药粉与护身符按需补给（源码完成，待在线验证）

- 修复 `BotBuyPoisonByShape` 候选赋值被注释及失败 direct-cost 候选仍可能进入购买的问题；购买边界仅为每 `60` 秒一次的 `ProcessBotTaoistSupply`。黄粉 `Shape 1`、灰粉 `Shape 0` 库存分别低于 `100` 时按约 `500` 补货，金币不足时按可负担数量缩减，`<=7` 级启动补给保留；fallback direct-buy 成本补充当前数据库九种全角小型护身符名称（普通、狂风、霹雷、幻影、寒气、神圣、火焰、暗黑、灵魂），ItemType/Shape 仍为资格与切换依据。现有 `Gold <= 0` 初始化路径中，道士一次获得 `100,000 + 200,000 = 300,000` 金币，其他职业仍为 `100,000`，正金币假人不重复补足。
- 所有源码核验的 `UseAmulet` 技能普通按 `Shape 1..8`、`Resurrection` 按灵魂护身符 `Shape 0` 按需购买/换装；不依赖硬编码 ItemName→Shape 映射。战斗路径不购买或枚举商店，仅在装备不匹配/数量不足时从背包换装，保留红→绿施毒顺序、施毒计数/last-cast 记录和 melee fallback；召唤不再被无上下文 `Shape 0` 预检卡住。
- TDD/回归：focused `37 PASS / 0 FAIL`；auto-skill `35 PASS / 1 FAIL`（唯一为 `BotManager.Combat.cs` 旧固定哈希例外）；phase1 `21 PASS`；level40/Assassin `6 PASS`；CPU/potion `21 PASS`；assassin-positioning `11 PASS / 1 FAIL`（唯一为 `BotManager.Support.cs` 旧固定哈希例外）。因此不宣称全部回归全绿、运行时修复或性能改善。
- 构建：`ServerLibrary` Debug 退出码 `0`、`0` 警告、`0` 错误；`Server` Debug/AnyCPU 退出码 `0`、`16` 条既有 `MSB3277` 警告、`0` 错误。隔离产物 `.build-check/bot-ai-taoist-consumable-supply-debug/Server/Server.exe` 大小 `83,104,768` 字节，SHA-256 `026B66DC6E6B23C03DBEF661CD00943042D24D36E8569236E469F23A482673A7`。
- 未部署、未复制或替换旧版 Server.exe。待人工验证：数据库中两种药粉/普通及灵魂护身符的 Shape、价格和可购买性；真实战斗中的红→绿换粉与近战回退；Resurrection 的 Shape 0 换入及普通技能换回；以及相同负载至少 5 分钟的 CPU、工作集/私有字节、managed/native 内存和喝药 A/B。观察客户端的 `LeftBuffBox.Process` 负宽度已在客户端侧钳制，Taoist Buff 文本和倒计时逻辑不变；Direct3D 实机观察仍待确认。

## 2026-08-20 - PC 世界地图高亮素材范围校正（待实机确认）

- 按世界图标注范围重制五张无文字黑边素材，道馆命中区校正为 `98×97 @ (540,103)`；索引 `39..43` 已更新，聚焦契约与 Release/AnyCPU 重建通过。

## 2026-08-19 - PC 世界地图新增五个高亮区域（待实机确认）

- `BigMapDialog` 新增道馆、灌木林、永丰长城、义马林、迷失地域五个高亮映射，并将透明高亮素材写入 `WorldMap.Zl` 索引 `39..43`；现有区域与数据库文件保持不变。

## 2026-08-18 - PC 大地图详情资源兼容（待实机确认）

- `BigMapDialog` 按当前 DB 的 `FileName` 与地图名称共同确认详情：数据库没有“潘夜村落”时，点击该高亮区域留在世界地图，不再误开“毒蛇山谷”；其他有效区域继续按当前 DB 详情索引，保留奔马岛 `302`、D009/D3904 世界图行为及顶部“世界地图”标题。契约及 Release/AnyCPU 重编译通过，未修改资源或数据库。

## 2026-08-15 - PC 韩版/145 共享大地图世界区域映射修正（待实机确认）

- `BigMapDialog` 世界区域改用当前 DB `FileName` 唯一解析，同时保留韩版显示名、世界高亮索引和韩版 MiniMap 索引；修正 19 项区域映射，奔马岛使用 `302`；D009 月河渊、D3904 额头族部落无当前 DB 记录时留在世界图；同一地图点击强制详情刷新且不修改 `MapInfo.MiniMap`。
- 聚焦契约完成 RED→GREEN；Release/AnyCPU Rebuild 退出码 `0`、`0 errors`，仅既有 `BigPatchConfig.ChkLockMonEffect` CS0649 warning，输出 `D:\Client\Mir3.exe`；未修改资源/数据库，未覆盖或部署受保护 Debug 客户端。剩余为实机 Direct3D 悬停、逐区点击、NPC 列表和详情图像确认。

## 2026-08-13 - PC 韩版/145 共享大地图世界图切换（待实机确认）

- 共享 `145Client\Scenes\Views\BigMapDialog.cs` 增加当前位置默认视图、`WorldMap.Zl` 索引 `0` 的全部地图视图、全部地图/当前位置文字按钮、地图名称搜索框与搜索按钮/回车；搜索按 `MapInfo.Description` 精确匹配优先、部分匹配其次，空输入或未匹配不改变当前显示；现有当前地图标记、寻路与 `InitCurrentPath` 保留。
- TDD：`.diagnostics\test_pc_big_map_world_view_contract.ps1` 源码修改前按预期 RED（`PASS: shared BigMapDialog implementation` 后 `FAIL: world-map display state`）；修改后 GREEN，世界图资源/索引、两个按钮、地图名称数据源、精确优先部分匹配和现有寻路入口断言全部 PASS。
- 构建：`145Client.csproj` Release/AnyCPU Rebuild 退出码 `0`、`0 errors`；仅保留既有 `BigPatchConfig.ChkLockMonEffect` CS0649 warning，输出为 `D:\Client\Mir3.exe`；未覆盖或部署 `D:\Debug\4月18日更新\Client\Mir3.exe`。
- 修改文件：`145Client\Scenes\Views\BigMapDialog.cs`、`.diagnostics\test_pc_big_map_world_view_contract.ps1`、`CHANGELOG.md`。剩余验证为真实 Direct3D 客户端中的窗口布局、按钮命中和切换视觉确认。
- 本轮补全：`GameInter.Zl` 已证明使用 `6100` 金色大地图框、`6172/6177` 当前位置/全部地图、`6187` 搜索图标、`6190` 金边输入框；WorldMap 区域按原版 `FileName -> WorldMap[20..38] -> hitbox` 映射，悬停使用 `6164` 标题动画；详细地图显示 `Globals.NPCInfoList.Binding` 中属于 `SelectedInfo` 的 NPC 列表与皮肤滚动条，世界总览隐藏列表，NPC 寻路仅限当前地图。
- 本轮缺陷修复：世界区域由稳定命中 panel 自身处理悬停/点击，高亮层保持穿透且不再重挂；详细地图 NPC 列表保留金色选中框并在目标坐标显示 14px 黄色目标点，非当前地图不跨图寻路；MovementInfo 出入口名称作为图标子控件常驻；关闭按钮固定在金框右上角并置于子控件绘制层之上。契约 GREEN；Release/AnyCPU Rebuild 退出码 0、0 errors，仅有既有 CS0649 警告，未部署。
- 最终验证：契约新增完整素材、NPC/滚动条、世界区域悬停/点击与当前地图寻路断言并通过；Release/AnyCPU Rebuild 退出码 `0`、`0 errors`，仅有既有 `BigPatchConfig.ChkLockMonEffect` CS0649 warning，输出 `D:\Client\Mir3.exe`，未部署或覆盖 Debug 客户端。
- Runtime correction (2026-08-14): world hover highlight now follows the hovered region, authoritative titles use explicit `DisplayName` values, and `DisplayName + FileName` uniquely resolves clickable maps while missing `D009`/`D3904` records remain on the world map. Pass-through hover layers use stable z-order; the independent top-level UI1 index `1221` close artwork now uses standard `DXButton` behavior without `FourStatu`. The NPC target marker remains 9px and movement destination labels remain direct `Image` children with map-switch/remove/dispose cleanup. Contract GREEN; Release/AnyCPU Rebuild succeeded with only the existing CS0649 warning. Output `D:\Client\Mir3.exe`; Debug client not overwritten or deployed.

## 2026-08-13 - 假人 AI 第一期：自卫链、装备评分与 30 人错峰（源码完成，待在线验证）

- 自卫受击链：`ServerLibrary` 在假人受到真人或其宠物主人的有效伤害后发布通知，`BotManager` 沿用现有威胁、社交和攻击模式记录；普通地图仍不主动搜索或攻击玩家。
- PK 修正：威胁只接受同地图、最大视野内且可合法反击的玩家；修正逃跑方向映射、达到 10 格后的逃跑结束、战士 `false` 风筝状态、同行会自检和队友集火威胁主体。
- 装备评分：背包自动换装、双槽排序、商店升级和交易保留统一使用职业加权评分；基础/附加属性保留正负号，负属性不再因绝对值变为加分。
- 30 人调度：主 AI 改为 4 个稳定的 200ms 调度片，每名假人仍约 800ms 完成一次主行为；登录、记忆和组队维护每四片执行一次；移除主管线重复喝药，保留独立 200ms 与战斗紧急喝药；跨线程防积压集合增加最小锁保护。
- 未改范围：金币、免费技能、符毒和药品库存扶持数值未改；未增加红名、敌对行会或 Boss 争夺主动 PK；未处理服务端启动内存峰值；未修改客户端、UI、脚本或正式服务端目录。
- TDD：`.diagnostics/bot-ai-phase1-contract.ps1` 在旧源码为 `0 passed / 19 failed`；补充安全距离语义和伤害结算重入断言后，修改版最终为 `21 assertions PASS`。
- 构建：`ServerLibrary` Release 为 0 警告、0 错误；`Server` Release 为 0 错误，保留项目原有 `System.Runtime.InteropServices.RuntimeInformation` 版本冲突警告。隔离产物为 `.build-check/bot-ai-phase1-release/Server.exe`，未覆盖运行服务端。
- 待在线验证：真人及宠物攻击假人后的反击/风筝/逃跑、30 个假人高密度打怪的 CPU/主循环帧耗时、职业装备选择结果。

## 2026-08-11 22:06 - PC 韩版职业徽标、聊天回车与技能图标回退修正（已部署，待实机确认）

- 原生边框复原（2026-08-12）：韩版窗口仅使用 `GameInter2.Zl:800-803` 职业顶框与 `810` 主体（`420×66 + 420×446`）；关闭通用 `DXWindow` 皮肤、标题与顶边框，移除额外职业徽标视口。分类图案不再重复绘制，实际 `MagicSchool` 组仅通过透明 `60×22` 命中区（`x=53,y=40`，每项递增 `60`）点击；列表背景/边框透明，145 UI 与共享文件保持隔离。
- 本轮验证：专项契约 PASS；Release/AnyCPU Rebuild 退出码 `0`、`0` errors，仅既有 `BigPatchConfig.ChkLockMonEffect` CS0649 warning。构建源文件 `D:\Client\Mir3.exe` 与正式部署文件 `D:\Debug\4月18日更新\Client\Mir3.exe` 均为 `3,963,392` 字节，SHA-256 均为 `A3CA1E2C282822E35D41D59BF437428FFDB6A5DFB933EAE159B63D49DFFD0550`。未创建新备份，沿用回滚备份 `D:\Debug\4月18日更新\Client\Mir3.exe.bak-20260811-222634-pc-korean-emblem-chat-soul-icon`，SHA-256 `621C9B8911508B8A73C80EE9933CD609AF733CF32FA25E45C5C6D753343F0332`；`Mir3.ini` 未改变，SHA-256 `1B8D5FDFB88A9F47962D406B468336A8F2DF85641F6D0A0BFF219CFFECDD698C`；正式 `GameInter2.Zl` 未改变且与英雄参考一致，SHA-256 `FC86F5EEC5414E4680A0ADDB0886E8296684A566FA97EF6A11218E56F1213195`。剩余检查为真实 Direct3D 客户端中确认韩版边框、分类命中区、滚动、关闭和移动行为。

- 顶栏视觉复正（本次）：韩版职业徽标/分类条由整体居中改为从 `KoreanListLeft=14` 起始；保持 `48×46` 视口、子图 `(0,-22)` 裁剪、800-803 索引和分类按钮顺序/交互不变；未改资源、数据库、145 UI 或字符数逻辑。
- 本次复正构建：Release/AnyCPU 重建退出码 0、0 错误，仅有既有 `BigPatchConfig` CS0649 警告；输出 `D:\Client\Mir3.exe`，大小 `3,963,392` 字节，SHA-256 为 `725102495B291BBBC9804D2F9A6D67F676EC5E1CCD0F542657ED9F157CE73F72`，生成时间 `2026-08-11 22:33:59.375`。主任务随后将该输出正式部署，未创建新备份，沿用既有回滚备份。

- 顶栏：`GameInter2.Zl:800-803` 继续使用原职业素材，但改为放入不可交互的 `48×46` 视口，子图以原尺寸在 `(0,-22)` 裁剪出实际职业徽标；分类按钮只按视口宽度排版，保持在 `423px` 窗口内。
- 聊天：回车/连续回车仅在 `!GameScene.Game.ChatBox.Visible` 时隐藏 `ChatTextBox`；聊天记录框可见时不再因韩版分支被隐藏。`Globals.MaxChatLength` 字符数逻辑未改。
- 图标：仅对 `MagicType.AugmentEvilSlayer` 在韩版行显示时将缺失的 `Info.Icon=526` 回退到 `524`，构造和已学/未学刷新后均重新应用；未修改数据库、`MagicInfo.Info.Icon`、技能逻辑或 145 UI。
- 证据：从 `D:\Video\英雄客户端\Data\MIcon.Zl` 与正式客户端旧 `D:\Video\客户端\客户端\Data\MIcon.Zl` 解码的 `458`（移花接木）和 `504`（屠龙斩）均为 `36×36`，逐像素差异为 `0`；未重映射这两个图标，也未复制或重建资源。
- 回退证据：`D:\Video\英雄客户端\Data\MIcon.Zl:526`、`D:\Video\英雄客户端\Data\145MIcon.Zl:526` 与正式客户端 `D:\Client\Data\MIcon.Zl:526` 均无图像；英雄 `MIcon.Zl` 的 `520/522/524` 均存在且为 `36×36`，解码 PNG SHA-256 均为 `8E2694E530B990180E0C6B25B1553C9FD596F3F4D942A3774863B5CFB1B526F7`。
- 构建与部署：上一中间版本正式部署文件的 SHA-256 为 `8A7B5A84F209AF2FC6F60414FB486E546AD2F601A6B4631090476772D91072D2`；主任务已将本次左对齐修正正式部署为 `D:\Debug\4月18日更新\Client\Mir3.exe`，大小 `3,963,392` 字节，SHA-256 为 `725102495B291BBBC9804D2F9A6D67F676EC5E1CCD0F542657ED9F157CE73F72`；未创建新备份，复用既有回滚备份 `D:\Debug\4月18日更新\Client\Mir3.exe.bak-20260811-222634-pc-korean-emblem-chat-soul-icon`，备份 SHA-256 为 `621C9B8911508B8A73C80EE9933CD609AF733CF32FA25E45C5C6D753343F0332`。
- 配置与验证：`Mir3.ini` 未覆盖或重写，最终 SHA-256 为 `1B8D5FDFB88A9F47962D406B468336A8F2DF85641F6D0A0BFF219CFFECDD698C`；专项契约通过，Release/AnyCPU 重建为 0 错误，仅保留既有 `BigPatchConfig` CS0649 警告。
- 剩余验证：进入游戏执行 Direct3D 视觉确认左对齐职业徽标/分类条。
- 修改文件：`145Client\Scenes\Views\MagicDialog.Korean.cs`、`145Client\Scenes\Views\ChatTextBox.cs`、`.diagnostics\test_pc_korean_magic_list_contract.ps1`、`CHANGELOG.md`。

## 2026-08-11 19:30 - PC 韩版魔法技能分类与图标修正（待实机确认）

- 根因：韩版列表把 `Passive`、`Neutral`、`Unconditional` 合并到 `WeaponSkills`，导致战士技能全部出现在一类；同时列表沿用了现客户端的 `MIcon.Zl`，图标与参考素材不一致。
- 分类：韩版改为按数据库原始 `MagicInfo.School` 分组并按职业稳定排序；战士显示武器技能、被动、通用三类，只绘制当前职业实际存在的分类，并过滤 `None`、`InternalSkill`。145 技能树逻辑保持不变。
- 顶栏：使用 `GameInter2.Zl:800-803` 对应职业徽标，徽标固定 `48×46`、不可点击且鼠标穿透；分类按钮使用 `Interface.Zl:53-67`，在 `423px` 窗口内居中排列。
- 图标隔离：`LibraryFile.MagicIcon` 单独映射到 `Data/KoreanMIcon.Zl`，文件来源为 `D:\Video\英雄客户端\Data\MIcon.Zl`；`MagicIcon145` 仍映射原 `Data/MIcon.Zl`，未覆盖原图标库或数据库。
- 修改文件：`145Client\Scenes\Views\MagicDialog.Korean.cs`、`Library\Libraries.cs`、`.diagnostics\test_pc_korean_magic_list_contract.ps1`。
- 验证：专项契约先按新规则 RED，修正后由 Luna Max 与主任务分别运行均为 GREEN；Release/AnyCPU Rebuild 0 错误，仅保留原有 `BigPatchConfig.ChkLockMonEffect` CS0649 警告。
- 部署：`D:\Debug\4月18日更新\Client\Mir3.exe`，SHA-256 `621C9B8911508B8A73C80EE9933CD609AF733CF32FA25E45C5C6D753343F0332`；新增 `Data\KoreanMIcon.Zl`，SHA-256 `63F9A8E75E695A7DF64D21EFAD8AF01A9DA8938B8187789ED5C748EF7FCEA14A`。
- 覆盖前备份：`D:\Debug\4月18日更新\Client\Mir3.exe.bak-20260811-1930-pc-korean-magic-list`，原 SHA-256 `EFF961409405BE995E98D43CADAE46BAF01C4EA65BBA70C45AC00BB9B7CE1E45`。
- 剩余验证：进入韩版 UI，确认职业徽标不可点击、战士顶部只有三个分类按钮且能切换对应列表、野蛮冲撞/烈火剑法等技能图标与参考图一致；再切换 145 UI 确认原技能树和图标不变。

## 2026-08-10 22:58 - PC 韩版聊天输入区加长加高（待实机确认）

- 韩版中间深色文字输入区由局部 `(60,8)、295x20` 调整为 `(48,5)、308x28`，左侧更靠近聊天模式按钮，右边缘 `48 + 308 = 356`，精确停在右侧三角按钮前，不与其重叠。
- 生产源码仅修改 `145Client\Scenes\Views\ChatTextBox.cs` 的韩版输入尺寸和局部位置两个表达式；`400x38` 组合尺寸、聊天模式按钮 `(0,0)`、三角按钮 `(356,0)`、上一轮整体下移 `+18px`、145 `560x20` 路径均保持不变。
- 用户明确取消 EXE 文件大小优化；本轮未修改 `FodyWeavers.xml`、`145Client.csproj`、依赖嵌入规则或调试符号设置。Release 文件仍为 `3,954,176` 字节。
- Luna Max 实现任务：继续使用 `019fe127-d36a-7141-bf0e-e6da6650db96`；focused contract 修改前因缺少 `(48,5)、308x28` 按预期 RED，修改后 GREEN。新增 `pc-korean-chat-input-area-size-contract.ps1`，同步更新 4 个仅受旧几何影响的契约断言。
- 主任务复验：14 个非 `config-reader` PC 双界面源码契约全部 GREEN；配置读写契约 GREEN；Release/AnyCPU Rebuild 0 错误，仅保留项目原有 `BigPatchConfig.ChkLockMonEffect` CS0649 警告。
- 部署：确认 `Mir3` 进程未运行后，仅覆盖 `D:\Debug\4月18日更新\Client\Mir3.exe`，未重复创建备份；SHA-256 `3A2A471E7138044380D52AAE70107DBA5CE7BA4D55E56DA6EDB2318C66BC6451`。
- 配置：`D:\Debug\4月18日更新\Client\Mir3.ini` 未覆盖、未改写，部署后 SHA-256 仍为 `3568911A16D3207A2E927584F85F678651F971573EEAC7F9B7ADBB846B581C67`。
- 剩余验证：需要在真实 Direct3D 客户端中确认输入区的长度、高度、文字垂直位置，以及左右按钮点击区域均正常。

## 2026-08-10 22:11 - PC 韩版聊天输入组合下移与输入区右移（待实机确认）

- 韩版聊天输入组合相对底部主面板锚点整体下移 `18px`，聊天记录框继续相对输入组合定位，因此两者保持原相邻关系并同步靠近底部 UI。
- 韩版实际文字输入区由局部 `(2,8)` 改为 `(60,8)`，从左侧聊天模式按钮右边开始；输入区仍为 `295x20`，右边缘位于 `X=355`，不覆盖从 `X=356` 开始的三角按钮。
- 仅修改 `145Client\Scenes\GameScene.cs` 与 `145Client\Scenes\Views\ChatTextBox.cs` 的韩版位置表达式；145 原定位、`218 → 166 → 118 → 隐藏 → 218` 循环、回车隐藏、按钮素材和命中区均保持不变。
- Luna Max 实现任务：继续使用 `019fe127-d36a-7141-bf0e-e6da6650db96`；先取得仅缺少 `+18` 与 `(60,8)` 的 focused RED，再修改到 GREEN。新增 `pc-korean-chat-input-bottom-align-contract.ps1`，同步更新 3 个只因旧 `(2,8)` 坐标失效的契约断言。
- 主任务复验：13 个非 `config-reader` PC 双界面源码契约全部 GREEN；配置读写契约 GREEN；Release/AnyCPU Rebuild 为 0 错误，仅保留项目原有 `BigPatchConfig.ChkLockMonEffect` CS0649 警告。
- 部署：确认 `Mir3` 进程未运行后，仅覆盖 `D:\Debug\4月18日更新\Client\Mir3.exe`，未重复创建备份；文件大小 `3,954,176` 字节，SHA-256 `5C50F675EBAA6D7B313E786FB3B0BA63836DC31B06E70CC7D9CA857D4E245B81`。
- 配置：`D:\Debug\4月18日更新\Client\Mir3.ini` 未覆盖、未改写，部署后 SHA-256 仍为 `3568911A16D3207A2E927584F85F678651F971573EEAC7F9B7ADBB846B581C67`。
- 剩余验证：需要在真实 Direct3D 客户端中确认输入组合贴近底部 UI、深色输入区从聊天模式按钮右侧开始且三角按钮可正常点击。

## 2026-08-10 21:27 - PC 韩版聊天单一三角、三档循环与回车隐藏（待实机确认）

- 韩版聊天记录框尺寸循环改为 `218px（▼）→ 166px（▼）→ 118px（▼）→ 隐藏（▲）→ 218px（▼）`；进入游戏和隐藏后恢复均从 `218px` 开始。
- 移除韩版聊天记录框内独立的 `ExpendButton/ShrinkButton` 三角及其专用创建方法；输入框右侧 `ChangeButton` 成为唯一尺寸/隐藏控制，韩版聊天窗口快捷键也转发给该按钮。145 界面继续使用原有独立按钮路径。
- 韩版输入框未显示时第一次按回车会重新显示并取得焦点；输入状态下第二次按回车沿用原发送/清空逻辑后隐藏整个输入框，空文本同样隐藏；新增恢复条件只响应 `Enter`，不会被同分支的 `Space` 误触发。145 回车规则未改。
- 韩版 `GameInter:3503` 背景层设置为不绘制，去掉输入框横向阴影；输入控件、聊天模式按钮、右侧三角的位置和命中区域均未改，资源文件未修改。
- 修改文件：`145Client\Scenes\Views\ChatDialog.Korean.cs`、`145Client\Scenes\Views\ChatTextBox.cs`、`145Client\Scenes\GameScene.cs`；设计与计划：`docs\superpowers\specs\2026-08-10-pc-korean-chat-single-triangle-enter-hide-design.md`、`docs\superpowers\plans\2026-08-10-pc-korean-chat-single-triangle-enter-hide.md`。
- TDD：新增 `pc-korean-chat-single-triangle-enter-hide-contract.ps1`，修改前按预期 RED，修改后 GREEN；同步更新 6 个被新规格取代的旧契约断言，最终 12 个 PC 双界面源码契约全部 GREEN，配置读取/写回契约 GREEN。
- 构建：VS 2022 MSBuild 对 `145Client.csproj` 执行 Release/AnyCPU Rebuild，0 错误，仅保留项目原有 `BigPatchConfig.ChkLockMonEffect` CS0649 警告。
- 部署：确认 `Mir3` 进程已关闭后，仅覆盖 `D:\Debug\4月18日更新\Client\Mir3.exe`；文件大小 `3,954,176` 字节，SHA-256 `899A9D0F3421972D39B60F6C0A2EA64A66E7FDA71D2A8C8D06B6E584762CFDA4`。按用户要求未重复创建备份。
- 配置：`D:\Debug\4月18日更新\Client\Mir3.ini` 未覆盖、未改写，本次部署前后 SHA-256 均为 `3568911A16D3207A2E927584F85F678651F971573EEAC7F9B7ADBB846B581C67`。
- 剩余验证：需在真实 Direct3D 客户端中确认三档高度、隐藏/恢复方向、独立三角消失、两次回车隐藏/再次打开、正常发送、输入阴影消失，以及 145 界面保持原样。

## 2026-08-10 00:08 - PC 韩版聊天布局按第二次示范坐标修正（待实机确认）

- 根据用户最新明确坐标重新校准韩版聊天组合：聊天记录框 `X=0, Y=74`，金色输入底框 `X=0, Y=240`，实际文字输入区 `X=2, Y=248`。
- 根因：上一版误把文字输入区放在金色底框下方，形成截图中的上下双层横向阴影；正确关系是文字输入区嵌入金色底框内部，局部偏移为 `(2,8)`。
- 最小源码改动：`145Client\Scenes\Views\ChatDialog.Korean.cs` 的默认第三档高度由 `168` 改为 `166`；`145Client\Scenes\Views\ChatTextBox.cs` 的韩版组合高度由 `58` 改为 `38`，文字输入位置由 `(0,38)` 改为 `(2,8)`。金色素材仍为局部 `(0,0)`、`380×38`，聊天模式按钮、三角按钮、其他缩放档位和 145 界面均未改。
- 坐标复核：`240-166=74`，`240+8=248`，`0+2=2`，与用户三个示范坐标逐项一致。
- TDD：聚焦契约修改前按预期 RED（缺少 `166 / 38 / (2,8)`），修改后 GREEN；同步更新 5 个旧坐标契约后，11 个 PC 双界面源码契约全部 GREEN，旧 `168 / 58 / (0,38)` 断言扫描为零；配置读取/写回契约 GREEN。
- 构建：VS 2022 MSBuild 对 `145Client.csproj` 执行 Release/AnyCPU Rebuild，0 错误，仅保留原有 `BigPatchConfig.ChkLockMonEffect` CS0649 警告。
- 部署：确认两个 `Mir3` 进程均已关闭后，仅覆盖 `D:\Debug\4月18日更新\Client\Mir3.exe`；文件大小 `3,954,176` 字节，SHA-256 `C31A9008C3B08CA77CCC38A0C715DF88B7424127564DA040687581154557BFC3`。按用户要求未重复创建备份。
- 配置：`D:\Debug\4月18日更新\Client\Mir3.ini` 未覆盖、未改写，本次部署前后 SHA-256 均为 `3568911A16D3207A2E927584F85F678651F971573EEAC7F9B7ADBB846B581C67`。
- 剩余验证：需要在真实 Direct3D 客户端中确认金色底框与输入区只绘制一层、文本可正常点击输入，以及四档缩小/隐藏循环仍符合预期。

## 2026-08-09 23:42 - PC 韩版聊天示范坐标与怪物窗口双界面隔离修正（待实机确认）

- 按用户拖拽示范坐标固定韩版首次布局关系：聊天记录框 `Y=18`、金色输入底框 `Y=186`、实际文字输入区 `Y=224`；首次聊天记录高度使用现有 `168px` 档位，记录框底部与金色底框顶部严格相接，无空隙、无重叠。
- 韩版聊天输入组合改为 `400×58`：`GameInter.Zl:3503` 金色底框位于局部 `(0,0)`、尺寸 `380×38`，实际文字输入区位于 `(0,38)`，聊天模式按钮位于 `(0,0)`，右侧三角按钮位于 `(356,0)`；背景启用排序后置，避免遮挡按钮。145 界面输入布局保持原样。
- 韩版聊天记录区的内部背景、文字面板和滚动条均延伸到记录窗口底边，消除原先底部残留的 `2px` 透明缝；四档缩小、隐藏和重新展开循环保持不变。
- 怪物信息窗口按界面类型隔离：韩版保留可移动窗口、人物移动时隐藏、鼠标移出不消失及真实 `70%` 内容背景；145 界面恢复原有 `240×120` 固定窗口、鼠标移出清空和原始布局，互不串用。
- 修改文件：`145Client\Scenes\GameScene.cs`、`145Client\Scenes\Views\ChatDialog.Korean.cs`、`145Client\Scenes\Views\ChatTextBox.cs`、`145Client\Scenes\Views\MonsterDialog.cs`；同步更新对应只读契约断言。
- 验证：11 个 PC 双界面源码契约全部 GREEN；配置读取/写回契约 GREEN；VS 2022 MSBuild 对 `145Client.csproj` 执行 Release/AnyCPU Rebuild，0 错误，仅保留原有 `BigPatchConfig.ChkLockMonEffect` CS0649 警告；fresh Sol 终审结论为 `ship`。
- 部署：仅覆盖 `D:\Debug\4月18日更新\Client\Mir3.exe`，文件大小 `3,954,176` 字节，SHA-256 `995380FCF52CB4CF35F5B8F057A09723233DE5AC1B31443F17683BBC48D53A05`；按用户要求未重复创建备份。
- 配置：`D:\Debug\4月18日更新\Client\Mir3.ini` 未覆盖、未改写，部署前后 SHA-256 均为 `B376F3D14E13753C061177DE637E096E470E7B124DCC98555251CD6DEA765B00`。
- 剩余验证：需在真实 Direct3D 客户端中确认首次显示坐标、四档缩放/隐藏循环、输入控件点击、韩版怪物窗口移动/透明度，以及切换到 145 界面后的原始怪物窗口行为。

## 2026-08-09 21:35 - PC 斜向场景阴影、聊天边界与怪物信息修正（待实机确认）

- 斜向移动阴影：`145Client\Models\UserObject.cs` 将最终场景移动偏移统一为偶数像素，消除斜向移动时树木、房屋半透明阴影在奇偶像素之间闪烁；Mir2 偏移、帧、反转及其他移动逻辑未改。
- 韩版聊天边界：`145Client\Scenes\GameScene.cs` 与 `145Client\Scenes\Views\ChatDialog.Korean.cs` 的聊天记录窗口默认定位和四级尺寸循环定位均向上移动 8px，避免压住输入框组合素材；聊天高度、行数、滚动条及隐藏循环不变。
- 怪物信息行为：人物处于 `Moving` 或 `Pushed` 时隐藏怪物信息窗口并跳过当帧刷新；人物停止且仍有有效鼠标/焦点怪物时恢复。鼠标移出不主动清空，ESC 和对象移除规则保持不变。
- 怪物信息外观：`145Client\Scenes\Views\MonsterDialog.cs` 的内容背景不透明度由 `0.85F` 改为 `0.7F`，信息文字由 8F 调为 9F；窗口边框、血条、文字和三角按钮不整体变淡。
- 设计与计划：`docs\superpowers\specs\2026-08-09-pc-scene-motion-chat-monster-correction-design.md`、`docs\superpowers\plans\2026-08-09-pc-scene-motion-chat-monster-correction.md`。
- TDD：新增 `pc-scene-motion-chat-monster-contract.ps1`，修改前 7 项 RED、修改后 GREEN；原有 9 个源码 UI 契约全部 GREEN。旧综合契约仅将怪物区段搜索上限由 1800 放宽为 2400 字符，判定语义未变。配置读写程序集契约 GREEN。
- 构建：VS 2022 MSBuild，`145Client.csproj` Release/AnyCPU Rebuild，0 error；仅保留原有 `BigPatchConfig.ChkLockMonEffect` 的 CS0649 warning。
- 部署：`D:\Debug\4月18日更新\Client\Mir3.exe`，3,949,568 字节，SHA-256 `CF991F194C4542427E00AAA78E2921F9332D0690968925F557603E2D64DBF65E`。按用户要求未重复创建备份。
- 配置：`D:\Debug\4月18日更新\Client\Mir3.ini` 未覆盖、未改写；部署前后 SHA-256 均为 `B376F3D14E13753C061177DE637E096E470E7B124DCC98555251CD6DEA765B00`。
- 剩余验证：需在真实 Direct3D 客户端中斜向连续经过树木/房屋，并检查四级聊天边界、人物移动隐藏怪物窗、停止恢复、70% 背景和 9F 字体是否符合视觉预期。

## 2026-08-07 - 恢复源码标准 Server.exe 直接启动

- 按 `Server\\Server.csproj` 的 Debug 配置重新编译，使用源码内嵌的 `Server.exe.licenses`、Costura 依赖和 `D:\\相聚\\.tools\\devexpress-23.2` 引用；未使用自定义启动器或 `ServerCore.exe`。
- 标准产物已覆盖 `D:\\Debug\\4月18日更新\\Server\\Server.exe`、`Server.exe.config`、`Server.pdb`，保留覆盖前备份：`Server.exe.bak-20260807-source-standard`、`Server.exe.config.bak-20260807-source-standard`、`Server.pdb.bak-20260807-source-standard`。
- 验证：直接启动部署后的 `Server.exe`，窗口标题为“Z3服务端”，进程保持运行且 `Responding=True`；程序集包含 `Server.exe.licenses`、`costura.license.dll.compressed` 和 26 个 DevExpress 内嵌资源。

## 2026-08-07 - Server.exe 可直接双击启动 Debug 服务端

- 按用户要求，恢复直接执行 `Server.exe` 的使用方式；新增无 DevExpress 依赖的 x64 启动壳 `Server.exe`，自动调用同目录 `启动服务端.cmd`，由批处理设置 `DEVPATH` 后运行实际 Debug 服务端 `ServerCore.exe`。
- `ServerCore.exe` 为此前已验证的 Debug/x64 服务端，保留 Debug 免授权、退出崩溃修复、DevExpress 嵌入资源和原业务逻辑；`Server.exe` 启动壳使用原 `Server\main.ico`，图标为 32×32。
- 启动壳使用独立配置：移除 `Server.exe.config` 中的 `developmentMode`，避免启动壳在进入代码前扫描损坏 GAC；完整配置保存在 `ServerCore.exe.config`，核心程序继续使用 `developmentMode` 和 `DEVPATH`。
- 验证：直接执行 `D:\Debug\4月18日更新\Server\Server.exe` 后自动启动 `ServerCore.exe`，窗口标题为“Z3服务端”，`Responding=True`；无需手动运行 `.cmd`。
- 覆盖前备份：`D:\Debug\4月18日更新\Server\Server.exe.bak-20260807-bootstrap-direct-cmd`（SHA-256：`4A071E78349BD7C973C05F7349A589DA13DC5D0F687471CDCA245F990EC613DE`）、`D:\Debug\4月18日更新\Server\Server.exe.config.bak-20260807-bootstrap-minimal`、`CHANGELOG.md.bak-20260807-direct-server-exe`。

## 2026-08-07 - 服务端改为 Debug 模式无需授权

- 按用户确认改用项目现有 Debug 授权规则，不修改、不删除授权校验代码；`Server.Helpers.LicenseHelper.CheckLicense()` 的 Debug 分支返回 `LicenseState.DebugMode`（枚举值 `102`，显示“Debug模式无需授权”）。
- `Server.csproj` 的 `Library.dll` 引用改为按 `$(Configuration)` 自动选择 Debug/Release 输出，避免 Debug 服务端错误嵌入 Release 库；`ServerLibrary` Debug 编译 0 警告、0 错误，完整服务端 Debug/x64 编译 0 错误，仅保留项目原有的 `RuntimeInformation` 4.0.1/4.0.2 警告。
- 验证：成品为 PE32+（x64），包含 `Server.exe.licenses`、`costura.library.dll.compressed` 和 26 个 DevExpress 资源；IL 反汇编确认 `CheckLicense()` Debug 末支返回 `102`；退出崩溃回归测试通过。
- 同时修正 `Server.ini` 的授权文件路径：原路径 `D:\mir3\Server\B177-79C9-0C58-3798-16C2.license` 不存在，改为实际文件 `D:\Debug\4月18日更新\Server\B177-79C9-0C58-3798-16C2.license`；配置保持原 UTF-16 LE 编码。
- 已覆盖 `D:\Debug\4月18日更新\Server\Server.exe`，SHA-256：`04A4167F83274CF8F47B1EFE3E1CCF36711D19351EE1F6D5168C374883CEAD64`；通过 `启动服务端.cmd` 真实启动后窗口标题为“Z3服务端”，进程持续运行且 `Responding=True`。
- 覆盖前备份：`D:\Debug\4月18日更新\Server\Server.exe.bak-20260807-release-license-invalid`（SHA-256：`A70A02C2A51585928AF9F89C919E768CD0284B2F07ACFC7B19774D3B81A06EB9`）、`D:\Debug\4月18日更新\Server\Server.ini.bak-20260807-license-path`（SHA-256：`37549E603EFF13537733BF532AE3217763C3D839E7B74EA71EAED37169232850`）、`CHANGELOG.md.bak-20260807-debug-no-license`。
- DevExpress 说明：新安装的 GAC 程序集虽然 26/26 可读取程序集信息，但直接执行 `BonusSkins.Register()` 仍以 `0xC0000005` 崩溃；当前继续使用已验证通过的 `developmentMode + DEVPATH` 专用启动脚本，不直接双击 `Server.exe`。
- 图标检查：当前 Debug `Server.exe`、覆盖前 Release 备份和项目 `Server\main.ico` 提取出的 32×32 图标 PNG 哈希完全一致，确认程序内图标资源未丢失；截图中的白色默认图标来自资源管理器同路径缓存，已发送单文件 Shell 更新通知并刷新图标缓存，未再次修改或覆盖 `Server.exe`。更新日志备份：`CHANGELOG.md.bak-20260807-server-icon-cache`。

## 2026-08-07 - 绕过损坏的 DevExpress GAC 并恢复服务端启动

- 根因：本机 Windows GAC 中 26 个 DevExpress 23.2.6 程序集中有 25 个为损坏文件；CLR 优先读取损坏的 `DevExpress.BonusSkins.v23.2.dll`，因此在 `Server.Program.Init()` 调用 `BonusSkins.Register()` 时抛出 `BadImageFormatException`。7 月 30 日旧服务端与当前服务端主程序均验证为有效程序集，重复编译不能修复系统 GAC。
- 最小绕过：在正式 `Server.exe.config` 的 `<runtime>` 中增加 `<developmentMode developerInstallation="true" />`；新增 `启动服务端.cmd`，启动前把 `DEVPATH` 指向服务端目录下的 `DevExpress23.2` 英文目录联接，再启动原 `Server.exe`。未修改服务端业务源码、数据库、脚本或 DevExpress DLL。
- 中文路径兼容：`cmd.exe` 会误读无 BOM UTF-8 中文依赖路径，因此新增目录联接 `D:\Debug\4月18日更新\Server\DevExpress23.2`，目标为 `D:\相聚\.tools\devexpress-23.2`；启动脚本仅使用 `%~dp0DevExpress23.2`。
- 验证：独立 `BonusSkins.Register()` 测试返回 `PASS`；随后通过 `启动服务端.cmd` 真实启动，`Server.exe` 进程持续运行，窗口标题为“Z3服务端”，状态 `Responding=True`，不再弹出 `BadImageFormatException`。
- 配置覆盖前备份：`D:\Debug\4月18日更新\Server\Server.exe.config.bak-20260807-before-devpath`，SHA-256：`5003D42EB2F4F7B6693DE532ACF8412FC43BE8238C8E33301148A4543AC43B47`；更新日志备份：`CHANGELOG.md.bak-20260807-devexpress-gac-bypass`。
- 说明：系统 GAC 中的损坏文件仍未被管理员权限修复；今后应使用 `启动服务端.cmd` 启动。若后续以管理员权限重新正确安装 DevExpress 23.2.6，可再移除此绕过配置。

## 2026-08-07 - 按 2026-07-30 22:35 方式重新编译并部署服务端

- 回溯确认旧版采用 Release 构建、x64 目标，复用原服务端内嵌的 `Server.exe.licenses`，并从 `D:\相聚\.tools\devexpress-23.2` 解析 DevExpress 23.2 编译依赖。
- 将服务端直接引用的 `Library.dll` 从 Debug 输出切换为 Release 输出；`ServerLibrary` Release 编译为 0 警告、0 错误，完整 `Server.exe` 编译无错误，仅保留项目原有的 `System.Runtime.InteropServices.RuntimeInformation` 4.0.1/4.0.2 冲突警告。
- 新成品验证为 PE32+（x64），包含 `Server.exe.licenses`、`costura.library.dll.compressed` 和 26 个 DevExpress 嵌入资源；`.diagnostics\test_disconnect_visibility_contract.ps1` 验证通过。
- 已覆盖 `D:\Debug\4月18日更新\Server\Server.exe`，SHA-256：`A70A02C2A51585928AF9F89C919E768CD0284B2F07ACFC7B19774D3B81A06EB9`。
- 覆盖前备份：`D:\Debug\4月18日更新\Server\Server.exe.bak-20260807-before-release-x64`，SHA-256：`1C51CC2002EA835DD7CF99852F3A1AEA68B4B8EF8AC3A9F23CC3295FC320545E`；更新日志备份：`CHANGELOG.md.bak-20260807-release-x64-deploy`。

## 2026-08-07 - 修复玩家退出导致服务端崩溃

- 根因：`PlayerObject.StopGame` 在清理可见对象时，玩家的 `CurrentMap` 已被 `Despawn` 清空；`MapObject.CanBeSeenBy` 仍继续读取 `CurrentMap.Info`，触发空引用并终止服务端主循环。
- 最小修复：在 `ServerLibrary\Models\MapObject.cs` 的 `CanBeSeenBy` 中，复用同文件 `CanDataBeSeenBy` 已有的空地图规则；任意一方没有当前地图时直接返回不可见。
- 构建同步：公共 `ClientFriendInfo` 缺失但服务端已在使用的 `IsBot` 布尔字段，已按工程保留旧版本原样补回；仅用于恢复服务端库编译。
- 影响范围：只影响退出、断线、切图等对象清理期间的可见性判断；不修改八大暗影脚本、战斗、掉落、封包或客户端逻辑。
- 免安装构建：从官方签名的 `DevExpressComponentsBundleSetup-23.2.6.exe` 使用 `-E` 参数提取 `23.2.6.0` Framework DLL；复用原 `Server.exe` 内嵌的 `Server.exe.licenses`，并以预编译 `Library.dll` 完成完整服务端构建。未运行第三方 Patch/Keygen，临时项目配置已恢复。
- 验证：`.diagnostics\test_disconnect_visibility_contract.ps1` 修复前失败、修复后通过；`ServerLibrary` Debug/Release 均为 0 错误、0 警告；完整 `Server.exe` 编译成功并确认包含 `Server.exe.licenses` 与内嵌 `Library.dll`。
- 部署：已覆盖 `D:\Debug\4月18日更新\Server\Server.exe`，SHA-256 为 `12A9842B75D734A91A97A7ED4FE88BF1C39F7F892D01CA857802CC0240AE9C78`。
- 覆盖前备份：`ServerLibrary\Models\MapObject.cs.bak-20260806-disconnect-visibility-nullmap`、`Library\Globals.cs.bak-20260806-client-friend-isbot`、`Server\Server.csproj.bak-20260807-portable-devexpress-build`、`CHANGELOG.md.bak-20260806-disconnect-visibility-nullmap`、`D:\Debug\4月18日更新\Server\Server.exe.bak-20260807-disconnect-visibility-nullmap`。

## 2026-08-06 - 修复八大暗影“开始挑战”操作失败

- 根因：八大暗影脚本在每日次数检查和写入时引用 `GV_BADA_COUNT`，但该变量未在 `Defines.py` 定义；服务端日志报 `global name 'GV_BADA_COUNT' is not defined`，因此点击“开始挑战”直接显示“操作失败”。
- 最小修复：新增 `GV_BADA_COUNT = 105`，编号经现有变量表核对为空闲；并在 `Ser\定时活动.py` 的 `OnDayChange` 中将其重置为 `0`。保留原脚本“每天一次”的既定规则。
- 未修改八大暗影的收费、地图、怪物、奖励、活动管理员入口或其他全局变量。
- 验证：`.diagnostics\test_bada_shadow_daily_reset.ps1` 先失败于缺失变量，修复后通过；`Defines.py` 和 `八大暗影.py` 通过 Python 2.7 语法检查。`定时活动.py` 使用 IronPython 专属中文模块导入，不能由 CPython 编译，但每日重置调用已被契约检查确认存在。
- 覆盖前备份：`Defines.py.bak-20260806-bada-shadow-daily-count`、`定时活动.py.bak-20260806-bada-shadow-daily-count`、`CHANGELOG.md.bak-20260806-bada-shadow-daily-count`。

## 2026-08-06 - 八大暗影入口移至活动管理员

- 八大暗影入口改接入现有“活动管理员”（NPC 332）：主菜单新增“八大暗影”，菜单 `80` 打开副本说明、`81` 开始挑战、`82` 刷新状态。
- 保留活动管理员原有菜单；根因是同一 NPC 的 `OnClick` 只能注册一个处理器，不能把八大暗影直接再绑定到 NPC 332。现由活动管理员转交上述菜单到八大暗影原有逻辑。
- 取消八大暗影原 NPC `5656` 的点击事件注册；副本地图 `387` 的 `OnEnter`、`OnLeave`、`OnCreate` 事件保持不变，进入费用 `500` 元宝、每层 `50` 元宝、怪物、奖励、每日次数和并发规则均未修改。
- 修改文件：`D:\Debug\4月18日更新\Server\Scripts\Npc\活动管理员.py`、`D:\Debug\4月18日更新\Server\Scripts\Npc\BOSS副本\八大暗影.py`；验证脚本：`.diagnostics\test_bada_shadow_activity_manager.py`。
- 验证：菜单转交行为测试通过；两份脚本均通过 Python 2.7 语法检查；八大暗影旧 NPC 监听已移除，三项地图事件仍存在。上线后需在服务端执行“重新加载脚本”或安全重启，再在游戏内完成一次入口与扣费验证。
- 覆盖前备份：`活动管理员.py.bak-20260806-bada-shadow-activity-manager`、`八大暗影.py.bak-20260806-bada-shadow-activity-manager`、`CHANGELOG.md.bak-20260806-bada-shadow-activity-manager`。

## 2026-08-06 - PC 装备比较框自动宽度与左右等高

- 根因：右侧人物装备比较框以固定 `190` 像素宽度起步，不能完全按实际文字内容收缩；左侧“装备外观｜物品属性”共同框和右侧比较框分别计算高度，导致上下边框不齐。
- 右框初始宽度改为 `0`，继续复用现有 `AddEquipmentCompareLabel()` 按每行文字位置与实际宽度自动扩展，不修改文字、属性或差值列位置。
- 左框先根据装备外观和物品属性计算基础高度；若右框内容更高，左框自动扩展到右框内容高度。右框随后同步左框最终高度，中间竖线和左侧属性区域也使用同一高度，避免任一侧文字越框。
- 仅修改 `145Client\Scenes\GameScene.cs`；宠物背包、角色装备栏、普通道具说明、人物四向边界、未装备隐藏差值和魔法窗口规则均保持不变，未修改服务端、封包、安卓端或资源文件。
- 设计与计划：`docs\superpowers\specs\2026-08-06-pc-equipment-compare-auto-size-design.md`、`docs\superpowers\plans\2026-08-06-pc-equipment-compare-auto-size.md`。
- 验证：修改前自动宽度、三方最大高度和右框同步三项检查均为 `False`；修改后自动尺寸及既有规则共 `12` 项检查全部通过，PC Debug 编译成功。客户端 SHA-256：`6DF9C11FD56FDF591D05BB47D9828E74A1409FA4CB2695F596409B48FA6105CA`。
- 覆盖前备份：`145Client\Scenes\GameScene.cs.bak-20260806-equipment-compare-auto-size`、`CHANGELOG.md.bak-20260806-equipment-compare-auto-size`、`D:\Debug\4月18日更新\Client\Mir3.exe.bak-20260806-equipment-compare-auto-size`。

## 2026-08-06 - PC 宠物背包与角色装备栏复用装备悬停展示

- 宠物背包 `GridType.CompanionInventory` 的可穿戴装备现与人物背包使用同一套逻辑：左侧装备外观和中间物品属性共用一个外框，右侧比较人物身上对应部位装备；未装备时沿用现有规则，不显示属性差值。
- 角色装备栏 `GridType.Equipment` 的已穿装备复用“装备外观｜物品属性”共同外框，但不进入右侧比较流程，避免身上装备与自身重复比较；宠物自身装备栏 `CompanionEquipment` 未改动。
- 修复人物背包、宠物背包和角色装备栏中药水、材料、技能书等普通道具完全没有说明框：根因是无外观框时 `ItemLabel.Parent` 和 `EquipmentAppearanceLabel` 同为 `null`，旧条件 `ItemLabel.Parent != EquipmentAppearanceLabel` 返回 `false`，已创建的独立说明框因此没有绘制。现先处理外观框为空或已销毁，再判断父级；嵌入共同外框的装备属性不会重复绘制。
- 仅修改 `145Client\Scenes\GameScene.cs`，未复制外观或比较代码，未修改服务端、封包、安卓端或资源文件；人物四向边界、未装备隐藏差值和魔法窗口修复均保留。
- 设计与计划：`docs\superpowers\specs\2026-08-06-pc-companion-character-equipment-hover-design.md`、`docs\superpowers\plans\2026-08-06-pc-companion-character-equipment-hover.md`。
- 验证：修改前宠物比较入口、宠物/角色外观入口和普通道具独立绘制三项检查均为 `False`；修改后入口范围、排除范围、独立绘制和既有规则共 `13` 项检查全部通过，PC Debug 编译成功。客户端 SHA-256：`F7C95323E41B6C0EE089D9951DABEEA90B7D6D0E5A78AAA363B0401896C341A4`。
- 覆盖前备份：`145Client\Scenes\GameScene.cs.bak-20260806-companion-character-hover`、`CHANGELOG.md.bak-20260806-companion-character-hover`、`D:\Debug\4月18日更新\Client\Mir3.exe.bak-20260806-companion-character-hover`。

## 2026-08-06 - PC 魔法窗口边框、人物预览边界与未装备差值修复

- 魔法技能窗口根因：此前为容纳分类按钮把 `UI1:1620` 主体额外加宽 `30` 像素，并叠加一份平移背景；技能树仍为原生 `304` 像素，滚动条随窗口右移，造成右侧空栏和重复边框。现恢复素材原生 `360` 像素窗口，删除整幅背景拼接，滚动条和关闭按钮回到原位置。
- 11 个分类按钮及页面切换全部保留；按钮横向范围仍为 `8～356`，可完整容纳在原生窗口。用户替换的 `D:\Debug\4月18日更新\Client\Data\UI1.Zl` 已只读解析，窗口、8 个原分类、3 个新增分类所需素材 `42/42` 完整，SHA-256 为 `DBCA955E400EA9478C4CE016BAA21824FCAD38BFE49A06520E6289821A5BA099`；本次未覆盖资源文件。
- 人物预览越框根因：旧实现只计算模型图层左右边界，预览高度和绘制基准仍固定为 `240/220`，脚部可能越过底框。现统一计算所有图层的 `Left/Top/Right/Bottom`，宽高和 X/Y 绘制基准均按真实边界生成，四周保留 `6` 像素且不缩放模型。
- 未装备差值根因：空槽位继续使用零属性进入差值计算。现仍显示“身上装备（部位）/未装备”，但在生成“属性/属性差值”前结束该槽位；已有装备时保持原对比和颜色逻辑。
- 修改文件：`145Client\Scenes\Views\MagicDialog.cs`、`145Client\Scenes\GameScene.cs`；设计与计划：`docs\superpowers\specs\2026-08-06-pc-magic-border-equipment-preview-fix-design.md`、`docs\superpowers\plans\2026-08-06-pc-magic-border-equipment-preview-fix.md`。
- 验证：三项失败契约修改前均为 `False`；修改后魔法窗口 9 项、人物边界 8 项、未装备比较 5 项检查全部通过，三个阶段均通过 PC Debug 编译。最终客户端 SHA-256：`F88DED1475251B114445CB57501A6F0B48183D2629CF4DCDD0427897A62D18F6`。
- 覆盖前备份：`145Client\Scenes\Views\MagicDialog.cs.bak-20260806-magic-border-final`、`145Client\Scenes\GameScene.cs.bak-20260806-preview-bounds-no-empty-diff`、`CHANGELOG.md.bak-20260806-magic-preview-final`、`D:\Debug\4月18日更新\Client\Mir3.exe.bak-20260806-magic-preview-final`。

## 2026-08-06 - PC 装备悬停单一外框与完整魔法技能窗口

- 装备悬停外观和物品属性改为同一个深色半透明外框：左侧继续按人物/装备素材动态最小宽度绘制，右侧复用原属性内容，中间仅保留一条 `1` 像素金色竖线；取消两个独立面板的双边框和间隙。
- 原 `ItemLabel` 改为共用外框的无背景、无边框子控件，属性文字内容和位置不变；右侧“身上装备/属性差值”比较面板仍独立显示在共用外框右侧，非装备物品仍沿用原提示框。
- 魔法窗口根因：当前 `MagicDialog.cs` 未启用扩展宽度，且缺少格斗、刺杀、暗杀三个按钮及页面；八个基础按钮整体右移，导致最后按钮进入右上角装饰区，基础技能树也使用了不完整素材。
- 仅参考 `MagicDialog.cs.bak-rollback-20260730-2355` 定点恢复额外 `30` 像素宽度、右侧背景、11个分类按钮、扩展页面素材 `1711～1718`、新增页面 `1741～1743` 及点击切换；未整体覆盖当前文件。
- 武器技能页不再重复收集 `Combat/Assassination/Assassinatie`，三类技能由各自页面单独加载，避免 `Magics.Add` 重复键；服务端、封包、安卓端和资源文件均未修改。
- 修改文件：`145Client\Scenes\GameScene.cs`、`145Client\Scenes\Views\MagicDialog.cs`；设计与计划：`docs\superpowers\specs\2026-08-06-pc-hover-frame-magic-dialog-fix-design.md`、`docs\superpowers\plans\2026-08-06-pc-hover-frame-magic-dialog-fix.md`。
- 验证：修复前共用外框3项、完整魔法窗口8项契约均失败；修复后单一外框、竖线、扩展宽度、三个按钮/页面、扩展素材、按下状态、页面切换和技能去重共14项全部通过。PC Debug Rebuild 成功（0错误，保留原有 `ChkLockMonEffect` 警告）。
- 客户端文件：`D:\Debug\4月18日更新\Client\Mir3.exe`，SHA-256：`9388BD5F8DA2BC1893D4C91B1202D0940C06621F8E8E0B0B11B92C8EDD017B9E`。
- 覆盖前备份：`145Client\Scenes\GameScene.cs.bak-20260806-hover-shared-frame`、`145Client\Scenes\Views\MagicDialog.cs.bak-20260806-complete-magic-window`、`D:\Debug\4月18日更新\Client\Mir3.exe.bak-20260806-hover-magic-fix`、`CHANGELOG.md.bak-20260806-hover-magic-fix`。

## 2026-08-06 - 优化 PC 装备外观预览边框宽度与对齐

- 根据实机截图和确认效果图，将衣服/时装外观框由固定 `180` 像素改为动态最小宽度：合并基础人物、发型和悬停衣服素材的实际尺寸及偏移，左右各保留 `6` 像素，人物保持原比例并自动水平居中。
- 武器、头盔、盾牌、首饰等其他装备外观框改为背包图像实际宽度加 `12` 像素，装备图像继续居中且不缩放。
- 左侧外观框与右侧物品属性框统一使用两者原高度中的较大值，顶部和底部边框完全对齐；属性文字位置、右侧装备比较面板和原悬停逻辑均未修改。
- 源码仍仅修改 `145Client\Scenes\GameScene.cs`；不涉及服务端、封包、安卓端或资源文件。设计与计划：`docs\superpowers\specs\2026-08-06-pc-equipment-appearance-frame-design.md`、`docs\superpowers\plans\2026-08-06-pc-equipment-appearance-frame.md`。
- 验证：失败测试先确认动态范围与等高方法不存在；实现后素材范围 `Left=-20/Right=50/Width=70`、高度 `240/135→240`、`120/260→260` 均通过，PC Debug Rebuild 成功（0 错误，保留原有 `ChkLockMonEffect` 警告）。
- 客户端文件：`D:\Debug\4月18日更新\Client\Mir3.exe`，SHA-256：`24FC9DE2E0D9F92BB05649BA9B3BE1B84882FAEB59D92063B22133B7D0453EB5`。
- 覆盖前备份：`145Client\Scenes\GameScene.cs.bak-20260806-equipment-appearance-frame`、`D:\Debug\4月18日更新\Client\Mir3.exe.bak-20260806-equipment-appearance-frame`、`CHANGELOG.md.bak-20260806-equipment-appearance-frame`。

## 2026-08-06 - PC 人物包裹装备悬停外观预览

- 仅在 PC 端人物包裹悬停可穿戴装备时新增左侧外观面板，原物品属性说明和右侧“身上装备/属性差值”保持不变；仓库、宠物包、商城、服务端和安卓端均未改动。
- 普通衣服和时装显示当前角色的基础人物，只叠加鼠标所指衣服或时装，不绘制当前已穿戴的武器、头盔、盾牌及其他装备；保留人物性别、职业、发型、发色、装备染色及幻化图像。
- 武器、头盔、盾牌、首饰等其他可穿戴装备不绘制人物，仅使用现有背包素材居中显示装备自身外观；碎片装备沿用实际合成装备图像。
- 三个悬停面板按“外观、物品说明、身上装备比较”排列，并统一纳入窗口边界定位、每秒刷新、选中销毁和鼠标移开销毁流程。
- 源码仅修改 `145Client\Scenes\GameScene.cs`；实施计划：`docs\superpowers\plans\2026-08-06-pc-equipment-appearance-preview.md`。
- 验证：修改前 PC Debug 基线编译成功且反射检查按预期因分类方法不存在失败；修改后分类验证结果为 `Armour=True`、`Fashion=True`、`Weapon=False`、`Helmet=False`，PC Debug 编译成功（0 错误，保留原有 `ChkLockMonEffect` 警告）。
- 客户端文件：`D:\Debug\4月18日更新\Client\Mir3.exe`，SHA-256：`5BF83D756AFAC99C267F18751C191E929EF656C5D76C1BFC7512D7B10EA903F4`。
- 覆盖前备份：`145Client\Scenes\GameScene.cs.bak-20260806-equipment-appearance-preview`、`D:\Debug\4月18日更新\Client\Mir3.exe.bak-20260806-equipment-appearance-preview`、`CHANGELOG.md.bak-20260806-equipment-appearance-preview`。

## 2026-08-06 - 接入八大暗影副本脚本并改为元宝收费

- 将 `D:\Video\八大暗影.py` 接入 `D:\Debug\4月18日更新\Server\Scripts\Npc\BOSS副本\八大暗影.py`，并在 BOSS 副本包初始化文件中加入自动导入；NPC 事件编号 5656、动态副本地图 387、菜单、怪物顺序、奖励、每日限制、并发池和刷新锁均保持原样。
- 按确认规则调整费用：入口 `500` 元宝，每层 `50` 元宝；入口扣费/失败退款改用 `SubGameGold`/`GiveGameGold`，每次初始化副本层前检查并扣除层费，元宝不足时不生成该层并沿原回城流程退出。
- 严格原样接入未改动原脚本进程池生命周期逻辑；原脚本已有的重复释放风险单独保留，未扩大本次修改范围。
- 验证：接入契约测试先按预期因目标文件不存在失败，接入后通过；`C:\Python27\python.exe` 语法编译通过，内置 IronPython 语法检查程序也通过。
- 设计与计划：`docs\superpowers\specs\2026-08-06-bada-shadow-integration-design.md`、`docs\superpowers\plans\2026-08-06-bada-shadow-integration.md`；新增契约测试 `.diagnostics\test_bada_shadow_contract.ps1`。
- 覆盖前备份：`D:\Debug\4月18日更新\Server\Scripts\Npc\BOSS副本\__init__.py.bak-20260806-bada-shadow`、`CHANGELOG.md.bak-20260806-bada-shadow`。
- 生效说明：当前仅完成文件接入和静态验证，服务端需要执行“重新加载脚本”或安全重启后，NPC 5656 的八大暗影菜单和地图事件才会生效。

## 2026-08-06 - PC 包裹装备双栏属性对比优化

- 根据实机参考图将上一版纵向追加的装备对比改为右侧独立面板；左侧原物品提示框保持不变，右侧显示“身上装备”、当前装备名称、原属性和“属性差值”。
- 属性差值直接显示在身上装备原属性的右边，不再重复生成下方差值列表；区间提升显示为 `+2～+5`，正值绿色、负值红色、正负混合黄色，零差值不显示。
- 戒指和手镯继续分别比较左右槽位；非装备物品不创建对比面板。对比面板已接入原提示框的定位、刷新、绘制、选中销毁和场景销毁流程。
- 仅修改 PC 客户端 `145Client\Scenes\GameScene.cs`，未修改服务端、封包、安卓端和资源素材；设计与计划记录在 `docs\superpowers\specs\2026-08-06-pc-equipment-compare-panel-design.md`、`docs\superpowers\plans\2026-08-06-pc-equipment-compare-panel.md`。
- 验证：真实程序集差值测试 `.diagnostics\test_pc_equipment_compare_contract.ps1` 先因缺少格式器失败，实现后通过；PC Debug 编译成功，0 错误，仅保留原有 `ChkLockMonEffect` 警告。
- 新文件：`D:\Debug\4月18日更新\Client\Mir3.exe`，SHA-256：`1AD8A24FBFD358E2010947192B3979E1A6D97A83407AA96F7977F615C46A7AB6`。
- 覆盖前备份：`145Client\Scenes\GameScene.cs.bak-20260806-equipment-compare-panel`、`D:\Debug\4月18日更新\Client\Mir3.exe.bak-20260806-equipment-compare-panel`、`CHANGELOG.md.bak-20260806-equipment-compare-panel`。

## 2026-08-05 - PC 包裹装备悬停属性对比（方案1）

- 修改 `145Client\Scenes\GameScene.cs`：悬停 PC 包裹中的可穿戴装备时，复用现有物品提示框追加身上对应部位装备、属性明细和属性差值；戒指、手镯分别比较左右槽位。
- 差值使用绿色表示提升、红色表示降低，混合变化显示黄色；未装备或无变化时给出对应提示。未修改服务端、封包、安卓端和原有拖拽/选中逻辑。
- 新增 `.diagnostics\test_pc_equipment_compare_contract.ps1` 源码契约检查；当前检查已通过。
- PC Debug 编译通过（0 错误，保留原有 `ChkLockMonEffect` 警告），产物已更新至 `D:\Debug\4月18日更新\Client\Mir3.exe`；SHA-256：`870560337EC6F36EA211FD7528DF91804C98B54C58E3361FD553F39F4A0D8545`。
- 覆盖前备份：`D:\Debug\4月18日更新\Client\Mir3.exe.bak-20260806-equipment-compare`。

## 2026-08-05 - 修复定时脚本 ScopeStorage 回调报错

- 根因：`main.py` 先加载 `Ser`，而 `Ser\__init__.py` 会反向加载定时活动脚本；随后注册的 `ServerEvent.AutoRecycleWeapons` 在脚本根作用域中偶发不可见，日志出现 `AttributeError: 'ScopeStorage' object has no attribute 'ServerEvent'`。
- 修复：将 `import ServerEvent` 调整到 `import Ser` 之前，避免循环导入影响根作用域；未改动自动回收、自动分解和定时回调逻辑。
- 验证：服务器 21:30:49 热加载成功，该次重载后未再出现 `DelayCall`、`ScopeStorage` 或脚本语法错误；定时回调、便捷菜单、GM、宠物分解/回收、周重置测试全部通过。
- 备份：`D:\Debug\4月18日更新\Server\Scripts\main.py.bak-20260805-serverevent-import-order`、`D:\相聚假人\Source\CHANGELOG.md.bak-20260805-serverevent-import-order`。

## 2026-08-05 - 补回便捷传送缺失功能

- 从 `D:\Video\便捷传送1.py` 按原逻辑补回宝宝购买、元宝换金币、随身仓库、一键出售、随身任务查询、江湖事迹任务和主线任务攻略。
- 保留原菜单 ID `52/63/65/66/67/69/26`，其中 `63` 的三档兑换和 `52` 的练级宝宝购买子菜单一并恢复；NPC 转调及找不到 NPC 的提示保持旧行为。
- 将按钮加入主菜单及回收/分解操作后的主菜单刷新路径，未改动现有传送、回收、自动分解和 GM 每日重置逻辑。
- 验证：便捷菜单契约测试通过；服务器于 21:11、21:12 及最终调整后的 21:15:44 自动加载脚本并记录“加载脚本成功”。
- 备份：`D:\Debug\4月18日更新\Server\Scripts\Npc\其他\便捷传送.py.bak-20260805-convenience-menu`、`D:\相聚假人\Source\CHANGELOG.md.bak-20260805-convenience-menu`。

## 2026-08-05 - 修复 GM 每日重置日志报错

- 根因：`Ser\定时活动.py` 的 `OnDayChange` 在完成每日重置后继续判断月份，但没有先从 `args[0].Day` 赋值给 `day_of_Month`，因此日志先显示“隔天调用成功”，随后记录 `global name 'day_of_Month' is not defined`。
- 修复：补充 `day_of_Month = args[0].Day`，未改动重置项目和 GM 菜单逻辑。
- 验证：OnDayChange 烟雾测试、GM 每日重置契约测试、宠物分解/回收及周切换测试全部通过；服务器已自动重新加载脚本。
- 备份：`D:\Debug\4月18日更新\Server\Scripts\Ser\定时活动.py.bak-20260805-gm-dayofmonth`、`D:\相聚假人\Source\CHANGELOG.md.bak-20260805-gm-dayofmonth`。

## 2026-08-05 - 移植 GM 每日重置功能到便捷传送
- 来源：`D:\Video\便捷传送1.py`。该文件是较旧的便捷传送版本，不能整体覆盖当前脚本，否则会丢失现有传送、装备回收和宠物包自动分解功能。
- 移植内容：仅加入 GM 专用 `[每日重置-危险操作:9999]` 菜单、调用 `Ser\定时活动.py` 的 `OnDayChange`、成功/失败提示和操作日志。
- 权限：只有 `TempAdmin` 或 `Admin` 账号可见并执行；普通玩家即使构造菜单编号也会收到无权限提示。
- 兼容：采用点击时延迟导入 `OnDayChange`，避免与现有定时活动脚本启动过程形成循环导入；原有传送、自动回收、自动分解和菜单编号保持不变。
- 验证：GM 每日重置烟雾测试先失败后通过；宠物分解烟雾测试、分解契约、回收契约、周期回调契约和周重置契约全部通过。
- 备份：`D:\Debug\4月18日更新\Server\Scripts\Npc\其他\便捷传送.py.bak-20260805-gm-daily-reset`、`D:\相聚假人\Source\CHANGELOG.md.bak-20260805-gm-daily-reset`。

## 2026-08-05 - 完成宠物包随时随地自动分解
- 根因：此前周期任务只在 `OnMinuteChange` 中注册，且自动分解函数缺少 `Server.Models.ItemCheck` 引用；任务未进入周期列表或进入后立即异常，NPC 外不会有任何动作。
- 修复：在脚本加载完成入口 `loadend.py` 注册 `ServerEvent.AutoRecycleWeapons` 每秒周期任务；在自动分解函数内补充 `ItemCheck` 导入。保留原有每分钟注册作为兼容兜底，并由服务端按目标去重。
- 规则：自动分解只扫描 `Companion.Inventory`，不要求 NPC、地图或距离；绑定/任务标记与手动分解规则一致，锁定、结婚、不可精炼、不可分解、金币和人物包空间保护保持不变。
- 在线验证：日志确认在线角色在离开 NPC 后周期回调进入，开启开关后自动分解成功；关闭开关的角色不会处理。
- 收尾：已移除 `[DEBUG-AF02]` 临时诊断日志。烟雾测试、分解契约、回收契约、周期回调契约和周重置契约全部通过。
- 备份：`loadend.py.bak-20260805-auto-fragment-loadend`、`定时活动.py.bak-20260805-af02-diagnostic`、`便捷传送.py.bak-20260805-itemcheck-import`。

## 2026-08-05 - 修复宠物包自动分解无反应（规则与手动分解一致）
- 根因：自动分解脚本比服务端原有手动分解多禁止了 `Bound`（绑定）和 `QuestItem`（任务）标记；因此部分手动可以分解的装备，在自动扫描时被静默跳过。
- 最小修复：只从 `ExecuteCompanionFragmentForSender` 的额外保护列表中移除 `Bound` 和 `QuestItem`；锁定、结婚、不可精炼、不可分解、金币、人物包空间等原有保护保持不变。
- 回归测试：宠物包分解烟雾测试新增“绑定/任务标记装备应与手动分解一致”的真实行为断言；修复前稳定失败（只处理 2 件），修复后应处理 4 件。
- 验证：修复后的真实脚本烟雾测试、分解契约、回收契约、定时回调入口和周重置契约共 5 项全部通过；脚本 SHA-256 为 `C7C4D1CE5CFBC93B3BFB8C423F299D6DDFD178C8D909E30B6BED0220D1CDC76A`。
- 生效说明：当前服务端进程启动于 07:59:30，早于本次脚本写入时间 08:28:28，且仍有客户端连接；为避免中断在线角色，本次未自动重启。需在服务端执行“重新加载脚本”或安全重启后再进行真实道具验证。
- 覆盖前备份：`D:\Debug\4月18日更新\Server\Scripts\Npc\其他\便捷传送.py.bak-20260805-fragment-rule-parity`。

## 2026-08-05 - 再修复宠物包自动分解定时入口（ServerEvent）

- 新日志 `D:\Video\Logs_8_5.txt` 证明上次根级回调方案仍失败：完整重启后每秒出现 `ScopeStorage` 找不到 `AutoRecycleWeapons`；说明服务端定时解析器不能访问该根级导入。
- 最小修复：移除 `main.py` 中无效的根级导入；在引擎启动时固定加载的 `ServerEvent.py` 增加一个薄转发函数；`定时活动.py` 改为调用 `ServerEvent.AutoRecycleWeapons`。分解规则、玩家开关、保护标记和奖励逻辑均未改变。
- 回归测试改为使用 IronPython 重放服务端同样的“按字符串逐级解析并调用”流程；修复前稳定复现 `ScopeStorage` 找不到 `AutoRecycleWeapons`，修复后实际调用成功。
- 验证：`main.py`、`ServerEvent.py`、`Defines.py`、便捷传送脚本和定时活动脚本均通过 IronPython 语法检查；周期回调、宠物分解、宠物回收、周切换契约及宠物分解烟测全部通过。
- 在线验证：服务端进程在新脚本写入后于 07:59:30 启动，7000 端口正常监听；跨过 08:00 定时触发点后，日志未再新增 `ScopeStorage` 或 `DelayCall` 回调错误。当前无客户端连接，尚未消耗在线真实道具。
- 备份：`main.py.bak-20260805-serverevent-periodic-callback`、`ServerEvent.py.bak-20260805-serverevent-periodic-callback`、`定时活动.py.bak-20260805-serverevent-periodic-callback`、`CHANGELOG.md.bak-20260805-serverevent-periodic-callback`。

## 2026-08-05 - 修复宠物包自动分解定时回调路径

- 根因：在线日志反复出现 `ScopeStorage` 找不到 `Ser`，原定时目标 `Ser.定时活动.AutoRecycleWeapons` 无法解析，导致自动扫描没有执行；手动分解逻辑本身未受影响。
- 最小修复：在 `Server/Scripts/main.py` 将 `AutoRecycleWeapons` 暴露到脚本根作用域；在 `Server/Scripts/Ser/定时活动.py` 将周期调用改为根级目标 `AutoRecycleWeapons`。未改动分解规则、开关含义或道具保护条件。
- 验证：调度契约测试先失败后通过；活动脚本、NPC脚本、主脚本和变量脚本均通过 IronPython 语法检查；宠物分解、宠物回收、周切换契约及宠物分解烟测均通过。
- 备份：`Server/Scripts/main.py.bak-20260805-auto-fragment-schedule`、`Server/Scripts/Ser/定时活动.py.bak-20260805-auto-fragment-schedule`、`CHANGELOG.md.bak-20260805-auto-fragment-schedule`。
- 在线状态：当前运行中的服务端是在本次修复前启动的，尚未重载新脚本；未对在线真实道具做任何消耗。重启/重载脚本后再进行一次测试装备验证。

## 2026-08-04 - 宠物包自动分解脚本（独立开关 A 方案）

- 新增独立玩家变量 `GV_PLAYER_AUTO_FRAGMENT_ENABLED=104`，默认关闭；在便捷功能菜单新增 `[自动分解开关:601]`，不与自动回收开关共用。
- 在 `便捷传送.py` 新增 `ExecuteCompanionFragmentForSender`：只扫描 `Companion.Inventory`，复用现有 `CanFragment`、`FragmentCost`、`FragmentCount` 和人物包空间检查；碎片进入人物包，手续费从人物金币扣除。
- 自动分解保护锁定、婚戒、不可分解、无价值、绑定和任务物品；堆叠物品每次按单件处理，避免沿用旧分解入口的堆叠计费差异。
- `定时活动.py` 启动时加载便捷传送脚本，确保服务器启动后菜单立即使用新开关；接入现有周期任务，仅对独立开关已开启的玩家执行；未修改客户端、APK 或 `Scripts888`。
- 覆盖前备份：
  - `D:\Debug\4月18日更新\Server\Scripts\Defines.py.bak-20260804-pet-fragment`
  - `D:\Debug\4月18日更新\Server\Scripts\Npc\其他\便捷传送.py.bak-20260804-pet-fragment`
  - `D:\Debug\4月18日更新\Server\Scripts\Ser\定时活动.py.bak-20260804-pet-fragment`
  - `D:\相聚假人\Source\CHANGELOG.md.bak-20260804-pet-fragment`
- 修改后文件：`Defines.py` 8184 字节，SHA-256 `A4B3C2E2B1D72D3F26DD77300D1DD30F51E734D0E4A295D71F2728A10DB1315D`；`便捷传送.py` 37947 字节，SHA-256 `E5F9E0789C11F96600DA39899F46955960A4D6C23D075DF00483C7095D0CB2CD`；`定时活动.py` 13900 字节，SHA-256 `71644A186F18240AE4A96DBEB0D0D9836DEDEB69CBDFFB7B2C533B149E1E6314`。
- 验证：自动分解契约测试、既有自动回收契约测试、周切换契约测试均通过；三个运行脚本经 IronPython 2.7 编译检查通过；使用模拟宠物包完成合法物品、保护标记、堆叠单件、金币扣除、碎片奖励和格子封包冒烟测试通过。
- 已知限制：尚未在在线服务端放入真实道具实测；重启或重新加载服务端脚本后生效，首次使用需在便捷功能菜单打开“自动分解”。

## 2026-08-02 - 使用 D:\Video\Mir3.ini 重新编译安卓客户端

- 以 `D:\Video\Mir3.ini` 为唯一配置来源，保持原文件不变；仅将 `[Network]` 的 `Port=7000` 调整为 `Port=7100`，其余配置文本不变。
- 安卓生效配置为 `MicroClientIP=114.132.90.203`、`Host=http://114.132.90.203:7090/`、`IPAddress=114.132.90.203`、`Port=7100`。
- 未修改 `DrodNative.cs`，未恢复此前导致黑屏风险的强制配置迁移；从稳定 `Data.zip` 出发仅替换根目录 `Mir3.ini`，两个 `.Zl` 资源哈希保持不变，ZIP 条目继续使用正斜杠路径。
- 将 `Mir3.Droid\Assets` 下两个旧备份 ZIP 移至 `.build-check` 保存，避免它们被误打进 APK；最终 APK 中备份资源数量为 `0`，文件大小恢复为 `58,959,089` 字节。
- Android Release/AOT 重建退出码为 `0`；APK 内 `assets/Data/Mir3.ini` 和 `assets/Data.zip/Mir3.ini` 均与目标配置全文一致。
- 新 APK：`D:\Debug\4月18日更新\Android-118.25.67.175\Mir3-114.132.90.203-7100-Signed.apk`；SHA-256：`23D543796EB89374570DB4BF5091EC64E5942C77A749D5B5D368A760A5AB8AD6`；v1/v2/v3 签名验证通过。
- 覆盖前的黑屏版本备份为 `Mir3-114.132.90.203-7100-Signed.apk.bak-20260802-video-config`；源配置和稳定 `Data.zip` 备份保存在 `.build-check`。旧 IP 稳定 APK、PC 客户端和服务端未覆盖。

## 2026-08-02 - 回滚新 IP 安卓客户端黑屏版本

- 按用户要求仅回滚本次新 IP 安卓改动，之前的界面和功能源码不变。
- 恢复 `Mir3.Droid\DrodNative.cs` 到新 IP 修改前版本，移除启动时强制迁移配置的代码。
- 恢复源码 `Mir3.ini`、`Assets\Data.zip` 以及交付目录配置为 `IPAddress=118.25.67.175`、`Port=7000`。
- 恢复稳定 APK `D:\Debug\4月18日更新\Android-118.25.67.175\Mir3-118.25.67.175-Signed.apk`，SHA-256：`2954CB60067D88BB57091C452C233B7FE6D7A4FB70873C5EAD60CCB0989E05B3`；v1/v2/v3 签名验证通过。
- 新 IP APK 和本次回滚前文件未删除，均已另存备份，便于后续追溯。

## 2026-08-02 - 新 IP 安卓客户端重新编译（最终版）

- 修复旧地址仍生效的问题：旧安装目录中的外部 `Mir3.ini` 与 APK 内置 `Data.zip` 可能分别保留旧配置。
- 安卓客户端的内置 `assets/Data/Mir3.ini`、`assets/Data.zip` 内置 `Mir3.ini`、交付目录配置均已统一为 `IPAddress=114.132.90.203`、`Port=7100`。
- `DrodNative` 增加最小迁移处理：已有安装启动时只更新外部 `Mir3.ini` 的 `[Network]` 段，避免覆盖安装后继续使用旧 IP。
- 新 APK 另存为 `D:\Debug\4月18日更新\Android-118.25.67.175\Mir3-114.132.90.203-7100-Signed.apk`，未覆盖原有 APK；最终重编译 SHA-256：`A479B5DFF2F1DBD91979E0CB669FC313E52D8D4B554325398BE424082924B95A`。
- APK 签名验证通过（v1/v2/v3）；旧 APK、旧配置和源文件均保留备份。PC 客户端和服务端未修改。

## 2026-08-02 - 安卓客户端服务器地址更新并重新编译

- 仅修改 `Mir3.Droid\Assets\Data\Mir3.ini` 的网络连接参数：`IPAddress=114.132.90.203`、`Port=7100`；其他登录、资源和客户端设置保持不变。
- 已完成安卓 Release/AOT 编译；从 APK 内置 `assets/Data/Mir3.ini` 复核确认地址和端口已写入。
- APK v1/v2/v3 签名验证通过。
- 已覆盖 `D:\Debug\4月18日更新\Android-118.25.67.175\Mir3-118.25.67.175-Signed.apk`，SHA-256：`9327D7ED29E47A7B148DAB5F1960EF598EF8973EF123F867DC7E0FB4AF26AC6A`。
- 覆盖前备份为 `Android-118.25.67.175\Mir3-118.25.67.175-Signed.apk.bak-20260802-11413290203-7100`；源码配置备份为 `Mir3.Droid\Assets\Data\Mir3.ini.bak-20260802-server-11413290203-7100`。未修改 PC 和服务端。

## 2026-07-31 21:30 - 回滚人物包滚动行数导致的启动黑屏

- 客户端错误日志确认：`Client.Controls.DXItemCell.set_Item` 在 `GameScene.FillItems` 中抛出 `System.IndexOutOfRangeException`；原因是服务端仍为 48 格，而客户端人物包临时扩为 6×12，启动装载第 49 格时越界。
- 已撤回本次 6×12 人物包和 `GridScrollBar` 源码改动，恢复到 2026-07-30 23:55 源码状态；背包恢复 6×8，容量保持 48，不再黑屏。
- 已恢复上一个可启动的 PC 文件 `Mir3.exe`，SHA-256：`FDDE3B807B1F2FE0B942A3C454F9196FCF7823ECDE6AD7FE2327C343FEA29EA9`。
- 已恢复上一个可启动的安卓 APK，SHA-256：`2954CB60067D88BB57091C452C233B7FE6D7A4FB70873C5EAD60CCB0989E05B3`。
- 本次失败版本及回滚前源码均已保留为 `failed-scroll-20260731-2130` 备份；服务端未修改。后续若要增加真实滚动行数，必须先同步服务端背包容量与 `FillItems` 数据长度，再重新实现。

## 2026-07-31 21:30 - PC 滚动条修复版本完成覆盖

- 用户关闭客户端后，已将 `D:\Client\Mir3.exe` 覆盖到 `D:\Debug\4月18日更新\Client\Mir3.exe`。
- 源文件与交付文件 SHA-256 均为 `B4625B64B6AD9D29E4F12E6537FE8DE3A44BF6270F236B11020C948C9B135816`。
- 覆盖前备份为 `Client\Mir3.exe.bak-20260731-2125`；服务端未修改。

## 2026-07-31 21:25 - 滚动条修复版本编译

- 修正 `GridScrollBar.MaxValue` 计算：控件的 `MaxValue` 已包含可视行数，改为 `Grid.GridSize.Height`，避免重复减去 `VisibleHeight` 导致滚动条被判定为不可用。
- PC Release 编译通过，0 错误；新编译文件 `D:\Client\Mir3.exe`，SHA-256：`B4625B64B6AD9D29E4F12E6537FE8DE3A44BF6270F236B11020C948C9B135816`。
- 安卓 Release/AOT 编译通过，APK v1/v2/v3 签名验证通过；已覆盖 `D:\Debug\4月18日更新\Android-118.25.67.175\Mir3-118.25.67.175-Signed.apk`，SHA-256：`CEDEE272CF1B83FE71D9B793175244DC8156AD9284EC6BA20261ED058B3198DA`。
- 安卓覆盖前备份为 `Android-118.25.67.175\Mir3-118.25.67.175-Signed.apk.bak-20260731-2125`。PC 正式文件因当前 `Mir3.exe` 进程占用暂未覆盖，关闭客户端后再替换；PC 覆盖前备份已生成。

## 2026-07-31 21:20 - 人物包滚动行数版本编译交付

- PC `145Client` Release 编译完成，0 错误；安卓 `Mir3.Droid` Release/AOT 编译完成，0 错误。
- 已覆盖 `D:\Debug\4月18日更新\Client\Mir3.exe`，SHA-256：`CC86D3ACEBC3D4DEFD3EBB1D11F98DC5ACEF3B9134B189B54489DD5A814BCA5E`。
- 已覆盖 `D:\Debug\4月18日更新\Android-118.25.67.175\Mir3-118.25.67.175-Signed.apk`，SHA-256：`219CC067ADA59186CEE0DE6201E2231EE4EC04235214B72266B21409A3C1B882`；APK v1/v2/v3 签名验证通过。
- 覆盖前备份为 `Client\Mir3.exe.bak-20260731-2120` 与 `Android-118.25.67.175\Mir3-118.25.67.175-Signed.apk.bak-20260731-2120`；未覆盖服务端。

## 2026-07-31 21:15 - 人物包增加可滚动行数

- PC 与安卓人物包保持原 6 列和 8 行可视区域，将总网格调整为 6×12；窗口高度、格子尺寸和物品协议不变。
- 新增人物包 `GridScrollBar`，复用原右侧索引条皮肤 `UI1:1225`，绑定 `Grid.ScrollValue`，最大滚动值为 `12-8=4`；鼠标滚轮也绑定到人物包格子。
- 安卓角色包只读窗口同步增加相同滚动控制；碎片包滚动逻辑不变。
- 未修改服务端背包容量（仍为 48），超出部分作为可滚动空槽，不改变已有物品数据和网络协议。
- PC Release 编译通过：0 错误；安卓 Release 编译通过：0 错误（保留项目原有警告）。本次只更新源码，未覆盖正式交付文件。

## 2026-07-31 - 源码回滚至 2026-07-30 23:55

- 按用户指定时间点，仅回滚源码目录 `D:\相聚假人\Source`，未覆盖 `D:\Debug\4月18日更新` 中的 PC/安卓交付文件，也未修改服务端运行目录。
- 恢复 23:55 时点的 PC 包裹窗口、PC 魔法技能窗口、安卓人物包/角色包窗口及共享 `Library\Globals.cs`；撤销之后加入的 8×8 背包扩展、窗口加宽、分段皮肤、右侧滚动条定位等改动。
- 回滚文件：`145Client\Scenes\Views\MagicDialog.cs`、`145Client\Scenes\Views\InventoryDialog.cs`、`Mir3.Mobile\Client\Scenes\Views\InventoryDialog.cs`、`Mir3.Mobile\Client\Scenes\Views\InventoryJueSeDialog.cs`、`Library\Globals.cs`。
- 每个被覆盖源码文件均已在同目录生成 `*.bak-rollback-20260730-2355` 备份，可恢复本次回滚前状态。

## 2026-07-31 20:25 - 右侧索引条交互位置跟随扩展窗口修复

- 修正 PC 与安卓人物包/碎片包 `PatchGridScrollBar` 的横坐标：由旧 `ClientArea.Right` 改为扩展后窗口 `Size.Width - 23`，确保滚动条命中区与最右侧皮肤一致，可直接拖动。
- 未改动格子数量、物品逻辑、按钮逻辑或服务端；右上角按钮继续使用扩展后的实际命中区域。
- PC Release 编译 0 错误；安卓 Release/AOT 编译完成并通过 APK 签名验证。
- 已覆盖 `D:\Debug\4月18日更新\Client\Mir3.exe`，SHA-256：`D7452EBA487366C362093E8D2E6616543DDC9FC475D75EBBDFFB1C1DAA499C3D`。
- 已覆盖 `D:\Debug\4月18日更新\Android-118.25.67.175\Mir3-118.25.67.175-Signed.apk`，SHA-256：`2954CB60067D88BB57091C452C233B7FE6D7A4FB70873C5EAD60CCB0989E05B3`。
- 覆盖前备份为 `Client\Mir3.exe.bak-20260731-2025` 与 `Android-118.25.67.175\Mir3-118.25.67.175-Signed.apk.bak-20260731-2025`。

## 2026-07-31 20:20 - 包裹透明度统一及右侧滚动条可交互修复

### 最终修复

- 根据最新截图确认，上一版右侧皮肤虽不再残影，但与左侧原皮肤透明度仍不一致；现将人物包和碎片包背景改为真正的左右两个裁切段，各自保持原透明度 `0.85/0.7`，消除叠加造成的深色差异。
- `InventoryBackGround` 与 `PatchBackGround` 改为完整扩展宽度的容器，内部左右皮肤段互不重叠；原右边框、顶部按钮框、底部整理框只绘制一次并移动到最右侧。
- 碎片包 `PatchGridScrollBar` 挂载到完整宽度的 `PatchBackGround` 上，不再被原始背景宽度裁切，右侧索引条可正常拖动；人物包仍保持 8 行全显示，不人为增加滚动行数。
- 包裹右上角 `GridButton/PatchButton` 继续使用右移后的实际命中区域，裁切层为非交互层，不拦截点击/触摸。
- PC 魔法技能窗口继续使用分段皮肤方式，右侧滚动区域、边框和分类按钮保持可交互。
- 背包容量、物品逻辑、服务端协议和数据库未修改。

### 编译与覆盖

- PC `145Client` Release 编译通过，0 错误；安卓 `Mir3.Droid` Release/AOT 编译通过，APK v1/v2/v3 签名验证通过。
- 已覆盖 `D:\Debug\4月18日更新\Client\Mir3.exe`，SHA-256：`004E6300A788AE51A2933071EB262E43B166E09288A857671FBC25DE187BD24E`。
- 已覆盖 `D:\Debug\4月18日更新\Android-118.25.67.175\Mir3-118.25.67.175-Signed.apk`，SHA-256：`DC3B90C62B54A87ACF2079866B6C35F361E146011BE01CFB172B226B318DC68A`。
- 覆盖前备份文件为 `Client\Mir3.exe.bak-20260731-2020` 和 `Android-118.25.67.175\Mir3-118.25.67.175-Signed.apk.bak-20260731-2020`；未创建新交付目录，未覆盖服务端。
- 覆盖后源文件与目标文件哈希一致，临时 `X:` 构建映射已清理；最终外观和按钮点击等待用户在游戏内手动复核。

## 2026-07-31 20:00 - 背包旧边框/整理框残影及顶部按钮点击修复

### 截图复核与原因

- 用户实机截图确认第一版裁切起点过晚且仍按 `0.85` 透明度叠加，导致原皮肤右侧竖框、顶部切换/搜索框和底部整理框从新皮肤下方透出，形成新旧两套框体。
- 顶部视觉框已经随皮肤右移，但对应 `GridButton/PatchButton` 控件仍停在原 `X=223`，因此点击新位置没有响应。
- PC 魔法技能窗口采用相同半透明叠加方式，也存在旧右框、旧滚动区域或旧关闭框残留的同类风险。

### 最小修复

- PC 与安卓背包皮肤覆盖起点由原第7列前提前到第5列前，将原最后两列、旧右框、旧顶部框和旧底部整理框作为一个整体向右平移两列；覆盖图改为不透明，旧皮肤不再透出。
- `GridButton` 与 `PatchButton` 的实际位置同步由 `X=223` 调整为 `X=223+76`，使顶部新位置的视觉框与鼠标/触摸命中区域一致。
- 所有皮肤裁切容器均设置 `IsControl=false` 和 `PassThrough=true`，不会拦截搜索/切换、整理、关闭或最右侧技能分类按钮。
- PC 魔法窗口覆盖起点再向左提前 `30` 像素，并改为不透明复用原 `UI1:1620` 皮肤；旧右框、旧滚动背景和旧关闭框被完整覆盖，只保留向右移动后的新位置。
- 背包容量继续为 `8×8=64`，未修改物品、整理、网络、服务端或数据库逻辑。

### 编译、备份与覆盖

- PC `145Client` Release 重建通过：`0` 错误，仅保留原有 `ChkLockMonEffect` 警告；已覆盖 `D:\Debug\4月18日更新\Client\Mir3.exe`，SHA-256：`F9890AA8BFE39428AD9F7EE22AB92A892823FEDE943357E211319E155709B176`。
- 安卓 `Mir3.Droid` Release/AOT 发布通过，APK v1/v2/v3 签名验证均为 `true`；已覆盖标准 APK，SHA-256：`07094313EEE153F59E3390BC932D52117837147183F5EE1D50685CB4C7EFF791`。
- 覆盖前已备份第一版 PC 文件为 `Client\Mir3.exe.bak-20260731-2000`，安卓文件为 `Android-118.25.67.175\Mir3-118.25.67.175-Signed.apk.bak-20260731-2000`；未新增整套目录。
- 覆盖后源文件与目标文件哈希一致，临时 `X:` 构建映射已清理；最终外观和按钮点击等待用户在游戏内手动复核。

## 2026-07-31 19:44 - 8×8 背包格子与 PC 魔法技能窗口皮肤修复

### 最小改动

- 修复此前仅扩大背包控件、右侧两列没有原皮肤格子和边框的问题：PC 与安卓均从原 `UI1:1220` 背包皮肤中裁取最后两列格子区域，向右平移后复用，新增两列现在具有与原六列完全一致的底纹和格线。
- 原背包右侧滚动槽、金边和底部边框随裁取区域整体移动到新窗口最右侧，不再保留中间旧边框或使用纯色补丁；人物背包继续保持 `8×8=64` 格，容量、物品逻辑和服务端协议未再次修改。
- 同步修改 PC `145Client\Scenes\Views\InventoryDialog.cs`、安卓 `Mir3.Mobile\Client\Scenes\Views\InventoryDialog.cs` 和只读人物背包 `InventoryJueSeDialog.cs`，碎片包裹、宠物包裹及仓库不变。
- 修复 PC 魔法技能窗口右侧纯色补块：从原 `UI1:1620` 窗口皮肤中裁取右侧内容与边框，向右平移 `30` 像素复用；右边框、滚动区域和底框保持原样，顶部全部技能分类按钮仍完整显示。

### 编译、备份与覆盖

- PC `145Client` Release 重建通过：`0` 错误，仅保留原有 `ChkLockMonEffect` 未赋值警告。
- 安卓 `Mir3.Droid` Release/AOT 发布通过；APK 经 `apksigner` 验证，v1、v2、v3 签名均为 `true`。
- 按用户新要求不再创建整套交付目录，只备份将覆盖的单个文件：原 PC 主程序备份为 `D:\Debug\4月18日更新\Client\Mir3.exe.bak-20260731-1945`。
- 原安卓标准包备份为 `D:\Debug\4月18日更新\Android-118.25.67.175\Mir3-118.25.67.175-Signed.apk.bak-20260731-1945`。
- 已覆盖 PC `Client\Mir3.exe`，SHA-256：`535493D0EF12C9730C8E3ED527B81AA7789B484963B24F37B4EFFAEF093AA75C`。
- 已覆盖安卓标准包 `Mir3-118.25.67.175-Signed.apk`，SHA-256：`3D05F8ACD2F5A7B5AA99461AC94E76405B655243665A5DD094B9FD93EB60F460`。
- 覆盖后源文件与目标文件哈希一致，临时 `X:` 构建映射已清理；本次未覆盖服务端、未自动安装 APK，最终游戏内视觉效果交由用户手动复核。

## 2026-07-31 00:58 - PC 服务端授权状态无效修复

### 原因与最小修复

- 定位确认新生成的 Release `Server.exe` 未经过原发行版使用的 .NET Reactor 发布保护流程；即使合法 `.license` 文件存在，`License.Status.Licensed` 仍会返回 `false`，因此界面显示“无效”。
- 未修改、删除或绕过 `Server\Helpers\LicenseHelper.cs` 的授权判断。修复包恢复使用原发布目录中已能正常运行的 `Server.exe`，仅在同目录增加本次编译的 `Library.dll`；CLR 程序集解析验证确认外置 DLL 优先于主程序内嵌旧 DLL 加载。
- 新 `Library.dll` 保留本次服务端人物背包容量 `64`，因此无需重新生成未经发布保护的主程序，也不影响其他服务端界面和逻辑。
- 同时修复复制目录中 `Server.ini` 的授权文件绝对路径：由本机不存在的 `D:\mir3\Server\...license` 改为新交付目录内实际存在的授权文件，保持 UTF-16 LE 原编码及其他配置不变。

### 修复后交付与验证

- 新完整服务端：`D:\Debug\4月18日更新\Server-背包8x8-授权修复`，共 `2,681` 个文件、`1,769,756,160` 字节。
- `Server.exe` 沿用原发布文件，SHA-256：`BF20E400CC2F4324900E6D0293F330BFB740FE1D40B60A56EC6F801E0B798B90`。
- 新 `Library.dll` 大小 `2,166,784` 字节，SHA-256：`B777E91826F2C398BABDF1D97DD738FF8935C7ED1E3BC0C51D652747892F5D95`。
- 隔离进程动态调用现有授权逻辑：授权文件加载结果为 `True`，状态由错误的 `Invalid` 恢复为原发布版既有的 `DebugMode`；源码将 `DebugMode` 判定为可启动状态。
- 同一动态验证进程确认实际加载路径为新目录下的 `Library.dll`，且 `Globals.InventorySize=64`。
- 隐藏启动管理端持续运行检查通过，随后已关闭测试进程；未点击启动服务器、未占用游戏端口，验证结束后 `Server` 进程数为 `0`。
- 上一目录 `D:\Debug\4月18日更新\Server-背包8x8` 保留用于问题回溯，不应继续使用；原始 `Server` 目录和当前数据均未覆盖。

## 2026-07-31 00:48 - 8×8 背包配套正式文件编译与独立交付

### 编译结果

- PC `145Client` Release 编译成功，生成包含人物背包 `8×8` 与魔法窗口加宽改动的 `Mir3.exe`。
- 安卓 `Mir3.Droid` Release/AOT 发布成功，连接配置沿用 `D:\Debug\4月18日更新\Mir3.ini` 的 `118.25.67.175:7000`。
- 完整服务端 `Server` Release 编译成功，内含共用人物背包容量 `64`；仅保留项目原有 `System.Runtime.InteropServices.RuntimeInformation` 版本解析警告，无编译错误。

### 独立交付文件

- PC 完整客户端：`D:\Debug\4月18日更新\Client-背包8x8-魔法窗口加宽`，共 `2,807` 个文件、`7,068,874,421` 字节。
- PC 主程序：`Mir3.exe`，大小 `3,924,992` 字节，SHA-256：`EA84511F790261ADCBF76FD6E157B96A9BA344BA86CD0BEABF7AF4777E32BA09`。
- 安卓 APK：`D:\Debug\4月18日更新\Android-背包8x8-118.25.67.175\Mir3-118.25.67.175-背包8x8-Signed.apk`，大小 `58,954,993` 字节，SHA-256：`1B428345C03E484978F2947FD406C92C4E822662DAC0D756BA01F2EC2F08F4E8`。
- 完整服务端：`D:\Debug\4月18日更新\Server-背包8x8`，共 `2,680` 个文件、`1,767,353,304` 字节。
- 服务端主程序：`Server.exe`，大小 `82,848,768` 字节，SHA-256：`73C5D6F66FBD60860A106C5F12969569D7B0F034D5E8E1CCE8579616E808A969`。

### 校验与不覆盖确认

- APK 经 `apksigner` 校验通过：v1、v2、v3 均为 `true`，签名者数量 `1`；v4 与 SourceStamp 未启用，符合项目现有发布配置。
- PC 与安卓交付目录内的 `Mir3.ini` 均取自用户指定文件，SHA-256：`23EED1EE14EC568FEAE73F166A966655198EB4D7C0D9C7ACCD910F52D6B8E481`。
- 原 PC `Client\Mir3.exe` SHA-256 仍为 `FDDE3B807B1F2FE0B942A3C454F9196FCF7823ECDE6AD7FE2327C343FEA29EA9`；原服务端 `Server\Server.exe` SHA-256 仍为 `BF20E400CC2F4324900E6D0293F330BFB740FE1D40B60A56EC6F801E0B798B90`，确认均未覆盖。
- 未停止或替换当前运行中的服务端，未自动安装 APK；正式启用 64 格背包时必须同时部署本次新服务端与对应 PC/安卓客户端。

## 2026-07-31 00:28 - PC/安卓人物背包扩展为 8×8，PC 魔法窗口加宽

### 最小改动

- 将共用人物背包容量 `Globals.InventorySize` 从 `48` 调整为 `64`，使新增格子具备真实存放、整理和服务端校验能力；未新增网络包字段，未修改数据库结构。
- PC `145Client\Scenes\Views\InventoryDialog.cs` 与安卓 `Mir3.Mobile\Client\Scenes\Views\InventoryDialog.cs` 的人物背包由 `6×8` 扩展为 `8×8`；仅向右增加两列宽度并补绘同色背景，关闭与整理按钮同步右移。
- 安卓只读人物背包 `Mir3.Mobile\Client\Scenes\Views\InventoryJueSeDialog.cs` 同步为 `8×8`，避免查看界面遗漏第 49–64 格物品。
- 碎片包裹 `PatchGrid`、宠物包裹、人物仓库及其他容器的容量和布局保持不变。
- PC `145Client\Scenes\Views\MagicDialog.cs` 仅将魔法技能窗口加宽 `30` 像素并补绘右侧背景，关闭按钮和原有滚动条随窗口右移；技能树、分类和点击逻辑未改。
- 用户中途提出的 `8×6` 仅用于编译验证，最终源码已统一改为本条记录的 `8×8`，不作为独立版本保留。

### 构建与验证

- PC `145Client` Release 重建通过：`0` 错误，仅保留原有 `ChkLockMonEffect` 未赋值警告；验证产物位于 `.build-check\inventory-8x8\pc\Mir3.exe`。
- `ServerLibrary` Release 构建通过：`0` 警告、`0` 错误；验证产物位于 `.build-check\inventory-8x8\server-library\Library.dll`。
- 安卓 `Mir3.Droid` Debug 完整构建通过：`0` 错误，仅保留项目原有 XML 注释、过时 API 和平台兼容性警告；构建后已移除临时 `X:` 映射。
- 静态核对确认 PC 与安卓人物背包均为 `8×8=64` 格，服务端与客户端共同引用容量 `64`。正式部署时 PC/安卓客户端与服务端必须配套更新，避免旧版 48 格客户端无法显示新增槽位。
- 本次只修改源码和更新日志，未覆盖 `D:\Debug\4月18日更新` 中的现有 PC、安卓或服务端正式产物，也未安装到设备。

本文件记录源码、运行配置、资源包和交付产物的实际变更。后续每次修改或重新编译均应同步更新此文件。

## 2026-07-30 23:55 - 源码回滚至 20:00 状态

### 回滚范围

- 按用户指定时间点，仅回滚 `D:\相聚假人\Source` 源码中 `2026-07-30 20:00` 之后加入的声望称号头顶显示与配套网络字段。
- 删除 `StartInformation`、`ObjectPlayer`、`PlayerUpdate` 后加的 `FameTitle` 字段，并删除服务端登录、进入视野和外观刷新包中的对应赋值。
- 删除 PC 与安卓客户端后加的 `FameTitle` 状态、标签创建、头顶绘制和外观更新接收逻辑。
- 保留项目原本已有的 `EquipmentSlot.FameTitle`、`ItemType.FameTitle`、声望称号装备槽及物品功能；本次只撤销后来新增的头顶文字显示协议。
- 保留特色称号原有 `CustomBuffInfo.OverheadTitle × 20 → Data\Title.Zl` 动画调用，未修改特色称号素材、Buff、属性或位置。
- 保留 `20:00` 及更早完成的安卓分解窗口、角色包/宠物包全选、功能栏布局和其他 UI 改动。
- 未修改 `D:\Debug`、`D:\Video`、运行服务、数据库或任何现有编译产物，也未创建新的发布目录。

### 验证

- `ServerLibrary` Release 临时编译通过：0 警告、0 错误。
- PC `145Client` Release 临时编译通过：0 错误，仅保留项目原有 `ChkLockMonEffect` 未赋值警告。
- 安卓 `Mir3.Droid` Debug 完整编译通过：0 错误，保留项目原有 XML 注释、过时 API 和平台兼容性警告。
- 静态检查确认上述 13 个新增点不再引用 `FameTitle`，PC 与安卓的 `HeadTopCreate(customBuff.OverheadTitle * 20, ...)` 特色称号调用仍存在。
- 编译验证仅写入源码树内 `.build-check` 及项目自身 `bin/obj` 临时目录；构建后已清理临时 `X:` 映射。

## 2026-07-30 23:39 - 回滚 PC 声望称号与特色称号至最初显示方式

### 回滚范围

- 根据 `2026-07-30 22:15` 的首次实现回滚 `145Client\Models\MapObject.cs`，撤销 `23:03` 增加的声望称号 12 号粗体、亮黄色橙红发光描边、特色称号位置以及声望优先互斥逻辑。
- 声望称号恢复默认 9 号字体、金色文字和灰色描边；存在成就称号时仍排列在成就称号上方。
- 特色称号恢复原有独立 `Title.Zl` 动画逻辑，不再因装备声望称号而隐藏；声望称号与特色称号重新允许同时显示。
- 服务端协议、声望称号脚本、特色称号配置、`Title.Zl` 素材、数据库和安卓客户端均未改动。

### 构建与验证

- `145Client` Release 重新编译成功，无编译错误；仅保留项目原有 `ChkLockMonEffect` 未赋值警告。
- 新建独立客户端目录：`D:\Debug\4月18日更新\Client-声望称号初始版回滚`，共 `2,811` 个文件、`7,069,071,422` 字节。
- 新 `Mir3.exe` 大小：`3,926,016` 字节。
- 新 `Mir3.exe` SHA-256：`738D67B243F103700F342BDF146A9E0A233C810D3A4851EA119F7A6551B89C38`。
- 初始客户端、上一份声望称号客户端及 `Client-声望称号特色位发光` 均未覆盖，发光版 `Mir3.exe` 哈希仍为 `0B1C96EB43D97A4EFE053648CB3D2B711D3DB33689C1FED828F1638D01F2E1DB`。

## 2026-07-30 23:03 - PC 声望称号移至特色称号位置并增强显示

### 最小改动

- 仅修改 `145Client\Models\MapObject.cs`，未修改服务端协议、称号属性、安卓端及其他 UI。
- 声望称号字体由默认 9 号常规字体调整为 12 号粗体，使用亮黄色文字和橙红色发光描边。
- 声望称号改为绘制在人物血条上方、原特色称号所在的头顶区域；标签底边与最高血条位置保留约 2 像素间距。
- 声望称号与特色称号互斥显示：存在声望称号时优先显示声望称号并移除当前特色称号头顶特效；声望称号为空时，原特色称号按既有逻辑自动恢复。特色称号 Buff、属性和持续时间不受影响。
- 成就称号、人物名字、行会名和血条的原有绘制逻辑未修改。

### 构建与验证

- `145Client` Release 编译成功，无编译错误；仅保留项目原有 `ChkLockMonEffect` 未赋值警告。
- 新建独立完整客户端目录：`D:\Debug\4月18日更新\Client-声望称号特色位发光`，未覆盖初始客户端及上一份声望称号客户端。
- 新 `Mir3.exe` 大小：`3,926,016` 字节。
- 新 `Mir3.exe` SHA-256：`0B1C96EB43D97A4EFE053648CB3D2B711D3DB33689C1FED828F1638D01F2E1DB`。
- 本次没有重新编译安卓端；服务端协议没有变化，继续与上一批声望称号服务端配套使用。

## 2026-07-30 22:35 - 全量编译并生成不覆盖原目录的独立发布包

### 编译与组装

- 将此前完成的源码改动统一编译为配套的服务端、PC 客户端和安卓客户端；新增 `FameTitle` 协议字段的三端来自同一份当前源码，部署时必须配套使用。
- 服务端使用 Release/x64 构建成功，沿用原服务端内嵌的 `Server.exe.licenses` 许可资源，并从本机 `D:\相聚\.tools\devexpress-23.2` 解析 DevExpress 23.2 编译依赖；生成文件已确认包含 `Server.exe.licenses`、`costura.library.dll.compressed` 及 DevExpress 23.2 嵌入资源。
- 服务端仅保留项目原有的 `System.Runtime.InteropServices.RuntimeInformation` 4.0.1/4.0.2 解析警告，无编译错误。
- PC 客户端使用此前验证通过的 `145Client` Release 构建文件；安卓使用此前完成的 Release/AOT 签名包。
- 为避免覆盖，先完整复制原发布资源，再仅在新目录中替换新编译主程序和服务器版声望称号脚本；未使用硬链接。

### 独立交付产物

- PC 客户端目录：`D:\Debug\4月18日更新\Client-声望称号头顶显示`，共 `2,807` 个文件、`7,068,873,887` 字节。
- PC 主程序：`Mir3.exe`，大小 `3,926,016` 字节，SHA-256：`EF2FC4E8BA6DCA3A6BEF8D31BAE0A9288C2D44A36C2E31E0BDE88252924B8E64`。
- 服务端目录：`D:\Debug\4月18日更新\Server-声望称号头顶显示`，共 `2,679` 个文件、`1,766,937,970` 字节。
- 服务端主程序：`Server.exe`，大小 `82,849,280` 字节，SHA-256：`40595A43CAAEA93037D91D77B02E41069748871AD773AB0597164701EE15A224`。
- 安卓 APK：`D:\Debug\4月18日更新\Android-118.25.67.175\Mir3-118.25.67.175-声望称号头顶显示-Signed.apk`，大小 `58,954,993` 字节，SHA-256：`CEBCD8C48C9B4995B269BBC6727EEF0876F2301514A0E8468C9556861C258278`。
- 新服务端的 `Scripts\Npc` 与 `Scripts888\Npc` 均放入服务器版 `管理中心.py` 和 `声望称号.py`；两套目录对应文件哈希一致。`管理中心.py` SHA-256：`D2B88336E3C48086DC8C938283FF407DDC764729378F95F8DD206A2D54C62B28`，`声望称号.py` SHA-256：`559C24BDCE3FFA9CD99F254169DB826335EBCF41B40C78717963D54DC9987F94`。

### 验证与不覆盖确认

- `robocopy` 核对：客户端原目录 `2,807` 个文件全部复制成功，服务端原目录 `2,679` 个文件全部复制成功，失败数均为 0。
- 原 PC `Mir3.exe` SHA-256 仍为 `FDDE3B807B1F2FE0B942A3C454F9196FCF7823ECDE6AD7FE2327C343FEA29EA9`；原服务端 `Server.exe` SHA-256 仍为 `BF20E400CC2F4324900E6D0293F330BFB740FE1D40B60A56EC6F801E0B798B90`，与新目录文件不同，原目录未被覆盖。
- 安卓 APK 通过 `apksigner` 复核：v1、v2、v3 为 `true`，签名者数量 1；v4 与 SourceStamp 未启用，符合项目原发布方式。
- 当前运行中的服务端进程未停止、未替换；新服务端未并行启动，以免争用端口、数据库和在线数据。
- 怪物模型偶发闪烁仍按用户要求列为待处理，本次仅编译现有改动，未改动该项代码。

## 2026-07-30 22:20 - 声望称号头顶显示安卓 Release 构建完成

### 构建修复

- 检测到新安装的系统 JDK 为 Oracle JDK 26；由于 .NET 8 Android 工具链要求兼容的 JDK 17，本次实际使用独立目录中的 Microsoft OpenJDK 17.0.8，不修改系统 `JAVA_HOME`。
- 此前 AAPT2 `APT2000` 并非资源缺失，而是 AAPT2 对源码中文路径的兼容问题；临时将 `D:\相聚假人\Source` 映射为纯英文盘符 `X:` 后，Android Debug 与 Release 资源打包均通过。构建结束后已移除临时盘符映射。
- Release 发布启用项目原有裁剪、AOT 和签名配置，发布成功，保留项目原有编译警告，无新增编译错误。

### 最终安卓产物

- APK：`D:\Debug\4月18日更新\Android-118.25.67.175\Mir3-118.25.67.175-声望称号头顶显示-Signed.apk`
- 大小：`58,954,993` 字节。
- SHA-256：`CEBCD8C48C9B4995B269BBC6727EEF0876F2301514A0E8468C9556861C258278`。
- `apksigner` 验证通过：v1、v2、v3 签名均为 `true`，签名者数量为 1；v4 未启用，与项目现有发布方式一致。

### 部署状态

- 当前检测到两个安卓设备：MuMu `127.0.0.1:7555` 与 `emulator-5554`。
- 本次未自动安装 APK。该客户端包含新增 `FameTitle` 协议字段，必须先部署配套重新编译的服务端；直接连接旧服务端存在协议不匹配风险。
- 服务端核心 `ServerLibrary` 已编译通过；完整 `Server.exe` 在本机仍受 DevExpress `licenses.licx` 的 `lc.exe` 授权编译步骤阻断，不能把未包含合法许可资源的临时构建当作正式服务端交付。

## 2026-07-30 22:15 - 声望称号显示在人物头顶

### 实现方式

- 九级声望称号仍由装备槽 `EquipmentSlot.FameTitle`（槽位 16）决定，不改称号属性、消耗、特色称号 Buff 或成就称号数据。
- 在现有登录信息 `StartInformation`、周围玩家信息 `ObjectPlayer` 和外观刷新包 `PlayerUpdate` 中各增加一个 `FameTitle` 字符串；服务端直接发送当前声望称号装备的物品名，没有新增独立消息类型。
- 服务端登录、进入视野与 `SendShapeUpdate` 三条现有同步路径均填充声望称号，自己与周围玩家使用同一数据来源。
- PC `145Client` 与安卓 `Mir3.Mobile` 复用现有头顶标签系统，新增金色 `『声望称号』` 文字；存在成就称号时自动显示在成就称号上方，避免相互覆盖。特色称号原有 `CustomBuffInfo.OverheadTitle` 图片效果保持不变，可同时显示。
- `D:\Video\声望称号.py` 在升级成功、扣除声望后补充调用 `SendShapeUpdate()`，保证升级换级后立即广播新称号。

### 修改文件

- `Library\Globals.cs`
- `Library\Network\ServerPackets.cs`
- `ServerLibrary\Models\Player\Initialize.cs`
- `ServerLibrary\Models\Player\PlayerObjectBase.cs`
- `ServerLibrary\Models\Player\GameControl.cs`
- `145Client\Models\MapObject.cs`、`PlayerObject.cs`、`UserObject.cs`、`Envir\CConnection.cs`
- `Mir3.Mobile\Client\Models\MapObject.cs`、`PlayerObject.cs`、`UserObject.cs`、`Envir\CConnection.cs`
- `D:\Video\声望称号.py`

### 验证

- `ServerLibrary` Release 编译成功；反射检查确认 `StartInformation`、`ObjectPlayer`、`PlayerUpdate` 均包含类型为 `string` 的 `FameTitle` 属性。
- PC `145Client` Release 编译成功，仅保留项目原有未使用字段警告；验证文件：`D:\相聚假人\Source\.build-check\fame-title\pc\Mir3.exe`。
- 安卓 Debug 已完成全部 C# 编译并生成 `Mir3.Droid.dll`；后续 AAPT2 打包阶段因项目现有 `obj\Debug\assets` 路径错误 `APT2000` 停止，该错误发生在代码编译之后，不是本次称号代码错误。验证文件：`D:\相聚假人\Source\Mir3.Droid\obj\Debug\Mir3.Droid.dll`。
- `D:\Video\管理中心.py` 与 `D:\Video\声望称号.py` 再次通过服务端同版本 IronPython 2.7 编译检查。
- 本次未覆盖 `D:\Debug\4月18日更新\Server` 的本地综合服务文件，也未替换现有服务端、PC 客户端或 APK 成品。

### 部署注意

- 本功能扩展了现有协议字段，服务端、PC 客户端和安卓客户端必须使用同一批次重新编译的版本，不能只更新脚本或单独更新一端。
- 尚未部署到运行服，人物头顶的最终位置与多人可见性需在配套服务端和客户端安装后进行游戏内验证。

## 2026-07-30 21:15 - 服务器版综合服务接入声望称号

### 服务器交付文件

- 以用户提供的服务器现用文件 `D:\Video\管理中心.py` 为唯一基准，只修改“声望称号”调用：入口菜单 `1` 直接调用声望脚本，后续使用隔离编号 `6001/6002/6003`，不再依赖地图上生成 210 号 NPC。
- 配套更新 `D:\Video\声望称号.py`，增加菜单偏移识别，并保留九级称号、逐级声望消耗以及此前完成的升级复检、背包空位检查和失败保护。
- 未使用服务器版覆盖 `D:\Debug\4月18日更新\Server` 本地目录；处理中曾短暂同步的服务器版 NPC 编号、死亡竞技入口和主菜单排版已经全部撤销，本地原内容保留。

### 验证与交付

- 使用服务端同版本 IronPython 2.7 对 `D:\Video\管理中心.py` 与 `D:\Video\声望称号.py` 编译检查，两份均通过。
- 配套调用静态核对通过：综合服务菜单 `1` 打开称号主菜单，`6001/6002/6003` 对应称号菜单 `1/2/3`。
- `D:\Video\管理中心.py` SHA-256：`D2B88336E3C48086DC8C938283FF407DDC764729378F95F8DD206A2D54C62B28`。
- `D:\Video\声望称号.py` SHA-256：`3C84ACB385C3E5DF144B49572110E057EAD753E7527F29FB95B7494CBAAE5CC7`。
- 上服务器时两份文件必须同时更新并重启/重载脚本；本次未连接远程服务器，也未改动在线角色数据。

## 2026-07-30 20:45 - 综合服务声望称号完善

### 服务端脚本修改

- 按 `D:\Video\声望称号.py` 保留原九级声望称号及逐级消耗：江湖初出 200、新进高手 1000、江湖侠客 2000、武林名宿 4000、仁义大侠 6000、善仁英雄 10000、尊扬义侠 15000、英雄豪杰 20000、武林至尊 50000；称号属性继续读取现有物品数据库，未修改数值。
- 修改 `D:\Debug\4月18日更新\Server\Scripts\Npc\管理中心.py` 和 `Scripts888\Npc\管理中心.py`：综合服务的“声望称号”不再依赖地图中必须存在 210 号 NPC，改为直接复用声望称号脚本，并使用独立菜单编号 `6001` 至 `6003`，避免与综合服务原菜单冲突；原 210 号 NPC 入口保持可用。
- 修改 `D:\Debug\4月18日更新\Server\Scripts\Npc\声望称号.py` 和 `Scripts888\Npc\声望称号.py`：确认升级时重新校验当前称号、声望及人物背包空位；满级或异常称号不再发生数组越界；创建新称号后核对装备结果，创建失败不扣声望，并尝试恢复原称号。
- 升级成功后显示新称号和剩余声望，并可继续逐级进阶；声望不足、背包无空位、物品数据异常均返回明确提示。

### 验证

- 使用服务端同版本 IronPython 2.7 运行库对 `Scripts`、`Scripts888` 下的四份修改脚本执行编译检查，全部通过。
- 静态核对九级称号顺序与消耗、满级边界、声望复检、背包空位、创建结果和失败恢复分支均存在；两份声望称号脚本 SHA-256 一致。
- 综合服务菜单路由核对通过：入口菜单 `1` 打开称号主菜单，后续 `6001/6002/6003` 分别映射称号脚本的 `1/2/3`，不再切换 `Sender.NPC`。
- 当前服务端进程未运行，因此未执行在线角色扣声望与装备称号的实机数据验证；启动或重启服务端加载脚本后需在游戏内手工验证一次。

## 2026-07-30 20:00 - 安卓分解标题栏布局、功能栏微调及全选有效性修复

### 界面调整

- 修改 `Mir3.Mobile\Client\Scenes\Views\NPCDialog.cs`：隐藏分解窗口标题“分解物品”，将“角色包全选、宠物包全选、分解”三个按钮移动到原标题栏，按钮宽度由 `79` 调整为 `70`，避开右侧关闭按钮。
- 分解窗口客户区高度由“物品格高度 + 50”缩短为“物品格高度 + 25”，取消原底部按钮行；“分解成本”保留在物品格下方并完整显示，改善小屏幕裁切问题。
- 修改 `Mir3.Mobile\Client\Scenes\GameScene.cs`：小地图左侧快捷按钮组 Y 坐标由 `130` 上移到 `70`，位于右上箭头下方；继续复用上一版互斥显隐逻辑，展开“附近/血量”时快捷组隐藏。
- 点击头像弹出的左侧竖排功能栏整体向右、向下各移动 `10` 像素：位置由头像面板偏移 `(+15, +100)` 调整为 `(+25, +110)`，内部按钮和间距不变。

### 全选按钮修复

- 用户验证上一版“角色包全选”和“宠物包全选”只有界面、点击无效果。
- 首次尝试将 PC 风格 `MouseClick` 改为安卓 `TouchUp`，用户复测后仍无效果；该方案不足以解决静默过滤问题。
- 最终在 `NPCItemFragmentDialog` 内增加局部批量链接方法：直接遍历指定人物包或宠物包，将符合现有分解规则的物品依次链接到空分解格，不再依赖单件拖拽入口的 `CheckLink/MoveItem` 状态。
- 安全规则保持不变：婚戒、锁定物品、不可分解物品继续跳过；已链接物品不重复选择；分解格满时停止；服务端 `NPCFragment` 协议和最终分解提交逻辑未修改。
- 当本次点击没有找到任何合法物品时，在聊天框提示“没有可分解物品”，避免再次表现为无反馈。

### 构建过程与中间版本

- 首次标题栏坐标代码误用了 `Point.Right`，被 C# 编译器拦截并改为 `X + Width`；错误版本未生成、未安装。
- 中间 APK `Mir3-118.25.67.175-分解按钮移至标题栏-快捷键上移-Signed.apk` 仅完成标题栏及快捷区布局，已被后续版本替代。
- 中间 APK `Mir3-118.25.67.175-分解全选触摸修复-功能栏微调-Signed.apk` 仅调整触摸事件，用户确认仍无效果，**不得作为最终版本交付**。

### 最终构建产物

- APK：`D:\Debug\4月18日更新\Android-118.25.67.175\Mir3-118.25.67.175-分解全选有效修复-功能栏微调-Signed.apk`。
- 大小：58,950,897 字节。
- SHA-256：`D41A29331CDB3E7B79F29F6DE494FACFEE02200D23181889F5CB4AF8FB96F307`。
- 内置服务器配置保持为 `118.25.67.175:7000`。

### 验证状态

- Android Release 发布成功，无编译错误；保留项目原有编译警告。
- 已覆盖安装到 MuMu 模拟器 `127.0.0.1:7555`；应用正常启动、进程存活，启动日志无致命异常。
- 安装前的布局截图已确认标题栏三按钮、缩短后的分解窗口、右侧快捷区上移均正常；左侧功能栏最终坐标已由源码和编译结果确认。
- 最终批量链接行为已交由用户在当前模拟器中复测；在用户确认前不标记为已完全验证。

## 2026-07-30 19:13 - 安卓包裹排行互换及分解双背包全选

### 源码修改

- 修改 `Mir3.Mobile\Client\Scenes\Views\Phone\PhoneDownCentButtons.cs`：仅交换小地图左侧功能区“包裹”和“排行”的坐标；右列由上到下调整为“排行、挖肉、包裹、角色”，其他快捷按钮位置和点击逻辑不变。
- 修改 `Mir3.Mobile\Client\Scenes\Views\NPCDialog.cs`：分解物品窗口原“全选”按钮明确为“角色包全选”，继续遍历人物背包并复用原 `CheckLink` 与 `MoveItem` 逻辑。
- 在原按钮与“分解”按钮之间新增“宠物包全选”，遍历宠物背包并复用相同的可分解校验和分解格链接逻辑；未新增服务端协议。
- 分解窗口原宽高足以容纳左、中、右三个 `79` 像素按钮，因此未扩大窗口，也未修改分解成本、分解数量或最终提交逻辑。
- 此前标记为待处理的怪物模型闪烁代码未修改。

### 构建产物

- APK：`D:\Debug\4月18日更新\Android-118.25.67.175\Mir3-118.25.67.175-包裹排行互换-分解双背包全选-Signed.apk`。
- 大小：58,950,897 字节。
- SHA-256：`3953364EA9EC42B37086FE3BF98713BF63BF3C34B50A61D3C5AD5F466F76E539`。
- 内置服务器配置保持为 `118.25.67.175:7000`。

### 验证

- Android Release 发布成功，无编译错误；保留项目原有编译警告。
- 源码回读确认：包裹按钮坐标为 `(60, 110)`，排行按钮坐标为 `(60, 0)`；分解窗口包含“角色包全选”和“宠物包全选”两个入口。
- 已覆盖安装到 MuMu 模拟器 `127.0.0.1:7555`，安装成功；应用启动后进程正常存活，启动日志无致命异常。
- 已实际进入游戏并打开分解窗口：确认底部依次显示“角色包全选、宠物包全选、分解”，窗口尺寸与文字显示正常；右侧快捷区确认“排行”在顶部、“包裹”在第三行。
- 验证截图：`D:\Debug\4月18日更新\Android-118.25.67.175\mir3_包裹排行互换_启动验证.png`。
- 两个全选按钮在背包存在可分解物品时的最终选择结果及分解提交，由用户在游戏内手动确认。

## 2026-07-30 18:55 - 安卓功能按钮切换、角色入口下移及宠物全部入包

### 源码修改

- 修改 `Mir3.Mobile\Client\Scenes\Views\Phone\PhoneDownCentButtons.cs`：在“排行”下方增加“角色”入口，按钮组由三行扩展为四行；角色按钮仍复用原 `PhoneUI` 素材索引 `55` 和原角色面板显隐逻辑。
- 修改 `Mir3.Mobile\Client\Scenes\Views\Phone\PhoneRightButtonsPanel.cs`：隐藏右下战斗面板中原有的重复“角色”入口。
- 修改 `Mir3.Mobile\Client\Scenes\GameScene.cs`：小地图左侧功能按钮组的 Y 坐标由 `70` 下移到 `130`，并仅将该按钮组公开给现有右上选人面板同步显隐。
- 修改 `Mir3.Mobile\Client\Scenes\Views\GroupDialog.cs`：复用原“附近/血量”选人箭头；选人面板展开时隐藏功能按钮组，收起时恢复功能按钮组，两个区域不再互相遮挡。
- 修改 `Mir3.Mobile\Client\Scenes\Views\CompanionDialog.cs`：按钮文字由“全部入仓”改为“全部入包”，批量移动目标由人物仓库改为人物背包，并移除仅适用于入仓的 `CanStore` 和婚戒过滤；锁定物品仍跳过，目标背包无空位时停止。
- PC 客户端、服务端协议和此前标记为待处理的怪物模型闪烁代码均未修改。

### 构建产物

- APK：`D:\Debug\4月18日更新\Android-118.25.67.175\Mir3-118.25.67.175-功能切换-角色下移-宠物全部入包-Signed.apk`。
- 大小：58,950,897 字节。
- SHA-256：`8E4F66A044B36B15DC587085CC456054962F302A247E5B944783CCE1ACC839C0`。
- 内置服务器配置保持为 `118.25.67.175:7000`。

### 验证

- Android Release 发布成功，无编译错误；首次并行 AOT 发布发生临时文件冲突，改为单进程增量发布后成功，未修改业务代码规避构建问题。
- 已覆盖安装到 MuMu 模拟器 `127.0.0.1:7555`，安装成功，应用正常启动并进入游戏场景，进程持续存活且日志无致命异常。
- 游戏场景截图确认功能按钮组已下移，“角色”位于“排行”下方；用户在模拟器中确认界面已经正常。
- 宠物背包实际有物品时的批量搬运结果由用户后续游戏操作继续确认。

## 2026-07-30 18:28 - 安卓怪物模型闪烁列为待处理

### 当前状态

- 历史状态（2026-07-30）：**待处理，尚未修复**。
- 用户实录：`D:\Video\MXClip_Screenrecorder-2026-07-30-09-21-15-975_202.mp4`。
- 已确认触发条件：攻击、受击、切换目标时更频繁；人物移动经过附近怪物时也会出现。
- 逐帧可见怪物本体会在相邻视频帧中完全消失再恢复，但人物、血条和目标状态仍在；因此不是单纯的选中高亮变化。

### 本次无效尝试与回退

- 曾在 `Mir3.Mobile\Client\Models\MonsterObject.cs` 尝试“当前纹理帧未就绪时沿用最近有效帧”，用户在模拟器手工验证后确认仍会闪烁。
- 实验 APK：`D:\Debug\4月18日更新\Android-118.25.67.175\Mir3-118.25.67.175-怪物模型帧回退修复-Signed.apk`。
- 大小：58,946,801 字节；SHA-256：`94642B18752CEE2656E1284EFE39E72D2D1F6D56929914B707506CE973A0AE30`。
- 此 APK 仅保留用于问题对比，**不得作为已修复版本交付**；当前模拟器安装的是该实验版。
- 已从源码撤销无效的帧回退逻辑，并恢复原怪物选中高亮行为；未重新编译，避免产生另一个无实际修复的新 APK。
- 后续需要继续排查怪物对象可见性、绘制排序/裁剪及移动端渲染状态，不再把“纹理帧未就绪”视为已确认根因。

### 2026-08-15 排查结论与最小修复（源码完成，待真机确认）

- 排查范围覆盖 PC `145Client`、活动移动端共享代码 `Mir3.Mobile`、Android `Mir3.Droid`、iOS 共享入口、怪物对象生命周期、MapControl/Cell 绘制、动画帧、纹理缓存、异步任务和 Android 条件编译。客户端没有怪物对象池，也没有 Unity 风格 `Renderer`、`Animator`、`SetActive`、LOD 或遮挡剔除链路；移动端实际使用 MonoGame `GraphicsDevice`、`Texture2D` 和 `SpriteBatch`。
- 定位根因：`Mir3.Mobile\Client\Envir\MirLibrary.cs` 的微端图片下载 `Task.Run` 曾在线程池线程直接执行 `ImageSetData`、`ShadowSetData`、`OverlaySetData`，创建/写入 GPU 纹理并修改 `DXManager.TextureList`。Android 渲染线程与后台任务之间的竞态会导致不同怪物、不同动作阶段随机出现本体消失；Windows 端没有同一条异步 GPU 提交路径。
- 最小修复：后台线程仅负责下载资源字节；通过每张图片的待提交缓冲交给游戏主线程，由 `CreateImage` 在绘制线程完成纹理创建；`DisposeTexture` 同步清除待提交数据，避免缓存清理后旧任务回写；不修改怪物动画、对象生命周期、MapControl 绘制排序或资源文件。
- 配置核对：游戏服务器为 `114.132.90.203:7100`，更新服务器为 `http://114.132.90.203:7090/`；本轮未重复修改已正确配置的 `Config.cs`。`MicroClientIP=192.168.2.241`、`MicroClientPort=8000` 是独立的微端资源服务配置，未擅自替换。
- 验证：修复前源码线程断言按预期 RED（后台任务直接触达三种纹理提交）；修复后 GREEN。`Mir3.Droid` Release/AOT 发布退出码 `0`、`0 errors`，仅保留项目既有 XML 注释、过时 API、平台兼容性和未使用字段警告；未部署或覆盖外部交付目录。
- 修改文件：`Mir3.Mobile\Client\Envir\MirLibrary.cs`、`CHANGELOG.md`。本轮 APK：`Mir3.Droid\bin\Release\net8.0-android\publish\com.xj.Mir3.Droid-Signed.apk`，SHA-256 `29B1F15B8D892A3BCB6A6B1C5C9378263D548A61F5ADECEF6F8FD09AFD6D0022`；源码 SHA-256 `0555DF92C2160336BD58064B6B67F87133BA0B77D64F704CD1BFB09376130E60`。
- 当前边界：尚未在模拟器和真机安装本次 APK 做运行时视觉复测；仍需覆盖怪物站立、移动、攻击、死亡、首次微端资源加载和地图切换场景，不能将静态断言/构建通过等同于视觉验收。

### 2026-08-15 第二轮真机复测后的缓存失效修复（源码完成，待再次真机复测）

- 用户确认使用刚编译的发布 APK 真机复测后仍会随机闪烁，因此排除“误测旧 APK”作为本轮解释；当前仍没有连接设备可供读取运行时日志。
- 第二轮静态定位发现：移动端地图通过 `MapControl.ControlTexture` 缓存整张地图，但 `MapObject.Visible`、`Dead`、`FrameIndex` 和换格位置变化没有统一使该 RenderTarget 失效；这会让 Android 继续显示对象的旧帧或空帧。该结论已通过修复前结构断言 RED 复现，属于源码缺口，仍需真机视觉确认是否覆盖全部闪烁路径。
- 最小修复：`Mir3.Mobile\\Client\\Models\\MapObject.cs` 将 `Visible` 改为带失效通知的属性；`FrameIndex`、`Dead` 和 `LocationChanged` 在状态变化时使 `MapControl.TextureValid=false`；未改对象池、怪物动画定义、网络协议、资源或服务端。
- 修复后结构断言全部 PASS；Android Release/AOT 发布退出码 `0`、`0 errors`，仅保留既有警告。
- 本轮 APK：`Mir3.Droid\\bin\\Release\\net8.0-android\\publish\\com.xj.Mir3.Droid-Signed.apk`，SHA-256 `20133CF6B3DC48D970D526AF530915E740AC2B725D5B8225C7248C5B8D24A94B`；`MapObject.cs` SHA-256 `0FE361BA4E27B425B14AC5CF47901F1BAA170E47071E60DF74E857E38A3CB027`；`MirLibrary.cs` 未变更，SHA-256 `0555DF92C2160336BD58064B6B67F87133BA0B77D64F704CD1BFB09376130E60`。
- 第三轮最小修复：`MirLibrary.cs` 仅在 `MapControl` 开启的短作用域内记录本次地图缓存刷新中“预期存在但暂未就绪、可重试”的纹理；`MapControl.cs` 使用一个有界候选 RenderTarget，只有所有预期纹理绘制完成才交换 `ControlTexture`，不完整刷新保留上一张完整前台并保持重试；候选和前台纹理在尺寸变化及生命周期中释放。
- 纹理完整性纠正：库头/图片数组尚未加载仍标记 transient；负索引、越界、空 image、`Position==0`、`1x1` 占位图和 `OverlayDataSize==0` 合法空叠加均不污染事务；阴影缺失继续按 body image fallback 的实际数据判断。所有 `texture == null` 分支均按 `MirImage` 与 `ImageType` 判断，后台下载仍只发布字节缓冲。
- 本轮修改文件仅为 `MirLibrary.cs`、`MapControl.cs`、`.diagnostics\\test_android_map_texture_completeness_contract.ps1` 与 `CHANGELOG.md`；未修改受保护的 `MapObject.cs`、`DXControl.cs`、资源或网络配置。契约受限于项目没有可执行 GPU seam，为最窄静态源码契约。
- 本轮 TDD：事务/纹理完整性契约先以 permanent/empty 反例 RED，生产修改后 GREEN；transient/expected typed marker、invalid/empty exclusions 和事务前后台断言全部通过。Android Release publish 退出码 `0`、`0 errors`，保留既有警告，未部署 APK。最终 APK 为 `Mir3.Droid\\bin\\Release\\net8.0-android\\publish\\com.xj.Mir3.Droid-Signed.apk`，65,144,136 字节，SHA-256 `C119F8031351C9BFD2B9BB64F51290D0C868C3549A285E152D97EB43674F4ACC`；`MirLibrary.cs` SHA-256 `66CC570CB45A8E8B05C12A13E7E455C552C1421DF545B8BABE1F71BB621E750A`；契约 SHA-256 `852A3BF42CA34B4A27E16151F9D9D1329A9603B6E082E104B7C1C1F06C80D416`。
- 本轮运行时验收仍为人工：需用 Release APK 在真机覆盖站立、移动、攻击、死亡、首次微端资源加载、地图切换及长时间缓存过期观察；静态契约和构建通过不等同于视觉验收。
- 运行时边界：尚未确认该 APK 在真机覆盖站立、移动、攻击、死亡及微端资源首次加载场景后是否消除闪烁；不能将本轮结构断言和构建通过等同于视觉验收。

## 2026-07-30 00:31 - 怪物高亮方向尝试（验证无效，已撤销）

### 当时判断与源码修改

- 修改 `Mir3.Mobile\Client\Scenes\Views\MapControl.cs`。
- 当时根据低频连续截图误判为移动端对当前怪物额外执行 `HIGHLIGHT` 混合重绘；后续用户视频和手工验证证明该判断不完整。
- 怪物已经通过移动端选中光圈、目标信息面板和血条提供明确反馈，因此仅跳过怪物的第二次高亮混合重绘。
- 怪物基础模型、阴影、动画、受击、死亡、伤害效果和战斗逻辑均未修改；玩家与 NPC 的原高亮逻辑保持不变，PC 客户端未修改。

### 构建产物

- APK：`D:\Debug\4月18日更新\Android-118.25.67.175\Mir3-118.25.67.175-怪物模型闪烁修复-Signed.apk`
- 大小：58,946,801 字节。
- SHA-256：`2883BBDB23967817F83F18B0B7E24BBCCF3BAD98C6D6DAB5A34B05176F55928A`。
- 内置服务器配置保持为 `118.25.67.175:7000`，并包含此前宠物全部入仓与小地图快捷键下移等改动。

### 当时自动验证（不足以确认修复）

- Android Release 发布成功，无编译错误；保留项目原有编译警告。
- APK v1、v2、v3 签名验证通过，MuMu Android 15 模拟器覆盖安装成功。
- 使用保存账号进入游戏并开启自动打怪，低频连续抓取 12 张截图未捕获到短暂闪烁，FPS 为 60–61；该采样方式后来被证明不足以覆盖相邻视频帧中的模型消失。
- 怪物选中光圈、目标信息面板、血条、伤害数字和死亡切换均正常，Android 日志未发现致命异常。
- 验证截图目录：`D:\Debug\4月18日更新\Android-118.25.67.175\flicker_fix_frames`。

## 2026-07-29 23:45 - 安卓小地图快捷按钮组下移

### 源码修改

- 修改 `Mir3.Mobile\Client\Scenes\GameScene.cs`。
- 根据模拟器实际画面，将小地图左侧六键快捷按钮组的 Y 坐标从 `0` 调整为 `70`。
- 仅改变整个按钮组的垂直位置；横向位置、两列三行内部排列、按钮功能和其他界面均未修改。
- 调整后避开小地图左上方的“附近”按钮，并保留约 5 像素视觉间距。

### 构建产物

- APK：`D:\Debug\4月18日更新\Android-118.25.67.175\Mir3-118.25.67.175-宠物全部入仓-快捷键下移70-Signed.apk`
- 大小：58,946,801 字节。
- SHA-256：`94225338CC774630724EFEA31811097A85245EF46673FA89094EA23782762771`。
- 上一版快捷键顶部对齐 APK 未覆盖，便于回滚对比。

### 验证与中断恢复

- 任务中断导致 Android AOT 缓存不完整，曾报 `Sequence contains no elements`；仅清理 Release 构建缓存后完整重建成功。
- Android Release 编译成功，APK v1、v2、v3 签名验证通过。
- MuMu Android 15 模拟器覆盖安装成功，应用启动无致命崩溃。
- 使用已保存的登录信息进入服务器、角色及游戏场景完成实际布局验证。
- 验证截图：`D:\Debug\4月18日更新\Android-118.25.67.175\mir3_shortcuts_y70_verified.png`。
- 截图确认“附近”按钮与六键快捷按钮组不再重叠。

## 2026-07-29 23:25 - 安卓快捷功能移动到小地图旁

### 源码修改

- 修改 `Mir3.Mobile\Client\Scenes\Views\Phone\PhoneDownCentButtons.cs`。
- 补齐现有安卓快捷按钮容器的尺寸和背包按钮，并按两列三行排列：技能/背包、设置/挖肉、聊天/排行。
- 修改 `Mir3.Mobile\Client\Scenes\GameScene.cs`，将快捷按钮容器固定在小地图左侧，间距 10 像素。
- 修改 `Mir3.Mobile\Client\Scenes\Views\Phone\PhoneRightButtonsPanel.cs`，隐藏右下角战斗面板内对应的六个重复入口。
- 六项功能的原点击事件、按钮素材和业务逻辑保持不变；PC 客户端未修改。
- 骑马、挂机、攻击以及战斗技能快捷键的位置和显示逻辑保持不变。

### 构建产物

- APK：`D:\Debug\4月18日更新\Android-118.25.67.175\Mir3-118.25.67.175-宠物全部入仓-快捷键小地图旁-Signed.apk`
- 大小：58,946,801 字节。
- SHA-256：`71D85819414EAE04405DB3E69D9302C12AB8AC5E2A364EDE9E9E7CA037AEC52D`。
- 本次 APK 包含上一版本的宠物包裹“全部入仓”功能，旧 APK 未覆盖。
- 内置服务器配置保持为 `118.25.67.175:7000`。

### 验证与中断恢复

- 连续任务中断曾留下损坏的 Android AOT 中间程序集，构建报 `BadImageFormatException: Missing data directory`。
- 仅执行 `dotnet clean` 清理 `Release/net8.0-android` 生成缓存后完整重建成功；源码和已交付 APK 未被清理。
- Android Release 发布成功，无编译错误。
- APK v1、v2、v3 签名验证通过。
- MuMu Android 15 模拟器重新连接后覆盖安装成功。
- 启动后应用进程正常存活，无黑屏、权限异常或致命崩溃。
- 模拟器当前停留在登录阶段，游戏内小地图旁的最终视觉位置及六个按钮点击仍需登录角色后人工确认。

## 2026-07-29 22:47 - 安卓宠物包裹新增全部入仓

### 源码修改

- 修改 `Mir3.Mobile\Client\Scenes\Views\CompanionDialog.cs`。
- 在安卓宠物状态栏底部新增“全部入仓”按钮。
- 点击后遍历宠物包裹，将可存仓的道具和装备依次移入人物仓库。
- 复用现有 `ItemMove` 协议和格子锁定逻辑，没有新增或修改服务端协议。
- 禁止存仓的物品及婚戒会被跳过；不会卸下宠物当前穿戴的装备。
- 仓库没有可用格子时停止继续提交，避免无效请求和目标格冲突。

### 构建产物

- APK：`D:\Debug\4月18日更新\Android-118.25.67.175\Mir3-118.25.67.175-宠物包裹全部入仓-Signed.apk`
- 大小：58,946,801 字节。
- SHA-256：`40094098C054F4C5C759F633588774F2F9A64E3E129A10A6E102E70D7B37D407`。
- 内置服务器配置保持为 `118.25.67.175:7000`，旧 APK 未覆盖。

### 验证

- Android Release 发布成功，无编译错误；保留项目原有编译警告。
- APK v1、v2、v3 签名验证通过。
- MuMu Android 15 模拟器覆盖安装成功。
- 启动后应用进程正常存活并进入登录界面，无黑屏或致命崩溃。
- 启动验证截图：`D:\Debug\4月18日更新\Android-118.25.67.175\mir3_storeall_smoke.png`。
- 因模拟器当前停留在登录界面，宠物有物品时的实际批量搬运仍需登录游戏后人工确认。

## 2026-07-29 22:25 - 补录完整历史变更

- 补录 Windows 专用网络防火墙规则及端口验证。
- 补录手机资源目录、旧更新清单和数据库比对结果。
- 补录初始 APK 资源结构及被替代的旧 APK 哈希。
- 补录 Server.Web 首次启动失败原因和最终修正方式。
- 补录真机 ADB、MuMu 模拟器及黑屏诊断过程。
- 补录构建环境、目录连接、服务监听和连接验证。
- 本次只更新文档，没有重新修改源码、配置或二进制产物。

## 2026-07-29 22:13 - 新增远程服务器配置安卓客户端

### 配置

- 使用 `D:\Debug\4月18日更新\Mir3.ini` 作为安卓客户端内置初始配置。
- 游戏服务器：`118.25.67.175:7000`。
- 微端资源服务器：`118.25.67.175:8000`。
- 更新服务器：`http://118.25.67.175:7090/`。
- 客户端版本：`1.2.5.13`。
- 将内置 `Mir3.ini` 从 UTF-16 规范化为 UTF-8，再写入 `Data.zip`。
- 重新生成 `Mir3.Droid\Assets\Data.zip`，并确认 `Mir3.ini` 的 ZIP 权限属性正确。

### 构建产物

- APK：`D:\Debug\4月18日更新\Android-118.25.67.175\Mir3-118.25.67.175-Signed.apk`
- 大小：58,942,705 字节。
- SHA-256：`9056BAF336DA3E5716006A8D6E42CF4F21BDFBDAFD13D050AC6B133D7976B7E5`。
- 原本机服务器版本 APK 未被覆盖。

### 验证

- APK v1、v2、v3 签名验证通过。
- APK 内嵌配置回读验证通过。
- MuMu Android 15 模拟器全新安装成功。
- 运行时配置确认使用 `118.25.67.175`。
- 成功连接 `118.25.67.175:7090` 并开始下载 `DataAdd.zip`。
- 应用进程正常，无黑屏、权限异常或致命崩溃。

### 注意

- 该 APK 与本机服务器版本使用相同包名和版本号。
- 覆盖安装会保留原应用数据；切换服务器配置时应卸载旧版或清除应用数据后安装。

## 2026-07-29 21:46 - 修复安卓启动后一秒黑屏

### 根因

- 原内置 `Data.zip` 将 `Mir3.ini` 解压为仅可写、不可读权限 `-----w----`。
- `ConfigReader.Load()` 读取配置时抛出 `UnauthorizedAccessException`。
- 全局异常处理器吞掉异常，最终表现为黑屏但进程可能仍然存在。

### 源码修改

- 修改 `Mir3.Droid\DrodNative.cs`。
- 启动时试读 `Mir3.ini`。
- 只在配置确实不可读时删除损坏文件，随后由修正后的内置 `Data.zip` 自动恢复。
- 正常可读的用户配置不会被删除。
- 重新生成 `Mir3.Droid\Assets\Data.zip`，修正 ZIP 权限属性。

### 未保留的诊断尝试

- `File.SetUnixFileMode`：在 MuMu x86 到 ARM AOT 转译环境触发 Mono 原生断言，已撤销。
- `Java.IO.File.SetReadable/SetWritable`：在相同环境触发 Mono AOT 断言，已撤销。
- 最终版本不包含上述两种实现。

### 构建产物

- APK：`D:\Debug\4月18日更新\Android\com.xj.Mir3.Droid-Signed.apk`
- 大小：58,942,705 字节。
- MD5：`37075E77B4366C93F525095D997D2DB6`。
- SHA-256：`9CDB22ED465F7BD1328B5F5974BF7A3659D8AA953A844BC9856C708AEDBFD2D0`。
- 更新服务器 APK：`D:\Debug\4月18日更新\AndroidUpdate\聚聚MIRv1.2.5.13.apk`。
- 更新清单：`D:\Debug\4月18日更新\AndroidUpdate\APKVersion.bin`。

### 回归验证

- 使用坏权限旧配置进行覆盖安装，自愈成功。
- 全新安装成功。
- 恢复后的 `Mir3.ini` 权限为 `-rw-rw----`。
- 下载并解压完整基础资源成功。
- 681 个地图文件存在。
- 正常进入账号登录界面。
- APK v1、v2、v3 签名验证通过。

## 2026-07-29 20:05 - 部署安卓更新及微端资源服务

### 资源包

- 手机资源来源：`D:\BaiduNetdisk\手机端补丁\Data`。
- 地图来源：`D:\Debug\4月18日更新\Client\Map`。
- 生成 `D:\Debug\4月18日更新\AndroidUpdate\DataAdd.zip`。
- 包含 11 个手机 Data 文件和 681 个地图文件。
- ZIP 全量读取和 CRC 验证通过。
- 大小：156,312,477 字节。
- MD5：`DEACBB26AD73BC0BFC2E411C2091FF92`。
- SHA-256：`C2BD9BC49169C95B00A61EAB0145F7138CE419412A8AC72B8C43271CA40596E1`。

### 更新清单

- 生成 `D:\Debug\4月18日更新\AndroidUpdate\APKVersion.bin`。
- APK 版本：`1.2.5.13`。
- 基础资源文件：`DataAdd.zip`。
- 文件长度、MD5 和二进制格式回读验证通过。
- 当前未生成 `PList.Bin`；客户端将其 404 视为没有增量补丁并继续进入游戏。

### Server.Web 修改

- 将 `Server.Web\Program.cs` 从 GBK 转换为 UTF-8。
- 创建应用时通过 `WebApplicationOptions.WebRootPath` 设置安卓更新目录。
- 更新服务监听：`7080`。
- 微端 API 监听：`8000`。
- PC 资源目录：`D:\Debug\4月18日更新\Client`。
- 安卓更新目录：`D:\Debug\4月18日更新\AndroidUpdate`。
- 发布自包含 win-x64 服务到 `D:\Debug\4月18日更新\MicroServer`。

### 服务验证

- `APKVersion.bin` HTTP 下载与本地 MD5 一致。
- `DataAdd.zip` 支持范围请求和断点下载。
- 8000 API 返回资源与 PC 客户端源文件 MD5 一致。

## 2026-07-29 19:49 - 编译本机服务器安卓客户端

### 安卓网络配置

- 修改 `Mir3.Mobile\Client\Envir\Config.cs`。
- 游戏服务器：`192.168.2.241:7000`。
- 更新服务器：`http://192.168.2.241:7080/`。
- 微端资源服务器：`192.168.2.241:8000`。
- 清除移动端源码中的旧地址 `192.168.1.7`。

### 构建环境

- .NET SDK：`8.0.401`。
- Android workload：`34.0.43`。
- Android SDK：`C:\Users\chen\AppData\Local\Android\Sdk`。
- JDK 17：`C:\Users\chen\AppData\Local\Android\Jdk`。
- 使用 ASCII 目录连接 `D:\Mir3AndroidSource` 规避 AAPT2 无法处理中文源码路径的问题。

### 构建产物

- APK：`D:\Debug\4月18日更新\Android\com.xj.Mir3.Droid-Signed.apk`。
- 包名：`com.xj.Mir3.Droid`。
- 版本：`1.2.5.13`。
- 最低 API：23。
- 目标 API：34。
- 包含四种 ABI。

## 2026-07-29 19:10 - 修改 PC 客户端及服务端局域网配置

### PC 客户端

- 修改 `D:\Debug\4月18日更新\Client\Data\Network.ini`。
- 连接地址由 `192.168.1.7` 改为 `127.0.0.1`。
- 游戏端口保持 `7000`。
- 已验证 PC 客户端连接本机服务端成功。

### 游戏服务端

- 修改 `D:\Debug\4月18日更新\Server\Server.ini`。
- `IPAddress` 从 `127.0.0.1` 改为 `0.0.0.0`，允许局域网连接。
- 将配置文件规范化为 UTF-8。
- MySQL、商城及账号网页相关的本机地址未修改。

## 2026-07-29 19:03 - 编译 PC 客户端

- 编译项目：`145Client`。
- 目标框架：.NET Framework 4.8。
- 输出：`D:\Debug\4月18日更新\Client\Mir3.exe`。
- 大小：4,126,208 字节。
- SHA-256：`FDDE3B807B1F2FE0B942A3C454F9196FCF7823ECDE6AD7FE2327C343FEA29EA9`。

## 2026-07-29 - Windows 防火墙放行（历史补录）

- 新增 Windows 入站规则：`Mir3MobileLocalServer`。
- 方向：入站。
- 操作：允许。
- 协议：TCP。
- 本地端口：`7000,7080,8000`。
- 网络配置文件：仅 `Private`，未对公用网络开放。
- Edge traversal：关闭。
- 已验证规则启用。
- 已验证 `7000` TCP 连接成功。
- 已验证 `7080` 返回 HTTP 200。
- 已验证 `8000` 资源 API 返回 HTTP 200。
- 第一次使用普通权限创建规则失败，之后通过管理员 UAC 授权成功创建。

## 2026-07-29 - 手机资源完整性检查（历史补录）

### 原始手机补丁目录

- 目录：`D:\BaiduNetdisk\手机端补丁`。
- 文件总数：12。
- 总大小：123,119,803 字节。
- 包含 `APKVersion.bin` 和 `Data` 目录中的 11 个手机资源文件。
- 主要资源包括 `ClientSystem.db`、`Interface1c.Zl`、`MiniMap.Zl`、`PhoneUI.Zl`、`UI1.Zl`、`UI2.Zl`、`Wemade.zl` 等。

### 原始 APKVersion.bin 检查

- APK 版本：`1.2.5.13`。
- 原记录 APK：`聚聚MIRv1.2.5.13.apk`。
- 原记录 APK 大小：48,555,748 字节。
- 原记录 APK MD5：`D7EC9EA9AF9076EC6DBEDCDE56344FF4`。
- 原记录基础包：`DataAdd.zip`。
- 原记录基础包大小：172,260,352 字节。
- 原记录基础包 MD5：`23A7F504144F041320E8BE7F8F7C1CE4`。
- 上述原 APK 和原 `DataAdd.zip` 未在手机补丁目录中找到，因此不能直接复用旧清单。
- 未找到 `PList.Bin`。
- 最终根据实际新 APK 和新 `DataAdd.zip` 重新生成清单。

### PC 资源盘点

- `Map`：681 个文件，约 737,295,661 字节。
- `Sound`：1,688 个文件，约 1,161,800,089 字节。
- `Data`：412 个文件，约 5,142,017,172 字节。
- 根据客户端更新逻辑，基础包只需要手机专用 `Data` 和完整 `Map`。
- 其他大型资源和声音由 8000 微端 API 按需获取，因此没有全部打入 APK 或 `DataAdd.zip`。

### 数据库比对

- 手机补丁 `ClientSystem.db`：6,957,024 字节。
- PC 客户端根目录数据库：10,053,712 字节。
- PC `Data\ClientSystem.db`：10,053,968 字节。
- 服务端数据库与 PC `Data\ClientSystem.db` 一致。
- 服务端配置 `CheckPhoneVersion=False`，不会因为手机数据库哈希不同拒绝连接。
- 保留手机补丁数据库，避免使用 PC 数据库覆盖手机专用数据。

## 2026-07-29 - 安卓 APK 初始资源检查（历史补录）

- 初始 APK 内置 `Data.zip` 只包含启动所需的三个文件：
  - `Data/Interface.Zl`
  - `Data/StartMobileScene.Zl`
  - `Mir3.ini`
- 这属于客户端设计：APK 只内置启动资源，完整手机 Data 和地图由更新服务器下载。
- 初始 `Data.zip` 大小约 6.2 MB。
- 初次本机服务器版 APK 大小：58,942,705 字节。
- 黑屏修复前 APK SHA-256：`07D5A60D43E4FB35630C697E74B30984EAA42DFEF20AB345CD21B4A778753889`。
- 该哈希已被黑屏修复后的正式 APK 替代，仅保留用于回溯。

## 2026-07-29 - Server.Web 启动问题及修正（历史补录）

- 首次尝试在创建 `WebApplicationBuilder` 后调用 `UseWebRoot`。
- ASP.NET 7 启动时报错：Web 根目录不能在构建器创建后修改。
- 失败进程退出，未占用 `7080` 或 `8000`。
- 最终调整初始化顺序：
  - 先读取配置。
  - 使用 `WebApplicationOptions.WebRootPath` 创建构建器。
  - 再配置 `UseUrls`。
- 修正后自包含发布成功。
- 资源服务启动后同时监听 `7080` 和 `8000`。
- 服务不是 Windows 服务，电脑重启后仍需手动运行 `D:\Debug\4月18日更新\MicroServer\Server.Web.exe`。

## 2026-07-29 - 安卓黑屏诊断过程（历史补录）

- USB 真机最初被 Windows 识别为小米 ADB Interface，但 ADB 状态反复为 `offline`，无法稳定读取日志。
- 尝试过：
  - `adb reconnect offline`
  - 重启 ADB server
  - USB 调试重新授权
  - 文件传输模式重新连接
- 真机 ADB 仍不稳定，随后改用 MuMu Android 15 模拟器。
- MuMu ADB 端口：`127.0.0.1:7555` 和 `127.0.0.1:5555`。
- 在模拟器中稳定复现启动画面一秒后全黑。
- 从 `/sdcard/Android/data/com.xj.Mir3.Droid/files/Errors/` 获取到实际异常堆栈。
- 确认 `Mir3.ini` 权限为 `0020`，即 `-----w----`。
- 修复后覆盖安装与全新安装均验证通过。

### 诊断截图

- `D:\Debug\4月18日更新\Android\black-screen-repro-valid.png`：黑屏复现。
- `D:\Debug\4月18日更新\Android\fixed-screen-3.png`：修复后更新界面。
- `D:\Debug\4月18日更新\Android\fresh-install-screen.png`：全新安装后登录界面。
- `D:\Debug\4月18日更新\Android-118.25.67.175\verification.png`：远程配置版下载基础包。

## 2026-07-29 - 构建辅助目录和目录连接（历史补录）

- `D:\Mir3AndroidSource` → `D:\相聚假人\Source`。
- `D:\Mir3AndroidOutput` → `D:\Debug\4月18日更新\Android`。
- `D:\PhonePatch` → `D:\BaiduNetdisk\手机端补丁`。
- `D:\Mir3Client` → `D:\Debug\4月18日更新\Client`。
- `D:\Mir3AndroidUpdate` → `D:\Debug\4月18日更新\AndroidUpdate`。
- 创建原因：Android AAPT2 在中文源码路径下构建失败，ASCII 目录连接用于规避该限制。
- 这些目录均为 Junction，不复制原始数据。

## 2026-07-29 - 运行服务及连接验证（历史补录）

- 游戏服务端监听：`0.0.0.0:7000`。
- 本机资源服务监听：`[::]:7080` 和 `[::]:8000`。
- PC 客户端连接 `127.0.0.1:7000` 成功。
- 安卓本机版连接地址：`192.168.2.241`。
- 安卓远程版连接地址：`118.25.67.175`。
- 模拟器成功从本机 7080 下载并解压新 `DataAdd.zip`。
- 模拟器成功从远程 7090 开始下载 `DataAdd.zip`。
- 本机版下载完整资源后，应用目录约 834 MB，并正常进入登录界面。

## 2026-07-29 - 构建及发布工具安装（历史补录）

- 安装或启用 .NET SDK `8.0.401`。
- 安装 Android workload `34.0.43`。
- 配置 Android SDK。
- 配置 JDK 17。
- Android Release 构建启用了多 ABI AOT 和程序集裁剪。
- APK 使用 Android Debug 证书签名。
- v1、v2、v3 APK 签名均验证通过。
- v4 签名和 SourceStamp 未启用。

## 2026-07-29 之后的记录要求

每次修改后至少记录：

- 修改时间和目的。
- 修改过的源码或配置文件。
- 关键配置值，但不在日志中记录密码、密钥等敏感信息。
- 新生成或覆盖的产物路径。
- 文件版本、大小和 SHA-256。
- 执行过的验证及结果。
- 已知限制、未完成事项和回滚注意点。
## 2026-08-02 - 安卓客户端视频配置包

- 生成独立 APK：`D:\Debug\4月18日更新\Android-video-114.132.90.203-7000-20260802\Mir3-114.132.90.203-7000-video-config-Signed.apk`。
- 内嵌 `Data.zip` 的网络配置来自 `D:\Video\Mir3.ini`：游戏地址 `114.132.90.203:7000`，微端地址 `114.132.90.203:8000`，更新地址 `http://114.132.90.203:7090/`。
- 以既有客户端 APK 为基础，仅替换内嵌启动配置并重新签名；未修改游戏 DLL、代码或其他资源。
- 签名校验通过 APK v1、v2、v3；因本包使用当前本机调试签名，安装前需先卸载旧客户端。
- 源工程的 `Mir3.ini` 和 `Data.zip` 已恢复；`Data.zip` 原文件备份为 `Mir3.Droid\Assets\Data.zip.bak-20260802-video-config`。
## 2026-08-02 - 安卓客户端游戏端口 7100 包

- 生成独立 APK：`D:\Debug\4月18日更新\Android-video-114.132.90.203-7100-20260802\Mir3-114.132.90.203-7100-video-config-Signed.apk`。
- 配置基于 `D:\Video\Mir3.ini`，仅将游戏端口由 `7000` 改为 `7100`；其他配置未改。
- 使用既有客户端 APK，仅替换内嵌启动配置并重新签名；未修改源码、游戏 DLL 或其他资源。

## 2026-08-03 - 宠物背包自动回收脚本

- 修改实际运行脚本：
  - `D:\Debug\4月18日更新\Server\Scripts\Npc\其他\便捷传送.py`
  - `D:\Debug\4月18日更新\Server\Scripts\Ser\定时活动.py`
- 新增 `ExecuteCompanionEquipmentRecycleForSender`：只扫描 `Companion.Inventory`，沿用 `回收配置.py` 中的 `RECYCLE_EQUIPMENT` 和 `RECYCLE_REWARDS`，回收后发送宠物包格子更新封包、刷新宠物负重并按原金币配置发放奖励。
- 跳过 `Locked`、`Bound`、`Marriage`、`QuestItem` 标记；复用 `GV_PLAYER_RECYCLE_ENABLED`，关闭玩家开关时不执行自动回收。
- 修正人物回收统计：从 `GetItemCount` 合计值中扣除宠物包数量，避免旧的人物回收逻辑误删宠物包道具。
- 将自动回收任务从一次性 `ScheduledCall` 改为 `PeriodicCall`（每 1 秒），并移除会导致任务异常中断的未定义调试变量调用。
- 覆盖前备份：
  - `D:\Debug\4月18日更新\Server\Scripts\Npc\其他\便捷传送.py.bak-20260803-pet-recycle`
  - `D:\Debug\4月18日更新\Server\Scripts\Ser\定时活动.py.bak-20260803-pet-recycle`
  - `D:\相聚假人\Source\CHANGELOG.md.bak-20260803-pet-recycle`
- 修改后文件：`便捷传送.py` 32946 字节，SHA-256 `C9CB217F29B059D6EE072F3E61DE7D84B7468C8EBF82F6D40695B15FBCA2B946`；`定时活动.py` 13629 字节，SHA-256 `CC29EF5AE6F2E07F5F4B1F1F175AB24AD2F8922AED22DE3253370B05BB6ED439`。
- 备份文件校验：`便捷传送.py.bak-20260803-pet-recycle` 30338 字节，SHA-256 `1C5AF046605D4A675141B27955243E46343F73F1CD2CCF1922E9AB62B417B751`；`定时活动.py.bak-20260803-pet-recycle` 13652 字节，SHA-256 `65E645028DB43095FF50C78CD1C32949D80F1EC0D3353B93D0A13F68FBA1FA95`。
- 验证：静态契约测试 `.diagnostics\test_pet_recycle_contract.ps1` 通过；使用 IronPython 2.7 编译检查两个运行脚本通过；使用模拟宠物包对象完成回收运行冒烟测试（白名单、保护标记、金币、格子封包）通过。
- 未修改 `Scripts888`、客户端或 APK；服务端重启/重新加载脚本后生效，尚未进行在线道具实测。

## 2026-08-04 - 修复定时活动周切换脚本报错

- 根因：实际运行的 `定时活动.py` 在 `OnWeekChange` 中使用了未声明的 `ResetVariable`，同时引用了 `Defines.py` 中缺失的 `GV_PLAYER_LIUYIPAOKUARMOUR` 和 `GV_PLAYER_JINGJIARMOUR`，导致截图中的 `NameError`。
- 修改文件：
  - `D:\Debug\4月18日更新\Server\Scripts\Ser\定时活动.py`
  - `D:\Debug\4月18日更新\Server\Scripts\Defines.py`
- 修复内容：补充周跑船/周竞技场重置列表；补充六一跑酷衣服和竞技场衣服变量定义（键值 341、347）；统一周/月判断分支缩进，避免脚本重新加载时出现缩进解析错误。
- 覆盖前备份：
  - `D:\Debug\4月18日更新\Server\Scripts\Ser\定时活动.py.bak-20260804-week-reset`
  - `D:\Debug\4月18日更新\Server\Scripts\Defines.py.bak-20260804-week-reset`
  - `D:\相聚假人\Source\CHANGELOG.md.bak-20260804-week-reset`
- 修改后校验：`定时活动.py` 13753 字节，SHA-256 `11661CB0128547D3C5D0307C507DB49E2BE530022748089CB9B5793D8FEA97F4`；`Defines.py` 8067 字节，SHA-256 `0DD295DF274A3A3B6269CD3143248E2B148E719C7D4B6E15C4998CA8068B3A14`。
- 验证：`.diagnostics\test_week_change_reset.ps1` 先失败后通过；IronPython 编译检查通过；`OnWeekChange` 运行冒烟测试通过。
- 需重启或重新加载服务端脚本后生效；未修改客户端、APK 或 `Scripts888`。
# 更新日志

## 2026-08-07 - 恢复源码标准 Server.exe 直接启动
- 按 `Server\\Server.csproj` 的 Debug 配置重新编译，使用源码内嵌的 `Server.exe.licenses`、Costura 依赖和 `D:\\相聚\\.tools\\devexpress-23.2` 引用；未使用自定义启动器或 `ServerCore.exe`。
- 标准产物已覆盖 `D:\\Debug\\4月18日更新\\Server\\Server.exe`、`Server.exe.config`、`Server.pdb`，保留覆盖前备份：`Server.exe.bak-20260807-source-standard`、`Server.exe.config.bak-20260807-source-standard`、`Server.pdb.bak-20260807-source-standard`。
- 验证：直接启动部署后的 `Server.exe`，窗口标题为“Z3服务端”，进程保持运行且 `Responding=True`；程序集包含 `Server.exe.licenses`、`costura.license.dll.compressed` 和 26 个 DevExpress 内嵌资源。

## 2026-08-07 - Android pig companion pickup and war pet tab

- Root cause: `CompanionInfo.Sorting` returned only `_Sorting`, so `Companion_Pig` did not reach the existing mobile pickup configuration or server `bSort` flow; the mobile war-pet handler had the two visibility values reversed.
- Changed: `Library/SystemModels/CompanionInfo.cs` now treats only null-safe `MonsterImage.Companion_Pig` as implicitly sorting-capable; `Mir3.Mobile/Client/Scenes/Views/CompanionDialog.cs` now hides `CompanionBackGround` and shows `WarPetBackGround` on the war-pet tab.
- Backups: `Library/SystemModels/CompanionInfo.cs.bak-20260807-pig-pickup-warpet`, `Mir3.Mobile/Client/Scenes/Views/CompanionDialog.cs.bak-20260807-pig-pickup-warpet`, and `CHANGELOG.md.bak-20260807-pig-pickup-warpet` were byte-for-byte verified before edits.
- Evidence: `powershell -NoProfile -ExecutionPolicy Bypass -File .\.diagnostics\test_mobile_pig_companion_contract.ps1` failed red with the pig and war-pet contract failures, then passed green; `dotnet build .\Library\Library.csproj -c Release --no-restore` could not run because `Library` is a shared project with no `.csproj`; the equivalent active build was `dotnet build .\Mir3.Droid\Mir3.Droid.csproj -c Release --no-restore -p:AndroidSdkDirectory='C:\Users\chen\AppData\Local\Android\Sdk'` from `D:\Mir3AndroidSource`, exiting 0 with 0 warnings and 0 errors and producing `Mir3.Droid\bin\Release\net8.0-android\com.xj.Mir3.Droid-Signed.apk`.
- 父级契约测试：PASS。
- Android 全量重建：在 `D:\Mir3AndroidSource` 运行 `dotnet build .\Mir3.Droid\Mir3.Droid.csproj -c Release --no-restore -t:Rebuild -m:1 -nr:false -p:UseSharedCompilation=false -p:BuildInParallel=false -p:AndroidSdkDirectory=C:\Users\chen\AppData\Local\Android\Sdk`；成功，保留 24 个既有警告、0 个错误，耗时 `00:02:58.42`。
- APK 已部署至 `D:\Debug\4月18日更新\Android\com.xj.Mir3.Droid-Signed.apk`：65,127,752 字节，SHA-256 `782F06D27DAB25801D2755B9723BB6E95597BF9C958BD3AB745A31D135FCB027`；覆盖前备份为同路径加 `.bak-20260807-pig-pickup-warpet`，SHA-256 `9CDB22ED465F7BD1328B5F5974BF7A3659D8AA953A844BC9856C708AEDBFD2D0`；APK v1/v2/v3 签名均为 true，v4 为 false。
- `ServerLibrary` Debug 构建成功（0 警告、0 错误）；Server Debug 标准构建成功，含 1 个既有 MSB3277 冲突警告，输出 `D:\相聚假人\Source\.build-check\pig-companion-server\Server.exe`；资源检查为 207 个 manifest resources，包含 `Server.exe.licenses`、Costura license 和 26 个 DevExpress resources。
- `Server.exe` 已部署至 `D:\Debug\4月18日更新\Server\Server.exe`：83,101,696 字节，SHA-256 `5E236462F810816693F285FE8376327FDE16AF529709FA910FFB7CDF3B41F82D`；备份 `.bak-20260807-pig-pickup-warpet` 的 SHA-256 为 `5FF327C1DEC50FC5EDC198519D0FCE98B293573AD6FAF5D4EF7FA28B8F722005`。
- `Server.pdb` 已同路径部署：1,705,472 字节，SHA-256 `F1C94E5B489D310D998914462C39032BB4E2ACC6EA77516F938CB8D33D67842B`；备份 SHA-256 为 `AEA8C3B61A87FC22EA2A4381D70434AA256E374CB6D89D9D0A531E5663805275`。既有 `Server.exe.config` 与构建输出哈希相同，未覆盖。
- 构建 APK 内嵌 `Mir3.ini` 仍为 `IPAddress=114.132.90.203`、`Port=7100`。
- Limitation: device UI behavior still needs manual confirmation.
- Sol-review 更正：根因是 `CompanionDialog.ConfigButton` 仍走失效的桌面 `AutoPick.TabButton.InvokeMouseClick()` 路径；本次 Luna 修正让 `CompanionDialog.ConfigButton` 与 `AutoPickButton.Tap` 共同复用移动端 `BigPatchDialog.ShowAutoPick()`，保留原有页面可见性和按钮索引更新。BigPatch 只读备份：`Mir3.Mobile\Client\Scenes\Views\BigPatch\BigPatchDialog.cs.bak-20260807-pig-pickup-warpet`；合同测试 `.diagnostics\test_mobile_pig_companion_contract.ps1`：PASS。
- Luna 增量构建证据：在 `D:\Mir3AndroidSource` 按 Release 命令退出 `0`，`0` 警告、`0` 错误；APK `D:\Mir3AndroidSource\Mir3.Droid\bin\Release\net8.0-android\com.xj.Mir3.Droid-Signed.apk` 为 `65,127,752` 字节，SHA-256 `DA5DC7B67D1BB8F8E00B9B9A4F6BA72C7A1DAFA8CD735A87CB36ABBA2FA8E5B8`。
- 本次仅完成增量构建；完整 `Rebuild`、重新部署及真机手测仍待主任务执行，本次未部署 APK 或重新构建/部署 `Server.exe`。
- 主任务新鲜全量重建：在 `D:\Mir3AndroidSource` 运行 `dotnet build .\Mir3.Droid\Mir3.Droid.csproj -c Release --no-restore -m:1 -nr:false -p:UseSharedCompilation=false -p:BuildInParallel=false -p:AndroidSdkDirectory=C:\Users\chen\AppData\Local\Android\Sdk -t:Rebuild`；退出 `0`，保留 `24` 个既有警告、`0` 个错误，耗时 `00:02:57.87`。
- 最终修正 APK：`D:\Mir3AndroidSource\Mir3.Droid\bin\Release\net8.0-android\com.xj.Mir3.Droid-Signed.apk`；`65,127,752` 字节；SHA-256 `274B47DF9E6AA45CA89C71C8FB1A97D7ABDB7B8C54A5B5E9CB571D3446363EF5`。
- 签名校验：v1/v2/v3 均为 `true`，v4 为 `false`，SourceStamp 为 `false`，signer 数量为 `1`。
- 已部署至 `D:\Debug\4月18日更新\Android\com.xj.Mir3.Droid-Signed.apk`，SHA-256 同为 `274B47DF9E6AA45CA89C71C8FB1A97D7ABDB7B8C54A5B5E9CB571D3446363EF5`。
- 紧邻的中间部署 APK 已备份至 `D:\Debug\4月18日更新\Android\com.xj.Mir3.Droid-Signed.apk.bak-20260807-pig-pickup-warpet-showautopick`，SHA-256 `782F06D27DAB25801D2755B9723BB6E95597BF9C958BD3AB745A31D135FCB027`。
- 原始功能前 APK 备份仍为 `D:\Debug\4月18日更新\Android\com.xj.Mir3.Droid-Signed.apk.bak-20260807-pig-pickup-warpet`，SHA-256 `9CDB22ED465F7BD1328B5F5974BF7A3659D8AA953A844BC9856C708AEDBFD2D0`。
- 最终修正未重建/重新部署 `Server.exe`：共享 Sorting 源码在已接受的构建/部署后未再变化。
- 剩余验证仅为真机/界面交互。

## 2026-08-08 - PC 宠物拾取设置与战宠标签修正

- 根因：活跃 PC 项目 `145Client/145Client.csproj` 中的 `WarPetButton` handler 误沿用了 CompanionButton 的可见性赋值；共享 `CompanionInfo.Sorting` 的 Pig-only/null-safe 修正已存在，本次保持不变。
- 修改：仅将 PC `WarPetButton` 改为隐藏 `CompanionBackGround`、显示 `WarPetBackGround`；保留 PC `ConfigButton -> AutoPick.TabButton.InvokeMouseClick()` 路径和 `DXTabControl` 结构，不引入 `ShowAutoPick`。
- 文件与备份：`D:\相聚假人\Source\145Client\Scenes\Views\CompanionDialog.cs`；精确变更前备份 `D:\相聚假人\Source\145Client\Scenes\Views\CompanionDialog.cs.bak-20260808-pc-pig-warpet`（字节一致，SHA-256 `658977A73C427448C31141D15ABD04F4F5EDEC61F619F3A8BEDE14C2BA1C4892`）；新增合同测试 `D:\相聚假人\Source\.diagnostics\test_pc_pig_companion_contract.ps1`。
- RED/GREEN：合同测试命令 `powershell.exe -NoProfile -ExecutionPolicy Bypass -File D:\相聚假人\Source\.diagnostics\test_pc_pig_companion_contract.ps1` 在修正前退出 `1`，唯一失败为反转的 WarPet handler；修正后退出 `0`，输出 `PASS: PC pig companion contract is satisfied.`。
- 隔离构建：`145Client` Release Rebuild 退出 `0`，1 个既有 `CS0649` 警告、0 个错误；产物 `D:\相聚假人\Source\.build-check\pc-pig-companion\Mir3.exe`，3,934,208 字节，SHA-256 `A1105FEBC0D0AA7824513642FAB531F115D83DF0EFCEE0C53924485D46A14021`。
- PC 构建与部署仍由主任务负责；本次未部署或覆盖 `D:\Debug\4月18日更新\Client`。
- 父任务最终 Release Rebuild：在 `D:\相聚假人\Source` 运行 `& 'C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\MSBuild\Current\Bin\MSBuild.exe' '.\145Client\145Client.csproj' /t:Rebuild /p:Configuration=Release /p:Platform=AnyCPU /p:OutputPath='D:\相聚假人\Source\.build-check\pc-pig-companion-parent\' /p:RestorePackages=false /m:1 /nr:false /v:minimal`；退出 `0`，保留 1 个既有 `CS0649` 警告、0 个错误。
- 父任务最终构建文件：`D:\相聚假人\Source\.build-check\pc-pig-companion-parent\Mir3.exe`，3,934,208 字节，SHA-256 `EC623DD8765FC810031BFB93618CFD8339A81BB94E61B7D3F9614013DE02ECA6`；已覆盖部署至 `D:\Debug\4月18日更新\Client\Mir3.exe`，大小和 SHA-256 完全相同。
- 覆盖前部署文件备份：`D:\Debug\4月18日更新\Client\Mir3.exe.bak-20260808-pc-pig-warpet`，4,136,448 字节，SHA-256 `6DF9C11FD56FDF591D05BB47D9828E74A1409FA4CB2695F596409B48FA6105CA`。
- 父任务独立复跑 `.diagnostics\test_pc_pig_companion_contract.ps1`：PASS。
- 剩余验证仅为 PC 游戏内人工验证：猪宠物背包出现拾取设置并打开原 PC 自动拾取页；战斗宠标签显示正确。

## 2026-08-08 - PC 145／韩版双游戏界面

- 设计与实施文档：`docs\superpowers\specs\2026-08-08-pc-dual-game-interface-design.md`、`docs\superpowers\plans\2026-08-08-pc-dual-game-interface.md`。
- 登录界面新增互斥的“145界面／韩版界面”选择；配置键为 `Mir3.ini` 的 `[Graphics] GameInterface`，合法值为 `145`、`Korean`，缺失或未知值回退到 `145`，选择后使用原 `ConfigReader.Save()` 保存。
- `LoadScene.CreateGame()` 在创建游戏场景前规范化并锁定选择；韩版必需资源缺失时回退到 145，避免构造半套界面或黑屏。每次进入游戏只构造一套主界面，不支持游戏内热切换。
- 韩版 1024×768 布局复用现有自带素材：`GameInter/50` 底部 HUD、`52/54/58` 动态 HP/MP/经验条、`460/465/470/475/480/485` 六项右侧菜单；聊天、快捷栏、背包、角色窗口和小地图继续复用已核验的现有 UI1 素材与业务逻辑。按用户确认未添加“英雄装备／英雄技能”两项。
- 韩版快捷栏定位为相对主面板 `Y + 216`，1024×768 下为 Y=616；HP/MP 标签与动态条对齐，未绑定准确位置的经验、负重和地图坐标标签在韩版主面板中隐藏。145 原布局分支保持不变。
- 修改文件：`145Client\Envir\Config.cs`、`145Client\Scenes\LoginScene.cs`、`145Client\Scenes\LoadScene.cs`、`145Client\Scenes\GameScene.cs`、`145Client\Scenes\Views\MainPanel.cs`、`145Client\145Client.csproj`；新增 `145Client\Scenes\Views\GameInterfaceTheme.cs`、`145Client\Scenes\Views\MainPanel.Korean.cs`、`docs\ui\pc-korean-interface-assets.md`。未修改服务端或安卓端；`Library\ConfigReader.cs` 已恢复为原文件，SHA-256 `DCEEC8453C1710520F2F3B0DE244D35816BA3DF29A118F3C53CE468A2CF70536`。
- 原源码备份使用后缀 `.bak-20260808-pc-dual-ui-195942104`；更新日志覆盖前备份为 `CHANGELOG.md.bak-20260808-pc-dual-ui`，SHA-256 `100AA5745D9B05CBBF83117D788006F0FCE604D24C0C9E661AFFF671B4C29A98`。
- 主任务新鲜 Release Rebuild：`MSBuild.exe .\145Client\145Client.csproj /t:Rebuild /p:Configuration=Release /p:Platform=AnyCPU /p:OutputPath=D:\相聚假人\Source\.build-check\pc-dual-ui-parent-20260808-2110\ /p:RestorePackages=false /m:1 /nr:false /v:minimal`；编译成功，0 个错误，仅保留 1 个既有 `CS0649` 警告。
- 主任务验证：PC 双界面源码合同通过；独立临时 ini 的 `GameInterface=Korean` 保存/重新读取往返通过；未向配置写入派生属性。
- 最终构建及部署文件：`D:\Debug\4月18日更新\Client\Mir3.exe`，3,942,912 字节，SHA-256 `C63AE26A36DE6069AD10FD1749B1C967E84E70BB54A95592A0330B0781B54F43`，与隔离构建文件哈希一致。
- 覆盖前客户端备份：`D:\Debug\4月18日更新\Client\Mir3.exe.bak-20260808-pc-dual-ui`，3,934,208 字节，SHA-256 `EC623DD8765FC810031BFB93618CFD8339A81BB94E61B7D3F9614013DE02ECA6`；同时备份未改动的 `Mir3.ini` 为 `Mir3.ini.bak-20260808-pc-dual-ui`，SHA-256 `0CAD32A83762F1BC0DA7D1DA3B4CB72909D0ABB78D469FBC3DC0176EEDF47EFA`。
- 部署后的 `Mir3.ini` 已保存选择 `GameInterface=Korean`，当前 SHA-256 `41D2BE8EF9A6D28AEA0983A097000A49396167686DBDD3667528F0FBC5E69F76`；与备份逐行比较仅新增这一行，IP、端口和其他配置未变化，因此保留该选择而未回滚配置。
- 未生成或覆盖新的 `.Zl` 资源包。剩余验证为用户在真实服务器中分别选择两种界面登录，检查 1024×768 视觉、按钮命中、HP/MP/经验变化、退出并重新进入；当前没有宣称已完成真实运行时像素级验收。

## 2026-08-08 - PC 韩版界面聊天、底部信息与按钮修正

- 根因：韩版仍无条件构造 145 的 `UI1/1101` 聊天框；`MainPanel.Korean.cs` 仅绘制 `GameInter/50` 底板，中央职业、等级和攻防数据未绑定，底部按钮使用了推测的大范围点击区。
- 修改：韩版聊天改用自带 `GameInter2/3500`、`3501` 与 `Interface/150` 组合，保留原聊天输入、频道、滚动和收缩逻辑；底部补齐 `GameInter/60~66` 标签并绑定职业、等级、DC、AC、MAC；九个按钮按素材矩形分别命中，最右 `GameInter/120` 对应商城。145 界面分支保持不变。
- 按用户反馈，小地图已经正常，本次未修改小地图；“英雄装备／英雄技能”仍不添加。当前数据模型没有 FP/CP 字段，因此这两个素材槽保持空白，没有伪造数值。
- 源码：`145Client\Scenes\Views\MainPanel.Korean.cs`、`MainPanel.cs`、`ChatDialog.cs`、`ChatDialog.Korean.cs`、`ChatTextBox.cs`、`145Client\Scenes\GameScene.cs`、`145Client\Scenes\Views\GameInterfaceTheme.cs`、`145Client\145Client.csproj`、`docs\ui\pc-korean-interface-assets.md`。
- 覆盖前备份：`D:\Debug\4月18日更新\Client\Mir3.exe.bak-20260808-235312-pc-korean-chat-hud`，SHA-256 `C63AE26A36DE6069AD10FD1749B1C967E84E70BB54A95592A0330B0781B54F43`；`D:\相聚假人\Source\CHANGELOG.md.bak-20260808-235312-pc-korean-chat-hud`，SHA-256 `02A04547BB90C82F5B09CD4C5FACB006A719416E9F4544D91298D083DB96D364`。
- 验证：韩版 HUD／聊天合同与 PC 双界面源码合同均输出 GREEN；Release Rebuild 退出码 0、0 错误，仅保留既有 `BigPatchConfig.cs` 的 `CS0649` 警告。
- 构建产物：`D:\相聚假人\Source\.build-check\pc-dual-ui-final-20260808-2354\Mir3.exe`，3,947,008 字节，SHA-256 `86D1487CA5BBE64A34DF88435AD9A8BD2F7B58C9170C82E2266D2D4774FE544E`。
- `D:\Debug\4月18日更新\Client\Mir3.ini` 不覆盖、不改写，继续保留 `GameInterface=Korean`；真实 Direct3D 界面外观和点击仍需用户在游戏中手动验收。

## 2026-08-09 - PC 韩版原版聊天、经验条、底部按钮与主菜单修正

- 根因：韩版分支仍使用临时组合的 `GameInter2` 聊天背景、368 高主面板及错误的 `GameInter/58` 经验条；底部按钮索引和动作与原版韩版界面不一致，主菜单也没有独立窗口。
- 最小修正：韩版主面板恢复为 `GameInter/50` 的 1024×68 布局，经验条改用 `GameInter/51` 外框与 `GameInter/56` 横向填充；底部依次接入角色、包裹、魔法、任务、好友/邮件、物品快捷栏、行会、主菜单和商城动作。
- 韩版聊天改为使用 `GameInter.ZL` 的 3500～3578 系列素材并保留现有消息、过滤、输入、链接和滚动业务逻辑；主菜单仅保留“环境设置、队伍信息、师徒信息、玛法排行榜、宠物状态、结束游戏”六项，不显示“英雄装备／英雄技能”。
- 修改文件：`145Client\Scenes\Views\MainPanel.Korean.cs`、`145Client\Scenes\Views\ChatDialog.Korean.cs`、`145Client\Scenes\Views\ChatTextBox.cs`、`145Client\Scenes\GameScene.cs`、`145Client\Scenes\Views\GameInterfaceTheme.cs`、`docs\ui\pc-korean-interface-assets.md`。145 界面、小地图、服务端、移动端和 `.ZL` 资源未修改。
- 六个源码/文档原文件均已创建 `.bak-20260809-pc-korean-original-port-*` 同目录备份并校验 SHA-256。
- 覆盖前部署备份：`D:\Debug\4月18日更新\Client\Mir3.exe.bak-20260809-1048-pc-korean-original-chat-menu`，SHA-256 `86D1487CA5BBE64A34DF88435AD9A8BD2F7B58C9170C82E2266D2D4774FE544E`；更新日志备份：`CHANGELOG.md.bak-20260809-1048-pc-korean-original-chat-menu`，SHA-256 `BDFA7EB853F6CF5385CB6ADC791A387D20F006A77963D377D8DF3A6457ED81A2`。
- 主任务独立验证：`pc-korean-original-ui-contract.ps1`、`korean-core-hud-contract.ps1`、`pc-dual-ui-contract.ps1` 均输出 GREEN；Release Rebuild 0 错误，仅保留 1 个既有 `CS0649` 警告。
- 主任务构建产物：`D:\相聚假人\Source\.build-check\pc-korean-original-port-parent-20260809-104430\Mir3.exe`，3,950,080 字节，SHA-256 `C31891574F2EEA729DE68A59A8B13C7633326160EFC620EBD900FE8DD727DD39`。
- `D:\Debug\4月18日更新\Client\Mir3.ini` 不覆盖、不改写，部署前 SHA-256 `41D2BE8EF9A6D28AEA0983A097000A49396167686DBDD3667528F0FBC5E69F76`。剩余验证为真实 Direct3D 中检查聊天外观、经验条变化、九个按钮和六项主菜单点击。

## 2026-08-09 - PC 韩版聊天四级缩放、透明背景与经验悬停提示

- 聊天框底部三角按钮改为唯一的大小控制入口，循环顺序为：最大 268 → 218 → 168 → 118 → 隐藏；四个可见状态使用朝下素材 `GameInter/3552`，隐藏后使用朝上素材 `GameInter/3542`，再次点击恢复最大状态。
- 顶部重复的放大/缩小按钮在韩版中隐藏并禁用；聊天框隐藏时保留底部输入栏。右侧滚动条及可见行数随四级高度同步调整，分别为 13、9、6、3 行。
- 韩版聊天标题、内容和输入背景约为 30% 不透明，文字、标签、边框、按钮和滚动条不整体变淡。
- 韩版细长经验条取消鼠标穿透；经验百分比不常驻显示，仅在鼠标指向经验条时提示精确格式 `[经验] xx%`。`GameInter/51` 外框、`GameInter/56` 填充和 145 界面原提示保持不变。
- 修改源码：`145Client\Scenes\Views\ChatDialog.Korean.cs`、`145Client\Scenes\Views\ChatTextBox.cs`、`145Client\Scenes\Views\MainPanel.Korean.cs`、`145Client\Scenes\GameScene.cs`。
- 新增设计与计划：`docs\superpowers\specs\2026-08-09-pc-korean-chat-resize-cycle-design.md`、`docs\superpowers\plans\2026-08-09-pc-korean-chat-resize-cycle.md`、`docs\superpowers\specs\2026-08-09-pc-korean-experience-hover-design.md`、`docs\superpowers\plans\2026-08-09-pc-korean-experience-hover.md`。
- 源码备份：`ChatDialog.Korean.cs.bak-20260809-pc-korean-chat-resize-cycle-01`、`ChatTextBox.cs.bak-20260809-pc-korean-chat-resize-cycle-01`、`MainPanel.Korean.cs.bak-20260809-pc-korean-experience-hover-01`、`GameScene.cs.bak-20260809-pc-korean-experience-hover-01`，均在修改前完成 SHA-256 校验。
- 覆盖前部署备份：`D:\Debug\4月18日更新\Client\Mir3.exe.bak-20260809-1232-pc-korean-chat-resize-exp-hover`，SHA-256 `C31891574F2EEA729DE68A59A8B13C7633326160EFC620EBD900FE8DD727DD39`；更新日志备份：`CHANGELOG.md.bak-20260809-1232-pc-korean-chat-resize-exp-hover`，SHA-256 `0DB0FD8FA7CE40E8CBF5BEA3C837B48F91BE5E5D610807560049EA8AAD0B85E1`。
- 主任务独立验证：经验悬停、聊天四级缩放、韩版原始 UI、韩版 HUD/聊天和 PC 双界面五项契约全部 GREEN；Release Rebuild 为 0 错误，仅保留 1 个既有 `CS0649` 警告。
- 主任务构建产物：`D:\相聚假人\Source\.build-check\pc-korean-chat-exp-parent-20260809-123025\Mir3.exe`，3,951,104 字节，SHA-256 `57C3B3C828B0D5CDB4C67CF0E74B1E80DA19CA47E69FB15C5C6DD08E8C176DAD`。
- `D:\Debug\4月18日更新\Client\Mir3.ini` 不覆盖、不改写，部署前 SHA-256 `41D2BE8EF9A6D28AEA0983A097000A49396167686DBDD3667528F0FBC5E69F76`。剩余验证为真实 Direct3D 中逐级点击、隐藏恢复、滚动条联动以及经验悬停提示。

## 2026-08-09 - PC 韩版聊天单层背景、透明度与原版滚动条修正

- 根因：韩版聊天内部仍额外绘制 `GameInter/3502` 底栏，与独立输入栏 `GameInter/3503` 形成双层阴影；原 `0.3F` 实际是 30% 不透明而不是约 30% 透明；通用 `DXVScrollBar` 的固定位置条偏移和轨道扣减也未匹配韩版原始滚动条几何。
- 最小修正：删除可见的内部 `GameInter/3502` 底栏，只保留唯一 `GameInter/3503` 输入栏；聊天标题、内容和输入背景改为 `0.7F` 不透明度（约 30% 透明），文字、按钮和滚动条不整体变淡。
- 韩版滚动条继续复用 `DXVScrollBar`，使用原版素材 `GameInter/3561`、`3562`、`3560`，位置条横向偏移 2、轨道扣减 40、上箭头位置 `(0,2)`；通用控件新增的两个参数默认仍为横向偏移 0、轨道扣减 50，其他现有调用方行为不变。
- 四级聊天高度仍为 268、218、168、118，消息背景、文字区和滚动条延伸到输入栏上方，可见行数同步为 14、11、7、4；隐藏后恢复最大状态的既有循环保持不变。
- 修改源码：`145Client\Controls\DXVScrollBar.cs`、`145Client\Scenes\Views\ChatDialog.Korean.cs`、`145Client\Scenes\Views\ChatTextBox.cs`。145 界面、经验悬停、小地图、服务端、移动端和 `.ZL` 资源未修改。
- 源码备份：`DXVScrollBar.cs.bak-20260809-pc-korean-chat-single-layer-scroll-01`，SHA-256 `F847767EBFF455C7AD621D64F2EC195510E2028F2631D3A51A3237D741B2AFAC`；`ChatDialog.Korean.cs.bak-20260809-pc-korean-chat-single-layer-scroll-01`，SHA-256 `4FC811B7B16BABC84E00BC92B65ED6265A30F4DD2D9CD96BC039E9F5B7F063B0`；`ChatTextBox.cs.bak-20260809-pc-korean-chat-single-layer-scroll-01`，SHA-256 `7D174F5F955922F3E8351EA6600CDB7A572F18AB4100068999E777E2D00DBC41`。
- 覆盖前部署备份：`D:\Debug\4月18日更新\Client\Mir3.exe.bak-20260809-1328-pc-korean-chat-single-layer-scroll`，SHA-256 `57C3B3C828B0D5CDB4C67CF0E74B1E80DA19CA47E69FB15C5C6DD08E8C176DAD`；更新日志备份：`CHANGELOG.md.bak-20260809-1328-pc-korean-chat-single-layer-scroll`，SHA-256 `167BBDB07B0768318A0B6D8F9A481B2207C79391B0EC484004992489618BBF2F`。
- 主任务独立验证：单层聊天/透明度/滚动条、经验悬停、聊天四级缩放、韩版原始 UI、韩版 HUD/聊天、PC 双界面六项契约全部 GREEN；Release Rebuild 0 错误，仅保留 1 个既有 `BigPatchConfig.cs` 的 `CS0649` 警告。
- 最终构建及部署文件：`D:\Debug\4月18日更新\Client\Mir3.exe`，3,951,104 字节，SHA-256 `57387A172D20BA01350E4E5C091FFA44A30486A65C903D3EA6CD679C899299C6`，与主任务构建产物一致。
- `D:\Debug\4月18日更新\Client\Mir3.ini` 未覆盖、未改写，SHA-256 仍为 `41D2BE8EF9A6D28AEA0983A097000A49396167686DBDD3667528F0FBC5E69F76`，配置仍为 `GameInterface=Korean`。剩余验证为真实 Direct3D 中确认双层阴影消失、背景透明度观感以及右侧滚动条拖动/轨道点击。

## 2026-08-09 - PC 韩版聊天卡死、透明度与输入栏双层绘制修正

- 根因：`DXButton.DrawMirTexture()` 在素材索引无有效图像时直接访问空对象，渲染循环会连续抛出 `NullReferenceException`，表现为点击聊天区域后客户端卡死；韩版聊天黑色内容背景未启用纹理绘制；韩版输入栏同时绘制 `DXWindow` 标准窗口层和 `GameInter/3503`，形成双层阴影。
- 最小修正：`DXButton.cs` 对空图像提前返回；`DXWindow.cs` 增加默认开启的 `DrawWindowTexture` 开关；仅韩版 `ChatTextBox` 关闭标准窗口层并保留 `GameInter/3503`；`KoreanTextBackground` 启用纹理绘制并保留 `Opacity=0.7F`（约 30% 透明）。
- 修改源码：`145Client\Controls\DXButton.cs`、`145Client\Controls\DXWindow.cs`、`145Client\Scenes\Views\ChatDialog.Korean.cs`、`145Client\Scenes\Views\ChatTextBox.cs`。滚动条索引和几何、四级高度循环、经验悬停、145 界面、小地图、服务端、移动端、`.ZL` 资源均未修改。
- 源码备份：四个修改文件同目录下的 `.bak-20260809-pc-korean-chat-freeze-opacity-single-input-01`，备份 SHA-256 分别为 `44577F7BAFC6C81C17D09B6020B07B139A4570DC6C8F856E20140FF65CD3ADE6`、`F1C83B78416DFA19D56F33336B9E128CBCDD6461CA67C5132000F4F2B2DA2F17`、`22E5FB63B7B471B5FEEE1B1DD2F45E8B06E801F642B01E024B4E1EED1BB973FB`、`347324CE09387F48EFFC9A5DDFC6F7DF1D7A730C4A8436CE2D43D901F0E20CF2`。
- 覆盖前部署备份：`D:\Debug\4月18日更新\Client\Mir3.exe.bak-20260809-pc-korean-chat-freeze-opacity-single-input-01`，SHA-256 `57387A172D20BA01350E4E5C091FFA44A30486A65C903D3EA6CD679C899299C6`；更新日志备份：`CHANGELOG.md.bak-20260809-pc-korean-chat-freeze-opacity-single-input-01`，SHA-256 `AE11BF237BB307CCF855CEEF73AEC6CD2ED5AA50D4BE37F82CBFFCA19D29BA1B`。
- 主任务独立验证：卡死/透明度/单输入层、单层滚动条、经验悬停、聊天四级缩放、韩版原始 UI、韩版 HUD/聊天、PC 双界面七项契约全部 GREEN；Release Rebuild 0 错误，仅保留 1 个既有 `BigPatchConfig.cs` 的 `CS0649` 警告。
- 最终构建及部署文件：`D:\Debug\4月18日更新\Client\Mir3.exe`，3,951,104 字节，SHA-256 `38F3FCCAE689F7FAB490D782BB45FEFFB119D4ECAB02648C7E7F4F982845B9DA`，与主任务独立构建产物一致。
- `D:\Debug\4月18日更新\Client\Mir3.ini` 未覆盖、未改写，部署前 SHA-256 `41D2BE8EF9A6D28AEA0983A097000A49396167686DBDD3667528F0FBC5E69F76`，配置仍为 `GameInterface=Korean`。剩余验证为真实 Direct3D 中确认点击不再卡死、输入栏阴影消失及背景透明度观感。

## 2026-08-09 - PC 韩版聊天复合素材去重与控制按钮修正（待实机确认）

- 根因：`GameInter/3500` 的 380×48 复合素材完整绘制了底部控制区域，同时又叠加独立滚动条；`GameInter/3503` 内嵌三角按钮又与独立 3542/3552 按钮错位，形成双按钮和阴影。韩版聊天窗口还保留通用 `DXWindow` 窗口层，关闭按钮未在尺寸变化后重新置顶，悬停提示固定为旧的“切换聊天框”。
- 最小修正：仅韩版 `ChatDialog` 关闭通用窗口层；`GameInter/3500` 固定裁剪为 380×27；内容背景、文字区和滚动条从 Y=27/31/27 开始，四级高度 268/218/168/118 与可见行数 14/11/7/4 保持联动；关闭按钮固定在 `(364,5)` 并置顶。
- 输入栏继续使用 `GameInter/3503` 的 380×25 素材；独立三角按钮固定在 `(356,8)` 覆盖素材内嵌位置。可见状态使用 3552，隐藏状态使用 3542；提示按状态显示“缩小聊天框”“隐藏聊天框”“展开聊天框”。
- 修改源码：`145Client\Scenes\Views\ChatDialog.Korean.cs`、`145Client\Scenes\Views\ChatTextBox.cs`。145 界面、共享控件、`.ZL` 资源、服务端和移动端未修改。
- 源码备份沿用本轮首次修改前已创建的 `ChatDialog.Korean.cs.bak-20260809-pc-korean-chat-composite-control-dedup-01`（SHA-256 `EBA056B9FACD6960956661E62417D67FAD7BA6779B79B3312EEA563BBC5E53DE`）和 `ChatTextBox.cs.bak-20260809-pc-korean-chat-composite-control-dedup-01`（SHA-256 `2DDDEBA29F71989F12FF6F0351EC616F0D913598F264745704FBDBC2A0315080`）。按用户要求，在正式实机确认前未重复创建部署文件或更新日志备份。
- 主任务独立验证：复合素材去重、卡死/透明度/单输入层、单层滚动条、经验悬停、聊天四级缩放、韩版原始 UI、韩版 HUD/聊天、PC 双界面共 8 项契约全部 GREEN；Release Rebuild 退出码 0、0 错误，仅保留 1 条既有 `BigPatchConfig.cs` 的 `CS0649` 警告。
- 构建及部署文件：`D:\Debug\4月18日更新\Client\Mir3.exe`，3,951,104 字节，SHA-256 `E177615228EDD9F54A948EBAFCACAC95C1A2782394FABD5C83CE871D8DA2F3C3`，与主任务独立构建产物一致。
- `D:\Debug\4月18日更新\Client\Mir3.ini` 未覆盖、未改写；部署后 SHA-256 `0DE33D1C34D105745B82E13B506D4C1984F9CE8D1A91DB01EFA1E5155C9320AA`，当前配置为 `GameInterface=145`。本项仍待用户在登录界面选择“韩版界面”后进行 Direct3D 实测，确认顶部/底部无双层绘制、仅一个三角按钮、关闭按钮完整可见且三个状态提示正确。

## 2026-08-09 20:15 - PC 韩版聊天、怪物信息、主菜单与模式栏综合修正（待实机确认）

- 聊天输入栏：`GameInter/3503` 按完整 `380×38` 素材加载并向上裁剪 8 像素，独立三角按钮移到 `(356,0)` 置顶；最左侧聊天控件悬停提示改为“切换聊天”。聊天记录背景、文字面板和右侧滚动条统一在输入栏上方预留 2 像素，避免记录区域压住输入框；四级高度、透明度、行数和切换逻辑保持不变。
- 怪物信息窗：改为 200 像素宽的深色金框可拖动窗口，显示等级、名称、动态红色血条、物防/魔防/物攻/魔攻和八项抗性。血条不再依赖 `AfterDraw + ProgUse/662`，由 `RefreshHealth()`、`RefreshStats()` 直接按当前 HP/MaxHP 更新子控件宽度；窗口外框与血条轨道均保留金色细框。
- 怪物信息交互：鼠标移出怪物后保留最后一次有效信息；对象被移除或按 ESC 时仍沿用既有清理逻辑。详情默认展开为 `200×160`，三角朝上并提示“隐藏怪物信息”；收起后为 `200×52`，三角朝下并提示“显示怪物信息”。首次显示居中，拖动后切换怪物不重置位置。
- 韩版主菜单：增加标题“主菜单”，菜单统一为“环境设置、队伍信息、爆率查询、玛法排行榜、宠物状态、辅助设置、结束游戏”；移除师徒信息入口。七个按钮文字统一使用标题金色 `Color.FromArgb(198,166,99)`，功能分别复用现有 `RateQueryBox`、`BigPatchBox` 等窗口。
- 韩版底部 IP 行：恢复显示人物攻击模式和宠物控制模式，两个标签使用青色并继续复用既有 `AttackModeChanged()`、`PetModeChanged()` 数据更新逻辑。
- 修改源码：`145Client\Scenes\Views\ChatTextBox.cs`、`145Client\Scenes\Views\ChatDialog.Korean.cs`、`145Client\Scenes\Views\MonsterDialog.cs`、`145Client\Scenes\Views\MainPanel.Korean.cs`、`145Client\Scenes\GameScene.cs`。未修改 `.ZL` 资源、145 界面、服务端或移动端。
- 按用户“正式修好前不用重复备份”的要求，本轮未创建新的源码、部署文件或更新日志备份；既有备份未覆盖。
- 主任务独立验证：专项综合契约、聊天复合去重、卡死/透明度/单输入层、单层滚动条、经验悬停、聊天四级缩放、韩版原始 UI、韩版 HUD/聊天和 PC 双界面共 9 项契约全部 GREEN。
- Release AnyCPU Rebuild：0 错误，仅保留 1 条既有 `BigPatchConfig.cs` 的 `CS0649` 警告。最终构建及部署文件：`D:\Debug\4月18日更新\Client\Mir3.exe`，3,949,568 字节，SHA-256 `E12744EEB576E7553F3154E54EECFF26D355F937962479625AD832BD5759350B`。
- `D:\Debug\4月18日更新\Client\Mir3.ini` 未覆盖、未改写，部署前后 SHA-256 均为 `A0B9690070FF803DF89357A5DFF1B38CBBE9E5B44C8449AA0537DDB1F1270A50`，当前为 `GameInterface=Korean`。剩余验证为真实 Direct3D 中确认动态血条、外框、三角折叠、拖动、鼠标移出保留、菜单颜色和聊天输入栏边界。

## 2026-08-11 - PC 韩版按职业分类的列表式技能窗口

- 仅韩版界面启用列表式魔法技能窗口；145 界面的 `UI1/1620` 技能树、分类按钮、技能坐标和操作路径保持原样。
- 韩版在角色对象创建后按 `MapObject.User.Class` 筛选当前职业全部技能，再按实际非空 `MagicSchool` 动态生成顶部分类按钮；按钮数量不固定，也不能切换查看其他职业。
- `WeaponSkills`、`Neutral`、`Passive`、`Unconditional` 合并为武技分类；其他学校按现有枚举顺序显示。分类内按 `NeedLevel1`、技能名称排序。
- 未学习技能继续显示对应图标，并以红色显示要求等级；已学习技能显示技能等级和熟练度进度，继续复用原悬停说明、选中和快捷键封包逻辑。新增真实右侧滚动条和鼠标滚轮支持。
- 生命周期修正：`MagicDialog` 先构建韩版空壳，`GameScene.User` 完成赋值后同步调用 `MagicBox.InitializeForUser()`，避免后续技能封包直接索引空 `Magics` 字典；韩版技能点击不会访问145专用的底部说明标签。
- 修改源码：`145Client\Scenes\Views\MagicDialog.cs`、`145Client\Scenes\GameScene.cs`、`145Client\145Client.csproj`；新增 `145Client\Scenes\Views\MagicDialog.Korean.cs`、`.diagnostics\test_pc_korean_magic_list_contract.ps1`。设计与计划：`docs\superpowers\specs\2026-08-10-pc-korean-magic-list-design.md`、`docs\superpowers\plans\2026-08-11-pc-korean-magic-list.md`。
- 未修改安卓、服务端、网络封包、数据库或 `.ZL` 资源；本次复用当前 `UI1`、`Interface`、`MagicIcon145` 索引，避免把 `D:\Video\英雄客户端\Data` 中未验证索引兼容性的资源覆盖到145界面。
- 主任务独立验证：`test_pc_equipment_compare_contract.ps1`、`test_pc_korean_magic_list_contract.ps1`、`test_pc_pig_companion_contract.ps1` 共3项全部退出 `0`；专项输出 `PASS: PC Korean magic list contract is satisfied.`。
- Release/AnyCPU Rebuild：`MSBuild.exe D:\相聚假人\Source\145Client\145Client.csproj /t:Rebuild /p:Configuration=Release /p:Platform=AnyCPU /m /v:minimal`；退出 `0`、0个错误，仅保留1条既有 `BigPatchConfig.cs CS0649` 警告。
- 构建与部署文件：`D:\Client\Mir3.exe` 和 `D:\Debug\4月18日更新\Client\Mir3.exe` 均为 `3,962,368` 字节，SHA-256 `EFF961409405BE995E98D43CADAE46BAF01C4EA65BBA70C45AC00BB9B7CE1E45`。
- 覆盖前唯一最终备份：`D:\Debug\4月18日更新\Client\Mir3.exe.bak-20260811-013818-pc-korean-magic-list`，SHA-256 `3A2A471E7138044380D52AAE70107DBA5CE7BA4D55E56DA6EDB2318C66BC6451`。
- `D:\Debug\4月18日更新\Client\Mir3.ini` 未覆盖、未改写，部署前后 SHA-256 均为 `3568911A16D3207A2E927584F85F678651F971573EEAC7F9B7ADBB846B581C67`。
- 启动冒烟：实际完整客户端目录的旧版和部署后新版均连续运行10秒未自行退出，再由测试流程关闭；单独从 `D:\Client` 运行因该目录资源环境不完整而访问冲突退出，因此不作为运行时验收依据。
- 剩余验证为游戏内人工检查：韩版各职业动态分类、未学习/已学习状态、滚动条与快捷键；145技能树视觉及操作不变。

## 2026-09-09 - 宠物包自动分解 GM Index 白名单（静态验证完成，待在线验收）

- 新增运行配置 `D:\Debug\4月18日更新\Server\Scripts\Npc\其他\自动分解配置.py`，仅允许其中的 `ItemInfo.Index` 进入现有宠物包自动分解流程；修改 `D:\Debug\4月18日更新\Server\Scripts\Npc\其他\便捷传送.py`，配置缺失、语法错误或类型错误时空名单拒绝并只在模块加载时记录一次日志。
- 从活动 `D:\Debug\4月18日更新\Server\Database\System.db` 的只读隔离副本生成并安装初始快照，共 `857` 条，重复 Index `0`；源库 SHA-256 `46FE189E57842D408EFC5FA974E1DE66A5EB36F0AAE62A5D49109064FE1E8C90`，两次生成哈希均为 `453358703CD7BE2335BFAB07208CB349649F2A0ADF7C301FC2F1AB377CCC6A49`，运行配置 SHA-256 `56C351258D8D343A51100E04FEBF089E6975D62374A928FFAE617E2DB930023F`。
- 两个运行脚本最终 SHA-256：`自动分解配置.py` `56C351258D8D343A51100E04FEBF089E6975D62374A928FFAE617E2DB930023F`；`便捷传送.py` `F3E1C57424BE6DCB9A01F085CE3B126FFFD2139FD57B4D91FB9937F92C77CFF0`。修改前备份：`便捷传送.py.bak-20260909-195258-auto-fragment-allowlist`，SHA-256 `E893BBCB05C4585FB7D4ABE9E47A7A0ACA5B5F1F74A32651305B2177871B7539`。
- 通过 `test_pet_fragment_contract.ps1`、`test_pet_fragment_schedule_contract.ps1`、`test_pet_recycle_contract.ps1`、`test_auto_fragment_allowlist_snapshot.ps1`、`PetFragmentSmoke`；`自动分解配置.py` 通过 Python 2.7 原始 `compile()`，`便捷传送.py` 的 CPython 2.7 原始 `compile()` 在修改前备份与当前文件均于既有第 18 行中文模块导入报 `SyntaxError`，其自动分解函数由 IronPython smoke 验证。未执行脚本重载、服务端重启、部署或在线允许/禁止物品验收。
