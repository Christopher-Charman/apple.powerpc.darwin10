#!/usr/bin/env python3
"""Verify pinned historical Apple OSS gitlinks and their .gitmodules paths.

Does not download source, guess release membership or mutate the checkout.
"""
import configparser
import json
import subprocess
import sys
from pathlib import Path


def verify(root):
    manifest = json.loads((root / 'historical' / 'SOURCE_LOCK.json').read_text())
    config = configparser.ConfigParser()
    config.read(str(root / '.gitmodules'))
    links = subprocess.check_output(['git', '-C', str(root), 'ls-tree', '-r', 'HEAD', 'historical'], universal_newlines=True)
    actual = {}
    for line in links.splitlines():
        meta, path = line.split('\t', 1)
        mode, kind, sha = meta.split()
        if mode == '160000' and kind == 'commit':
            actual[path] = sha
    expected = {}
    for item in manifest['sources']:
        path = item['path']
        if path in expected:
            raise ValueError('duplicate source path: ' + path)
        if item['release_family'] not in ('10.5', '10.6') or not path.startswith('historical/' + item['release_family'] + '/'):
            raise ValueError('release path mismatch: ' + path)
        if not (len(item['commit']) == 40 and all(c in '0123456789abcdef' for c in item['commit'])):
            raise ValueError('invalid commit: ' + path)
        section = 'submodule "{}"'.format(path)
        if not config.has_section(section) or config.get(section, 'path') != path or config.get(section, 'url') != item['url']:
            raise ValueError('submodule mapping mismatch: ' + path)
        expected[path] = item['commit']
    if expected != actual:
        raise ValueError('gitlink lock mismatch: missing={}, unexpected={}, differing={}'.format(sorted(set(expected)-set(actual)), sorted(set(actual)-set(expected)), sorted(p for p in set(expected)&set(actual) if expected[p] != actual[p])))
    return len(expected)


if __name__ == '__main__':
    try:
        print('Verified {} pinned historical source trees'.format(verify(Path(__file__).resolve().parents[1])))
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        print('Historical source lock invalid: {}'.format(exc), file=sys.stderr)
        sys.exit(1)
