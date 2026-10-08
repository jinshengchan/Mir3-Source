using System.Drawing;
using Client.Models;

namespace Library
{
    public enum LibraryFile { Title }
    public enum MirDirection { Up }
    public enum BlendType { NORMAL }
    public enum ImageType { Image }
    public enum MagicType { DragonTornado, Cyclone, BlowEarth, FrozenEarth, GreaterFrozenEarth }
}
namespace Microsoft.Xna.Framework
{
    public struct Vector3 { public Vector3(float x, float y, float z) { } }
}
namespace Client.Envir
{
    public static class CEnvir
    {
        public static DateTime Now;
        public static Dictionary<Library.LibraryFile, MirLibrary> LibraryList = new();
    }
    public static class Config { public static bool EnableParticle; }
}
namespace Client.Models
{
    public class MapObject
    {
        public static MapObject User = new();
        public static int OffSetX, OffSetY, CellWidth = 48, CellHeight = 32;
        public Point CurrentLocation, MovingOffSet;
        public int DrawX, DrawY;
        public List<MirEffect> Effects = new();
    }
    public class MirLibrary
    {
        public void Draw(int frame, int x, int y, Color colour, bool offset, float opacity, Library.ImageType type) { }
        public void DrawBlend(int frame, int x, int y, Color colour, bool offset, float rate, Library.ImageType type, Library.BlendType blendType) { }
    }
}
namespace Client.Scenes
{
    public class GameScene
    {
        public static GameScene Game = new();
        public MapControl MapControl = new();
    }
    public class MapControl
    {
        public bool TextureValid;
        public DateTime ParticleRenderTime;
        public List<MirEffect> Effects = new();
        public Particle m_xSmoke = new(), m_xBoom = new();
    }
    public class Particle
    {
        public int GetRandomNum(int min, int max) => min;
        public void SetSmokeParticleEx6(Microsoft.Xna.Framework.Vector3 point) { }
        public void SetSmokeParticleEx10(Microsoft.Xna.Framework.Vector3 point) { }
        public void SetSmokeParticleEx4(Microsoft.Xna.Framework.Vector3 point) { }
        public void SetBoomParticle2(Microsoft.Xna.Framework.Vector3 point) { }
        public void SetBoomParticle5(Microsoft.Xna.Framework.Vector3 point) { }
        public void SetBoomParticle(Microsoft.Xna.Framework.Vector3 point) { }
    }
}
