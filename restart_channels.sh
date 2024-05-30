#!/usr/bin/env bash

#docker-compose -f docker-compose.yml -p prup restart channels

docker-compose -f docker-compose.yml -p prup exec channels /bin/bash -c "kill -HUP \$(cat /var/run/supervisord.pid)"