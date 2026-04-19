#!/usr/bin/env bash
set -euo pipefail

test_fallback() {
    mkdir -p X/sub Y1/sub Y2/sub

    echo 'X_VERSION\n' > X/sub/test.log
    echo 'Y_VERSION\n' > Y1/sub/test.log
    cp Y1/sub/test.log Y2/sub/test.log

    python3 src/main.py --auto-accept X Y1 Y2 -d
    [ ! -e Y1/sub/test.log ] || return 1
    [ ! -e Y2/sub/test.log ] || return 1
    [ -f X/_dups/test.log ]  || return 1

    [ "$(cat X/sub/test.log)" = 'X_VERSION\n' ]   || return 1
    [ "$(cat X/_dups/test.log)" = "Y_VERSION\n" ] || return 1

    rm -rf X Y1 Y2
    return 0
}

test_keep_in_x() {
    mkdir -p X Y1 Y2

    echo 'SAME\n' > X/a.txt
    cp X/a.txt Y1/a.txt
    cp X/a.txt Y2/a.txt

    python3 src/main.py --auto-accept X Y1 Y2 -d
    [ ! -e Y1/a.txt ] || return 1
    [ ! -e Y2/a.txt ] || return 1
    [ "$(cat X/a.txt)" = 'SAME\n' ] || return 1

    rm -rf X Y1 Y2
    return 0
}

test_move_to_x() {
    mkdir -p X Y1/sub Y2/sub

    echo 'MOVE_ME\n' > Y1/sub/test.log
    cp Y1/sub/test.log Y2/sub/test.log

    python3 src/main.py --auto-accept X Y1 Y2 -d
    [ ! -e Y2/sub/test.log ] || return 1
    [ -f X/sub/test.log ] || return 1
    [ "$(cat X/sub/test.log)" = 'MOVE_ME\n' ] || return 1

    rm -rf X Y1 Y2
    return 0
}

test_fallback  || exit 1
test_keep_in_x || exit 1
test_move_to_x || exit 1
