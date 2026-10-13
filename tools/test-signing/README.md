# Fixed public test signing identity

`mir3-public-test.keystore` is an intentionally public development key generated
for this repository's bundled test APKs. It is not a production credential.
Anyone with the repository can sign with it; do not use it to establish publisher
trust or to publish a production release.

- Alias: `mir3-test`
- Store and key password: `android` (public test configuration)
- Certificate SHA-256: `cf3fde595340c00308c09809e18ee924b55e84c1805374da51c3b86416b8333e`

`BundledResourceTestBuild=true` selects this identity for both local and CI builds.
Keep this file unchanged so future test APKs can update each other. CI verifies the
signed APK certificate against the pinned fingerprint and preserves v1/v2/v3
signature verification. Production builds must supply their own private signing
configuration.

Switching from an APK signed by MT or an earlier CI-generated debug certificate
may require one uninstall/reinstall. After that, use the delivered APK directly;
re-signing it in another tool changes the identity again.
