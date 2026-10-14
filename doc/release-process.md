Garlicoin Core release process
==============================

This document describes the maintained release process for the Garlicoin Core 0.18.x line in this repository.

Release principles
------------------

Maintenance releases should remain narrowly scoped. They must not intentionally change Garlicoin consensus, proof of work, network identity, address formats, existing blockchain/datadir compatibility, or the Berkeley DB 4.8 wallet format unless such a change is explicitly planned and reviewed as a separate project.

The repository's maintained release path is GitHub Actions based. Historical Gitian instructions and the old Linux-to-Darwin cross-build are not the current release procedure.

Prepare the release
-------------------

1. Update the version in `configure.ac` and confirm the generated package version is correct.
2. Add or update `doc/release-notes-X.Y.Z.md` with the user-visible changes, compatibility statement, supported platforms, and dependency baseline.
3. Update the root `README.md` when the new release becomes the maintained public version.
4. Keep dependency changes, build-system changes, and unrelated code changes out of the release-preparation commit unless they are part of the release itself.
5. For a release candidate, use `vX.Y.Z-rcN`. For the stable release, use `vX.Y.Z`.

Validation before tagging
-------------------------

All relevant pull-request checks should be green before the release is tagged. The maintained release set currently validates at least:

- Linux x86_64 build and tests;
- Windows x86_64 MinGW build;
- native macOS Intel x86_64 build;
- native macOS Apple Silicon ARM64 build;
- wallet compatibility and smoke coverage relevant to the changes;
- cross-platform release packaging through `.github/workflows/release-validation-ci.yml`.

The release-validation workflow builds the pinned `depends` stack and checks release artifacts for the expected target format. The macOS jobs additionally verify Mach-O architecture, deployment target, dynamic linkage, app packaging, and DMG contents. Apple Silicon validation also covers the dedicated ARM64 package and the wallet interchange checks defined by the current workflow.

Run release validation on the exact commit that will be tagged. A successful run on an earlier branch head is useful evidence, but it does not replace exact-tag validation when the release source has moved.

Release tags
------------

Release tags must identify the exact validated commit and should be **annotated tags**, not lightweight tags.

The 0.18.x build metadata is derived through the legacy `share/genbuild.sh` path. Its `git describe` behavior recognizes annotated tags by default. A lightweight release-candidate tag can therefore produce binaries whose embedded version falls back to a commit-suffix form instead of the expected `vX.Y.Z-rcN` string.

Create and verify an annotated tag explicitly, for example:

```sh
git tag -a v0.18.5 -m "Garlicoin Core 0.18.5" <validated-commit>
git show --no-patch v0.18.5
git rev-parse 'v0.18.5^{commit}'
```

For an RC, use the corresponding `vX.Y.Z-rcN` tag name. Do not move or recreate a public release tag after artifacts have been distributed. If a tag is wrong, stop publication and resolve the release procedure deliberately rather than silently retargeting it.

Release artifacts
-----------------

The maintained release workflow currently produces:

- Linux x86_64 archive;
- source archive;
- Windows x86_64 ZIP;
- Windows x86_64 NSIS installer;
- macOS Intel x86_64 archive;
- macOS Intel x86_64 DMG;
- macOS Apple Silicon ARM64 archive;
- macOS Apple Silicon ARM64 DMG;
- a combined `SHA256SUMS` manifest for the published files.

Before publishing, verify that every expected file exists, filenames contain the intended release label, and the packaged binaries report the intended version. Do not attach temporary CI logs, dependency caches, or intermediate build products to the public release.

Publish
-------

The maintained publisher is `.github/workflows/tagged-release.yml`. It dispatches exact-tag release validation, waits for that validation to pass, downloads the platform artifacts, assembles the public asset set, verifies the packaged version, generates the combined checksum manifest, and creates or updates the GitHub release.

For a release candidate:

- publish it as a GitHub pre-release;
- keep the stable release designation on the previous stable version;
- use the RC to collect any required real-hardware or community validation before promotion to the final release.

For a stable release:

- publish `vX.Y.Z` only after the final release commit and exact tag have passed the required validation;
- use `Garlicoin Core X.Y.Z - GRLC.eu Maintenance Release` as the maintained release title;
- verify the release page, download links, asset names, checksums, and reported binary versions after publication.

After publication
-----------------

- Confirm the root `README.md` points to the current stable release and correct downloads.
- Keep version-specific release notes in `doc/` as the durable repository record.
- Keep the successful exact-tag validation and publishing runs long enough to provide a clear release audit trail.
- Record any release-specific regression or follow-up work as a separate issue or maintenance change rather than silently altering an already published artifact.
- Regenerate committed command man pages from the release binaries before the final stable release when their embedded version/help text is stale.

Legacy build paths
------------------

The old Gitian release process and Linux-to-Darwin cross-build are not maintained for the current Qt 5.15/OpenSSL 3.5 line. The supported macOS release paths are native Intel x86_64 and native Apple Silicon ARM64 through `.github/workflows/release-validation-ci.yml`.
