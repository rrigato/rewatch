#! /bin/bash

#exits program immediately if a command is not sucessful
set -e

if [ -z "$1" ]; then
    echo "Missing commit message arguement 1"
    exit 1
fi


git add -A

git commit -m "$1"


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

git push origin dev

echo "pushed to remote"

gh pr create --title "$1" \
--body "Automated PR creation" \
--head dev \
--base master

echo "created PR"


echo "----------------------"
echo "deployment successful"