KICAD_PYTHON_PATH="/Applications/KiCad.app/Contents/Frameworks/Python.framework/Versions/Current/bin/python3.9"
if [[ ! -e $KICAD_PYTHON_PATH ]]; then
  echo "$KICAD_PYTHON_PATH is not found." >&2
  exit 1
fi

PROJECT_PATH=$(cd "$(dirname "$0")"/.. >/dev/null; pwd)
VENV_PATH=$PROJECT_PATH/.venv

if [[ ! -d $VENV_PATH ]]; then
  # Use Python provided in KiCad which has required modules such as `pcbnew`.
  "$KICAD_PYTHON_PATH" -m venv --system-site-package "$VENV_PATH"
fi
