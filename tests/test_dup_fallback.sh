#!/usr/bin/env bash
set -euo pipefail

rm -rf X Y1 Y2
mkdir -p X/sub Y1/sub Y2/sub

echo 'X_VERSION\n' > X/sub/test.log
echo 'Y_VERSION\n' > Y1/sub/test.log
cp Y1/sub/test.log Y2/sub/test.log

python3 src/main.py X Y1 Y2 -d
