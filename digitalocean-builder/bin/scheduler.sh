#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "${DIR}/.."

echo 'Starting scheduler...'
# don't want to create a celerybeat pid file because can cause startup issues... pass in empty str
exec newrelic-admin run-program celery --app=config.celery.APP beat --pidfile=''
