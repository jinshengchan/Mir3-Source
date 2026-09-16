# PC 韩版聊天卡死、背景透明度与输入框单层修正设计

## 目标

在不改变 145 界面、聊天业务、四级缩放和韩版滚动条素材的前提下，修复三个已复现问题：聊天内容背景没有按约 30% 透明绘制、聊天区域连续点击后出现逐帧异常导致客户端假死、输入框出现额外窗框阴影。

## 已确认根因

1. `KoreanTextBackground` 使用普通 `DXControl`，只设置了 `BackColour` 和 `Opacity = 0.7F`，但普通控件默认 `DrawTexture = false`，因此黑色内容背景根本没有绘制。
2. 客户端错误日志在同一秒连续记录 `Client.Controls.DXButton.DrawMirTexture()` 的 `NullReferenceException`。`MirLibrary.CreateImage()` 在索引或纹理不可用时允许返回 `null`，而 `DXButton.DrawMirTexture()` 直接读取 `image.Image`；渲染循环每帧重试，形成异常风暴和界面假死。
3. 韩版 `ChatTextBox` 继承 `DXWindow`，窗口仍执行标准 `DrawWindow()` 路径，同时又绘制 `GameInter/3503` 输入素材。韩版输入框需要显式关闭标准窗口层，只保留一套素材层。

## 最小实现

- 在 `KoreanTextBackground` 初始化中设置 `DrawTexture = true`，保持 `BackColour = Color.Black` 与 `Opacity = 0.7F`，即约 30% 透明。
- 为 `DXWindow` 增加默认开启的单一布尔开关，用于控制是否执行标准窗口纹理绘制；默认值必须保持现有窗口行为。仅韩版 `ChatTextBox` 关闭该开关，继续保留 `GameInter/3503` 背景、聊天模式按钮、文本输入和三角按钮。
- 在 `DXButton.DrawMirTexture()` 中读取 `MirLibrary.CreateImage()` 后，使用与 `DXImageControl.DrawMirTexture()` 相同的 `image?.Image == null` 防护并直接返回。正常图片路径和全部按钮交互保持不变。

## 保持不变

- 韩版滚动条仍使用 `GameInter/3561`、`3562`、`3560`。
- 四级高度仍为 268、218、168、118，并继续按最大、逐级缩小、隐藏、恢复最大循环。
- 不改变聊天频道过滤、输入发送、物品链接、滚轮、拖动和轨道点击业务。
- 不改变 145 界面、经验悬停、小地图、服务端、移动端、`Mir3.ini` 和 `.ZL` 资源。
- 不增加日志刷屏、重试器、备用素材或新的 UI 配置项。

## 验证

- 新增一个聚焦源码契约，修改前必须因以下三项缺失而 RED：内容背景没有 `DrawTexture = true`；韩版输入框没有禁用标准窗口层；`DXButton` 没有空图片防护。
- 修改后聚焦契约必须 GREEN，并重跑现有六项韩版聊天、经验和双界面契约。
- 使用 VS 2022 Build Tools 对 `145Client\145Client.csproj` 执行 Release Rebuild，要求 0 错误；既有 `BigPatchConfig.cs` 的 `CS0649` 警告允许保留。
- 部署前确认目标 `D:\Debug\4月18日更新\Client\Mir3.exe` 未运行，备份被覆盖文件及 `CHANGELOG.md`，部署后核对构建产物和目标文件 SHA-256 完全一致，`Mir3.ini` SHA-256 不变。
- 自动验证不能替代真实 Direct3D 验收；最终人工检查内容背景深浅、输入框阴影、滚动条连续点击与拖动。
