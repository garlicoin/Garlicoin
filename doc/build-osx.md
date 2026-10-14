macOS BUILD NOTES
=================

This document describes the two native macOS build paths for the maintained Garlicoin Core 0.18.x line. Intel and Apple Silicon are built separately; the project does not currently publish a Universal2 binary.

Validated CI baseline
---------------------

The repository currently validates:

| Target | GitHub runner | Deployment target | Artifact family |
| --- | --- | ---: | --- |
| Intel x86_64 | `macos-15-intel` | macOS 10.13 | `osx64` |
| Apple Silicon ARM64 | `macos-15` | macOS 11.0 | `osx-arm64` |

Both paths use Xcode 16, macOS SDK 15.0, Qt 5.15.19, OpenSSL 3.5.9, and Berkeley DB 4.8.30 for wallet compatibility.

Qt, OpenSSL, Berkeley DB, and the other pinned dependencies are built through the repository `depends` system. Release validation checks that the expected pinned libraries are used and that non-system Qt/OpenSSL/BDB dynamic dependencies are not left behind.

The CI matrix is the supported release path. Other macOS/Xcode combinations may work, but are not implied to be validated by this document.

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

Use a native Intel Mac/runner for the x86_64 build and a native Apple Silicon Mac/runner for the ARM64 build.

Intel x86_64
------------

```sh
export MACOSX_DEPLOYMENT_TARGET=10.13
export DEVELOPER_DIR=/Applications/Xcode_16.app/Contents/Developer
export SDKROOT="$(xcrun --sdk macosx --show-sdk-path)"
export OSX_SDK_VERSION="$(xcrun --sdk macosx --show-sdk-version)"
export HOST="$(depends/config.guess)"

test "$(uname -m)" = x86_64

gmake -j3 -C depends HOST="$HOST" \
  OSX_MIN_VERSION="$MACOSX_DEPLOYMENT_TARGET" \
  OSX_SDK_VERSION="$OSX_SDK_VERSION" \
  OSX_SDK="$SDKROOT" \
  darwin_CXX="$(xcrun -f clang++) -mmacosx-version-min=$MACOSX_DEPLOYMENT_TARGET -stdlib=libc++ -Wno-error=enum-constexpr-conversion" \
  HOST_ID_SALT=native-xcode16-enum-compat \
  darwin_native_packages= \
  qt_config_opts_darwin="-platform macx-clang -no-framework"

./autogen.sh
CONFIG_SITE="$PWD/depends/$HOST/share/config.site" \
  ./configure \
    --enable-wallet \
    --with-gui=qt5 \
    --disable-tests \
    --disable-bench

gmake -j3
```

For the validated Intel release path, `HOST` must resolve to an `x86_64-apple-darwin*` target.

Apple Silicon ARM64
-------------------

GNU Autotools calls the canonical CPU `aarch64`; Apple Clang, Mach-O and `lipo` call it `arm64`. The repository config scripts accept `arm64-apple-darwin` and canonicalize it to `aarch64-apple-darwin`. This does not imply emulation.

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
  OSX_SDK_VERSION="$OSX_SDK_VERSION" \
  OSX_SDK="$SDKROOT" \
  darwin_CXX="$(xcrun -f clang++) -mmacosx-version-min=$MACOSX_DEPLOYMENT_TARGET -stdlib=libc++ -Wno-error=enum-constexpr-conversion" \
  HOST_ID_SALT=native-xcode16-enum-compat \
  darwin_native_packages= \
  qt_config_opts_darwin="-platform macx-clang -no-framework QMAKE_APPLE_DEVICE_ARCHS=arm64 QMAKE_MACOSX_DEPLOYMENT_TARGET=11.0"

./autogen.sh
CRYPTO_CFLAGS="-I$PWD/depends/$HOST/include" \
CRYPTO_LIBS="$PWD/depends/$HOST/lib/libcrypto.a" \
CONFIG_SITE="$PWD/depends/$HOST/share/config.site" \
  ./configure \
    --prefix=/ \
    --enable-wallet \
    --with-gui=qt5 \
    --enable-tests \
    --disable-bench

gmake -j3
```

Explicit `CRYPTO_CFLAGS` and `CRYPTO_LIBS` keep recursive secp256k1 OpenSSL test cross-checks on the pinned `depends` archive. They do not disable those tests.

Expected binaries
-----------------

Both architectures produce:

```text
src/garlicoind
src/garlicoin-cli
src/garlicoin-tx
src/qt/garlicoin-qt
```

Create the application bundle with:

```sh
gmake appbundle
```

The GUI executable is:

```text
Garlicoin-Qt.app/Contents/MacOS/Garlicoin-Qt
```

Architecture and linkage verification
-------------------------------------

For ARM64, check all executables and the app bundle:

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

For Intel, perform the same architecture/linkage checks with `x86_64` as the expected Mach-O architecture.

The local ad-hoc signature used by the ARM64 validation path seals the app resources. It uses no Apple certificate, identity, or credentials and is separate from Developer ID signing and notarization.

Release validation
------------------

Do not treat a successful local compile as release validation. `.github/workflows/release-validation-ci.yml` is the source of truth for the current release checks.

The maintained macOS validation covers architecture, deployment load commands, system-only dynamic linkage, app metadata/signature, mounted DMG contents, focused Core/secp tests, Allium vectors, and CLI/Cocoa wallet smoke coverage. The release pipeline also verifies Intel -> ARM64 -> Intel Berkeley DB wallet interchange.

ARM64 artifacts use `garlicoin-X.Y.Z-osx-arm64.tar.gz` and `garlicoin-X.Y.Z-osx-arm64.dmg`. Intel retains the existing `osx64` artifact names.

Runtime and signing limits
--------------------------

The native CI runtime is macOS 15. A deployment load command of 10.13 or 11.0 is not by itself runtime certification on every older macOS release.

The maintenance pipeline does not currently add Apple Developer ID signing or notarization. Gatekeeper behavior for downloaded public builds remains a separate real-device validation concern.

Legacy paths
------------

The historical Linux-to-Darwin cross-build workflows and the temporary Qt 5.15/OpenSSL 3 proof workflow have been removed. The maintained release paths are the two native jobs described above.
