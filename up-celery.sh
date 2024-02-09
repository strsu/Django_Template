#!/usr/bin/env bash

echo "Up Celery"
docker-compose -f docker-compose-celery.yml -p celery up -d --build
