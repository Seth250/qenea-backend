#!/bin/sh

# stops the execution if a command during the execution has an error
set -e

python manage.py migrate --noinput

gunicorn qenea_backend.asgi --bind 0.0.0.0 --worker-class uvicorn.workers.UvicornWorker \
    --workers 4 --log-file -