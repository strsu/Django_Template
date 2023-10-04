FROM python:3.8

# python envs
ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

RUN apt-get update && apt-get install -y supervisor ffmpeg cron
COPY ./conf/daphne.conf /etc/supervisor/conf.d/
COPY ./conf/requirements.txt /
RUN /usr/local/bin/python -m pip install --upgrade pip && pip install -r ./requirements.txt

# supervisor를 foreground로 실행시켜야 컨테이너가 꺼지지 않는다.
RUN echo '[supervisord]'  >> /etc/supervisor/supervisord.conf
RUN echo 'nodaemon=true'  >> /etc/supervisor/supervisord.conf 

WORKDIR /opt/
EXPOSE 8000 8001