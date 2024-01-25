#!/usr/bin/env bash

set -euo pipefail

BIN_PATH=$(cd "$(dirname "$0")" >/dev/null; pwd)
readonly BIN_PATH
source "$BIN_PATH"/venv.sh

if ! "$VENV_PATH"/bin/pip3 show -q kbplacer 2>/dev/null 1>&2; then
  "$VENV_PATH"/bin/pip3 install kbplacer
fi

exec "$VENV_PATH"/bin/python3 -m kbplacer "$@"
