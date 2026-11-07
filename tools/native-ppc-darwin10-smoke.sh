#!/bin/sh
# Native Darwin 10 PowerPC ABI acceptance. Run on an owned PowerPC Mac.
set -eu
[ "$(uname -s)" = Darwin ] || { echo "Darwin required" >&2; exit 1; }
[ "${OSTYPE:-}" = "" ] || :
case "$(uname -r)" in 10.*) ;; *) echo "Darwin 10 required" >&2; exit 1;; esac
case "$(uname -p)" in powerpc|powerpc64) ;; *) echo "PowerPC required" >&2; exit 1;; esac
: "${SLPPC_WORKDIR:=$HOME/slppc-native-qualification}"
mkdir -p "$SLPPC_WORKDIR"
[ -d "$SLPPC_WORKDIR" ] || exit 1
printf '%s\n' 'int main(void) { return 0; }' > "$SLPPC_WORKDIR/main.c"
gcc -arch ppc -mmacosx-version-min=10.6 -o "$SLPPC_WORKDIR/smoke" "$SLPPC_WORKDIR/main.c"
file "$SLPPC_WORKDIR/smoke" | grep -E 'Mach-O.*(ppc|PowerPC)'
lipo -info "$SLPPC_WORKDIR/smoke" | grep -E '(ppc|PowerPC)'
otool -hv "$SLPPC_WORKDIR/smoke"
"$SLPPC_WORKDIR/smoke"
printf '%s\n' 'NATIVE_PPC_DARWIN10_ABI_SMOKE_PASS'
