#!/usr/bin/env bash
set -euo pipefail

rm -rf X Y1 Y2
mkdir -p X Y1 Y2

echo 'SAME\n' > X/a.txt
cp X/a.txt Y1/a.txt
cp X/a.txt Y2/a.txt

python3 src/main.py X Y1 Y2 -d
