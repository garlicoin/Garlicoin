Garlicoin Core 0.18.5 release notes
===================================

Garlicoin Core 0.18.5 is the stable maintenance release for the maintained 0.18.x line.
It promotes the 0.18.5 release-candidate work after automated release validation and real Apple Silicon testing, and supersedes v0.18.4 as the current stable release.

Published release
-----------------

Garlicoin Core v0.18.5 was published on 2026-10-16 from commit `241847936223a3024cdb507d2b43bbb29aa33694`. The public `v0.18.5` tag points to that exact commit.

The final exact-tag Release Validation run `38888269314` completed successfully across the maintained release matrix, and Tagged Release Publisher run `38888241886` then assembled the final assets, generated `SHA256SUMS`, verified the packaged version, and published the stable GitHub release.

Release page:

https://github.com/garlicoin/Garlicoin/releases/tag/v0.18.5

Highlights
----------

- Adds native macOS ARM64 release artifacts for Apple Silicon Macs.
- Keeps the existing native macOS x86_64 release for Intel Macs.
- Preserves the current Linux x86_64 and Windows x86_64 release targets.
- Keeps the existing Qt 5.15.19, OpenSSL 3.5.9 and Berkeley DB 4.8.30 maintenance baseline.
- Extends release validation with native ARM64 packaging, DMG checks, Allium regression vectors and Intel -> ARM64 -> Intel wallet compatibility checks.
- Includes targeted P2P and validation robustness fixes developed and validated during the 0.18.5 release-candidate cycle.
- Refreshes the Garlicoin Core / GRLC.eu maintenance presentation and points the About dialog at the maintained garlicoin/Garlicoin source repository.

P2P and validation maintenance
------------------------------

- Improves compact-block reconstruction state handling after a reconstruction attempt has completed.
- Ensures the `getdata` receive queue continues to make progress when it contains an inventory item that is not handled by the current path.
- Limits redundant `getheaders` responses while processing a single `inv` message.
- Fixes the lifetime of precomputed transaction data used by script checks during block connection.
- Makes orphan-transaction processing resumable instead of requiring all dependent work to complete in one pass.
- Preserves the peer ownership relationship for blocks that are already in flight.
- Adds per-peer rate limiting to `addr` processing to bound the amount of work performed for address announcements.
- Widens internal addrman entry identifiers to 64-bit values while keeping the existing serialized `peers.dat` format unchanged.

Build and release maintenance
-----------------------------

- Fixes the native ARM64 release path so the ccache configuration directory exists before the parallel build starts.
- Makes build metadata recognize lightweight release tags so release binaries can be verified against the exact public tag.
- Finalizes the 0.18.5 user-visible maintenance text, including the Garlicoin Core 2011-2026 copyright range while preserving the historical Bitcoin Core 2009-2022 line.

Compatibility
-------------

This release does not intentionally change Garlicoin consensus, Allium proof of work, network identity, address formats, blockchain/datadir compatibility, RPC behavior, or the Berkeley DB wallet format.

It does include targeted maintenance changes to P2P state handling and resource management. Existing Garlicoin Core 0.18.x datadirs and wallets are intended to remain compatible.

macOS targets
-------------

This release provides two separate macOS builds:

- Intel x86_64, deployment target macOS 10.13;
- Apple Silicon ARM64, deployment target macOS 11.0.

The ARM64 build is a native thin ARM64 build. A Universal Binary is not part of 0.18.5.

Validation
----------

The 0.18.5 release-candidate line passed the maintained release-validation pipeline across Linux x86_64, Windows x86_64, macOS Intel x86_64 and native macOS Apple Silicon ARM64, including packaging, DMG checks, focused tests, Allium regression vectors and Intel -> ARM64 -> Intel Berkeley DB wallet interchange.

A real Apple Silicon end-user test also confirmed that the ARM64 build launches and connects to peers successfully.

The final `v0.18.5` tag was rebuilt and validated again by the exact-tag release pipeline before the public release artifacts were published.

Signing and Gatekeeper
----------------------

The current maintenance release pipeline does not add Apple Developer ID signing or notarization. macOS may therefore show the usual Gatekeeper warning for an unsigned application downloaded from the internet.

Release artifacts
-----------------

The stable release includes:

- Linux x86_64 tarball;
- Windows x86_64 ZIP and installer;
- macOS Intel x86_64 TAR and DMG;
- macOS Apple Silicon ARM64 TAR and DMG;
- source archive;
- SHA256SUMS.

Verify downloaded artifacts against the published `SHA256SUMS` file before installation.
