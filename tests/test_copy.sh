#!/usr/bin/env bash
set -euo pipefail

test_basic_copy() {
    mkdir -p X Y1
    echo 'CONTENT' > Y1/file.txt

    python3 src/main.py --auto-accept X Y1 -c
    [ -f X/file.txt ] || return 1
    [ "$(cat X/file.txt)" = 'CONTENT' ] || return 1

    rm -rf X Y1
}

test_already_present() {
    mkdir -p X Y1
    echo 'IN_X' > X/file.txt
    echo 'IN_Y' > Y1/file.txt

    python3 src/main.py --auto-accept X Y1 -c
    [ "$(cat X/file.txt)" = 'IN_X' ] || return 1

    rm -rf X Y1
}

test_multiple_y_dirs() {
    mkdir -p X Y1 Y2
    echo 'FROM_Y1' > Y1/a.txt
    echo 'FROM_Y2' > Y2/b.txt

    python3 src/main.py --auto-accept X Y1 Y2 -c
    [ -f X/a.txt ] || return 1
    [ -f X/b.txt ] || return 1

    rm -rf X Y1 Y2
}

test_subdirectory_preserved() {
    mkdir -p X Y1/sub
    echo 'NESTED' > Y1/sub/file.txt

    python3 src/main.py --auto-accept X Y1 -c
    [ -f X/sub/file.txt ] || return 1
    [ "$(cat X/sub/file.txt)" = 'NESTED' ] || return 1

    rm -rf X Y1
}

test_same_name_different_path() {
    mkdir -p X Y1/sub
    echo 'IN_X_ROOT' > X/file.txt
    echo 'IN_Y_SUB' > Y1/sub/file.txt

    python3 src/main.py --auto-accept X Y1 -c
    [ "$(cat X/file.txt)" = 'IN_X_ROOT' ] || return 1
    [ -f X/sub/file.txt ] || return 1
    [ "$(cat X/sub/file.txt)" = 'IN_Y_SUB' ] || return 1

    rm -rf X Y1
}

test_nothing_to_copy() {
    mkdir -p X Y1
    echo 'SAME' > X/file.txt
    echo 'SAME' > Y1/file.txt

    OUTPUT=$(python3 src/main.py --auto-accept X Y1 -c)
    echo "$OUTPUT" | grep -q 'Found 0 files' || return 1
    [ "$(cat X/file.txt)" = 'SAME' ] || return 1

    rm -rf X Y1
}

test_empty_y_dirs() {
    mkdir -p X Y1 Y2
    echo 'EXISTING' > X/keep.txt

    python3 src/main.py --auto-accept X Y1 Y2 -c
    [ -f X/keep.txt ] || return 1

    rm -rf X Y1 Y2
}

test_basic_copy               || exit 1
test_already_present          || exit 1
test_multiple_y_dirs          || exit 1
test_subdirectory_preserved   || exit 1
test_same_name_different_path || exit 1
test_nothing_to_copy          || exit 1
test_empty_y_dirs             || exit 1
