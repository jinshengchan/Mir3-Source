using Android.App;
using Android.Content;
using Android.OS;
using Android.Util;
using AndroidX.Core.Content;
using Client.Envir;
using Library;
using Microsoft.Xna.Framework;
using Mir3.Mobile;
using System;
using System.IO;
using System.IO.Compression;
using Config = Client.Envir.Config;

namespace Mir3.Droid
{
    public class DrodNative : INative
    {
        public string SafeCode => MainActivity.Main.GetVersionName();

        public IUI UI => MainActivity.Main;

        public byte[] GetFileBytes(string path)
        {
            byte[] data;
            using (System.IO.Stream stream = Game.Activity.Assets!.Open(path))
            {
                MemoryStream memoryStream = new MemoryStream();
                stream.CopyTo(memoryStream);
                memoryStream.Seek(0L, SeekOrigin.Begin);
                stream.Close();
                data = memoryStream.ToArray();
            }
            return data;
        }

        public Stream GetFileStream(string path)
        {
            try { return Game.Activity.Assets!.Open(path); }
            catch (Java.IO.FileNotFoundException ex)
            {
                // Keep optional bundled assets compatible with online-only APKs.
                throw new FileNotFoundException("Android asset not found: " + path, ex);
            }
        }

        public void HideInputField()
        {
            MainActivity.HideInputField();
        }

        public void InitData()
        {
#if BUNDLED_RESOURCE_TEST
            // Preserve the phone's private update credential across bootstrap extraction.
            bool hasLocalConfig = File.Exists(Path.Combine(CEnvir.MobileClientPath, "Mir3.ini"));
            string updatePassword = Config.Password;
#endif
            var code = MainActivity.Main.GetVersionCode();
            var name = MainActivity.Main.GetVersionName();
#if DEBUG
#else
            if (Config.VersionCode != code || Config.VersionName != name ||
                !File.Exists(Path.Combine(CEnvir.MobileClientPath, "Data", "StartMobileScene.Zl")))
#endif
            {
                Patch.BundledResources.InstallZip(() => GetFileStream("Data.zip"), CEnvir.MobileClientPath);
                // Advance the APK version only after the bootstrap archive was installed.
                ConfigReader.Load();
                Config.VersionCode = code;
                Config.VersionName = name;
                ConfigReader.Save();

            }
#if BUNDLED_RESOURCE_TEST
            Config.UseNetworkConfig = true;
            Config.IPAddress = "118.25.67.175";
            Config.Port = 7000;
            Config.MicroClientIP = "118.25.67.175";
            Config.MicroClientPort = 8000;
            Config.Host = "http://118.25.67.175:7080/";
            Config.UseLogin = true;
            Config.UserName = "mobile";
            if (hasLocalConfig) Config.Password = updatePassword;
            ConfigReader.Save();
            Mir3.Mobile.ConnectionDiagnostics.Record("test-server game=118.25.67.175:7000 micro=118.25.67.175:8000 update=http://118.25.67.175:7080/");
#endif
#if DEBUG
            Config.DebugLabel = true;
#endif
        }
        public bool IsPad => Game1.Game.Graphics.PreferredBackBufferWidth / Game1.Game.Graphics.PreferredBackBufferHeight < 1.5F;

        public void Initialize()
        {
            //手机目录
            CEnvir.MobileClientPath = Application.Context.GetExternalFilesDir(null)!.AbsolutePath + "/";
#if BUNDLED_RESOURCE_TEST
            try { Mir3.Mobile.ConnectionDiagnostics.Initialize(CEnvir.MobileClientPath); }
            catch (Exception ex) { UI.ShowMsg("诊断日志无法创建：" + ex.GetType().Name); }
#endif

            //旧版 Data.zip 可能将配置文件解压为仅可写权限，导致启动读取配置时黑屏
            string configPath = Path.Combine(CEnvir.MobileClientPath, "Mir3.ini");
            if (File.Exists(configPath))
            {
                try
                {
                    using var stream = File.OpenRead(configPath);
                }
                catch (UnauthorizedAccessException)
                {
                    File.Delete(configPath);
                }
            }

            //根据手机分辨率和dpi设置客户端缩放比率
            DisplayMetrics displayMetrics = new DisplayMetrics();
            MainActivity.Main.WindowManager!.DefaultDisplay!.GetMetrics(displayMetrics);
            CEnvir.Target = new System.Drawing.Size(Game1.Game.Graphics.PreferredBackBufferWidth, Game1.Game.Graphics.PreferredBackBufferHeight);
            CEnvir.Density = displayMetrics.Density;
            CEnvir.DeviceHeight = Game1.Game.Graphics.PreferredBackBufferHeight / displayMetrics.Ydpi;
            //屏幕比例 <1.5 就 4:3 比例
            if (Game1.Game.Graphics.PreferredBackBufferWidth / Game1.Game.Graphics.PreferredBackBufferHeight < 1.5F)
            {
                CEnvir.DevicePercent = 4;
                Config.GameSize = new System.Drawing.Size(1024, 768);
            }
            //屏幕比例 >=1.5 就 16:9 比例
            else
            {
                CEnvir.DevicePercent = 16;
                Config.GameSize = new System.Drawing.Size(960, 540);
            }
        }

        public void OpenUrl(string url)
        {
            //System.Diagnostics.Process.Start(url);
            MainActivity.Main.StartWebView(url);
        }

        public void ShowInputField(string text)
        {
            MainActivity.ShowInputField(text);
        }

        public bool UpdateAPKVersion(string filename)
        {
            try
            {
                string apkfile = Path.Combine(Path.Combine(CEnvir.MobileClientPath, "Patchs"), filename);
                Activity activity = Game.Activity;
                Java.IO.File file = new Java.IO.File(apkfile);
                bool exist = file.Exists();
                if (!exist || file.Length() <= 0)
                {
                    CEnvir.SaveError("APK文件不存在或者大小为0");
                    return false;
                }
                if (Build.VERSION.SdkInt >= BuildVersionCodes.N)
                {
                    Android.Net.Uri uriForFile = FileProvider.GetUriForFile(activity, activity.ApplicationInfo.PackageName + ".fileProvider", file);
                    Intent intent = new Intent(Intent.ActionInstallPackage);
                    intent.SetData(uriForFile);
                    intent.SetFlags(ActivityFlags.GrantReadUriPermission);
                    activity.StartActivity(intent);
                }
                else
                {
                    Android.Net.Uri data = Android.Net.Uri.FromFile(file);
                    Intent intent2 = new Intent(Intent.ActionView);
                    intent2.SetDataAndType(data, "application/vnd.android.package-archive");
                    intent2.SetFlags(ActivityFlags.NewTask);
                    activity.StartActivity(intent2);
                }
                return true;
            }
            catch (Exception ex)
            {
                CEnvir.SaveError(ex.Message);
                return false;
            }

        }
    }
}
