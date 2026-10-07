#!/usr/bin/env python3
"""Read packet IDs and property order from an APK, without executing its code."""
import argparse
import base64
import gzip
import hashlib
import json
import pathlib
import re
import struct
import zipfile

import dnfile
import lz4.block


def runtime_packet_sort(packets):
    """Match Packet's comparer and .NET List.Sort, including unstable ties.

    Client/server types with the same name compare equal. Their metadata input
    order and introsort swaps therefore matter to the actual wire IDs.
    """
    def compare(a, b):
        if a['namespace'] != b['namespace']:
            if a['namespace'] == 'Library.Network.GeneralPackets':
                return -1
            if b['namespace'] == 'Library.Network.GeneralPackets':
                return 1
        return (a['name'] > b['name']) - (a['name'] < b['name'])

    def swap(a, b):
        packets[a], packets[b] = packets[b], packets[a]

    def order(a, b):
        if a != b and compare(packets[a], packets[b]) > 0:
            swap(a, b)

    def down_heap(i, n, lo):
        value = packets[lo + i - 1]
        while i <= n // 2:
            child = 2 * i
            if child < n and compare(packets[lo + child - 1], packets[lo + child]) < 0:
                child += 1
            if compare(value, packets[lo + child - 1]) >= 0:
                break
            packets[lo + i - 1] = packets[lo + child - 1]
            i = child
        packets[lo + i - 1] = value

    def intro(lo, hi, depth):
        while hi > lo:
            size = hi - lo + 1
            if size <= 16:
                if size == 2:
                    order(lo, hi)
                elif size == 3:
                    order(lo, hi - 1)
                    order(lo, hi)
                    order(hi - 1, hi)
                else:
                    for i in range(lo, hi):
                        value, j = packets[i + 1], i
                        while j >= lo and compare(value, packets[j]) < 0:
                            packets[j + 1] = packets[j]
                            j -= 1
                        packets[j + 1] = value
                return
            if depth == 0:
                for i in range(size // 2, 0, -1):
                    down_heap(i, size, lo)
                for i in range(size, 1, -1):
                    swap(lo, lo + i - 1)
                    down_heap(1, i - 1, lo)
                return
            depth -= 1
            mid = lo + (hi - lo) // 2
            order(lo, mid)
            order(lo, hi)
            order(mid, hi)
            pivot = packets[mid]
            swap(mid, hi - 1)
            left, right = lo, hi - 1
            while left < right:
                left += 1
                while compare(packets[left], pivot) < 0:
                    left += 1
                right -= 1
                while compare(pivot, packets[right]) < 0:
                    right -= 1
                if left >= right:
                    break
                swap(left, right)
            swap(left, hi - 1)
            intro(left + 1, hi, depth)
            hi = left - 1
    if len(packets) > 1:
        intro(0, len(packets) - 1, 2 * len(packets).bit_length())


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
    def decode_signature(signature):
        cursor = 2  # PROPERTY calling convention followed by parameter count
        def compressed():
            nonlocal cursor
            first = signature[cursor]
            cursor += 1
            if first < 128:
                return first
            size = 1 if first < 192 else 3
            value = first & (63 if size == 1 else 31)
            for _ in range(size):
                value = (value << 8) | signature[cursor]
                cursor += 1
            return value
        def type_name():
            nonlocal cursor
            element = signature[cursor]
            cursor += 1
            primitives = {2: 'System.Boolean', 3: 'System.Char', 4: 'System.SByte', 5: 'System.Byte',
                          6: 'System.Int16', 7: 'System.UInt16', 8: 'System.Int32', 9: 'System.UInt32',
                          10: 'System.Int64', 11: 'System.UInt64', 12: 'System.Single',
                          13: 'System.Double', 14: 'System.String', 28: 'System.Object'}
            if element in primitives:
                return primitives[element]
            if element in (17, 18):
                token = compressed()
                table = (tables.TypeDef, tables.TypeRef, tables.TypeSpec)[token & 3]
                row = table.rows[(token >> 2) - 1]
                return str(row.TypeNamespace) + '.' + str(row.TypeName)
            if element == 21:
                generic = type_name()
                count = compressed()
                return generic + '[' + ','.join(type_name() for _ in range(count)) + ']'
            if element == 29:
                return type_name() + '[]'
            raise ValueError(f'Unsupported property element {element:#x}')
        return type_name()
    properties = {}
    property_maps = {}
    ignored_properties = set()
    ignore_constructors = set()
    for definition in tables.TypeDef:
        if str(definition.TypeName) == 'IgnorePropertyPacket':
            ignore_constructors.update(id(method.row) for method in definition.MethodList)
    for attribute in tables.CustomAttribute or []:
        constructor = attribute.Type.row
        owner = getattr(constructor, 'Class', None)
        if id(constructor) in ignore_constructors or (owner and str(getattr(owner.row, 'TypeName', '')) == 'IgnorePropertyPacket'):
            ignored_properties.add(id(attribute.Parent.row))
    for entry in tables.PropertyMap or []:
        parent = entry.Parent.row
        property_maps[(str(parent.TypeNamespace), str(parent.TypeName))] = entry
    def model_properties(key):
        entry = property_maps.get(key)
        if entry is None:
            return []
        return [
            {'name': str(prop.row.Name), 'signature': prop.row.Type.value.hex(),
             'type': decode_signature(prop.row.Type.value)} for prop in entry.PropertyList
            if id(prop.row) not in ignored_properties
        ]
    for key in property_maps:
        if key[0].startswith('Library.Network.'):
            properties[key] = model_properties(key)
    # Packet properties can refer to wire models in Library (ClientControl,
    # StartInformation, Stats, etc.). Inspect the complete reachable model graph.
    pending = [prop['type'] for value in properties.values() for prop in value]
    visited = {namespace + '.' + name for namespace, name in properties}
    while pending:
        for type_name in re.findall(r'Library\.[\w.`]+', pending.pop()):
            if type_name in visited:
                continue
            visited.add(type_name)
            namespace, model_name = type_name.rsplit('.', 1)
            key = (namespace, model_name)
            if key in property_maps:
                properties[key] = model_properties(key)
                pending.extend(prop['type'] for prop in properties[key])
    packets = []
    enums = {}
    constants = {id(entry.Parent.row): entry.Value.value.hex() for entry in tables.Constant or []}
    for entry in tables.TypeDef:
        namespace, type_name = str(entry.TypeNamespace), str(entry.TypeName)
        base = entry.Extends.row if entry.Extends else None
        if base and str(getattr(base, 'TypeName', '')) == 'Packet' and namespace.startswith('Library.Network.'):
            packets.append({'namespace': namespace, 'name': type_name,
                            'properties': properties.get((namespace, type_name), [])})
        if base and str(getattr(base, 'TypeName', '')) == 'Enum' and namespace.startswith('Library'):
            enums[namespace + '.' + type_name] = {
                str(field.row.Name): constants[id(field.row)] for field in entry.FieldList
                if id(field.row) in constants
            }
    runtime_packet_sort(packets)
    for packet_id, packet in enumerate(packets):
        packet['id'] = packet_id
    return {'assembly': name, 'sha256': hashlib.sha256(image).hexdigest(), 'packets': packets,
            'models': {namespace + '.' + name: value for (namespace, name), value in properties.items()},
            'enums': enums}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('apk')
    parser.add_argument('--output', required=True)
    parser.add_argument('--annotations', action='store_true')
    parser.add_argument('--compare', help='Require packet IDs and layouts to match this original report')
    args = parser.parse_args()
    reports = [inspect(name, image) for name, image in images(args.apk)]
    reports = [report for report in reports if report['packets']]
    if not reports:
        raise ValueError('No packet definitions found')
    payload = json.dumps(reports, ensure_ascii=True, separators=(',', ':')).encode()
    pathlib.Path(args.output).write_bytes(payload)
    if args.compare:
        expected = json.loads(pathlib.Path(args.compare).read_bytes())
        if len(expected) != 1 or len(reports) != 1:
            raise ValueError('Compatibility check requires exactly one packet assembly')
        def shape(packet):
            return (packet['id'], packet['namespace'], packet['name'],
                    [(prop['name'], prop['type']) for prop in packet['properties']])
        if [shape(p) for p in expected[0]['packets']] != [shape(p) for p in reports[0]['packets']]:
            raise ValueError('Packet IDs or serialized properties differ from original APK')
        for name, properties in expected[0].get('models', {}).items():
            actual = reports[0]['models'].get(name)
            if actual is None or [(p['name'], p['type']) for p in properties] != [(p['name'], p['type']) for p in actual]:
                raise ValueError('Serialized model differs from original APK: ' + name)
        for name in ('Library.LoginResult', 'Library.NewAccountResult', 'Library.ChangePasswordResult',
                     'Library.DisconnectReason', 'Library.Platform', 'Library.StartGameResult'):
            if expected[0]['enums'].get(name) != reports[0]['enums'].get(name):
                raise ValueError('Login enum differs from original APK: ' + name)
        print(f'::notice title=Original Android protocol compatibility::Verified {len(reports[0]["packets"])} packet IDs, property layouts and login result enums against original APK')
    for report in reports:
        print(report['assembly'], 'packet count:', len(report['packets']))
        for packet in report['packets']:
            if packet['name'] in ('Login', 'Logout', 'NewAccount', 'GoodVersion', 'Ping', 'RequestStartGame'):
                print(packet['id'], packet['namespace'] + '.' + packet['name'],
                      ', '.join(prop['name'] for prop in packet['properties']))
    if args.annotations:
        # A workflow step accepts at most ten notice annotations. Keep the
        # downloadable report complete; publish only enums relevant to login.
        login_enums = {'LoginResult', 'NewAccountResult', 'ChangePasswordResult',
                       'DisconnectReason', 'Platform', 'GameStage', 'StartGameResult'}
        summaries = [{**report, 'enums': {name: values for name, values in report['enums'].items()
                      if name.rsplit('.', 1)[-1] in login_enums}} for report in reports]
        summary = json.dumps(summaries, ensure_ascii=True, separators=(',', ':')).encode()
        encoded = base64.b64encode(gzip.compress(summary, mtime=0)).decode()
        # GitHub truncates individual annotation messages at 4096 characters.
        chunks = [encoded[i:i + 3800] for i in range(0, len(encoded), 3800)]
        if len(chunks) > 10:
            raise ValueError('Protocol summary exceeds annotation limit')
        for index, chunk in enumerate(chunks):
            print(f'::notice title=Original protocol {index + 1}/{len(chunks)}::{chunk}')


if __name__ == '__main__':
    main()
