# PC 左侧道士 BUFF 每行倒计时设计

## 目标

修正 PC 桌面客户端 `145Client` 左侧道士 BUFF 文本：当一个 BUFF 展开为多条可见属性行时，每条属性行都显示该 BUFF 的同一个剩余秒数。

以启用 `PhysicalResistanceSwitch` 的神圣战甲术为例，当前输出是：

```text
物理防御
体质6
```

修正后输出为：

```text
物理防御6
体质6
```

实际显示仍沿用现有 padding 对齐，以上示例省略中间空格。

## 已确认根因

服务端 `ServerLibrary/Models/Player/TaoistMagic.cs` 为神圣战甲术的同一个 `BuffType.Resilience` 依次提供 `Stat.MaxAC` 和 `Stat.PhysicalResistance`。客户端 `LeftBuffBox.Process()` 会把它们分别显示为“物理防御”和“体质”。

当前 `LeftBuffBox.Process()` 在属性 `foreach` 循环结束后才追加一次 `buff.RemainingTime.TotalSeconds`，所以秒数只能跟在该 BUFF 的最后一条可见属性行后面。只读反馈命令稳定复现为：

```text
LINE_1=物理防御
LINE_2=体质6
RED exact symptom reproduced
```

这不是计时同步、padding、控件裁切或服务端 BUFF 数据缺失问题，而是客户端文本拼接位置错误。

## 方案

仅在 `145Client/Scenes/Views/LeftBuffBox.cs` 的四类既有道士 BUFF 分支中调整文本拼接：

1. 保留 `Stat.Duration` 跳过、`GetShortDisplay()`/“体质”本地化、`temp == null` 跳过、中文宽度计算和非负 padding。
2. 每生成一条可见属性文本，就在该行末尾追加 `(int)buff.RemainingTime.TotalSeconds`。
3. 删除属性循环结束后的单次倒计时追加。

推荐的最小生产代码形态是：

```csharp
text += $"\n{temp}{(int)buff.RemainingTime.TotalSeconds}";
```

单属性 BUFF 的视觉结果不变；多属性 BUFF 的每条可见行显示同一个剩余秒数。所有行仍引用同一 `ClientBuffInfo.RemainingTime`，不会创建独立计时器或改变倒计时更新机制。

## 范围

允许修改：

- `145Client/Scenes/Views/LeftBuffBox.cs`
- `.diagnostics/test_pc_left_buff_box_padding_contract.ps1`
- 本设计文档及后续实施计划文档

明确不修改：

- `145Client/Scenes/GameScene.cs` 中已批准的整体下移 10 像素定位
- `145Client/Extentions/StatEx.cs`
- `Library/Enum.cs`
- `ServerLibrary/Models/Player/TaoistMagic.cs` 及所有服务端源码
- 移动端、`ClientSystem.db`、任何 `.Zl` 资源和活动客户端

不改变 BUFF 类型筛选、属性顺序、文字颜色、窗口尺寸、行距、语言规则、数值或持续时间。

## 验证

1. 扩展现有 `.diagnostics/test_pc_left_buff_box_padding_contract.ps1`，新增聚焦断言：倒计时与每条可见属性文本在 `foreach` 内共同拼接，并且不存在循环外单独追加倒计时的旧形态。
2. 在生产代码修改前运行契约，要求新增断言稳定 RED，原有 10 项断言保持通过。
3. 应用一处最小生产改动后重跑，要求全部 GREEN。
4. 保留并继续验证以下既有行为：四类道士 BUFF、“体质”本地化、其他属性的 `GetShortDisplay()`、中文宽度、`PadLeft(Math.Max(0, 20 - len))`、整体下移 10 像素和无异常吞噬。
5. 使用 VS 2022 Build Tools 对 `145Client/145Client.csproj` 执行 Release/AnyCPU Rebuild，要求退出码为 0，并记录警告。
6. 记录获准文件及 `D:\Client\Mir3.exe` 的 SHA-256，并确认活动 `Mir3.exe`、`ClientSystem.db`、受保护源码和全部活动 `.Zl` 资源不变。

静态契约和构建不能证明 Direct3D 实际呈现。仍需人工进游戏确认：物理防御和体质都显示相同且持续更新的剩余秒数，其他道士 BUFF、位置、行距和裁切均正常。

## 成功标准

- 同一个 BUFF 展开的每条可见属性行都显示该 BUFF 的相同剩余秒数。
- 神圣战甲术的“物理防御”和“体质”两行均显示倒计时。
- 单属性道士 BUFF 的显示行为不变。
- 聚焦契约与 Release/AnyCPU 构建通过。
- 改动严格限于获准文件，没有部署或资源变更。

## 执行通道

用户已明确授权通过 Sol Advisor 的用户可见 Luna 任务通道执行，模型为 `gpt-5.6-luna`，推理强度为 `max`。主任务负责完整任务包、监控、实际改动检查、独立复跑验证和最终验收。
