#!/bin/bash

# This file is run by Dockerfile.web to start up the web server:

set -euo pipefail

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
APP_ROOT="$(cd "$DIR/.." && pwd)"

main()
{
    cd "$APP_ROOT"

    if is_dev; then
        bin/wait_for_db.py
    fi

    echo 'Running database migrations...'
    set +o pipefail # unless someone knows a way to make yes play nicely with pipefail?
    yes "yes" | python manage.py migrate
    set -o pipefail

    echo 'Booting application...'
    if is_dev; then
        exec python manage.py runserver 0.0.0.0:8000
    else
        check_django_secret
        exec newrelic-admin run-program uwsgi --ini /digitalocean-builder/config/uwsgi.ini
    fi
}

# Return true/success/0 if DEV==true, i.e. we're in dev mode:
is_dev() {
    local dev
    dev="${DEV:-false}"
    dev="${dev,,}" #lowercase
    [ "$dev" == "true" ]
}

check_django_secret()
{
    # Make sure we've specified a key, and not used the insecure default:
    if [ "${DJANGO_SECRET_KEY:-dev}" == "dev" ]; then
        echo "ERROR: You must specify DJANGO_SECRET_KEY."
        echo 'Tip: `pwgen --secure 50` to generate one. :)'
        exit 1
    fi
}

main "$@"
