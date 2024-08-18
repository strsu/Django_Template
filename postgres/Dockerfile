# PostgreSQL 13 이미지를 기반으로 합니다.
FROM postgres:13

# PostGIS 및 기타 필요한 패키지를 설치합니다.
RUN apt-get update && apt-get install -y \
    postgresql-13-postgis-3 \
    postgresql-13-postgis-3-scripts \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 초기화 스크립트를 사용하여 데이터베이스 생성 시 자동으로 PostGIS를 활성화합니다.
COPY ./initdb-postgis.sh /docker-entrypoint-initdb.d/

# PostgreSQL 컨테이너의 기본 포트
EXPOSE 5432
