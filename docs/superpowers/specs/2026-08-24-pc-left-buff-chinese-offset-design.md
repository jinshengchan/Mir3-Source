# PC 道士 BUFF 中文显示与整体下移设计

## 目标

仅修改 PC 桌面客户端 `145Client` 的左侧道士 BUFF 展示：

1. 将当前显示为 `StrongElement.PhysicalResistance` 的属性改为项目现有中文术语“体质”。
2. 将整组 `LeftBuffBox` 在现有位置基础上向下移动 10 像素。

截图中英文末尾的数字是 BUFF 剩余秒数，不属于属性名称；修正后仍保留倒计时。

## 已确认根因

`LeftBuffBox.Process()` 调用 `Stats.GetShortDisplay(Stat.PhysicalResistance)`。该方法为元素抗性模式拼出 `StrongElement.PhysicalResistance` 并调用字符串本地化，但当前活动 `ClientSystem.db` 的简体中文 `LangClient` 记录中不存在这个键，所以客户端回退显示原始英文。

同一数据库已存在 `Library.Stat.PhysicalResistance = 体质`，因此不需要新增或修改语言数据库。

## 方案

### 中文显示

在 `145Client/Scenes/Views/LeftBuffBox.cs` 的 BUFF 属性循环中，仅当 `pair.Key == Stat.PhysicalResistance` 时使用 `pair.Key.Lang()`；其他属性继续调用现有 `stats.GetShortDisplay(pair.Key)`。

这样只修正左侧 BUFF 面板，不改变通用 `StatEx.GetShortDisplay()` 的其他调用者，也不修改数据库或公共语言规则。现有中文宽度计算、非负 `PadLeft` 保护、四类道士 BUFF、颜色和倒计时保持不变。

### 整体下移

在 `145Client/Scenes/GameScene.cs` 的界面定位逻辑中，将：

```csharp
LeftBuffBox.Location = new Point(0, (Size.Height - LeftBuffBox.Size.Height) / 2);
```

改为：

```csharp
LeftBuffBox.Location = new Point(0, (Size.Height - LeftBuffBox.Size.Height) / 2 + 10);
```

只改变整组控件的 Y 坐标；水平位置、控件尺寸、文字行距及各行相对位置不变。

## 不在范围内

- 不修改 `ClientSystem.db`、语言数据库或 `.Zl` 资源。
- 不修改 `StatEx.GetShortDisplay()`、`Library/Enum.cs`、服务端或移动端。
- 不改变 BUFF 类型筛选、数值、持续时间、行距、颜色或布局尺寸。
- 不部署或覆盖现有运行客户端。

## 验证

1. 扩展现有 `.diagnostics/test_pc_left_buff_box_padding_contract.ps1`，增加以下聚焦断言：
   - `PhysicalResistance` 在 `LeftBuffBox` 中通过枚举本地化显示。
   - 其他属性仍调用 `GetShortDisplay()`。
   - 现有四类 BUFF、倒计时和非负 padding 保护保持不变。
   - `LeftBuffBox` 的整体 Y 坐标只增加 10 像素。
2. 在生产代码修改前运行扩展契约，确认新增行为为 RED。
3. 应用两处最小源码改动后再次运行，确认全部 GREEN。
4. 使用 VS 2022 Build Tools 对 `145Client.csproj` 执行 Release/AnyCPU Rebuild，要求退出码为 0，并记录警告。
5. 复核允许文件及 SHA-256，确认活动客户端、数据库和资源未变化。

静态契约和构建不能证明 Direct3D 实际显示。仍需人工进游戏确认：英文已变为“体质”，剩余秒数正常更新，所有左侧道士 BUFF 整体向下移动 10 像素且没有遮挡或裁切。

## 成功标准

- 左侧 BUFF 面板不再显示 `StrongElement.PhysicalResistance`，而是显示“体质”。
- 倒计时仍紧随对应 BUFF 文本正常更新。
- 整组 `LeftBuffBox` 相对原位置向下移动 10 像素。
- 聚焦契约与 Release/AnyCPU 构建通过。
- 改动仅限获准源码、聚焦契约和本设计/计划文档。
