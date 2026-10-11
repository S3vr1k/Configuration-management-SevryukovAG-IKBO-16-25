#!/bin/sh
set -eu

cd "$(dirname "$0")/.."

./run.sh
./run.sh --vfs fixtures/demo.csv
./run.sh --script scripts/stage2_ok.txt
./run.sh --vfs fixtures/demo.csv --script scripts/stage2_ok.txt