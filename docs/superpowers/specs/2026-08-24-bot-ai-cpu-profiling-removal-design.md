# Bot AI CPU Profiling Removal Design

## Goal

Remove the temporary runtime CPU profiling instrumentation now that the 15-bot ten-minute measurement has completed, while preserving every functional CPU optimization and bot behavior change.

## Chosen approach

Perform a surgical removal of the profiling implementation and its dedicated contract:

- Remove the six `BotPerfBucket` counters, timestamp/atomic aggregation helpers, 60-second `[BotPerf]` summary, reset call, and all profiling `try/finally` wrappers.
- Remove the pathfinding bridge methods and wrapper from `BotPathFinder.ComputeAndCache`.
- Delete `.diagnostics/bot-ai-cpu-profiling-contract.ps1`, because its required behavior is intentionally being removed.
- Extend `.diagnostics/bot-ai-cpu-optimization-contract.ps1` first to assert that no `[BotPerf]` symbols, log text, path profiling bridge, or profiling-only `Stopwatch` usage remains. This must produce RED before production removal and GREEN afterward.

This is preferred over disabling the logger or leaving dormant counters because complete removal has the lowest runtime overhead and leaves no dead diagnostic state.

## Preserved behavior

The removal must not change:

- 200 ms potion monitoring, four-slice main scheduling, or combat cadence.
- Equipment 30 s, consumables 20 s, inventory 60 s, class support 10 s, high-BOSS scan 180 s, skill learning/resupply 30 s, social 30-60 s, trade 120/180 s, and map evaluation 120 s.
- Lazy potion exclusion allocation and current potion thresholds.
- Strict below-5%-HP single-bot recall and recall recovery ordering before trade, siege, and PK.
- Any class skill priority, movement, targeting, pickup, group, PK, or siege behavior.

## Verification

1. Update the optimization contract and obtain a genuine RED caused only by profiling symbols still being present.
2. Remove the instrumentation and profiling contract.
3. Run the optimization, potion, phase-one, level-40/Assassin, and Taoist/Wizard priority contracts.
4. Confirm no `BotPerf`, `[BotPerf]`, `BeginBotPathPerfSample`, or `RecordBotPathComputePerf` remains in production source.
5. Rebuild `ServerLibrary` and an isolated Debug/AnyCPU `Server.exe` with zero errors; existing `MSB3277` warnings remain acceptable.
6. Record final hashes and artifact metadata. Do not deploy, restart, back up, or use Git/PR operations.

## Files

Modify:

- `Server/BotManager.cs`
- `Server/BotManager.Combat.cs`
- `Server/BotPathFinder.cs`
- `.diagnostics/bot-ai-cpu-optimization-contract.ps1`

Delete:

- `.diagnostics/bot-ai-cpu-profiling-contract.ps1`

Documentation and isolated build output are the only additional writes.
