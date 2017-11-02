#!/bin/sh

sleep 10s

./manage.py migrate
./manage.py collectstatic --noinput

gunicorn project.wsgi:application -w 2 --reload -b=unix:/app/run/gunicorn.socket
