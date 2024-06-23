#!/usr/bin/env bash

# docker-compose -f docker-compose-celery.yml -p celery exec celery /bin/bash -c "python3 manage.py celery_worker_v2 action"
docker-compose -f docker-compose-celery.yml -p celery exec celery /bin/bash -c "sh ./scripts/restart_celery.sh"