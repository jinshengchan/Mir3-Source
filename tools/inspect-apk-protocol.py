#!/usr/bin/env python3
"""Read packet IDs and property order from an APK, without executing its code."""
import argparse
import base64
import gzip
import hashlib
import json
import pathlib
import struct
import zipfile

import dnfile
import lz4.block


def unpack_image(image):
    if image[:4] == b'XALZ':
        image = lz4.block.decompress(image[12:], uncompressed_size=struct.unpack_from('<I', image, 8)[0])
    if image[:2] != b'MZ':
        raise ValueError('Assembly is not a managed PE image')
    return image


def images(apk):
    with zipfile.ZipFile(apk) as archive:
        names = archive.namelist()
        elf = 'lib/arm64-v8a/libassemblies.arm64-v8a.blob.so'
        if elf in names:
            blob = archive.read(elf)
            start = blob.find(b'XABA')
            if start < 0:
                raise ValueError('Assembly store header missing')
            magic, version, count, index_count, index_size = struct.unpack_from('<5I', blob, start)
            if version & 0xffff not in (2, 3) or not 0 < count < 10000:
                raise ValueError(f'Unsupported assembly store version {version:#x}')
            descriptors = start + 20 + index_size
            cursor = descriptors + count * 28
            for index in range(count):
                length, = struct.unpack_from('<I', blob, cursor)
                cursor += 4
                if not 0 < length < 1024:
                    raise ValueError('Invalid assembly name length')
                name = blob[cursor:cursor + length].decode('utf-8')
                cursor += length
                if pathlib.PurePosixPath(name).name.removesuffix('.dll') not in ('Mir3.Droid', 'Library'):
                    continue
                mapping, offset, size, *_ = struct.unpack_from('<7I', blob, descriptors + index * 28)
                yield name, unpack_image(blob[start + offset:start + offset + size])
        elif 'assemblies/assemblies.manifest' in names:
            manifest = archive.read('assemblies/assemblies.manifest').decode('utf-8')
            for line in manifest.splitlines()[1:]:
                columns = line.split()
                if len(columns) != 5 or columns[4] not in ('Mir3.Droid', 'Library'):
                    continue
                blob_id, index = int(columns[2]), int(columns[3])
                if blob_id != 0:
                    raise ValueError('Unsupported architecture-specific application assembly')
                blob = archive.read('assemblies/assemblies.blob')
                offset, size, *_ = struct.unpack_from('<6I', blob, 20 + index * 24)
                yield columns[4], unpack_image(blob[offset:offset + size])
        else:
            raise ValueError('No supported assembly store found in APK')


def inspect(name, image):
    pe = dnfile.dnPE(data=image, clr_lazy_load=True)
    tables = pe.net.mdtables
    properties = {}
    for entry in tables.PropertyMap or []:
        parent = entry.Parent.row
        properties[(str(parent.TypeNamespace), str(parent.TypeName))] = [
            {'name': str(prop.row.Name), 'signature': prop.row.Type.value.hex()} for prop in entry.PropertyList
        ]
    packets = []
    for entry in tables.TypeDef:
        namespace, type_name = str(entry.TypeNamespace), str(entry.TypeName)
        base = entry.Extends.row if entry.Extends else None
        if base and str(getattr(base, 'TypeName', '')) == 'Packet' and namespace.startswith('Library.Network.'):
            packets.append({'namespace': namespace, 'name': type_name,
                            'properties': properties.get((namespace, type_name), [])})
    packets.sort(key=lambda p: (p['namespace'] != 'Library.Network.GeneralPackets', p['namespace'], p['name']))
    for packet_id, packet in enumerate(packets):
        packet['id'] = packet_id
    return {'assembly': name, 'sha256': hashlib.sha256(image).hexdigest(), 'packets': packets}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('apk')
    parser.add_argument('--output', required=True)
    parser.add_argument('--annotations', action='store_true')
    args = parser.parse_args()
    reports = [inspect(name, image) for name, image in images(args.apk)]
    reports = [report for report in reports if report['packets']]
    if not reports:
        raise ValueError('No packet definitions found')
    payload = json.dumps(reports, ensure_ascii=True, separators=(',', ':')).encode()
    pathlib.Path(args.output).write_bytes(payload)
    for report in reports:
        print(report['assembly'], 'packet count:', len(report['packets']))
        for packet in report['packets']:
            if packet['name'] in ('Login', 'Logout', 'NewAccount', 'GoodVersion', 'Ping'):
                print(packet['id'], packet['namespace'] + '.' + packet['name'],
                      ', '.join(prop['name'] for prop in packet['properties']))
    if args.annotations:
        encoded = base64.b64encode(gzip.compress(payload, mtime=0)).decode()
        chunks = [encoded[i:i + 6000] for i in range(0, len(encoded), 6000)]
        for index, chunk in enumerate(chunks):
            print(f'::notice title=Original protocol {index + 1}/{len(chunks)}::{chunk}')


if __name__ == '__main__':
    main()
