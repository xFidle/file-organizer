#!/usr/bin/env bash
set -euo pipefail

mkdir -p X Y1 Y2

echo 'SAME\n' > X/a.txt
cp X/a.txt Y1/a.txt
cp X/a.txt Y2/a.txt

python3 src/main.py --auto-accept X Y1 Y2 -d
[ ! -e Y1/a.txt ] || exit 1
[ ! -e Y2/a.txt ] || exit 1
[ "$(cat X/a.txt)" = 'SAME\n' ] || exit 1

rm -rf X Y1 Y2
echo "PASS"
