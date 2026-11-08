#!/usr/bin/env python3
"""Enforce independent historical evidence planes and directly observable PPC build paths."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def inspect():
    build = (ROOT / 'tooling/darwinbuild/plists/10A432.plist').read_text(encoding='utf-8')
    cf = (ROOT / 'src/releases/10.6.8/CF-550.43/BuildCFLite').read_text(encoding='utf-8')
    binary = json.loads((ROOT / 'docs/build_zip_direct_binary_inventory.json').read_text(encoding='utf-8'))
    assert 'RC_ARCHS = "i386 x86_64"' in build, 'Darwinbuild Intel default changed'
    assert 'ARCHFLAGS="-arch ppc -arch i386 -arch x86_64"' in cf, 'CF PPC target missing'
    assert 'CFUnicodeData-B.mapping' in cf and '"powerpc"' in cf, 'CF PPC endian path missing'
    assert len(binary['macho_magic_candidates']) == 126, 'original binary corpus mismatch'
    return {'evidence_planes': {
        'source_release': 'source-releases/10.6.8.json',
        'build_recipe': 'tooling/darwinbuild/plists/10A432.plist',
        'build_patch_archive': 'tooling/darwinbuild/patches',
        'historical_owner_binary': 'docs/build_zip_direct_binary_inventory.json',
        'shipping_state': 'not_verified',
        'darwinbuild_root_binaries': 'not_recovered'},
        'cf_550_43': {'powerpc_compile_target': True, 'powerpc_big_endian_unicode': True,
                      'system_corefoundation_abi_parity': 'not_verified'},
        'historical_builds': ['10A096', '10A190', '10A222', '10A432', '10B504', '10K540']}


if __name__ == '__main__':
    print(json.dumps(inspect(), indent=2))
