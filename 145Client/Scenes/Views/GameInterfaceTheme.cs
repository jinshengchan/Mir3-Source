using Client.Envir;
using Library;
using System;
using System.Drawing;

namespace Client.Scenes.Views
{
    /// <summary>
    /// The immutable interface decision used by one GameScene instance.
    /// </summary>
    public sealed class GameInterfaceTheme
    {
        public const string DefaultValue = "145";
        public const string KoreanValue = "Korean";

        public string Value { get; }
        public bool IsKorean => Value == KoreanValue;

        public GameInterfaceTheme(string value)
        {
            Value = Normalize(value);
        }

        public static string Normalize(string value)
        {
            return string.Equals(value, KoreanValue, StringComparison.OrdinalIgnoreCase) ? KoreanValue : DefaultValue;
        }

        public static bool IsKoreanValue(string value)
        {
            return Normalize(value) == KoreanValue;
        }

        public static bool HasRequiredKoreanAssets()
        {
            return HasImage(LibraryFile.GameInter, 50, new Size(1024, 68))
                && HasImage(LibraryFile.GameInter, 51, new Size(992, 10))
                && HasImage(LibraryFile.GameInter, 52, new Size(220, 8))
                && HasImage(LibraryFile.GameInter, 54, new Size(220, 8))
                && HasImage(LibraryFile.GameInter, 56, new Size(980, 4))
                && HasImage(LibraryFile.GameInter, 60, new Size(20, 12))
                && HasImage(LibraryFile.GameInter, 61, new Size(32, 12))
                && HasImage(LibraryFile.GameInter, 62, new Size(24, 12))
                && HasImage(LibraryFile.GameInter, 63, new Size(36, 12))
                && HasImage(LibraryFile.GameInter, 64, new Size(20, 12))
                && HasImage(LibraryFile.GameInter, 65, new Size(20, 12))
                && HasImage(LibraryFile.GameInter, 66, new Size(20, 12))
                && HasImage(LibraryFile.GameInter, 460, new Size(100, 26))
                && HasImage(LibraryFile.GameInter, 465, new Size(100, 26))
                && HasImage(LibraryFile.GameInter, 470, new Size(100, 26))
                && HasImage(LibraryFile.GameInter, 475, new Size(100, 26))
                && HasImage(LibraryFile.GameInter, 480, new Size(100, 26))
                && HasImage(LibraryFile.GameInter, 485, new Size(100, 26))
                && HasImage(LibraryFile.GameInter, 82, new Size(36, 34))
                && HasImage(LibraryFile.GameInter, 87, new Size(36, 34))
                && HasImage(LibraryFile.GameInter, 92, new Size(36, 34))
                && HasImage(LibraryFile.GameInter, 97, new Size(36, 34))
                && HasImage(LibraryFile.GameInter, 102, new Size(36, 34))
                && HasImage(LibraryFile.GameInter, 107, new Size(36, 34))
                && HasImage(LibraryFile.GameInter, 112, new Size(36, 34))
                && HasImage(LibraryFile.GameInter, 117, new Size(36, 34))
                && HasImage(LibraryFile.GameInter, 122, new Size(48, 48))
                && HasImage(LibraryFile.GameInter, 240, new Size(16, 14))
                && HasImage(LibraryFile.GameInter, 241, new Size(16, 14))
                && HasImage(LibraryFile.GameInter, 3500, new Size(380, 48))
                && HasImage(LibraryFile.GameInter, 3502, new Size(380, 60))
                && HasImage(LibraryFile.GameInter, 3503, new Size(380, 38))
                && HasImage(LibraryFile.GameInter, 3505, new Size(48, 22))
                && HasImage(LibraryFile.GameInter, 3506, new Size(48, 22))
                && HasImage(LibraryFile.GameInter, 3510, new Size(48, 22))
                && HasImage(LibraryFile.GameInter, 3511, new Size(48, 22))
                && HasImage(LibraryFile.GameInter, 3515, new Size(48, 22))
                && HasImage(LibraryFile.GameInter, 3516, new Size(48, 22))
                && HasImage(LibraryFile.GameInter, 3518, new Size(44, 20))
                && HasImage(LibraryFile.GameInter, 3520, new Size(48, 22))
                && HasImage(LibraryFile.GameInter, 3521, new Size(48, 22))
                && HasImage(LibraryFile.GameInter, 3523, new Size(44, 20))
                && HasImage(LibraryFile.GameInter, 3525, new Size(48, 22))
                && HasImage(LibraryFile.GameInter, 3526, new Size(48, 22))
                && HasImage(LibraryFile.GameInter, 3528, new Size(44, 20))
                && HasImage(LibraryFile.GameInter, 3530, new Size(48, 22))
                && HasImage(LibraryFile.GameInter, 3531, new Size(48, 22))
                && HasImage(LibraryFile.GameInter, 3535, new Size(48, 22))
                && HasImage(LibraryFile.GameInter, 3536, new Size(48, 22))
                && HasImage(LibraryFile.GameInter, 3542, new Size(20, 18))
                && HasImage(LibraryFile.GameInter, 3545, new Size(16, 18))
                && HasImage(LibraryFile.GameInter, 3552, new Size(20, 18))
                && HasImage(LibraryFile.GameInter, 3560, new Size(16, 14))
                && HasImage(LibraryFile.GameInter, 3561, new Size(20, 10))
                && HasImage(LibraryFile.GameInter, 3562, new Size(20, 10))
                && HasImage(LibraryFile.GameInter, 3568, new Size(44, 20))
                && HasImage(LibraryFile.GameInter, 3573, new Size(44, 20))
                && HasImage(LibraryFile.GameInter, 3578, new Size(44, 20))
                && HasImage(LibraryFile.UI1, 1210, new Size(280, 48))
                && HasImage(LibraryFile.UI1, 1220, new Size(284, 468))
                && HasImage(LibraryFile.UI1, 1280, new Size(328, 492))
                && HasImage(LibraryFile.UI1, 1486, new Size(32, 36))
                && HasImage(LibraryFile.UI1, 1487, new Size(32, 36))
                && HasImage(LibraryFile.UI1, 1488, new Size(32, 36))
                && HasImage(LibraryFile.UI1, 1489, new Size(32, 36))
                && HasImage(LibraryFile.Interface, 200, new Size(1500, 12))
                && HasImage(LibraryFile.Interface, 203, new Size(1024, 28));
        }

        private static bool HasImage(LibraryFile file, int index, Size expected)
        {
            try
            {
                if (!CEnvir.LibraryList.TryGetValue(file, out MirLibrary library)) return false;
                return library.GetSize(index) == expected;
            }
            catch
            {
                return false;
            }
        }
    }
}
