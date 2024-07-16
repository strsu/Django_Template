#!/usr/bin/env bash

URL="http://localhost:8000/api/swagger/"
STATUS=0

## GREEN, BLUE 결정
EXIST=$(docker-compose -f docker-compose-rolling.yml -p prup ps | grep backend_a)

GREEN=backend_a # 새 버전
BLUE=backend_b # 이전 버전
NGINX_CONF=nginx_B

if [ -z "$EXIST" ]; then
    GREEN=backend_b
    BLUE=backend_a
    NGINX_CONF=nginx_A
fi

## BLUE 올리기
echo "Start $BLUE"
docker-compose -f docker-compose-rolling.yml -p prup start $BLUE

while [ $STATUS -ne 200 ]; do
    STATUS=$(docker-compose -f docker-compose-rolling.yml -p prup exec $BLUE curl -s -o /dev/null -w "%{http_code}" $URL)
    echo -n -e "\r[`date`] Waiting for the server to respond with status 200... Current State : $STATUS"
    sleep 1  # 1초 대기 후 다시 시도합니다. 원하는 대기 시간으로 변경할 수 있습니다.
done

STATUS=0
echo -e "\nChange nginx.conf for $BLUE"
cp ./nginx/$NGINX_CONF.conf ./nginx/nginx_rolling.conf

echo "Reload nginx.conf for $BLUE"
docker-compose -f docker-compose-rolling.yml -p prup exec nginx nginx -s reload

while [ $STATUS -ne 200 ]; do
    STATUS=$(docker-compose -f docker-compose-rolling.yml -p prup exec $BLUE curl -s -o /dev/null -w "%{http_code}" $URL)
    echo -n -e "\r[`date`] Waiting for the server to respond with status 200... Current State : $STATUS"
    sleep 1  # 1초 대기 후 다시 시도합니다. 원하는 대기 시간으로 변경할 수 있습니다.
done

## BLUE 종료, Stop을 하는 이유는 rollback을 하기 위함
echo -e "\nStop $GREEN"
docker-compose -f docker-compose-rolling.yml -p prup stop $GREEN