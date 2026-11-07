#!/usr/bin/env python3
"""Compare PowerPC preprocessor guards between official release source trees."""
import argparse
import json
import re
from pathlib import Path

GUARD = re.compile(r'^\s*#\s*(?:if|ifdef|ifndef|elif)\b.*(?:__ppc__|__POWERPC__|TARGET_CPU_PPC|__ppc64__)')
SUFFIXES = {'.c', '.cc', '.cpp', '.cxx', '.h', '.hpp', '.m', '.mm', '.s', '.S'}


def inventory(root):
    result = {}
    for path in sorted(root.rglob('*')):
        if not path.is_file() or path.suffix not in SUFFIXES:
            continue
        directives = []
        for line in path.read_text(encoding='utf-8', errors='replace').splitlines():
            if GUARD.search(line):
                directives.append(line.strip())
        if directives:
            result[path.relative_to(root).as_posix()] = directives
    return result


def compare(old_root, new_root):
    old, new = inventory(old_root), inventory(new_root)
    changes = []
    for path in sorted(old):
        previous, current = old[path], new.get(path, [])
        remaining = list(current)
        removed = []
        for directive in previous:
            if directive in remaining:
                remaining.remove(directive)
            else:
                removed.append(directive)
        if removed:
            changes.append({'path': path, 'old_count': len(previous),
                            'new_count': len(current), 'removed_guards': removed,
                            'file_missing': not (new_root / path).is_file()})
    return {'classification': 'static_evidence_not_automatic_patch',
            'old_tree': str(old_root), 'new_tree': str(new_root),
            'affected_files': len(changes), 'changes': changes}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('old_tree', type=Path)
    parser.add_argument('new_tree', type=Path)
    args = parser.parse_args()
    if not args.old_tree.is_dir() or not args.new_tree.is_dir():
        parser.error('both source trees must exist')
    print(json.dumps(compare(args.old_tree, args.new_tree), indent=2))


if __name__ == '__main__':
    main()
