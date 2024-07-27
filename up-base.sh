#!/usr/bin/env bash
echo "Up Base"
docker network create proxynet
#docker network inspect proxynet
docker-compose -f docker-compose-base.yml -p base up -d --build