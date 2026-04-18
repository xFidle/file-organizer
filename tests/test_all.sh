#!/usr/bin/env bash
set -uo pipefail

TESTS_DIR="$(cd "$(dirname "$0")" && pwd)"
failed=0

for test in "$TESTS_DIR"/test_*.sh; do
    [[ "$test" == *test_all.sh ]] && continue
    name="$(basename "$test")"
    if  bash "$test" > /dev/null 2>&1; then
        echo "PASS: $name"
    else
        echo "FAIL: $name"
        failed=$((failed + 1))
     fi
 done

 [ "$failed" -eq 0 ] || exit 1
