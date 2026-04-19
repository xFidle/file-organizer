#!/usr/bin/env bash
set -euo pipefail

test_y_newer() {
    mkdir -p X Y1

    echo 'OLD\n' > X/report.txt
    echo 'NEW\n' > Y1/report.txt

    python3 src/main.py --auto-accept X Y1 -s
    [ ! -e Y1/report.txt ] || return 1
    [ "$(cat X/report.txt)" = 'NEW\n' ] || return 1

    rm -rf X Y1
    return 0
}

test_x_newer() {
    mkdir -p X Y1

    echo 'OLD\n' > Y1/report.txt
    echo 'NEW\n' > X/report.txt

    python3 src/main.py --auto-accept X Y1 -s
    [ ! -e Y1/report.txt ] || return 1
    [ "$(cat X/report.txt)" = 'NEW\n' ] || return 1

    rm -rf X Y1
    return 0
}

test_multiple_y_newest_wins() {
    mkdir -p X Y1 Y2

    echo 'OLD\n' > X/data.txt
    echo 'MIDDLE\n' > Y1/data.txt
    echo 'NEWEST\n' > Y2/data.txt

    python3 src/main.py --auto-accept X Y1 Y2 -s
    [ ! -e Y1/data.txt ] || return 1
    [ ! -e Y2/data.txt ] || return 1
    [ "$(cat X/data.txt)" = 'NEWEST\n' ] || return 1

    rm -rf X Y1 Y2
    return 0
}

test_y_newer                || exit 1
test_x_newer                || exit 1
test_multiple_y_newest_wins || exit 1
