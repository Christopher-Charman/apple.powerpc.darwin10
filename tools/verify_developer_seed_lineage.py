#!/usr/bin/env python3
"""Keep developer-seed/toolchain evidence distinct from Apple retail source manifests."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def verify():
    data = json.loads((ROOT / 'docs/provenance/developer-seed-toolchain-lineage.json').read_text(encoding='utf-8'))
    seeds = {entry['build']: entry for entry in data['developer_seeds']}
    required = ('10A096', '10A190', '10A222', '10A261', '10A286', '10A314', '10A354', '10A432', '10B504', '10K540')
    if set(seeds) != set(required):
        raise ValueError('developer-seed lineage incomplete')
    if any('not verified' not in entry['artifact_state'] and 'present' not in entry['artifact_state'] for entry in seeds.values()):
        raise ValueError('developer-seed evidence state missing')
    tools = {entry['linker_generation'] for entry in data['developer_tools']}
    if not {'ld64-87.3.1', 'ld64-91', 'ld64-95.2', 'ld64-95.2.3', 'ld64-97.17', 'ld64-127.2'} <= tools:
        raise ValueError('intermediate Xcode linker lineage incomplete')
    required_tracks = ('Educovas', 'Julian Fairfax', 'Jazzzny', 'barracuda156', 'KDK', 'Darwinbuild')
    if not all(any(word in x['name'] for x in data['additional_source_tracks']) for word in required_tracks):
        raise ValueError('non-Apple source track missing')
    return len(seeds), len(tools), len(data['additional_source_tracks'])


if __name__ == '__main__':
    print('PASS: {} developer seeds, {} linker generations, {} additional source tracks'.format(*verify()))
