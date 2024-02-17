#!/bin/bash

set -e

aws lambda invoke \
    --function-name "${PROJECT_NAME}-handler" \
    --cli-binary-format raw-in-base64-out \
    --payload '{}' \
    --region $REGION_NAME \
    --no-cli-pager

