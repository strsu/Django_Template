#!/usr/bin/env bash


# kill -HUP $(cat ./gunicorn.pid)

# docker-compose -f docker-compose-celery.yml -p prup exec -it backend /bin/bash && kill -HUP $(cat /opt/gunicorn.pid)
docker-compose -f docker-compose-celery.yml -p prup exec -it backend /bin/bash -c "kill -HUP \$(cat /opt/gunicorn.pid)"
