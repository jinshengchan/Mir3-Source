# Android 内置资源 APK

Android 可以将启动资源、基础包和 gzip 补丁一起打进 APK。安装包提供初始资源，运行时仍可从更新服务器获取后续版本；有完整内置资源时，更新服务器暂时不可用不会阻止资源初始化。游戏登录仍需游戏服务器。

## 资源目录

资源可放在 `Mir3.Droid/Assets`，也可放在仓库之外，通过 `BundledResourceDirectory` 指定：

```text
资源目录/
  Data.zip
  LocalUpdate/
    DataAdd.zip
    APKVersion.bin
    PList.Bin
    Data-*.Zl.gz
    ...其余清单中的 gzip 文件
```

`Data.zip` 根目录为 `Data/StartMobileScene.Zl`、`Data/Interface.Zl`、`Mir3.ini`。`DataAdd.zip` 根目录为 `Map/`、`Sound/`、`Data/Map Data/`，不能再套一层客户端目录。目录名和文件名保留大小写。配置中必须使用自己的游戏服务器设置。

补丁清单使用已有 `PatchManager` 的格式：依次写入 .NET BinaryWriter 的字符串、Int64 压缩长度、Int32 摘要长度和 MD5 摘要。摘要对应解压后的原文件。资源相对路径中的反斜杠改为连字符，再追加 `.gz`，得到 APK 内文件名。

`APKVersion.bin` 格式保持原项目兼容：APKVersion、APKFileName、APKCompressedLength、APKCheckSum、BaseZipFileName、BaseZipCompressedLength、BaseZipCheckSum。内置安装器使用基础包名称、长度与摘要；更新服务器仍自行负责 APK 发布信息。APK 中的旧 APK 发布信息不能作为新 APK 的发布清单直接上传。

## 安装行为

1. Android 初始化将 Data.zip 流式复制到临时文件再解压，成功后才保存版本。
2. 进入更新流程时，先检查 LocalUpdate。没有内置清单的旧 APK 继续走原网络流程。
3. 首次安装或资源快照改变时，校验基础 ZIP 的长度和 MD5，逐文件解压；gzip 补丁先解压至临时文件，验证 MD5 后替换目标。
4. 全部完成后写入 Version.bin、APKVersion.bin 和资源快照标记。失败不会标记新快照成功，保留临时失败文件对应的旧目标，清理临时文件。
5. 同一快照重启时跳过初始化，避免覆盖在线更新后的文件。缺少 Map 目录或清单中的文件会重新安装；“修复”会重新校验和恢复内置资源，再执行网络更新。

目录越界项会被拒绝。ZIP 与 gzip 在 APK 内不再压缩。大 ZIP 不依赖 Android Assets 流支持 Seek，也不会把完整基础包读入 byte[]。逐文件替换并非整个资源目录的事务回滚；中途失败可在下次安装重试。

样本 APK 约 2.11 GB，基础包展开约 2.85 GB，还需加补丁展开、基础 ZIP 临时副本和系统安装开销，手机应预留充足空间。构建前确认资源目录内没有日志、配置备份和私密材料。

## 构建

要求仓库 global.json 指定的 .NET SDK、Android workload、Android SDK API 34/Build Tools 34、JDK 17，以及有效的 APK 签名配置。

```bash
dotnet workload install android
bash tools/build-bundled-apk.sh /absolute/resource-directory \
  -p:AndroidSdkDirectory=/absolute/android-sdk \
  -p:JavaSdkDirectory=/absolute/jdk17
```

此脚本使用项目默认 Release 设置。为了缩短本地验证构建，可以额外指定：

```text
-p:RuntimeIdentifier=android-arm64
-p:RunAOTCompilation=False
-p:AotAssemblies=False
-p:AndroidEnableProfiledAot=False
-p:PublishTrimmed=False
```

上述选项仅生成 arm64 并关闭 AOT/裁剪，正式发布应根据设备范围和性能需求重新选择。使用原签名才能覆盖安装已有客户端；本地测试签名不能替代原发布签名。不要把签名密码提交到仓库，也不要把本地构建的 APK 清单当作已经发布的版本。

版本名称和版本号必须与更新服务器的 APKVersion 匹配，可通过 `-p:ApplicationDisplayVersion=...` 和 `-p:ApplicationVersion=...` 指定。样本文件名为“1403安卓客户端.apk”，但实际 AndroidManifest 为版本名称 1.3.8、版本号 26；它内置的 APKVersion.bin 又记录 1.3.0.18，说明内置 APK 发布字段可能是旧值。不要从文件名或内置清单推断当前发布版本。本地安装器只使用其中的基础包信息。

在只允许写工作目录的云环境中，构建前将 `DOTNET_CLI_HOME`、`NUGET_PACKAGES`、`XDG_DATA_HOME`、`XDG_CACHE_HOME`、`XDG_CONFIG_HOME` 指向可写目录；Android 工具和测试签名会写入用户数据目录。

## 验证

```bash
dotnet run --project tests/BundledResources.Tests/BundledResources.Tests.csproj
dotnet run --project tests/BundledResources.Tests/BundledResources.Tests.csproj -- \
  --assets /absolute/resource-directory /empty/smoke-install-directory
```

第一条覆盖非 Seek 流、首次安装、重启保留在线更新、修复、损坏基础包和补丁、失败后重试、路径越界与临时文件清理。第二条使用真实资源执行启动包和全资源安装并验证摘要，目标目录应为独立空目录，可能占数 GB。

设备验收仍需检查首次安装、断开更新服务器后启动、升级、手动修复、空间不足及游戏登录。主机上的文件安装验证不能替代 Android 真机验收。

## 本次验证结果

- Release/arm64 完整 APK 构建成功，关闭 AOT 和裁剪；构建有 25 个 Android API 等警告，无错误。
- 测试 APK 大小 2,078,853,522 字节，包含全部 156 个内置资源文件，资源名称和长度与样本匹配，未打入 partial/tmp 文件。
- APK ZIP CRC 完整性检查通过，apksigner 验证 v1/v2/v3 签名通过；签名为 Android Debug 测试签名。
- 19 项安装器检查通过；对真实启动包、基础 ZIP 和 152 个 gzip 补丁的实际解压、MD5 校验和版本写入通过。
- APK SHA-256：`47e681e4cf03105ed71a771abc5cd2293246a7c1eccd5ffab87c61a9bc775c87`。
- 未在 Android 真机安装和运行，未验证游戏登录，未发布更新服务器。

## 从 GitHub 下载

`codex/bundled-apk-delivery` 分支提供 GitHub Actions 构建流程。该分支推送后自动构建，资源来自已授权共享的样本 Google Drive 文件。进入仓库的 Actions，打开 `Build bundled Android APK`，等待运行成功，在 Artifacts 中下载 `Mir3-bundled-arm64-test-apk`，解压得到 APK。附件仅保留一天，过期后可以重新运行任务。

此流程不会创建公开 Release 或修改 main，生成的仍为测试签名 APK。需要仓库启用 Actions 并有可用的构建与附件存储配额；运行成功和附件下载以 GitHub 页面实际结果为准。

## 启动进度修复

内置资源安装现在报告基础 ZIP 复制、解压以及 gzip 补丁读取进度。启动界面在游戏主线程每帧读取状态，不再依赖下载进度回调刷新文字。更新清单请求限制为 15 秒，未捕获的启动异常会记录日志并显示原因。完整内置资源安装完成后，更新服务不可达时仍按原流程进入登录界面；游戏服务器登录是否成功需单独验证。

CI 测试包显式设置 `-p:BundledResourceTestBuild=true`，跳过 APK 自身的强制更新，保留资源更新。此选项默认关闭，正式发布应配置正确版本和签名。CI 在构建工作区写入样本清单的版本 `1.3.8`（版本号 26），并在打包后检查实际清单；仓库原始 AndroidManifest 保持不变。原清单显式指定版本会覆盖 ApplicationVersion 参数，不能只依赖该参数改变包版本。各次 CI 的临时测试签名可能不同，不能保证覆盖安装；覆盖失败时先备份需要保留的数据，再更换测试包。

## 登录和注册反馈修复

上个测试包使用 `1.2.5-test3.30` 作为版本标识，但该项目在游戏握手时也发送这个标识；服务端开启手机版本检查时会拒绝连接。本次恢复样本 APK 的 `1.3.8.26`，不修改服务端版本或数据库校验，登录界面附加“连接修复测试”字样区分测试包。

Android 登录页显示当前游戏连接状态、地址、重试和连接失败原因。登录、注册、改密码和找回密码在未通过握手或服务器信息未加载时明确提示，不再静默丢掉请求。注册同时检查确认密码，已入队请求显示等待回复提示。版本和数据库拒绝提示通过 Android 主线程显示；账号控件读写、登录页初始化、可见性和关闭弹窗也统一到 Android UI 线程。修正旧 TCP 连接回调误清空新连接的问题。

验证覆盖连接未就绪时禁止发送且显示提示、正常连接时仅发送一次，以及原有资源安装与进度检查（合计 34 项）。实际登录和注册仍需真机及服务器验收。用户确认原始“1403安卓客户端”可连接同一服务器。
