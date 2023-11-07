#!/usr/bin/env bash

# cp ./nginx/nginx_A.conf ./nginx/nginx.conf

# docker-compose -f docker-compose.yml -p prup build backend_a


# docker-compose -f docker-compose.yml -p prup down backend_b

# docker-compose -f docker-compose.yml -p prup exec nginx "nginx reload"

EXIST_A=$(docker-compose -f docker-compose.yml -p prup ps | grep backend_a)

if [ -z "$EXIST_A" ]; then
    # A를 올린다
    echo "UP backend_a"
    cp ./nginx/nginx_A.conf ./nginx/nginx.conf

    echo "Build backend_a"
    docker-compose -f docker-compose.yml -p prup up -d --build backend_a
    
    echo "Reload nginx.conf for backend_a"
    docker-compose -f docker-compose.yml -p prup exec nginx nginx -s reload
    
    echo "Down backend_b"
    docker-compose -f docker-compose.yml -p prup down backend_b
else
    echo "UP backend_b"
    cp ./nginx/nginx_B.conf ./nginx/nginx.conf

    echo "Build backend_b"
    docker-compose -f docker-compose.yml -p prup up -d --build backend_b
    
    echo "Reload nginx.conf for backend_b"
    docker-compose -f docker-compose.yml -p prup exec nginx nginx -s reload
    
    echo "Down backend_a"
    docker-compose -f docker-compose.yml -p prup down backend_a
fi
