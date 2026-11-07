#!/usr/bin/env python3
"""Validate exact source-release graph and checked-in XNU baseline (stdlib only)."""
import re
import subprocess
import sys
from pathlib import Path

SNOW = "src/apple-darwin-10.6.8/"
LATER = "src/apple-distributions-macos11/"
XNU = "src/xnu-1504.15.3/"
XNU_COMMIT = "99c11f3f90a18f35d3692ea77444b51fd972a4f4"


def run(*args):
    return subprocess.check_output(["git", *args], text=True)


def verify():
    data = Path(".gitmodules").read_text()
    names = re.findall(r'^\[submodule "([^"]+)"\]$', data, re.M)
    paths = re.findall(r"^\s*path\s*=\s*(\S+)", data, re.M)
    entries = run("ls-tree", "-r", "HEAD", SNOW, LATER).splitlines()
    links = [x.split("\t", 1)[1] for x in entries if x.startswith("160000 commit ")]
    assert len(names) == len(set(names)) == len(paths) == len(links) == 582, "submodule count/name mismatch"
    assert set(paths) == set(links), "submodule mapping does not match pinned gitlinks"
    assert sum(x.startswith(SNOW) for x in paths) == 353, "Snow Leopard graph changed"
    assert sum(x.startswith(LATER) for x in paths) == 229, "macOS 11 reference graph changed"
    assert len(run("ls-tree", "-r", "--name-only", "HEAD", XNU).splitlines()) == 3386, "XNU source snapshot incomplete"
    entry = run("ls-tree", "HEAD", SNOW + "xnu").strip()
    assert entry.startswith("160000 commit " + XNU_COMMIT + "\t"), "Snow Leopard XNU pin changed"
    print("PASS: release-specific graphs, 582 gitlinks and exact XNU 1504.15.3 source")


if __name__ == "__main__":
    try:
        verify()
    except (AssertionError, OSError, subprocess.CalledProcessError) as exc:
        print(f"source graph invalid: {exc}", file=sys.stderr)
        sys.exit(1)
