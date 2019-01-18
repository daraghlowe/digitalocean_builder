#!/bin/bash

###
# Start a Django Celery worker process.
###

set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "${DIR}/.."

echo 'Starting worker...'
exec newrelic-admin run-program celery worker --app=config.celery.APP
