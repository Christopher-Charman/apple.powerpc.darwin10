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
# Generate alongside the destination and rename only after successful
# completion, so interrupted/failed generation cannot truncate the last
# valid kernel export list. A same-directory temporary file keeps the rename
# on the destination filesystem.
output_dir=$(dirname "$OUTPUT")
output_name=$(basename "$OUTPUT")
temporary=$(mktemp "${output_dir}/.${output_name}.XXXXXX") || exit 1
trap 'rm -f "$temporary"' EXIT HUP INT TERM

# Preserve the original export normalization. A grep pass with no matches is
# valid; actual input errors still cause failure.
( grep -h -v ":" "$@" || [ "$?" -eq 1 ]; grep -h ":" "$@" | awk -F: '{print $2}' ) | sort -u > "$temporary" || exit 1
mv -f "$temporary" "$OUTPUT" || exit 1
trap - EXIT HUP INT TERM

exit 0
