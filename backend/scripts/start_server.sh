#!/usr/bin/env bash

mkdir -p log

python manage.py makemigrations # 실제 운영에서는 주석처리 하기!
python manage.py migrate
python manage.py collectstatic --noinput --verbosity 0

# service cron start
# python manage.py crontab add
# python manage.py crontab show

if [ "$WHOAMI" == "prod" ]; then
    gunicorn -c config/gunicorn.conf.py config.wsgi:application
else
    python manage.py runserver 0.0.0.0:8000
fi