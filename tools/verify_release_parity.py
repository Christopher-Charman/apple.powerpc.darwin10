#!/usr/bin/env python3
"""Check official 10.5/10.6 release manifests against local historical source trees."""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSIONS = ('10.5.1',) + tuple('10.6.' + str(i) for i in range(1, 9)) + ('10.6',)


def run(*args):
    return subprocess.check_output(['git', '-C', str(ROOT)] + list(args), universal_newlines=True)


def verify():
    releases = {}
    for version in VERSIONS:
        obj = json.loads((ROOT / 'source-releases' / (version + '.json')).read_text(encoding='utf-8'))
        if obj.get('release') != 'Mac OS X ' + version:
            raise ValueError('release identity mismatch: ' + version)
        projects = obj.get('projects', [])
        if not projects or any(not isinstance(p.get('project'), str) or not isinstance(p.get('tag'), str) for p in projects):
            raise ValueError('invalid project membership: ' + version)
        if len({p['project'] for p in projects}) != len(projects):
            raise ValueError('duplicate project: ' + version)
        releases[version] = {p['project']: p['tag'] for p in projects}
    for version, name in (('10.5.1', 'xnu'), ('10.6.8', 'xnu')):
        if name not in releases[version]:
            raise ValueError('missing xnu in ' + version)
    for version, names in (('10.5.1', ('xnu', 'Libc')), ('10.6.8', ('xnu', 'Libc'))):
        if any(n not in releases[version] for n in names):
            raise ValueError('missing core component: ' + version)
    lock = json.loads((ROOT / 'historical/SOURCE_LOCK.json').read_text(encoding='utf-8'))
    for item in lock['sources']:
        component, tag = item['component'], item['tag']
        family = item['release_family']
        matching = [version for version, projects in releases.items() if version.startswith(family) and projects.get(component) == tag]
        if not matching:
            print('CANDIDATE_NOT_RELEASE_MATCHED: {} {} {}'.format(family, component, tag))
    print('PASS: {} first-party release manifests, {} unique source-family entries'.format(len(releases), len(set().union(*(set(v) for v in releases.values())))))
    for name in ('xnu', 'Libc', 'cups', 'libxml2', 'cctools', 'ld64', 'dyld', 'launchd', 'Libsystem'):
        values = [(v, releases[v].get(name, 'not published')) for v in VERSIONS]
        print(name + ': ' + ', '.join('{}={}'.format(v, tag) for v, tag in values))


if __name__ == '__main__':
    try:
        verify()
    except (ValueError, OSError, subprocess.CalledProcessError) as exc:
        print('release parity rejected: ' + str(exc), file=sys.stderr)
        sys.exit(1)
