# 八大暗影接入活动管理员 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 让八大暗影仅通过活动管理员（NPC 332）进入，同时不影响两个脚本的既有功能。

**Architecture:** 活动管理员继续作为 NPC 332 的唯一 `OnClick` 监听器，在其主菜单增加入口并把菜单 80/81/82 转交给八大暗影模块。八大暗影保留副本地图事件，但移除独立 NPC 5656 监听器，避免两个 `OnClick` 互相覆盖。

**Tech Stack:** IronPython 2.7 服务端脚本、PowerShell 静态契约检查。

## Global Constraints

- 只修改 `活动管理员.py`、`八大暗影.py` 和 `CHANGELOG.md`，并在覆盖前逐文件备份。
- 活动管理员的 NPC 编号固定为 332；不改它已有菜单的行为。
- 八大暗影使用菜单 80（打开）、81（开始）、82（刷新），不使用活动管理员已占用的菜单号。
- 八大暗影不再注册 NPC 5656；地图 387 的 `OnEnter`、`OnLeave`、`OnCreate` 事件保留。
- 不改副本收费 500/50 元宝、地图、怪物、奖励、每日次数和并发限制。
- 所有改动追加到 `D:\相聚假人\Source\CHANGELOG.md`；不生成客户端产物。

---

### Task 1: 建立失败契约检查

**Files:**
- Create: `D:\相聚假人\Source\.diagnostics\test_bada_shadow_activity_manager.py`
- Test: `D:\相聚假人\Source\.diagnostics\test_bada_shadow_activity_manager.py`

**Interfaces:**
- Consumes: `活动管理员.py` 的 `OnClick(args)` 与 `八大暗影.py` 的 `OnClick(args)`。
- Produces: 对入口菜单、菜单转交、监听器和地图事件的可重复静态校验。

- [ ] **Step 1: 写入失败测试**

```python
# -*- coding: utf-8 -*-
import sys
import types

calls = []
def install(name, module):
    sys.modules[name] = module

class Reference(object):
    def __getitem__(self, item):
        return lambda: None

clr = types.ModuleType('clr')
clr.Reference = Reference()
clr.AddReference = lambda name: None
install('clr', clr)
system = types.ModuleType('System')
system.Object = object
install('System', system)
for name in ('Globals', 'Library', 'Defines', 'Server', 'Utils', 'Utils.TimeUtil'):
    install(name, types.ModuleType(name))
npc_event = types.ModuleType('NpcEvent')
npc_event.add_listener = lambda *args: None
install('NpcEvent', npc_event)
npc = types.ModuleType('Npc')
boss = types.ModuleType('Npc.BOSS副本')
shadow = types.ModuleType('Npc.BOSS副本.八大暗影')
shadow.OnClick = lambda args: calls.append(args) or {'menu': args[2]}
npc.BOSS副本 = boss
boss.八大暗影 = shadow
install('Npc', npc)
install('Npc.BOSS副本', boss)
install('Npc.BOSS副本.八大暗影', shadow)

scope = {}
path = r'D:\Debug\4月18日更新\Server\Scripts\Npc\活动管理员.py'
exec(compile(open(path, 'rb').read(), path, 'exec'), scope)
for incoming, expected in ((80, 1), (81, 11), (82, 12)):
    result = scope['OnClick']((object(), object(), incoming))
    assert result == {'menu': expected}
assert [entry[2] for entry in calls] == [1, 11, 12]
assert '[八大暗影:80]' in scope['OnClick']((object(), object(), 0))['Say']
print 'bada shadow activity-manager behavior passed'
```

- [ ] **Step 2: 运行测试，确认当前失败**

Run: `C:\Python27\python.exe D:\相聚假人\Source\.diagnostics\test_bada_shadow_activity_manager.py`

Expected: FAIL，提示活动管理员尚未包含八大暗影入口或转交逻辑。

### Task 2: 将入口接入活动管理员

**Files:**
- Modify: `D:\Debug\4月18日更新\Server\Scripts\Npc\活动管理员.py`
- Modify: `D:\Debug\4月18日更新\Server\Scripts\Npc\BOSS副本\八大暗影.py`
- Backup: 同目录下两个文件各自的 `.bak-20260806-bada-shadow-activity-manager`
- Test: `.diagnostics\test_bada_shadow_activity_manager.py`

**Interfaces:**
- Consumes: `BadaShadow.OnClick((Self, Sender, Menu))`。
- Produces: NPC 332 唯一处理点击，菜单 80/81/82 分别转交为八大暗影的展示/开始/刷新调用。

- [ ] **Step 1: 备份两个待修改脚本**

```powershell
Copy-Item -LiteralPath 'D:\Debug\4月18日更新\Server\Scripts\Npc\活动管理员.py' -Destination 'D:\Debug\4月18日更新\Server\Scripts\Npc\活动管理员.py.bak-20260806-bada-shadow-activity-manager' -ErrorAction Stop
Copy-Item -LiteralPath 'D:\Debug\4月18日更新\Server\Scripts\Npc\BOSS副本\八大暗影.py' -Destination 'D:\Debug\4月18日更新\Server\Scripts\Npc\BOSS副本\八大暗影.py.bak-20260806-bada-shadow-activity-manager' -ErrorAction Stop
```

- [ ] **Step 2: 在活动管理员中写入最小转交逻辑**

在既有导入区增加动态加载，避免 Python 2.7 对中文包名导入语法的不兼容：

```python
BadaShadow = __import__('Npc.BOSS副本.八大暗影', fromlist=['OnClick'])
```

在 `OnClick(args)` 解包 `Self`、`Sender`、`Menu` 后、任何原有 `if (Menu == ...)` 前增加：

```python
	if Menu in (80, 81, 82):
		shadowMenu = 1 if Menu == 80 else (11 if Menu == 81 else 12)
		return BadaShadow.OnClick((Self, Sender, shadowMenu))
```

在主菜单 `say` 中、`[离开:0]` 前增加：

```text
	[八大暗影:80]

```

- [ ] **Step 3: 改写八大暗影的菜单号并移除旧 NPC 监听器**

将脚本内生成按钮的两个字符串替换为：

```python
enter_button = "[开始挑战:81] \r\n\r\n" if enter_available else ""
refresh_button = "[刷新状态:82] 刷新状态信息\r\n\r\n"
```

冷却中的刷新按钮保持原文本和倒计时，仅将菜单号改为 `82`。移除以下独立 NPC 监听器，保留其后所有地图事件注册：

```python
NpcEvent.add_listener(5656, "OnClick", OnClick)
```

- [ ] **Step 4: 运行契约测试，确认通过**

Run: `C:\Python27\python.exe D:\相聚假人\Source\.diagnostics\test_bada_shadow_activity_manager.py`

Expected: PASS，表明入口、转交、菜单号、旧 NPC 解绑及三项地图事件均符合设计。

### Task 3: 语法与更新日志验证

**Files:**
- Modify: `D:\相聚假人\Source\CHANGELOG.md`
- Backup: `D:\相聚假人\Source\CHANGELOG.md.bak-20260806-bada-shadow-activity-manager`
- Test: `.diagnostics\test_bada_shadow_activity_manager.py`

**Interfaces:**
- Consumes: Task 2 已通过的脚本。
- Produces: 可回溯日志和通过的静态/语法验证结果。

- [ ] **Step 1: 对两个脚本运行 IronPython 2.7 语法检查**

Run:

```powershell
& 'C:\Python27\python.exe' -c "import sys; compile(open(sys.argv[1], 'rb').read(), sys.argv[1], 'exec')" 'D:\Debug\4月18日更新\Server\Scripts\Npc\活动管理员.py'
& 'C:\Python27\python.exe' -c "import sys; compile(open(sys.argv[1], 'rb').read(), sys.argv[1], 'exec')" 'D:\Debug\4月18日更新\Server\Scripts\Npc\BOSS副本\八大暗影.py'
```

Expected: 两个命令均返回退出码 0。

- [ ] **Step 2: 备份并更新更新日志**

```powershell
Copy-Item -LiteralPath 'D:\相聚假人\Source\CHANGELOG.md' -Destination 'D:\相聚假人\Source\CHANGELOG.md.bak-20260806-bada-shadow-activity-manager' -ErrorAction Stop
```

在日志顶部新增一条：日期、活动管理员 NPC 332、菜单 80/81/82、取消 5656、保留地图 387 事件、两份脚本备份路径以及契约/语法检查结果。

- [ ] **Step 3: 复跑完整验证**

Run: `C:\Python27\python.exe D:\相聚假人\Source\.diagnostics\test_bada_shadow_activity_manager.py`

Expected: PASS。

- [ ] **Step 4: 手工线上验证**

服务端执行“重新加载脚本”或安全重启后，玩家点击活动管理员：

1. 主菜单显示“八大暗影”。
2. 点击入口显示八大暗影说明与“开始挑战”。
3. 点击开始挑战后仍按现有规则扣 500 元宝并进入地图 387 副本。
4. 原活动管理员菜单仍可正常使用，NPC 5656 不再显示八大暗影入口。
