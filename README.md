Garlicoin Core
==============

[![Linux CI](https://github.com/garlicoin/Garlicoin/actions/workflows/linux-ci.yml/badge.svg?branch=master)](https://github.com/garlicoin/Garlicoin/actions/workflows/linux-ci.yml)
[![Ubuntu Toolchain CI](https://github.com/garlicoin/Garlicoin/actions/workflows/ubuntu-toolchain-ci.yml/badge.svg?branch=master)](https://github.com/garlicoin/Garlicoin/actions/workflows/ubuntu-toolchain-ci.yml)
[![Qt GUI CI](https://github.com/garlicoin/Garlicoin/actions/workflows/qt-ci.yml/badge.svg?branch=master)](https://github.com/garlicoin/Garlicoin/actions/workflows/qt-ci.yml)
[![Windows MinGW CI](https://github.com/garlicoin/Garlicoin/actions/workflows/windows-ci.yml/badge.svg?branch=master)](https://github.com/garlicoin/Garlicoin/actions/workflows/windows-ci.yml)
[![Release Validation 0.18.5-rc1](https://img.shields.io/badge/release%20validation-0.18.5--rc1%20passed-brightgreen)](https://github.com/garlicoin/Garlicoin/actions/runs/38521909244)
![Maintained 2026](https://img.shields.io/badge/maintained-2026-brightgreen)
![Stable release 0.18.4](https://img.shields.io/badge/stable-0.18.4-blue)
![Prerelease 0.18.5-rc1](https://img.shields.io/badge/prerelease-0.18.5--rc1-orange)
![License MIT](https://img.shields.io/badge/license-MIT-blue)

This is the actively maintained Garlicoin Core repository under the [garlicoin](https://github.com/garlicoin) GitHub organization, continuing the historical [GarlicoinOrg/Garlicoin](https://github.com/GarlicoinOrg/Garlicoin) codebase.

Official website: [garlicoin.io](https://garlicoin.io/)

Network infrastructure, explorer and project services: [grlc.eu](https://grlc.eu/)

The latest stable release is **Garlicoin Core 0.18.4**. The current public prerelease is **Garlicoin Core 0.18.5-rc1**, which adds native Apple Silicon ARM64 release artifacts alongside Linux x86_64, Windows x86_64 and macOS Intel x86_64 builds.

The maintained 0.18.x line preserves Garlicoin consensus, Allium proof of work, DarkGravityWave, wallet format, address formats, network identity and existing user datadirs. Garlicoin is Litecoin-derived, with Litecoin Core 0.18.1 used as the primary upstream reference for compatible maintenance fixes.

The **0.18.4** release was published as the **GRLC.eu Maintenance Release**, reflecting the infrastructure and maintenance work used to revive the 0.18.x line. The project itself remains Garlicoin Core.

Current maintenance baseline
----------------------------

The maintained 0.18.x source line currently includes:

- Qt **5.15.19**;
- OpenSSL **3.5.9**;
- Berkeley DB **4.8.30** wallet compatibility;
- Linux x86_64 build and release validation;
- Windows x86_64 MinGW build and release validation;
- native macOS Intel x86_64 validation with Xcode 16 / macOS SDK 15.0, retaining deployment target **10.13**;
- native macOS Apple Silicon ARM64 validation with Xcode 16 / macOS SDK 15.0 and deployment target **11.0**;
- Python 3.12+ compatible P2P functional-test transport;
- removal of the legacy BIP70 Payment Protocol runtime and implementation while keeping normal `garlicoin:` payment URI support;
- maintained dependency sources, build-system fixes and selected security/robustness backports;
- original wallet appearance with corrected Qt High-DPI scaling and refreshed Garlicoin / grlc.eu maintenance branding.

These maintenance changes are intended to improve buildability, portability and maintainability without changing the existing Garlicoin network or wallet compatibility.

Release status
--------------

### Stable: Garlicoin Core 0.18.4

Garlicoin Core **v0.18.4** is the latest stable release. It includes validated Linux x86_64, Windows x86_64 and macOS Intel x86_64 artifacts, source code and SHA256 checksums.

[View the v0.18.4 release](https://github.com/garlicoin/Garlicoin/releases/tag/v0.18.4)

Stable downloads:

- [Windows installer (x86_64)](https://github.com/garlicoin/Garlicoin/releases/download/v0.18.4/garlicoin-0.18.4-win64-setup.exe)
- [Windows ZIP (x86_64)](https://github.com/garlicoin/Garlicoin/releases/download/v0.18.4/garlicoin-0.18.4-win64.zip)
- [Linux tarball (x86_64)](https://github.com/garlicoin/Garlicoin/releases/download/v0.18.4/garlicoin-0.18.4-linux-x86_64.tar.gz)
- [macOS DMG (Intel x86_64)](https://github.com/garlicoin/Garlicoin/releases/download/v0.18.4/garlicoin-0.18.4-osx64.dmg)
- [macOS tarball (Intel x86_64)](https://github.com/garlicoin/Garlicoin/releases/download/v0.18.4/garlicoin-0.18.4-osx64.tar.gz)
- [Source tarball](https://github.com/garlicoin/Garlicoin/releases/download/v0.18.4/garlicoin-0.18.4.tar.gz)
- [SHA256SUMS](https://github.com/garlicoin/Garlicoin/releases/download/v0.18.4/SHA256SUMS)

### Prerelease: Garlicoin Core 0.18.5-rc1

Garlicoin Core **v0.18.5-rc1** is the current release candidate for the next maintenance release. Its main purpose is to add and validate native Apple Silicon ARM64 support without introducing unrelated consensus, wallet-format or network changes.

Automated exact-tag release validation passed for:

- Linux x86_64;
- Windows x86_64 MinGW;
- macOS Intel x86_64;
- macOS Apple Silicon ARM64;
- Intel -> ARM64 -> Intel Berkeley DB wallet interchange.

The remaining release-candidate gate is real-device testing of the ARM64 macOS build on an Apple Silicon Mac, including launch / Gatekeeper behavior, wallet creation and reopening, restart and initial synchronization. Until that confirmation is complete, **v0.18.4 remains the recommended stable release**.

[View the v0.18.5-rc1 release](https://github.com/garlicoin/Garlicoin/releases/tag/v0.18.5-rc1)

Prerelease downloads:

- [Windows installer (x86_64)](https://github.com/garlicoin/Garlicoin/releases/download/v0.18.5-rc1/garlicoin-0.18.5-rc1-win64-setup.exe)
- [Windows ZIP (x86_64)](https://github.com/garlicoin/Garlicoin/releases/download/v0.18.5-rc1/garlicoin-0.18.5-rc1-win64.zip)
- [Linux tarball (x86_64)](https://github.com/garlicoin/Garlicoin/releases/download/v0.18.5-rc1/garlicoin-0.18.5-rc1-linux-x86_64.tar.gz)
- [macOS DMG (Intel x86_64)](https://github.com/garlicoin/Garlicoin/releases/download/v0.18.5-rc1/garlicoin-0.18.5-rc1-osx64.dmg)
- [macOS tarball (Intel x86_64)](https://github.com/garlicoin/Garlicoin/releases/download/v0.18.5-rc1/garlicoin-0.18.5-rc1-osx64.tar.gz)
- [macOS DMG (Apple Silicon ARM64)](https://github.com/garlicoin/Garlicoin/releases/download/v0.18.5-rc1/garlicoin-0.18.5-rc1-osx-arm64.dmg)
- [macOS tarball (Apple Silicon ARM64)](https://github.com/garlicoin/Garlicoin/releases/download/v0.18.5-rc1/garlicoin-0.18.5-rc1-osx-arm64.tar.gz)
- [Source tarball](https://github.com/garlicoin/Garlicoin/releases/download/v0.18.5-rc1/garlicoin-0.18.5-rc1.tar.gz)
- [SHA256SUMS](https://github.com/garlicoin/Garlicoin/releases/download/v0.18.5-rc1/SHA256SUMS)

Verify downloaded release artifacts against the corresponding `SHA256SUMS` file before installation.

Building
--------

Start with [INSTALL.md](INSTALL.md) and the maintained documentation index in [`doc/README.md`](doc/README.md).

Platform notes:

- Linux / Unix: [`doc/build-unix.md`](doc/build-unix.md)
- Ubuntu toolchain validation: [`doc/ubuntu-toolchain.md`](doc/ubuntu-toolchain.md)
- Windows x86_64: [`doc/build-windows.md`](doc/build-windows.md)
- macOS Intel x86_64 / Apple Silicon ARM64: [`doc/build-osx.md`](doc/build-osx.md)

Testing
-------

```sh
make check
python3 test/functional/test_runner.py
```

See [`src/test/README.md`](src/test/README.md) and [`test/functional/`](test/functional/) for details.

Documentation
-------------

The maintained documentation lives in [`doc/`](doc/) and is indexed in [`doc/README.md`](doc/README.md).

Historical Bitcoin and Litecoin documentation inherited from upstream is not kept in the maintained documentation tree when it does not describe the current Garlicoin line. Older material remains available through Git history and the respective upstream projects.

Development
-----------

The `master` branch is the maintained integration branch. The current release goal is to complete real-device Apple Silicon validation and promote the 0.18.5 maintenance line once the release candidate is confirmed.

Maintenance changes should remain narrowly scoped and should not mix routine build/dependency work with consensus or wallet-format changes.

See [CONTRIBUTING.md](CONTRIBUTING.md).

Historical Garlicoin release tags remain available in the [previous GarlicoinOrg repository](https://github.com/GarlicoinOrg/Garlicoin/tags).

Community discussion: [Discord](https://discord.gg/mmAb4ewGb6)

License
-------

Garlicoin Core is released under the MIT license. See [COPYING](COPYING).
