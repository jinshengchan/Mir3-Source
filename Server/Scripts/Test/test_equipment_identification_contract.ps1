$ErrorActionPreference = 'Stop'

function Assert-Contract {
    param(
        [bool]$Condition,
        [string]$Message
    )

    if (-not $Condition) {
        throw "CONTRACT FAILURE: $Message"
    }
}

function Read-Utf8 {
    param([string]$Path)
    return [System.IO.File]::ReadAllText($Path, [System.Text.Encoding]::UTF8)
}

$scriptRoot = 'D:\Debug\4月18日更新\Server\Scripts'
$sourceRoot = 'D:\相聚假人\Source'
$identifyPath = Join-Path $scriptRoot 'Npc\鉴定稀世装备.py'
$exchangePath = Join-Path $scriptRoot 'Npc\兑换鉴定石.py'
$npcInitPath = Join-Path $scriptRoot 'Npc\__init__.py'
$panyeInitPath = Join-Path $scriptRoot 'Npc\潘夜岛\__init__.py'
$managerPath = Join-Path $scriptRoot 'Npc\管理中心.py'

Assert-Contract (Test-Path -LiteralPath $identifyPath) '缺少鉴定稀世装备.py'
Assert-Contract (Test-Path -LiteralPath $exchangePath) '缺少兑换鉴定石.py'

$identifyText = Read-Utf8 $identifyPath
$exchangeText = Read-Utf8 $exchangePath
$npcInit = Read-Utf8 $npcInitPath
$panyeInit = Read-Utf8 $panyeInitPath
$manager = Read-Utf8 $managerPath

Assert-Contract (([regex]::Matches($npcInit, '(?m)^\s*import Npc\.鉴定稀世装备\s*$')).Count -eq 1) '主入口未恰好导入鉴定模块一次'
Assert-Contract (([regex]::Matches($npcInit, '(?m)^\s*import Npc\.兑换鉴定石\s*$')).Count -eq 1) '主入口未恰好导入兑换模块一次'
Assert-Contract ($panyeInit -notmatch '(?m)^\s*import Npc\.潘夜岛\.钓鱼商俊熙\s*$') '旧钓鱼商俊熙模块仍被潘夜岛入口导入'
Assert-Contract ($panyeInit -notmatch '(?m)^\s*import Npc\.潘夜岛\.钓鱼商秀贤\s*$') '旧钓鱼商秀贤模块仍被潘夜岛入口导入'

Assert-Contract (([regex]::Matches($manager, '(?m)^\s*import Npc\.鉴定稀世装备 as EquipmentIdentification\s*$')).Count -eq 1) '管理中心未显式导入装备鉴定 ASCII 别名'
Assert-Contract (([regex]::Matches($manager, '(?m)^\s*import Npc\.兑换鉴定石 as IdentificationStoneExchange\s*$')).Count -eq 1) '管理中心未显式导入鉴定石兑换 ASCII 别名'

Assert-Contract (([regex]::Matches($identifyText, 'NpcEvent\.add_listener\(\s*215\s*,\s*.*?OnClick\s*\)')).Count -eq 1) 'NPC 215 未恰好注册一次'
Assert-Contract (([regex]::Matches($exchangeText, 'NpcEvent\.add_listener\(\s*216\s*,\s*.*?OnClick\s*\)')).Count -eq 1) 'NPC 216 未恰好注册一次'

Assert-Contract ($manager -match '(?s)Menu\s*==\s*38.*?GetNPCObject\(\s*215\s*\).*?EquipmentIdentification\.OnClick') '管理中心菜单 38 未通过 ASCII 别名调用 NPC 215'
Assert-Contract ($manager -match '(?s)Menu\s*==\s*39.*?GetNPCObject\(\s*216\s*\).*?IdentificationStoneExchange\.OnClick') '管理中心菜单 39 未通过 ASCII 别名调用 NPC 216'
Assert-Contract ($manager -notmatch 'Npc\.鉴定稀世装备\.OnClick') '管理中心仍直接通过 Npc 包属性调用装备鉴定'
Assert-Contract ($manager -notmatch 'Npc\.兑换鉴定石\.OnClick') '管理中心仍直接通过 Npc 包属性调用鉴定石兑换'
Assert-Contract ($manager -match '装备鉴定\s*:\s*38') '管理中心缺少装备鉴定可见入口'
Assert-Contract ($manager -match '鉴定石分解\s*:\s*39') '管理中心缺少鉴定石分解可见入口'

$expectedStones = @(
    '1\s*:\s*.*鉴定石一级',
    '2\s*:\s*.*鉴定石二级',
    '3\s*:\s*.*鉴定石三级',
    '4\s*:\s*.*鉴定石四级',
    '5\s*:\s*.*鉴定石五级'
)
foreach ($pattern in $expectedStones) {
    Assert-Contract ($identifyText -match $pattern) "鉴定等级映射缺少: $pattern"
}
Assert-Contract ($identifyText -match 'RequiredAmount') '鉴定脚本未按 RequiredAmount 读取等级'
Assert-Contract ($identifyText -match 'startswith\(.*未鉴定.*\)') '鉴定脚本未校验未鉴定前缀'
Assert-Contract ($identifyText -match 'ItemInfoList\.Binding') '鉴定脚本未校验成品映射唯一性'
Assert-Contract ($identifyText -match 'Rarity\.Elite') '鉴定脚本未校验稀世成品品质'
Assert-Contract ($identifyText -match 'Sender\.Inventory\[slot\]') '鉴定脚本未按背包槽位读取选择'
Assert-Contract ($identifyText -match 'CanGainItems') '鉴定脚本未检查产物容量'
Assert-Contract ($identifyText -match 'ItemCheck') '鉴定脚本未构造产物容量检查'
Assert-Contract ($identifyText -match 'CreateFreshItem') '鉴定脚本未用现有 API 创建产物'
Assert-Contract ($identifyText -match 'GainItem') '鉴定脚本未用现有 API 发放产物'
Assert-Contract ($identifyText -match 'UserItemFlags\.Bound') '鉴定产物未保留 Bound 标记'
Assert-Contract ($identifyText -match 'UserItemFlags\.Worthless') '鉴定产物未保留 Worthless 标记'
Assert-Contract ($identifyText -match 'TakeItem\(source_item\s*,\s*1\)') '鉴定未精确扣除选中源装备一件'

$identifyOperation = $identifyText.Substring($identifyText.IndexOf('def _identify'))
$identifyGiveIndex = $identifyOperation.IndexOf('if not _give_item')
$identifyTakeIndex = $identifyOperation.IndexOf('TakeItem(source_item')
Assert-Contract ($identifyGiveIndex -ge 0 -and $identifyTakeIndex -gt $identifyGiveIndex) '鉴定必须先发放产物再扣除源装备'
$identifyStoneTakeIndex = $identifyOperation.IndexOf('TakeItem(stone_name')
Assert-Contract ($identifyStoneTakeIndex -gt $identifyGiveIndex) '鉴定必须先发放产物再扣除鉴定石'

$expectedCosts = @(
    @{ Stone = '鉴定石一级'; Fragments = 1; GameGold = 50 },
    @{ Stone = '鉴定石二级'; Fragments = 2; GameGold = 100 },
    @{ Stone = '鉴定石三级'; Fragments = 3; GameGold = 150 },
    @{ Stone = '鉴定石四级'; Fragments = 4; GameGold = 200 },
    @{ Stone = '鉴定石五级'; Fragments = 5; GameGold = 250 }
)
foreach ($cost in $expectedCosts) {
    $costPattern = [regex]::Escape($cost.Stone) + '.*?:\s*\(\s*' + $cost.Fragments + '\s*,\s*' + $cost.GameGold + '\s*\)'
    Assert-Contract ($exchangeText -match $costPattern) "兑换成本不匹配: $($cost.Stone)"
}
Assert-Contract ($exchangeText -match '高级碎片') '兑换脚本未使用高级碎片成本'
Assert-Contract ($exchangeText -match 'GameGold|元宝|SubGameGold') '兑换脚本未使用元宝成本'
Assert-Contract ($exchangeText -match 'CanGainItems') '兑换脚本未检查产物容量'
Assert-Contract ($exchangeText -match 'ItemCheck') '兑换脚本未构造产物容量检查'
Assert-Contract ($exchangeText -match 'CreateFreshItem') '兑换脚本未用现有 API 创建产物'
Assert-Contract ($exchangeText -match 'GainItem') '兑换脚本未用现有 API 发放产物'
Assert-Contract ($exchangeText -match 'GiveItems') '购买鉴定石未使用带成功返回值的现有发放 API'
Assert-Contract ($exchangeText -match 'TakeItem\(source_item\s*,\s*1\)') '分解未精确扣除选中鉴定石一颗'
Assert-Contract ($exchangeText -match 'UserItemFlags\.Bound') '分解产物未保留 Bound 标记'
Assert-Contract ($exchangeText -match 'UserItemFlags\.Worthless') '分解产物未保留 Worthless 标记'
$purchaseOperation = $exchangeText.Substring($exchangeText.IndexOf('def _purchase'))
$purchaseGiveIndex = $purchaseOperation.IndexOf('if not sender.GiveItems')
$purchaseGoldIndex = $purchaseOperation.IndexOf('SubGameGold')
$purchaseFragmentIndex = $purchaseOperation.IndexOf('TakeItem(u"高级碎片"')
Assert-Contract ($purchaseGiveIndex -ge 0 -and $purchaseGoldIndex -gt $purchaseGiveIndex -and $purchaseFragmentIndex -gt $purchaseGiveIndex) '购买鉴定石必须先发放产物再扣除成本'
$decomposeOperation = $exchangeText.Substring($exchangeText.IndexOf('def _decompose'))
$decomposeGiveIndex = $decomposeOperation.IndexOf('if not _give_item')
$decomposeTakeIndex = $decomposeOperation.IndexOf('TakeItem(source_item')
Assert-Contract ($decomposeGiveIndex -ge 0 -and $decomposeTakeIndex -gt $decomposeGiveIndex) '分解必须先发放低级石再扣除高级石'
Assert-Contract ($exchangeText -match '鉴定石五级.*?:\s*.*鉴定石四级') '缺少五级到四级 1:1 分解'
Assert-Contract ($exchangeText -match '鉴定石四级.*?:\s*.*鉴定石三级') '缺少四级到三级 1:1 分解'
Assert-Contract ($exchangeText -match '鉴定石三级.*?:\s*.*鉴定石二级') '缺少三级到二级 1:1 分解'
Assert-Contract ($exchangeText -match '鉴定石二级.*?:\s*.*鉴定石一级') '缺少二级到一级 1:1 分解'
Assert-Contract ($exchangeText -notmatch '鉴定石一级.*?:\s*.*鉴定石') '一级鉴定石不应继续向下分解'

$pythonCandidates = @(
    'C:\Python27\python.exe',
    (Get-Command python.exe -ErrorAction SilentlyContinue).Source
) | Where-Object { $_ -and (Test-Path -LiteralPath $_) }
Assert-Contract ($pythonCandidates.Count -gt 0) '找不到可用的 Python 语法编译器'
$python = $pythonCandidates | Select-Object -First 1
$menuReplayCode = @'
import re
import sys
import types

sys.modules['Globals'] = types.ModuleType('Globals')
sys.modules['System'] = types.ModuleType('System')
sys.modules['NpcEvent'] = types.ModuleType('NpcEvent')
sys.modules['NpcEvent'].add_listener = lambda *args: None
server = types.ModuleType('Server')
server.__path__ = []
envir = types.ModuleType('Server.Envir')
envir.__path__ = []
senvir = types.ModuleType('Server.Envir.SEnvir')
models = types.ModuleType('Server.Models')
models.ItemCheck = object
server.Envir = envir
server.Models = models
envir.SEnvir = senvir
sys.modules['Server'] = server
sys.modules['Server.Envir'] = envir
sys.modules['Server.Envir.SEnvir'] = senvir
sys.modules['Server.Models'] = models

source_path = sys.argv[1]
namespace = {}
source = open(source_path, 'rb').read()
exec(compile(source, source_path, 'exec'), namespace)

class ItemInfo(object):
    ItemName = u'\u672a\u9274\u5b9a\u4fee\u7f57\u6218\u7532'
    RequiredAmount = 1

class Item(object):
    Info = ItemInfo()

class Inventory(object):
    Length = 1
    def __getitem__(self, index):
        if index == 0:
            return Item()
        raise IndexError(index)

class Sender(object):
    Inventory = Inventory()

menu = namespace['_build_item_menu'](Sender())
assert ItemInfo.ItemName in menu
assert namespace['STONE_BY_TIER'][1] in menu
match = re.search(ur'\[(?P<Text>.*?):(?P<ID>.+?)\]', menu, re.S)
assert match is not None
identifier = match.group('ID')
try:
    parsed_id = int(identifier)
except ValueError:
    raise AssertionError('client ID parse failed: %r' % identifier)
assert parsed_id == 1000
assert u'\uff09' not in identifier
'@
& $python -c $menuReplayCode $identifyPath
if ($LASTEXITCODE -ne 0) {
    throw "CONTRACT FAILURE: 客户端菜单 ID 回放退出 $LASTEXITCODE"
}
$compileCode = "import sys; [compile(open(p, 'rb').read(), p, 'exec') for p in sys.argv[1:]]"
& $python -c $compileCode $identifyPath $exchangePath
if ($LASTEXITCODE -ne 0) {
    throw "CONTRACT FAILURE: Python syntax compilation exited $LASTEXITCODE"
}

$packageDlls = Get-ChildItem -LiteralPath (Join-Path $sourceRoot 'packages') -Recurse -File -Filter '*.dll' |
    Where-Object { $_.FullName -match '\\lib\\netstandard2\.0\\' } |
    Group-Object Name |
    ForEach-Object { $_.Group | Select-Object -First 1 }
foreach ($file in $packageDlls) {
    try { [System.Reflection.Assembly]::LoadFrom($file.FullName) | Out-Null } catch {}
}

$libraryPath = Join-Path $sourceRoot 'Server\bin\Debug\Library.dll'
Assert-Contract (Test-Path -LiteralPath $libraryPath) "缺少数据库读取程序集: $libraryPath"
$library = [System.Reflection.Assembly]::LoadFrom($libraryPath)
$databaseRoot = 'D:\Debug\4月18日更新\Server\Database\'
$backupRoot = 'D:\Debug\4月18日更新\Server\Backup\'
Assert-Contract (Test-Path -LiteralPath (Join-Path $databaseRoot 'System.db')) '缺少当前 System.db'
$session = [Activator]::CreateInstance(
    [MirDB.Session],
    [object[]]@([MirDB.SessionMode]::ServerTool, [System.Reflection.Assembly[]]@($library), $false, '', $databaseRoot, $backupRoot)
)
$session.Init()
$getCollection = $session.GetType().GetMethod('GetCollection', [Type[]]@())
$itemCollection = $getCollection.MakeGenericMethod([Library.SystemModels.ItemInfo]).Invoke($session, $null)
$items = $itemCollection.GetType().GetField('Binding').GetValue($itemCollection)
$unidentified = @($items | Where-Object { $_.ItemName -like '未鉴定*' })
Assert-Contract ($unidentified.Count -gt 0) 'System.db 中没有未鉴定装备数据'
foreach ($item in $unidentified) {
    $tier = [int]$item.RequiredAmount
    Assert-Contract ($tier -ge 1 -and $tier -le 5) "非法鉴定等级: $($item.ItemName)"
    $targetName = $item.ItemName.Substring(3)
    $matches = @($items | Where-Object { $_.ItemName -eq $targetName })
    Assert-Contract ($matches.Count -eq 1) "无法唯一映射稀世成品: $($item.ItemName)"
    Assert-Contract ($matches[0].Rarity.ToString() -eq 'Elite') "鉴定目标不是 Elite: $($item.ItemName) -> $targetName"
}

Write-Output 'PASS: equipment identification contract'
