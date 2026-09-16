# D键危险地图传送：本国领土与神舰 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在实际生效的 D 键危险传送主菜单中增加本国领土和神舰入口，两个入口均消耗 50,000 金币。

**Architecture:** 继续使用现有 NPC 211 的 `OnClick` 菜单分支，不抽取新辅助函数或改变注册方式。在 50,000 金币菜单区域增加未占用的菜单编号 28、29，并在同一处理函数中复用现有 `SubGold` 和 `TeleportByMapIndex` 模式。

**Tech Stack:** IronPython 风格服务器脚本、PowerShell 静态回归合同、服务器脚本热加载日志。

## Global Constraints

- 只修改 `D:\Debug\4月18日更新\Server\Scripts\Npc\便捷传送.py` 的 D 键主菜单和对应处理分支。
- 本国领土使用 `TeleportByMapIndex(490, 127, 45)`。
- 神舰使用 `TeleportByMapIndex(246, 40, 60)`。
- 两个入口均检查并扣除 50,000 金币。
- 不修改元宝传送菜单、其他传送入口、NPC 注册方式、数据库或平行旧脚本。
- 静态检查和日志检查不等同于游戏内点击传送验证。

---

### Task 1: 创建 D 键危险传送回归合同并确认 RED

**Files:**
- Create: `.diagnostics/test_dkey_danger_teleport_contract.ps1`
- Read: `D:\Debug\4月18日更新\Server\Scripts\Npc\便捷传送.py`

**Interfaces:**
- Consumes: 实际生效的 `Npc\便捷传送.py` 文件文本。
- Produces: 在实现缺失时失败、实现后可重复运行的 PowerShell 合同。

- [ ] **Step 1: Write the failing test**

创建 `.diagnostics/test_dkey_danger_teleport_contract.ps1`，内容如下：

```powershell
$ErrorActionPreference = 'Stop'

$scriptPath = 'D:\Debug\4月18日更新\Server\Scripts\Npc\便捷传送.py'

function Assert-Contract([bool]$condition, [string]$message) {
    if (-not $condition) {
        throw $message
    }
}

Assert-Contract (Test-Path -LiteralPath $scriptPath) "active convenience teleport script missing: $scriptPath"
$scriptText = Get-Content -LiteralPath $scriptPath -Raw -Encoding UTF8

$dangerMenu = [regex]::Match(
    $scriptText,
    '(?s)危险地图传送：费用50000金币.*?元宝地图传送'
).Value
Assert-Contract ($dangerMenu -match '\[本国领土:28\]\s+\[神舰:29\]') '50,000-gold danger menu must expose 本国领土:28 and 神舰:29'

foreach ($entry in @(
    @{ Id = 28; Map = '490,127,45'; Name = '本国领土' },
    @{ Id = 29; Map = '246,40,60'; Name = '神舰' }
)) {
    $handler = [regex]::Match(
        $scriptText,
        "(?s)elif\(Menu == $($entry.Id)\):.*?Sender\.TeleportByMapIndex\($($entry.Map)\)\s*return"
    ).Value
    Assert-Contract ($handler.Length -gt 0) "Menu $($entry.Id) ($($entry.Name)) must have a teleport handler"
    Assert-Contract ($handler -match 'Sender\.Gold\s*<\s*50000') "Menu $($($entry.Id)) must check 50,000 gold"
    Assert-Contract ($handler -match 'SubGold\(Sender,50000\)') "Menu $($($entry.Id)) must deduct 50,000 gold"
}

Assert-Contract (([regex]::Matches($scriptText, '\bMenu\s*==\s*(28|29)\b')).Count -eq 2) 'Menu 28 and 29 must each have exactly one handler'

Write-Output 'D-key danger teleport contract passed'
```

- [ ] **Step 2: Run test to verify it fails**

Run:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File D:\相聚假人\Source\.diagnostics\test_dkey_danger_teleport_contract.ps1
```

Expected: FAIL because the current menu has no `[本国领土:28] [神舰:29]` entries and has no `Menu == 28`/`Menu == 29` handlers. Do not modify production code to make this first run pass.

### Task 2: 实现两个 50,000 金币传送入口

**Files:**
- Modify: `D:\Debug\4月18日更新\Server\Scripts\Npc\便捷传送.py` in the existing danger-menu handler block and main-menu text.
- Test: `.diagnostics/test_dkey_danger_teleport_contract.ps1`

**Interfaces:**
- Consumes: Task 1 的 failing contract and existing `OnClick(args)` conventions.
- Produces: Menu 28/29 handlers and main-menu buttons recognized by the contract.

- [ ] **Step 1: Write the minimal implementation**

在现有 `elif(Menu == 27):` 分支之后、元宝菜单分支之前加入以下两个分支：

```python
	elif(Menu == 28):
		if (Sender.Gold < 50000):
			say = """你没有足够的金币，无法传送。
				
				[关闭:0]"""	
		else:
			SubGold(Sender,50000)
			Sender.TeleportByMapIndex(490,127,45)
			return
	elif(Menu == 29):
		if (Sender.Gold < 50000):
			say = """你没有足够的金币，无法传送。
				
				[关闭:0]"""	
		else:
			SubGold(Sender,50000)
			Sender.TeleportByMapIndex(246,40,60)
			return
```

在主菜单现有 `[黑度宫:22] [真天宫:21] [诺玛遗址:23] [西沙漠:24]` 行后增加：

```text
		[本国领土:28]    [神舰:29]
```

保持现有制表符风格和其他菜单内容不变。

- [ ] **Step 2: Run the focused contract**

Run:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File D:\相聚假人\Source\.diagnostics\test_dkey_danger_teleport_contract.ps1
```

Expected: PASS with `D-key danger teleport contract passed`.

### Task 3: 运行既有回归检查并确认服务器脚本加载

**Files:**
- Read: `D:\相聚假人\Source\.diagnostics\test_debug_server_scripts_contract.ps1`
- Read: `D:\Debug\4月18日更新\Server\Logs\Logs_8_22.txt`
- Verify: `D:\Debug\4月18日更新\Server\Scripts\Npc\便捷传送.py`

**Interfaces:**
- Consumes: Task 2 的修改后脚本和现有诊断合同。
- Produces: 静态合同、脚本加载日志和变更范围证据。

- [ ] **Step 1: Run the existing debug-server contract**

Run:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File D:\相聚假人\Source\.diagnostics\test_debug_server_scripts_contract.ps1
```

Expected: PASS with `debug server scripts contract passed`.

- [ ] **Step 2: Check the changed-file scope**

Run:

```powershell
rg -n -C 3 '本国领土:28|神舰:29|Menu == 28|Menu == 29|TeleportByMapIndex\((490,127,45|246,40,60)\)' D:\Debug\4月18日更新\Server\Scripts\Npc\便捷传送.py
```

Expected: only the new main-menu labels and their two handlers are present; existing Menu 924 yuanbao handling remains unchanged.

- [ ] **Step 3: Check the current server log after script reload**

Run:

```powershell
$logPath = 'D:\Debug\4月18日更新\Server\Logs\Logs_8_22.txt'
Get-Content -LiteralPath $logPath -Tail 120 -Encoding UTF8
```

Expected: no new Python script-load exception or traceback attributable to `Npc\便捷传送.py`. Do not stop or restart the already-running local server as part of this task.

- [ ] **Step 4: Record the runtime acceptance boundary**

Report static contract and log results separately from manual game acceptance. A player must still open D 键, select each new option, and confirm the 50,000-gold deduction and destination in the game client; this cannot be proven by the static checks alone.

## Completion Notes

This workspace is not a Git repository, so no commit step is included. Preserve the existing server process and do not deploy files to another server unless separately requested.
