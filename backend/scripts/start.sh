#!/usr/bin/env bash

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput --verbosity 0

daphne -b 0.0.0.0 -p 8001 config.asgi:application -v2 &
python manage.py runserver 0.0.0.0:8000 -v2

#daphne -b 0.0.0.0 -p 8001 config.asgi:application
#gunicorn -c config/gunicorn.conf.py config.wsgi:application