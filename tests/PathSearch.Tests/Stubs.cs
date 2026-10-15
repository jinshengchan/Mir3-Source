namespace Client.Envir
{
    public static class CEnvir { public static void SaveError(string error) => throw new Exception(error); }
}
namespace Client.Scenes.Views
{
    public sealed class MapCells
    {
        private readonly bool[,] _blocked;
        public MapCells(int width, int height) { _blocked = new bool[width, height]; }
        public void Block(int x, int y) => _blocked[x, y] = true;
        public bool EmptyCell(int x, int y) => x >= 0 && y >= 0 && x < _blocked.GetLength(0) && y < _blocked.GetLength(1) && !_blocked[x, y];
    }
    public sealed class MapControl
    {
        public int Width, Height;
        public MapCells Cells;
        public MapControl(int width, int height) { Width = width; Height = height; Cells = new MapCells(width, height); }
    }
}
