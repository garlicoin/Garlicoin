#!/usr/bin/env python3
"""Compare executable sections across symbol stripping and ad-hoc bundle sealing."""
import hashlib
from pathlib import Path
import struct
import sys


def contents(path):
    data = Path(path).read_bytes()
    header = struct.unpack_from('<IiiIIIII', data)
    assert header[0] == 0xfeedfacf, 'Expected a thin 64-bit little-endian Mach-O'
    sections = {}
    identity = [header[1], header[2], header[3]]
    position = 32
    for _ in range(header[4]):
        command, size = struct.unpack_from('<II', data, position)
        assert size >= 8 and position + size <= len(data)
        if command == 0x19:  # LC_SEGMENT_64
            count = struct.unpack_from('<I', data, position + 64)[0]
            for index in range(count):
                start = position + 72 + index * 80
                section, segment, address, length, offset, alignment, reloff, nreloc, flags, *_ = struct.unpack_from('<16s16sQQIIIIIIII', data, start)
                section, segment = section.rstrip(b'\0'), segment.rstrip(b'\0')
                if segment == b'__DWARF':
                    continue
                zero_fill = (flags & 0xff) in (1, 0xc, 0x12)
                payload = b'' if zero_fill else data[offset:offset + length]
                assert zero_fill or len(payload) == length
                sections[(segment, section)] = (address, length, flags, hashlib.sha256(payload).hexdigest())
        elif command in (0x1b, 0x80000028):  # LC_UUID / LC_MAIN
            identity.append((command, data[position + 8:position + size]))
        position += size
    assert sections
    return identity, sections

assert len(sys.argv) == 3
assert contents(sys.argv[1]) == contents(sys.argv[2]), 'Executable code/data or UUID/entry point changed'
print('PASS: Mach-O code/data sections, UUID and entry point match across packaging')
