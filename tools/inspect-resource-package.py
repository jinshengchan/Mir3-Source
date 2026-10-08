#!/usr/bin/env python3
"""Inventory an authorized resource archive; source catalog gaps are not all fatal."""
import argparse
import hashlib
import json
import pathlib
import re
import subprocess
import zipfile


def normalize(name):
    name = name.replace('\\', '/').strip('/')
    parts = pathlib.PurePosixPath(name).parts
    if '..' in parts or ':' in name:
        raise ValueError('Unsafe archive path: ' + name)
    for i, part in enumerate(parts):
        if part.lower() in ('data', 'map', 'sound', 'localupdate'):
            return '/'.join(parts[i:])
    return name


def inventory(path):
    if zipfile.is_zipfile(path):
        with zipfile.ZipFile(path) as archive:
            bad = archive.testzip()
            if bad:
                raise ValueError('Archive CRC mismatch: ' + bad)
            return 'zip', [{'name': i.filename, 'size': i.file_size} for i in archive.infolist() if not i.is_dir()]
    listing = subprocess.run(['7z', 'l', '-slt', str(path)], check=True, capture_output=True, text=True).stdout
    subprocess.run(['7z', 't', str(path)], check=True, stdout=subprocess.DEVNULL)
    records = []
    body = listing.split('----------', 1)[-1]
    for block in body.split('\n\n'):
        fields = dict(line.split(' = ', 1) for line in block.splitlines() if ' = ' in line)
        if 'Path' in fields and fields.get('Folder') != '+' and 'Size' in fields:
            records.append({'name': fields['Path'], 'size': int(fields['Size'])})
    return '7z-supported', records


def inspect(path, repository, output):
    kind, entries = inventory(path)
    archive_hash = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            archive_hash.update(block)
    names = {normalize(e['name']).lower(): e for e in entries}
    catalog = (repository / 'Library/Libraries.cs').read_text(encoding='utf-8-sig')
    catalog = '\n'.join(line for line in catalog.splitlines() if not line.lstrip().startswith('//'))
    expected = sorted(set(re.findall(r'\[LibraryFile\.[^\]]+\]\s*=\s*@?"([^"]+)"', catalog)))
    missing = [name for name in expected if name.replace('\\', '/').lower() not in names]
    critical = ['Data/ClientSystem.db', 'Data/StartMobileScene.Zl', 'Data/Interface.Zl', 'Data/GameInter.Zl', 'Data/PhoneUI.Zl']
    groups = {group: sum(normalize(e['name']).lower().startswith(group.lower() + '/') for e in entries)
              for group in ('Data', 'Map', 'Sound', 'LocalUpdate')}
    containers = [e['name'] for e in entries if pathlib.PurePosixPath(e['name']).name.lower() in ('data.zip', 'dataadd.zip', 'plist.bin', 'apkversion.bin')]
    result = {'format': kind, 'archive_bytes': path.stat().st_size,
              'archive_sha256': archive_hash.hexdigest(),
              'archive_integrity': 'passed', 'files': len(entries), 'uncompressed_bytes': sum(e['size'] for e in entries),
              'groups': groups, 'containers': containers,
              'critical_missing': [p for p in critical if p.lower() not in names],
              'missing_source_catalog': missing,
              'zero_length_files': [e['name'] for e in entries if e['size'] == 0],
              'note': 'Catalog includes optional/streamed libraries. Missing catalog files do not alone prove an unusable package. Nested resource containers require a second inspection. Image completeness is not established by file presence.',
              'entries': entries}
    output.mkdir(parents=True, exist_ok=True)
    (output / 'resource-report.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    lines = ['# Resource package inspection', '',
             f"Archive integrity: passed; format: {kind}; files: {len(entries)}; compressed bytes: {result['archive_bytes']}; expanded bytes: {result['uncompressed_bytes']}",
             f"SHA256: `{result['archive_sha256']}`", '', f"Directory counts: `{json.dumps(groups)}`", '',
             '## Required startup resources absent from this archive level', '', *['- `' + p + '`' for p in result['critical_missing']], '',
             '## Resource containers (inspect their contents next)', '', *['- `' + p + '`' for p in containers], '',
             '## Absent source catalog entries (includes optional libraries)', '', *['- `' + p + '`' for p in missing], '',
             '## Zero-length files', '', *['- `' + p + '`' for p in result['zero_length_files']], '',
             '## Full file inventory', '', '| File | Bytes |', '| --- | ---: |',
             *[f"| `{e['name'].replace('|', '')}` | {e['size']} |" for e in entries]]
    (output / 'resource-report.md').write_text('\n'.join(lines) + '\n')
    print(f"::notice title=Resource archive::Format {kind}; files {len(entries)}; archive bytes {result['archive_bytes']}; expanded bytes {result['uncompressed_bytes']}; integrity passed")
    print('::notice title=Resource directory counts::' + json.dumps(groups))
    print('::notice title=Resource containers::' + '; '.join(containers))
    print('::notice title=Required files absent at archive level::' + '; '.join(result['critical_missing']))
    print(f"::notice title=Source catalog gaps::{len(missing)} optional or required source libraries absent; {len(result['zero_length_files'])} empty files. See summary for complete list.")
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('archive', type=pathlib.Path)
    parser.add_argument('--repository', type=pathlib.Path, default=pathlib.Path('.'))
    parser.add_argument('--output', type=pathlib.Path, default=pathlib.Path('.build/resource-inspection'))
    args = parser.parse_args()
    inspect(args.archive, args.repository, args.output)
