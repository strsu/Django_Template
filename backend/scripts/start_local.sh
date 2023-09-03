#!/usr/bin/env bash

mkdir -p log

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput --verbosity 0

#nohup service supervisor start & # 이걸 해줘야 supervisor가 정상적으로 동작한다.
supervisord &
python manage.py runserver 0.0.0.0:8000
#gunicorn -c config/gunicorn.conf.py config.wsgi:application