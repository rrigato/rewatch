#! /bin/bash

#exits program immediately if a command is not sucessful
set -e

export PROJECT_NAME="rewatch"
export BUCKET_NAME="${PROJECT_NAME}-app-artifacts"
export DEPLOYMENT_PACKAGE="${PROJECT_NAME}_deployment_package.zip"
export FUNCTION_NAME="${PROJECT_NAME}-reddit-post"



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

if [ -e $DEPLOYMENT_PACKAGE ]; then
    rm $DEPLOYMENT_PACKAGE
fi

zip $DEPLOYMENT_PACKAGE -r $PROJECT_NAME  \
    -x *__pycache__*  --quiet

zip -u $DEPLOYMENT_PACKAGE -j handlers/${PROJECT_NAME}_handler.py  \
    -x *__pycache__* --quiet


# aws s3api put-object --bucket $BUCKET_NAME \
#     --key $DEPLOYMENT_PACKAGE \
#     --body $DEPLOYMENT_PACKAGE \
#     --tagging "cloudformation_managed=no&project=${PROJECT_NAME}&prod=yes"




git push origin master

echo "----------------------"
echo "deployment successful"