#!/usr/bin/env python3
"""Resolve actual recovered PPC Mach-O dylib dependencies to official 10.6.8 source families."""
import collections
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# These mappings are source-family candidates, not proof of ABI or runtime parity.
LIBRARY_FAMILIES = {
    'libSystem.B.dylib': ('Libsystem', 'Libc'),
    'libnetsnmp.15.dylib': ('net_snmp',),
    'libnetsnmpagent.15.dylib': ('net_snmp',),
    'libnetsnmphelpers.15.dylib': ('net_snmp',),
    'libnetsnmpmibs.15.dylib': ('net_snmp',),
    'libnetsnmptrapd.15.dylib': ('net_snmp',),
    'libcrypto.0.9.8.dylib': ('OpenSSL098',),
    'libgcc_s.1.dylib': ('libgcc',),
    'libiconv.2.dylib': ('libiconv',),
    'libexpat.1.dylib': ('expat',),
    'libz.1.dylib': ('zlib',),
    'libncurses.5.4.dylib': ('ncurses',),
    'libedit.2.dylib': ('libedit',),
    'libfreetype.6.dylib': (),
    'libpng12.0.dylib': (),
    'libcdt.0.dylib': ('graphviz',),
    'libgraph.0.dylib': ('graphviz',),
    'libagraph.0.dylib': ('graphviz',),
    'libpathplan.0.dylib': ('graphviz',),
    'libexpr.0.dylib': ('graphviz',),
}
FRAMEWORK_FAMILIES = {
    'IOKit': ('IOKitUser',),
    'ApplicationServices': (),
    'DiskArbitration': ('DiskArbitration',),
    'CoreFoundation': ('CF',),
    'CoreServices': (),
    'Carbon': (),
}


def resolve(inventory, release):
    manifest = {x['project']: x['tag'] for x in release['projects']}
    dependencies = collections.Counter()
    for item in inventory['macho_magic_candidates']:
        if item['contains_ppc']:
            for slice_info, cpu in zip(item['slice_load_commands'], item['cpu_types']):
                if cpu in (18, 0x01000012):
                    dependencies.update(slice_info['dependencies'])
    result = []
    for name, count in sorted(dependencies.items()):
        if '/Frameworks/' in name:
            framework = name.split('/Frameworks/', 1)[1].split('.framework/', 1)[0]
            families = FRAMEWORK_FAMILIES.get(framework)
        else:
            families = LIBRARY_FAMILIES.get(name.rsplit('/', 1)[-1])
        if families is None:
            raise ValueError('unclassified recovered PowerPC dependency: ' + name)
        missing = [family for family in families if family not in manifest]
        if missing:
            raise ValueError('source family missing from official release: ' + str(missing))
        for tag in (manifest[family] for family in families):
            if not (ROOT / 'src/releases/10.6.8' / tag).is_dir():
                raise ValueError('release source not vendored: ' + tag)
        result.append({'install_name': name, 'ppc_references': count,
                       'official_source_tags': [manifest[family] for family in families],
                       'source_availability': 'release_exact_vendored' if families else 'external_or_closed_source'})
    return {'release': release['release'], 'dependencies': result,
            'abi_parity': 'not_assessed', 'runtime_parity': 'not_assessed'}


def main():
    inventory = json.loads((ROOT / 'docs/build_zip_direct_binary_inventory.json').read_text(encoding='utf-8'))
    release = json.loads((ROOT / 'source-releases/10.6.8.json').read_text(encoding='utf-8'))
    result = resolve(inventory, release)
    assert len(result['dependencies']) == 26, 'unexpected recovered PPC dependency set'
    print('PASS: {} recovered PowerPC dependencies mapped to vendored official 10.6.8 source families'.format(len(result['dependencies'])))
    return result


if __name__ == '__main__':
    main()
