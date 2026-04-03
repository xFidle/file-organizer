#!/usr/bin/env bash
set -euo pipefail

mkdir -p X Y1 Y2

echo > "Y1/file with spaces?.txt"
echo > "Y2/[bad]name#.txt"

python3 src/main.py --auto-accept X Y1 Y2 -m 
[ -f Y1/file_with_spaces_.txt ]  || exit 1
[ -f Y2/_bad_name_.txt ]  || exit 1

rm -rf X Y1 Y2
echo "PASS"
