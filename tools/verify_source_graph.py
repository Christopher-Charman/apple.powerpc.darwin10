#!/usr/bin/env python3
"""Check Darwin 9/10 source graph and reject unqualified modern source trees."""
import configparser
import subprocess
import sys
from pathlib import Path

SNOW = 'src/apple-darwin-10.6.8/'
EXPECTED = {
    'src/releases/10.5/xnu-1228.15.4': ('9d80f9528906753d682f9d65d56a0276bad56b4d', 3156),
    'src/releases/10.6/xnu-1456.1.26': ('46708ce5a6d4a42164ddb67a90fa6fbc7f986430', 3379),
    'src/releases/10.6.8/xnu-1504.15.3': ('0ffff24afe52ed47d20c5a06f07a10200f89f32b', 3386),
    'src/releases/10.6/cups-218': ('9938def0573b75abc0d2394b8a5e9ad66eca6609', 1336),
    'src/releases/10.6/libxml2-21': ('fc7b70e014720bcd2841ea820dcd796857f73380', 3786),
    'src/releases/10.6.8/cctools-750': ('fd5088e19976086ee468e14f7ac9d99aea9feb67', 434),
    'src/releases/10.6.8/ld64-95.2.12': ('6eddbd84730dc25fb0e273d21dc60b484cb2a6a1', 757),
    'src/releases/10.6.8/Libc-594.9.5': ('c577656a4766b334a0c8e0d6bc8dbd68c2bb4ae0', 2737),
    'src/releases/10.6.2/xnu-1486.2.11': ('1b4d746adf265f0459a9a3a87dcb9d483f085208', 3379),
    'src/releases/10.6.3/xnu-1504.3.12': ('c1c00d94faad04b56ded4d40e21a1724898c3e13', 3386),
    'src/releases/10.5.8/notify-16': ('bdf9bfe291059e6e8d3958b653e88d9da8728407', 24),
    'src/releases/10.6/notify-23': ('38946c7473e54cd68bbe85d8b6c907f835ba9d2c', 22),
    'src/releases/10.6.8/notify-25.1': ('11e89af8448d664497294015b8f128878b16b4de', 21),
    'src/releases/10.6/Libnotify-53': ('f403157be8da7e5a737a0d218f02683731737800', 22),
    'src/releases/10.6.8/Libnotify-54.3': ('7e626c25a337eeebdddd3a2f6640354f304b5cb6', 23),
    'src/releases/10.6/Libc-583': ('75515abbc4ece291741c3d9129eceef5a85e913e', 2732),
    'src/releases/10.6/kext_tools-177': ('0de81839fd993341ff03e412969f47ff72fa9936', 76),
    'src/releases/10.6.8/kext_tools-180.2.1': ('191e8d87a847864dde821469ffd23b10315e31c2', 77),
    'src/releases/10.6/DirectoryService-621': ('bd53241aacad6a7e39e953a02f8663508bab9ce5', 391),
    'historical-vendored/xnu-1228.15.4': ('9d80f9528906753d682f9d65d56a0276bad56b4d', 3156),
    'historical-vendored/xnu-1456.1.26': ('46708ce5a6d4a42164ddb67a90fa6fbc7f986430', 3379),
    'historical-vendored/xnu-1504.15.3': ('0ffff24afe52ed47d20c5a06f07a10200f89f32b', 3386),
}
EXCLUDED = ('src/xnu/', 'src/apple-distributions-macos11/')


def run(*args):
    return subprocess.check_output(['git', *args], universal_newlines=True)


def verify():
    cfg = configparser.ConfigParser()
    if not cfg.read('.gitmodules'):
        raise ValueError('missing root .gitmodules')
    paths = [cfg.get(section, 'path') for section in cfg.sections()]
    if len(paths) != len(set(paths)) or len(cfg.sections()) != len(paths):
        raise ValueError('duplicate submodule path')
    entries = run('ls-tree', '-r', 'HEAD').splitlines()
    links = {line.split('\t', 1)[1] for line in entries if line.startswith('160000 commit ')}
    if set(paths) != links or len(links) != 367:
        raise ValueError('gitlink mapping mismatch')
    if sum(path.startswith(SNOW) for path in paths) != 353:
        raise ValueError('10.6.8 component graph mismatch')
    if sum(path.startswith('historical/') for path in paths) != 14:
        raise ValueError('10.5/10.6 historical graph mismatch')
    for path in EXCLUDED:
        if any(line.split('\t', 1)[1].startswith(path) for line in entries):
            raise ValueError('unqualified modern source tree: ' + path)
    for path, (tree_sha, count) in EXPECTED.items():
        if run('rev-parse', 'HEAD:' + path).strip() != tree_sha:
            raise ValueError('source tree hash mismatch: ' + path)
        if len(run('ls-tree', '-r', '--name-only', 'HEAD', path).splitlines()) != count:
            raise ValueError('source tree file count mismatch: ' + path)
    pin = run('ls-tree', 'HEAD', SNOW + 'xnu').strip()
    if not pin.startswith('160000 commit 99c11f3f90a18f35d3692ea77444b51fd972a4f4\t'):
        raise ValueError('10.6.8 XNU pin mismatch')
    xnu = sum('/xnu-' in path for path in EXPECTED)
    print('PASS: 353 Snow Leopard + 14 historical source pins; {} verified XNU snapshots; modern whole-tree exclusions'.format(xnu))


if __name__ == '__main__':
    try:
        verify()
    except (ValueError, OSError, subprocess.CalledProcessError) as exc:
        print('source graph invalid: {}'.format(exc), file=sys.stderr)
        sys.exit(1)
