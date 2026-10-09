param(
    [switch]$ParserOnly,
    [switch]$RendererOnly,
    [switch]$CanvasOnly,
    [switch]$RealDataOnly,
    [string]$AssemblyPath = '',
    [string]$RealMapPath = '',
    [string]$PreviewPath = ''
)

$ErrorActionPreference = 'Stop'

function Assert-Contract([bool]$condition, [string]$message) {
    if (-not $condition) { throw $message }
}

$root = Split-Path -Parent $PSScriptRoot
$localOutput = [IO.Path]::GetFullPath((Join-Path $root '..\..\..\Debug\LibraryEditor'))
$defaultAssembly = Get-ChildItem -LiteralPath $localOutput -Filter '*.exe' -ErrorAction SilentlyContinue |
    Select-Object -First 1 -ExpandProperty FullName
if ([string]::IsNullOrWhiteSpace($defaultAssembly)) {
    $defaultAssembly = Get-ChildItem -LiteralPath 'D:\Debug\LibraryEditor' -Filter '*.exe' -ErrorAction SilentlyContinue |
        Select-Object -First 1 -ExpandProperty FullName
}
if ([string]::IsNullOrWhiteSpace($AssemblyPath)) { $AssemblyPath = $defaultAssembly }
if (-not (Test-Path -LiteralPath $AssemblyPath)) {
    $AssemblyPath = Join-Path $root 'LibraryEditor\bin\Debug\Z3专用客户端素材编辑器.exe'
}
Assert-Contract (Test-Path -LiteralPath $AssemblyPath) "LibraryEditor assembly not found: $AssemblyPath"

$tempRoot = Join-Path ([IO.Path]::GetTempPath()) ('map-coordinate-contract-' + [Guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $tempRoot | Out-Null
$harnessSource = Join-Path $tempRoot 'ContractHarness.cs'
$harnessExe = Join-Path $tempRoot 'ContractHarness.exe'
$mode = if ($ParserOnly) { 'parser' } elseif ($RendererOnly) { 'renderer' } elseif ($CanvasOnly) { 'canvas' } elseif ($RealDataOnly) { 'real' } else { 'all' }

$harness = @'
using System;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Runtime.Serialization;
using System.Windows.Forms;

internal static class ContractHarness
{
    private static readonly BindingFlags AnyInstance = BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic;
    private static readonly BindingFlags AnyStatic = BindingFlags.Static | BindingFlags.Public | BindingFlags.NonPublic;
    private static Assembly Product;

    private static Type ProductType(string name)
    {
        return Product.GetType("LibraryEditor." + name, true);
    }

    private static object New(string typeName, params object[] args)
    {
        return Activator.CreateInstance(ProductType(typeName), AnyInstance, null, args, null);
    }

    private static object Get(object instance, string name)
    {
        FieldInfo field = instance.GetType().GetField(name, AnyInstance);
        if (field != null) return field.GetValue(instance);
        PropertyInfo property = instance.GetType().GetProperty(name, AnyInstance);
        if (property != null) return property.GetValue(instance, null);
        throw new MissingMemberException(instance.GetType().FullName, name);
    }

    private static void Set(object instance, string name, object value)
    {
        FieldInfo field = instance.GetType().GetField(name, AnyInstance);
        if (field != null) { field.SetValue(instance, value); return; }
        PropertyInfo property = instance.GetType().GetProperty(name, AnyInstance);
        if (property != null) { property.SetValue(instance, value, null); return; }
        throw new MissingMemberException(instance.GetType().FullName, name);
    }

    private static object Invoke(object instance, string name, params object[] args)
    {
        MethodInfo method = instance.GetType().GetMethods(AnyInstance)
            .Where(item => item.Name == name && item.GetParameters().Length == args.Length)
            .FirstOrDefault();
        if (method == null) throw new MissingMethodException(instance.GetType().FullName, name);
        return method.Invoke(instance, args);
    }

    private static object InvokeStatic(Type type, string name, params object[] args)
    {
        MethodInfo method = type.GetMethods(AnyStatic)
            .Where(item => item.Name == name && item.GetParameters().Length == args.Length)
            .FirstOrDefault();
        if (method == null) throw new MissingMethodException(type.FullName, name);
        return method.Invoke(null, args);
    }

    private static object Cell(object map, int x, int y)
    {
        return Invoke(map, "GetCell", x, y);
    }

    private static void Equal(object actual, object expected, string message)
    {
        if (!object.Equals(actual, expected))
            throw new InvalidOperationException(message + ": expected " + expected + ", got " + actual);
    }

    private static string TempFile(string suffix)
    {
        return Path.Combine(Path.GetTempPath(), "map-coordinate-contract-" + Guid.NewGuid().ToString("N") + suffix);
    }

    private static void ParserContract()
    {
        Type reader = ProductType("MapFileReader");
        string customFile = TempFile(".map");
        string koreanFile = TempFile(".map");
        try
        {
            byte[] custom = new byte[8 + 26];
            custom[0] = 1; custom[2] = 0x43; custom[3] = 0x23;
            BitConverter.GetBytes((short)1).CopyTo(custom, 4);
            BitConverter.GetBytes((short)1).CopyTo(custom, 6);
            BitConverter.GetBytes((short)200).CopyTo(custom, 8);
            BitConverter.GetBytes(1).CopyTo(custom, 10);
            BitConverter.GetBytes((short)201).CopyTo(custom, 14);
            BitConverter.GetBytes((short)2).CopyTo(custom, 16);
            BitConverter.GetBytes((short)202).CopyTo(custom, 18);
            BitConverter.GetBytes((short)3).CopyTo(custom, 20);
            custom[24] = 4; custom[25] = 5; custom[26] = 6; custom[27] = 7;
            File.WriteAllBytes(customFile, custom);

            object customMap = InvokeStatic(reader, "Read", customFile);
            object customCell = Cell(customMap, 0, 0);
            Equal(Get(customCell, "FrontAnimationFrame"), (byte)4, "custom front animation frame");
            Equal(Get(customCell, "FrontAnimationTick"), (byte)5, "custom front animation tick");
            Equal(Get(customCell, "MiddleAnimationFrame"), (byte)6, "custom middle animation frame");
            Equal(Get(customCell, "MiddleAnimationTick"), (byte)7, "custom middle animation tick");

            byte[] korean = new byte[28 + 3 + 14 * 4];
            korean[0] = 0;
            BitConverter.GetBytes((short)2).CopyTo(korean, 22);
            BitConverter.GetBytes((short)2).CopyTo(korean, 24);
            korean[28] = 0; korean[29] = 0; korean[30] = 0;
            int offset = 31;
            korean[offset] = 3;
            korean[offset + 1] = 0xB2;
            korean[offset + 2] = 0xFF;
            korean[offset + 3] = 0;
            korean[offset + 4] = 1;
            korean[offset + 5] = 0; korean[offset + 6] = 0;
            korean[offset + 7] = 0; korean[offset + 8] = 0;
            File.WriteAllBytes(koreanFile, korean);

            object koreanMap = InvokeStatic(reader, "Read", koreanFile);
            object koreanCell = Cell(koreanMap, 0, 0);
            Equal(Get(koreanCell, "MiddleAnimationFrame"), (byte)0xB2, "Korean middle animation frame and blend flag");
            Equal(Get(koreanCell, "FrontAnimationFrame"), (byte)0, "Korean front animation frame");
            Equal(Get(koreanCell, "MiddleAnimationTick"), (byte)0, "Korean middle animation tick");
            Equal(Get(koreanCell, "FrontAnimationTick"), (byte)0, "Korean front animation tick");
            Console.WriteLine("parser: PASS");
        }
        finally
        {
            if (File.Exists(customFile)) File.Delete(customFile);
            if (File.Exists(koreanFile)) File.Delete(koreanFile);
        }
    }

    private static object NewMap(int width, int height)
    {
        return New("MapFileData", width, height);
    }

    private static Bitmap Image(Color color, int width, int height)
    {
        Bitmap bitmap = new Bitmap(width, height);
        using (Graphics graphics = Graphics.FromImage(bitmap)) graphics.Clear(color);
        return bitmap;
    }

    private static void RendererContract()
    {
        object map = NewMap(2, 2);
        object cell = Cell(map, 0, 0);
        Set(cell, "BackFile", (short)1); Set(cell, "BackImage", 1);
        Set(cell, "MiddleFile", (short)2); Set(cell, "MiddleImage", 1);
        Set(cell, "FrontFile", (short)3); Set(cell, "FrontImage", 1);
        object tallCell = Cell(map, 1, 1);
        Set(tallCell, "MiddleFile", (short)4); Set(tallCell, "MiddleImage", 1);

        Bitmap back = Image(Color.Red, 48, 32);
        Bitmap middle = Image(Color.Green, 48, 32);
        Bitmap front = Image(Color.Blue, 48, 32);
        Bitmap tall = Image(Color.Yellow, 20, 64);
        Bitmap animationBase = Image(Color.DarkGreen, 20, 64);
        Bitmap animationFrame = Image(Color.Magenta, 20, 64);
        Func<short, int, Image> resolve = delegate(short file, int index)
        {
            if (file == 1 && index == 0) return back;
            if (file == 2 && index == 0) return middle;
            if (file == 3 && index == 0) return front;
            if (file == 4 && index == 0) return tall;
            if (file == 5 && index == 0) return animationBase;
            if (file == 5 && index == 1) return animationFrame;
            return null;
        };

        object renderer = New("MapCoordinateTileRenderer");
        MethodInfo draw = renderer.GetType().GetMethods(AnyInstance)
            .Where(item => item.Name == "Draw" && item.GetParameters().Length == 7).FirstOrDefault();
        if (draw == null) throw new MissingMethodException("MapCoordinateTileRenderer.Draw");
        using (Bitmap canvas = new Bitmap(96, 96))
        using (Graphics graphics = Graphics.FromImage(canvas))
        {
            graphics.Clear(Color.Black);
            draw.Invoke(renderer, new object[] { graphics, map, new Rectangle(0, 0, 96, 96), Point.Empty, 1F, 0, resolve });
            Equal(canvas.GetPixel(16, 16).ToArgb(), Color.Blue.ToArgb(), "layer order Back < Middle < Front");
            Equal(canvas.GetPixel(58, 8).ToArgb(), Color.Yellow.ToArgb(), "tall object bottom alignment");
        }

        object animationCell = Cell(map, 0, 1);
        Set(animationCell, "MiddleFile", (short)5); Set(animationCell, "MiddleImage", 1);
        Set(animationCell, "MiddleAnimationFrame", (byte)3);
        using (Bitmap canvas = new Bitmap(96, 96))
        using (Graphics graphics = Graphics.FromImage(canvas))
        {
            graphics.Clear(Color.Black);
            draw.Invoke(renderer, new object[] { graphics, map, new Rectangle(0, 0, 96, 96), Point.Empty, 1F, 1, resolve });
            Equal(canvas.GetPixel(16, 48).ToArgb(), Color.Magenta.ToArgb(), "middle animation index");
        }

        Set(tallCell, "FrontFile", (short)5); Set(tallCell, "FrontImage", 1);
        Set(tallCell, "FrontAnimationFrame", (byte)2); Set(tallCell, "FrontAnimationTick", (byte)1);
        using (Bitmap canvas = new Bitmap(96, 96))
        using (Graphics graphics = Graphics.FromImage(canvas))
        {
            graphics.Clear(Color.Black);
            draw.Invoke(renderer, new object[] { graphics, map, new Rectangle(0, 0, 96, 96), Point.Empty, 1F, 2, resolve });
            Equal(canvas.GetPixel(58, 8).ToArgb(), Color.Magenta.ToArgb(), "front animation tick/index");
        }

        object missingCell = Cell(map, 1, 0);
        Set(missingCell, "MiddleFile", (short)9); Set(missingCell, "MiddleImage", 1);
        using (Bitmap canvas = new Bitmap(96, 96))
        using (Graphics graphics = Graphics.FromImage(canvas))
        {
            graphics.Clear(Color.Black);
            draw.Invoke(renderer, new object[] { graphics, map, new Rectangle(0, 0, 96, 96), Point.Empty, 1F, 0, resolve });
            Equal(canvas.GetPixel(70, 16).ToArgb(), Color.Black.ToArgb(), "missing image must be skipped");
        }

        object missingSource = New("MapCoordinateTileSource", TempFile("-missing-client-data"));
        object missingResult = Invoke(missingSource, "Resolve", (short)200, 0);
        Equal(missingResult, null, "missing library must return no image");
        Assert((bool)Get(missingSource, "HasRenderableLibraries") == false, "missing library must not enable real rendering");
        Assert((int)Get(missingSource, "MissingLibraryCount") == 1, "missing library counter must be deterministic");
        ((IDisposable)missingSource).Dispose();
        Console.WriteLine("renderer: PASS");
    }

    private static void CanvasContract()
    {
        object map = NewMap(1000, 1000);
        Type canvasType = ProductType("MapCoordinateCanvas");
        using (Control canvas = (Control)Activator.CreateInstance(canvasType, true))
        using (Panel host = new Panel { Width = 120, Height = 90, AutoScroll = true })
        {
            host.Controls.Add(canvas);
            MethodInfo setMap = canvasType.GetMethods(AnyInstance)
                .Where(item => item.Name == "SetMap" && item.GetParameters().Length >= 4).FirstOrDefault();
            if (setMap == null) throw new MissingMethodException("MapCoordinateCanvas.SetMap");
            object renderer = New("MapCoordinateTileRenderer");
            Func<short, int, Image> resolve = delegate { return null; };
            object[] args = new object[] { map, null, renderer, null, true };
            if (setMap.GetParameters().Length == 4) args = new object[] { map, null, renderer, resolve };
            setMap.Invoke(canvas, args);
            Invoke(canvas, "SetZoom", 1F);
            Size extent = (Size)Get(canvas, "VirtualExtent");
            Assert(extent.Width >= 48000 && extent.Height >= 32000, "virtual extent must use 48x32 cells");
            Assert(canvas.Width < 1000 && canvas.Height < 1000, "large map must keep a viewport-sized control");
            MethodInfo toMap = canvasType.GetMethods(AnyInstance)
                .Where(item => item.Name == "ToMapPoint" && item.GetParameters().Length == 1).FirstOrDefault();
            if (toMap == null) throw new MissingMethodException("MapCoordinateCanvas.ToMapPoint");
            Point point = (Point)toMap.Invoke(canvas, new object[] { new Point(49, 33) });
            Equal(point, new Point(1, 1), "screen coordinate conversion");

            object missingCell = Cell(map, 0, 0);
            Set(missingCell, "BackFile", (short)200);
            Set(missingCell, "BackImage", 1);
            object missingSource = New("MapCoordinateTileSource", TempFile("-missing-client-data"));
            using (Bitmap fallback = new Bitmap(1, 1))
            {
                fallback.SetPixel(0, 0, Color.Green);
                object[] fallbackArgs = new object[] { map, fallback, renderer, missingSource, true };
                setMap.Invoke(canvas, fallbackArgs);
                using (Bitmap rendered = new Bitmap(canvas.Width, canvas.Height))
                {
                    canvas.DrawToBitmap(rendered, new Rectangle(Point.Empty, canvas.Size));
                    Equal(rendered.GetPixel(5, 5).ToArgb(), Color.Green.ToArgb(),
                        "large-map MiniMap fallback must paint the visible viewport");
                }
                Assert((bool)Get(canvas, "LastFrameUsedFallback"), "missing Map Data must remain on MiniMap fallback");
            }
            ((IDisposable)missingSource).Dispose();
            setMap.Invoke(canvas, new object[] { map, null, renderer, null, false });
            using (Form window = new Form { ClientSize = new Size(140, 110) })
            {
                window.Controls.Add(host);
                window.Show();
                Application.DoEvents();
                host.AutoScrollPosition = new Point(96, 64);
                Application.DoEvents();
                Equal(canvas.Location, Point.Empty, "scroll must keep canvas pinned to viewport");
                Equal((Point)toMap.Invoke(canvas, new object[] { new Point(1, 1) }),
                    new Point(2, 2), "scrolled screen coordinate conversion");
                window.Close();
            }
        }
        using (Form mapForm = (Form)New("MapCoordinateForm", string.Empty))
        {
            mapForm.CreateControl();
            Panel leftHost = (Panel)Get(mapForm, "_leftCanvasHost");
            Control leftCanvas = (Control)Get(mapForm, "_leftCanvas");
            Assert(leftHost.ClientSize.Width > 2 && leftHost.ClientSize.Height > 2, "map pane must have a viewport");
            object largeMap = NewMap(800, 800);
            Set(mapForm, "_leftMapData", largeMap);
            Invoke(leftCanvas, "SetMap", largeMap, null);
            Invoke(mapForm, "FitMap", true);
            Size fitted = (Size)Get(leftCanvas, "VirtualExtent");
            Assert(fitted.Width <= leftHost.ClientSize.Width && fitted.Height <= leftHost.ClientSize.Height,
                "default zoom must show the entire large map");
            Assert((float)Get(leftCanvas, "Zoom") < 0.05F, "large-map overview must use MiniMap when available");
            object overviewCell = Cell(largeMap, 0, 0);
            Set(overviewCell, "BackFile", (short)200);
            Set(overviewCell, "BackImage", 1);
            object overviewSource = New("MapCoordinateTileSource", TempFile("-missing-overview-data"));
            using (Bitmap miniMap = Image(Color.Green, 2, 2))
            using (Bitmap overview = new Bitmap(leftCanvas.Width, leftCanvas.Height))
            {
                Invoke(leftCanvas, "SetMap", largeMap, miniMap, New("MapCoordinateTileRenderer"), overviewSource, true);
                Invoke(mapForm, "FitMap", true);
                leftCanvas.DrawToBitmap(overview, new Rectangle(Point.Empty, overview.Size));
                Color overviewColor = overview.GetPixel(overview.Width / 2, overview.Height / 2);
                Assert(overviewColor.G > 80 && overviewColor.R == 0 && overviewColor.B == 0,
                    "full-map overview must display MiniMap");
                Assert(!(bool)Get(leftCanvas, "LastFrameUsedFallback"), "intentional overview must not report missing real tiles");
                Equal(Get(overviewSource, "MissingLibraryCount"), 0, "full-map overview must not load every real tile");
            }
            ((IDisposable)overviewSource).Dispose();
            Invoke(mapForm, "ResetZoom", true);
            Equal(Get(leftCanvas, "Zoom"), 1F, "reset must retain 1:1 pixels");
        }
        Console.WriteLine("canvas: PASS");
    }

    private static void RealDataContract(string mapPath, string dataPath, string previewPath)
    {
        Type lmainType = ProductType("LMain");
        object fakeMain = FormatterServices.GetUninitializedObject(lmainType);
        FieldInfo progressField = lmainType.GetField("toolStripProgressBar", AnyInstance);
        progressField.SetValue(fakeMain, new ToolStripProgressBar());
        lmainType.GetField("form1", AnyStatic).SetValue(null, fakeMain);

        object map = InvokeStatic(ProductType("MapFileReader"), "Read", mapPath);
        object source = New("MapCoordinateTileSource", dataPath);
        MethodInfo resolve = source.GetType().GetMethod("Resolve", AnyInstance);
        int width = (int)Get(map, "Width");
        int height = (int)Get(map, "Height");
        int backResolved = 0;
        int middleResolved = 0;
        int frontResolved = 0;
        string backSample = string.Empty;
        string middleSample = string.Empty;
        string frontSample = string.Empty;
        for (int x = 0; x < width; x++)
            for (int y = 0; y < height; y++)
            {
                object cell = Cell(map, x, y);
                int backFile = (short)Get(cell, "BackFile");
                int backIndex = (int)Get(cell, "BackImage") - 1;
                int middleFile = (short)Get(cell, "MiddleFile");
                int middleIndex = (int)Get(cell, "MiddleImage") - 1;
                int frontFile = (short)Get(cell, "FrontFile");
                int frontIndex = ((int)Get(cell, "FrontImage") & 0x7FFF) - 1;
                if (backResolved == 0 && backFile >= 0 && backIndex >= 0)
                {
                    Image image = (Image)resolve.Invoke(source, new object[] { (short)backFile, backIndex });
                    if (image != null) { backResolved = 1; backSample = backFile + ":" + backIndex + "=" + image.Width + "x" + image.Height; }
                }
                if (middleResolved == 0 && middleFile >= 0 && middleIndex >= 0)
                {
                    Image image = (Image)resolve.Invoke(source, new object[] { (short)middleFile, middleIndex });
                    if (image != null) { middleResolved = 1; middleSample = middleFile + ":" + middleIndex + "=" + image.Width + "x" + image.Height; }
                }
                if (frontResolved == 0 && frontFile >= 0 && frontIndex >= 0)
                {
                    Image image = (Image)resolve.Invoke(source, new object[] { (short)frontFile, frontIndex });
                    if (image != null) { frontResolved = 1; frontSample = frontFile + ":" + frontIndex + "=" + image.Width + "x" + image.Height; }
                }
                if (backResolved > 0 && middleResolved > 0 && frontResolved > 0) break;
            }
        Console.WriteLine("real map=" + Path.GetFileName(mapPath) + " size=" + width + "x" + height);
        Console.WriteLine("real Back=" + backResolved + " " + backSample);
        Console.WriteLine("real Middle=" + middleResolved + " " + middleSample);
        Console.WriteLine("real Front=" + frontResolved + " " + frontSample);
        Console.WriteLine("real HasRenderableLibraries=" + Get(source, "HasRenderableLibraries"));
        Console.WriteLine("real MissingLibraries=" + Get(source, "MissingLibraryCount") + " MissingImages=" + Get(source, "MissingImageCount"));
        object renderer = New("MapCoordinateTileRenderer");
        Func<short, int, Image> resolver = delegate(short file, int index)
        {
            return (Image)resolve.Invoke(source, new object[] { file, index });
        };
        MethodInfo draw = renderer.GetType().GetMethods(AnyInstance)
            .Where(item => item.Name == "Draw" && item.GetParameters().Length == 7).FirstOrDefault();
        using (Bitmap rendered = new Bitmap(string.IsNullOrEmpty(previewPath) ? 192 : 768,
            string.IsNullOrEmpty(previewPath) ? 128 : 512))
        using (Graphics graphics = Graphics.FromImage(rendered))
        {
            graphics.Clear(Color.Black);
            draw.Invoke(renderer, new object[] { graphics, map, new Rectangle(Point.Empty, rendered.Size), Point.Empty, 1F, 0, resolver });
            if (!string.IsNullOrEmpty(previewPath))
                rendered.Save(previewPath, System.Drawing.Imaging.ImageFormat.Png);
        }
        int renderedTiles = (int)Get(renderer, "RenderedTileCount");
        Console.WriteLine("real RenderedTiles=" + renderedTiles);
        Assert(renderedTiles > 0, "real renderer did not draw any map tile");
        Invoke(source, "ClearCache");
        Assert(!(bool)Get(source, "HasRenderableLibraries"), "map switch must release old libraries");
        Assert((int)Get(source, "MissingLibraryCount") == 0, "map switch must reset missing-resource status");
        if (backResolved > 0)
        {
            string[] sample = backSample.Split(new char[] { ':', '=' });
            Image reopened = (Image)resolve.Invoke(source, new object[] { short.Parse(sample[0]), int.Parse(sample[1]) });
            Assert(reopened != null, "other visible map must reload a shared library after switch");
        }
        ((IDisposable)source).Dispose();
        Assert(backResolved > 0 && middleResolved > 0 && frontResolved > 0, "real client did not resolve all three map layers");
        Console.WriteLine("real-data: PASS");
    }

    private static void Assert(bool condition, string message)
    {
        if (!condition) throw new InvalidOperationException(message);
    }

    public static int Main(string[] args)
    {
        try
        {
            Product = Assembly.LoadFrom(args[0]);
            string mode = args.Length > 1 ? args[1] : "all";
            if (mode == "parser" || mode == "all") ParserContract();
            if (mode == "renderer" || mode == "all") RendererContract();
            if (mode == "canvas" || mode == "all") CanvasContract();
            if (mode == "real") RealDataContract(args[2], args[3], args.Length > 4 ? args[4] : string.Empty);
            return 0;
        }
        catch (Exception ex)
        {
            Console.Error.WriteLine(ex.ToString());
            return 1;
        }
    }
}
'@

try {
    [IO.File]::WriteAllText($harnessSource, $harness)
    $csc = Join-Path $env:WINDIR 'Microsoft.NET\Framework\v4.0.30319\csc.exe'
    Assert-Contract (Test-Path -LiteralPath $csc) "x86 C# compiler not found: $csc"
    & $csc /nologo /target:exe /platform:x86 /out:$harnessExe /r:System.dll /r:System.Core.dll /r:System.Drawing.dll /r:System.Windows.Forms.dll $harnessSource
    Assert-Contract ($LASTEXITCODE -eq 0) 'Contract harness compilation failed.'
    if ($mode -eq 'real') {
        $clientRoot = Get-ChildItem -LiteralPath 'D:\Debug' -Directory -ErrorAction SilentlyContinue |
            Where-Object { Test-Path -LiteralPath (Join-Path $_.FullName 'Client\Data') } |
            Select-Object -First 1 -ExpandProperty FullName
        Assert-Contract (-not [string]::IsNullOrWhiteSpace($clientRoot)) 'Real client root not found below D:\Debug.'
        $realMap = if ([string]::IsNullOrWhiteSpace($RealMapPath)) { Join-Path $clientRoot 'Client\Map\0_000.map' } else { $RealMapPath }
        $realData = Join-Path $clientRoot 'Client\Data'
        Assert-Contract (Test-Path -LiteralPath $realMap) "Real map not found: $realMap"
        & $harnessExe $AssemblyPath $mode $realMap $realData $PreviewPath
    }
    else {
        & $harnessExe $AssemblyPath $mode
    }
    $exitCode = $LASTEXITCODE
    Assert-Contract ($exitCode -eq 0) "Map-coordinate contract failed with exit code $exitCode."
}
finally {
    if (Test-Path -LiteralPath $tempRoot) { Remove-Item -LiteralPath $tempRoot -Recurse -Force }
}
