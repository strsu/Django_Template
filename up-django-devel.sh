#!/usr/bin/env bash
echo "Up backend"
docker-compose -f docker-compose-devel.yml -p prup up -d --build