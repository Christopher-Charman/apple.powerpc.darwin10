#!/usr/bin/env python3
"""Check original darwinbuild build indexes and keep architecture defaults explicit."""
import json
import plistlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLISTS = ROOT / 'tooling/darwinbuild/plists'
BUILDS = ('10A432', '10B504', '10C540', '10D573', '10F569', '10H574', '10J567', '10J869', '10K540')


def inspect():
    result = []
    for build in BUILDS:
        path = PLISTS / (build + '.plist')
        source = path.read_text(encoding='utf-8')
        xml = source.lstrip().startswith('<?xml')
        parsed = plistlib.loads(source.encode('utf-8')) if xml else None
        identity = str(parsed.get('build')) if xml else None
        if (identity != build if xml else not re.search(r'\bbuild\s*=\s*' + build + r'\s*;', source)):
            raise ValueError('build index identity mismatch: ' + build)
        inheritance = re.search(r'\binherits\s*=\s*([A-Za-z0-9]+)\s*;', source)
        architectures = re.search(r'\bRC_ARCHS\s*=\s*"([^"]+)"\s*;', source)
        result.append({'build': build, 'inherits': str(parsed['inherits']) if xml and 'inherits' in parsed else (inheritance.group(1) if inheritance else None),
                       'default_architectures': parsed.get('environment', {}).get('RC_ARCHS', '').split() if xml and 'RC_ARCHS' in parsed.get('environment', {}) else (architectures.group(1).split() if architectures else None),
                       'index': 'tooling/darwinbuild/plists/' + build + '.plist'})
    for entry in result:
        if entry['inherits'] and entry['inherits'] not in BUILDS:
            raise ValueError('unresolved build index inheritance: ' + entry['build'])
    return result


if __name__ == '__main__':
    print(json.dumps({'builds': inspect(), 'powerpc_override_required': True,
                      'runtime_build_acceptance': 'not_assessed'}, indent=2))
