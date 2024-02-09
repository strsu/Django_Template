#!/usr/bin/env bash

python3 init_celery_schedule.py

cp /opt/supervisor/celery.conf /etc/supervisor/conf.d/celery.conf
supervisord

# celery -A config worker --beat --scheduler django --pool prefork --loglevel=info --loglevel=info --pidfile=/opt/celery.pid
# celery -A config worker restart --pidfile=/opt/celery.pid

# celery multi start 1 -A config --beat --scheduler django --pool prefork --loglevel=info --pidfile=/opt/celery.pid