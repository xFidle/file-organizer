#!/usr/bin/env bash
set -euo pipefail

rm -rf X Y1 Y2
mkdir -p X Y1 Y2

echo "X_FILE" > X/p1.txt
echo "Y1_FILE" > Y1/p2.txt
echo "Y2_FILE" > Y2/p3.txt

chmod 777 Y1/p2.txt || true
chmod 600 Y2/p3.txt || true

python3 src/main.py X Y1 Y2 -p
