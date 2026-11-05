# Mir3 Unity 地图读取原型

这个目录是独立原型，基于 `Mir3.Mobile/Client/Scenes/Views/MapControl.cs` 的韩版传奇3（类型5）地图布局。它读取一张 `.map` 的地砖索引与通行标志，在 Unity 2D 场景中绘制最多 40×40 个格子的局部预览。现有客户端和服务端不受影响。

## 在 Unity 中查看

1. 新建 Unity 2D 项目，把本目录的 `Assets/Mir3` 拷入项目 `Assets`。
2. 复制一张韩版传奇3 `.map`，仅把副本的扩展名改成 `.bytes` 后放入 `Assets`。Unity 会将它作为 `TextAsset` 导入；不要改变文件内容。
3. 场景里建一个空对象，添加 `Mir3KoreanMapPreview`，把 `.bytes` 拖到 `Map Bytes`。相机设为正交投影，运行场景。
4. 没有图片资源时以灰色占位地砖显示。要看真实地砖，先将对应资源图片导出为 PNG/Sprite，设置 **Pixels Per Unit = 32、Pivot = Top Left**，再在 `Floor Sprites` 中按地图的 **文件号和从零开始的图片索引**绑定。`BackFile` 等于韩版地图资源号加 200；地图中存储的图片号从零开始。
5. 勾选 `Show Blocked Cells` 可叠加显示阻挡格。通过 `Start X / Start Y` 选择局部区域。

## 当前范围

- 只支持韩版类型5地图，且要求高度为偶数；其他地图类型会明确报错。
- 只绘制地面层；建筑、人物、动画、特效、原 `.lib` 资源解码、网络与 UI 尚未接入。
- 地图图片缺失时的颜色块仅用于核对解析与坐标；不能代表最终画质。
- Unity 编辑器编译、真实资源及手机性能尚未验证；首次接入时应选一张已知类型5地图对照现有客户端逐格核验。

下一步先做资源库图片转换和地面/建筑分层，然后做人物动画与协议适配。不要把约 3GB 资源直接放进 Unity `Resources` 目录。
