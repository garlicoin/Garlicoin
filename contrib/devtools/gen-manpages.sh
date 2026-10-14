#!/bin/bash

set -euo pipefail

TOPDIR=${TOPDIR:-$(git rev-parse --show-toplevel)}
SRCDIR=${SRCDIR:-$TOPDIR/src}
MANDIR=${MANDIR:-$TOPDIR/doc/man}

GARLICOIND=${GARLICOIND:-$SRCDIR/garlicoind}
GARLICOINCLI=${GARLICOINCLI:-$SRCDIR/garlicoin-cli}
GARLICOINTX=${GARLICOINTX:-$SRCDIR/garlicoin-tx}
GARLICOINQT=${GARLICOINQT:-$SRCDIR/qt/garlicoin-qt}

for cmd in "$GARLICOIND" "$GARLICOINCLI" "$GARLICOINTX" "$GARLICOINQT"; do
  if [ ! -x "$cmd" ]; then
    echo "$cmd not found or not executable." >&2
    exit 1
  fi
done

if ! command -v help2man >/dev/null 2>&1; then
  echo "help2man is required to regenerate command man pages." >&2
  exit 1
fi

VERSION="$($GARLICOINCLI --version | head -n1 | sed -n 's/^.* version //p')"
if [ -z "$VERSION" ]; then
  echo "Could not determine Garlicoin Core version from $GARLICOINCLI." >&2
  exit 1
fi

mkdir -p "$MANDIR"
FOOTER="$(mktemp)"
trap 'rm -f "$FOOTER"' EXIT

{
  echo "[COPYRIGHT]"
  "$GARLICOIND" --version | sed -n '1!p'
} > "$FOOTER"

for cmd in "$GARLICOIND" "$GARLICOINCLI" "$GARLICOINTX" "$GARLICOINQT"; do
  cmdname="${cmd##*/}"
  outfile="$MANDIR/${cmdname}.1"

  help2man -N \
    --version-string="$VERSION" \
    --include="$FOOTER" \
    -o "$outfile" \
    "$cmd"

  if ! grep -Fq "$VERSION" "$outfile"; then
    echo "$outfile does not contain expected version $VERSION." >&2
    exit 1
  fi

  if [ "$(wc -l < "$outfile")" -lt 25 ]; then
    echo "$outfile is unexpectedly short; command help likely failed." >&2
    exit 1
  fi

  if grep -Eqi 'error while loading shared libraries|could not find the qt platform plugin|no qt platform plugin could be initialized|failed to start' "$outfile"; then
    echo "$outfile contains a runtime error instead of command help." >&2
    exit 1
  fi
done
