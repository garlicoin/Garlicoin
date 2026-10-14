Garlicoin Core documentation
============================

This directory contains documentation relevant to the maintained Garlicoin Core 0.18.x line.

The repository source, `depends` recipes, chain parameters, and GitHub Actions workflows are the source of truth when a document and the implementation disagree. The currently validated release platforms are Linux x86_64, Windows x86_64 (MinGW), native macOS Intel x86_64, and native macOS Apple Silicon ARM64.

The latest published pre-release is Garlicoin Core 0.18.5-rc2. The current stable release remains 0.18.4 until 0.18.5 is promoted after release-candidate validation.

Building
--------

- [Dependencies](dependencies.md)
- [Unix build notes](build-unix.md)
- [Ubuntu toolchain validation](ubuntu-toolchain.md)
- [Windows x86_64 build notes](build-windows.md)
- [macOS Intel and Apple Silicon build notes](build-osx.md)

Development
-----------

- [Developer notes](developer-notes.md)
- [Release process](release-process.md)
- [Unauthenticated REST interface](REST-interface.md)
- [Shared libraries](shared-libraries.md)
- [DNS seed policy](dnsseed-policy.md)
- [Benchmarking](benchmarking.md)
- [Fuzz testing](fuzzing.md)
- [Translation strings policy](translation_strings_policy.md)

Operation and integration
-------------------------

- [Data files](files.md)
- [Reduce traffic](reduce-traffic.md)
- [Tor support](tor.md)
- [ZMQ](zmq.md)

Release notes
-------------

- [Garlicoin Core 0.18.5 / 0.18.5-rc2](release-notes-0.18.5.md)
- [Garlicoin Core 0.18.4](release-notes-0.18.4.md)
- [Garlicoin Core 0.18.3](release-notes-0.18.3.md)
- [Garlicoin Core 0.18.2](release-notes-0.18.2.md)

Version-specific release notes are kept as the durable repository record. Older inherited Bitcoin and Litecoin release-note archives and unverified upstream protocol matrices are intentionally not duplicated here; they remain available through Git history and the respective upstream projects.

Project information
-------------------

The [root README](../README.md) describes the maintained fork, current stable release, supported artifacts, and CI status.

- [Contributing](../CONTRIBUTING.md)
- [Asset attribution](assets-attribution.md)
- [MIT license](../COPYING)
