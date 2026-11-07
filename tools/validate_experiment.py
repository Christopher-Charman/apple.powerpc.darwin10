#!/usr/bin/env python3
"""Validate reproducible PowerPC Darwin experiment receipts (stdlib only).

Usage: python3 tools/validate_experiment.py path/to/run.json
No filesystem writes, network access, or inferred build identity.
"""
import json
import re
import sys
from pathlib import Path

SHA256 = re.compile(r"^[0-9a-f]{64}$")
VERDICTS = {"planned", "passed", "failed", "falsified", "null", "inconclusive"}
FIELDS = ("run_id", "target", "hypothesis", "prediction", "falsifier",
          "procedure", "source", "toolchain", "hardware", "image", "results")
IDENTITY = ("identifier", "sha256")
HARDWARE = ("model", "boot_rom", "cpu", "ram_bytes")
RESULTS = ("verdict", "observations", "artifacts")

def validate(data):
    errors = []
    if not isinstance(data, dict):
        return ["root must be an object"]
    for key in FIELDS:
        if key not in data:
            errors.append(f"missing {key}")
    for key in ("run_id", "target", "hypothesis", "prediction", "falsifier", "procedure"):
        if key in data and (not isinstance(data[key], str) or not data[key].strip()):
            errors.append(f"{key} must be a nonempty string")
    for key in ("source", "toolchain", "image"):
        value = data.get(key)
        if not isinstance(value, dict):
            errors.append(f"{key} must be an object")
            continue
        for field in IDENTITY:
            item = value.get(field)
            if not isinstance(item, str) or not item.strip():
                errors.append(f"{key}.{field} must be a nonempty string")
            elif field == "sha256" and not SHA256.fullmatch(item):
                errors.append(f"{key}.{field} must be a lowercase SHA-256 digest")
    hardware = data.get("hardware")
    if not isinstance(hardware, dict):
        errors.append("hardware must be an object")
    else:
        for field in HARDWARE:
            value = hardware.get(field)
            if field == "ram_bytes":
                if type(value) is not int or value <= 0:
                    errors.append("hardware.ram_bytes must be a positive integer")
            elif not isinstance(value, str) or not value.strip():
                errors.append(f"hardware.{field} must be a nonempty string")
    results = data.get("results")
    if not isinstance(results, dict):
        errors.append("results must be an object")
    else:
        verdict = results.get("verdict")
        if verdict not in VERDICTS:
            errors.append("results.verdict must be one of " + ", ".join(sorted(VERDICTS)))
        observations = results.get("observations")
        artifacts = results.get("artifacts")
        if not isinstance(observations, list) or any(not isinstance(x, str) or not x.strip() for x in observations):
            errors.append("results.observations must be a list of nonempty strings")
        if not isinstance(artifacts, list):
            errors.append("results.artifacts must be a list")
        else:
            for i, artifact in enumerate(artifacts):
                if not isinstance(artifact, dict) or not isinstance(artifact.get("path"), str) or not artifact["path"].strip() or not isinstance(artifact.get("sha256"), str) or not SHA256.fullmatch(artifact["sha256"]):
                    errors.append(f"results.artifacts[{i}] requires path and lowercase sha256")
        if verdict != "planned" and not observations:
            errors.append("terminal verdict requires at least one observation")
    if data.get("evidence_class") not in {"historical", "source_tested", "live_verified"}:
        errors.append("evidence_class must be historical, source_tested or live_verified")
    if data.get("evidence_class") == "live_verified" and data.get("results", {}).get("verdict") == "planned":
        errors.append("planned experiment cannot be live_verified")
    return errors

def main(argv):
    if len(argv) != 2:
        print("usage: validate_experiment.py RUN.json", file=sys.stderr)
        return 2
    try:
        data = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print(f"invalid input: {exc}", file=sys.stderr)
        return 2
    errors = validate(data)
    for error in errors:
        print(error, file=sys.stderr)
    if errors:
        return 1
    print("VALID experiment receipt")
    return 0

if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
