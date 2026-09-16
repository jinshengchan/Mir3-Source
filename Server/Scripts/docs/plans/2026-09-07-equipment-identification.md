# 装备鉴定脚本修正 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 恢复 NPC 215 的稀世装备鉴定和 NPC 216 的鉴定石向下分解，并从现有管理中心提供可用入口。

**Architecture:** 两个独立 IronPython NPC 模块分别承担鉴定和分解。玩家从管理中心进入隐藏 NPC；脚本按背包格子定位具体物品，在操作时重新校验，并先确认产物可以发放再扣除材料。未鉴定装备通过“去掉未鉴定前缀”动态解析当前数据库中的唯一稀世成品，不维护重复的静态装备表。

**Tech Stack:** IronPython NPC 脚本、Mir3 `NpcEvent`/`ServerUtils`/`SEnvir` API、PowerShell 5.1 静态与数据库契约。

## Global Constraints

- 只修改 `D:\Debug\4月18日更新\Server\Scripts`。
- 不修改 `Scripts888`、数据库、C#、构建产物或运行中服务器。
- 不删除两个旧钓鱼商脚本，只停止导入它们，防止重复监听 215/216。
- 鉴定 100% 成功，每次消耗一件未鉴定装备和一颗同等级鉴定石。
- 分解只允许向下一级，比例 1:1。
- NPC 216 直接购买鉴定石的固定成本为：一级 `高级碎片 x1 + 元宝 x50`、二级 `x2 + x100`、三级 `x3 + x150`、四级 `x4 + x200`、五级 `x5 + x250`。
- 产物发放使用当前可用的 `GiveItems` 或 `ItemCheck`、`CanGainItems`、`SEnvir.CreateFreshItem`、`GainItem` API。
- 保留源物品的 `Bound` 和 `Worthless` 标记；任何校验或发放失败均不扣材料。
- 当前目录非 Git 仓库，因此计划中不执行提交。

---

### Task 1: 建立失败契约

**Files:**
- Create: `D:\Debug\4月18日更新\Server\Scripts\Test\test_equipment_identification_contract.ps1`

**Interfaces:**
- Consumes: 当前主脚本树及 `D:\Debug\4月18日更新\Server\Database\System.db`。
- Produces: 一个退出码为 0/1 的 PowerShell 契约，覆盖文件、导入、监听、入口和数据库映射。

- [ ] **Step 1: 写入当前必然失败的文件与绑定契约**

```powershell
$scriptRoot = 'D:\Debug\4月18日更新\Server\Scripts'
$identify = Join-Path $scriptRoot 'Npc\鉴定稀世装备.py'
$exchange = Join-Path $scriptRoot 'Npc\兑换鉴定石.py'
$npcInit = Get-Content -LiteralPath (Join-Path $scriptRoot 'Npc\__init__.py') -Encoding UTF8 -Raw
$panyeInit = Get-Content -LiteralPath (Join-Path $scriptRoot 'Npc\潘夜岛\__init__.py') -Encoding UTF8 -Raw
$manager = Get-Content -LiteralPath (Join-Path $scriptRoot 'Npc\管理中心.py') -Encoding UTF8 -Raw

if (-not (Test-Path -LiteralPath $identify)) { throw '缺少鉴定稀世装备.py' }
if (-not (Test-Path -LiteralPath $exchange)) { throw '缺少兑换鉴定石.py' }
if ($npcInit -notmatch 'import Npc\.鉴定稀世装备') { throw '主入口未导入鉴定模块' }
if ($npcInit -notmatch 'import Npc\.兑换鉴定石') { throw '主入口未导入分解模块' }
if ($panyeInit -match '钓鱼商俊熙|钓鱼商秀贤') { throw '旧脚本仍占用 215/216' }
if ($manager -notmatch 'Menu == 38' -or $manager -notmatch 'GetNPCObject\(215\)') { throw '缺少装备鉴定入口' }
if ($manager -notmatch 'Menu == 39' -or $manager -notmatch 'GetNPCObject\(216\)') { throw '缺少鉴定石分解入口' }
```

- [ ] **Step 2: 加入脚本行为静态契约**

```powershell
$identifyText = Get-Content -LiteralPath $identify -Encoding UTF8 -Raw
$exchangeText = Get-Content -LiteralPath $exchange -Encoding UTF8 -Raw
if ($identifyText -notmatch 'add_listener\(215') { throw 'NPC 215 未监听' }
if ($exchangeText -notmatch 'add_listener\(216') { throw 'NPC 216 未监听' }
if ($identifyText -notmatch 'RequiredAmount' -or $identifyText -notmatch 'startswith\(u?"未鉴定"\)') { throw '鉴定等级或前缀校验缺失' }
if ($identifyText -notmatch 'CanGainItems' -or $identifyText -notmatch 'ItemCheck' -or $identifyText -notmatch 'TakeItem\(source_item,\s*1\)') { throw '鉴定发放/精确扣除契约缺失' }
if ($exchangeText -notmatch 'GiveItems' -or $exchangeText -notmatch 'TakeItem\(source_item,\s*1\)') { throw '分解发放/精确扣除契约缺失' }

$sourceRoot = 'D:\相聚假人\Source'
$packageDlls = Get-ChildItem -LiteralPath (Join-Path $sourceRoot 'packages') -Recurse -File -Filter '*.dll' |
    Where-Object { $_.FullName -match '\\lib\\netstandard2\.0\\' } |
    Group-Object Name |
    ForEach-Object { $_.Group | Select-Object -First 1 }
foreach ($file in $packageDlls) {
    try { [System.Reflection.Assembly]::LoadFrom($file.FullName) | Out-Null } catch {}
}
$library = [System.Reflection.Assembly]::LoadFrom((Join-Path $sourceRoot 'Server\bin\Debug\Library.dll'))
$databaseRoot = 'D:\Debug\4月18日更新\Server\Database\'
$backupRoot = 'D:\Debug\4月18日更新\Server\Backup\'
$session = [Activator]::CreateInstance(
    [MirDB.Session],
    [object[]]@([MirDB.SessionMode]::ServerTool, [System.Reflection.Assembly[]]@($library), $false, '', $databaseRoot, $backupRoot)
)
$session.Init()
$getCollection = $session.GetType().GetMethod('GetCollection', [Type[]]@())
$itemCollection = $getCollection.MakeGenericMethod([Library.SystemModels.ItemInfo]).Invoke($session, $null)
$items = $itemCollection.GetType().GetField('Binding').GetValue($itemCollection)
foreach ($item in $items | Where-Object { $_.ItemName -like '未鉴定*' }) {
    $tier = [int]$item.RequiredAmount
    if ($tier -lt 1 -or $tier -gt 5) { throw "非法鉴定等级: $($item.ItemName)" }
    $targetName = $item.ItemName.Substring(3)
    $matches = @($items | Where-Object ItemName -eq $targetName)
    if ($matches.Count -ne 1 -or $matches[0].Rarity.ToString() -ne 'Elite') {
        throw "无法唯一映射稀世成品: $($item.ItemName)"
    }
}
Write-Output 'PASS: equipment identification contract'
```

- [ ] **Step 3: 运行契约并确认红灯**

Run:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File 'D:\Debug\4月18日更新\Server\Scripts\Test\test_equipment_identification_contract.ps1'
```

Expected: 退出码非 0，首个错误为“缺少鉴定稀世装备.py”。

---

### Task 2: 实现 NPC 215 装备鉴定

**Files:**
- Create: `D:\Debug\4月18日更新\Server\Scripts\Npc\鉴定稀世装备.py`
- Test: `D:\Debug\4月18日更新\Server\Scripts\Test\test_equipment_identification_contract.ps1`

**Interfaces:**
- Consumes: `args = [Self, Sender, Menu, optional Links]`、`Sender.Inventory`、`SEnvir.GetItemInfo(name)`、背包内物品计数、`Sender.CanGainItems`、`ItemCheck`、`SEnvir.CreateFreshItem`、`Sender.GainItem`、`Sender.TakeItem(UserItem, count)`。
- Produces: `OnClick(args) -> dict` 和 `NpcEvent.add_listener(215, "OnClick", OnClick)`。

- [ ] **Step 1: 建立固定等级映射与标记读取函数**

```python
# -*- coding: utf-8 -*-
from Globals import *
import System
import NpcEvent
import Server.Envir.SEnvir as SEnvir
from Server.Models import ItemCheck

STONE_BY_TIER = {
    1: u"鉴定石一级",
    2: u"鉴定石二级",
    3: u"鉴定石三级",
    4: u"鉴定石四级",
    5: u"鉴定石五级",
}

def has_flag(item, flag):
    return (item.Flags & flag) == flag
```

- [ ] **Step 2: 用背包格子生成玩家当前可鉴定列表**

```python
def build_item_menu(sender):
    links = []
    for slot in range(Globals.InventorySize):
        item = sender.Inventory[slot]
        if item is None or item.Info is None:
            continue
        name = item.Info.ItemName
        if not name.startswith(u"未鉴定"):
            continue
        tier = int(item.Info.RequiredAmount)
        if tier not in STONE_BY_TIER:
            continue
        links.append(u"[{}（需{}）:{}]".format(name, STONE_BY_TIER[tier], 1000 + slot))
    if not links:
        return u"你的背包里没有可鉴定装备。\n\n[离开:0]"
    return u"请选择要鉴定的装备：\n\n{}\n\n[离开:0]".format(u"\n".join(links))
```

- [ ] **Step 3: 实现点击时的完整重校验与无损失败顺序**

```python
def identify(sender, slot):
    if slot < 0 or slot >= Globals.InventorySize:
        return u"无效的背包位置。\n\n[返回:99]"
    source_item = sender.Inventory[slot]
    if source_item is None or source_item.Info is None:
        return u"该位置已经没有装备。\n\n[返回:99]"
    source_name = source_item.Info.ItemName
    if not source_name.startswith(u"未鉴定"):
        return u"该物品不是未鉴定装备。\n\n[返回:99]"
    tier = int(source_item.Info.RequiredAmount)
    if tier not in STONE_BY_TIER:
        return u"该装备的鉴定等级无效。\n\n[返回:99]"
    target_name = source_name[3:]
    target_info = SEnvir.GetItemInfo(target_name)
    if target_info is None or target_info.Rarity != Rarity.Elite:
        return u"找不到对应的稀世成品，请联系管理员。\n\n[返回:99]"
    stone_name = STONE_BY_TIER[tier]
    if get_inventory_count(sender, stone_name) < 1:
        return u"缺少{}。\n\n[返回:99]".format(stone_name)
    check = ItemCheck(target_info, 1, get_preserved_flags(source_item), System.TimeSpan.Zero)
    if not sender.CanGainItems(False, check):
        return u"背包空间不足，鉴定未执行。\n\n[返回:99]"
    sender.GainItem(SEnvir.CreateFreshItem(check))
    sender.TakeItem(source_item, 1)
    sender.TakeItem(stone_name, 1)
    return u"鉴定成功，获得{}。\n\n[继续鉴定:99]\n[离开:0]".format(target_name)
```

- [ ] **Step 4: 接入菜单与监听器**

```python
def OnClick(args):
    sender = args[1]
    menu = args[2]
    result = {}
    if menu >= 1000 and menu < 1000 + Globals.InventorySize:
        say = identify(sender, menu - 1000)
    else:
        say = build_item_menu(sender)
    result['Say'] = say
    return result

NpcEvent.add_listener(215, "OnClick", OnClick)
```

- [ ] **Step 5: 编译语法并观察总契约仍因未接线而失败**

Run:

```powershell
& 'C:\Python27\python.exe' -c "import sys; [compile(open(p, 'rb').read(), p, 'exec') for p in sys.argv[1:]]" 'D:\Debug\4月18日更新\Server\Scripts\Npc\鉴定稀世装备.py'
powershell.exe -NoProfile -ExecutionPolicy Bypass -File 'D:\Debug\4月18日更新\Server\Scripts\Test\test_equipment_identification_contract.ps1'
```

Expected: Python 编译成功；总契约继续因缺少 216 模块或入口而失败。

---

### Task 3: 实现 NPC 216 鉴定石向下分解

NPC 216 主菜单还提供五档直接购买；购买必须按上面的固定成本先校验元宝和高级碎片，调用 `GiveItems({stone_name: 1})` 成功后才扣除成本。

**Files:**
- Create: `D:\Debug\4月18日更新\Server\Scripts\Npc\兑换鉴定石.py`
- Test: `D:\Debug\4月18日更新\Server\Scripts\Test\test_equipment_identification_contract.ps1`

**Interfaces:**
- Consumes: `args = [Self, Sender, Menu, optional Links]`、`Sender.Inventory`、`Sender.GiveItems(dict)`、`Sender.CanGainItems`、`ItemCheck`、`SEnvir.CreateFreshItem`、`Sender.GainItem`、`Sender.TakeItem(UserItem, count)`、`UserItemFlags.Bound` 和 `UserItemFlags.Worthless`。
- Produces: `OnClick(args) -> dict` 和 `NpcEvent.add_listener(216, "OnClick", OnClick)`。

- [ ] **Step 1: 建立独立模块导入、标记读取函数和只向下一级的映射**

```python
# -*- coding: utf-8 -*-
from Globals import *
import System
import NpcEvent
import Server.Envir.SEnvir as SEnvir
from Server.Models import ItemCheck

def has_flag(item, flag):
    return (item.Flags & flag) == flag

LOWER_STONE = {
    u"鉴定石五级": u"鉴定石四级",
    u"鉴定石四级": u"鉴定石三级",
    u"鉴定石三级": u"鉴定石二级",
    u"鉴定石二级": u"鉴定石一级",
}
```

- [ ] **Step 2: 按背包格子列出可分解石头并在点击时重校验**

```python
def build_stone_menu(sender):
    links = []
    for slot in range(Globals.InventorySize):
        item = sender.Inventory[slot]
        if item is None or item.Info is None:
            continue
        source_name = item.Info.ItemName
        if source_name in LOWER_STONE:
            links.append(u"[{} → {}:{}]".format(source_name, LOWER_STONE[source_name], 2000 + slot))
    if not links:
        return u"你的背包里没有可向下分解的鉴定石。\n\n[离开:0]"
    return u"每次按 1:1 向下分解一颗：\n\n{}\n\n[离开:0]".format(u"\n".join(links))

def exchange(sender, slot):
    if slot < 0 or slot >= Globals.InventorySize:
        return u"无效的背包位置。\n\n[返回:99]"
    source_item = sender.Inventory[slot]
    if source_item is None or source_item.Info is None:
        return u"该位置已经没有鉴定石。\n\n[返回:99]"
    source_name = source_item.Info.ItemName
    if source_name not in LOWER_STONE:
        return u"该物品不能向下分解。\n\n[返回:99]"
    target_name = LOWER_STONE[source_name]
    target_info = SEnvir.GetItemInfo(target_name)
    if target_info is None:
        return u"找不到对应的低级鉴定石，请联系管理员。\n\n[返回:99]"
    check = ItemCheck(target_info, 1, get_preserved_flags(source_item), System.TimeSpan.Zero)
    if not sender.CanGainItems(False, check):
        return u"背包空间不足，分解未执行。\n\n[返回:99]"
    sender.GainItem(SEnvir.CreateFreshItem(check))
    sender.TakeItem(source_item, 1)
    return u"分解成功，获得{}。\n\n[继续分解:99]\n[离开:0]".format(target_name)
```

- [ ] **Step 3: 接入菜单与监听器并验证语法**

```python
def OnClick(args):
    sender = args[1]
    menu = args[2]
    result = {}
    if menu >= 2000 and menu < 2000 + Globals.InventorySize:
        say = exchange(sender, menu - 2000)
    else:
        say = build_stone_menu(sender)
    result['Say'] = say
    return result

NpcEvent.add_listener(216, "OnClick", OnClick)
```

Run:

```powershell
& 'C:\Python27\python.exe' -c "import sys; [compile(open(p, 'rb').read(), p, 'exec') for p in sys.argv[1:]]" 'D:\Debug\4月18日更新\Server\Scripts\Npc\兑换鉴定石.py'
```

Expected: 退出码 0。

---

### Task 4: 接入主入口并解除错误监听

**Files:**
- Modify: `D:\Debug\4月18日更新\Server\Scripts\Npc\__init__.py`
- Modify: `D:\Debug\4月18日更新\Server\Scripts\Npc\潘夜岛\__init__.py`
- Modify: `D:\Debug\4月18日更新\Server\Scripts\Npc\管理中心.py:1275`
- Test: `D:\Debug\4月18日更新\Server\Scripts\Test\test_equipment_identification_contract.ps1`

**Interfaces:**
- Consumes: Task 2 的 `Npc.鉴定稀世装备.OnClick` 和 Task 3 的 `Npc.兑换鉴定石.OnClick`。
- Produces: 管理中心菜单 38/39、唯一监听 215/216、服务器启动时自动导入两个模块。

- [ ] **Step 1: 修改导入关系**

在 `Npc\__init__.py` 的管理中心相关导入附近加入：

```python
import Npc.鉴定稀世装备
import Npc.兑换鉴定石
```

从 `Npc\潘夜岛\__init__.py` 删除以下两行，文件本身保留：

```python
import Npc.潘夜岛.钓鱼商俊熙
import Npc.潘夜岛.钓鱼商秀贤
```

- [ ] **Step 2: 增加管理中心处理器**

在现有 `Menu == 37` 分支后增加：

```python
elif (Menu == 38):
    NPCObject = ServerUtils.GetNPCObject(215)
    if NPCObject:
        Sender.NPC = NPCObject
        return Npc.鉴定稀世装备.OnClick([Self, Sender, 0])
    say = """未找到指定的NPC"""
elif (Menu == 39):
    NPCObject = ServerUtils.GetNPCObject(216)
    if NPCObject:
        Sender.NPC = NPCObject
        return Npc.兑换鉴定石.OnClick([Self, Sender, 0])
    say = """未找到指定的NPC"""
```

- [ ] **Step 3: 在管理中心主菜单增加可见入口**

在主菜单功能区加入：

```python
[装备鉴定:38]      [鉴定石分解:39]
```

- [ ] **Step 4: 运行总契约并确认绿灯**

Run:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File 'D:\Debug\4月18日更新\Server\Scripts\Test\test_equipment_identification_contract.ps1'
```

Expected: 输出 `PASS: equipment identification contract`，退出码 0。

---

### Task 5: 最终静态验收

**Files:**
- Verify only; no additional files.

**Interfaces:**
- Consumes: Tasks 1-4 的所有产物。
- Produces: 可复核的语法、唯一监听、数据库映射和改动范围证据。

- [ ] **Step 1: 编译全部 owned Python 文件**

Run the repository's IronPython syntax checker once for each owned Python file:

```powershell
$checker = 'D:\相聚假人\Source\.diagnostics\IronPythonSyntaxCheck\bin\Debug\net8.0\IronPythonSyntaxCheck.exe'
& $checker 'D:\Debug\4月18日更新\Server\Scripts\Npc\鉴定稀世装备.py'
& $checker 'D:\Debug\4月18日更新\Server\Scripts\Npc\兑换鉴定石.py'
& $checker 'D:\Debug\4月18日更新\Server\Scripts\Npc\管理中心.py'
& $checker 'D:\Debug\4月18日更新\Server\Scripts\Npc\__init__.py'
& $checker 'D:\Debug\4月18日更新\Server\Scripts\Npc\潘夜岛\__init__.py'
```

Expected: 退出码 0，无语法错误。

- [ ] **Step 2: 验证监听器唯一性**

Run:

```powershell
rg -n "add_listener\((215|216)" 'D:\Debug\4月18日更新\Server\Scripts\Npc'
```

Expected: 仅新脚本各一条有效监听；旧钓鱼商文件中的两条文本仍存在，但其模块不再由任何 `__init__.py` 导入。结合导入扫描确认运行时唯一。

- [ ] **Step 3: 运行数据库映射契约**

运行 Task 1 已写入测试脚本的数据库契约；其核心断言为：

```powershell
$tier = [int]$item.RequiredAmount
if ($tier -lt 1 -or $tier -gt 5) { throw "非法鉴定等级: $($item.ItemName)" }
$targetName = $item.ItemName.Substring(3)
$matches = @($items | Where-Object ItemName -eq $targetName)
if ($matches.Count -ne 1 -or $matches[0].Rarity.ToString() -ne 'Elite') {
    throw "无法唯一映射稀世成品: $($item.ItemName)"
}
```

Expected: 当前全部未鉴定物品通过。

- [ ] **Step 4: 核对改动范围与哈希**

Run:

```powershell
Get-FileHash -Algorithm SHA256 `
  'D:\Debug\4月18日更新\Server\Scripts\Npc\鉴定稀世装备.py', `
  'D:\Debug\4月18日更新\Server\Scripts\Npc\兑换鉴定石.py', `
  'D:\Debug\4月18日更新\Server\Scripts\Npc\管理中心.py', `
  'D:\Debug\4月18日更新\Server\Scripts\Npc\__init__.py', `
  'D:\Debug\4月18日更新\Server\Scripts\Npc\潘夜岛\__init__.py', `
  'D:\Debug\4月18日更新\Server\Scripts\Test\test_equipment_identification_contract.ps1'
```

Expected: 六个 owned 功能/测试文件均产生 SHA-256。设计与计划文档只作为流程产物单独列出。

- [ ] **Step 5: 明确未执行层**

报告必须写明：未修改数据库/C#，未改 `Scripts888`，未重载脚本、未重启服务器、未完成游戏内点击和物品扣发验收。
