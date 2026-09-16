# 雪原活动副本单人进入 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在 `Server\Scripts` 的雪原荒村副本入口中允许符合现有条件的单人进入，并保持现有组队行为不变。

**Architecture:** 在 `Menu == 1` 的准入分支中保留队长判断，只对有队伍且非队长的请求拒绝；有队伍使用原 `Sender.GroupMembers`，无队伍使用 `[Sender]`。校验、建图、变量设置、扣费和传送共用同一套玩家集合，避免复制副本逻辑。

**Tech Stack:** IronPython NPC 脚本、PowerShell 5.1 静态合同检查；服务器运行时验收由用户复制脚本并重启脚本宿主后完成。

## Global Constraints

- 只修改 `D:\Debug\4月18日更新\Server\Scripts\Npc\雪原活动管理员.py`。
- 不修改 `Scripts888`、客户端菜单、其他菜单或其他副本。
- 单人仍必须满足活动时间、等级至少50、每日次数、100元宝和2个魔晶石条件。
- 有队伍时继续要求队长发起，并保留原有逐队员检查。
- 不把现有组队人数判断从 `< 0` 改成 `< 5`。
- 不改变地图1530、地图时间120分钟、怪物、费用、材料、变量名或传送坐标 `(90,121)`。
- 不复制到服务器、不重启服务、不做运行时部署；本计划只覆盖本地脚本修改和静态验证。
- `D:\相聚假人\Source` 无 `.git` 目录，因此不执行提交操作。

---

## 文件与职责

- Create: `D:\相聚假人\Source\.diagnostics\test_snowfield_solo_entry_contract.ps1` — 读取目标脚本并验证单人回退集合、组队队长保护、既有准入条件和进入副作用。
- Modify: `D:\Debug\4月18日更新\Server\Scripts\Npc\雪原活动管理员.py:39-114` — 只调整雪原荒村 `Menu == 1` 的入口分支和两处玩家遍历。
- Do not modify: `D:\Debug\4月18日更新\Server\Scripts888\Npc\雪原活动管理员.py`。
- Existing reference: `D:\相聚假人\Source\docs\superpowers\specs\2026-09-01-snowfield-solo-entry-design.md` — 已确认的设计边界，不在实施中重复修改。

### Task 1: Write the failing static contract

**Files:**
- Create: `D:\相聚假人\Source\.diagnostics\test_snowfield_solo_entry_contract.ps1`
- Read: `D:\Debug\4月18日更新\Server\Scripts\Npc\雪原活动管理员.py`

**Interfaces:**
- Consumes: target script as UTF-8 text.
- Produces: exit code `1` with named failed assertions until the production script contains the approved single-player path; exit code `0` only after all assertions pass.

- [x] **Step 1: Create the contract with the exact assertions below**

```powershell
$ErrorActionPreference = 'Stop'

$targetPath = 'D:\Debug\4月18日更新\Server\Scripts\Npc\雪原活动管理员.py'
if (-not (Test-Path -LiteralPath $targetPath -PathType Leaf)) {
    Write-Error "Missing target script: $targetPath"
    exit 2
}

$source = Get-Content -LiteralPath $targetPath -Encoding UTF8 -Raw
$menuStart = $source.IndexOf('if (Menu == 1):')
$menuEnd = if ($menuStart -ge 0) { $source.IndexOf('elif (Menu == 2):', $menuStart) } else { -1 }

$passed = 0
$failures = @()
function Assert-Contract {
    param(
        [Parameter(Mandatory = $true)][bool]$Condition,
        [Parameter(Mandatory = $true)][string]$Name
    )

    if ($Condition) {
        $script:passed++
        Write-Host "PASS: $Name"
    } else {
        $script:failures += $Name
        Write-Host "FAIL: $Name"
    }
}

Assert-Contract ($menuStart -ge 0 -and $menuEnd -gt $menuStart) 'snowfield Menu == 1 block exists'
$menu = if ($menuEnd -gt $menuStart) { $source.Substring($menuStart, $menuEnd - $menuStart) } else { '' }

Assert-Contract ($menu -match 'if\s*\(\s*Sender\.GroupMembers\s+and\s+Sender\s*!=\s*Sender\.GroupMembers\[0\]\s*\)') 'group non-leader guard remains'
Assert-Contract ($menu -match 'entry_players\s*=\s*Sender\.GroupMembers') 'group requests use GroupMembers'
Assert-Contract ($menu -match 'entry_players\s*=\s*\[Sender\]') 'solo requests use a single-player fallback'
Assert-Contract ([regex]::Matches($menu, 'for player in entry_players:').Count -eq 2) 'validation and entry effects both use the fallback collection'
Assert-Contract ($menu -notmatch 'for player in Sender\.GroupMembers:') 'Menu 1 no longer directly iterates a missing solo collection'
Assert-Contract ($menu -notmatch '没有队伍') 'solo requests are not rejected for having no group'

Assert-Contract ($menu -match 'current_time_is_between\("17:59:00", "23:00:00"\)') 'activity time guard remains'
Assert-Contract ($menu -match 'Sender\.GetItemCount\("魔晶石"\)\s*>\s*1') 'sender material gate remains'
Assert-Contract ($menu -match 'PlayerGetV\(Sender,GV_ZDBOSSFB_COUNT\)\s*==\s*0') 'sender daily-entry gate remains'
Assert-Contract ($menu -match 'PlayerGetV\(player,GV_ZDBOSSFB_COUNT\)\s*==\s*1') 'member daily-entry check remains'
Assert-Contract ($menu -match 'player\.Level\s*<\s*50') 'member level check remains'
Assert-Contract ($menu -match 'player\.GameGold\s*<\s*100') 'member gold check remains'
Assert-Contract ($menu -match 'player\.GetItemCount\("魔晶石"\)\s*<\s*2') 'member material check remains'
Assert-Contract ($menu -match 'len\(Sender\.GroupMembers\)\s*<\s*0') 'existing group-count behavior remains unchanged'
Assert-Contract ($menu -notmatch 'len\(Sender\.GroupMembers\)\s*<\s*5') 'group-count behavior is not newly changed to five'

Assert-Contract ($menu -match 'CreateMap\(1530\)') 'snowfield map remains 1530'
Assert-Contract ($menu -match 'MapTime\s*=\s*datetime\.now\(\)\+timedelta\(minutes=120\)') 'map duration remains 120 minutes'
Assert-Contract ($menu -match 'SubGameGold\(player,100\)') 'entry fee remains 100 gold'
Assert-Contract ($menu -match 'player\.TakeItem\("魔晶石",2\)') 'entry material cost remains two crystals'
Assert-Contract ($menu -match 'player\.Teleport\(map,90,121\)') 'entry teleport remains (90,121)'

if ($failures.Count -gt 0) {
    Write-Host "RESULT: FAIL ($passed passed; $($failures.Count) failed)"
    $failures | ForEach-Object { Write-Host "FAILED ASSERTION: $_" }
    exit 1
}

Write-Host "RESULT: PASS ($passed assertions)"
exit 0
```

- [x] **Step 2: Run the contract before production changes to verify RED**

Run:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File 'D:\相聚假人\Source\.diagnostics\test_snowfield_solo_entry_contract.ps1'
```

Expected: exit code `1`; the failures must include `solo requests use a single-player fallback`, `validation and entry effects both use the fallback collection`, and `solo requests are not rejected for having no group`. Do not edit the production script until this expected failure is observed.

### Task 2: Implement the minimal single-player path

**Files:**
- Modify: `D:\Debug\4月18日更新\Server\Scripts\Npc\雪原活动管理员.py:39-114`
- Preserve: all code outside `Menu == 1`, including the `Scripts888` copy.

**Interfaces:**
- Consumes: `Sender.GroupMembers`, `Sender`, and the existing `Menu == 1` checks.
- Produces: local `entry_players`, containing the original group members for a group or `[Sender]` for a solo request.

- [x] **Step 1: Record the pre-edit hashes**

Run:

```powershell
Get-FileHash -LiteralPath 'D:\Debug\4月18日更新\Server\Scripts\Npc\雪原活动管理员.py' -Algorithm SHA256
Get-FileHash -LiteralPath 'D:\Debug\4月18日更新\Server\Scripts888\Npc\雪原活动管理员.py' -Algorithm SHA256
```

Expected before editing: both files report `2E4C3E28AA05A01441D26DDD8F57CDE0963F2010F767234DC6F9DD7248A8B823`.

- [x] **Step 2: Replace only the existing Menu 1 group wrapper and two loops with this control flow**

At the current `if(Sender.GroupMembers):` block, make the non-leader rejection apply only when a group exists, then assign the common collection. The complete resulting block must have this structure and retain the existing validation, monster creation, variable, fee, material, and teleport statements:

```python
					if(Sender.GroupMembers and Sender != Sender.GroupMembers[0]):   #队长判断
						say = """不是队长
						
						[离开:0]"""
					else:
						if(Sender.GroupMembers):
							entry_players = Sender.GroupMembers
						else:
							entry_players = [Sender]
						bOpen = True
						if Sender.GroupMembers and len(Sender.GroupMembers) < 0:    #判断队伍人数
							bOpen = False
							say = """队员数不足5人,无法进入.
							
							[离开:0]"""
						else:
							for player in entry_players:                 #遍历所有队员或单人
								if(PlayerGetV(player,GV_ZDBOSSFB_COUNT) == 1):  #队员变量判断  数值判断是否进入次数
									bOpen = False
									say = """队伍中有队员已经去过副本了
									无法进入
									
									[离开:0]"""
									break
								if player.Level < 50 :                      #队员等级判断
									bOpen = False
									say = """队伍中有队员等级不够50级，去了躺板板
									无法进入
									
									[离开:0]"""
									break
								if (player.GameGold < 100):                   #队员金币判断
									bOpen = False
									say = """队伍中有队员元宝不足，需要100元宝的门票！
									无法进入
									
									[离开:0]"""
									break
								if(player.GetItemCount("魔晶石") < 2):  #队员材料判断
									bOpen = False
									say = """队伍中有队员“魔晶石”都不带一颗，想混水摸鱼哦~
									无法进入
									
									[离开:0]"""
									break
						if bOpen:    #如果可以开启
							map = Server.Envir.SEnvir.CreateMap(1530)               #开启副本地图  （地图ID）
							map.MapTime = datetime.now()+timedelta(minutes=120)    #副本地图关卡时间设置（分钟）
							map.CreateMon(48,44,2,'沃玛教主【副本】',1)
							map.CreateMon(48,56,100,'石岩射手',40)
							map.CreateMon(106,43,100,'石岩射手',40)
							map.CreateMon(148,51,100,'石岩射手',30)
							map.CreateMon(65,113,100,'石岩射手',30)
							map.CreateMon(118,83,100,'石岩射手',30)
							map.CreateMon(237,58,100,'石岩射手',30)
							map.CreateMon(227,96,100,'反手一刀',30)
							map.CreateMon(184,53,100,'反手一刀',30)
							map.CreateMon(188,104,100,'反手一刀',30)
							map.CreateMon(212,155,100,'反手一刀',30)
							map.CreateMon(137,55,100,'反手一刀',30)
							map.CreateMon(162,176,100,'蓝色背刺',40)
							map.CreateMon(207,145,100,'蓝色背刺',40)
							map.CreateMon(231,188,100,'蓝色背刺',40)
							map.CreateMon(179,232,100,'蓝色背刺',40)
							map.CreateMon(228,234,100,'蓝色背刺',40)
							PlayerSetV(Sender,GV_ZDBOSSFB_COUNT,1)
							PlayerSetV(Sender,GV_KILLMON_WMGWCOUNT,0)
							PlayerSetV(Sender,GV_KILLMON_WMGWJSCOUNT,0)
							PlayerSetV(Sender,GV_KILLMON_WMWSJSCOUNT,0)
							PlayerSetV(Sender,GV_KILLMON_ZMGWCOUNT,0)
							for player in entry_players:                     #遍历所有队员或单人
								PlayerSetV(player,GV_ZDBOSSFB_COUNT,1)             #赋值变量为1，代表进入
								SubGameGold(player,100)                              #扣除金币
								player.TakeItem("魔晶石",2)                    #扣除材料
								player.Teleport(map,90,121)                        #把全组人或单人传送进副本
```

The only semantic additions are `entry_players = [Sender]`, the group-qualified leader guard, the group-qualified existing count check, and replacing the two `Sender.GroupMembers` loops with `entry_players`. Keep the existing group-specific failure messages exactly as they are.

### Task 3: Verify GREEN and protected scope

**Files:**
- Test: `D:\相聚假人\Source\.diagnostics\test_snowfield_solo_entry_contract.ps1`
- Inspect: `D:\Debug\4月18日更新\Server\Scripts\Npc\雪原活动管理员.py`
- Protect: `D:\Debug\4月18日更新\Server\Scripts888\Npc\雪原活动管理员.py`

**Interfaces:**
- Consumes: the edited target script and the pre-edit hashes from Task 2.
- Produces: contract PASS, source syntax evidence if a Python runtime is available, and a protected-copy hash check.

- [x] **Step 1: Run the contract after the edit**

Run:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File 'D:\相聚假人\Source\.diagnostics\test_snowfield_solo_entry_contract.ps1'
```

Expected: exit code `0` and `RESULT: PASS`. If it fails, correct the target script rather than weakening the assertions.

- [x] **Step 2: Parse the edited file when Python is available**

Run:

```powershell
$python = Get-Command py -ErrorAction SilentlyContinue
if ($null -ne $python) {
    py -3 -c "from pathlib import Path; p=Path(r'D:\Debug\4月18日更新\Server\Scripts\Npc\雪原活动管理员.py'); compile(p.read_text(encoding='utf-8'), str(p), 'exec'); print('PYTHON SYNTAX: PASS')"
} else {
    Write-Host 'PYTHON SYNTAX: SKIPPED (py launcher unavailable)'
}
```

Expected when available: `PYTHON SYNTAX: PASS`; the script is source-only and does not require live server globals for this parse check.

Execution result: skipped because `py` is unavailable and `python` resolves only to `C:\Users\chen\AppData\Local\Microsoft\WindowsApps\python.exe`, which is not a working interpreter.

- [x] **Step 3: Confirm only the approved script changed and the alternate copy stayed unchanged**

Run:

```powershell
$targetHash = (Get-FileHash -LiteralPath 'D:\Debug\4月18日更新\Server\Scripts\Npc\雪原活动管理员.py' -Algorithm SHA256).Hash
$alternateHash = (Get-FileHash -LiteralPath 'D:\Debug\4月18日更新\Server\Scripts888\Npc\雪原活动管理员.py' -Algorithm SHA256).Hash
Write-Host "TARGET SHA256: $targetHash"
Write-Host "SCRIPTS888 SHA256: $alternateHash"
if ($alternateHash -ne '2E4C3E28AA05A01441D26DDD8F57CDE0963F2010F767234DC6F9DD7248A8B823') { exit 1 }
if ($targetHash -eq '2E4C3E28AA05A01441D26DDD8F57CDE0963F2010F767234DC6F9DD7248A8B823') { exit 1 }
Write-Host 'SCOPE HASH CHECK: PASS'
```

Expected: the target hash differs because of the approved change, `Scripts888` remains at its pre-edit hash, and `SCOPE HASH CHECK: PASS` is printed. Also inspect the changed `Menu == 1` range with:

```powershell
$lines = Get-Content -LiteralPath 'D:\Debug\4月18日更新\Server\Scripts\Npc\雪原活动管理员.py' -Encoding UTF8
for ($i = 30; $i -le 114; $i++) { '{0,4}: {1}' -f ($i + 1), $lines[$i] }
```

### Task 4: Hand off runtime acceptance without deployment

**Files:**
- Runtime target for the user to copy: `D:\Debug\4月18日更新\Server\Scripts\Npc\雪原活动管理员.py`

- [ ] **Step 1: Copy the verified file to the server's actual `Server\Scripts` directory and restart the script host**

This step is intentionally not performed by Codex because the user has not authorized deployment or restart.

- [ ] **Step 2: Test the approved behavior in the running server**

Use this acceptance matrix:

| Case | Expected result |
| --- | --- |
| Qualified solo player | Creates the snowfield instance, charges 100 gold and 2 crystals once, and teleports the player to `(90,121)`. |
| Solo player missing any existing requirement | Refuses entry and does not create/charge/teleport. |
| Qualified group leader | Existing group flow remains available and checks every member. |
| Qualified group non-leader | Still receives “不是队长”. |
| Server restart/import | `Npc.雪原活动管理员` loads without a script import error. |

Static contract and syntax checks do not prove that the deployed server loaded the file or that live map creation succeeded; report those as separate runtime evidence.
