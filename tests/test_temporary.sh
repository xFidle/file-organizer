#!/usr/bin/env bash
set -euo pipefail

rm -rf X Y1 Y2
mkdir -p X Y1 Y2

echo 'tmp\n' > Y1/a.tmp
echo 'swp\n' > Y2/b.swp
echo 'ok\n' > X/normal.txt

python3 src/main.py X Y1 Y2 -t
