#!/usr/bin/env python3
"""Read-only release-bound patch gate; applying/reverting requires a reviewed Git commit."""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RELEASE = re.compile(r'^src/releases/10\.(?:5|6)(?:\.8)?/[A-Za-z0-9_.-]+/.+')
DENIED = ('src/apple-distributions-macos11/', 'src/xnu/', 'toolchains/darwin-xtools/')


def git(*args, **kw):
    return subprocess.run(['git', '-C', str(ROOT)] + list(args), stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, universal_newlines=True, **kw)


def inspect(manifest):
    data = json.loads(manifest.read_text(encoding='utf-8'))
    for key in ('target', 'source_tree', 'source_tree_sha', 'patch', 'rationale', 'reviewer'):
        if not isinstance(data.get(key), str) or not data[key].strip():
            raise ValueError('missing/invalid field: ' + key)
    target = data['source_tree'].rstrip('/')
    if not re.match(r'^src/releases/10\.(?:5|6)(?:\.8)?/[A-Za-z0-9_.-]+$', target):
        raise ValueError('source tree outside Darwin 9/10 release namespace')
    family = target.split('/')[2]
    if data['target'] != family and not (family == '10.6.8' and data['target'].startswith('10.6.8')):
        raise ValueError('target and source release mismatch')
    component_tag = target.rsplit('/', 1)[-1]
    if '-' not in component_tag:
        raise ValueError('source tree missing component tag')
    component = component_tag.split('-', 1)[0]
    release = data['target']
    release_file = ROOT / 'source-releases' / (release + '.json')
    if release_file.is_file():
        projects = json.loads(release_file.read_text(encoding='utf-8')).get('projects', [])
        published = {p['project']: p['tag'] for p in projects}
        if component in published and published[component] != component_tag and not data.get('historical_override'):
            raise ValueError('source tag not in official release; explicit historical_override required')
    if not re.fullmatch(r'[0-9a-f]{40}', data['source_tree_sha']):
        raise ValueError('invalid pinned source tree SHA')
    current = git('rev-parse', 'HEAD:' + target)
    if current.returncode or current.stdout.strip() != data['source_tree_sha']:
        raise ValueError('source tree identity changed; rebase and re-review')
    patch_path = (ROOT / data['patch']).resolve()
    if not str(patch_path).startswith(str(ROOT) + '/'):
        raise ValueError('patch outside repository')
    if not patch_path.is_file() or patch_path.is_symlink() or patch_path.suffix != '.patch':
        raise ValueError('patch must be a regular .patch file')
    if not str(patch_path.relative_to(ROOT)).startswith('patches/'):
        raise ValueError('patch outside patches namespace')
    paths = git('apply', '--numstat', '--', str(patch_path))
    if paths.returncode:
        raise ValueError('malformed patch: ' + paths.stderr.strip())
    touched = []
    for row in paths.stdout.splitlines():
        parts = row.split('\t', 2)
        if len(parts) != 3 or not parts[2].startswith(target + '/') or not RELEASE.fullmatch(parts[2]):
            raise ValueError('patch touches unexpected path: ' + row)
        if any(parts[2].startswith(p) for p in DENIED):
            raise ValueError('post-10.7 source patch rejected')
        touched.append(parts[2])
    if not touched:
        raise ValueError('empty patch')
    forward = git('apply', '--check', '--', str(patch_path))
    reverse = git('apply', '--reverse', '--check', '--', str(patch_path))
    if forward.returncode and reverse.returncode:
        raise ValueError('patch neither applies nor reverses cleanly')
    return {'source_tree': target, 'files': touched, 'state': 'ready_to_apply' if forward.returncode == 0 else 'ready_to_reverse',
            'reviewer': data['reviewer'], 'source_tree_sha': data['source_tree_sha']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest', type=Path)
    args = parser.parse_args()
    try:
        print(json.dumps(inspect(args.manifest.resolve()), sort_keys=True))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print('patch gate rejected: ' + str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
