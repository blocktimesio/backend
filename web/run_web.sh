#!/bin/sh

sleep 7s

cd /code/
python manage.py migrate

gunicorn web.wsgi:application -b 0.0.0.0:8000 -w 2 --reload --timeout 360
