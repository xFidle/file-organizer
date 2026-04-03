#!/usr/bin/env bash
set -euo pipefail

mkdir -p X/sub Y1/sub Y2/sub

echo 'X_VERSION\n' > X/sub/test.log
echo 'Y_VERSION\n' > Y1/sub/test.log
cp Y1/sub/test.log Y2/sub/test.log

python3 src/main.py --auto-accept X Y1 Y2 -d
[ ! -e Y1/sub/test.log ] || exit 1
[ ! -e Y2/sub/test.log ] || exit 1
[ -f X/_dups/test.log ]  || exit 1

[ "$(cat X/sub/test.log)" = 'X_VERSION\n' ]   || exit 1
[ "$(cat X/_dups/test.log)" = "Y_VERSION\n" ] || exit 1

rm -rf X Y1 Y2
echo "PASS"
