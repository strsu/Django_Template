#!/usr/bin/env bash

mkdir -p log

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput --verbosity 0

service cron start
python manage.py crontab add
python manage.py crontab show

supervisord & # 이렇게 하면 os.environ을 사용할 수 있다, 즉 환경변수 인식이 가능
# service supervisor start # 이걸 해줘야 supervisor가 정상적으로 동작한다. # <- 이 방법은 os 환경변수 인식을 못 한다.
# daphne -b 0.0.0.0 -p 8001 config.asgi:application # <- daphne 실행방법

if [ "$WHOAMI" == "prod" ]; then
    gunicorn -c config/gunicorn.conf.py config.wsgi:application
else
    python manage.py runserver 0.0.0.0:8000
fi