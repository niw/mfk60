#!/usr/bin/env bash

BIN_PATH=$(cd "$(dirname "$0")" >/dev/null; pwd)
source "$BIN_PATH"/venv.sh

exec "$VENV_PATH"/bin/python3 "$@"
