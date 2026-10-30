#!/bin/sh
set -eu

cd "$(dirname "$0")/.."

./run.sh
./run.sh --vfs fixtures/nested.csv
./run.sh --script scripts/stage2_ok.txt
./run.sh --vfs fixtures/nested.csv --script scripts/stage2_ok.txt
