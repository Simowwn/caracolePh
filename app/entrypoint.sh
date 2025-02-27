#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -o errexit
# Exit if any of the intermediate steps in a pipeline fails.
set -o pipefail
# Exit if trying to use an uninitialized variable.
set -o nounset

python manage.py makemigrations
python manage.py migrate
python manage.py create_default_superuser
python manage.py collectstatic --no-input --clear

echo "Finish running python manage.py commands."

exec "$@"