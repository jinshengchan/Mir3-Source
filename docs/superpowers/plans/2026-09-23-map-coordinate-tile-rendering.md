# Map Coordinate Tile Rendering Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Render the map-coordinate editor from the real `.map` Back, Middle, and Front layers with the same placement rules as the built-in map editor, while preserving the existing coordinate-editing behavior and MiniMap fallback.

**Architecture:** Extend the existing parser with animation metadata already present in the supported map formats. Add a focused GDI+ tile-rendering unit backed by a shared lazy ZL resource cache, then make `MapCoordinateCanvas` a virtual scrolling viewport that draws only visible cells and existing overlays. `MapCoordinateForm` owns the shared cache and selects real-layer rendering or the existing MiniMap fallback.

**Tech Stack:** C# compatible with .NET Framework 4.8, WinForms, System.Drawing/GDI+, existing `BlackDragonLibrary`, existing `Library.Libraries` path and `KROrder` mappings, MSBuild Debug/x86.

## Global Constraints

- Preserve all current uncommitted LibraryEditor work; do not recreate or revert existing appearance, item-settings, merge-preview, map-coordinate, font, layout, or zoom changes.
- Support only the two map formats currently accepted by `MapFileReader`: Korean Mir3 and C# custom format.
- Do not add SharpDX, DevExpress, ServerTool project references, NuGet packages, or deployment changes.
- Do not modify, copy, convert, rename, or overwrite any file below the selected Client directory.
- Keep map connection read, edit, save, database, marker, blocked-cell, and selection behavior unchanged.
- Missing map libraries or image indexes must never stop the window; skip individual tiles and fall back to `MiniMap.Zl` only when no real tile layer can be rendered.
- Use nearest-neighbor scaling for map artwork and normal GDI+ drawing for text and overlays.
- Do not commit, push, create a PR, or alter branches. Report the complete diff and verification evidence to the primary task.

---

### Task 1: Preserve map animation metadata in the existing parser

**Files:**
- Modify: `LibraryEditor/MapCoordinateCore.cs`
- Create: `tests/test_libraryeditor_map_coordinate_tile_rendering_contract.ps1`

**Interfaces:**
- Produces: `MapCellData.MiddleAnimationFrame`, `MiddleAnimationTick`, `FrontAnimationFrame`, and `FrontAnimationTick` as bytes.
- Preserves: `MapFileReader.Read(string fileName)`, `MapFileData.GetCell(int x, int y)`, dimensions, layer indexes, and blocked-cell semantics.

- [ ] **Step 1: Add a failing parser contract**

Create a PowerShell contract that compiles a temporary x86 reflection harness against the built LibraryEditor assembly. The harness constructs one minimal custom-format cell and one minimal Korean Mir3 cell, calls internal `MapFileReader.Read`, and verifies exact animation fields from known offsets. Remove all temporary source, map, and executable files in `finally`.

- [ ] **Step 2: Run it and observe the expected failure**

Run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\tests\test_libraryeditor_map_coordinate_tile_rendering_contract.ps1 -ParserOnly
```

Expected: non-zero because the four animation fields do not exist or do not contain fixture values.

- [ ] **Step 3: Extend both supported readers**

For Korean Mir3, read middle animation at `offset + 1` unchanged; read front animation at `offset + 2`, translate front value 255 to 0 and apply the built-in editor's `0x8F` mask. Set both ticks to 0. For each 26-byte custom cell, read front frame/tick at bytes 16/17 and middle frame/tick at bytes 18/19. Do not change existing file or image offsets.

- [ ] **Step 4: Rerun the parser contract**

Expected: exit 0 with exact values for both fixtures.

---

### Task 2: Add real-map resource lookup and three-layer drawing

**Files:**
- Create: `LibraryEditor/MapCoordinateTileRenderer.cs`
- Modify: `LibraryEditor/LibraryEditor.csproj`
- Modify: `tests/test_libraryeditor_map_coordinate_tile_rendering_contract.ps1`

**Interfaces:**
- Produce: `MapCoordinateTileSource(string dataDirectory)`, `Image Resolve(short file, int imageIndex)`, `bool HasRenderableLibraries`, and deterministic missing-library/index counters.
- Produce: `MapCoordinateTileRenderer.Draw(Graphics graphics, MapFileData map, Rectangle viewport, Point scrollOffset, float zoom, int animation, Func<short, int, Image> resolveImage)`.
- Preserve: `BlackDragonLibrary` remains the only ZL decoder used by LibraryEditor.

- [ ] **Step 1: Add a failing synthetic render contract**

Create a 96×96 bitmap, a small synthetic `MapFileData`, and solid-color fake images supplied by a resolver delegate. Assert representative pixels proving Back is behind Middle, Middle is behind Front, and tall objects bottom-align to `(cellY + 1) * 32 * zoom`. Add missing-image and animation-index cases.

- [ ] **Step 2: Run the renderer contract and observe failure**

Run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\tests\test_libraryeditor_map_coordinate_tile_rendering_contract.ps1 -RendererOnly
```

Expected: non-zero because renderer/source types do not exist.

- [ ] **Step 3: Implement the minimal tile source**

Resolve Client root as the parent of configured Data. Use `Libraries.KROrder` to map map-file numbers to `LibraryFile`, then `Libraries.LibraryList` for paths such as `Data\Map Data\Tilesc.Zl`. Open a `BlackDragonLibrary` only on first reference, share it across both canvases, validate indexes before `CreateImage`, and close/dispose every opened library exactly once.

- [ ] **Step 4: Implement built-in editor draw order**

Draw only cells intersecting the viewport plus at most 20 lower rows for tall objects:

1. Back images on even X/even Y using `(BackImage & 0x1FFFF) - 1`.
2. Middle and Front images whose native size is 48×32 or 96×64.
3. Remaining Middle objects, bottom-aligned.
4. Remaining Front objects, bottom-aligned.

Apply the Middle and Front animation formulas from `ServerTool/Views/MapViewer.cs`. Use nearest-neighbor interpolation, half-pixel offset, source-over composition, and unscaled source images.

- [ ] **Step 5: Rerun renderer and full contracts**

Run the renderer-only command and then the script without mode switches. Expected: exit 0; ordering, alignment, animation, and missing-image cases pass.

---

### Task 3: Integrate virtual scrolling, overlays, zoom, and fallback

**Files:**
- Modify: `LibraryEditor/MapCoordinateCanvas.cs`
- Modify: `LibraryEditor/MapCoordinateForm.cs`
- Modify: `tests/test_libraryeditor_map_coordinate_tile_rendering_contract.ps1`

**Interfaces:**
- Change `MapCoordinateCanvas.SetMap` to receive map data, fallback MiniMap image, shared tile renderer/source, and real-render availability.
- Preserve canvas members used by the form: `Selection`, `Markers`, `ShowBlockedCells`, `CoordinateChanged`, `SelectionChanged`, `CurrentCoordinate`, `SetSelection`, and `ClearSelection`.
- Produce: `SetZoom(float zoom)` and a virtual map extent of `map.Width * 48 * zoom` by `map.Height * 32 * zoom`, without creating a physically huge WinForms control.

- [ ] **Step 1: Add failing viewport and coordinate contracts**

Instantiate the canvas through reflection with a synthetic map, zoom, and scroll offset. Verify screen-to-map conversion, selection, markers, blocked-cell overlays, and virtual extent all use 48×32 cells. Include a large virtual map and assert the real control remains viewport-sized.

- [ ] **Step 2: Run the canvas contract and observe failure**

Run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\tests\test_libraryeditor_map_coordinate_tile_rendering_contract.ps1 -CanvasOnly
```

Expected: non-zero because the canvas still maps coordinates through MiniMap dimensions and resizes to full image.

- [ ] **Step 3: Convert canvas to a virtual scrolling viewport**

Keep the canvas at host size, store a logical scroll offset, and expose the full logical extent through WinForms scrolling. Paint real layers first, then blocked cells, markers, selection, and grid. Convert mouse coordinates with `(screen + scrollOffset) / (48×32×zoom)`. Clip overlay loops to visible cells.

- [ ] **Step 4: Integrate shared source and fallback**

Create one shared tile source after settings paths are validated and pass it to both canvases. Use real layers when at least one map library opens. If none opens, retain `GetMiniMap` and show one fallback reason in `_status`. Individual missing files or indexes only skip their tiles. Dispose the source during existing form cleanup.

- [ ] **Step 5: Preserve zoom around viewport center**

Keep current toolbar and zoom limits. Make Reset use 1.0 actual pixels. Before changing zoom, capture the map coordinate at viewport center and restore it to center afterward. Do not change selection or map connection data.

- [ ] **Step 6: Add bounded animation refresh**

Use one WinForms timer at the built-in editor's 100 ms cadence. Advance a shared animation counter only while the form is visible and either canvas has visible animated cells. Stop invalidating when no visible animated cells remain.

- [ ] **Step 7: Run all focused contracts**

Run the contract script without mode switches. Expected: exit 0 for parser, renderer, canvas, large extent, missing resources, and overlay alignment.

---

### Task 4: Build and perform real-data acceptance

**Files:**
- Modify only if a verified defect is found: files owned by Tasks 1–3.
- Treat `D:\Debug\4月18日更新\Client\Data`, `Client\Map`, and all databases as read-only.

**Interfaces:**
- Output: `D:\Debug\LibraryEditor\Z3专用客户端素材编辑器.exe` from existing Debug/x86 configuration.

- [ ] **Step 1: Rebuild with Visual Studio MSBuild**

Run:

```powershell
& 'C:\Program Files\Microsoft Visual Studio\2022\Community\MSBuild\Current\Bin\MSBuild.exe' 'LibraryEditor\LibraryEditor.csproj' /t:Rebuild /p:Configuration=Debug /p:Platform=x86 /m /v:minimal /nologo
```

Expected: exit 0 and no errors. Existing unrelated `CQZZLibrary._version` warning may remain.

- [ ] **Step 2: Run the complete contract against the rebuilt assembly**

Run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\tests\test_libraryeditor_map_coordinate_tile_rendering_contract.ps1 -AssemblyPath 'D:\Debug\LibraryEditor\Z3专用客户端素材编辑器.exe'
```

Expected: exit 0 and no temporary diagnostic files left behind.

- [ ] **Step 3: Validate one real map without writes**

Load one map known to display in the built-in editor. Record evidence that at least one Back, Middle, and Front image resolves from `Data\Map Data`, actual-layer mode is active, and a fixed cell aligns with the built-in editor.

- [ ] **Step 4: Validate fallback and responsiveness**

Use a temporary path override to a nonexistent Map Data directory without moving real resources. Confirm responsive MiniMap fallback and one status message. Repeatedly switch and zoom a large real map; confirm no unhandled exception or UI hang and stable cache ownership.

- [ ] **Step 5: Inspect scope and artifact**

Run:

```powershell
git diff --check -- LibraryEditor/MapCoordinateCore.cs LibraryEditor/MapCoordinateTileRenderer.cs LibraryEditor/MapCoordinateCanvas.cs LibraryEditor/MapCoordinateForm.cs LibraryEditor/LibraryEditor.csproj tests/test_libraryeditor_map_coordinate_tile_rendering_contract.ps1
git status --short --branch
Get-FileHash 'D:\Debug\LibraryEditor\Z3专用客户端素材编辑器.exe' -Algorithm SHA256
```

Expected: no whitespace errors; only owned files changed by this implementation; exact executable hash reported. Do not commit or create a PR.
