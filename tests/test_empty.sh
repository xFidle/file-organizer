#!/usr/bin/env bash
set -euo pipefail

mkdir -p X Y1 Y2

touch X/e1.txt
touch Y1/e2.txt
touch Y2/e3.txt
echo 'NOT_EMPTY\n' > X/keep.txt

python3 src/main.py --auto-accept X Y1 Y2 -e 
[ ! -e X/e1.txt ]  || exit 1
[ ! -e Y1/e2.txt ] || exit 1
[ ! -e Y2/e3.txt ] || exit 1
[ -f X/keep.txt ]  || exit 1

rm -rf X Y1 Y2
echo "PASS"


