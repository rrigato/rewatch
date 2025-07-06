#!/bin/bash

set -e

#setup git config
git config user.name "github_action_bot"
git config user.email "no_email_address"

#puts the static string replace where the second . is
# example
# v1.1.0 -> v1.1replace0
# Get the latest tag sorted by semantic version
current_tag=$(git tag --sort=version:refname | tail -n1 | sed 's/\./replace/2')
echo "current_tag - ${current_tag}"
echo "current_minor_version - ${current_tag##*replace}"

# takes everything after the string 'replace' and adds 1
# v1.1replace0 -> 1
new_minor_version=$((${current_tag##*replace} + 1))
echo "new_minor_version - ${new_minor_version}"

# takes everything before the string 'replace'
# v1.1replace0 -> v1.1
tag_without_minor_version="${current_tag%replace*}."
echo "tag_without_minor_version - ${tag_without_minor_version}"

#concatenates new tag
new_tag=${tag_without_minor_version}${new_minor_version}
echo "new_tag - ${new_tag}"


tag_message="prevent_disable - ${tag_without_minor_version}${new_minor_version}"
echo "tag_message - ${tag_message}"


# only add a tag on the 10th day of the month
if [ $(date +%d) = "10" ]; then

    git tag $new_tag -m "$tag_message"
    echo "added unnecessary tag"

    git push origin $new_tag
    echo "tag addition complete"

fi

git tag