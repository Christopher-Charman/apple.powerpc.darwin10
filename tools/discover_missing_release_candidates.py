#!/usr/bin/env python3
"""Find historical Apple OSS donor candidates absent from the 10.6.8 release.

This is a candidate discovery tool, NOT a transitive dependency resolver.
Only a verified producer/consumer edge can promote a candidate to a requirement.
"""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RELEASES = ROOT / "source-releases"


def projects(release):
    data = json.loads((RELEASES / (release + ".json")).read_text())
    return {entry["project"]: entry["tag"] for entry in data["projects"]}


def discover():
    target = projects("10.6.8")
    donors = {}
    for path in sorted(RELEASES.glob("10.5.*.json")) + sorted(RELEASES.glob("10.6.*.json")):
        release = path.stem
        if release == "10.6.8":
            continue
        for name, tag in projects(release).items():
            if name not in target:
                donors.setdefault(name, []).append({"release": release, "tag": tag})
    return {
        "target": "Mac OS X 10.6.8",
        "target_project_count": len(target),
        "classification": "historical_source_candidates_not_verified_dependencies",
        "candidates": [
            {"project": name, "historical_sources": versions,
             "dependency_verified": False, "ppc_patch_verified": False}
            for name, versions in sorted(donors.items())
        ],
        "excluded_from_scope": [
            "separately published Developer Tools sources not in these manifests",
            "DarwinBuild Roots, patches and generated/private headers",
            "unpublished or proprietary components",
            "transitive build and runtime dependency resolution"
        ]
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Write deterministic JSON")
    args = parser.parse_args()
    report = json.dumps(discover(), indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(report)
    else:
        print(report, end="")


if __name__ == "__main__":
    main()
