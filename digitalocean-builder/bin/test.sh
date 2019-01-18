#!/usr/bin/env bash

set -euo pipefail

BIN_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DJANGO_ROOT="$( cd "$BIN_DIR/.." && pwd)"

main()
{
    cd "$DJANGO_ROOT"

    # Validate swagger
    "$BIN_DIR/validate_swagger.py"
    echo "Swagger schema validated!"

    "$BIN_DIR/wait_for_db.py"

    export DJANGO_SETTINGS_MODULE=config.settings.test
    export DJANGO_SECRET_KEY=test

    check_migrations

    # TODO: Figure out how to exclude a directory or modules from checking. Generated migration files fail
    #mypy -s apps/
    export COVERAGE_FILE=./artifacts/.coverage
    coverage run ./manage.py test --noinput --with-xunit --xunit-file=artifacts/junit.xml
    coverage html --fail-under=0 #otherwise the specified limit in .coveragerc will prevent the other reports
    coverage xml --fail-under=0
    coverage report -m || die "Test coverage too low! Configured in .coveragerc"
    echo "All tests pass!"
}

# Fail the build if we've forgotten to run `manage.py makemigrations`:
check_migrations()
{
    python manage.py makemigrations --dry-run --check || die 'Did you forget to run `manage.py makemigrations`?'
}

die()
{
    echo "ERROR: $*"
    exit 1
}

main "$@"
