#!/usr/bin/env python3
"""Exercise the real Packet initializer and serializer against the original IDs."""
import argparse
import json
import pathlib
import subprocess
import tempfile
from xml.sax.saxutils import escape


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('original_report')
    parser.add_argument('--dotnet', default='dotnet')
    parser.add_argument('--repository', action='store_true')
    parser.add_argument('--server-assembly', help='Verify IDs against the server actual static Packet initializer')
    args = parser.parse_args()
    reports = json.loads(pathlib.Path(args.original_report).read_text())
    assert len(reports) == 1
    names = [p['namespace'] + '.' + p['name'] for p in reports[0]['packets']]
    root = pathlib.Path(__file__).resolve().parent.parent
    with tempfile.TemporaryDirectory(prefix='mir3-packet-order-') as directory:
        work = pathlib.Path(directory)
        order = 'RepositoryServerPacketOrder' if args.repository else 'OriginalAndroidPacketOrder'
        sources = [root / 'Library/Network/Packet.cs', root / ('Mir3.Mobile/' + order + '.cs')]
        includes = ''.join(f'<Compile Include="{escape(str(p))}" />' for p in sources)
        (work / 'Check.csproj').write_text(
            '<Project Sdk="Microsoft.NET.Sdk"><PropertyGroup>'
            '<OutputType>Exe</OutputType><TargetFramework>net8.0</TargetFramework>'
            '<ImplicitUsings>enable</ImplicitUsings>'
            '<DefineConstants>ANDROID;BUNDLED_RESOURCE_TEST' + (';REPOSITORY_SERVER_PROTOCOL' if args.repository else '') + '</DefineConstants>'
            '</PropertyGroup><ItemGroup>' + includes + '</ItemGroup></Project>')
        # Reverse input order to ensure metadata order cannot change wire IDs.
        fixtures = []
        for name in reversed(names):
            namespace, short = name.rsplit('.', 1)
            properties = ''
            if name == 'Library.Network.ClientPackets.RequestStartGame':
                properties = ('public int CharacterIndex {get;set;}'
                              'public string ClientMACInfo {get;set;}'
                              'public string ClientCPUInfo {get;set;}'
                              'public string ClientHDDInfo {get;set;}')
            fixtures.append(f'namespace {namespace} {{ public sealed class {short} : '
                            f'Library.Network.Packet {{ {properties} }} }}')
        (work / 'Fixtures.cs').write_text('\n'.join(fixtures))
        (work / 'Expected.json').write_text(json.dumps(names))
        program = '''
using Library.Network;
using C = Library.Network.ClientPackets;
using S = Library.Network.ServerPackets;
var expected = System.Text.Json.JsonSerializer.Deserialize<string[]>(File.ReadAllText(args[0]));
if (!Packet.Packets.Select(t => t.FullName).SequenceEqual(expected))
    throw new Exception("Runtime packet IDs differ from original APK.");
var request = new C.RequestStartGame { CharacterIndex = 123456 };
byte[] bytes = request.GetPacketBytes();
int originalId = Array.IndexOf(expected, typeof(C.RequestStartGame).FullName);
int serializedId = (bytes[4] ^ Packet.xorma) | ((bytes[5] ^ Packet.xorma) << 8);
if (bytes.Length != 14 || serializedId != originalId)
    throw new Exception("Wrong serialized start request ID or length.");
var decoded = Packet.ReceivePacket(bytes, out var extra) as C.RequestStartGame;
if (decoded?.CharacterIndex != 123456 || extra.Length != 0)
    throw new Exception("Start request did not round-trip.");
if (Packet.ReceivePacket(new S.RequestStartGame().GetPacketBytes(), out _) is not S.RequestStartGame)
    throw new Exception("Server start reply resolves to wrong direction.");
var reordered = Packet.Packets.AsEnumerable().Reverse().ToList();
OriginalAndroidPacketOrder.Apply(reordered);
if (!reordered.Select(t => t.FullName).SequenceEqual(expected))
    throw new Exception("Packet order depends on metadata enumeration.");
reordered[0] = typeof(string);
try { OriginalAndroidPacketOrder.Apply(reordered); }
catch (InvalidOperationException) {
    Console.WriteLine($"PASS: {expected.Length} runtime IDs, start request bytes, reply direction, metadata order and unknown-type rejection.");
    return;
}
throw new Exception("Unknown packet accepted.");
'''.replace('OriginalAndroidPacketOrder', order)
        if args.server_assembly:
            program = program.replace('var request =', '''
var serverPath = Path.GetFullPath(args[1]);
System.Runtime.Loader.AssemblyLoadContext.Default.Resolving += (context, name) => {
    var dependency = Path.Combine(Path.GetDirectoryName(serverPath)!, name.Name + ".dll");
    return File.Exists(dependency) ? context.LoadFromAssemblyPath(dependency) : null;
};
var server = System.Runtime.Loader.AssemblyLoadContext.Default.LoadFromAssemblyPath(serverPath);
var realNames = ((System.Collections.IEnumerable)server.GetType("Library.Network.Packet")!
    .GetField("Packets")!.GetValue(null)!).Cast<Type>().Select(t => t.FullName);
if (!realNames.SequenceEqual(expected)) throw new Exception("Actual server runtime IDs differ from metadata report.");
var request =''')
        (work / 'Program.cs').write_text(program)
        subprocess.run([args.dotnet, 'run', '--project', str(work / 'Check.csproj'),
                        '--', str(work / 'Expected.json')] +
                       ([str(pathlib.Path(args.server_assembly).resolve())] if args.server_assembly else []), check=True)


if __name__ == '__main__':
    main()
