#!/usr/bin/env python3
"""Reproducible first-pass PowerPC conditional compilation inventory; not a compile test."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FAMILIES = ('IOGraphics-392.1', 'IOPCIFamily-144', 'IOFireWireFamily-426.4.1', 'IOUSBFamily-424.4.1')
SUFFIXES = {'.c', '.cc', '.cpp', '.cxx', '.h', '.hpp', '.m', '.mm'}
GUARDS = re.compile(r'^\s*#\s*(?:if|elif|ifdef|ifndef)\b.*(?:__ppc__|__POWERPC__|TARGET_CPU_PPC|__i386__|__x86_64__|__BIG_ENDIAN__|__LITTLE_ENDIAN__|__ppc64__)')
PPC = re.compile(r'__ppc__|__POWERPC__|TARGET_CPU_PPC|__ppc64__')
INTEL = re.compile(r'__i386__|__x86_64__')


def scan():
    rows = []
    for family in FAMILIES:
        base = ROOT / 'src/releases/10.6.8' / family
        if not base.is_dir():
            raise ValueError('missing official source tree: ' + family)
        for path in sorted(base.rglob('*')):
            if not path.is_file() or path.suffix.lower() not in SUFFIXES:
                continue
            for line_number, line in enumerate(path.read_text(encoding='utf-8', errors='replace').splitlines(), 1):
                if GUARDS.search(line):
                    rows.append({'family': family, 'file': path.relative_to(ROOT).as_posix(),
                                 'line': line_number, 'directive': line.strip(),
                                 'ppc_mentioned': bool(PPC.search(line)), 'intel_mentioned': bool(INTEL.search(line))})
    return rows


if __name__ == '__main__':
    rows = scan()
    print(json.dumps({'scope': list(FAMILIES), 'classification': 'static_conditional_evidence_only',
                      'guard_count': len(rows), 'guards': rows}, indent=2))
