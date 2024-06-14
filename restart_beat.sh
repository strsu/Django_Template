#!/usr/bin/env bash

docker-compose -f docker-compose-celery.yml -p celery exec celery /bin/bash -c "kill -HUP \$(cat beat.pid)"