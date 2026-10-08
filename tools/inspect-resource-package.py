#!/usr/bin/env python3
"""Inventory an authorized resource archive; source catalog gaps are not all fatal."""
import argparse
import hashlib
import json
import pathlib
import re
import subprocess
import gzip
import io
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


def inspect_update(archive, repository, output):
    outer = inspect(archive, repository, output / 'outer')
    extracted = output / 'extracted'
    extracted.mkdir(parents=True, exist_ok=True)
    subprocess.run(['7z', 'x', '-y', '-o' + str(extracted), str(archive)], check=True, stdout=subprocess.DEVNULL)
    manifests = list(extracted.rglob('PList.Bin'))
    if len(manifests) != 1:
        raise ValueError('Expected one update manifest, found ' + str(len(manifests)))
    update = manifests[0].parent
    for name in ('APKVersion.bin', 'DataAdd.zip'):
        if not (update / name).is_file():
            raise ValueError('Missing update package file: ' + name)
    scope = __import__('runpy').run_path(str(repository / 'tools/verify-bundled-resources.py'))
    issues = []
    with (update / 'APKVersion.bin').open('rb') as stream:
        version = scope['read_string'](stream)
        scope['read_string'](stream)
        scope['read_length'](stream)
        scope['read_hash'](stream)
        base_name = scope['read_string'](stream)
        expected_length = scope['read_length'](stream)
        expected_hash = scope['read_hash'](stream)
    if base_name != pathlib.PurePosixPath(base_name).name or '\\' in base_name:
        raise ValueError('Invalid manifest base filename')
    base = update / base_name
    actual_length = base.stat().st_size if base.is_file() else None
    actual_hash = None
    if base.is_file():
        with base.open('rb') as stream:
            actual_hash = scope['digest'](stream)
    if actual_length != expected_length:
        issues.append(f'Base ZIP length mismatch: expected {expected_length}, actual {actual_length}')
    if actual_hash != expected_hash:
        issues.append(f'Base ZIP MD5 mismatch: expected {expected_hash.hex()}, actual {actual_hash.hex() if actual_hash else None}')
    patches = []
    verified = 0
    with (update / 'PList.Bin').open('rb') as stream:
        while stream.tell() < (update / 'PList.Bin').stat().st_size:
            name = scope['read_string'](stream)
            length = scope['read_length'](stream)
            checksum = scope['read_hash'](stream)
            patches.append(name)
            patch = update / (name.replace('\\', '-').replace('/', '-') + '.gz')
            if not patch.is_file():
                issues.append('Missing patch: ' + name)
                continue
            if patch.stat().st_size != length:
                issues.append(f'Patch length mismatch: {name}; expected {length}, actual {patch.stat().st_size}')
            try:
                with gzip.open(patch, 'rb') as data:
                    digest = scope['digest'](data)
                if digest != checksum:
                    issues.append('Patch MD5 mismatch: ' + name)
                elif patch.stat().st_size == length:
                    verified += 1
            except Exception as error:
                issues.append(f'Patch decompression failed: {name}; {error}')
    integrity = {'version': version, 'base': base_name, 'expected_bytes': expected_length,
                 'actual_bytes': actual_length, 'expected_md5': expected_hash.hex(),
                 'actual_md5': actual_hash.hex() if actual_hash else None,
                 'patches_verified': verified, 'patches_declared': len(patches), 'issues': issues}
    alternatives = []
    for candidate in (update / 'DataAdd.zip.gz', update / 'Data-DataAdd.zip.gz'):
        if not candidate.is_file():
            continue
        hashed = hashlib.md5()
        size = 0
        try:
            with gzip.open(candidate, 'rb') as stream:
                for block in iter(lambda: stream.read(1024 * 1024), b''):
                    size += len(block)
                    hashed.update(block)
            alternatives.append({'file': candidate.name, 'expanded_bytes': size, 'md5': hashed.hexdigest(),
                                 'matches_manifest': size == expected_length and hashed.digest() == expected_hash})
        except Exception as error:
            alternatives.append({'file': candidate.name, 'error': str(error)})
    integrity['alternative_base_packages'] = alternatives
    (output / 'update-integrity.json').write_text(json.dumps(integrity, indent=2) + '\n')
    try:
        inner = inspect(base, repository, output / 'base')
    except Exception as error:
        issues.append('Base ZIP inspection failed: ' + str(error))
        inner = {'entries': [], 'missing_source_catalog': outer['missing_source_catalog'], 'critical_missing': outer['critical_missing']}
    installed = {normalize(e['name']).lower() for e in inner['entries']}
    installed.update(name.replace('\\', '/').lower() for name in patches)
    missing = [p for p in inner['missing_source_catalog'] if p.replace('\\', '/').lower() not in installed]
    critical = [p for p in inner['critical_missing'] if p.lower() not in installed]
    result = {'outer': {k: v for k, v in outer.items() if k != 'entries'}, 'integrity': integrity,
              'combined_critical_missing': critical, 'combined_source_catalog_missing': missing,
              'base_groups': inner.get('groups'),
              'update_files': [{'name': str(p.relative_to(update)), 'size': p.stat().st_size} for p in update.rglob('*') if p.is_file()]}
    (output / 'combined-report.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    lines = ['# Combined base and update resources', '',
             f"Verified patches: {verified}/{len(patches)}; base bytes expected {expected_length}, actual {actual_length}; base MD5 `{integrity['actual_md5']}`.", '',
             '## Integrity issues', '', *['- ' + issue for issue in issues], '',
             '## Critical files missing after applying all patches', '', *['- `' + p + '`' for p in critical], '',
             '## Source catalog gaps after applying all patches (includes optional libraries)', '', *['- `' + p + '`' for p in missing], '',
             '## Update files', '', *[f"- `{p['name']}` ({p['size']} bytes)" for p in result['update_files']]]
    (output / 'combined-report.md').write_text('\n'.join(lines) + '\n')
    print(f"::notice title=Update package checksums::{verified}/{len(patches)} patches verified; base bytes expected {expected_length}, actual {actual_length}; base MD5 {integrity['actual_md5']}")
    for issue in issues:
        print('::notice title=Resource integrity problem::' + issue)
    print('::notice title=Empty archive files::' + '; '.join(outer['zero_length_files']))
    print('::notice title=Combined critical missing files::' + ('; '.join(critical) or 'None'))
    print(f"::notice title=Combined catalog gaps::{len(missing)} files; includes optional libraries")
    for i in range(0, len(missing), 30):
        print('::notice title=Catalog gap names::' + '; '.join(missing[i:i + 30]))
    for i in range(0, len(result['update_files']), 30):
        print('::notice title=Update file inventory::' + '; '.join(p['name'] for p in result['update_files'][i:i + 30]))
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('archive', type=pathlib.Path)
    parser.add_argument('--repository', type=pathlib.Path, default=pathlib.Path('.'))
    parser.add_argument('--output', type=pathlib.Path, default=pathlib.Path('.build/resource-inspection'))
    args = parser.parse_args()
    inspect(args.archive, args.repository, args.output)
