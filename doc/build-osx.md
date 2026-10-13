macOS BUILD NOTES
=================

This document describes the native macOS build paths for the maintained Garlicoin Core 0.18.x line.

Validated CI baseline
---------------------

The repository currently validates macOS with:

- Intel x86_64 runner: `macos-15-intel`;
- Xcode 16;
- macOS SDK 15.0;
- deployment target: macOS 10.13;
- Qt 5.15.19;
- OpenSSL 3.5.9;
- Berkeley DB 4.8.30 for wallet compatibility.

Qt, OpenSSL, Berkeley DB, and the other pinned dependencies are built through the repository `depends` system. The release build verifies that Qt/OpenSSL/BDB are not left as non-system dynamic dependencies.

The CI baseline is the supported release path. Other macOS/Xcode combinations may work, but are not implied to be validated by this document.

Prerequisites
-------------

Install Xcode 16 and select it as the active developer directory. Install the build tools with Homebrew:

```sh
brew install autoconf automake libtool pkg-config make
```

Verify the native architecture, Xcode, and SDK:

```sh
uname -m
xcodebuild -version
xcrun --sdk macosx --show-sdk-version
```

The validated CI values are `x86_64`, Xcode 16, and SDK 15.0.

Build pinned dependencies
-------------------------

From the repository root:

```sh
export MACOSX_DEPLOYMENT_TARGET=10.13
export DEVELOPER_DIR=/Applications/Xcode_16.app/Contents/Developer
export SDKROOT="$(xcrun --sdk macosx --show-sdk-path)"
export OSX_SDK_VERSION="$(xcrun --sdk macosx --show-sdk-version)"
export HOST="$(depends/config.guess)"

gmake -j3 -C depends HOST="$HOST" \
  OSX_MIN_VERSION="$MACOSX_DEPLOYMENT_TARGET" \
  OSX_SDK_VERSION="$OSX_SDK_VERSION" \
  OSX_SDK="$SDKROOT" \
  darwin_CXX="$(xcrun -f clang++) -mmacosx-version-min=$MACOSX_DEPLOYMENT_TARGET -stdlib=libc++ -Wno-error=enum-constexpr-conversion" \
  HOST_ID_SALT=native-xcode16-enum-compat \
  darwin_native_packages= \
  qt_config_opts_darwin="-platform macx-clang -no-framework"
```

The detected host must be an `x86_64-apple-darwin*` target for the validated release configuration.

Configure and build Core + Qt
-----------------------------

```sh
./autogen.sh
CONFIG_SITE="$PWD/depends/$HOST/share/config.site" \
  ./configure \
    --enable-wallet \
    --with-gui=qt5 \
    --disable-tests \
    --disable-bench

gmake -j3
```

Expected binaries include:

```text
src/garlicoind
src/garlicoin-cli
src/garlicoin-tx
src/qt/garlicoin-qt
```

Create the app bundle
---------------------

The native release path creates the application bundle with:

```sh
gmake appbundle
```

The resulting GUI executable is located at:

```text
Garlicoin-Qt.app/Contents/MacOS/Garlicoin-Qt
```

The release workflow additionally creates and validates the DMG using native macOS tooling.

Verification
------------

For release work, do not rely only on a successful compile. The maintained release-validation workflow checks the Mach-O architecture, deployment target, static dependency linkage, CLI/GUI version output, app bundle, and release packaging.

See `.github/workflows/release-validation-ci.yml`.

Legacy Linux-to-Darwin cross-build workflows and the temporary Qt 5.15/OpenSSL 3 macOS proof workflow have been removed from the active GitHub Actions set. The Intel release build remains native x86_64 through the release-validation workflow; the separate Apple Silicon path is described below.

Native Apple Silicon ARM64
--------------------------

Apple Silicon is built separately from Intel; this is not a universal/universal2 build. GitHub Actions uses `macos-15`, verifies `uname -m = arm64`, and pins Xcode 16 / SDK 15.0. ARM64 uses deployment target **11.0**. The Intel job above retains **10.13**.

GNU Autotools calls the canonical CPU `aarch64`; Apple Clang, Mach-O and `lipo` call it `arm64`. The repository config scripts accept `arm64-apple-darwin` and canonicalize it to `aarch64-apple-darwin`. This does not imply emulation.

On a native Apple Silicon Mac, after installing the same build tools:

```sh
test "$(uname -m)" = arm64
export MACOSX_DEPLOYMENT_TARGET=11.0
export DEVELOPER_DIR=/Applications/Xcode_16.app/Contents/Developer
export SDKROOT="$(xcrun --sdk macosx --show-sdk-path)"
export OSX_SDK_VERSION="$(xcrun --sdk macosx --show-sdk-version)"
test "$OSX_SDK_VERSION" = 15.0
export HOST="$(depends/config.guess)"

gmake -j3 -C depends HOST="$HOST" \
  OSX_MIN_VERSION="$MACOSX_DEPLOYMENT_TARGET" \
  OSX_SDK_VERSION="$OSX_SDK_VERSION" OSX_SDK="$SDKROOT" \
  darwin_CXX="$(xcrun -f clang++) -mmacosx-version-min=$MACOSX_DEPLOYMENT_TARGET -stdlib=libc++ -Wno-error=enum-constexpr-conversion" \
  HOST_ID_SALT=native-xcode16-enum-compat \
  darwin_native_packages= \
  qt_config_opts_darwin="-platform macx-clang -no-framework QMAKE_APPLE_DEVICE_ARCHS=arm64 QMAKE_MACOSX_DEPLOYMENT_TARGET=11.0"

./autogen.sh
CRYPTO_CFLAGS="-I$PWD/depends/$HOST/include" \
CRYPTO_LIBS="$PWD/depends/$HOST/lib/libcrypto.a" \
CONFIG_SITE="$PWD/depends/$HOST/share/config.site" \
  ./configure --prefix=/ --enable-wallet --with-gui=qt5 --enable-tests --disable-bench
gmake -j3
```

Explicit `CRYPTO_CFLAGS`/`CRYPTO_LIBS` keep the recursive secp256k1 OpenSSL test cross-checks on the pinned depends archive. They do not disable those tests.

Check all four executables:

```sh
for binary in src/garlicoind src/garlicoin-cli src/garlicoin-tx src/qt/garlicoin-qt; do
  file "$binary"
  test "$(lipo -archs "$binary")" = arm64
  otool -L "$binary"
  otool -l "$binary"
done

gmake appbundle
codesign --force --sign - --timestamp=none Garlicoin-Qt.app
codesign --verify --deep --strict Garlicoin-Qt.app
test "$(lipo -archs Garlicoin-Qt.app/Contents/MacOS/Garlicoin-Qt)" = arm64
```

The local ad-hoc signature seals the ARM64 app's resources. It uses no Apple certificate, identity or credentials and is separate from distribution signing/notarization.

The release-validation ARM64 job checks every depends archive/native generator, thin ARM64 binaries, deployment load commands, system-only dynamic linkage, app metadata/signature, mounted DMG content, existing focused Core/secp tests, Allium vectors and CLI/Cocoa wallet smoke tests. Additional jobs transfer a throwaway regtest wallet **Intel -> ARM64 -> Intel**, verify ownership/signing/version preservation and delete the generated wallet fixtures.

ARM64 artifacts are named `garlicoin-X.Y.Z-osx-arm64.tar.gz` and `garlicoin-X.Y.Z-osx-arm64.dmg`. Intel keeps the existing `osx64` names. The artifact packaging test does not publish a release or change the Core version.

Native runtime proof is on macOS 15; load-command deployment 11.0 alone is not a macOS 11 runtime certification. The workflow tests the packaged Cocoa app on the native runner; older macOS runtime compatibility and distribution notarization remain separate validation tasks.
