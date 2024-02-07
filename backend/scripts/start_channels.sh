#!/usr/bin/env bash

mkdir -p log

supervisord & # 이렇게 하면 os.environ을 사용할 수 있다, 즉 환경변수 인식이 가능
# service supervisor start # 이걸 해줘야 supervisor가 정상적으로 동작한다. # <- 이 방법은 os 환경변수 인식을 못 한다.
# daphne -b 0.0.0.0 -p 8001 config.asgi:application # <- daphne 실행방법
