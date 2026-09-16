# 假人 AI CPU 回归低开销诊断 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 生成一个行为不变的 Debug / AnyCPU 诊断版，用六个低开销聚合计时桶定位 15 个假人运行时的 CPU 时间落点。

**Architecture:** 在现有 `BotManager` partial class 中维护固定长度的 ticks/count 数组，用 `Stopwatch.GetTimestamp()` 和 `Interlocked` 记录同步方法耗时；`BotTick` 每 60 秒最多输出一条 `[BotPerf]` 汇总。战斗和 A* 只调用该聚合入口，不创建逐次日志、计时对象、任务、线程或新定时器。

**Tech Stack:** C# 7.2、.NET Framework 4.8、Mir3 Server、PowerShell 5.1 静态契约、MSBuild 17、Debug / AnyCPU。

## Global Constraints

- 只修改 `Server/BotManager.cs`、`Server/BotManager.Combat.cs`、`Server/BotPathFinder.cs`、`.diagnostics/bot-ai-cpu-profiling-contract.ps1`、本规格和计划文档。
- 保持 `BotMainSliceIntervalMs = 200`、`BotMainSliceCount = 4`、`BotPotionMonitorIntervalMs = 200`。
- 不修改技能顺序、喝药阈值、寻路策略、数据库、配置文件、部署目录或当前运行进程。
- 每个测量点只允许 `Stopwatch.GetTimestamp()` 和 `Interlocked` 聚合；不得使用 `Stopwatch.StartNew()`、`new Stopwatch()`、闭包、任务、线程或新定时器。
- 六个桶固定为 `TickDispatch`、`AiPipeline`、`Potion`、`Combat`、`TaoistCombat`、`PathCompute`；桶之间是包含关系，不相加。
- 每 60 秒最多一条 `[BotPerf]`，仅包含桶名、调用次数、累计毫秒和平均毫秒。
- 当前目录不是 Git 工作树；所有提交检查点改为记录相关文件 SHA-256。

---

### Task 1: 专项契约与真实 RED

**Files:**
- Create: `.diagnostics/bot-ai-cpu-profiling-contract.ps1`
- Verify: `Server/BotManager.cs`
- Verify: `Server/BotManager.Combat.cs`
- Verify: `Server/BotPathFinder.cs`

**Interfaces:**
- Consumes: 现有 PowerShell `Assert-Contract`、按括号深度提取方法块的模式。
- Produces: 对六个桶、60 秒汇总、低分配计时、调用点、周期常量和禁止项的静态契约。

- [ ] **Step 1: 记录生产文件基线哈希和契约不存在状态**

Run:

```powershell
Test-Path -LiteralPath .diagnostics\bot-ai-cpu-profiling-contract.ps1
Get-FileHash -Algorithm SHA256 Server\BotManager.cs,Server\BotManager.Combat.cs,Server\BotPathFinder.cs
```

Expected: 专项契约不存在；输出三个生产文件 SHA-256。

- [ ] **Step 2: 创建编码安全的专项契约**

契约以 UTF-8 显式读取三个源文件，内置完整方法块提取器，并至少包含以下断言：

```powershell
$ErrorActionPreference = 'Stop'

$root = Split-Path -Parent $PSScriptRoot
$managerPath = Join-Path $root 'Server\BotManager.cs'
$combatPath = Join-Path $root 'Server\BotManager.Combat.cs'
$pathFinderPath = Join-Path $root 'Server\BotPathFinder.cs'

$manager = [IO.File]::ReadAllText($managerPath, [Text.Encoding]::UTF8)
$combat = [IO.File]::ReadAllText($combatPath, [Text.Encoding]::UTF8)
$pathFinder = [IO.File]::ReadAllText($pathFinderPath, [Text.Encoding]::UTF8)
$failures = [Collections.Generic.List[string]]::new()
$passed = 0

function Assert-Contract([bool]$condition, [string]$message) {
    if ($condition) { $script:passed++; return }
    $script:failures.Add($message)
}

function Get-MethodBlock([string]$source, [string]$methodName) {
    $escapedName = [regex]::Escape($methodName)
    $signature = [regex]::Match($source,
        "(?ms)^\s*(?:private|protected|public|internal)\s+(?:static\s+)?[^\r\n{;]*\b$escapedName\s*\([^)]*\)\s*\{")
    if (-not $signature.Success) { return '' }
    $openBrace = $source.IndexOf('{', $signature.Index)
    $depth = 0
    for ($index = $openBrace; $index -lt $source.Length; $index++) {
        if ($source[$index] -eq '{') { $depth++ }
        elseif ($source[$index] -eq '}') {
            $depth--
            if ($depth -eq 0) {
                return $source.Substring($signature.Index, $index - $signature.Index + 1)
            }
        }
    }
    return ''
}

$botTick = Get-MethodBlock $manager 'BotTick'
$pipeline = Get-MethodBlock $manager 'ProcessBotBehaviorPipeline'
$potion = Get-MethodBlock $manager 'ProcessBotPotionModule'
$beginSample = Get-MethodBlock $manager 'BeginBotPerfSample'
$recordSample = Get-MethodBlock $manager 'RecordBotPerfSample'
$logSummary = Get-MethodBlock $manager 'TryLogBotPerfSummary'
$combatMethod = Get-MethodBlock $combat 'ProcessBotCombat'
$taoistMethod = Get-MethodBlock $combat 'ProcessBotTaoistCombatAction'
$pathCompute = Get-MethodBlock $pathFinder 'ComputeAndCache'

foreach ($bucket in 'TickDispatch','AiPipeline','Potion','Combat','TaoistCombat','PathCompute') {
    Assert-Contract ($manager -match "\b$bucket\b") "missing performance bucket $bucket"
}
Assert-Contract ($manager -match 'BotPerfLogIntervalSeconds\s*=\s*60') 'summary interval is not 60 seconds'
Assert-Contract ($beginSample -match 'Stopwatch\.GetTimestamp\s*\(') 'sample start is not allocation-free timestamping'
Assert-Contract ($recordSample -match 'Stopwatch\.GetTimestamp\s*\(' -and $recordSample -match 'Interlocked\.(Add|Increment)') 'sample recording does not atomically aggregate ticks and calls'
Assert-Contract ($logSummary -match 'Interlocked\.CompareExchange' -and $logSummary -match 'Interlocked\.Exchange') 'summary window is not atomically gated and reset'
Assert-Contract (([regex]::Matches($logSummary, 'SEnvir\.Log\s*\(')).Count -eq 1 -and $logSummary -match '\[BotPerf\]') 'summary must emit exactly one BotPerf log call'

$instrumented = @(
    @{ Block=$botTick; Bucket='TickDispatch' },
    @{ Block=$pipeline; Bucket='AiPipeline' },
    @{ Block=$potion; Bucket='Potion' },
    @{ Block=$combatMethod; Bucket='Combat' },
    @{ Block=$taoistMethod; Bucket='TaoistCombat' }
)
foreach ($entry in $instrumented) {
    Assert-Contract ($entry.Block -match 'try\s*\{' -and $entry.Block -match 'finally\s*\{' -and $entry.Block -match "BotPerfBucket\.$($entry.Bucket)") `
        "missing try/finally instrumentation for $($entry.Bucket)"
}
Assert-Contract ($pathCompute -match 'BeginBotPathPerfSample' -and $pathCompute -match 'finally\s*\{' -and $pathCompute -match 'RecordBotPathComputePerf') 'PathCompute instrumentation is missing'

Assert-Contract ($manager -match 'BotMainSliceIntervalMs\s*=\s*200') 'main slice interval changed'
Assert-Contract ($manager -match 'BotMainSliceCount\s*=\s*4') 'main slice count changed'
Assert-Contract ($combat -match 'BotPotionMonitorIntervalMs\s*=\s*200') 'potion monitor interval changed'

$diagnosticSource = $beginSample + $recordSample + $logSummary
Assert-Contract ($diagnosticSource -notmatch 'Stopwatch\.StartNew|new\s+Stopwatch|Task\.Run|new\s+Thread|new\s+Timer') 'diagnostics add a prohibited timer, thread, task, or Stopwatch object'

if ($failures.Count -gt 0) {
    Write-Host "BOT AI CPU PROFILING CONTRACT: FAIL ($passed passed, $($failures.Count) failed)" -ForegroundColor Red
    $failures | ForEach-Object { Write-Host " - $_" -ForegroundColor Red }
    exit 1
}
Write-Host "BOT AI CPU PROFILING CONTRACT: PASS ($passed assertions)" -ForegroundColor Green
```

- [ ] **Step 3: 运行专项契约并确认真实 RED**

Run:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .diagnostics\bot-ai-cpu-profiling-contract.ps1
```

Expected: exit code `1`；失败只来自六个桶、诊断方法和调用点尚不存在；三个周期常量断言继续通过。

- [ ] **Step 4: 记录 RED 哈希**

Run:

```powershell
Get-FileHash -Algorithm SHA256 .diagnostics\bot-ai-cpu-profiling-contract.ps1,Server\BotManager.cs,Server\BotManager.Combat.cs,Server\BotPathFinder.cs
```

Expected: 生产文件仍为 Step 1 哈希；只有新契约出现新哈希。

---

### Task 2: 通用无分配聚合计时和主AI/喝药接线

**Files:**
- Modify: `Server/BotManager.cs:1-16,385-456,1015-1237,1336-1382`
- Test: `.diagnostics/bot-ai-cpu-profiling-contract.ps1`

**Interfaces:**
- Produces: `BotPerfBucket`、`BeginBotPerfSample()`、`RecordBotPerfSample(BotPerfBucket,long)`、`BeginBotPathPerfSample()`、`RecordBotPathComputePerf(long)`、`TryLogBotPerfSummary()`。
- Consumes: `SEnvir.Now`、`SEnvir.Log(string)`、`Stopwatch.Frequency`、`Interlocked`。

- [ ] **Step 1: 加入 Stopwatch 命名空间和固定诊断状态**

在 `BotManager.cs` 增加 `using System.Diagnostics;`，并在调度常量附近加入：

```csharp
private enum BotPerfBucket
{
    TickDispatch,
    AiPipeline,
    Potion,
    Combat,
    TaoistCombat,
    PathCompute,
    Count,
}

private const int BotPerfLogIntervalSeconds = 60;
private static readonly string[] BotPerfBucketNames =
{
    "TickDispatch",
    "AiPipeline",
    "Potion",
    "Combat",
    "TaoistCombat",
    "PathCompute",
};
private static readonly long[] _botPerfElapsedTicks = new long[(int)BotPerfBucket.Count];
private static readonly long[] _botPerfCallCounts = new long[(int)BotPerfBucket.Count];
private static long _botPerfNextLogTimeTicks;
```

- [ ] **Step 2: 实现采样、重置和单行汇总方法**

在 `BotManager.cs` 调度常量附近加入以下方法，格式化只发生在每 60 秒一次的汇总路径：

```csharp
private static long BeginBotPerfSample()
{
    return Stopwatch.GetTimestamp();
}

private static void RecordBotPerfSample(BotPerfBucket bucket, long started)
{
    int index = (int)bucket;
    long elapsed = Stopwatch.GetTimestamp() - started;
    Interlocked.Add(ref _botPerfElapsedTicks[index], elapsed);
    Interlocked.Increment(ref _botPerfCallCounts[index]);
}

internal static long BeginBotPathPerfSample()
{
    return BeginBotPerfSample();
}

internal static void RecordBotPathComputePerf(long started)
{
    RecordBotPerfSample(BotPerfBucket.PathCompute, started);
}

private static void ResetBotPerfCounters()
{
    for (int index = 0; index < (int)BotPerfBucket.Count; index++)
    {
        Interlocked.Exchange(ref _botPerfElapsedTicks[index], 0L);
        Interlocked.Exchange(ref _botPerfCallCounts[index], 0L);
    }

    Interlocked.Exchange(ref _botPerfNextLogTimeTicks,
        SEnvir.Now.AddSeconds(BotPerfLogIntervalSeconds).Ticks);
}

private static void TryLogBotPerfSummary()
{
    long nowTicks = SEnvir.Now.Ticks;
    long expected = Interlocked.Read(ref _botPerfNextLogTimeTicks);
    if (nowTicks < expected)
        return;

    long next = SEnvir.Now.AddSeconds(BotPerfLogIntervalSeconds).Ticks;
    if (Interlocked.CompareExchange(ref _botPerfNextLogTimeTicks, next, expected) != expected)
        return;

    StringBuilder summary = new StringBuilder("[BotPerf]");
    for (int index = 0; index < (int)BotPerfBucket.Count; index++)
    {
        long elapsedTicks = Interlocked.Exchange(ref _botPerfElapsedTicks[index], 0L);
        long calls = Interlocked.Exchange(ref _botPerfCallCounts[index], 0L);
        double totalMs = elapsedTicks * 1000D / Stopwatch.Frequency;
        double averageMs = calls == 0 ? 0D : totalMs / calls;
        summary.AppendFormat(" {0}: calls={1}, totalMs={2:F3}, avgMs={3:F4};",
            BotPerfBucketNames[index], calls, totalMs, averageMs);
    }

    SEnvir.Log(summary.ToString());
}
```

- [ ] **Step 3: 在启动定时器前重置窗口**

在 `Start` 中、两个 `Timer.Change` 之前调用一次：

```csharp
ResetBotPerfCounters();
```

- [ ] **Step 4: 用 try/finally 接入 TickDispatch、AiPipeline 和 Potion**

每个方法在原有空值/未运行快速返回之后插入 `started` 和 `try` 开括号，在该方法原有最后一个闭括号之前插入对应的 `finally`。不得改写被包住的既有语句。`BotTick` 的插入内容为：

```csharp
long started = BeginBotPerfSample();
try
{
}
finally
{
    RecordBotPerfSample(BotPerfBucket.TickDispatch, started);
    TryLogBotPerfSummary();
}
```

空的 `try` 块表示开括号紧接现有第一条主体语句，闭括号放在现有主体末尾。`ProcessBotBehaviorPipeline` 的 finally 精确使用：

```csharp
finally
{
    RecordBotPerfSample(BotPerfBucket.AiPipeline, started);
}
```

`ProcessBotPotionModule` 的 finally 精确使用：

```csharp
finally
{
    RecordBotPerfSample(BotPerfBucket.Potion, started);
}
```

- [ ] **Step 5: 运行专项契约确认通用计时通过、战斗和路径仍 RED**

Run:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .diagnostics\bot-ai-cpu-profiling-contract.ps1
```

Expected: 诊断状态、60秒汇总、TickDispatch、AiPipeline、Potion 断言通过；Combat、TaoistCombat、PathCompute 调用点仍失败，整体 exit code `1`。

- [ ] **Step 6: 记录主计时实现哈希**

Run:

```powershell
Get-FileHash -Algorithm SHA256 Server\BotManager.cs
```

---

### Task 3: 战斗、道士和 A* 接线并取得 GREEN

**Files:**
- Modify: `Server/BotManager.Combat.cs:1449-2043,2397-2436`
- Modify: `Server/BotPathFinder.cs:272-284`
- Test: `.diagnostics/bot-ai-cpu-profiling-contract.ps1`

**Interfaces:**
- Consumes: `BotManager.BeginBotPathPerfSample()`、`BotManager.RecordBotPathComputePerf(long)` 和 Task 2 的私有通用采样方法。
- Produces: `Combat`、`TaoistCombat`、`PathCompute` 三个计时桶数据。

- [ ] **Step 1: 包装完整战斗入口**

`ProcessBotCombat` 在方法开括号之后、现有第一条语句之前插入 `started` 和 `try` 开括号；在方法原有最后一个闭括号之前关闭 try 并插入 finally：

```csharp
long started = BeginBotPerfSample();
try
{
}
finally
{
    RecordBotPerfSample(BotPerfBucket.Combat, started);
}
```

- [ ] **Step 2: 包装道士职业战斗入口**

`ProcessBotTaoistCombatAction` 在方法开括号之后插入 `long started = BeginBotPerfSample();` 和 `try` 开括号，在方法原有最后一个闭括号之前关闭 try；其 finally 固定为：

```csharp
RecordBotPerfSample(BotPerfBucket.TaoistCombat, started);
```

不得改变 `ExplosiveTalisman`、`EvilSlayer`、`GreaterEvilSlayer` 和可选施毒的数据流。

- [ ] **Step 3: 包装 A* 重新计算入口**

`BotPathFinder.ComputeAndCache` 使用对外的路径专用包装器：

```csharp
long started = BotManager.BeginBotPathPerfSample();
try
{
    Queue<Point> path = FindPath(map, from, to);
    if (path == null || path.Count == 0) return false;

    _pathCache[objectId] = new PathCache
    {
        Path = path,
        Goal = to,
        ExpireTime = SEnvir.Now.AddSeconds(PathCacheExpireSeconds),
    };
    return true;
}
finally
{
    BotManager.RecordBotPathComputePerf(started);
}
```

- [ ] **Step 4: 运行专项契约并确认 GREEN**

Run:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .diagnostics\bot-ai-cpu-profiling-contract.ps1
```

Expected: exit code `0`；全部断言通过。

- [ ] **Step 5: 静态检查无新增调度和逐次日志**

Run:

```powershell
rg -n "Stopwatch\.StartNew|new Stopwatch|Task\.Run|new Thread|new Timer|\[BotPerf\]" Server\BotManager.cs Server\BotManager.Combat.cs Server\BotPathFinder.cs
```

Expected: 只出现一处 `[BotPerf]` 汇总字符串；不存在 `Stopwatch.StartNew`、`new Stopwatch`、`Task.Run`、`new Thread`；已有 `new Timer` 仅为原始 `Initialize` 中两个定时器，相关行与基线一致。

- [ ] **Step 6: 记录最终生产与专项契约哈希**

Run:

```powershell
Get-FileHash -Algorithm SHA256 Server\BotManager.cs,Server\BotManager.Combat.cs,Server\BotPathFinder.cs,.diagnostics\bot-ai-cpu-profiling-contract.ps1
```

---

### Task 4: 回归、Debug / AnyCPU 独立构建和运行采集交付

**Files:**
- Verify: `.diagnostics/bot-ai-cpu-profiling-contract.ps1`
- Verify: `.diagnostics/bot-ai-cpu-potion-contract.ps1`
- Verify: `.diagnostics/bot-ai-phase1-contract.ps1`
- Verify: `.diagnostics/bot-ai-level40-assassin-contract.ps1`
- Verify: `.diagnostics/bot-ai-taoist-wizard-combat-priority-contract.ps1`
- Build output: `.build-check/bot-ai-cpu-profiling-debug-anycpu/Server.exe`

**Interfaces:**
- Consumes: Tasks 1–3 的最终源码和契约。
- Produces: 诊断版 Server、版本/大小/SHA-256、运行采集说明和明确的未部署状态。

- [ ] **Step 1: 并行运行五个核心契约**

Run each with Windows PowerShell 5.1:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .diagnostics\bot-ai-cpu-profiling-contract.ps1
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .diagnostics\bot-ai-cpu-potion-contract.ps1
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .diagnostics\bot-ai-phase1-contract.ps1
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .diagnostics\bot-ai-level40-assassin-contract.ps1
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .diagnostics\bot-ai-taoist-wizard-combat-priority-contract.ps1
```

Expected: 五个命令均 exit code `0`。历史固定哈希契约不修改或放宽。

- [ ] **Step 2: 构建 Debug ServerLibrary**

Run:

```powershell
dotnet build ServerLibrary\ServerLibrary.csproj -c Debug --no-restore
```

Expected: exit code `0`、0 errors。

- [ ] **Step 3: 独立重建 Debug / AnyCPU Server**

Run:

```powershell
$output = 'D:\相聚假人\Source\.build-check\bot-ai-cpu-profiling-debug-anycpu\'
$obj = 'D:\相聚假人\Source\.build-check\bot-ai-cpu-profiling-debug-anycpu-obj\'
New-Item -ItemType Directory -Force -Path $output,$obj | Out-Null
$msbuild = 'C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\MSBuild\Current\Bin\MSBuild.exe'
& $msbuild Server\Server.csproj /t:Rebuild /m /v:minimal /p:Configuration=Debug /p:Platform=AnyCPU "/p:OutputPath=$output" "/p:BaseIntermediateOutputPath=$obj"
```

Expected: exit code `0`、0 errors；只允许报告项目既有 `MSB3277` 程序集版本冲突警告。

- [ ] **Step 4: 构建后重跑专项契约并记录产物**

Run:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .diagnostics\bot-ai-cpu-profiling-contract.ps1
$artifact = Get-Item -LiteralPath '.build-check\bot-ai-cpu-profiling-debug-anycpu\Server.exe'
$artifact | Select-Object FullName,Length,LastWriteTime,@{Name='Version';Expression={$_.VersionInfo.FileVersion}}
Get-FileHash -Algorithm SHA256 -LiteralPath $artifact.FullName
```

Expected: 专项契约仍 GREEN；产物存在且输出版本、大小和 SHA-256。

- [ ] **Step 5: 确认未部署和运行进程未重启**

Run:

```powershell
Get-FileHash -Algorithm SHA256 -LiteralPath 'D:\Debug\4月18日更新\Server\Server.exe'
Get-Process -Name Server -ErrorAction SilentlyContinue | Select-Object Id,StartTime
```

Expected: 部署文件仍为进入任务时的哈希，运行进程 ID/启动时间不因本任务改变。

- [ ] **Step 6: 交付运行采集命令**

用户手动部署并重启诊断版后，运行至少 10 分钟。采集部署目录中包含 `[BotPerf]` 的日志行，并同时用下列命令采样 CPU：

```powershell
$logical = [Environment]::ProcessorCount
$process = Get-Process -Name Server | Sort-Object StartTime -Descending | Select-Object -First 1
$previousCpu = $process.CPU
$previousTime = Get-Date
1..60 | ForEach-Object {
    Start-Sleep -Seconds 1
    $process.Refresh()
    $now = Get-Date
    $cpuNow = $process.CPU
    [pscustomobject]@{
        Time = $now
        CpuPercent = (($cpuNow - $previousCpu) / ($now - $previousTime).TotalSeconds / $logical) * 100
    }
    $previousCpu = $cpuNow
    $previousTime = $now
}
```

Expected: 获得至少 10 条连续 `[BotPerf]` 和同负载 CPU 区间。运行数据决定下一任务唯一优化桶；本诊断任务不直接宣称 CPU 已降低。
