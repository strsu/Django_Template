#!/usr/bin/env bash

mkdir log

python manage_local.py makemigrations
python manage_local.py migrate
python manage_local.py collectstatic --noinput --verbosity 0

nohup service supervisor start & # 이걸 해줘야 supervisor가 정상적으로 동작한다.
python manage_local.py runserver 0.0.0.0:8000