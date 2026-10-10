using Client.Envir;
using System.IO.Compression;

int passed = 0;
void Check(bool condition, string name)
{
    if (!condition) throw new Exception(name);
    Console.WriteLine("PASS " + name);
    passed++;
}
void Reject(Action action, string name)
{
    try { action(); } catch (InvalidDataException) { Check(true, name); return; }
    catch (EndOfStreamException) { Check(true, name); return; }
    throw new Exception(name);
}
byte[] Deflate(byte[] bytes)
{
    using var output = new MemoryStream();
    using (var stream = new DeflateStream(output, CompressionLevel.Fastest, true)) stream.Write(bytes);
    return output.ToArray();
}
MapImagePixels.Plane Plane(byte[] bytes, byte type) => new(bytes.Length, 4, 4, type);
var empty = new MapImagePixels.Plane(0, 0, 0, 0);
bool Visible(float x, float y, int w = 96, int h = 64, int ox = 0, int oy = 0,
    float zoom = 1, int ui = 0) => MapImageVisibility.Intersects(x, y, w, h, ox, oy, zoom, ui, 1280, 720);
Check(Visible(600, 300), "Visible floor tile retains its loading path");
Check(!Visible(100, 1000), "Offscreen lower rows do not start loading");
Check(!Visible(-200, 100) && !Visible(1400, 100) && !Visible(100, -200), "Cull completely offscreen sprites on every edge");
Check(Visible(100, -63) && Visible(-95, 100) && Visible(1279, 719), "Keep partial sprites across screen edges");
Check(Visible(100, 800 - 512, 96, 512), "Tall building anchored below screen still renders");
Check(!Visible(100, 1200 - 128, 96, 128), "Small building entirely below screen stays deferred");
Check(Visible(1400, 100, ox: -200) && !Visible(1200, 100, ox: 200), "Apply signed sprite offsets before clipping");
Check(Visible(100, 800, oy: -200) && !Visible(100, 600, oy: 200), "Vertical offsets preserve overhanging map decorations");
Check(Visible(2000, 100, zoom: .5f) && !Visible(1000, 100, zoom: 2), "Use scaled sprite bounds and target dimensions");
Check(Visible(2300, 100, zoom: .5f, ui: 100) && !Visible(2300, 100, zoom: .5f, ui: 200), "Respect UI offset in scaled draws");
Check(Visible(1200, 100, ui: 200), "Unit-scale path ignores unused UI offset like Sprite.Draw");
Check(Visible(-3, 100, 1, 1), "Include texture block padding near edges");
Check(Visible(-97, 100) && Visible(1281, 100), "Conservative pixel guard avoids filtering-edge gaps");
Check(Visible(10000, 10000, w: 0) && Visible(10000, 10000, zoom: float.NaN), "Unknown bounds retain original validation path");

// Compare loading candidates from the existing overscan with all rectangles
// that truly touch the viewport. The +25 lower rows remain available for tall
// buildings, while completely hidden pictures cannot consume loading slots.
int candidates = 0, retained = 0;
for (int y = -128; y <= 720 + 25 * 32; y += 32)
    for (int x = -192; x <= 1280 + 192; x += 48)
    {
        candidates++;
        bool visible = Visible(x, y);
        if (visible) retained++;
        if (x < 1280 && y < 720 && x + 96 > 0 && y + 64 > 0 && !visible)
            throw new Exception("Culling lost a visible map rectangle.");
    }
Check(retained < candidates / 2, "Overscan fixture removes hidden loading candidates without losing screen coverage");
byte[] greenDxt1 = { 0xE0, 0x07, 0, 0, 0, 0, 0, 0 };
byte[] greenDxt3 = Enumerable.Repeat((byte)255, 8).Concat(greenDxt1).ToArray();
byte[] greenDxt5 = new byte[] { 255, 255, 0, 0, 0, 0, 0, 0 }.Concat(greenDxt1).ToArray();
bool Green(byte[] pixels) => pixels.Length == 64 && Enumerable.Range(0, 16).All(i => pixels[i * 4] == 0 && pixels[i * 4 + 1] == 255 && pixels[i * 4 + 2] == 0 && pixels[i * 4 + 3] == 255);
foreach (var (type, bytes) in new[] { ((byte)1, greenDxt1), ((byte)3, greenDxt3), ((byte)5, greenDxt5) })
{
    var pixels = MapImagePixels.Decode(bytes, true, Plane(bytes, type), empty, empty);
    Check(Green(pixels.Image) && pixels.Shadow == null && pixels.Overlay == null, "Zircon DXT" + type);
    var compressed = Deflate(bytes);
    pixels = MapImagePixels.Decode(compressed, false, Plane(compressed, type), empty, empty);
    Check(Green(pixels.Image), "BlackDragon Deflate + DXT" + type);
}
byte[] image = Deflate(greenDxt1), shadow = Deflate(greenDxt3), overlay = Deflate(greenDxt5);
var combined = MapImagePixels.Decode(image.Concat(shadow).Concat(overlay).ToArray(), false, Plane(image, 1), Plane(shadow, 3), Plane(overlay, 5));
Check(Green(combined.Image) && Green(combined.Shadow) && Green(combined.Overlay), "Independent image, shadow and overlay offsets");
byte[] raw = Enumerable.Range(0, 64).Select(i => (byte)i).ToArray();
byte[] rawCompressed = Deflate(raw);
Check(MapImagePixels.Decode(rawCompressed, false, Plane(rawCompressed, 32), empty, empty).Image.SequenceEqual(raw), "RGBA bytes preserved");
Reject(() => MapImagePixels.Decode(image[..^1], false, Plane(image, 1), empty, empty), "Reject truncated combined payload");
Reject(() => MapImagePixels.Decode(new byte[4], true, new(4, 4, 4, 1), empty, empty), "Reject short DXT block");
Reject(() => MapImagePixels.Decode(new byte[4], true, new(4, 4, 4, 32), empty, empty), "Reject wrong decoded pixel length");
Reject(() => MapImagePixels.Decode(image, false, new(image.Length, 0, 4, 1), empty, empty), "Reject zero texture width");

var queue = new BudgetedPreloadQueue<int>();
queue.Add(1); queue.Add(1); queue.Add(2);
Check(queue.Count == 2, "Deduplicate shared tile textures");
var calls = new List<int>();
queue.Process(item => { calls.Add(item); return item == 2; }, 6, TimeSpan.FromSeconds(1));
Check(calls.SequenceEqual(new[] { 1, 2 }) && queue.Count == 1, "Unready tile cannot block ready neighbours or spin within a frame");
queue.Add(2);
Check(queue.Count == 1, "Do not repeat completed requests in the same region");
queue.Process(item => true, 6, TimeSpan.FromSeconds(1));
Check(queue.Count == 0, "Retry asynchronous tile on a later frame");
queue.Clear();
for (int i = 0; i < 600; i++) queue.Add(i);
Check(queue.Count == 512, "Bound speculative work per region");
queue.Process(item => true, 6, TimeSpan.FromSeconds(1));
Check(queue.Count == 506, "Cap additional requests in one frame");
queue.Process(item => true, 6, TimeSpan.Zero);
Check(queue.Count == 506, "No work when time budget is exhausted");
calls.Clear();
queue.Process(item => { calls.Add(item); Thread.Sleep(15); return true; }, 6, TimeSpan.FromMilliseconds(2));
Check(calls.Count == 1, "Do not start another upload after expensive preparation");
queue.Clear(); queue.Add(1);
Check(queue.Count == 1, "Discard old region when map or destination changes");
if (args.Length == 1) passed += ActualMapImages.Run(args[0]);
var preparation = new MapPixelPreparation();
var ready = preparation.TryStart(greenDxt1, true, Plane(greenDxt1, 1), empty, empty, DateTime.UtcNow);
await ready.Task.WaitAsync(TimeSpan.FromSeconds(5));
Check(Green(ready.Take().Image) && preparation.Count == 0, "Worker prepares pixels without GPU access and releases memory after upload handoff");

var jobs = new List<MapPixelPreparation.Pending>();
for (int i = 0; i < 32; i++)
    jobs.Add(preparation.TryStart(greenDxt1, true, Plane(greenDxt1, 1), empty, empty, DateTime.UtcNow));
await Task.WhenAll(jobs.Select(job => job.Task)).WaitAsync(TimeSpan.FromSeconds(5));
Check(preparation.Count == 32 && preparation.TryStart(greenDxt1, true, Plane(greenDxt1, 1), empty, empty, DateTime.UtcNow) == null, "Bound completed and running CPU preparations together");
preparation.CancelAll();
Check(preparation.Count == 0 && jobs.All(job => job.Take() == null), "Teleport cancellation discards stale pixels and frees capacity");

var now = DateTime.UtcNow;
var old = preparation.TryStart(greenDxt1, true, Plane(greenDxt1, 1), empty, empty, now);
await old.Task.WaitAsync(TimeSpan.FromSeconds(5));
var replacement = preparation.TryStart(greenDxt1, true, Plane(greenDxt1, 1), empty, empty, now.AddSeconds(6));
await replacement.Task.WaitAsync(TimeSpan.FromSeconds(5));
Check(old.Cancelled && preparation.Count == 1 && Green(replacement.Take().Image), "Expire unused completed preparations instead of retaining pixels indefinitely");

var oversized = preparation.TryStart(raw, true, new(raw.Length, 4096, 2048, 32), empty, empty, DateTime.UtcNow);
try { await oversized.Task.WaitAsync(TimeSpan.FromSeconds(5)); } catch (InvalidDataException) { }
Check(preparation.TryStart(greenDxt1, true, Plane(greenDxt1, 1), empty, empty, DateTime.UtcNow) == null, "Bound total decoded pixel memory even for a large pending plane");
Reject(() => oversized.Take(), "Decode errors propagate to game-thread recovery");
Check(preparation.Count == 0, "Failed preparation releases its memory budget");

jobs.Clear();
for (int i = 0; i < 32; i++)
    jobs.Add(preparation.TryStart(greenDxt1, true, Plane(greenDxt1, 1), empty, empty, DateTime.UtcNow));
var tasks = jobs.Select(job => job.Task).ToArray();
preparation.CancelAll();
await Task.WhenAll(tasks).WaitAsync(TimeSpan.FromSeconds(5));
await Task.Delay(20); // Completion callbacks release cancelled workers.
Check(preparation.Count == 0 && jobs.All(job => job.Cancelled), "Cancel queued CPU work during rapid successive teleports");
Console.WriteLine($"Passed {passed} map loading checks.");
