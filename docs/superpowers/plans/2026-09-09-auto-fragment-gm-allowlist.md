# 自动分解 GM 白名单实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在不改变手动 NPC 分解和现有分解公式的前提下，为宠物包自动分解增加由 GM 手工维护的 `ItemInfo.Index` 白名单，并用当前实际 `System.db` 一次性生成初始冻结名单。

**Architecture:** 自动分解函数在现有实例级保护和 `CanFragment()` 规则之外增加一道 Index 准入检查。白名单存放在独立 IronPython 配置模块中；模块缺失、语法错误或导出对象类型错误时使用空字典并只在模块加载时记录一次错误。初始名单由只读诊断工具从活动数据库的隔离副本生成，安装后不再自动同步数据库。

**Tech Stack:** IronPython 2.7、C#/.NET 8 诊断控制台、MirDB `Session`、PowerShell 5.1 契约测试、现有 IronPython 烟雾测试。

## Global Constraints

- 实际运行脚本范围只允许：`D:\Debug\4月18日更新\Server\Scripts`；不得改 `Scripts888`、旧脚本副本、客户端或数据库。
- 只改变自动分解；手动 NPC 分解、费用、碎片类型/数量、定时周期和玩家个人开关全部保持不变。
- 白名单唯一生效键是 `ItemInfo.Index`；名称和注释只供 GM 阅读。
- 新物品默认拒绝；不得加入按稀有度、类型、等级或名称自动放行的运行时规则。
- 白名单加载失败必须 fail closed：空名单、一次加载日志、每秒扫描不刷日志。
- 首次快照只读活动 `D:\Debug\4月18日更新\Server\Database\System.db` 的隔离副本；不得由生成工具保存数据库。
- 当前工作区不是 Git 仓库，不执行 commit、checkout 或 reset。实施前对两个运行脚本做带时间戳备份，验收记录 SHA-256。
- 所有源码和配置编辑使用 `apply_patch`；生成工具只可直接写 `.artifacts` 下的候选产物，运行配置必须经人工查看后再用 `apply_patch` 安装。
- 静态测试不等于在线验收。未经单独授权，不重载脚本、不重启服务器、不执行在线物品测试。

---

## File Map

**运行文件**

- Create: `D:\Debug\4月18日更新\Server\Scripts\Npc\其他\自动分解配置.py`
- Modify: `D:\Debug\4月18日更新\Server\Scripts\Npc\其他\便捷传送.py`

**测试与一次性工具**

- Modify: `D:\相聚假人\Source\.diagnostics\test_pet_fragment_contract.ps1`
- Modify: `D:\相聚假人\Source\.diagnostics\PetFragmentSmoke\pet_fragment_smoke.py`
- Create: `D:\相聚假人\Source\.diagnostics\AutoFragmentAllowlistSnapshot\AutoFragmentAllowlistSnapshot.csproj`
- Create: `D:\相聚假人\Source\.diagnostics\AutoFragmentAllowlistSnapshot\Program.cs`
- Create: `D:\相聚假人\Source\.diagnostics\test_auto_fragment_allowlist_snapshot.ps1`
- Modify: `D:\相聚假人\Source\CHANGELOG.md`

**只读输入与暂存产物**

- Read only: `D:\Debug\4月18日更新\Server\Database\System.db`
- Generated: `D:\相聚假人\Source\.artifacts\auto-fragment-allowlist-snapshot\Database\System.db`
- Generated: `D:\相聚假人\Source\.artifacts\auto-fragment-allowlist-snapshot\自动分解配置.generated.py`

---

### Task 1: 固化现状并先写失败测试

**Files:**

- Modify: `.diagnostics\test_pet_fragment_contract.ps1`
- Modify: `.diagnostics\PetFragmentSmoke\pet_fragment_smoke.py`
- Test: `.diagnostics\test_pet_fragment_contract.ps1`
- Test: `.diagnostics\PetFragmentSmoke\PetFragmentSmoke.csproj`

- [ ] **Step 1: 记录运行文件基线和备份**

在已获得实施授权后执行；备份目标是明确的两个文件，不能递归复制目录：

```powershell
$stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$script = 'D:\Debug\4月18日更新\Server\Scripts\Npc\其他\便捷传送.py'
$config = 'D:\Debug\4月18日更新\Server\Scripts\Npc\其他\自动分解配置.py'
Get-FileHash -Algorithm SHA256 -LiteralPath $script
Copy-Item -LiteralPath $script -Destination ($script + '.bak-' + $stamp + '-auto-fragment-allowlist')
if (Test-Path -LiteralPath $config) {
    Get-FileHash -Algorithm SHA256 -LiteralPath $config
    Copy-Item -LiteralPath $config -Destination ($config + '.bak-' + $stamp + '-auto-fragment-allowlist')
}
```

- [ ] **Step 2: 扩展契约测试，要求独立配置和 fail-closed 导入**

在 `test_pet_fragment_contract.ps1` 中固定活动根目录为 `D:\Debug\4月18日更新`，新增 `$allowlistPath`，并断言：

```powershell
$allowlistPath = Join-Path $scriptsRoot 'Npc\其他\自动分解配置.py'
if (-not (Test-Path -LiteralPath $allowlistPath)) {
    throw 'missing auto fragment allowlist config'
}

$allowlist = Get-Content -LiteralPath $allowlistPath -Raw -Encoding UTF8
foreach ($token in @(
    '(?m)^AUTO_FRAGMENT_ALLOWLIST\s*=\s*\{',
    '只有此表中的 ItemInfo\.Index 才能自动分解',
    '修改后必须完整重载服务器脚本或重启服务端'
)) {
    if ($allowlist -notmatch $token) { throw "missing allowlist token: $token" }
}

foreach ($token in @(
    'from Npc\.其他\.自动分解配置 import AUTO_FRAGMENT_ALLOWLIST',
    'except Exception as e:',
    'AUTO_FRAGMENT_ALLOWLIST\s*=\s*\{\}',
    '自动分解白名单加载失败',
    'int\(item\.Info\.Index\) not in AUTO_FRAGMENT_ALLOWLIST'
)) {
    if ($npc -notmatch $token) { throw "missing fail-closed allowlist token: $token" }
}
```

保留现有全部断言，不删除对绑定、任务标记、实例保护、费用和碎片行为的覆盖。

- [ ] **Step 3: 扩展烟雾测试，区分名单内外**

把 `_Info` 和 `_Item` 改为显式携带 Index：

```python
class _Info(object):
    def __init__(self, rarity, name, index=0):
        self.Rarity = rarity
        self.ItemName = name
        self.Index = index

class _Item(object):
    def __init__(self, rarity, cost, fragments, flags=0, count=1,
                 name="equipment", index=0):
        self.Info = _Info(rarity, name, index)
        self.Flags = flags
        self.Count = count
        self._cost = cost
        self._fragments = fragments
        self.deleted = False
```

在构造测试物品前加入：

```python
AUTO_FRAGMENT_ALLOWLIST = {
    1001: u"eligible",
    1002: u"stacked",
    1003: u"bound",
    1004: u"quest",
    1005: u"locked",
}
```

给现有五件装备分别传入 1001–1005；新增一件完全满足旧规则但 Index 为 9999 的 `not_allowed`，断言它仍留在宠物包。现有允许项结果必须继续为 `(4, 500, 30)`。再增加空白名单用例：

```python
AUTO_FRAGMENT_ALLOWLIST = {}
denied = _Item(Rarity.Elite, 100, 7, index=2001)
denied_sender = _Sender([denied], 1000)
assert ExecuteCompanionFragmentForSender(denied_sender) == (0, 0, 0)
assert denied_sender.Companion.Inventory[0] is denied
assert denied_sender.Gold == 1000
```

- [ ] **Step 4: 运行 RED 验证**

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .diagnostics\test_pet_fragment_contract.ps1
dotnet run --project .diagnostics\PetFragmentSmoke\PetFragmentSmoke.csproj -- "D:\Debug\4月18日更新\Server\Scripts\Npc\其他\便捷传送.py" ".diagnostics\PetFragmentSmoke\pet_fragment_smoke.py"
```

预期：契约因配置文件/导入/准入判断尚不存在而失败；烟雾测试因名单外物品仍被处理而失败。若测试意外通过，先修正测试，不进入生产改动。

---

### Task 2: 实现最小的运行时白名单门禁

**Files:**

- Create: `D:\Debug\4月18日更新\Server\Scripts\Npc\其他\自动分解配置.py`
- Modify: `D:\Debug\4月18日更新\Server\Scripts\Npc\其他\便捷传送.py`
- Test: `.diagnostics\test_pet_fragment_contract.ps1`
- Test: `.diagnostics\PetFragmentSmoke\PetFragmentSmoke.csproj`

- [ ] **Step 1: 新建可人工维护的空配置骨架**

先用 `apply_patch` 创建以下内容；初始数据库名单在 Task 4 安装：

```python
# -*- coding: utf-8 -*-

# 只有此表中的 ItemInfo.Index 才能自动分解。
# 冒号左侧 Index 是唯一生效值；名称和注释只供 GM 核对。
# 删除整行表示禁止；新增一行表示允许；每行必须保留结尾逗号。
# 修改后必须完整重载服务器脚本或重启服务端。

AUTO_FRAGMENT_ALLOWLIST = {
}
```

- [ ] **Step 2: 在模块加载处安全导入**

紧跟现有 `回收配置` 导入之后加入：

```python
try:
    from Npc.其他.自动分解配置 import AUTO_FRAGMENT_ALLOWLIST
    if not isinstance(AUTO_FRAGMENT_ALLOWLIST, dict):
        raise TypeError("AUTO_FRAGMENT_ALLOWLIST must be a dict")
except Exception as e:
    AUTO_FRAGMENT_ALLOWLIST = {}
    SEnvir.Log("自动分解白名单加载失败，已禁止全部自动分解: {}".format(e))
```

这段代码只在脚本模块加载时执行；不得把日志放进每秒循环，不得在异常时继续沿用旧的全量规则。

- [ ] **Step 3: 在自动分解候选处增加 Index 门禁**

把原来的组合判断：

```python
        if skip_item or not item.CanFragment():
            continue
```

最小拆分为：

```python
        if skip_item:
            continue
        if int(item.Info.Index) not in AUTO_FRAGMENT_ALLOWLIST:
            continue
        if not item.CanFragment():
            continue
```

不得修改此函数的其他扣费、产物、堆叠、空间和通知逻辑。

- [ ] **Step 4: 运行 GREEN 验证**

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .diagnostics\test_pet_fragment_contract.ps1
dotnet run --project .diagnostics\PetFragmentSmoke\PetFragmentSmoke.csproj -- "D:\Debug\4月18日更新\Server\Scripts\Npc\其他\便捷传送.py" ".diagnostics\PetFragmentSmoke\pet_fragment_smoke.py"
```

预期两项通过，并且原有 `(4, 500, 30)`、绑定/任务标记、锁定保护和金币不足断言不变。

---

### Task 3: 建立一次性、确定性的初始名单生成器

**Files:**

- Create: `.diagnostics\AutoFragmentAllowlistSnapshot\AutoFragmentAllowlistSnapshot.csproj`
- Create: `.diagnostics\AutoFragmentAllowlistSnapshot\Program.cs`
- Create: `.diagnostics\test_auto_fragment_allowlist_snapshot.ps1`

- [ ] **Step 1: 先写生成器契约测试**

测试脚本必须验证：项目和程序存在；程序源码包含七种允许类型、Common 的 `RequiredAmount > 15`、Superior/Elite、按 `Rarity/ItemType/Index` 排序、重复 Index 拒绝、UTF-8 BOM 输出和每行结尾逗号。核心断言：

```powershell
$programPath = Join-Path $PSScriptRoot 'AutoFragmentAllowlistSnapshot\Program.cs'
$source = Get-Content -LiteralPath $programPath -Raw -Encoding UTF8
foreach ($token in @(
    'ItemType\.Weapon', 'ItemType\.Armour', 'ItemType\.Helmet',
    'ItemType\.Necklace', 'ItemType\.Bracelet', 'ItemType\.Ring', 'ItemType\.Shoes',
    'item\.Rarity == Rarity\.Common && item\.RequiredAmount > 15',
    'item\.Rarity == Rarity\.Superior', 'item\.Rarity == Rarity\.Elite',
    'OrderBy\(item => item\.Rarity\)', 'ThenBy\(item => item\.ItemType\)',
    'ThenBy\(item => item\.Index\)', 'duplicate ItemInfo\.Index',
    'new UTF8Encoding\(true\)'
)) {
    if ($source -notmatch $token) { throw "missing snapshot generator token: $token" }
}
```

先运行并确认因文件不存在而失败：

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .diagnostics\test_auto_fragment_allowlist_snapshot.ps1
```

- [ ] **Step 2: 创建 .NET 8 项目**

```xml
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <OutputType>Exe</OutputType>
    <TargetFramework>net8.0</TargetFramework>
    <ImplicitUsings>enable</ImplicitUsings>
    <Nullable>disable</Nullable>
  </PropertyGroup>
  <ItemGroup>
    <ProjectReference Include="..\..\ServerLibrary\ServerLibrary.csproj" />
  </ItemGroup>
</Project>
```

- [ ] **Step 3: 实现只读生成逻辑**

`Program.cs` 使用 `MirDB.Session` 读取传入目录，禁止保存：

```csharp
using System.Text;
using Library;
using Library.SystemModels;
using MirDB;

if (args.Length != 2)
    throw new ArgumentException("expected database root and output config path");

string databaseRoot = Path.GetFullPath(args[0]);
string outputPath = Path.GetFullPath(args[1]);
string systemPath = Path.Combine(databaseRoot, "System.db");
if (!File.Exists(systemPath))
    throw new FileNotFoundException("System.db was not found", systemPath);

string root = databaseRoot.TrimEnd(Path.DirectorySeparatorChar, Path.AltDirectorySeparatorChar)
              + Path.DirectorySeparatorChar;
string backup = Path.Combine(databaseRoot, "UnusedBackup") + Path.DirectorySeparatorChar;

var allowedTypes = new HashSet<ItemType>
{
    ItemType.Weapon, ItemType.Armour, ItemType.Helmet, ItemType.Necklace,
    ItemType.Bracelet, ItemType.Ring, ItemType.Shoes,
};

using var session = new Session(
    SessionMode.ServerTool,
    new[] { typeof(ItemInfo).Assembly },
    false,
    "",
    root,
    backup)
{
    BackUp = false,
};
session.Init();

bool IsOriginallyFragmentable(ItemInfo item) =>
    item != null &&
    allowedTypes.Contains(item.ItemType) &&
    ((item.Rarity == Rarity.Common && item.RequiredAmount > 15) ||
     item.Rarity == Rarity.Superior ||
     item.Rarity == Rarity.Elite);

var items = session.GetCollection<ItemInfo>()
    .Where(IsOriginallyFragmentable)
    .OrderBy(item => item.Rarity)
    .ThenBy(item => item.ItemType)
    .ThenBy(item => item.Index)
    .ToList();

var duplicate = items.GroupBy(item => item.Index).FirstOrDefault(group => group.Count() > 1);
if (duplicate != null)
    throw new InvalidDataException($"duplicate ItemInfo.Index: {duplicate.Key}");

static string EscapePythonString(string value) => (value ?? "")
    .Replace("\\", "\\\\")
    .Replace("\"", "\\\"")
    .Replace("\r", "\\r")
    .Replace("\n", "\\n");

var lines = new List<string>
{
    "# -*- coding: utf-8 -*-",
    "",
    "# 只有此表中的 ItemInfo.Index 才能自动分解。",
    "# 冒号左侧 Index 是唯一生效值；名称和注释只供 GM 核对。",
    "# 删除整行表示禁止；新增一行表示允许；每行必须保留结尾逗号。",
    "# 修改后必须完整重载服务器脚本或重启服务端。",
    "",
    "AUTO_FRAGMENT_ALLOWLIST = {",
};

Rarity? currentRarity = null;
foreach (ItemInfo item in items)
{
    if (currentRarity != item.Rarity)
    {
        if (currentRarity != null) lines.Add("");
        currentRarity = item.Rarity;
        lines.Add($"    # {item.Rarity}");
    }
    lines.Add($"    {item.Index}: u\"{EscapePythonString(item.ItemName)}\", " +
              $"# {item.ItemType} | RequiredAmount={item.RequiredAmount}");
}
lines.Add("}");
lines.Add("");

Directory.CreateDirectory(Path.GetDirectoryName(outputPath)!);
File.WriteAllLines(outputPath, lines, new UTF8Encoding(true));
Console.WriteLine($"generated {items.Count} entries: {outputPath}");
```

如果编译器对顶级语句中的局部函数位置报错，只移动 `IsOriginallyFragmentable` 的声明位置；不得改变筛选谓词。

- [ ] **Step 4: 完成生成器测试并构建**

在契约脚本末尾运行项目构建，并要求退出码为 0：

```powershell
& dotnet build (Join-Path $PSScriptRoot 'AutoFragmentAllowlistSnapshot\AutoFragmentAllowlistSnapshot.csproj') --configuration Debug
if ($LASTEXITCODE -ne 0) { throw 'snapshot generator build failed' }
Write-Output 'auto fragment allowlist snapshot contract passed'
```

执行：

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .diagnostics\test_auto_fragment_allowlist_snapshot.ps1
```

---

### Task 4: 从当前活动数据库生成并安装冻结初始名单

**Files:**

- Read only: `D:\Debug\4月18日更新\Server\Database\System.db`
- Generate: `.artifacts\auto-fragment-allowlist-snapshot\Database\System.db`
- Generate: `.artifacts\auto-fragment-allowlist-snapshot\自动分解配置.generated.py`
- Modify: `D:\Debug\4月18日更新\Server\Scripts\Npc\其他\自动分解配置.py`

- [ ] **Step 1: 创建隔离副本并核对哈希**

```powershell
$sourceDb = 'D:\Debug\4月18日更新\Server\Database\System.db'
$artifactRoot = 'D:\相聚假人\Source\.artifacts\auto-fragment-allowlist-snapshot'
$snapshotDbRoot = Join-Path $artifactRoot 'Database'
New-Item -ItemType Directory -Force -Path $snapshotDbRoot | Out-Null
Copy-Item -LiteralPath $sourceDb -Destination (Join-Path $snapshotDbRoot 'System.db') -Force
$sourceHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $sourceDb).Hash
$copyHash = (Get-FileHash -Algorithm SHA256 -LiteralPath (Join-Path $snapshotDbRoot 'System.db')).Hash
if ($sourceHash -ne $copyHash) { throw 'isolated System.db hash mismatch' }
"System.db SHA256=$sourceHash"
```

执行前再次确认 `D:\Debug\4月18日更新\Server\Server.ini` 仍为 `MySqlEnable=False`、`EnableDBEncryption=False`；若任一值变化，停止，不按本计划猜测数据库来源或密钥。

- [ ] **Step 2: 连续生成两次并证明输出确定**

```powershell
$project = 'D:\相聚假人\Source\.diagnostics\AutoFragmentAllowlistSnapshot\AutoFragmentAllowlistSnapshot.csproj'
$generated = Join-Path $artifactRoot '自动分解配置.generated.py'
$generated2 = Join-Path $artifactRoot '自动分解配置.generated.second.py'
dotnet run --project $project -- $snapshotDbRoot $generated
if ($LASTEXITCODE -ne 0) { throw 'first allowlist generation failed' }
dotnet run --project $project -- $snapshotDbRoot $generated2
if ($LASTEXITCODE -ne 0) { throw 'second allowlist generation failed' }
if ((Get-FileHash $generated).Hash -ne (Get-FileHash $generated2).Hash) {
    throw 'allowlist generation is not deterministic'
}
```

- [ ] **Step 3: 检查语法、重复 Index 和基本数量**

```powershell
$python27 = 'C:\Python27\python.exe'
& $python27 -c "import sys; compile(open(sys.argv[1], 'rb').read(), sys.argv[1], 'exec')" $generated
if ($LASTEXITCODE -ne 0) { throw 'generated allowlist is not valid Python 2.7' }

$ids = Select-String -LiteralPath $generated -Pattern '^\s*(\d+)\s*:' |
    ForEach-Object { [int]$_.Matches[0].Groups[1].Value }
if ($ids.Count -eq 0) { throw 'generated allowlist is empty' }
$duplicates = $ids | Group-Object | Where-Object Count -gt 1
if ($duplicates) { throw "duplicate generated Index: $($duplicates.Name -join ',')" }
"generated entry count=$($ids.Count)"
```

人工查看 Common、Superior、Elite 三个分组和若干已知高级装备。这里不能宣称“安全上线”：完整旧规则快照仍包含当前数据库中原本可分解的高级装备，GM 应先删除明确需要保护的行。

- [ ] **Step 4: 用 apply_patch 安装生成内容**

读取 `.artifacts\auto-fragment-allowlist-snapshot\自动分解配置.generated.py` 全文，经 GM 审阅后，用 `apply_patch` 替换运行配置的空字典。不得用 `Copy-Item` 直接覆盖运行配置。

安装后比较生成文件和运行配置的有效 Index 集合：

```powershell
$activeConfig = 'D:\Debug\4月18日更新\Server\Scripts\Npc\其他\自动分解配置.py'
$generatedIds = Select-String -LiteralPath $generated -Pattern '^\s*(\d+)\s*:' |
    ForEach-Object { [int]$_.Matches[0].Groups[1].Value }
$activeIds = Select-String -LiteralPath $activeConfig -Pattern '^\s*(\d+)\s*:' |
    ForEach-Object { [int]$_.Matches[0].Groups[1].Value }
$difference = Compare-Object $generatedIds $activeIds
if ($difference) { throw 'active initial allowlist differs from reviewed snapshot' }
```

如果 GM 在安装前删掉保护项，则把这些删除项单独列成“GM 审阅排除清单”，比较时允许且只允许这些 Index 缺失，不能静默接受其他差异。

---

### Task 5: 全量静态回归、维护说明和验收边界

**Files:**

- Modify: `CHANGELOG.md`
- Test: 所有本计划涉及的脚本和现有周期回调测试

- [ ] **Step 1: 运行 IronPython 2.7 语法检查**

```powershell
$python27 = 'C:\Python27\python.exe'
& $python27 -c "import sys; [compile(open(p, 'rb').read(), p, 'exec') for p in sys.argv[1:]]" `
  'D:\Debug\4月18日更新\Server\Scripts\Npc\其他\自动分解配置.py' `
  'D:\Debug\4月18日更新\Server\Scripts\Npc\其他\便捷传送.py'
if ($LASTEXITCODE -ne 0) { throw 'IronPython 2.7 syntax check failed' }
```

- [ ] **Step 2: 运行相关契约和烟雾回归**

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .diagnostics\test_pet_fragment_contract.ps1
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .diagnostics\test_pet_fragment_schedule_contract.ps1
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .diagnostics\test_pet_recycle_contract.ps1
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .diagnostics\test_auto_fragment_allowlist_snapshot.ps1
dotnet run --project .diagnostics\PetFragmentSmoke\PetFragmentSmoke.csproj -- "D:\Debug\4月18日更新\Server\Scripts\Npc\其他\便捷传送.py" ".diagnostics\PetFragmentSmoke\pet_fragment_smoke.py"
```

全部命令必须退出码 0。失败时只修复与本任务直接相关的测试或代码，不顺手改其他回收/传送逻辑。

- [ ] **Step 3: 记录变更证据**

在 `CHANGELOG.md` 增加一条简短记录，包含：运行配置路径、自动分解脚本路径、初始白名单条目数、源 `System.db` SHA-256、两个运行脚本最终 SHA-256、通过的命令，以及“尚未执行脚本重载/在线验收”。

```powershell
Get-FileHash -Algorithm SHA256 -LiteralPath `
  'D:\Debug\4月18日更新\Server\Scripts\Npc\其他\自动分解配置.py', `
  'D:\Debug\4月18日更新\Server\Scripts\Npc\其他\便捷传送.py'
```

- [ ] **Step 4: 交付 GM 日常操作说明**

交付说明必须明确：

1. 允许：在对应稀有度分组新增 `Index: u"名称", # 类型 | RequiredAmount=数值` 一行。
2. 禁止：删除对应整行；不要只改名称。
3. 每行保留逗号；保存后先跑 Python 2.7 语法检查。
4. 文件保存不会自动改变已加载模块；必须完整重载脚本或重启服务端。
5. 重载后用一次性测试装备各验证一个允许项和一个禁止项。
6. 未来数据库新增装备不会自动进入名单，必须由 GM 手工加入。

- [ ] **Step 5: 在线验收仅在单独授权后执行**

在线验收成功标准：名单内合法测试装备被自动分解；名单外合法测试装备保留；锁定名单内装备保留；金币与碎片数量符合旧规则；日志无每秒重复错误。若未获得重载/重启和测试物品授权，最终报告必须停在“静态与烟雾验证通过，在线验收待执行”。

