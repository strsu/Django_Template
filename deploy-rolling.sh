#!/usr/bin/env bash

# cp ./nginx/nginx_A.conf ./nginx/nginx.conf

# docker-compose -f docker-compose.yml -p prup build backend_a


# docker-compose -f docker-compose.yml -p prup down backend_b

# docker-compose -f docker-compose.yml -p prup exec nginx "nginx reload"

EXIST_A=$(docker-compose -f docker-compose.yml -p prup ps | grep backend_a)

if [ -z "$EXIST_A" ]; then
    echo "Build backend_a"
    docker-compose -f docker-compose.yml -p prup up -d --build backend_a

    sleep 5
    
    echo "Change nginx.conf for backend_a"
    cp ./nginx/nginx_A.conf ./nginx/nginx.conf

    sleep 1

    echo "Reload nginx.conf for backend_a"
    docker-compose -f docker-compose.yml -p prup exec nginx nginx -s reload

    sleep 10

    echo "Down backend_b"
    docker-compose -f docker-compose.yml -p prup down backend_b
else
    echo "Build backend_b"
    docker-compose -f docker-compose.yml -p prup up -d --build backend_b

    sleep 5

    echo "Change nginx.conf for backend_b"
    cp ./nginx/nginx_B.conf ./nginx/nginx.conf

    sleep 1
    
    echo "Reload nginx.conf for backend_b"
    docker-compose -f docker-compose.yml -p prup exec nginx nginx -s reload

    sleep 10

    echo "Down backend_a"
    docker-compose -f docker-compose.yml -p prup down backend_a
fi
