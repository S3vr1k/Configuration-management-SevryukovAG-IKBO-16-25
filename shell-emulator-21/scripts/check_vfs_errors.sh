#!/bin/sh
set -eu
cd "$(dirname "$0")/.."

./run.sh --vfs fixtures/missing.csv
./run.sh --vfs fixtures/invalid.csv
./run.sh --vfs fixtures/invalid_base64.csv
./run.sh --vfs fixtures/invalid_parent.csv
