using System;
using System.Collections.Generic;
using UnityEngine;

namespace Mir3.UnityPrototype
{
    // A small, bounded preview. This is not the production map renderer.
    public sealed class Mir3KoreanMapPreview : MonoBehaviour
    {
        [Serializable]
        public sealed class FloorSprite
        {
            public int fileId;
            public int imageIndex;
            public Sprite sprite;
        }

        [SerializeField] private TextAsset mapBytes;
        [SerializeField] private FloorSprite[] floorSprites = new FloorSprite[0];
        [SerializeField] private int startX;
        [SerializeField] private int startY;
        [SerializeField, Range(2, 40)] private int width = 24;
        [SerializeField, Range(2, 40)] private int height = 18;
        [SerializeField] private bool showBlockedCells;

        private const float PixelsPerUnit = 32f;
        private readonly List<GameObject> created = new List<GameObject>();
        private Texture2D fallbackTexture;
        private Sprite fallbackSprite;

        private void Start()
        {
            if (mapBytes == null)
            {
                Debug.LogError("Assign a .map file copied as .bytes to Map Bytes.", this);
                return;
            }

            try { DrawMap(new Mir3KoreanMap(mapBytes.bytes)); }
            catch (Exception ex) { Debug.LogException(ex, this); }
        }

        private void DrawMap(Mir3KoreanMap map)
        {
            int minX = Mathf.Clamp(startX, 0, map.Width - 1);
            int minY = Mathf.Clamp(startY, 0, map.Height - 1);
            int maxX = Mathf.Min(map.Width, minX + width);
            int maxY = Mathf.Min(map.Height, minY + height);
            var sprites = new Dictionary<long, Sprite>();
            foreach (FloorSprite entry in floorSprites)
            {
                if (entry != null && entry.sprite != null)
                    sprites[Key(entry.fileId, entry.imageIndex)] = entry.sprite;
            }

            // The original client draws only even X/Y floor cells, at 48x32 pixels per cell.
            // Clamp the viewport first to avoid creating thousands of GameObjects.
            for (int x = minX + (minX & 1); x < maxX; x += 2)
            for (int y = minY + (minY & 1); y < maxY; y += 2)
            {
                Mir3KoreanMap.Cell cell = map.GetCell(x, y);
                Sprite image;
                bool found = sprites.TryGetValue(Key(cell.BackFile, cell.BackIndex), out image);
                var tile = new GameObject("Floor " + x + "," + y);
                tile.transform.SetParent(transform, false);
                tile.transform.localPosition = new Vector3(
                    (x - minX) * 48f / PixelsPerUnit,
                    -(y - minY) * 32f / PixelsPerUnit, 0f);
                var renderer = tile.AddComponent<SpriteRenderer>();
                renderer.sprite = found ? image : Fallback();
                renderer.color = found ? Color.white : (cell.Blocked
                    ? new Color(0.45f, 0.25f, 0.25f) : new Color(0.25f, 0.32f, 0.38f));
                created.Add(tile);
            }

            if (!showBlockedCells) return;
            for (int x = minX; x < maxX; x++)
            for (int y = minY; y < maxY; y++)
            {
                if (!map.GetCell(x, y).Blocked) continue;
                var marker = new GameObject("Blocked " + x + "," + y);
                marker.transform.SetParent(transform, false);
                marker.transform.localPosition = new Vector3(
                    (x - minX) * 48f / PixelsPerUnit,
                    -(y - minY) * 32f / PixelsPerUnit, -0.1f);
                marker.transform.localScale = new Vector3(0.5f, 0.5f, 1f);
                var renderer = marker.AddComponent<SpriteRenderer>();
                renderer.sprite = Fallback();
                renderer.color = new Color(1f, 0.1f, 0.1f, 0.35f);
                renderer.sortingOrder = 1;
                created.Add(marker);
            }
        }

        private static long Key(int file, int index)
        {
            return ((long)file << 32) | (uint)index;
        }

        private Sprite Fallback()
        {
            if (fallbackSprite != null) return fallbackSprite;
            fallbackTexture = new Texture2D(3, 2, TextureFormat.RGBA32, false);
            fallbackTexture.filterMode = FilterMode.Point;
            fallbackTexture.SetPixels(new[] {
                Color.white, Color.white, Color.white,
                Color.white, Color.white, Color.white });
            fallbackTexture.Apply();
            fallbackSprite = Sprite.Create(fallbackTexture, new Rect(0, 0, 3, 2),
                new Vector2(0, 1), 1f); // placeholder spans 3x2 world units
            return fallbackSprite;
        }

        private void OnDestroy()
        {
            foreach (GameObject item in created)
                if (item != null) Destroy(item);
            if (fallbackSprite != null) Destroy(fallbackSprite);
            if (fallbackTexture != null) Destroy(fallbackTexture);
        }
    }
}
