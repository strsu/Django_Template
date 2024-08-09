#!/usr/bin/env bash

## docker network 생성
docker network create proxynet

RUNNING=$(docker-compose -f docker-compose-slave-rolling.yml -p prup ps -q | wc -l)

## 서비스가 없으면 서비스를 올린다
if [ $RUNNING -eq 0 ] ; then
  docker-compose -f docker-compose-slave-rolling.yml -p prup up -d --build
fi

URL="http://localhost:8000/api/swagger/"
STATUS=0

## GREEN, BLUE 결정
EXIST=$(docker-compose -f docker-compose-slave-rolling.yml -p prup ps | grep backend_b)

GREEN=backend_a # 새 버전
BLUE=backend_b # 이전 버전
NGINX_CONF=nginx_A

if [ -z "$EXIST" ]; then
    GREEN=backend_b
    BLUE=backend_a
    NGINX_CONF=nginx_B
fi

## GREEN 올리기
echo "Build $GREEN"
docker-compose -f docker-compose-slave-rolling.yml -p prup up -d --build $GREEN

echo "Build Complete, Server Start `date`"
while [ $STATUS -ne 200 ]; do
    STATUS=$(docker-compose -f docker-compose-slave-rolling.yml -p prup exec $GREEN curl -s -o /dev/null -w "%{http_code}" $URL)
    echo -n -e "\r[`date`] Waiting for the server to respond with status 200... Current State : $STATUS"
    sleep 1  # 1초 대기 후 다시 시도합니다. 원하는 대기 시간으로 변경할 수 있습니다.
done

STATUS=0
echo -e "\nChange nginx.conf for $GREEN"
cp ./nginx/$NGINX_CONF.conf ./nginx/nginx_rolling.conf

echo "Reload nginx.conf for $GREEN"
docker-compose -f docker-compose-slave-rolling.yml -p prup exec nginx nginx -s reload

while [ $STATUS -ne 200 ]; do
    STATUS=$(docker-compose -f docker-compose-slave-rolling.yml -p prup exec $GREEN curl -s -o /dev/null -w "%{http_code}" $URL)
    echo -n -e "\r[`date`] Waiting for the server to respond with status 200... Current State : $STATUS"
    sleep 1  # 1초 대기 후 다시 시도합니다. 원하는 대기 시간으로 변경할 수 있습니다.
done

## BLUE 종료, Stop을 하는 이유는 rollback을 하기 위함
echo -e "\nStop $BLUE"
docker-compose -f docker-compose-slave-rolling.yml -p prup stop $BLUE