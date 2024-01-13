#!/usr/bin/env bash

BIN_PATH=$(cd "$(dirname "$0")" >/dev/null; pwd)
source "$BIN_PATH"/venv.sh

if ! "$VENV_PATH"/bin/pip3 show -q kikit 2>/dev/null 1>&2; then
  "$VENV_PATH"/bin/pip3 install kikit
fi

exec "$VENV_PATH"/bin/kikit "$@"
