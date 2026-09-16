# PC 超强骷髅模型与掉落查询文案设计

## 目标

仅修改 PC 桌面客户端 `145Client`：

1. 道士召唤的 `JinSkeleton`（超强骷髅）使用现有可显示的 `WhiteBone` 模型与对应音效。
2. 主菜单和查询窗口标题统一显示“掉落查询”。

## 已确认根因

当前客户端数据库中的“超强骷髅”记录为 `MonsterFlag.JinSkeleton`、`MonsterImage.DiyMonsMon`、`BodyShape=254`。现有客户端解析会将其映射到 `Mon-26.Zl` 的第 4 组，即从索引 4000 开始；实际资源只有 3000 个槽位，因此主体图像请求越界并返回空模型。

旧客户端数据库曾将同一怪物配置为 `MonsterImage.WhiteBone`，该模型路径使用现有 `Mon-6.Zl` 资源并可解析有效帧。

## 方案

### 模型解析

在 `145Client/Models/MonsterObject.cs` 的 `UpdateLibraries()` 中，仅对 `MonsterInfo.Flag == MonsterFlag.JinSkeleton` 覆盖本次客户端对象使用的 `Image`，将其设为 `MonsterImage.WhiteBone`；其他怪物仍使用 `MonsterInfo.Image`。

这项覆盖只影响客户端渲染和既有 `WhiteBone` 音效分支，不修改共享数据库对象，也不改变服务端召唤、属性、AI、伤害或网络协议。

### UI 文案

仅修改两处玩家可见字符串：

- `145Client/Scenes/Views/MainPanel.Korean.cs`：主菜单“爆率查询”改为“掉落查询”。
- `145Client/Scenes/Views/RateQueryDiglog.cs`：窗口标题“暴率查询”改为“掉落查询”。

类名、快捷键、配置项、注释和内部 `RateQuery` 标识保持不变。

## 不在范围内

- 不修改 `ClientSystem.db`、服务端数据库或 `.Zl` 资源。
- 不修改 `Mir3.Mobile`、`Mir3.Mobile000` 或服务端工程。
- 不部署或覆盖现有运行客户端。
- 不重命名类型、配置项、快捷键动作或内部接口。

## 验证

1. 新增一个聚焦诊断契约并先运行至 RED：捕获当前 `JinSkeleton` 未走 `WhiteBone` 解析，以及两处旧 UI 文案。
2. 应用最小生产代码修改后再次运行契约，要求全部 GREEN。
3. 使用 VS 2022 Build Tools 对 `145Client.csproj` 执行 Release/AnyCPU Rebuild，要求退出码为 0；单独记录既有警告。
4. 复核目标文件和 SHA-256，确认没有数据库、资源、服务端、移动端或部署文件变化。

静态契约和构建不能证明 Direct3D 运行效果。仍需人工进游戏验收：召唤超强骷髅后确认站立、移动、攻击、受击、死亡模型与声音，并确认主菜单及查询窗口标题均显示“掉落查询”。

## 成功标准

- `JinSkeleton` 在 PC 客户端稳定使用 `WhiteBone` 模型路径。
- 两处指定玩家可见文案均为“掉落查询”。
- 聚焦契约通过，Release/AnyCPU 构建通过。
- 改动严格限制在获准源码、诊断契约和本设计/计划文档内。
