#!/bin/bash
set -euo pipefail

#parse the current git commit hash
COMMIT=$(git rev-parse --short HEAD)

VERSION=$COMMIT

# check for changed files (not untracked files)
if [ -n "$(git diff --shortstat 2> /dev/null | tail -n1)" ]; then
    VERSION="${VERSION}-dirty"
fi

echo $VERSION