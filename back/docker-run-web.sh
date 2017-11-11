#!/bin/sh

sleep 10s

./manage.py migrate
./manage.py collectstatic --noinput
./manage.py loaddata project/fixtures/*.json

gunicorn project.wsgi:application -w 2 --log-level=info \
            --reload -b=unix:/app/run/gunicorn.socket \
            --error-logfile=/app/logs/gunicorn-error.log \
            --access-logfile=/app/logs/gunicorn-access.log
