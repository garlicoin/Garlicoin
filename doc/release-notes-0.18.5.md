Garlicoin Core 0.18.5 release candidate notes
==============================================

Garlicoin Core 0.18.5-rc1 is a pre-release for the maintained 0.18.x line.
Its main purpose is to validate the new native Apple Silicon build on real M-series Macs before the final 0.18.5 release.

Highlights
----------

- Adds native macOS ARM64 release artifacts for Apple Silicon Macs.
- Keeps the existing native macOS x86_64 release for Intel Macs.
- Preserves the current Linux x86_64 and Windows x86_64 release targets.
- Keeps the existing Qt 5.15.19, OpenSSL 3.5.9 and Berkeley DB 4.8.30 maintenance baseline.
- Extends release validation with native ARM64 packaging, DMG checks, Allium regression vectors and Intel -> ARM64 -> Intel wallet compatibility checks.

Compatibility
-------------

This release candidate does not intentionally change Garlicoin consensus, Allium proof of work, network identity, address formats, datadir compatibility, RPC behavior, P2P behavior, or the Berkeley DB wallet format.

Existing Garlicoin Core 0.18.x datadirs and wallets are intended to remain compatible.

macOS targets
-------------

The release candidate provides two separate macOS builds:

- Intel x86_64, deployment target macOS 10.13;
- Apple Silicon ARM64, deployment target macOS 11.0.

The ARM64 build is a native thin ARM64 build. A Universal Binary is not part of 0.18.5-rc1.

Real-Mac testing requested
--------------------------

The ARM64 build has passed the project release-validation pipeline on a native Apple Silicon GitHub Actions runner, but this release candidate is specifically intended to add one final real-user check on an M1/M2/M3/M4 Mac.

For the ARM64 DMG, please verify:

- the DMG mounts normally;
- Garlicoin-Qt launches;
- a wallet can be created or opened;
- the application can be restarted and the wallet still opens;
- network synchronization starts normally;
- any Gatekeeper message is reported exactly as shown.

If possible, include the Mac model/chip and macOS version with the test result.

Signing and Gatekeeper
----------------------

The current maintenance release pipeline does not add Apple Developer ID signing or notarization. macOS may therefore show the usual Gatekeeper warning for an unsigned application downloaded from the internet.

Release-candidate status
------------------------

This is a GitHub pre-release and is not intended to replace v0.18.4 as the current stable release yet.
After successful real-Mac validation, the project can publish the final v0.18.5 release.

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
