#!/usr/bin/env bash

docker-compose -f docker-compose-celery.yml -p prup restart celery
