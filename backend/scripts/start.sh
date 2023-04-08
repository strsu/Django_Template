#!/usr/bin/env bash

mkdir log

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput --verbosity 0

service supervisor start # 이걸 해줘야 supervisor가 정상적으로 동작한다.

#supervisorctl reread
#supervisorctl update

#supervisorctl start gunicorn
#supervisorctl start daphne

#daphne -b 0.0.0.0 -p 8001 config.asgi:application -v2 &
#python manage.py runserver 0.0.0.0:8000 #-v2

#gunicorn -c config/gunicorn.conf.py config.wsgi:application &&
#daphne -b 0.0.0.0 -p 8001 config.asgi:application