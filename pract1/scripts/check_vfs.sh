#!/bin/sh
set -eu
cd "$(dirname "$0")/.."

./run.sh --vfs fixtures/minimal.csv
./run.sh --vfs fixtures/several.csv
./run.sh --vfs fixtures/nested.csv
