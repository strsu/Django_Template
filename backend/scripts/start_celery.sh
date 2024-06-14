#!/usr/bin/env bash

mkdir -p log

python3 init_celery_schedule.py

echo "stop"
celery multi stopwait hipri -E -A config --pidfile=/opt/celery_hipri.pid
celery multi stopwait lopri -E -A config --pidfile=/opt/celery_lopri.pid

echo "remove pid files"
rm celery_*.pid

echo "start"
celery multi start hipri -E -A config -Q hipri -P prefork --concurrency=1 -l info --pidfile=/opt/celery_hipri.pid --logfile=/opt/log/hipri.log
celery multi start lopri -E -A config -Q lopri -P prefork --concurrency=2 -l info --pidfile=/opt/celery_lopri.pid --logfile=/opt/log/lopri.log

cp /opt/supervisor/celery.conf /etc/supervisor/conf.d/celery.conf
supervisord

# celery -A config worker --beat --scheduler django --pool prefork --loglevel=info --loglevel=info --pidfile=/opt/celery.pid
# celery -A config worker restart --pidfile=/opt/celery.pid
# celery multi start 1 -A config --beat --scheduler django --pool prefork --loglevel=info --pidfile=/opt/celery.pid