#!/usr/bin/env python3
"""Verify actual bundled files against their manifests and optionally the built APK."""
import argparse
import gzip
import hashlib
import io
import json
import pathlib
import struct
import zipfile


def read_exact(stream, length):
    if length < 0:
        raise ValueError('Invalid length')
    data = stream.read(length)
    if len(data) != length:
        raise ValueError('Truncated resource manifest')
    return data


def read_string(stream):
    size = 0
    for shift in range(0, 35, 7):
        value = read_exact(stream, 1)[0]
        size |= (value & 127) << shift
        if value < 128:
            if size > 4096:
                raise ValueError('Resource name too long')
            return read_exact(stream, size).decode('utf-8')
    raise ValueError('Invalid manifest string')


def read_length(stream):
    value = struct.unpack('<q', read_exact(stream, 8))[0]
    if value < 0:
        raise ValueError('Invalid resource length')
    return value


def read_hash(stream):
    if struct.unpack('<i', read_exact(stream, 4))[0] != 16:
        raise ValueError('Invalid resource MD5 length')
    return read_exact(stream, 16)


def digest(stream):
    h = hashlib.md5()
    for block in iter(lambda: stream.read(1024 * 1024), b''):
        h.update(block)
    return h.digest()


def verify(root, apk=None):
    update = root / 'LocalUpdate'
    manifest = (update / 'APKVersion.bin').read_bytes()
    stream = io.BytesIO(manifest)
    read_string(stream)
    read_string(stream)
    read_length(stream)
    read_hash(stream)
    name, length, expected = read_string(stream), read_length(stream), read_hash(stream)
    if stream.read(1) or pathlib.PurePosixPath(name).name != name or '\\' in name or name in ('', '.', '..'):
        raise ValueError('Invalid base package manifest')
    base = update / name
    if base.stat().st_size != length:
        raise ValueError('Source base ZIP length mismatch')
    with base.open('rb') as source:
        actual = digest(source)
    if actual != expected:
        raise ValueError(f'Source base ZIP MD5 mismatch: expected {expected.hex()}, actual {actual.hex()}')
    patches = io.BytesIO((update / 'PList.Bin').read_bytes())
    count = 0
    while patches.tell() < len(patches.getbuffer()):
        relative, compressed, checksum = read_string(patches), read_length(patches), read_hash(patches)
        asset = relative.replace('\\', '-').replace('/', '-') + '.gz'
        if ':' in asset or asset.startswith('.'):
            raise ValueError('Invalid patch name')
        path = update / asset
        if path.stat().st_size != compressed:
            raise ValueError(f'Compressed patch length mismatch: {relative}')
        with gzip.open(path, 'rb') as source:
            if digest(source) != checksum:
                raise ValueError(f'Patch MD5 mismatch: {relative}')
        count += 1
    if apk:
        with zipfile.ZipFile(apk) as package:
            if package.read('assets/LocalUpdate/APKVersion.bin') != manifest:
                raise ValueError('APK package manifest differs from source')
            item = package.getinfo('assets/LocalUpdate/' + name)
            if item.file_size != length:
                raise ValueError('APK base ZIP length mismatch')
            with package.open(item) as source:
                if digest(source) != expected:
                    raise ValueError('APK base ZIP MD5 mismatch')
    return {'base': name, 'bytes': length, 'expected_md5': expected.hex(),
            'actual_md5': actual.hex(), 'patches_verified': count,
            'apk_base_verified': bool(apk)}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('root', type=pathlib.Path)
    parser.add_argument('--apk', type=pathlib.Path)
    parser.add_argument('--report', type=pathlib.Path)
    args = parser.parse_args()
    result = verify(args.root, args.apk)
    report = json.dumps(result, indent=2)
    print(report)
    if args.report:
        args.report.write_text(report + '\n')
    print(f"::notice title=Bundled resource integrity::Base MD5 {result['actual_md5']}; length {result['bytes']}; {result['patches_verified']} patches verified; APK verified {result['apk_base_verified']}")
