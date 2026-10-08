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

## 校验失败定位

`Bundled ZIP checksum mismatch` 发生在基础 ZIP 已复制、长度符合清单后，表示整包 MD5 不符，不能直接判断是下载截断。原始样本基础包 DataAdd.zip 长度为 1,123,514,838 字节，MD5 为 `ea9cba07c8e11cc5b9892b3bdaf30bb9`。签名验证、外层 ZIP CRC 校验和内置基础包 MD5 校验是不同的检查。手机上修改后的 APK 需要单独比对，不能用未修改的构建结果代替验证。

CI 在构建前校验真实基础包与 152 个补丁，在构建后再次核对 APK 内基础 ZIP 的 MD5 和版本清单，附件包含 BUNDLED-INTEGRITY.json、实际 APK 元数据和 SHA-256。此前构建虽检查了 ZIP CRC，未在 CI 对下载到的真实资源做这项清单比对；本次补上该检查。校验失败时停止发布附件，保留原校验要求。
# Original Android protocol compatibility

The entry diagnostic test build labels the login screen `进入诊断v1` and appends
`connection-debug.txt` in the external files root at startup, independently of
`Errors` and its exception limit. It records touch/start actions, selected-role
presence, packet type/ID/length, socket send completion, start permission and
scene transitions, server disconnect reasons, EOF and local timeout state.
Packet contents, passwords and account text are not recorded. Each session is
limited to 5000 events. Missing role selection and disconnected start requests
now have visible feedback. Local closes report their observed cause instead of
always labeling the failure a timeout. Actual server disconnect packets keep
their reason-specific dialogs; the file records the reason too.

After login began working, starting a character exposed a second wire-layout
difference: the sample's `Library.ClientControl` includes `OnTeamHookTab` between
`OnAutoHookTab` and `OnBrightBox`. The previous check only inspected models in
`Library.Network`, so it did not cover this nested `Library` object. The test
build restores that byte in the original position. The metadata reader now
recursively follows packet property types to reachable `Library` models, skips
`IgnorePropertyPacket` properties, and checks `StartGameResult` as well. The
pre-fix assembly has all 489 packet types but fails this expanded comparison on
`Library.ClientControl`. A phone's generic disconnect message alone does not
identify database or network failure; its current error log is still useful.

The working 1403 sample contains 489 packet subclasses; the previous bundled
Android build contained 484. `Packet` assigns IDs by sorting these types, so
missing classes changed runtime IDs. Earlier reports quoted namespace-grouped
indices, not the actual wire IDs; that inspection error is corrected below. The phone log reported received packets as
`ClientPackets.Logout` with no handler; this was a protocol compatibility clue,
not evidence that the server had received a valid login request.

`OriginalAndroidPackets.cs` restores the five definitions found in the sample,
and `MarriageTeleport` restores its three sample properties. Both changes are
limited to `ANDROID && BUNDLED_RESOURCE_TEST`, the build intended for this
existing server. Other client and server build configurations keep their current
protocol. Changing this gate requires choosing which deployed server to target.

`tools/inspect-apk-protocol.py` reads managed metadata from v1 assembly blobs or
v2/v3 ELF assembly stores without executing APK code. It requires `dnfile==0.18.0`
and `lz4==4.4.5`. The build workflow reads the original APK before extracting its
resources, then compares the signed result's complete packet table, ordered
property names/types, network model layouts, and login-related enum values.
Metadata token numbers and assembly hashes may differ between compilations;
semantic field types and packet IDs must match. The artifact includes both
`ORIGINAL-PROTOCOL.json` and `APK-PROTOCOL.json` for review.

Earlier validation checked all 489 packet definitions and their property layouts,
but its namespace-grouped ID calculation did not match the runtime comparer.
The previous 484-packet assembly was rejected, and all 34 existing resource/account
checks passed; the ID claim is superseded by the runtime validation below. These checks establish package compatibility, not successful login from
the user's phone. The deployed server is not accessible from this executor.


The phone diagnostic at 17:52:05 logged a 14-byte
`ClientPackets.RequestStartGame` with ID **415**. The original APK's runtime
ordering assigns **416** to that request and **415** to the server reply. No
start reply arrived; the remote socket closed at 17:52:10. Login succeeded
because its client/server IDs, 250/251, happened to match.

The legacy comparer orders general packets first, then sorts by simple type
name across client/server namespaces. Equal client/server names compare as
zero. .NET `List.Sort` is unstable: different metadata input order swapped
42 pairs (84 IDs) despite identical class names and property layouts. The
metadata reader now reproduces .NET introsort, checked against the real runtime
on 68 test cases and against the phone's logged IDs. It rejects the diagnostic
APK against the original table.

For `ANDROID && BUNDLED_RESOURCE_TEST` only, `OriginalAndroidPacketOrder.cs`
pins all 489 wire IDs to the working sample table (source assembly SHA256
`0668a86de0adec777ec9c273de680822dfb4d12c4d8119628de7e1255cf42838`).
It rejects missing or unknown packet types instead of silently shifting IDs.
Other configurations retain the legacy protocol. The APK inspector reads this
canonical table when present and compares it to the original runtime ordering.
`tools/verify-runtime-packet-order.py` also compiles the real `Packet.cs` and
canonical initializer against reverse-ordered packet fixtures: all 489 IDs must
match the independent original report; the request's serialized ID and length,
reply direction, reordered input and unknown-type rejection must pass. This
check runs in CI before building the APK. Phone entry into a map still requires
user testing; wire compatibility alone cannot prove server gameplay behavior.


After entering the map, the phone showed UI/nameplates over a black scene until
resources loaded, and intermittent frozen walking poses while terrain moved.
`MapControl.CreateTexture` previously discarded every candidate frame if any
visible library image was unavailable. With no previous texture this kept the
map black; with a previous texture it could retain stale actor poses. The map
now presents each rendered candidate, keeps retrying missing images, and tracks
floor availability separately so missing actor/effect frames do not invalidate
an already loaded floor. Missing images can appear progressively; this does not
make unavailable server resources available or remove the initial decoding cost.
The surface restore remains in `finally`; a render exception still preserves the
previous texture rather than publishing the failed candidate.

`UserObject` also now uses the independently computed `mir2Frame` for legacy
armour/weapon images, instead of reusing the Mir3 frame index. The test APK adds
at most 60 map-cache snapshots and 120 movement snapshots to
`connection-debug.txt` and displays `画面刷新修复` on the login page. This lets the
phone report actual animation frames and pending resources. Android compilation
and protocol checks are available locally; actual visual behavior needs phone
verification because this executor has no attached Android device.


The follow-up phone log contains 1,907 image response length mismatches, 1,730
DXT read-past-end exceptions and 3,072 invalid Deflate exceptions across three
sessions. Wood/Tilesc, Tilesc, Housesc, Wallsc, SmObjectsc, Tiles30c and Cliffsc
are affected; weapon/ shield decoding also fails. Motion records show frame
indices advancing. Comparing the original APK IL confirmed identical image
record constructors, micro image response parsing, pixel decoding and Deflate
algorithms; the old bundled/saved library indices therefore need checking
against the currently served data, not a relaxed byte-count check.

Image downloads now require both length and storage position to match the local
index. A mismatch, invalid compressed payload or truncated DXT payload requests
a current micro-server header, with one outstanding request and a one-minute
cooldown per library. `LibraryHeaderValidator` parses the full metadata, including
encrypted v2/v3 and legacy Zircon layouts, and checks lengths, counts and payload
bounds. A rejected server header leaves the existing resource intact. A valid
header is written to a temporary sparse file, then installed atomically on the
game thread; matching library readers and map textures are invalidated and the
old queued disk writes are cleared. New image requests use the current positions
and sizes. Shared synchronization protects cache lists and prevents the timer
writer from modifying a file during replacement. Decode errors are retried no
more than once per second, avoiding the prior per-frame exception storm.
Each replacement also advances a library generation, rejecting image responses
from requests that began before the replacement so they cannot repopulate the
new file with stale cache data.

The 23 recovery checks include five real bundled headers, invalid metadata,
server response length/position rejection, successful replacement and subsequent
image fetch, duplicate refresh suppression, map invalidation and preservation of
old files on a malformed server response. The HTTP recovery test uses an
in-process loopback fixture and links the real helper, parser and validator.
Nonlocal destinations retain the inherited proxy. CI runs these checks against
the actual extracted bundle. The test login label is `资源索引修复`; phone
verification and successful hydration from the live micro server remain required.

The new-server test build targets game `118.25.67.175:7000`, micro resources
`118.25.67.175:8000` and updates `http://118.25.67.175:7080/`. The test-only
native startup applies these endpoints after bootstrap configuration is loaded,
forces network configuration on and uses update username `mobile`. It preserves
an existing phone configuration's private update password across bootstrap
extraction; a fresh installation must set the update password in `Mir3.ini`.
No new update credential is stored in source control. CI stamps the APK version
`1.0.0.1` as supplied for this server and displays `新服务器测试` on login.
This lower Android versionCode may require uninstalling an older test APK;
back up phone configuration before doing so. Packet ordering remains matched to
the original inspected Android APK. The new server's binary and actual login
have not been verified; missing server-side handlers require a separate protocol
comparison, not a claim that changing endpoints resolves them.

The follow-up new-server phone log repeatedly requests the missing local
`Data/StartMobileScene.Zl` header and receives HTTP NotFound. `ReadLibrary` only
requests headers when the local file does not exist. Bootstrap previously skipped
`Data.zip` when the phone's configured APK version matched the installed APK;
manually supplied Game settings can therefore suppress missing UI installation.
Native startup now also installs the bootstrap when StartMobileScene.Zl is
missing, retaining the existing test-build password preservation and endpoint
application. The same log shows login request ID 250, then incoming ID 249
classified as LevelChanged with a 10436-byte payload and handler errors. The user
confirmed the new server is an externally obtained binary. Its actual protocol
assembly is required to compare packet numbering; this UI fix does not establish
login compatibility with that server and no packet IDs have been guessed.

At the user's request, the bundled test workflow now builds with
`RepositoryServerProtocol=true`. It compiles `ServerLibrary/ServerLibrary.csproj`
and derives the canonical 484-packet wire table from that Release assembly.
The runtime fixture loads the actual server assembly, runs its Packet static
initializer and checks every ID independently against the metadata report,
then checks Android's pinned table, serialized start request, reply direction,
metadata-order independence and unknown-type rejection. CI refuses stale tables.
In this mode the five original-APK-only packet types, MarriageTeleport fields
and ClientControl.OnTeamHookTab are excluded. The final APK protocol is compared
against the newly built repository server, including reachable model property
layouts and login enums. Server Login is 249, client Login 250, server
RequestStartGame 414 and client RequestStartGame 415. The original-APK mode
remains available when the flag is absent. The login marker is `仓库协议测试`.

All 156 available original resource assets (Data.zip, base ZIP, manifests and
152 compressed patches) remain bundled and verified. This incorporates all
available packages; it does not synthesize images missing from those packages.
The server addresses, phone update credential preservation and missing UI
bootstrap recovery remain unchanged. The externally downloaded running server
has not been inspected, so compatibility is verified against repository source,
with actual login to be tested on the phone.
