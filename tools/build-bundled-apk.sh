#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 1 ]; then
  echo "Usage: bash tools/build-bundled-apk.sh /absolute/resource-directory [additional dotnet properties...]" >&2
  exit 2
fi
resource_dir=$(cd "$1" && pwd)
shift
repo_dir=$(cd "$(dirname "$0")/.." && pwd)
for required in Data.zip LocalUpdate/DataAdd.zip LocalUpdate/PList.Bin LocalUpdate/APKVersion.bin; do
  test -f "$resource_dir/$required" || { echo "Missing resource: $required" >&2; exit 1; }
done
cd "$repo_dir"
dotnet build Mir3.Droid/Mir3.Droid.csproj -c Release -f net8.0-android \
  -p:AndroidPackageFormat=apk \
  -p:BundledResourceDirectory="$resource_dir" \
  "$@"
