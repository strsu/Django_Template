#!/usr/bin/env bash

#python manage.py makemigrations
#python manage.py migrate
python manage.py collectstatic --noinput --verbosity 0
python manage.py runserver 0.0.0.0:8000

#gunicorn -c config/gunicorn.conf.py config.wsgi:application