# PC 客户端道士 Buff 观察闪退修复设计

## 问题与证据

观察假人道士华佗、唐EV 时，Windows Application 日志在 2026-08-22 22:31:53、22:32:33、22:34:01 记录 `System.ArgumentOutOfRangeException`，调用栈均落在 `Client.Scenes.Views.LeftBuffBox.Process()`。当前代码按简体中文将属性文本长度乘二，再执行 `PadLeft(20 - len)`；当翻译缺失或属性名较长时，补齐宽度为负数并终止客户端。

服务器当前启用 `PhysicalResistanceSwitch=True`。道士神圣战甲术产生的 `PhysicalResistance` 是已确认可形成负宽度的输入：未翻译时长度计算为 `36`，目标宽度为 `-16`。九种护身符购买修复没有修改客户端，但会让道士获得施法材料，从而更容易触发既有客户端缺陷。

## 方案

仅修改 `145Client/Scenes/Views/LeftBuffBox.cs` 的显示补齐逻辑：保留现有语言长度计算、Buff 类型、文本内容和倒计时，只把传给 `PadLeft` 的宽度限制为不小于零。长文本不再补空格，短文本继续保持原来的 20 列对齐。

不修改道士技能、Buff 属性、护身符购买、语言数据库、服务器配置或观察者协议。不会通过关闭 `PhysicalResistanceSwitch` 或禁止道士施放 Buff 来绕过问题。

## 验证

新增聚焦 PowerShell 契约，先在旧实现上证明负宽度输入会失败，并要求生产代码对补齐宽度执行非负保护；契约 RED 后再修改生产源码并验证 GREEN。

随后运行现有 PC 客户端相关契约，并以 Debug/AnyCPU 重建 `145Client` 到隔离目录。静态契约和构建不能替代 Direct3D 运行时验收；最终仍需人工依次观察华佗、唐EV及一个非道士假人，确认不再出现新的 `LeftBuffBox.Process` 崩溃事件，同时确认 Buff 文本和倒计时正常显示。

## 范围与边界

允许修改：

- `145Client/Scenes/Views/LeftBuffBox.cs`
- 新增一个 `.diagnostics` 聚焦契约
- `CHANGELOG.md` 中相邻的道士 AI 条目

禁止修改或执行：

- `Server/BotManager*.cs`、数据库、NPC、语言资源和部署配置
- 自动替换正在使用的客户端、启动或停止客户端/服务器
- Release 构建、备份、Git、PR 或部署

## 验收标准

- `PhysicalResistance` 等长度超过 10 个简中字符单位的文本不会向 `PadLeft` 传入负数。
- 四种现有道士 Buff 的筛选、属性内容、倒计时和短文本对齐保持不变。
- 聚焦契约先 RED 后 GREEN，既有 PC 契约无新增失败。
- Debug/AnyCPU 构建 0 错误，产物只位于隔离目录并报告 SHA-256。
- 人工观察验收前不宣称客户端闪退已在线修复。
