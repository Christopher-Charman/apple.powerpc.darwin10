#!/usr/bin/env python3
"""Verify recovered binary bytes against an explicit historical artifact manifest."""
import argparse
import json
import re
import sys
from pathlib import Path
from inspect_ppc_macho import inspect


def verify(manifest, root):
    data = json.loads(Path(manifest).read_text(encoding='utf-8'))
    if not isinstance(data.get('artifacts'), list) or not data['artifacts']:
        raise ValueError('manifest requires artifacts')
    if not re.fullmatch(r'[0-9a-f]{64}', data.get('archive_sha256', '')):
        raise ValueError('archive SHA-256 required')
    root = Path(root).resolve()
    seen = set()
    results = []
    for item in data['artifacts']:
        name = item['path']
        if not isinstance(name, str) or not name or name in seen or name.startswith('/') or '..' in Path(name).parts:
            raise ValueError('invalid or duplicate artifact path')
        seen.add(name)
        expected = item['sha256']
        if not re.fullmatch(r'[0-9a-f]{64}', expected):
            raise ValueError('invalid artifact SHA-256')
        path = (root / name).resolve()
        if not str(path).startswith(str(root) + '/') or not path.is_file():
            raise ValueError('artifact missing or outside root: ' + name)
        result = inspect(path)
        if result['sha256'] != expected:
            raise ValueError('artifact byte mismatch: ' + name)
        if item.get('requires_ppc', True) and not result['contains_ppc']:
            raise ValueError('PowerPC slice absent: ' + name)
        results.append({'path': name, 'sha256': expected, 'architectures': [s['cpu'] for s in result['architectures']]})
    return {'archive_sha256': data['archive_sha256'], 'verified': results,
            'image_runtime_parity': 'not_assessed'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest')
    parser.add_argument('extracted_root')
    args = parser.parse_args()
    try:
        print(json.dumps(verify(args.manifest, args.extracted_root), indent=2, sort_keys=True))
    except (ValueError, KeyError, TypeError, OSError) as exc:
        print('artifact verification rejected: ' + str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
