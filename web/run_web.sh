#!/bin/sh

pip install -r requirements.txt

./manage.py migrate
gunicorn project.wsgi:application -b 0.0.0.0:8000 -w 2 --reload --timeout 360
