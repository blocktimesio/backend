#!/bin/sh

sleep 10s

celery -A project worker --beat --loglevel=info \
                        --pidfile="run/celery.pid" \
                        --logfile="logs/celery.log" \
                        --schedule="run/celerybeat-schedule"