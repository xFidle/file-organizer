#!/usr/bin/env bash
set -euo pipefail

test_x_oldest() {
    mkdir -p X Y1

    echo 'SAME\n' > X/logs_x.log
    touch -t 01010101 X/logs_x.log

    echo 'SAME\n' > Y1/logs_y1.log
    touch -t 01010102 Y1/logs_y1.log

    python3 src/main.py --auto-accept X Y1 -d
    [ ! -e Y1/logs_y1.log ] || return 1
    [ "$(cat X/logs_x.log)" = 'SAME\n' ] || return 1

    rm -rf X Y1
    return 0
}

test_y_oldest() {
    mkdir -p X Y1

    echo 'SAME\n' > Y1/logs_y1.log
    touch -t 01010101 Y1/logs_y1.log

    echo 'SAME\n' > X/logs_x.log
    touch -t 01010102 X/logs_x.log

    python3 src/main.py --auto-accept X Y1 -d
    [ ! -e X/logs_x.log ] || return 1
    [ "$(cat Y1/logs_y1.log)" = 'SAME\n' ] || return 1

    rm -rf X Y1
    return 0
}

test_multiple_oldest_wins() {
    mkdir -p X Y1 Y2

    echo 'SAME\n' > X/logs_x.log
    touch -t 01010101 X/logs_x.log

    echo 'SAME\n' > Y1/logs_y1.log
    touch -t 01010102 Y1/logs_y1.log

    echo 'SAME\n' > Y2/logs_y2.log
    touch -t 01010103 Y2/logs_y2.log

    python3 src/main.py --auto-accept X Y1 Y2 -d
    [ ! -e Y1/logs_y1.log ] || return 1
    [ ! -e Y2/logs_y2.log ] || return 1
    [ "$(cat X/logs_x.log)" = 'SAME\n' ] || return 1

    rm -rf X Y1 Y2
    return 0
}

test_x_oldest             || exit 1
test_y_oldest             || exit 1
test_multiple_oldest_wins || exit 1
