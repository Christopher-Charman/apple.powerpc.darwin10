#!/usr/bin/env python3
"""Read-only, hash-bound inventory of the historical BUILD.zip embedded 7z."""
import ctypes
import hashlib
import io
from inspect_ppc_macho import _validate_slice
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


def macho_load_commands(data, offset, length):
    """Parse bounded Mach-O dylib dependencies from a validated slice."""
    magic = bytes(data[offset:offset + 4])
    if magic not in (b'\xfe\xed\xfa\xce', b'\xce\xfa\xed\xfe', b'\xfe\xed\xfa\xcf', b'\xcf\xfa\xed\xfe'):
        raise ValueError('invalid Mach-O slice magic')
    endian = '>' if magic in (b'\xfe\xed\xfa\xce', b'\xfe\xed\xfa\xcf') else '<'
    wide = magic in (b'\xfe\xed\xfa\xcf', b'\xcf\xfa\xed\xfe')
    header = 32 if wide else 28
    if length < header:
        raise ValueError('truncated Mach-O header')
    filetype, ncmds, sizeofcmds = struct.unpack(endian + 'III', data[offset + 12:offset + 24])
    if ncmds > 65536 or sizeofcmds > length - header:
        raise ValueError('Mach-O load command table exceeds slice')
    position = offset + header
    limit = position + sizeofcmds
    deps = []
    dylib_versions = []
    install_name = None
    for _ in range(ncmds):
        if position + 8 > limit:
            raise ValueError('truncated Mach-O load command')
        cmd, cmdsize = struct.unpack(endian + 'II', data[position:position + 8])
        if cmdsize < 8 or position + cmdsize > limit:
            raise ValueError('invalid Mach-O load command bounds')
        base_cmd = cmd & 0x7fffffff
        if base_cmd in (0xc, 0xd, 0x18, 0x1f, 0x23):
            if cmdsize < 24:
                raise ValueError('truncated Mach-O dylib command')
            name_offset = struct.unpack(endian + 'I', data[position + 8:position + 12])[0]
            if name_offset < 24 or name_offset >= cmdsize:
                raise ValueError('invalid dylib install name offset')
            raw = bytes(data[position + name_offset:position + cmdsize]).split(b'\0', 1)[0]
            name = raw.decode('utf-8', 'replace')
            timestamp, current, compatibility = struct.unpack(endian + 'III', data[position + 12:position + 24])
            record = {'name': name, 'current_version': current, 'compatibility_version': compatibility, 'command': base_cmd}
            if base_cmd == 0xd:
                install_name = name
            else:
                deps.append(name)
                dylib_versions.append(record)
        position += cmdsize
    return {'filetype': filetype, 'dependencies': deps, 'dylib_versions': dylib_versions, 'install_name': install_name}


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
            candidate_bytes = bytearray()
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
                if candidate_bytes or block[:4] in MAGIC:
                    candidate_bytes.extend(block)
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
                    ranges = []
                    for i in range(narch):
                        cpu = struct.unpack(endian + 'I', prefix[8 + i * width:12 + i * width])[0]
                        cpus.append(cpu)
                        start, length = struct.unpack(endian + ('QQ' if wide else 'II'), prefix[16 + i * width:16 + i * width + (16 if wide else 8)])
                        if length < 12 or start + length > size:
                            raise ValueError('invalid FAT slice bounds: ' + name)
                        ranges.append((start, length))
                    metadata = []
                    for i, (start, length) in enumerate(ranges):
                        for other_start, other_length in ranges[i + 1:]:
                            if start < other_start + other_length and other_start < start + length:
                                raise ValueError('overlapping FAT slices: ' + name)
                        embedded = candidate_bytes[start:start + 12]
                        if len(embedded) < 12 or bytes(embedded[:4]) not in MAGIC - {b'\xca\xfe\xba\xbe', b'\xbe\xba\xfe\xca', b'\xca\xfe\xba\xbf', b'\xbf\xba\xfe\xca'}:
                            raise ValueError('invalid embedded Mach-O: ' + name)
                        inner_endian = '>' if bytes(embedded[:4]) in (b'\xfe\xed\xfa\xce', b'\xfe\xed\xfa\xcf') else '<'
                        if struct.unpack(inner_endian + 'I', embedded[4:8])[0] != cpus[i]:
                            raise ValueError('FAT CPU mismatch: ' + name)
                        _validate_slice(io.BytesIO(candidate_bytes), start, length, cpus[i])
                        metadata.append(macho_load_commands(candidate_bytes, start, length))
                else:
                    endian = '>' if magic in (b'\xfe\xed\xfa\xce', b'\xfe\xed\xfa\xcf') else '<'
                    cpus = [struct.unpack(endian + 'I', prefix[4:8])[0]]
                    _validate_slice(io.BytesIO(candidate_bytes), 0, size)
                    metadata = [macho_load_commands(candidate_bytes, 0, size)]
                matches.append({'path': name, 'bytes': size, 'sha256': digest.hexdigest(),
                                'magic': magic.hex(), 'cpu_types': cpus, 'slice_load_commands': metadata,
                                'contains_ppc': any(cpu in (18, 0x01000012) for cpu in cpus)})
    finally:
        lib.archive_read_free(handle)
    return {'archive_sha256': ARCHIVE_HASH, 'tome_sha256': TOME_HASH,
            'entries': count, 'macho_magic_candidates': matches,
            'binary_architecture_verification': 'FAT bounds, complete embedded Mach-O headers, load commands and CPU identity verified'}


if __name__ == '__main__':
    try:
        print(json.dumps(inventory(Path(sys.argv[1])), sort_keys=True, indent=2))
    except (ValueError, OSError, IndexError, KeyError, zipfile.BadZipFile) as exc:
        print('BUILD inspection rejected: ' + str(exc), file=sys.stderr)
        sys.exit(1)
