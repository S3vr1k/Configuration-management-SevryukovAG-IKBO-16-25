#!/bin/sh
set -eu

cd "$(dirname "$0")/.."

./run.sh
./run.sh --vfs "fixtures/my vfs.csv"
./run.sh --script scripts/missing.txt
./run.sh --vfs fixtures/nested.csv --script scripts/stage2_error.txt
