# 奔马岛便捷传送 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在当前生效的便捷传送脚本中增加 `[奔马岛:30]`，收费50000金币并传送到地图1551的现有坐标 `(96,218)`。

**Architecture:** 复用现有 `TELEPORT_DATA["danger"]` 和 `handle_teleport`，只新增一个数据记录，不新增传送分支。把同一个菜单按钮追加到当前脚本中4个重复的主菜单刷新文本，保证初始打开和回收功能刷新后的菜单一致。

**Tech Stack:** IronPython/Python脚本、PowerShell 5.1静态合同检查、SHA-256文件哈希。

## Global Constraints

- 只修改 `D:\Debug\4月18日更新\Server\Scripts\Npc\其他\便捷传送.py` 和本计划指定的静态合同文件。
- 新菜单必须使用编号 `30`、费用 `50000`、地图 `1551`、坐标 `(96,218)`。
- 保留现有菜单 `28`（本国领土）和 `29`（神舰）的数据及行为。
- 不修改旧版 `D:\Debug\4月18日更新\Server\Scripts\Npc\便捷传送.py`。
- 不修改 `D:\Debug\4月18日更新\Server\Scripts888`，不复制文件到服务器，不重启服务，不进行在线验收。
- 不增加桃源仙境其他地图的传送入口，不修改地图、数据库、客户端资源或NPC活动逻辑。
- 不创建提交或PR；完成后保留工作区改动供用户检查。

---

## 文件结构

- `D:\Debug\4月18日更新\Server\Scripts\Npc\其他\便捷传送.py`：当前生效的便捷传送数据和4个主菜单刷新文本；唯一的生产脚本修改目标。
- `D:\相聚假人\Source\.diagnostics\test_taoyuan_entry_teleport_contract.ps1`：聚焦静态合同，验证菜单数据、显示文本和既有28/29数据。
- `D:\相聚假人\Source\docs\superpowers\specs\2026-09-05-taoyuan-entry-teleport-design.md`：已确认的设计说明，本任务不再修改。

### Task 1: 建立桃源入口静态合同并确认修改前失败

**Files:**
- Create: `D:\相聚假人\Source\.diagnostics\test_taoyuan_entry_teleport_contract.ps1`
- Read: `D:\Debug\4月18日更新\Server\Scripts\Npc\其他\便捷传送.py`

**Interfaces:**
- Consumes: 当前生效便捷传送脚本的UTF-8文本。
- Produces: 一个可在修改前失败、修改后通过的PowerShell合同。

- [x] **Step 1: 记录修改前的范围哈希**

运行以下只读命令，记录目标脚本、旧版脚本和 `Scripts888` 对应文件的SHA-256；后续只允许目标脚本哈希变化：

```powershell
$trackedPaths = @(
    'D:\Debug\4月18日更新\Server\Scripts\Npc\其他\便捷传送.py',
    'D:\Debug\4月18日更新\Server\Scripts\Npc\便捷传送.py',
    'D:\Debug\4月18日更新\Server\Scripts888\Npc\其他\便捷传送.py'
)
foreach ($trackedPath in $trackedPaths) {
    if (-not (Test-Path -LiteralPath $trackedPath)) {
        throw "missing tracked file: $trackedPath"
    }
    Get-FileHash -Algorithm SHA256 -LiteralPath $trackedPath
}
```

- [x] **Step 2: 写入失败合同**

用 `apply_patch` 创建合同文件，内容如下：

```powershell
$ErrorActionPreference = 'Stop'

$targetPath = 'D:\Debug\4月18日更新\Server\Scripts\Npc\其他\便捷传送.py'
if (-not (Test-Path -LiteralPath $targetPath)) {
    throw "missing active convenience teleport script: $targetPath"
}

$content = Get-Content -LiteralPath $targetPath -Raw -Encoding UTF8

$newRecord = '30: {"cost": 50000, "map": 1551, "x": 96, "y": 218}  # 奔马岛'
$recordCount = ([regex]::Matches($content, [regex]::Escape($newRecord))).Count
if ($recordCount -ne 1) {
    throw "expected exactly one Benma Island teleport record, found $recordCount"
}

$menuLine = '[本国领土:28] [神舰:29] [奔马岛:30]'
$menuLineCount = ([regex]::Matches($content, [regex]::Escape($menuLine))).Count
if ($menuLineCount -ne 4) {
    throw "expected the Benma Island button in all 4 main-menu refresh paths, found $menuLineCount"
}

$existingRecords = @(
    '28: {"cost": 50000, "map": 490, "x": 127, "y": 45}  # 本国领土',
    '29: {"cost": 50000, "map": 246, "x": 40, "y": 60}  # 神舰'
)
foreach ($existingRecord in $existingRecords) {
    $existingCount = ([regex]::Matches($content, [regex]::Escape($existingRecord))).Count
    if ($existingCount -ne 1) {
        throw "existing teleport record changed or duplicated: $existingRecord"
    }
}

if ($content.IndexOf('elif Menu == 0 or Menu == MAIN_MENU', [System.StringComparison]::Ordinal) -lt 0) {
    throw 'main menu branch is missing'
}

Write-Output 'taoyuan entry teleport contract passed'
```

- [x] **Step 3: 运行合同，确认修改前为失败状态**

运行：

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File 'D:\相聚假人\Source\.diagnostics\test_taoyuan_entry_teleport_contract.ps1'
```

预期：命令失败，并指出缺少桃源仙境传送记录；因为生产脚本尚未修改，失败是合同的RED状态。

### Task 2: 增加桃源入口并完成静态验证

**Files:**
- Modify: `D:\Debug\4月18日更新\Server\Scripts\Npc\其他\便捷传送.py:63,284,594,639,686`（行号以修改前文件为准）
- Test: `D:\相聚假人\Source\.diagnostics\test_taoyuan_entry_teleport_contract.ps1`

**Interfaces:**
- Consumes: Task 1 的失败合同和当前 `TELEPORT_DATA`/主菜单文本。
- Produces: 菜单30可由现有 `handle_teleport(Sender, "danger", 30)` 处理的脚本文本。

- [x] **Step 1: 在危险地图数据中加入唯一记录**

在现有神舰记录之后、危险地图字典结束之前加入这一行。保留28和29的费用、地图和坐标；由于29原本是字典最后一项，需要只补一个逗号作为语法分隔符：

```python
30: {"cost": 50000, "map": 1551, "x": 96, "y": 218}  # 奔马岛
```

- [x] **Step 2: 更新4个主菜单刷新文本**

将目标脚本中4处完全相同的：

```text
[本国领土:28] [神舰:29]
```

分别改为：

```text
[本国领土:28] [神舰:29] [奔马岛:30]
```

必须只修改这4处菜单显示和1处数据记录，不调整其他菜单排列、收费或传送逻辑。

- [x] **Step 3: 运行合同，确认GREEN状态**

运行：

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File 'D:\相聚假人\Source\.diagnostics\test_taoyuan_entry_teleport_contract.ps1'
```

预期输出：

```text
taoyuan entry teleport contract passed
```

- [x] **Step 4: 核对实际变更范围和关键文本**

运行以下只读检查：

```powershell
$targetPath = 'D:\Debug\4月18日更新\Server\Scripts\Npc\其他\便捷传送.py'
$oldPath = 'D:\Debug\4月18日更新\Server\Scripts\Npc\便捷传送.py'
$scripts888Path = 'D:\Debug\4月18日更新\Server\Scripts888\Npc\其他\便捷传送.py'

Select-String -LiteralPath $targetPath -Pattern '30: \{"cost"|\[本国领土:28\] \[神舰:29\] \[奔马岛:30\]' |
    Select-Object LineNumber, Line

foreach ($path in @($oldPath, $scripts888Path)) {
    Get-FileHash -Algorithm SHA256 -LiteralPath $path
}
```

预期：关键文本只出现在目标脚本；旧版脚本和 `Scripts888` 文件哈希与 Task 1 Step 1 记录一致。

- [x] **Step 5: 停在静态验证边界并报告**

报告目标脚本最终SHA-256、合同输出和未执行事项。不得复制到服务器运行目录、重启服务或宣称已完成在线传送验收；实际服务器验收需要用户后续授权和操作窗口。
