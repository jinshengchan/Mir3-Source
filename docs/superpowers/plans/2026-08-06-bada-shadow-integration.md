# 八大暗影脚本接入实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将外部八大暗影副本脚本接入当前 `Server\Scripts` 自动加载链路，并把入口/层费用改为真正扣除 500/50 元宝。

**Architecture:** 复用现有 `Npc.BOSS副本` 包的自动导入机制，不新增根级加载入口。脚本主体保持原样，仅做费用函数与数值的必要改动；每层开始时检查并扣除元宝，入口失败使用现有元宝退款函数。

**Tech Stack:** IronPython 2.7 服务端脚本、PowerShell 5.1 契约测试、现有 `Globals.py` 元宝函数。

## Global Constraints

- 目标脚本系统固定为 `D:\Debug\4月18日更新\Server\Scripts`。
- 严格保留 NPC=5656、地图=387、原菜单/怪物/奖励/次数/并发配置。
- 入口费用为 500 元宝，每层费用为 50 元宝。
- 修改前只备份将被覆盖的文件；不覆盖 `Scripts888` 或无关文件。
- 所有变更写入 `CHANGELOG.md`，不生成客户端产物。

---

### Task 1: 建立失败契约测试

**Files:**
- Create: `.diagnostics/test_bada_shadow_contract.ps1`

**Interfaces:**
- Consumes: `D:\Debug\4月18日更新\Server\Scripts\Npc\BOSS副本`
- Produces: 对目标脚本路径、包导入、事件注册、费用函数和 Python 语法的可重复检查。

- [x] **Step 1: Write the failing test**

  创建以下测试脚本；中文文件名由 Unicode code point 在运行时构造，避免 Windows PowerShell 5.1 按本地代码页解析测试源码：

  ```powershell
  $ErrorActionPreference = 'Stop'
  $serverRoot = Get-ChildItem -LiteralPath 'D:\Debug' -Directory |
      Where-Object { $_.Name -like '4*' } |
      Select-Object -First 1 -ExpandProperty FullName
  if (-not $serverRoot) { throw 'server root not found' }
  $bossDir = Join-Path $serverRoot 'Server\Scripts\Npc\BOSS副本'
  $moduleName = -join ([char]0x516B,[char]0x5927,[char]0x6697,[char]0x5F71)
  $yuanbao = -join ([char]0x5143,[char]0x5B9D)
  $target = Join-Path $bossDir ($moduleName + '.py')
  if (-not (Test-Path -LiteralPath $target)) { throw "target missing: $target" }
  $content = Get-Content -LiteralPath $target -Raw -Encoding UTF8
  $init = Get-Content -LiteralPath (Join-Path $bossDir '__init__.py') -Raw -Encoding UTF8
  if ($init.IndexOf(('import Npc.BOSS副本.' + $moduleName), [StringComparison]::Ordinal) -lt 0) { throw 'BOSS package import missing' }
  foreach ($token in @('BADA_FUBEN_MAP_INDEX = 387','NpcEvent.add_listener(5656','BADA_ENTER_COST = ("' + $yuanbao + '", 500)','BADA_LEVEL_COST = ("' + $yuanbao + '", 50)','SubGameGold(player, BADA_ENTER_COST[1])','SubGameGold(player, BADA_LEVEL_COST[1])','GiveGameGold(player, BADA_ENTER_COST[1])')) {
      if ($content.IndexOf($token, [StringComparison]::Ordinal) -lt 0) { throw "missing token: $token" }
  }
  & 'C:\Python27\python.exe' -c "import sys; compile(open(sys.argv[1], 'rb').read(), sys.argv[1], 'exec')" $target
  if ($LASTEXITCODE -ne 0) { throw 'Python 2.7 syntax check failed' }
  Write-Output 'bada shadow contract passed'
  ```

- [x] **Step 2: Run test to verify it fails**

  Run: `powershell -NoProfile -ExecutionPolicy Bypass -File D:\相聚假人\Source\.diagnostics\test_bada_shadow_contract.ps1`

  Expected: FAIL，提示目标八大暗影脚本尚未接入。

### Task 2: 备份并接入脚本

**Files:**
- Create: `D:\Debug\4月18日更新\Server\Scripts\Npc\BOSS副本\八大暗影.py`
- Modify: `D:\Debug\4月18日更新\Server\Scripts\Npc\BOSS副本\__init__.py`
- Backup: 同目录 `__init__.py.bak-20260806-bada-shadow`

**Interfaces:**
- Consumes: `D:\Video\八大暗影.py`、`Globals.SubGameGold`、`Globals.GiveGameGold`。
- Produces: 可由 `Npc` 包加载并注册 NPC/地图事件的八大暗影模块。

- [x] **Step 1: Back up the existing package initializer**

  仅复制 `BOSS副本\__init__.py` 为带时间标签的备份；目标八大暗影文件不存在，不覆盖任何同名脚本。

- [x] **Step 2: Copy the source script into the target package**

  将 `D:\Video\八大暗影.py` 复制为目标文件，然后只修改入口/层费用数值、入口扣费/退款函数和层费用检查。

- [x] **Step 3: Add the package import**

  在 BOSS 包初始化文件末尾增加 `import Npc.BOSS副本.八大暗影`，不调整既有导入顺序。

- [x] **Step 4: Apply only the requested fee changes**

  将入口配置改为 `BADA_ENTER_COST = ("元宝", 500)`，层配置改为 `BADA_LEVEL_COST = ("元宝", 50)`；入口扣费改为检查 `player.GameGold` 并调用 `SubGameGold(player, BADA_ENTER_COST[1])`，入口失败和队列已满的退款改为 `GiveGameGold(player, BADA_ENTER_COST[1])`。

  在 `InitNewLevel(args)` 取得 `player` 后、清理地图怪物前加入以下最小检查；不足时不生成该层并沿原回城流程退出：

  ```python
  if not hasattr(player, 'GameGold') or int(player.GameGold or 0) < BADA_LEVEL_COST[1]:
      player.Connection.ReceiveChat("元宝不足，无法进入本层副本。", MessageType.System)
      TeleportBackToTown(player)
      return
  SubGameGold(player, BADA_LEVEL_COST[1])
  ```

### Task 3: 运行契约与静态验证

**Files:**
- Test: `.diagnostics/test_bada_shadow_contract.ps1`

**Interfaces:**
- Consumes: Task 2 的目标模块和包初始化文件。
- Produces: 通过的导入、费用和语法检查结果。

- [x] **Step 1: Run the contract test**

  Run: `powershell -NoProfile -ExecutionPolicy Bypass -File D:\相聚假人\Source\.diagnostics\test_bada_shadow_contract.ps1`

  Expected: PASS；同时 Python 2.7 `compile()` 返回成功。

- [x] **Step 2: Review the exact diff scope**

  确认只有目标脚本、BOSS 包初始化、契约测试、设计/计划文档、更新日志和备份文件发生变化。

### Task 4: 更新日志与交付说明

**Files:**
- Modify: `CHANGELOG.md`
- Backup: `CHANGELOG.md.bak-20260806-bada-shadow`

**Interfaces:**
- Consumes: Task 2/3 的路径、费用和验证结果。
- Produces: 可回溯的接入记录和服务端重新加载说明。

- [x] **Step 1: Back up and prepend the changelog entry**

  记录源文件、目标文件、NPC/地图编号、500/50 元宝规则、未修改范围、验证命令和备份路径。

- [x] **Step 2: Report reload requirement**

  说明脚本文件接入后需要在服务端执行“重新加载脚本”或安全重启；不代替用户重启正在运行的服务端。
