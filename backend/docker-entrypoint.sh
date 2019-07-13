#!/bin/sh
set -eo pipefail

# Check that the database is available
if [ -n "$DB_URL" ]
    then
    echo "Waiting for $DB_URL to be ready"
    while ! mysqladmin ping -h "$DB_URL" -P "$port" --silent; do
        # Show some progress
        echo -n '.';
        sleep 1;
    done
    echo "$DB_URL is ready"
    # Give it another second.
    sleep 1;
fi

exec uwsgi\
    --http '0.0.0.0:8081'\
    --plugin python\
    --wsgi-file backend.py\
    --callable app\
    --processes 4\
    --threads 2\
    --buffer-size 32768\