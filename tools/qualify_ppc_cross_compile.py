#!/usr/bin/env python3
"""Compile original Snow Leopard kernel C++ sources to real PPC ELF32 objects.

ELF object qualification is a CPU code-generation gate, not a Darwin Mach-O ABI gate.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import struct
import subprocess

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ('new_op.cc', 'del_op.cc')


def qualify(clang, output_dir):
    output_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    for name in SOURCES:
        source = ROOT / 'src/releases/10.6.8/Libcpp_kext-8' / name
        target = output_dir / (name + '.ppc.o')
        subprocess.run([str(clang), '-target', 'powerpc-unknown-none', '-std=gnu++98',
                        '-ffreestanding', '-fno-exceptions', '-fno-rtti', '-c',
                        str(source), '-o', str(target)], check=True)
        data = target.read_bytes()
        if len(data) < 52 or data[:4] != b'\x7fELF' or data[4] != 1 or data[5] != 2:
            raise ValueError('expected ELF32 big-endian object: ' + name)
        if struct.unpack_from('>H', data, 18)[0] != 20:
            raise ValueError('expected PowerPC e_machine=20: ' + name)
        if struct.unpack_from('>H', data, 16)[0] != 1:
            raise ValueError('expected relocatable object: ' + name)
        rows.append({'source': source.relative_to(ROOT).as_posix(),
                     'object': target.name, 'sha256': hashlib.sha256(data).hexdigest(),
                     'format': 'ELF32', 'endianness': 'big', 'machine': 'PowerPC',
                     'darwin_macho_abi_qualified': False})
    return {'gate': 'PPC_ELF32_CROSS_COMPILE', 'result': 'PASS', 'objects': rows,
            'darwin_link_and_runtime': 'not_qualified'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--clang', type=Path, default=Path(os.environ.get('PPC_CLANG', '/usr/bin/clang')))
    parser.add_argument('--output-dir', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(qualify(args.clang, args.output_dir), indent=2))
