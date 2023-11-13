#!/usr/bin/env bash
echo "Change nginx.conf for default backend"
cp ./nginx/default.conf ./nginx/nginx.conf

echo "Up backend"
docker-compose -f docker-compose.yml -p prup up -d --build

echo "Up Celery"
docker-compose -f docker-compose-celery.yml -p celery up -d --build