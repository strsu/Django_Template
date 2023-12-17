#!/usr/bin/env bash

python3 init_celery_schedule.py

celery -A config worker --beat --scheduler django --pool prefork --loglevel=info