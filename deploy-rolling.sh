#!/usr/bin/env bash

# cp ./nginx/nginx_A.conf ./nginx/nginx.conf

# docker-compose -f docker-compose-rolling.yml -p prup up -d --build


# docker-compose -f docker-compose.yml -p prup down backend_b

# docker-compose -f docker-compose.yml -p prup exec nginx "nginx reload"

URL="http://localhost:8000/api/swagger/"
STATUS=0

EXIST=$(docker-compose -f docker-compose-rolling.yml -p prup ps | grep backend_b)

GREEN=backend_a # 새 버전
BLUE=backend_b # 이전 버전
NGINX_CONF=nginx_A

if [ -z "$EXIST" ]; then
    GREEN=backend_b
    BLUE=backend_a
    NGINX_CONF=nginx_B
fi

echo "Build $GREEN"
docker-compose -f docker-compose-rolling.yml -p prup up -d --build $GREEN

echo "Build Complete, Server Start"
while [ $STATUS -ne 200 ]; do
    echo "Waiting for the server to respond with status 200..."
    STATUS=$(docker-compose -f docker-compose-rolling.yml -p prup exec $GREEN curl -s -o /dev/null -w "%{http_code}" $URL)
    echo $STATUS
    sleep 1  # 1초 대기 후 다시 시도합니다. 원하는 대기 시간으로 변경할 수 있습니다.
done

STATUS=0
echo "Change nginx.conf for $GREEN"
cp ./nginx/$NGINX_CONF.conf ./nginx/nginx_rolling.conf

echo "Reload nginx.conf for $GREEN"
docker-compose -f docker-compose-rolling.yml -p prup exec nginx nginx -s reload

while [ $STATUS -ne 200 ]; do
    echo "Waiting for the server to respond with status 200..."
    STATUS=$(docker-compose -f docker-compose-rolling.yml -p prup exec $GREEN curl -s -o /dev/null -w "%{http_code}" $URL)
    echo $STATUS
    sleep 1  # 1초 대기 후 다시 시도합니다. 원하는 대기 시간으로 변경할 수 있습니다.
done

echo "Down $BLUE"
docker-compose -f docker-compose-rolling.yml -p prup down $BLUE