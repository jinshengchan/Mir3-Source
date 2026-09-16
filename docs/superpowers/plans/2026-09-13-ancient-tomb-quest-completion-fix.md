# 古墓三字符任务完成脚本修复 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 让任务 172、173、174 完成后按顺序保存三个不重复的墓碑字符编号，使古墓 1 层入口能够正确显示并校验字符。

**Architecture:** 保留现有 `OnCompleteQuest`/`GumuQuest` 事件入口，只恢复其实际逻辑并补上事件模块导入。字符使用客户端已经支持的字符串编号 `"1"`–`"24"` 写入对应 `UserQuest.ExtraInfo`；前置字符缺失或无效时不生成后续字符，已有值不覆盖。

**Tech Stack:** IronPython-compatible Python scripts, `PlayerEvent`, PowerShell diagnostics, CPython standard-library test harness.

## Global Constraints

- 只修改 `D:\Debug\4月18日更新\Server\Scripts` 下的 `Player\事件触发\完成任务.py` 和 `Player\事件触发\__init__.py`。
- `Scripts888` 不属于本次目标；不修改客户端、服务器 C# 源码、数据库或 `Server.ini`。
- 不复制文件到服务器、不重启服务端、不提交 Git；实机进入古墓属于后续人工验收。
- 保持任务编号 172、173、174、字符范围 1–24、顺序校验和已有 `ExtraInfo` 值不变。

---

## 文件结构

- Create: `D:\相聚假人\Source\.diagnostics\test_ancient_tomb_quest_completion_contract.py` — 在本地用模块桩加载目标脚本，验证事件注册、字符生成、顺序依赖和幂等行为；不部署到服务器。
- Modify: `D:\Debug\4月18日更新\Server\Scripts\Player\事件触发\完成任务.py` — 恢复任务完成事件和古墓字符生成逻辑。
- Modify: `D:\Debug\4月18日更新\Server\Scripts\Player\事件触发\__init__.py` — 导入任务完成模块，使服务器加载监听器。
- Read-only verification: `D:\相聚假人\Source\ServerLibrary\Models\Player\Quest.cs`、`D:\相聚假人\Source\ServerLibrary\Envir\SConnection.cs`、客户端 `NPCDialog.cs` — 已确认数据契约，本计划不修改。

## Task 1: 建立会失败的回归契约

**Files:**
- Create: `D:\相聚假人\Source\.diagnostics\test_ancient_tomb_quest_completion_contract.py`
- Read: `D:\Debug\4月18日更新\Server\Scripts\Player\事件触发\完成任务.py`
- Read: `D:\Debug\4月18日更新\Server\Scripts\Player\事件触发\__init__.py`

**Interfaces:**
- Consumes: 目标脚本的 `OnCompleteQuest(args)`、`PlayerEvent.add_listener(name, function)`、`Sender.GetUserQuestByQuestIndex(index)`。
- Produces: 可重复运行的本地契约，断言监听器已注册，并验证 172/173/174 的 `ExtraInfo` 行为。

- [x] **Step 1: 写入失败契约测试**

创建以下文件：

```python
from pathlib import Path
import re
import runpy
import sys
import types


TARGET = Path(r"D:\Debug\4月18日更新\Server\Scripts\Player\事件触发\完成任务.py")
EVENT_INIT = Path(r"D:\Debug\4月18日更新\Server\Scripts\Player\事件触发\__init__.py")

assert TARGET.is_file(), "missing completion script"
assert EVENT_INIT.is_file(), "missing event package initializer"

source = TARGET.read_text(encoding="utf-8")
compile(source, str(TARGET), "exec")
event_init = EVENT_INIT.read_text(encoding="utf-8")
assert re.search(r"(?m)^\s*import Player\.事件触发\.完成任务\s*$", event_init), "completion module is not imported"
assert "say(" not in source, "undefined say() call remains"

listeners = {}
player_event = types.ModuleType("PlayerEvent")


def add_listener(name, function):
    listeners[name] = function


player_event.add_listener = add_listener
sys.modules["PlayerEvent"] = player_event

for module_name in ("Globals", "Defines", "Library"):
    sys.modules[module_name] = types.ModuleType(module_name)

clr = types.ModuleType("clr")
clr.AddReference = lambda name: None
sys.modules["clr"] = clr

server = types.ModuleType("Server")
server.__path__ = []
envir = types.ModuleType("Server.Envir")
envir.__path__ = []
senvir = types.ModuleType("Server.Envir.SEnvir")
server.Envir = envir
envir.SEnvir = senvir
sys.modules["Server"] = server
sys.modules["Server.Envir"] = envir
sys.modules["Server.Envir.SEnvir"] = senvir

namespace = runpy.run_path(str(TARGET))
handler = namespace.get("OnCompleteQuest")
assert callable(handler), "OnCompleteQuest is not active"
assert listeners.get("OnCompleteQuest") is handler, "OnCompleteQuest listener is not registered"


class QuestInfo:
    def __init__(self, index):
        self.Index = index


class UserQuest:
    def __init__(self, index, extra_info=""):
        self.QuestInfo = QuestInfo(index)
        self.ExtraInfo = extra_info


class Sender:
    def __init__(self, quests):
        self.quests = quests

    def GetUserQuestByQuestIndex(self, index):
        for quest in self.quests:
            if quest.QuestInfo.Index == index:
                return quest
        return None


def complete(sender, quest):
    handler((sender, quest))


valid_values = {str(index) for index in range(1, 25)}
quests = [UserQuest(172), UserQuest(173), UserQuest(174)]
sender = Sender(quests)
for quest in quests:
    complete(sender, quest)

characters = [quest.ExtraInfo for quest in quests]
assert all(character in valid_values for character in characters), characters
assert len(set(characters)) == 3, characters

first_value = quests[0].ExtraInfo
complete(sender, quests[0])
assert quests[0].ExtraInfo == first_value, "existing character was overwritten"

missing_previous = UserQuest(173)
missing_sender = Sender([missing_previous])
complete(missing_sender, missing_previous)
assert missing_previous.ExtraInfo == "", "character generated without its predecessor"

invalid_previous = [UserQuest(172, "not-a-character"), UserQuest(173)]
invalid_sender = Sender(invalid_previous)
complete(invalid_sender, invalid_previous[1])
assert invalid_previous[1].ExtraInfo == "", "character generated from an invalid predecessor"

existing = [UserQuest(172, "7"), UserQuest(173), UserQuest(174)]
existing_sender = Sender(existing)
complete(existing_sender, existing[0])
complete(existing_sender, existing[1])
complete(existing_sender, existing[2])
assert existing[0].ExtraInfo == "7", existing[0].ExtraInfo
assert existing[1].ExtraInfo in valid_values and existing[1].ExtraInfo != "7"
assert existing[2].ExtraInfo in valid_values
assert existing[2].ExtraInfo not in ("7", existing[1].ExtraInfo)

print("ancient tomb quest completion contract passed")
```

- [x] **Step 2: 运行测试，确认当前版本确实失败**

运行：

```powershell
python 'D:\相聚假人\Source\.diagnostics\test_ancient_tomb_quest_completion_contract.py'
```

预期：失败，原因应落在“completion module is not imported”或 `OnCompleteQuest` 未激活；此失败证明测试能捕获当前缺陷。

## Task 2: 恢复事件加载和最小字符生成逻辑

**Files:**
- Modify: `D:\Debug\4月18日更新\Server\Scripts\Player\事件触发\完成任务.py`
- Modify: `D:\Debug\4月18日更新\Server\Scripts\Player\事件触发\__init__.py`
- Test: `D:\相聚假人\Source\.diagnostics\test_ancient_tomb_quest_completion_contract.py`

**Interfaces:**
- Consumes: `args[0]` 作为 `Sender`、`args[1]` 作为 `UserQuest`；`UserQuest.QuestInfo.Index`；`UserQuest.ExtraInfo`。
- Produces: `GumuQuest(Sender, UserQuest, QuestInfo) -> None`；对 172、173、174 写入合法的字符串编号；`PlayerEvent` 中唯一的 `OnCompleteQuest` 监听器。

- [x] **Step 1: 用现有风格恢复完成任务处理函数**

将 `完成任务.py` 中原来被注释的处理块替换为以下逻辑，保留现有导入和任务编号：

```python
CHAR_MIN = 1
CHAR_MAX = 24


def GetQuestChar(Sender, QuestIndex):
    Quest = Sender.GetUserQuestByQuestIndex(QuestIndex)
    if Quest is None or not Quest.ExtraInfo:
        return None

    try:
        Char = int(Quest.ExtraInfo)
    except (TypeError, ValueError):
        return None

    if Char < CHAR_MIN or Char > CHAR_MAX:
        return None
    return Char


def GetRandomChar(Used):
    Available = [value for value in range(CHAR_MIN, CHAR_MAX + 1) if value not in Used]
    return str(random.choice(Available))


def OnCompleteQuest(args):
    Sender = args[0]
    UserQuest = args[1]
    QuestInfo = UserQuest.QuestInfo

    if QuestInfo.Index in GUMU_QUESTS:
        GumuQuest(Sender, UserQuest, QuestInfo)


def GumuQuest(Sender, UserQuest, QuestInfo):
    if UserQuest.ExtraInfo:
        return

    Used = []
    if QuestInfo.Index == 173:
        firstChar = GetQuestChar(Sender, 172)
        if firstChar is None:
            return
        Used.append(firstChar)
    elif QuestInfo.Index == 174:
        firstChar = GetQuestChar(Sender, 172)
        secondChar = GetQuestChar(Sender, 173)
        if firstChar is None or secondChar is None or firstChar == secondChar:
            return
        Used.extend([firstChar, secondChar])

    UserQuest.ExtraInfo = GetRandomChar(Used)


PlayerEvent.add_listener("OnCompleteQuest", OnCompleteQuest)
```

- [x] **Step 2: 把任务完成模块加入事件包加载链**

在 `Player\事件触发\__init__.py` 的现有导入列表中加入一行：

```python
import Player.事件触发.完成任务
```

不要改变其他事件模块的顺序或内容。

- [x] **Step 3: 运行回归契约，确认行为通过**

运行：

```powershell
python 'D:\相聚假人\Source\.diagnostics\test_ancient_tomb_quest_completion_contract.py'
```

预期：输出 `ancient tomb quest completion contract passed` 并以退出码 0 结束。

## Task 3: 做语法、静态范围和交付前检查

**Files:**
- Read: `D:\Debug\4月18日更新\Server\Scripts\Player\事件触发\完成任务.py`
- Read: `D:\Debug\4月18日更新\Server\Scripts\Player\事件触发\__init__.py`
- Read: `D:\相聚假人\Source\.diagnostics\test_ancient_tomb_quest_completion_contract.py`

**Interfaces:**
- Consumes: Task 2 的两个脚本和回归契约。
- Produces: 静态可验证结果，以及明确的“未部署、未重启、未改 Scripts888”边界报告。

- [x] **Step 1: 编译两个目标脚本而不生成 `__pycache__`**

运行：

```powershell
@'
from pathlib import Path

paths = [
    Path(r"D:\Debug\4月18日更新\Server\Scripts\Player\事件触发\完成任务.py"),
    Path(r"D:\Debug\4月18日更新\Server\Scripts\Player\事件触发\__init__.py"),
]
for path in paths:
    compile(path.read_text(encoding="utf-8"), str(path), "exec")
    print("compiled: {}".format(path))
'@ | python -
```

预期：两个文件均输出 `compiled`，目标目录不新增编译缓存。

- [x] **Step 2: 检查有效监听器、字符范围和未定义调用**

运行：

```powershell
$ErrorActionPreference = 'Stop'
$completion = 'D:\Debug\4月18日更新\Server\Scripts\Player\事件触发\完成任务.py'
$eventInit = 'D:\Debug\4月18日更新\Server\Scripts\Player\事件触发\__init__.py'
$completionText = Get-Content -LiteralPath $completion -Raw -Encoding UTF8
$eventInitText = Get-Content -LiteralPath $eventInit -Raw -Encoding UTF8
if (([regex]::Matches($completionText, '(?m)^\s*PlayerEvent\.add_listener\("OnCompleteQuest"')).Count -ne 1) { throw 'expected one active OnCompleteQuest registration' }
if ($completionText -match '(?m)^\s*#.*OnCompleteQuest|say\s*\(') { throw 'commented-only handler or undefined say() remains' }
if ($completionText -notmatch 'CHAR_MIN\s*=\s*1' -or $completionText -notmatch 'CHAR_MAX\s*=\s*24') { throw 'character range contract is missing' }
if ($completionText -notmatch 'UserQuest\.ExtraInfo\s*=\s*GetRandomChar') { throw 'ExtraInfo assignment is missing' }
if ($eventInitText -notmatch '(?m)^\s*import Player\.事件触发\.完成任务\s*$') { throw 'completion module import is missing' }
Write-Output 'ancient tomb static contract passed'
```

- [x] **Step 3: 检查目标范围和未部署状态**

运行：

```powershell
rg -n 'OnCompleteQuest|GUMU_QUESTS|ExtraInfo|Player\.事件触发\.完成任务' 'D:\Debug\4月18日更新\Server\Scripts\Player\事件触发\完成任务.py' 'D:\Debug\4月18日更新\Server\Scripts\Player\事件触发\__init__.py'
Get-FileHash -LiteralPath 'D:\Debug\4月18日更新\Server\Scripts\Player\事件触发\完成任务.py','D:\Debug\4月18日更新\Server\Scripts\Player\事件触发\__init__.py' -Algorithm SHA256
```

确认输出只涉及两个目标脚本和本地诊断文件；不执行复制、上传、进程重启或数据库写入。最终报告区分静态测试通过与服务器实机验收尚未执行。
