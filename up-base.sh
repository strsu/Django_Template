#!/usr/bin/env bash
echo "Up Base"
docker-compose -f docker-compose-base.yml -p base up -d --build