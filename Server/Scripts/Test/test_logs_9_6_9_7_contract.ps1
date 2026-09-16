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
$definesPath = Join-Path $scriptRoot 'Defines.py'
$stonePath = Join-Path $scriptRoot 'Npc\古墓\等候厅古代石碑.py'
$definesText = Read-Utf8 $definesPath
$stoneText = Read-Utf8 $stonePath

$killProgressPattern = '(?m)^\s*BV_NQ_NMKILL\s*=\s*500\s*(?:#.*)?$'
Assert-Contract (([regex]::Matches($definesText, $killProgressPattern)).Count -eq 1) 'Defines.py 必须恰有 BV_NQ_NMKILL = 500'

$strInitIndex = $stoneText.IndexOf('str = ""')
$firstMenuIndex = $stoneText.IndexOf('if(Menu == 1)')
Assert-Contract ($strInitIndex -ge 0 -and $strInitIndex -lt $firstMenuIndex) '古代石碑必须在菜单 1 分支前初始化 str'

foreach ($mapIndex in 673..677) {
    $teleportPattern = "TeleportByMapIndex\(\s*$mapIndex\s*,\s*198\s*,\s*200\s*\)"
    Assert-Contract (([regex]::Matches($stoneText, $teleportPattern)).Count -eq 1) "古代石碑缺少地图 $mapIndex 的固定坐标 198,200"
}

$python = 'C:\Python27\python.exe'
Assert-Contract (Test-Path -LiteralPath $python) '找不到受控执行用 Python 2.7'
$harness = @'
import sys
import types

sys.modules['Globals'] = types.ModuleType('Globals')
clr = types.ModuleType('clr')
clr.AddReference = lambda name: None
sys.modules['clr'] = clr
sys.modules['Library'] = types.ModuleType('Library')
npc_event = types.ModuleType('NpcEvent')
npc_event.add_listener = lambda *args: None
sys.modules['NpcEvent'] = npc_event

source_path = sys.argv[1]
namespace = {}
source = open(source_path, 'rb').read()
exec(compile(source, source_path, 'exec'), namespace)

class Sender(object):
    def __init__(self):
        self.teleports = []

    def TeleportByMapIndex(self, *args):
        self.teleports.append(args)

for menu in range(1, 6):
    sender = Sender()
    result = namespace['OnClick']([None, sender, menu])
    expected = 672 + menu
    assert sender.teleports == [(expected, 198, 200)]
    assert result.get('Say') == ''

print('PASS: logs 9_6/9_7 contract')
'@
& $python -c $harness $stonePath
if ($LASTEXITCODE -ne 0) {
    throw "CONTRACT FAILURE: 古代石碑受控执行退出 $LASTEXITCODE"
}

Write-Output 'PASS: logs 9_6/9_7 contract'
