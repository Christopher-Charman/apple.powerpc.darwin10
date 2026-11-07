#!/usr/bin/env python3
"""Hash a local engineering input without modifying it or asserting its provenance.

Usage: python3 tools/hash_input.py /path/to/image-or-build-artifact
Prints JSON suitable for copying into an experiment receipt after review.
Files only: directories require an explicit, separately versioned manifest.
"""
import hashlib
import json
import os
import stat
import sys
from pathlib import Path


def hash_file(path):
    # Refuse symlinks, special files, and directories; no implicit traversal.
    info = path.lstat()
    if not stat.S_ISREG(info.st_mode):
        raise ValueError("input must be a regular file (not a symlink or directory)")
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        opened = os.fstat(stream.fileno())
        if not stat.S_ISREG(opened.st_mode) or (opened.st_dev, opened.st_ino) != (info.st_dev, info.st_ino):
            raise ValueError("input changed between inspection and open")
        while chunk := stream.read(1024 * 1024):
            digest.update(chunk)
        after = os.fstat(stream.fileno())
    if (opened.st_size, opened.st_mtime_ns, opened.st_ctime_ns) != (after.st_size, after.st_mtime_ns, after.st_ctime_ns):
        raise ValueError("input changed during hashing")
    return {"identifier": str(path), "sha256": digest.hexdigest(), "bytes": after.st_size}


def main(argv):
    if len(argv) != 2:
        print("usage: hash_input.py FILE", file=sys.stderr)
        return 2
    try:
        result = hash_file(Path(argv[1]))
    except (OSError, ValueError) as exc:
        print(f"cannot hash input: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
