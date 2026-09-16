# Bot AI CPU Profiling Removal Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remove the temporary six-bucket Bot AI CPU profiler and its dedicated contract while preserving all functional CPU optimizations and bot behavior.

**Architecture:** Turn the existing CPU optimization contract into the durable absence guard, obtain RED while profiling symbols remain, then surgically unwrap the five instrumented execution paths and pathfinder bridge. Delete only the now-obsolete profiling contract and rebuild an isolated Debug/AnyCPU artifact.

**Tech Stack:** C#, .NET Framework/MSBuild, Windows PowerShell 5.1 contracts, SHA-256 verification.

## Global Constraints

- Shared non-Git workspace: `D:\相聚假人\Source`; preserve unrelated and concurrent work.
- No deployment, restart, backup, database/client/script/resource changes, Git, commit, branch, push, or PR.
- Preserve `BotMainSliceIntervalMs = 200`, `BotMainSliceCount = 4`, `BotPotionMonitorIntervalMs = 200`, combat cadence, potion thresholds, and all class behavior.
- Preserve every maintenance interval and strict below-5%-HP single-bot recall added by the CPU optimization task.
- Remove the profiling implementation completely; do not replace it with a flag, dormant counters, another logger, thread, timer, task, or profiler.
- Build only Debug/AnyCPU into `.build-check\bot-ai-cpu-no-profiling-debug-anycpu\` and matching `-obj` directory.

---

### Task 1: Add the durable absence contract and obtain RED

**Files:**

- Modify: `.diagnostics/bot-ai-cpu-optimization-contract.ps1`
- Read: `Server/BotManager.cs`
- Read: `Server/BotManager.Combat.cs`
- Read: `Server/BotPathFinder.cs`

**Interfaces:**

- Consumes: current UTF-8 source text already loaded by the optimization contract.
- Produces: assertions that fail while profiling code exists and remain GREEN after removal.

- [ ] **Step 1: Verify exact starting hashes before edits**

```powershell
Get-FileHash -Algorithm SHA256 -LiteralPath `
  'Server\BotManager.cs', `
  'Server\BotManager.Combat.cs', `
  'Server\BotPathFinder.cs', `
  '.diagnostics\bot-ai-cpu-profiling-contract.ps1', `
  '.diagnostics\bot-ai-cpu-optimization-contract.ps1'
```

Expected current hashes:

- `BotManager.cs`: `FD4D4870FD830B36086A780E8425F47F5F51AD3B81693F9B5FFFC8944B294212`
- `BotManager.Combat.cs`: `759DC9D5CDFA2BA2B9CAC212B60ABF862680C2F8CCE204DF70B8A41A44B376A3`
- `BotPathFinder.cs`: `7C23ED1E087F6C5A613DD33CEB5ED64EF392148DBEFA2F9A18074841BE7B0615`
- profiling contract: `0A3C79C840619B3F9FD693D83B3E0C0BDC87272CD301A37B35CB6C3DBD8FF357`
- optimization contract: `CE282B03B42CF73C0281CE672DC0771798754E740E09F4E0D7D9F3DE0682EA8B`

If any differs, inspect current content and preserve concurrent changes rather than restoring an old snapshot.

- [ ] **Step 2: Extend the optimization contract with exact absence assertions**

Load `Server/BotPathFinder.cs` using the contract's existing no-BOM UTF-8 reader and add assertions equivalent to:

```powershell
Assert-NotMatch ($manager + $combat + $pathFinder) '\bBotPerf(?:Bucket|LogIntervalSeconds|BucketNames)?\b' 'temporary BotPerf symbols are removed'
Assert-NotMatch ($manager + $combat + $pathFinder) '\[BotPerf\]' 'temporary BotPerf log line is removed'
Assert-NotMatch ($manager + $combat + $pathFinder) '\b(?:Begin|Record|Reset|TryLog)BotPerf\w*\b' 'temporary BotPerf helpers are removed'
Assert-NotMatch ($manager + $combat + $pathFinder) '\b(?:BeginBotPathPerfSample|RecordBotPathComputePerf)\b' 'path profiling bridge is removed'
Assert-NotMatch ($manager + $combat + $pathFinder) 'Stopwatch\.GetTimestamp\s*\(' 'profiling timestamp calls are removed'
```

Retain all existing 83 optimization assertions, especially maintenance frequencies, potion behavior, recall ordering, and no-new-thread/timer checks.

- [ ] **Step 3: Run the contract and capture genuine RED**

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File '.diagnostics\bot-ai-cpu-optimization-contract.ps1'
```

Expected: non-zero exit caused only by the newly added absence assertions finding the still-present `BotPerf` profiler. Record passed/failed assertion counts and failure names before any production edit.

---

### Task 2: Remove BotManager and combat profiling wrappers

**Files:**

- Modify: `Server/BotManager.cs`
- Modify: `Server/BotManager.Combat.cs`
- Test: `.diagnostics/bot-ai-cpu-optimization-contract.ps1`

**Interfaces:**

- Consumes: existing original method bodies inside profiling-only `try/finally` wrappers.
- Produces: the same methods and return behavior without timestamps, counters, or summary logging.

- [ ] **Step 1: Remove the profiler definitions from BotManager.cs**

Delete only:

```csharp
private enum BotPerfBucket { ... }
private const int BotPerfLogIntervalSeconds = 60;
private static readonly string[] BotPerfBucketNames = ...;
private static readonly long[] _botPerfElapsedTicks = ...;
private static readonly long[] _botPerfCallCounts = ...;
private static long _botPerfNextLogTimeTicks;
private static long BeginBotPerfSample() { ... }
private static void RecordBotPerfSample(...) { ... }
internal static long BeginBotPathPerfSample() { ... }
internal static void RecordBotPathComputePerf(...) { ... }
private static void ResetBotPerfCounters() { ... }
private static void TryLogBotPerfSummary() { ... }
```

Remove any `using System.Diagnostics;` or `using System.Text;` only if it becomes unused after this deletion; do not remove imports used elsewhere.

- [ ] **Step 2: Remove profiler initialization and dispatch logging**

Delete the `ResetBotPerfCounters();` initialization call. Restore `BotTick` to its original direct body by removing:

```csharp
long started = BeginBotPerfSample();
try
{
    // existing body
}
finally
{
    RecordBotPerfSample(BotPerfBucket.TickDispatch, started);
    TryLogBotPerfSummary();
}
```

The existing body and every early return remain unchanged and in the same order.

- [ ] **Step 3: Unwrap potion and AI pipeline methods**

For `ProcessBotPotionModule` and `ProcessBotBehaviorPipeline`, remove only the profiler timestamp and outer `try/finally`; keep their existing method bodies byte-for-byte apart from indentation:

```csharp
// remove
long started = BeginBotPerfSample();
try { /* existing body */ }
finally { RecordBotPerfSample(..., started); }
```

Do not alter the 200 ms potion monitor, four-slice scheduler, maintenance gates, recall helper call before trade/conquest, or any return path.

- [ ] **Step 4: Unwrap combat and Taoist combat methods**

In `ProcessBotCombat` and `ProcessBotTaoistCombatAction`, remove only:

```csharp
long started = BeginBotPerfSample();
try { /* existing body */ }
finally { RecordBotPerfSample(BotPerfBucket.Combat /* or TaoistCombat */, started); }
```

Preserve the complete inner methods, including all skill ordering, ranged repositioning, pickup, path, and early-return behavior.

- [ ] **Step 5: Run the optimization contract checkpoint**

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File '.diagnostics\bot-ai-cpu-optimization-contract.ps1'
```

Expected at this checkpoint: profiler assertions may still fail only for the pathfinder bridge until Task 3; all functional optimization assertions remain GREEN.

---

### Task 3: Remove pathfinder profiling and obsolete contract

**Files:**

- Modify: `Server/BotPathFinder.cs`
- Delete: `.diagnostics/bot-ai-cpu-profiling-contract.ps1`
- Test: `.diagnostics/bot-ai-cpu-optimization-contract.ps1`

**Interfaces:**

- Consumes: existing `ComputeAndCache` path calculation body.
- Produces: the same `ComputeAndCache` signature and cache/path semantics without calls into `BotManager` profiling helpers.

- [ ] **Step 1: Unwrap ComputeAndCache**

Remove only:

```csharp
long started = BotManager.BeginBotPathPerfSample();
try
{
    // existing ComputeAndCache body
}
finally
{
    BotManager.RecordBotPathComputePerf(started);
}
```

Keep the existing `ComputePath`, cache write, result, and all returns unchanged.

- [ ] **Step 2: Delete the obsolete profiling contract**

Delete exactly:

```text
.diagnostics/bot-ai-cpu-profiling-contract.ps1
```

Do not delete `.diagnostics/bot-ai-cpu-optimization-contract.ps1` or any historical runtime log.

- [ ] **Step 3: Run GREEN and static absence scan**

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File '.diagnostics\bot-ai-cpu-optimization-contract.ps1'
rg -n 'BotPerf|\[BotPerf\]|BeginBotPathPerfSample|RecordBotPathComputePerf|Stopwatch\.GetTimestamp' `
  'Server\BotManager.cs' 'Server\BotManager.Combat.cs' 'Server\BotPathFinder.cs'
```

Expected: contract exits zero; `rg` returns no matches. Confirm the deleted profiling contract no longer exists with `Test-Path` returning `False`.

---

### Task 4: Regression, isolated Debug/AnyCPU rebuild, and evidence

**Files:**

- Test: `.diagnostics/bot-ai-cpu-optimization-contract.ps1`
- Test: `.diagnostics/bot-ai-cpu-potion-contract.ps1`
- Test: `.diagnostics/bot-ai-phase1-contract.ps1`
- Test: `.diagnostics/bot-ai-level40-assassin-contract.ps1`
- Test: `.diagnostics/bot-ai-taoist-wizard-combat-priority-contract.ps1`
- Output: `.build-check/bot-ai-cpu-no-profiling-debug-anycpu/`
- Output: `.build-check/bot-ai-cpu-no-profiling-debug-anycpu-obj/`

**Interfaces:**

- Consumes: profiler-free production source from Tasks 2-3.
- Produces: verified Debug/AnyCPU `Server.exe` and final SHA-256 evidence.

- [ ] **Step 1: Run the complete authoritative regression set**

```powershell
$contracts = @(
  '.diagnostics\bot-ai-cpu-optimization-contract.ps1',
  '.diagnostics\bot-ai-cpu-potion-contract.ps1',
  '.diagnostics\bot-ai-phase1-contract.ps1',
  '.diagnostics\bot-ai-level40-assassin-contract.ps1',
  '.diagnostics\bot-ai-taoist-wizard-combat-priority-contract.ps1'
)
foreach ($contract in $contracts) {
    powershell.exe -NoProfile -ExecutionPolicy Bypass -File $contract
    if ($LASTEXITCODE -ne 0) { throw "Contract failed: $contract" }
}
```

Expected: all five contracts exit zero with their current assertion counts. Do not use stale fixed-hash Taoist/Assassin contracts as authority for files intentionally changed by later approved work.

- [ ] **Step 2: Build ServerLibrary**

```powershell
dotnet build 'ServerLibrary\ServerLibrary.csproj' -c Debug --no-restore
```

Expected: zero errors.

- [ ] **Step 3: Rebuild isolated Debug/AnyCPU Server.exe**

```powershell
$output = 'D:\相聚假人\Source\.build-check\bot-ai-cpu-no-profiling-debug-anycpu\'
$obj = 'D:\相聚假人\Source\.build-check\bot-ai-cpu-no-profiling-debug-anycpu-obj\'
New-Item -ItemType Directory -Force -Path $output, $obj | Out-Null
$msbuild = 'C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\MSBuild\Current\Bin\MSBuild.exe'
& $msbuild 'Server\Server.csproj' /t:Rebuild /m /v:minimal /p:Configuration=Debug /p:Platform=AnyCPU "/p:OutputPath=$output" "/p:BaseIntermediateOutputPath=$obj"
if ($LASTEXITCODE -ne 0) { throw 'Debug/AnyCPU rebuild failed.' }
```

Expected: zero errors; existing `MSB3277` assembly version warning is allowed and must be reported.

- [ ] **Step 4: Re-run GREEN after the build and record hashes**

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File '.diagnostics\bot-ai-cpu-optimization-contract.ps1'
Get-FileHash -Algorithm SHA256 -LiteralPath `
  'Server\BotManager.cs', `
  'Server\BotManager.Combat.cs', `
  'Server\BotPathFinder.cs', `
  '.diagnostics\bot-ai-cpu-optimization-contract.ps1', `
  'docs\superpowers\specs\2026-08-24-bot-ai-cpu-profiling-removal-design.md', `
  'docs\superpowers\plans\2026-08-24-bot-ai-cpu-profiling-removal.md', `
  '.build-check\bot-ai-cpu-no-profiling-debug-anycpu\Server.exe'
```

Report artifact path, bytes, version, SHA-256, actual changed/deleted files, RED/GREEN evidence, regression counts, build warnings/errors, and that deployment/process state was not changed. The removed runtime profiler means future CPU comparison requires explicit temporary instrumentation again; do not claim further runtime reduction without a new measurement.
