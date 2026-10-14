Garlicoin Core 0.18.5 release candidate notes
==============================================

Garlicoin Core 0.18.5-rc2 is a pre-release for the maintained 0.18.x line.
It supersedes 0.18.5-rc1 and combines the Apple Silicon release work with the maintenance and P2P robustness changes merged since rc1.

Highlights
----------

- Adds native macOS ARM64 release artifacts for Apple Silicon Macs.
- Keeps the existing native macOS x86_64 release for Intel Macs.
- Preserves the current Linux x86_64 and Windows x86_64 release targets.
- Keeps the existing Qt 5.15.19, OpenSSL 3.5.9 and Berkeley DB 4.8.30 maintenance baseline.
- Extends release validation with native ARM64 packaging, DMG checks, Allium regression vectors and Intel -> ARM64 -> Intel wallet compatibility checks.
- Includes targeted P2P and validation maintenance merged after 0.18.5-rc1.

Changes since 0.18.5-rc1
-------------------------

- Improves compact-block reconstruction state handling after a reconstruction attempt has completed.
- Ensures the `getdata` receive queue continues to make progress when it contains an inventory item that is not handled by the current path.
- Limits redundant `getheaders` responses while processing a single `inv` message.
- Fixes the lifetime of precomputed transaction data used by script checks during block connection.
- Makes orphan-transaction processing resumable instead of requiring all dependent work to complete in one pass.
- Preserves the peer ownership relationship for blocks that are already in flight.
- Adds per-peer rate limiting to `addr` processing to bound the amount of work performed for address announcements.
- Widens internal addrman entry identifiers to 64-bit values while keeping the existing serialized `peers.dat` format unchanged.
- Refreshes maintained CI and release documentation used by the 0.18.x release process.

Compatibility
-------------

This release candidate does not intentionally change Garlicoin consensus, Allium proof of work, network identity, address formats, blockchain/datadir compatibility, RPC behavior, or the Berkeley DB wallet format.

It does include targeted maintenance changes to P2P state handling and resource management. Existing Garlicoin Core 0.18.x datadirs and wallets are intended to remain compatible.

macOS targets
-------------

The release candidate provides two separate macOS builds:

- Intel x86_64, deployment target macOS 10.13;
- Apple Silicon ARM64, deployment target macOS 11.0.

The ARM64 build is a native thin ARM64 build. A Universal Binary is not part of 0.18.5.

Release-candidate testing requested
-----------------------------------

The ARM64 build has passed the project release-validation pipeline on a native Apple Silicon GitHub Actions runner, but a final real-user check on an M1/M2/M3/M4 Mac is still requested before the stable 0.18.5 release.

For the ARM64 DMG, please verify:

- the DMG mounts normally;
- Garlicoin-Qt launches;
- a wallet can be created or opened;
- the application can be restarted and the wallet still opens;
- network synchronization starts normally;
- any Gatekeeper message is reported exactly as shown.

For all platforms, normal startup, synchronization, wallet use and peer connectivity are useful rc2 checks.

If possible, include the platform version and, for macOS, the Mac model/chip with the test result.

Signing and Gatekeeper
----------------------

The current maintenance release pipeline does not add Apple Developer ID signing or notarization. macOS may therefore show the usual Gatekeeper warning for an unsigned application downloaded from the internet.

Release-candidate status
------------------------

This is a GitHub pre-release and is not intended to replace v0.18.4 as the current stable release yet.
After successful rc2 validation and real-hardware testing, the project can publish the final v0.18.5 release.

Release artifacts
-----------------

The pre-release is expected to include:

- Linux x86_64 tarball;
- Windows x86_64 ZIP and installer;
- macOS Intel x86_64 TAR and DMG;
- macOS Apple Silicon ARM64 TAR and DMG;
- source archive;
- SHA256SUMS.

Verify downloaded artifacts against the published `SHA256SUMS` file before installation.
