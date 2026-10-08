#!/usr/bin/env python3
"""Pin Android wire IDs to the compiled repository server's packet metadata."""
import argparse
import json
import pathlib
import runpy

p = argparse.ArgumentParser()
p.add_argument('assembly')
p.add_argument('--report', required=True)
p.add_argument('--order', required=True)
p.add_argument('--check', action='store_true')
a = p.parse_args()
inspector = runpy.run_path(str(pathlib.Path(__file__).with_name('inspect-apk-protocol.py')))
report = inspector['inspect']('Repository server Library.dll', pathlib.Path(a.assembly).read_bytes())
names = '\n'.join(packet['namespace'] + '.' + packet['name'] for packet in report['packets'])
template = pathlib.Path(__file__).resolve().parents[1] / 'Mir3.Mobile/OriginalAndroidPacketOrder.cs'
source = template.read_text(encoding='utf-8')
source = source.replace('#if ANDROID && BUNDLED_RESOURCE_TEST && !REPOSITORY_SERVER_PROTOCOL',
                        '#if ANDROID && BUNDLED_RESOURCE_TEST && REPOSITORY_SERVER_PROTOCOL')
start = source.index('    // Canonical')
end = source.index('    internal static class', start)
source = source[:start] + '    // Generated from the compiled repository server; do not reorder manually.\n' + source[end:]
start = source.index('internal const string WireOrderNames = @"') + len('internal const string WireOrderNames = @"')
end = source.index('";', start)
source = source[:start] + names + source[end:]
source = source.replace('OriginalAndroidPacketOrder', 'RepositoryServerPacketOrder')
source = source.replace('Original Android', 'Repository server').replace('original Android', 'repository server')
output = pathlib.Path(a.order)
if a.check:
    if output.read_text(encoding='utf-8') != source:
        raise ValueError('Pinned packet table differs from freshly compiled repository server')
else:
    output.write_text(source, encoding='utf-8')
pathlib.Path(a.report).write_text(json.dumps([report], separators=(',', ':')), encoding='utf-8')
print('Repository server packet count:', len(report['packets']))
for packet in report['packets']:
    if packet['name'] in ('Login', 'RequestStartGame'):
        print(packet['id'], packet['namespace'] + '.' + packet['name'])
