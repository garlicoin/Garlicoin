Garlicoin Core release process
==============================

This document describes the maintained release process for the Garlicoin Core 0.18.x line in this repository.

Release principles
------------------

Maintenance releases should remain narrowly scoped. They must not intentionally change Garlicoin consensus, proof of work, network identity, address formats, existing blockchain/datadir compatibility, or the Berkeley DB 4.8 wallet format unless such a change is explicitly planned and reviewed as a separate project.

The repository's maintained release path is GitHub Actions based. Historical Gitian instructions and the old Linux-to-Darwin cross-build are not the current release procedure.

Prepare the release
-------------------

1. Set `configure.ac` to the intended base version `X.Y.Z` and keep `_CLIENT_VERSION_BUILD` at `0`. Release-candidate suffixes are supplied by the Git tag rather than by changing the base package version to `-rcN`.
2. Add or update `doc/release-notes-X.Y.Z.md` with the user-visible changes, compatibility statement, supported platforms, dependency baseline, and any release-candidate testing requests.
3. Update the root `README.md` when the new release becomes the maintained public version.
4. Keep dependency changes, build-system changes, and unrelated code changes out of the release-preparation commit unless they are part of the release itself.
5. For a release candidate, the release label is `vX.Y.Z-rcN`. For the stable release, it is `vX.Y.Z`.

Validation before publication
-----------------------------

All relevant pull-request and branch checks should be green before requesting publication. The maintained release set currently validates at least:

- Linux x86_64 build and tests;
- Windows x86_64 MinGW build;
- native macOS Intel x86_64 build;
- native macOS Apple Silicon ARM64 build;
- wallet compatibility and smoke coverage relevant to the changes;
- cross-platform release packaging through `.github/workflows/release-validation-ci.yml`.

The release-validation workflow builds the pinned `depends` stack and checks release artifacts for the expected target format. The macOS jobs additionally verify Mach-O architecture, deployment target, dynamic linkage, app packaging, and DMG contents. Apple Silicon validation also covers the dedicated ARM64 package and the wallet interchange checks defined by the current workflow.

A successful run on the final `master` commit is useful pre-publication evidence, but the publisher always dispatches a fresh validation run for the exact release tag. The exact-tag run is the publication gate.

Request a release
-----------------

The normal release request is a branch creation event.

Create a branch named exactly:

```text
release/vX.Y.Z-rcN
```

for a release candidate, or:

```text
release/vX.Y.Z
```

for a stable release. The branch must point at the exact commit intended for publication.

For example:

```sh
git fetch origin
git branch release/v0.18.5-rc2 <validated-commit>
git push origin release/v0.18.5-rc2
```

Creating that branch triggers `.github/workflows/tagged-release.yml`. The publisher removes the `release/` prefix, validates the version metadata, and then creates or verifies the corresponding `vX.Y.Z[-rcN]` tag on the same commit.

Do not create a separate release tag manually during the normal branch-triggered path. If a tag of the requested name already exists, the publisher requires it to resolve to the exact same commit and fails rather than silently moving it.

Release tags and build metadata
-------------------------------

The normal publisher creates the release tag directly as a Git ref. This is a lightweight tag.

`share/genbuild.sh` uses `git describe --tags --abbrev=0`, so both lightweight and annotated tags are recognized for build metadata. On an exact tagged and clean commit, an RC binary must therefore report the exact `vX.Y.Z-rcN` release label.

Do not move or recreate a public release tag after artifacts have been distributed. If a publication attempt fails before a GitHub Release exists, diagnose the failure first. Any deliberate tag cleanup or recreation should happen before public artifacts are published and should preserve a clear audit trail.

The `workflow_dispatch` entry point in `tagged-release.yml` is intended for an existing release tag. It still runs the same exact-tag validation and publication checks; it is not a bypass around the release gate.

Exact-tag validation and publication
------------------------------------

After the release request is accepted, `.github/workflows/tagged-release.yml`:

1. validates the requested release label and the `configure.ac` base version;
2. creates or verifies the exact release tag on the requested commit;
3. dispatches `.github/workflows/release-validation-ci.yml` using that tag;
4. waits for the exact-tag validation run to succeed;
5. downloads the Linux, Windows, macOS Intel, and macOS ARM64 artifacts;
6. verifies the ARM64 checksums and assembles the public asset names;
7. generates a combined `SHA256SUMS` manifest;
8. extracts the packaged Linux daemon and verifies its reported version against the requested release label;
9. creates or updates the GitHub Release.

For a release candidate, the binary-version check requires an exact match such as:

```text
Garlicoin Core Daemon version v0.18.5-rc2
```

A commit-suffix fallback is not accepted for an RC.

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

Before treating publication as complete, verify that every expected file exists, filenames contain the intended release label, checksums are present, and the packaged binaries report the intended version. Do not attach temporary CI logs, dependency caches, or intermediate build products to the public release.

Release candidates
------------------

For a release candidate:

- publish it as a GitHub pre-release;
- keep the stable release designation on the previous stable version;
- use the RC to collect any required real-hardware or community validation before promotion to the final release.

The published `v0.18.5-rc2` release is an example of the maintained path: the `release/v0.18.5-rc2` request targeted the final source commit, the publisher created/verified the exact tag, exact-tag release validation passed, the packaged RC version was verified, and the pre-release assets were published.

Stable releases
---------------

For a stable release:

- create `release/vX.Y.Z` only after the final release commit is ready;
- allow the publisher to create/verify `vX.Y.Z` and run the same exact-tag validation gate;
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
