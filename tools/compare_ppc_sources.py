#!/usr/bin/env python3
"""Compare checked-in historical source trees without changing either baseline."""
import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT)] + list(args), universal_newlines=True)


def compare(left, right):
    prefix = 'src/releases/'
    for name in (left, right):
        if not name.startswith(prefix) or '..' in Path(name).parts:
            raise ValueError('source outside historical release namespace')
        if not git('ls-tree', 'HEAD', name).strip().startswith('040000 tree '):
            raise ValueError('source tree not committed: ' + name)
    a = git('rev-parse', 'HEAD:' + left).strip()
    b = git('rev-parse', 'HEAD:' + right).strip()
    lines = git('diff', '--no-renames', '--name-status', a, b).splitlines()
    changes = [{'status': line.split('\t', 1)[0], 'path': line.split('\t', 1)[1]} for line in lines]
    return {'left': left, 'right': right, 'left_tree': a, 'right_tree': b,
            'changed_files': len(changes), 'changes': changes,
            'runtime_parity': 'not_assessed', 'reversion_recommendation': 'requires PPC build and runtime evidence'}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('left')
    p.add_argument('right')
    p.add_argument('--output', type=Path)
    a = p.parse_args()
    try:
        result = compare(a.left, a.right)
        content = json.dumps(result, indent=2, sort_keys=True) + '\n'
        if a.output:
            if not str(a.output.resolve()).startswith(str(ROOT) + '/'):
                raise ValueError('output outside repository')
            a.output.write_text(content, encoding='utf-8')
        else:
            sys.stdout.write(content)
    except (ValueError, OSError, subprocess.CalledProcessError) as exc:
        print('comparison rejected: {}'.format(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
