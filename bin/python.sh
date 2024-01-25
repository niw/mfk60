#!/usr/bin/env bash

set -euo pipefail

BIN_PATH=$(cd "$(dirname "$0")" >/dev/null; pwd)
readonly BIN_PATH
source "$BIN_PATH"/venv.sh

exec "$VENV_PATH"/bin/python3 "$@"
