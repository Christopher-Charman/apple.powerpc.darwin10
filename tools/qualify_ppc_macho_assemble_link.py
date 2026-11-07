#!/usr/bin/env python3
"""Build and validate a real 32-bit PowerPC Mach-O relocatable with cctools."""
import argparse
import hashlib
import json
import struct
from inspect_ppc_macho import _validate_slice
import subprocess
from pathlib import Path


def check(path):
    data = path.read_bytes()
    if len(data) < 28 or data[:4] != b'\xfe\xed\xfa\xce':
        raise ValueError('expected big-endian 32-bit Mach-O: ' + str(path))
    cpu, subtype, kind, ncmds, cmdsize, flags = struct.unpack_from('>6I', data, 4)
    if cpu != 18 or kind != 1 or cmdsize > len(data) - 28:
        raise ValueError('invalid PPC MH_OBJECT header: ' + str(path))
    with path.open('rb') as stream:
        checked_cpu, _subtype, checked_kind = _validate_slice(stream, 0, len(data))
    if checked_cpu != 18 or checked_kind != 1:
        raise ValueError('invalid PPC32 relocatable Mach-O')
    return {'sha256': hashlib.sha256(data).hexdigest(),
            'bytes': len(data), 'cpu': cpu, 'filetype': kind,
            'ncmds': ncmds, 'sizeofcmds': cmdsize}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--assembler', type=Path, required=True)
    parser.add_argument('--linker', type=Path, required=True)
    parser.add_argument('--output-dir', type=Path, required=True)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    source = args.output_dir / 'ppc-abi.s'
    assembled = args.output_dir / 'ppc-abi.o'
    linked = args.output_dir / 'ppc-abi-linked.o'
    source.write_text('.text\n.globl _ppc_abi_probe\n_ppc_abi_probe:\n li r3, 7\n blr\n', encoding='ascii')
    subprocess.run([str(args.assembler), '-o', str(assembled), str(source)], check=True)
    first = check(assembled)
    subprocess.run([str(args.linker), '-arch', 'ppc', '-r', '-o', str(linked),
                    str(assembled)], check=True)
    second = check(linked)
    print(json.dumps({'gate': 'PPC_MACHO_ASSEMBLE_RELOCATABLE_LINK',
                      'result': 'PASS', 'assembled': first, 'linked': second,
                      'executable_sdk_link': 'not_qualified',
                      'physical_runtime': 'not_qualified'}, indent=2))


if __name__ == '__main__':
    main()
