#! /bin/bash

#exits program immediately if a command is not sucessful
set -e

export PROJECT_NAME="rewatch"

source avenv/bin/activate

secret_scan_results=$(detect-secrets scan | \
python3 -c "import sys, json; print(json.load(sys.stdin)['results'])" )

# static scan for security credentials that terminates if any secrets are found
if [ "${secret_scan_results}" != "{}" ]; then
    echo "detect-secrets scan failed"
    exit 125
fi

python -m unittest

deactivate

git push origin master

echo "----------------------"
echo "deployment successful"