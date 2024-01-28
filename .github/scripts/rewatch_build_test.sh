#!/bin/bash

set -e

python -m venv avenv

source avenv/bin/activate
pip install -r requirements/requirements-dev.txt

secret_scan_results=$(detect-secrets scan | \
python3 -c "import sys, json; print(json.load(sys.stdin)['results'])" )

# static scan for security credentials that terminates if any secrets are found
if [ "${secret_scan_results}" != "{}" ]; then
    echo "detect-secrets scan failed"
    exit 125
fi


python -m unittest