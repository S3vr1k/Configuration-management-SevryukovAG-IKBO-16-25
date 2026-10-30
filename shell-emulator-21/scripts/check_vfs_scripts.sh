#!/bin/sh
set -eu
cd "$(dirname "$0")/.."

./run.sh --vfs fixtures/minimal.csv --script scripts/stage3_ok.txt
./run.sh --vfs fixtures/several.csv --script scripts/stage3_ok.txt
./run.sh --vfs fixtures/nested.csv --script scripts/stage3_ok.txt
./run.sh --vfs fixtures/nested.csv --script scripts/stage3_error.txt
./run.sh --vfs fixtures/nested.csv --script scripts/stage3_exit.txt
./run.sh --vfs fixtures/nested.csv --script scripts/stage3_bad_args.txt
./run.sh --vfs fixtures/nested.csv --script scripts/stage3_bad_quotes.txt
./run.sh --vfs fixtures/nested.csv --script scripts/stage3_bad_exit.txt
