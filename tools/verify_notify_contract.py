#!/usr/bin/env python3
"""Enforce known notifyd/Libnotify source and MIG pairings before PPC builds."""
from pathlib import Path
import sys
import re

ROOT = Path(__file__).resolve().parents[1]
PAIRS = (
    ('10.6', 'notify-23', 'Libnotify-53', '_notify_lib_notify_state_new(0);',
     '_notify_lib_notify_state_new(uint32_t flags);'),
    ('10.6.8', 'notify-25.1', 'Libnotify-54.3', '_notify_lib_notify_state_new(0, 1024);',
     '_notify_lib_notify_state_new(uint32_t flags, uint32_t table_size);'),
)


def check():
    for release, daemon, library, call, declaration in PAIRS:
        d = ROOT / 'src/releases' / release / daemon / 'notifyd.tproj'
        lib = ROOT / 'src/releases' / release / library
        assert call in (d / 'daemon.c').read_text(encoding='utf-8'), 'daemon API mismatch: ' + daemon
        assert declaration in (lib / 'libnotify.h').read_text(encoding='utf-8'), 'library API mismatch: ' + library
        assert (lib / 'notify_ipc.defs').is_file(), 'missing MIG source: ' + library
        impl = (lib / 'libnotify.c').read_text(encoding='utf-8')
        assert re.search(r'_notify_lib_notify_state_new\s*\(\s*uint32_t flags\s*' +
                         (r',\s*uint32_t table_size\s*' if release == '10.6.8' else '') +
                         r'\)', impl), 'implementation signature mismatch: ' + library
        if release == '10.6.8':
            assert '$(SDKROOT)/usr/local/include/notify_ipc.defs' in (d / 'Makefile').read_text(encoding='utf-8')
            assert 'notify_ipc.defs in Headers' in (lib / 'Libnotify.xcodeproj/project.pbxproj').read_text(encoding='utf-8')
        print('PASS: {} {} + {} source API/MIG pairing'.format(release, daemon, library))


if __name__ == '__main__':
    try:
        check()
    except (AssertionError, OSError) as exc:
        print('notify contract rejected: {}'.format(exc), file=sys.stderr)
        sys.exit(1)
