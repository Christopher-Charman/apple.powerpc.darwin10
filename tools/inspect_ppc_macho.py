#!/usr/bin/env python3
"""Read-only Mach-O/FAT architecture inspection for recovered Darwin artifacts."""
import argparse
import hashlib
import json
import struct
import sys
from pathlib import Path

CPU = {7: 'i386', 0x01000007: 'x86_64', 18: 'ppc', 0x01000012: 'ppc64'}
FAT = {b'\xca\xfe\xba\xbe': ('>', False), b'\xbe\xba\xfe\xca': ('<', False),
       b'\xca\xfe\xba\xbf': ('>', True), b'\xbf\xba\xfe\xca': ('<', True)}
THIN = {b'\xfe\xed\xfa\xce': '>', b'\xce\xfa\xed\xfe': '<',
        b'\xfe\xed\xfa\xcf': '>', b'\xcf\xfa\xed\xfe': '<'}


def _validate_slice(stream, offset, length, declared_cpu=None):
    """Verify the embedded Mach-O header and bounded load-command sequence."""
    stream.seek(offset)
    prefix = stream.read(4)
    if prefix not in THIN:
        raise ValueError('FAT slice is not a Mach-O object')
    endian = THIN[prefix]
    wide = prefix in (b'\xfe\xed\xfa\xcf', b'\xcf\xfa\xed\xfe')
    header_size = 32 if wide else 28
    if length < header_size:
        raise ValueError('truncated Mach-O header')
    header = stream.read(header_size - 4)
    if len(header) != header_size - 4:
        raise ValueError('truncated Mach-O header')
    cpu, subtype, filetype, ncmds, sizeofcmds, flags = struct.unpack(endian + 'IIIIII', header[:24])
    if declared_cpu is not None and cpu != declared_cpu:
        raise ValueError('FAT architecture does not match embedded CPU')
    if cpu in (18, 0x01000012) and endian != '>':
        raise ValueError('PowerPC Mach-O must be big-endian')
    if not 1 <= filetype <= 12:
        raise ValueError('invalid Mach-O file type')
    if sizeofcmds > length - header_size or ncmds > sizeofcmds // 8:
        raise ValueError('invalid Mach-O load-command bounds')
    consumed = 0
    for _ in range(ncmds):
        raw = stream.read(8)
        if len(raw) != 8:
            raise ValueError('truncated Mach-O load command')
        _cmd, cmdsize = struct.unpack(endian + 'II', raw)
        if cmdsize < 8 or cmdsize > sizeofcmds - consumed:
            raise ValueError('invalid Mach-O load command size')
        consumed += cmdsize
        stream.seek(cmdsize - 8, 1)
    if consumed != sizeofcmds:
        raise ValueError('Mach-O load-command size mismatch')
    return cpu, subtype, filetype


def inspect(path):
    path = Path(path)
    size = path.stat().st_size
    with path.open('rb') as stream:
        header = stream.read(8)
        if len(header) < 8:
            raise ValueError('truncated Mach-O header')
        magic = header[:4]
        if magic in FAT:
            endian, wide = FAT[magic]
            n = struct.unpack(endian + 'I', header[4:8])[0]
            entry_size = 32 if wide else 20
            if n > 128 or 8 + n * entry_size > size:
                raise ValueError('invalid FAT architecture table')
            slices = []
            for i in range(n):
                raw = stream.read(entry_size)
                if len(raw) != entry_size:
                    raise ValueError('truncated FAT architecture entry')
                if wide:
                    cpu, subtype, offset, length, align, reserved = struct.unpack(endian + 'IIQQII', raw)
                else:
                    cpu, subtype, offset, length, align = struct.unpack(endian + 'IIIII', raw)
                if not length or offset < 8 + n * entry_size or offset + length > size:
                    raise ValueError('invalid FAT slice bounds')
                slices.append({'cpu': CPU.get(cpu, 'unknown:' + str(cpu)), 'subtype': subtype,
                               'offset': offset, 'size': length, 'cpu_number': cpu})
            for i, a in enumerate(slices):
                for b in slices[i + 1:]:
                    if a['offset'] < b['offset'] + b['size'] and b['offset'] < a['offset'] + a['size']:
                        raise ValueError('overlapping FAT slices')
            # A FAT table alone is insufficient: inspect each embedded Mach-O header.
            for item in slices:
                _validate_slice(stream, item['offset'], item['size'], item['cpu_number'])
            for item in slices:
                del item['cpu_number']
            kind = 'fat64' if wide else 'fat32'
        elif magic in THIN:
            cpu, subtype, _filetype = _validate_slice(stream, 0, size)
            kind = 'mach-o'
            slices = [{'cpu': CPU.get(cpu, 'unknown:' + str(cpu)), 'subtype': subtype,
                       'offset': 0, 'size': size}]
        else:
            raise ValueError('not Mach-O')
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(chunk)
    return {'file': str(path), 'sha256': digest.hexdigest(), 'bytes': size,
            'format': kind, 'architectures': slices,
            'contains_ppc': any(s['cpu'] in ('ppc', 'ppc64') for s in slices)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('paths', nargs='+')
    args = parser.parse_args()
    try:
        print(json.dumps([inspect(p) for p in args.paths], indent=2, sort_keys=True))
    except (ValueError, OSError) as exc:
        print('Mach-O inspection rejected: ' + str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
