#!/usr/bin/env python3
"""Qualify a freestanding 32-bit PowerPC Darwin Mach-O executable link.

This is a cross-link artifact gate, not SDK linkage or native execution.
"""
import argparse
import hashlib
import json
import struct
import subprocess
import tempfile
from pathlib import Path

from inspect_ppc_macho import _validate_slice


def inspect_executable(path):
    data = path.read_bytes()
    if len(data) < 28 or data[:4] != b'\xfe\xed\xfa\xce':
        raise ValueError('not big-endian 32-bit Mach-O')
    cpu, subtype, filetype, ncmds, sizeofcmds, flags = struct.unpack_from('>6I', data, 4)
    if cpu != 18 or filetype != 2:
        raise ValueError('expected PPC32 MH_EXECUTE')
    with path.open('rb') as stream:
        checked_cpu, _, checked_kind = _validate_slice(stream, 0, len(data))
    if (checked_cpu, checked_kind) != (18, 2):
        raise ValueError('invalid PPC executable load commands')
    cursor = 28
    commands = []
    for _ in range(ncmds):
        command, size = struct.unpack_from('>II', data, cursor)
        commands.append(command)
        cursor += size
    if cursor != 28 + sizeofcmds:
        raise ValueError('load command accounting mismatch')
    if 1 not in commands or 5 not in commands:
        raise ValueError('missing LC_SEGMENT or LC_UNIXTHREAD')
    return {'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data),
            'cpu': cpu, 'filetype': filetype, 'ncmds': ncmds,
            'sizeofcmds': sizeofcmds, 'load_commands': commands}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--assembler', type=Path, required=True)
    parser.add_argument('--linker', type=Path, required=True)
    parser.add_argument('--output-dir', type=Path, required=True)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='ppc-executable-', dir=args.output_dir) as directory:
        root = Path(directory)
        source = root / 'start.s'
        obj = root / 'start.o'
        binary = root / 'start'
        source.write_text('.text\n.globl _start\n_start:\n li r3, 0\n blr\n', encoding='ascii')
        subprocess.run([str(args.assembler), '-o', str(obj), str(source)], check=True)
        subprocess.run([str(args.linker), '-arch', 'ppc', '-macosx_version_min',
                        '10.6', '-e', '_start', '-o', str(binary), str(obj)], check=True)
        result = inspect_executable(binary)
        print(json.dumps({'gate': 'PPC_MACHO_FREESTANDING_EXECUTABLE_LINK',
                          'result': 'PASS', 'executable': result,
                          'sdk_link': 'not_qualified',
                          'native_runtime': 'not_qualified'}, indent=2))


if __name__ == '__main__':
    main()
