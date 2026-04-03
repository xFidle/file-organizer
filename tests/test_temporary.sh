#!/usr/bin/env bash
set -euo pipefail

mkdir -p X Y1 Y2

echo 'tmp\n' > Y1/a.tmp
echo 'swp\n' > Y2/b.swp
echo 'ok\n' > X/normal.txt

python3 src/main.py --auto-accept X Y1 Y2 -t 
[ ! -e Y1/a.tmp ]   || exit 1
[ ! -e Y2/b.swp ]   || exit 1
[ -f X/normal.txt ] || exit 1

rm -rf X Y1 Y2
echo "PASS"
