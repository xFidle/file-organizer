#!/usr/bin/env bash
set -euo pipefail

rm -rf X Y1 Y2
mkdir -p X Y1 Y2

echo > "Y1/file with spaces?.txt"
echo > "Y2/[bad]name#.txt"

python3 src/main.py X Y1 Y2 -m
