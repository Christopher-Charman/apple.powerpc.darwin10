#!/usr/bin/env python3
"""Read-only, hash-bound inventory of the historical BUILD.zip embedded 7z."""
import ctypes
import hashlib
import io
import json
import struct
import sys
import zipfile
from pathlib import Path

ARCHIVE_HASH = 'a7bb2bab2112673dec9fe57e66221431b78d06a2ec134ac75ae0fc24b24fe77f'
TOME_HASH = '0121ff2d17ce7492706b00eda1c9fdb04b803f54c0a33e11c1ce6a12a3d727ec'
TOME_PATH = 'BUILD.app/Contents/Resources/Tome.7z'
MAGIC = {b'\xfe\xed\xfa\xce', b'\xce\xfa\xed\xfe', b'\xfe\xed\xfa\xcf', b'\xcf\xfa\xed\xfe',
         b'\xca\xfe\xba\xbe', b'\xbe\xba\xfe\xca', b'\xca\xfe\xba\xbf', b'\xbf\xba\xfe\xca'}


def inventory(outer):
    if hashlib.sha256(outer.read_bytes()).hexdigest() != ARCHIVE_HASH:
        raise ValueError('BUILD.zip identity mismatch')
    with zipfile.ZipFile(str(outer)) as z:
        tome = z.read(TOME_PATH)
    if hashlib.sha256(tome).hexdigest() != TOME_HASH:
        raise ValueError('Tome.7z identity mismatch')
    lib = ctypes.CDLL('libarchive.so.13')
    lib.archive_read_new.restype = ctypes.c_void_p
    lib.archive_read_support_format_7zip.argtypes = [ctypes.c_void_p]
    lib.archive_read_support_filter_all.argtypes = [ctypes.c_void_p]
    lib.archive_read_open_memory.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t]
    lib.archive_read_next_header.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_void_p)]
    lib.archive_entry_pathname.argtypes = [ctypes.c_void_p]
    lib.archive_entry_pathname.restype = ctypes.c_char_p
    lib.archive_entry_size.argtypes = [ctypes.c_void_p]
    lib.archive_entry_size.restype = ctypes.c_int64
    lib.archive_read_data.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t]
    lib.archive_read_data.restype = ctypes.c_ssize_t
    lib.archive_read_free.argtypes = [ctypes.c_void_p]
    handle = lib.archive_read_new()
    buffer = ctypes.create_string_buffer(tome)
    if lib.archive_read_support_format_7zip(handle) != 0 or lib.archive_read_support_filter_all(handle) != 0:
        raise ValueError('libarchive 7z support unavailable')
    if lib.archive_read_open_memory(handle, buffer, len(tome)) != 0:
        raise ValueError('cannot open embedded Tome')
    count = 0
    matches = []
    chunk = ctypes.create_string_buffer(65536)
    try:
        while True:
            entry = ctypes.c_void_p()
            code = lib.archive_read_next_header(handle, ctypes.byref(entry))
            if code == 1:
                break
            if code != 0:
                raise ValueError('corrupt Tome header at entry {}'.format(count))
            count += 1
            name = lib.archive_entry_pathname(entry).decode('utf-8', 'replace')
            size = lib.archive_entry_size(entry)
            digest = hashlib.sha256()
            prefix = b''
            while True:
                n = lib.archive_read_data(handle, chunk, len(chunk))
                if n < 0:
                    raise ValueError('corrupt Tome data: ' + name)
                if n == 0:
                    break
                block = chunk.raw[:n]
                digest.update(block)
                if len(prefix) < 16384:
                    prefix += block[:16384 - len(prefix)]
            if prefix[:4] in MAGIC:
                magic = prefix[:4]
                if magic in (b'\xca\xfe\xba\xbe', b'\xbe\xba\xfe\xca', b'\xca\xfe\xba\xbf', b'\xbf\xba\xfe\xca'):
                    endian = '>' if magic in (b'\xca\xfe\xba\xbe', b'\xca\xfe\xba\xbf') else '<'
                    wide = magic in (b'\xca\xfe\xba\xbf', b'\xbf\xba\xfe\xca')
                    narch = struct.unpack(endian + 'I', prefix[4:8])[0]
                    width = 32 if wide else 20
                    if narch > 128 or len(prefix) < 8 + narch * width:
                        raise ValueError('invalid FAT table: ' + name)
                    cpus = []
                    for i in range(narch):
                        cpu = struct.unpack(endian + 'I', prefix[8 + i * width:12 + i * width])[0]
                        cpus.append(cpu)
                else:
                    endian = '>' if magic in (b'\xfe\xed\xfa\xce', b'\xfe\xed\xfa\xcf') else '<'
                    cpus = [struct.unpack(endian + 'I', prefix[4:8])[0]]
                matches.append({'path': name, 'bytes': size, 'sha256': digest.hexdigest(),
                                'magic': magic.hex(), 'cpu_types': cpus,
                                'contains_ppc': any(cpu in (18, 0x01000012) for cpu in cpus)})
    finally:
        lib.archive_read_free(handle)
    return {'archive_sha256': ARCHIVE_HASH, 'tome_sha256': TOME_HASH,
            'entries': count, 'macho_magic_candidates': matches,
            'binary_architecture_verification': 'CPU headers checked; embedded FAT slice consistency not assessed'}


if __name__ == '__main__':
    try:
        print(json.dumps(inventory(Path(sys.argv[1])), sort_keys=True, indent=2))
    except (ValueError, OSError, IndexError, KeyError, zipfile.BadZipFile) as exc:
        print('BUILD inspection rejected: ' + str(exc), file=sys.stderr)
        sys.exit(1)
