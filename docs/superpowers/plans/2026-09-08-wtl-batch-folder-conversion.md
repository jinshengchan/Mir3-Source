# WTL Batch and Folder Conversion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `sol-advisor:orchestration` with the explicitly authorized GPT-5.6 Luna / Max user-visible task lane. Execute every task with test-first RED→GREEN evidence. This source tree is not a Git repository, so do not create commits; record exact changed-file lists and SHA-256 checkpoints instead.

**Goal:** Fix V2 WTL mask-flag parsing and add reliable multi-file and current-folder WTL-to-Black-Dragon-ZL conversion with isolated output and per-file failure reporting.

**Architecture:** Normalize the V2 mask texture byte at the WTL frame parser boundary, then route both UI entry points through one sequential batch service. The service owns top-level file discovery, `ConvertedZL` output paths, per-file disposal, and result aggregation; `LMain` owns dialogs and user-facing summaries only.

**Tech Stack:** C# / .NET Framework 4.8 WinForms, Ionic.Zlib, legacy MSBuild, PowerShell 5.1-compatible regression contracts.

## Global Constraints

- Change only `LibraryEditor` WTL-to-ZL conversion code, its focused tests, project compile list, and the approved design/plan documents.
- Folder conversion scans only the selected folder's top level; never recurse into subfolders.
- Write each result under the source file's sibling `ConvertedZL` directory; never overwrite source WTL files or pre-existing source-directory ZL files.
- Continue after an individual conversion failure and report successful count, failed count, and failed file names.
- Convert sequentially to keep WinForms progress access and error attribution deterministic.
- Do not change `Graphics/WTLLibrary.cs` or other format-conversion paths.
- Do not deploy over `D:\111\8.31素材编辑器\Z3素材编辑器.exe` without a later explicit user instruction.
- Preserve original files under `D:\Video\好玩新服4区完整端.rar\Data`; use copied inputs for runtime conversion acceptance.

---

## File Structure

- Create `LibraryEditor/WtlConversionBatch.cs`: top-level folder discovery, sequential conversion, output path construction, and focused result objects.
- Create `LibraryEditor/.diagnostics/test_wtl_v2_batch_conversion_contract.ps1`: real binary RED/GREEN regression and batch continuation contract.
- Modify `LibraryEditor/Graphics/WTL1to1ZL.cs`: normalize the V2 mask byte and support an explicit output filename while preserving the existing overload.
- Modify `LibraryEditor/LMain.cs`: connect file and folder dialogs to the batch service and display one summary.
- Modify `LibraryEditor/LMain.Designer.cs`: rename the existing multi-file command and add the folder command.
- Modify `LibraryEditor/LibraryEditor.csproj`: compile `WtlConversionBatch.cs`.

---

### Task 1: Lock Down and Fix the V2 Mask-Flag Regression

**Files:**
- Create: `D:\相聚假人\Source\LibraryEditor\.diagnostics\test_wtl_v2_batch_conversion_contract.ps1`
- Modify: `D:\相聚假人\Source\LibraryEditor\Graphics\WTL1to1ZL.cs:244-254`

**Interfaces:**
- Consumes: `WTL1to1ZL(string filename)` and real input `D:\Video\好玩新服4区完整端.rar\Data\Equip.wtl`.
- Produces: V2 `MaskTextureType` values with bit `0x80` removed before `HasMask` is calculated.

- [ ] **Step 1: Capture protected hashes**

Run:

```powershell
$targets = @(
  'D:\Video\好玩新服4区完整端.rar\Data\Equip.wtl',
  'D:\111\8.31素材编辑器\Z3素材编辑器.exe',
  'D:\相聚假人\Source\LibraryEditor\Graphics\WTLLibrary.cs'
)
$targets | ForEach-Object { Get-FileHash -LiteralPath $_ -Algorithm SHA256 }
```

Expected: three SHA-256 values are recorded before edits; `Equip.wtl` is `13BB937C13DFAA498F0C2D9A05725404CD356F810DB188ED7086F5A054C2D161`.

- [ ] **Step 2: Write the failing real-input test**

The PowerShell contract must:

```powershell
param(
    [Parameter(Mandatory = $true)][string]$EditorExe,
    [Parameter(Mandatory = $true)][string]$EquipWtl,
    [Parameter(Mandatory = $true)][string]$SourceRoot
)

# Load every managed DLL beside EditorExe, instantiate LibraryEditor.LMain on an STA
# thread, then instantiate LibraryEditor.WTL1to1ZL with EquipWtl through reflection.
# Assert that construction succeeds and that the public Images array length is 20000.
# On exception, unwrap all InnerException values and print:
# FAIL: Equip.wtl conversion reader: <type>: <message>
# Exit 1 on failure and print TOTAL PASS <n> FAIL <n> before exiting.
```

The contract must use the actual compiled editor and the actual `Equip.wtl`, not a mocked byte array or source-text assertion.

- [ ] **Step 3: Run the test and verify RED**

Run against the current executable:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -STA -File "D:\相聚假人\Source\LibraryEditor\.diagnostics\test_wtl_v2_batch_conversion_contract.ps1" `
  -EditorExe "D:\111\8.31素材编辑器\Z3素材编辑器.exe" `
  -EquipWtl "D:\Video\好玩新服4区完整端.rar\Data\Equip.wtl" `
  -SourceRoot "D:\相聚假人\Source\LibraryEditor"
```

Expected: exit 1 with `Ionic.Zlib.ZlibException` and `Bad state (invalid stored block lengths)`.

- [ ] **Step 4: Apply the minimal parser fix**

In the V2 branch of `WTL1to1ZL.MImage`, replace the raw assignment with high-bit normalization before calculating `HasMask`:

```csharp
var maskU1 = bReader.ReadByte();
MaskTextureType = (byte)(bReader.ReadByte() & 0x7F);

HasMask = MaskTextureType > 0;
```

Do not alter the V1 branch or `WTLLibrary.cs`.

- [ ] **Step 5: Build to an isolated artifact directory**

Run:

```powershell
& 'C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\MSBuild\Current\Bin\MSBuild.exe' `
  'D:\相聚假人\Source\LibraryEditor\LibraryEditor.csproj' `
  /t:Build /p:Configuration=Release /p:Platform=x64 `
  /p:OutputPath='D:\相聚假人\Source\.artifacts\wtl-converter-fixed\' /m
```

Expected: exit 0 and `D:\相聚假人\Source\.artifacts\wtl-converter-fixed\Z3专用客户端素材编辑器.exe` exists.

- [ ] **Step 6: Run the test and verify GREEN**

Run the Step 3 command with `-EditorExe` changed to the isolated build.

Expected: exit 0, `Images.Length = 20000`, and `TOTAL ... FAIL 0`.

- [ ] **Step 7: Record the non-Git checkpoint**

Record the SHA-256 of the test, `WTL1to1ZL.cs`, and isolated executable. Confirm protected hashes from Step 1 are unchanged.

---

### Task 2: Add the Sequential Batch Conversion Core

**Files:**
- Create: `D:\相聚假人\Source\LibraryEditor\WtlConversionBatch.cs`
- Modify: `D:\相聚假人\Source\LibraryEditor\Graphics\WTL1to1ZL.cs:114-121`
- Modify: `D:\相聚假人\Source\LibraryEditor\LibraryEditor.csproj:115-152`
- Test: `D:\相聚假人\Source\LibraryEditor\.diagnostics\test_wtl_v2_batch_conversion_contract.ps1`

**Interfaces:**
- Produces: `internal static string[] GetTopLevelWtlFiles(string folderPath)`.
- Produces: `internal static WtlConversionBatchResult ConvertFiles(IEnumerable<string> fileNames, bool crypt)`.
- Produces: `internal sealed class WtlConversionFailure` with constructor `WtlConversionFailure(string fileName, string message)` and read-only `FileName` / `Message` properties.
- Produces: `internal sealed class WtlConversionBatchResult` with `int SuccessCount`, `List<WtlConversionFailure> Failures`, and `List<string> OutputFiles`; `SuccessCount` increments only after `ToMLibrary` returns successfully.
- Produces: `public void ToMLibrary(bool crypt, string outputFileName)` while preserving `public void ToMLibrary(bool crypt)`.

- [ ] **Step 1: Extend the contract for output isolation and continuation**

Add contract setup that creates one temporary root with:

```text
Input/
  Equip.wtl              (copied real valid input)
  Broken.wtl             (small deliberately invalid file)
  Nested/Ignored.wtl     (copy; must not be discovered)
```

Through reflection, assert:

```text
GetTopLevelWtlFiles(Input) returns exactly Equip.wtl and Broken.wtl.
ConvertFiles([Broken.wtl, Equip.wtl], false) reports SuccessCount = 1.
Failures contains Broken.wtl and its actual exception message.
OutputFiles contains Input\ConvertedZL\Equip.Zl.
No ZL is created directly under Input or Nested.
```

Always clean the temporary root in `finally` after verifying its resolved path is under `%TEMP%`.

- [ ] **Step 2: Run the extended contract and verify RED**

Run the focused contract against the Task 1 isolated build.

Expected: exit 1 because `LibraryEditor.WtlConversionBatch` and the explicit-output overload do not exist.

- [ ] **Step 3: Preserve the old output overload and add the explicit path overload**

Implement:

```csharp
public void ToMLibrary(bool crypt)
{
    ToMLibrary(crypt, Path.ChangeExtension(_fileName, ".Zl"));
}

public void ToMLibrary(bool crypt, string outputFileName)
{
    string fileName = outputFileName;
    // retain the existing body unchanged from the old method after fileName assignment
}
```

Reject a null or empty `outputFileName` with `ArgumentException`. Do not add configuration options.

- [ ] **Step 4: Implement the focused batch service**

Implement `WtlConversionBatch.cs` with these exact result types and behaviors:

```csharp
internal sealed class WtlConversionFailure
{
    public string FileName { get; private set; }
    public string Message { get; private set; }

    public WtlConversionFailure(string fileName, string message)
    {
        FileName = fileName;
        Message = message;
    }
}

internal sealed class WtlConversionBatchResult
{
    public int SuccessCount { get; set; }
    public List<WtlConversionFailure> Failures { get; private set; }
    public List<string> OutputFiles { get; private set; }

    public WtlConversionBatchResult()
    {
        Failures = new List<WtlConversionFailure>();
        OutputFiles = new List<string>();
    }
}
```

Implement folder discovery exactly as follows:

```csharp
internal static string[] GetTopLevelWtlFiles(string folderPath)
{
    return Directory.GetFiles(folderPath, "*.wtl", SearchOption.TopDirectoryOnly)
        .OrderBy(x => x, StringComparer.OrdinalIgnoreCase)
        .ToArray();
}
```

For each file in `ConvertFiles`:

```csharp
string outputDirectory = Path.Combine(Path.GetDirectoryName(fileName), "ConvertedZL");
Directory.CreateDirectory(outputDirectory);
string outputFile = Path.Combine(outputDirectory, Path.GetFileNameWithoutExtension(fileName) + ".Zl");

WTL1to1ZL library = null;
try
{
    library = new WTL1to1ZL(fileName);
    library.ToMLibrary(crypt, outputFile);
    // increment success and record outputFile
}
catch (Exception ex)
{
    // record fileName and ex.GetBaseException().Message, then continue
}
finally
{
    if (library != null) library.Dispose();
}
```

If `fileNames` is empty, return zero counts without creating a directory. Keep conversion sequential.

- [ ] **Step 5: Add the new source file to the project**

Add exactly:

```xml
<Compile Include="WtlConversionBatch.cs" />
```

inside the existing compile `ItemGroup`.

- [ ] **Step 6: Rebuild and verify GREEN**

Run the isolated x64 Release build, then the full focused contract.

Expected: build exit 0; contract exit 0; one valid output, one recorded failure, nested file ignored, `TOTAL ... FAIL 0`.

- [ ] **Step 7: Record the non-Git checkpoint**

Record exact hashes for the three changed/created implementation files and the contract. Verify `Graphics/WTLLibrary.cs` is unchanged.

---

### Task 3: Add Explicit File and Folder UI Commands

**Files:**
- Modify: `D:\相聚假人\Source\LibraryEditor\LMain.cs:345-384`
- Modify: `D:\相聚假人\Source\LibraryEditor\LMain.Designer.cs:258-294,1007-1022`
- Test: `D:\相聚假人\Source\LibraryEditor\.diagnostics\test_wtl_v2_batch_conversion_contract.ps1`

**Interfaces:**
- Consumes: `WtlConversionBatch.ConvertFiles(...)` and `GetTopLevelWtlFiles(...)` from Task 2.
- Produces: menu commands “批量选择 WTL 转换 ZL” and “选择文件夹转换 WTL 到 ZL”.

- [ ] **Step 1: Add failing UI source contracts**

Add assertions that compiled `LMain` contains two distinct event handlers and that source contains:

```text
OpenFileDialog.Multiselect = true
FolderBrowserDialog
WtlConversionBatch.GetTopLevelWtlFiles
WtlConversionBatch.ConvertFiles
```

Also assert the two exact Chinese menu captions are present in `LMain.Designer.cs`.

- [ ] **Step 2: Run the contract and verify RED**

Expected: exit 1 because the folder menu and handler do not exist and the existing caption is unchanged.

- [ ] **Step 3: Refactor the existing file handler to the shared batch service**

Keep its multiselect dialog and existing encryption prompt. Replace the `Parallel.For` and unconditional success message with one call to `ConvertFiles` followed by a shared result-summary method.

The summary must state:

```text
转换完成
成功：<count>
失败：<count>
输出目录：各源文件目录\ConvertedZL
失败文件：
<one file and base error per line, only when failures exist>
```

- [ ] **Step 4: Add the folder handler**

Instantiate `FolderBrowserDialog` in the handler. After OK, call `GetTopLevelWtlFiles(selectedPath)`. If no files are returned, show `所选文件夹当前层没有 WTL 文件。` and return before asking for encryption or creating `ConvertedZL`.

Reuse the same encryption selection, batch conversion, and summary methods as the file handler.

- [ ] **Step 5: Wire the Designer menu**

Rename the existing menu caption to `批量选择 WTL 转换 ZL`. Add one `ToolStripMenuItem` field, initialize it, append it immediately after the existing WTL command, set its caption to `选择文件夹转换 WTL 到 ZL`, and wire its click event to the folder handler. Match existing Designer style and do not reformat unrelated generated code.

- [ ] **Step 6: Rebuild and verify GREEN**

Run the isolated x64 Release build and focused contract.

Expected: build exit 0; all parser, batch, continuation, output, and UI contract assertions pass.

- [ ] **Step 7: Record the non-Git checkpoint**

Record hashes for `LMain.cs`, `LMain.Designer.cs`, the isolated executable, and all prior owned files. Confirm no other source file changed.

---

### Task 4: End-to-End Isolated Acceptance

**Files:**
- Test inputs: copies under `D:\Video\好玩新服4区完整端.rar\Tools\MonsterZL-Test\BatchInput`
- Generated outputs: `D:\Video\好玩新服4区完整端.rar\Tools\MonsterZL-Test\BatchInput\ConvertedZL`
- Build artifact: `D:\相聚假人\Source\.artifacts\wtl-converter-fixed\Z3专用客户端素材编辑器.exe`

**Interfaces:**
- Consumes: completed isolated build and real `Equip.wtl` plus one previously working V2 sample.
- Produces: verifiable Black-Dragon ZL files without deployment.

- [ ] **Step 1: Prepare exact isolated inputs**

Create `BatchInput`, then copy—not move—`Equip.wtl` and `MagicEx11.wtl` from the Data directory. Record source and copy SHA-256 values and require each pair to match.

- [ ] **Step 2: Run the batch conversion contract against both copies**

Invoke `WtlConversionBatch.ConvertFiles` through the focused contract with both copied inputs.

Expected: success 2, failure 0; exactly two `.Zl` files under `BatchInput\ConvertedZL`; none beside the input WTL files.

- [ ] **Step 3: Validate target file structure**

For each generated file:

```powershell
# Assert the initial ASCII bytes contain "Black-Dragon Version".
# Instantiate LibraryEditor.BlackDragonLibrary against the generated path.
# Assert Equip.Zl has 20000 image slots and no open/decompression exception.
```

Expected: both generated files reopen successfully; `Equip.Zl` has 20,000 slots.

- [ ] **Step 4: Re-run the complete focused contract fresh**

Run the focused contract once more from a clean temporary directory.

Expected: exit 0 and `TOTAL ... FAIL 0`.

- [ ] **Step 5: Re-run the x64 Release build fresh**

Delete only the verified isolated artifact directory, rebuild with the Task 1 command, and confirm MSBuild exit 0. Do not delete or clean any broad source/output root.

- [ ] **Step 6: Verify scope and protected hashes**

Expected changed source set:

```text
LibraryEditor/.diagnostics/test_wtl_v2_batch_conversion_contract.ps1
LibraryEditor/Graphics/WTL1to1ZL.cs
LibraryEditor/WtlConversionBatch.cs
LibraryEditor/LMain.cs
LibraryEditor/LMain.Designer.cs
LibraryEditor/LibraryEditor.csproj
docs/superpowers/specs/2026-09-08-wtl-batch-folder-conversion-design.md
docs/superpowers/plans/2026-09-08-wtl-batch-folder-conversion.md
```

Confirm the original `Equip.wtl`, current `Z3素材编辑器.exe`, and `Graphics/WTLLibrary.cs` still match their Task 1 hashes. Report that live GUI clicking has not been claimed unless actually performed.

- [ ] **Step 7: Return structured evidence to the primary task**

Report exact changed files, focused RED and GREEN output, build command/exit code, generated paths and hashes, BlackDragon reopen results, protected hashes, and any unperformed manual UI acceptance. Do not deploy, replace executables, create a PR, or claim Git state.
