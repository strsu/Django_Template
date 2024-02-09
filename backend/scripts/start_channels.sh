#!/usr/bin/env bash

mkdir -p log

#supervisord로 서비스를 올려야 os.environ을 사용할 수 있다, 즉 환경변수 인식이 가능, & <- 백그라운드로 실행시키면 안된다

cp /opt/supervisor/daphne.conf /etc/supervisor/conf.d/dapnhe.conf
supervisord

# service supervisor start # 이걸 해줘야 supervisor가 정상적으로 동작한다. # <- 이 방법은 os 환경변수 인식을 못 한다.
# daphne -b 0.0.0.0 -p 8001 config.asgi:application # <- daphne 실행방법
