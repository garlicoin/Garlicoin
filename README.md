Garlicoin Core
==============

[![Linux CI](https://github.com/garlicoin/Garlicoin/actions/workflows/linux-ci.yml/badge.svg?branch=master)](https://github.com/garlicoin/Garlicoin/actions/workflows/linux-ci.yml)
[![Ubuntu Toolchain CI](https://github.com/garlicoin/Garlicoin/actions/workflows/ubuntu-toolchain-ci.yml/badge.svg?branch=master)](https://github.com/garlicoin/Garlicoin/actions/workflows/ubuntu-toolchain-ci.yml)
[![Qt GUI CI](https://github.com/garlicoin/Garlicoin/actions/workflows/qt-ci.yml/badge.svg?branch=master)](https://github.com/garlicoin/Garlicoin/actions/workflows/qt-ci.yml)
[![Windows MinGW CI](https://github.com/garlicoin/Garlicoin/actions/workflows/windows-ci.yml/badge.svg?branch=master)](https://github.com/garlicoin/Garlicoin/actions/workflows/windows-ci.yml)
[![Release Validation CI](https://github.com/garlicoin/Garlicoin/actions/workflows/release-validation-ci.yml/badge.svg?branch=master)](https://github.com/garlicoin/Garlicoin/actions/workflows/release-validation-ci.yml)
![Maintained 2026](https://img.shields.io/badge/maintained-2026-brightgreen)
![Stable release 0.18.6](https://img.shields.io/badge/stable-0.18.6-blue)
![License MIT](https://img.shields.io/badge/license-MIT-blue)

This is the actively maintained Garlicoin Core repository under the [garlicoin](https://github.com/garlicoin) GitHub organization, continuing the historical [GarlicoinOrg/Garlicoin](https://github.com/GarlicoinOrg/Garlicoin) codebase.

Official website: [garlicoin.io](https://garlicoin.io/)

Network infrastructure, explorer and project services: [grlc.eu](https://grlc.eu/) and [garlicoin.org](https://garlicoin.org/)

Garlicoin Core **0.18.6** is the current stable maintenance release. It adds native Linux ARM64 daemon, CLI and GUI packages, fixes historical reindexing and peer timestamp overflow, and unifies website and source attribution in Qt About and daemon version output. See [0.18.6 release notes](doc/release-notes-0.18.6.md).

For peer-time security hardening and historical reindex fixes, upgrade to [Garlicoin Core v0.18.6](https://github.com/garlicoin/Garlicoin/releases/tag/v0.18.6). Earlier releases do not include these fixes.

The maintained 0.18.x line preserves Garlicoin consensus, Allium proof of work, DarkGravityWave, wallet format, address formats, network identity and existing user datadirs. Garlicoin is Litecoin-derived, with Litecoin Core 0.18.1 used as the primary upstream reference for compatible maintenance fixes.

The **0.18.6** release is published as the **GRLC.eu Maintenance Release**, reflecting the infrastructure and maintenance work used to maintain the 0.18.x line. The project itself remains Garlicoin Core.

Current maintenance baseline
----------------------------

The maintained 0.18.x source line currently includes:

- Qt **5.15.19**;
- OpenSSL **3.5.9**;
- Berkeley DB **4.8.30** wallet compatibility;
- Linux x86_64 build and release validation;
- native Linux ARM64 full wallet/GUI/daemon release packaging and validation;
- Windows x86_64 MinGW build and release validation;
- native macOS Intel x86_64 validation with Xcode 16 / macOS SDK 15.0, retaining deployment target **10.13**;
- native macOS Apple Silicon ARM64 validation with Xcode 16 / macOS SDK 15.0 and deployment target **11.0**;
- Python 3.12+ compatible P2P functional-test transport;
- removal of the legacy BIP70 Payment Protocol runtime and implementation while keeping normal `garlicoin:` payment URI support;
- maintained dependency sources, build-system fixes and selected security/robustness backports;
- targeted P2P hardening for compact-block reconstruction, `getdata` queue progress, `inv`/`getheaders` handling, orphan processing, blocks-in-flight ownership, `addr` rate limiting and addrman internal IDs;
- validation lifetime hardening for precomputed transaction data used by script checks;
- original wallet appearance with corrected Qt High-DPI scaling and refreshed Garlicoin / grlc.eu maintenance branding.

These maintenance changes are intended to improve buildability, portability, robustness and maintainability without changing the existing Garlicoin network or wallet compatibility.

Release status
--------------

### Stable: Garlicoin Core 0.18.6

Garlicoin Core **v0.18.6** is the maintained stable release. The tagged
publisher validates exact-tag builds for Linux x86_64 and ARM64, Windows x86_64,
macOS Intel and Apple Silicon before distributing the release assets.

[View the v0.18.6 release](https://github.com/garlicoin/Garlicoin/releases/tag/v0.18.6)

Stable downloads:

- [Windows installer (x86_64)](https://github.com/garlicoin/Garlicoin/releases/download/v0.18.6/garlicoin-0.18.6-win64-setup.exe)
- [Windows ZIP (x86_64)](https://github.com/garlicoin/Garlicoin/releases/download/v0.18.6/garlicoin-0.18.6-win64.zip)
- [Linux tarball (x86_64)](https://github.com/garlicoin/Garlicoin/releases/download/v0.18.6/garlicoin-0.18.6-linux-x86_64.tar.gz)
- [Linux tarball (ARM64)](https://github.com/garlicoin/Garlicoin/releases/download/v0.18.6/garlicoin-0.18.6-linux-arm64.tar.gz)
- [macOS DMG (Intel x86_64)](https://github.com/garlicoin/Garlicoin/releases/download/v0.18.6/garlicoin-0.18.6-osx64.dmg)
- [macOS tarball (Intel x86_64)](https://github.com/garlicoin/Garlicoin/releases/download/v0.18.6/garlicoin-0.18.6-osx64.tar.gz)
- [macOS DMG (Apple Silicon ARM64)](https://github.com/garlicoin/Garlicoin/releases/download/v0.18.6/garlicoin-0.18.6-osx-arm64.dmg)
- [macOS tarball (Apple Silicon ARM64)](https://github.com/garlicoin/Garlicoin/releases/download/v0.18.6/garlicoin-0.18.6-osx-arm64.tar.gz)
- [Source tarball](https://github.com/garlicoin/Garlicoin/releases/download/v0.18.6/garlicoin-0.18.6.tar.gz)
- [SHA256SUMS](https://github.com/garlicoin/Garlicoin/releases/download/v0.18.6/SHA256SUMS)

See [`doc/release-notes-0.18.6.md`](doc/release-notes-0.18.6.md) for details
of the current maintenance release.

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

The `master` branch is the maintained integration branch. Garlicoin Core 0.18.6 is the current stable release; future maintenance should continue as separate, narrowly scoped changes with the same compatibility and validation discipline.

Maintenance changes should remain narrowly scoped and should not mix routine build/dependency work with consensus or wallet-format changes.

See [CONTRIBUTING.md](CONTRIBUTING.md).

Historical Garlicoin release tags remain available in the [previous GarlicoinOrg repository](https://github.com/GarlicoinOrg/Garlicoin/tags).

Community discussion: [Discord](https://discord.gg/mmAb4ewGb6)

License
-------

Garlicoin Core is released under the MIT license. See [COPYING](COPYING).
