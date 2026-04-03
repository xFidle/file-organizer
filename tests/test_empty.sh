#!/usr/bin/env bash
set -euo pipefail

rm -rf X Y1 Y2
mkdir -p X Y1 Y2

touch X/e1.txt
touch Y1/e2.txt
touch Y2/e3.txt
echo 'NOT_EMPTY\n' > X/keep.txt

python3 src/main.py X Y1 Y2 -e
