#!/usr/bin/env bash

if docker-compose -f docker-compose.yml -p prup exec backend /bin/bash -c "python3 manage.py test api/v1/*/tests"; then
    echo Success;
else
    echo Fail;
fi