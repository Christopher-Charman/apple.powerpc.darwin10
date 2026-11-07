#!/bin/sh
# Native Darwin 10 PowerPC ABI acceptance. Run on an owned PowerPC Mac.
set -eu
[ "$(uname -s)" = Darwin ] || { echo "Darwin required" >&2; exit 1; }
case "$(uname -r)" in 10.*) ;; *) echo "Darwin 10 required" >&2; exit 1;; esac
case "$(uname -p)" in powerpc|powerpc64) ;; *) echo "PowerPC required" >&2; exit 1;; esac
: "${SLPPC_WORKDIR:=$HOME/slppc-native-qualification}"
mkdir -p "$SLPPC_WORKDIR"
[ -d "$SLPPC_WORKDIR" ] && [ ! -L "$SLPPC_WORKDIR" ] || exit 1
run_dir="$(mktemp -d "$SLPPC_WORKDIR/run.XXXXXXXX")"
trap 'rm -rf "$run_dir"' EXIT HUP INT TERM
printf '%s\n' 'int main(void) { return 0; }' > "$run_dir/main.c"
gcc -arch ppc -mmacosx-version-min=10.6 -o "$run_dir/smoke" "$run_dir/main.c"
file "$run_dir/smoke" | grep -E 'Mach-O.*(ppc|PowerPC)'
lipo -info "$run_dir/smoke" | grep -E '(ppc|PowerPC)'
otool -hv "$run_dir/smoke"
"$run_dir/smoke"
printf '%s\n' 'NATIVE_PPC_DARWIN10_ABI_SMOKE_PASS'
