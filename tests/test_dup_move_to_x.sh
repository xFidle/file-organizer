#!/usr/bin/env bash
set -euo pipefail

mkdir -p X Y1/sub Y2/sub

echo 'MOVE_ME\n' > Y1/sub/test.log
cp Y1/sub/test.log Y2/sub/test.log

python3 src/main.py --auto-accept X Y1 Y2 -d
[ ! -e Y2/sub/test.log ] || exit 1
[ -f X/sub/test.log ] || exit 1
[ "$(cat X/sub/test.log)" = 'MOVE_ME\n' ] || exit 1

rm -rf X Y1 Y2
exit 0
