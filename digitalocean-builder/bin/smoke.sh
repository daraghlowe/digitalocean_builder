#!/usr/bin/env bash

# Called by `make smoke-test` within Docker to run post-deploy smoke tests.

set -u
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
pushd ${DIR}/..

mkdir -p artifacts/
rm -rf artifacts/*

# Specifying file path based on what domain is being used - production or staging.
nosetests --with-xunit --xunit-file=artifacts/smoke-tests-$(echo $SMOKE_DOMAIN | cut -d . -f 1).xml tests/smoke.py
