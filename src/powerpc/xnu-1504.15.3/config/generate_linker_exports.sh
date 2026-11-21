#!/bin/sh

set -e

if [ "$#" -lt 2 ]; then
    echo "Usage: $0 output.exp input1 [input2 ... ]" >&2
    exit 1
fi

OUTPUT="$1"
shift

# Fail before writing if any architecture-specific export input is missing.
# A missing PPC export list must not silently produce a truncated kernel ABI.
for input in "$@"; do
    if [ ! -f "$input" ]; then
        echo "Missing kernel export input: $input" >&2
        exit 1
    fi
done

# Preserve the original two-pass symbol normalization and unique sorting.
# grep returns 1 when a pass has no matches; this is not an error.
( grep -h -v ":" "$@" || [ "$?" -eq 1 ]; grep -h ":" "$@" | awk -F: '{print $2}' ) | sort -u > "$OUTPUT"

exit 0
