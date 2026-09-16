using Library;
using Library.SystemModels;
using Server.Models;
using System;
using System.Collections.Generic;
using System.Drawing;

namespace Server.Envir
{
    /// <summary>
    /// 假人 A* 寻路系统。
    /// 使用二叉堆优化 A*，支持8方向移动，对角穿墙角检查，路径缓存3秒。
    /// 导航网格按地图索引缓存，只检查静态地形，不检查动态对象。
    /// </summary>
    public static class BotPathFinder
    {
        // ══════════════════════════════════════════════════════════════════════
        //  常量
        // ══════════════════════════════════════════════════════════════════════

        /// <summary>启用 A* 的最小距离（格）。距离小于此值直接移动。</summary>
        public const int MinPathfindDistance = 4;

        /// <summary>A* 最大搜索节点数，防止过度消耗 CPU。</summary>
        private const int MaxSearchNodes = 40000;

        /// <summary>路径缓存过期时间（秒）。</summary>
        private const double PathCacheExpireSeconds = 3.0;

        /// <summary>路径目标偏移超过此格数时缓存失效。</summary>
        private const int PathCacheInvalidateDist = 2;

        /// <summary>漫游搜索怪物的半径（格）。</summary>
        public const int RoamSearchRadius = 18;

        /// <summary>漫游搜索最多检查的目标数。</summary>
        private const int RoamMaxTargets = 8;

        // 8方向移动：直线10，对角14
        private static readonly Point[] Directions = {
            new Point(0, -1),  new Point(1, 0),   new Point(0, 1),   new Point(-1, 0),
            new Point(1, -1),  new Point(1, 1),   new Point(-1, 1),  new Point(-1, -1),
        };
        private static readonly int[] MoveCost = { 10, 10, 10, 10, 14, 14, 14, 14 };

        // ══════════════════════════════════════════════════════════════════════
        //  缓存
        // ══════════════════════════════════════════════════════════════════════

        /// <summary>导航网格缓存：地图索引 → bool[width, height]（true=可通行）。</summary>
        private static readonly Dictionary<int, bool[,]> _navGridCache
            = new Dictionary<int, bool[,]>();

        /// <summary>路径缓存：假人 ObjectID → 路径信息。</summary>
        private static readonly Dictionary<uint, PathCache> _pathCache
            = new Dictionary<uint, PathCache>();

        private sealed class PathCache
        {
            public Queue<Point> Path;
            public Point Goal;
            public DateTime ExpireTime;
        }

        // ══════════════════════════════════════════════════════════════════════
        //  公共 API
        // ══════════════════════════════════════════════════════════════════════

        /// <summary>
        /// 尝试为假人更新追击路径（近战/远程追击调用）。
        /// 若已有未过期且目标未偏移的缓存，直接复用；否则重新计算。
        /// </summary>
        public static bool TryUpdateChasePath(PlayerObject player, MapObject target)
        {
            if (player == null || target == null || player.CurrentMap == null) return false;

            Point from = player.CurrentLocation;
            Point to = target.CurrentLocation;

            PathCache cache;
            if (_pathCache.TryGetValue(player.ObjectID, out cache)
                && cache != null
                && SEnvir.Now < cache.ExpireTime
                && cache.Path != null
                && cache.Path.Count > 0
                && Functions.Distance(cache.Goal, to) <= PathCacheInvalidateDist)
            {
                return true; // 复用缓存
            }

            return ComputeAndCache(player.ObjectID, player.CurrentMap, from, to);
        }

        /// <summary>
        /// 尝试为假人更新漫游路径（目标为固定坐标格子，不依赖 MapObject）。
        /// 用于漫游时导航到 A* 搜索到的最近怪物格。
        /// </summary>
        public static bool TryUpdateRoamPath(PlayerObject player, Point targetPoint)
        {
            if (player == null || player.CurrentMap == null) return false;

            Point from = player.CurrentLocation;
            Point to = targetPoint;

            PathCache cache;
            if (_pathCache.TryGetValue(player.ObjectID, out cache)
                && cache != null
                && SEnvir.Now < cache.ExpireTime
                && cache.Path != null
                && cache.Path.Count > 0
                && Functions.Distance(cache.Goal, to) <= PathCacheInvalidateDist)
            {
                return true; // 复用缓存
            }

            return ComputeAndCache(player.ObjectID, player.CurrentMap, from, to);
        }

        /// <summary>
        /// 消费路径队列，执行一步移动。若路径消耗完或动态阻挡，尝试侧移兜底。
        /// 返回 true 表示执行了移动（或侧移），false 表示无路径。
        /// </summary>
        public static bool TryMoveBotAlongPath(PlayerObject player)
        {
            if (player == null) return false;

            PathCache cache;
            if (!_pathCache.TryGetValue(player.ObjectID, out cache)
                || cache == null
                || cache.Path == null
                || cache.Path.Count == 0
                || SEnvir.Now >= cache.ExpireTime)
            {
                ClearPath(player.ObjectID);
                return false;
            }

            Point next = cache.Path.Dequeue();
            Point delta = new Point(next.X - player.CurrentLocation.X, next.Y - player.CurrentLocation.Y);
            MirDirection dir = Functions.DirectionFromPoint(Point.Empty, delta);
            int distance = 1;

            // 检查下一格是否被动态对象占用，若占用则侧移
            if (!CanMoveToCell(player.CurrentMap, next))
            {
                // 尝试侧移到左右各45度
                MirDirection left = (MirDirection)(((int)dir + 7) % 8);
                MirDirection right = (MirDirection)(((int)dir + 1) % 8);

                Point leftCell = Functions.Move(player.CurrentLocation, left, 1);
                Point rightCell = Functions.Move(player.CurrentLocation, right, 1);

                if (CanMoveToCell(player.CurrentMap, leftCell))
                    dir = left;
                else if (CanMoveToCell(player.CurrentMap, rightCell))
                    dir = right;
                else
                    return false; // 周围都堵了
            }
            else if (cache.Path.Count > 0)
            {
                Point second = cache.Path.Peek();
                Point secondDelta = new Point(second.X - next.X, second.Y - next.Y);
                MirDirection secondDir = Functions.DirectionFromPoint(Point.Empty, secondDelta);

                if (secondDir == dir && CanMoveToCell(player.CurrentMap, second))
                {
                    cache.Path.Dequeue();
                    distance = 2;
                }
            }

            player.Move(dir, distance);
            return true;
        }

        /// <summary>
        /// 获取缓存路径的下一步方向（不消费队列，仅预览）。
        /// </summary>
        public static bool TryPeekNextDirection(uint objectId, out MirDirection dir)
        {
            dir = MirDirection.Up;
            PathCache cache;
            if (!_pathCache.TryGetValue(objectId, out cache)
                || cache == null
                || cache.Path == null
                || cache.Path.Count == 0
                || SEnvir.Now >= cache.ExpireTime)
                return false;

            Point[] arr = cache.Path.ToArray();
            // 需要起点来算方向，此处仅返回第一个路径格本身
            // 调用方用 player.CurrentLocation 计算 delta
            dir = MirDirection.Up; // placeholder，调用方按需计算
            return true;
        }

        /// <summary>
        /// 检查某假人是否有可用的未过期路径。
        /// </summary>
        public static bool HasValidPath(uint objectId)
        {
            PathCache cache;
            if (!_pathCache.TryGetValue(objectId, out cache)) return false;
            return cache != null && cache.Path != null && cache.Path.Count > 0 && SEnvir.Now < cache.ExpireTime;
        }

        /// <summary>
        /// 漫游时，用 A* 搜索附近可攻击怪物的格子，返回目标格坐标。
        /// 找不到返回 Point.Empty。
        /// </summary>
        public static Point FindNearestMonsterCellByAStar(PlayerObject player)
        {
            if (player == null || player.CurrentMap == null) return Point.Empty;

            var map = player.CurrentMap;
            Point origin = player.CurrentLocation;
            int checked_ = 0;

            // 按距离排序后检查最近 RoamMaxTargets 个怪
            var monsters = new List<(MonsterObject mob, int dist)>();
            foreach (MapObject obj in map.Objects)
            {
                MonsterObject mob = obj as MonsterObject;
                if (mob == null || mob.Dead || mob.Node == null) continue;

                int d = Functions.Distance(origin, mob.CurrentLocation);
                if (d > RoamSearchRadius) continue;

                monsters.Add((mob, d));
            }

            monsters.Sort((a, b) => a.dist.CompareTo(b.dist));

            foreach (var (mob, _) in monsters)
            {
                if (checked_++ >= RoamMaxTargets) break;

                // 尝试找到离怪物最近的可到达格
                Point target = mob.CurrentLocation;
                bool[,] grid = GetOrBuildNavGrid(map);
                if (grid == null) return target;

                // 直接返回怪物格子，让 A* 负责找路
                return target;
            }

            return Point.Empty;
        }

        /// <summary>
        /// 清除某假人的路径缓存。
        /// 切图/卡死/死亡/换目标时调用。
        /// </summary>
        public static void ClearPath(uint objectId)
        {
            _pathCache.Remove(objectId);
        }

        /// <summary>
        /// 使地图的导航网格缓存失效（MapObjects 发生变化时调用）。
        /// </summary>
        public static void InvalidateNavGrid(int mapIndex)
        {
            _navGridCache.Remove(mapIndex);
        }

        // ══════════════════════════════════════════════════════════════════════
        //  A* 核心
        // ══════════════════════════════════════════════════════════════════════

        private static bool ComputeAndCache(uint objectId, Map map, Point from, Point to)
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

        private static Queue<Point> FindPath(Map map, Point from, Point to)
        {
            if (map == null) return null;

            bool[,] grid = GetOrBuildNavGrid(map);
            if (grid == null) return null;

            int width = map.Width;
            int height = map.Height;

            if (!InBounds(to, width, height) || !grid[to.X, to.Y])
                return null;

            // A* with binary heap
            var heap = new BinaryHeap<ANode>(256);
            var closed = new HashSet<int>();
            var gScore = new Dictionary<int, int>();
            var parent = new Dictionary<int, int>();

            int startKey = from.X * height + from.Y;
            int goalKey = to.X * height + to.Y;

            gScore[startKey] = 0;
            heap.Push(new ANode(startKey, Heuristic(from, to)));

            int searched = 0;
            while (heap.Count > 0 && searched < MaxSearchNodes)
            {
                ANode cur = heap.Pop();
                if (closed.Contains(cur.Key)) continue;
                closed.Add(cur.Key);
                searched++;

                if (cur.Key == goalKey)
                    return ReconstructPath(parent, startKey, goalKey, height);

                Point curPt = new Point(cur.Key / height, cur.Key % height);

                for (int i = 0; i < 8; i++)
                {
                    int nx = curPt.X + Directions[i].X;
                    int ny = curPt.Y + Directions[i].Y;

                    if (!InBounds(nx, ny, width, height)) continue;
                    if (!grid[nx, ny]) continue;

                    // 对角穿墙角检查
                    if (i >= 4)
                    {
                        if (!grid[curPt.X + Directions[i].X, curPt.Y] ||
                            !grid[curPt.X, curPt.Y + Directions[i].Y])
                            continue;
                    }

                    int nKey = nx * height + ny;
                    if (closed.Contains(nKey)) continue;

                    int curG;
                    gScore.TryGetValue(cur.Key, out curG);
                    int tentG = curG + MoveCost[i];

                    int existG;
                    if (gScore.TryGetValue(nKey, out existG) && tentG >= existG)
                        continue;

                    gScore[nKey] = tentG;
                    parent[nKey] = cur.Key;
                    int f = tentG + Heuristic(new Point(nx, ny), to);
                    heap.Push(new ANode(nKey, f));
                }
            }

            return null;
        }

        private static Queue<Point> ReconstructPath(Dictionary<int, int> parent, int startKey, int goalKey, int height)
        {
            var stack = new Stack<int>();
            int cur = goalKey;
            while (cur != startKey)
            {
                stack.Push(cur);
                cur = parent[cur];
            }

            var queue = new Queue<Point>(stack.Count);
            while (stack.Count > 0)
            {
                int k = stack.Pop();
                queue.Enqueue(new Point(k / height, k % height));
            }
            return queue;
        }

        private static int Heuristic(Point a, Point b)
        {
            int dx = Math.Abs(a.X - b.X);
            int dy = Math.Abs(a.Y - b.Y);
            // 对角线距离
            return 10 * (dx + dy) - 6 * Math.Min(dx, dy);
        }

        // ══════════════════════════════════════════════════════════════════════
        //  导航网格
        // ══════════════════════════════════════════════════════════════════════

        private static bool[,] GetOrBuildNavGrid(Map map)
        {
            if (map == null) return null;

            bool[,] grid;
            if (_navGridCache.TryGetValue(map.Info.Index, out grid)) return grid;

            int w = map.Width;
            int h = map.Height;
            if (w <= 0 || h <= 0) return null;

            grid = new bool[w, h];
            for (int x = 0; x < w; x++)
            {
                for (int y = 0; y < h; y++)
                {
                    var cell = map.GetCell(x, y);
                    // null=不可通行（边界/未加载）
                    // SafeZone != null=安全区格子，假人寻路时不经过安全区，
                    // 避免路径穿越安全区边界导致在边界反复横跳卡住
                    if (cell == null || cell.SafeZone != null)
                    {
                        grid[x, y] = false;
                        continue;
                    }
                    grid[x, y] = true;
                }
            }

            _navGridCache[map.Info.Index] = grid;
            return grid;
        }

        // ══════════════════════════════════════════════════════════════════════
        //  辅助方法
        // ══════════════════════════════════════════════════════════════════════

        private static bool InBounds(Point p, int w, int h)
            => p.X >= 0 && p.X < w && p.Y >= 0 && p.Y < h;

        private static bool InBounds(int x, int y, int w, int h)
            => x >= 0 && x < w && y >= 0 && y < h;

        private static bool CanMoveToCell(Map map, Point p)
        {
            if (map == null) return false;
            var cell = map.GetCell(p.X, p.Y);
            if (cell == null) return false;
            // 安全区格子不可进入：防止假人在安全区/非安全区边界来回横跳卡住
            if (cell.SafeZone != null) return false;
            return cell.Objects == null || cell.Objects.Count == 0;
        }

        // ══════════════════════════════════════════════════════════════════════
        //  二叉堆（最小堆，1-indexed，带索引映射表）
        // ══════════════════════════════════════════════════════════════════════

        private struct ANode : IComparable<ANode>
        {
            public int Key;
            public int F;
            public ANode(int key, int f) { Key = key; F = f; }
            public int CompareTo(ANode other) => F.CompareTo(other.F);
        }

        private sealed class BinaryHeap<T> where T : IComparable<T>
        {
            private T[] _data;
            private int _size;

            public int Count => _size;

            public BinaryHeap(int capacity)
            {
                _data = new T[capacity + 1];
                _size = 0;
            }

            public void Push(T item)
            {
                if (_size + 1 >= _data.Length)
                    Array.Resize(ref _data, _data.Length * 2);

                _data[++_size] = item;
                SiftUp(_size);
            }

            public T Pop()
            {
                T top = _data[1];
                _data[1] = _data[_size--];
                if (_size > 0) SiftDown(1);
                return top;
            }

            private void SiftUp(int i)
            {
                while (i > 1)
                {
                    int p = i / 2;
                    if (_data[p].CompareTo(_data[i]) <= 0) break;
                    T tmp = _data[p]; _data[p] = _data[i]; _data[i] = tmp;
                    i = p;
                }
            }

            private void SiftDown(int i)
            {
                while (true)
                {
                    int smallest = i;
                    int l = i * 2, r = i * 2 + 1;
                    if (l <= _size && _data[l].CompareTo(_data[smallest]) < 0) smallest = l;
                    if (r <= _size && _data[r].CompareTo(_data[smallest]) < 0) smallest = r;
                    if (smallest == i) break;
                    T tmp = _data[i]; _data[i] = _data[smallest]; _data[smallest] = tmp;
                    i = smallest;
                }
            }
        }
    }
}
