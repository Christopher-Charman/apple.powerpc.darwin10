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

# Keep normalization and sorting in separate checked stages. The original
# grep/awk/sort pipeline masked read errors because only sort's status was
# visible; an unreadable PPC export could otherwise yield a partial ABI list.
# For colon records, preserve the original second-field extraction.
normalized="${temporary}.normalized"
trap 'rm -f "$temporary" "$normalized"' EXIT HUP INT TERM
awk -F: '{ if (index($0, ":")) print $2; else print $0 }' "$@" > "$normalized" || exit 1
sort -u "$normalized" > "$temporary" || exit 1
rm -f "$normalized" || exit 1
mv -f "$temporary" "$OUTPUT" || exit 1
trap - EXIT HUP INT TERM

exit 0
