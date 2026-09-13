#!/bin/bash
set -euo pipefail

PROJECT_NAME="${PROJECT_NAME:-rewatch}"
DEPLOYMENT_PACKAGE="${DEPLOYMENT_PACKAGE:-${PROJECT_NAME}_deployment_package.zip}"

# Build from an empty directory so removed files cannot survive a redeploy.
build_dir=$(mktemp -d)
trap 'rm -rf "$build_dir"' EXIT
python -m pip install -r requirements/requirements-prod.txt --target "$build_dir"
cp -R "$PROJECT_NAME" "$build_dir/"
cp "handlers/${PROJECT_NAME}_handler.py" "$build_dir/"
python - "$build_dir" "$DEPLOYMENT_PACKAGE" <<'PY'
from pathlib import Path
import sys
from zipfile import ZIP_DEFLATED, ZipFile

source = Path(sys.argv[1])
with ZipFile(sys.argv[2], "w", ZIP_DEFLATED) as archive:
    for path in sorted(source.rglob("*")):
        if path.is_file() and "__pycache__" not in path.parts and path.suffix != ".pyc":
            archive.write(path, path.relative_to(source))
PY
