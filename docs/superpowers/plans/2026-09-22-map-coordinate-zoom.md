# Map Coordinate Zoom Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 统一地图坐标按钮字体，并消除底图缩放时的宽高拉伸和低质量插值。

**Architecture:** `MapCoordinateCanvas` 暴露底图原始尺寸并负责高质量绘制；`MapCoordinateForm` 使用该尺寸计算适配和缩放后的画布大小。按钮工厂统一赋予同一字体。

**Tech Stack:** .NET Framework WinForms、System.Drawing、VS 2022 MSBuild。

## Global Constraints

- 不修改地图、数据库、MiniMap.Zl。
- 无底图时保留现有黑色坐标画布。
- 不修改主资源编辑器的图片缩放功能。

---

### Task 1: 缩放比例与按钮字体契约

**Files:**
- Create temporarily: `.diagnostics/VerifyMapCoordinateZoom.cs`
- Modify: `LibraryEditor/MapCoordinateForm.cs`
- Modify: `LibraryEditor/MapCoordinateCanvas.cs`

**Interfaces:**
- `MapCoordinateCanvas.SourceImageSize : Size`
- `MapCoordinateForm.ResizeCanvas(bool source)` consumes `SourceImageSize`

- [ ] 写入诊断程序，断言 900×600 底图缩放后仍为 3:2，并断言地图坐标按钮字体一致。
- [ ] 在修改前运行诊断程序，确认因画布为正方形或接口不存在而失败。
- [ ] 添加 `SourceImageSize`，按图片尺寸计算 fit/zoom；无图片时使用地图尺寸。
- [ ] 将底图绘制切换为高质量双三次插值。
- [ ] 让按钮工厂统一使用 9pt Microsoft YaHei UI。
- [ ] 重建并重新运行诊断程序，确认比例、字体和真实底图加载通过。
- [ ] 删除临时诊断程序，不提交或推送。
