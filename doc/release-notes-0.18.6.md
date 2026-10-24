Garlicoin Core 0.18.6 release notes
===================================

Garlicoin Core 0.18.6 is a maintenance release in the existing 0.18.x line.
It supersedes v0.18.5, adding full native Linux ARM64 release packaging,
historical reindex fixes, peer-time hardening and consistent project links.

Highlights
----------

- Adds native Linux ARM64 (AArch64) packages with garlicoind, garlicoin-cli,
  garlicoin-qt and Berkeley DB 4.8 wallet compatibility (PR #83).
- Adds native ARM64 GitHub Actions release validation with ELF checks, focused
  unit/wallet/CLI tests, Xvfb GUI smoke, packaged-version check and SHA256.
- Fixes historical -reindex failures: corrects genesis-era BIP34 activation
  height/hash metadata and repairs height lookup when importing blocks with
  an out-of-order parent (PR #78).
- Hardens untrusted P2P time samples against signed int64 overflow, both in
  median-time handling and subtraction of peer VERSION timestamps (PR #80,
  PR #82; CVE-2024-52912-related mitigation and boundary regression tests).
- Adds a missing C++ <array> header to net_processing.cpp (PR #79).
- Aligns garlicoind -version and Qt About: garlicoin.io is the official site,
  grlc.eu and garlicoin.org are additional resources, and source code lives
  at github.com/garlicoin/Garlicoin. Retains MIT license and attributes
  Garlicoin Core 2011-2026 / Bitcoin Core 2009-2022 (PR #84).

Reindex and compatibility
-------------------------

The BIP34 activation metadata correction concerns validation of the early
mainnet chain during reindexing; it is not intended to create a chain fork.
The release is designed to retain the existing Garlicoin blockchain,
Allium proof of work, difficulty rules, address formats, network identity,
block/transaction serialization, existing datadirs and Berkeley DB 4.8
wallet.dat compatibility. No wallet format migration is required.

Linux ARM64 runtime
-------------------

The new native Linux ARM64 tarball contains the full Qt GUI wallet, daemon
and CLI. On Linux ARM64, GUI use needs system Qt/X11/XCB runtime libraries
documented in doc/build-unix.md. These are not bundled in the tarball.
Daemon-only installations do not require the GUI runtime dependencies.

Other maintained release targets remain Linux x86_64, Windows x86_64,
macOS Intel x86_64 and macOS Apple Silicon ARM64.

Release validation and platform baseline
----------------------------------------

The maintained dependency baseline remains Qt 5.15.19, OpenSSL 3.5.9 and
Berkeley DB 4.8.30.

Prior ARM64 integration validation passed across the release platform matrix
in Release Validation CI run 40122257474 (2026-10-24). The tagged release
publisher always repeats validation on the exact v0.18.6 release tag before
publication; the tagged results and SHA256SUMS are authoritative for the
published assets. Native Linux ARM64 runner validation does not guarantee
compatibility with every ARM64 Linux distribution.

Expected release assets
-----------------------

- Linux x86_64 tarball;
- Linux ARM64 tarball (new);
- Windows x86_64 ZIP and installer;
- macOS Intel x86_64 TAR and DMG;
- macOS Apple Silicon ARM64 TAR and DMG;
- source tarball and combined SHA256SUMS.

Verify downloaded artifacts using SHA256SUMS. macOS builds remain unsigned
and unnotarized; Apple Gatekeeper may display an expected warning.

Project links
-------------

- Official website: https://garlicoin.io
- Additional services: https://grlc.eu and https://garlicoin.org
- Repository: https://github.com/garlicoin/Garlicoin
- Previous release: https://github.com/garlicoin/Garlicoin/releases/tag/v0.18.5
