FROM python:3.8

RUN apt-get update && apt-get install -y supervisor
COPY ./conf/daphne.conf /etc/supervisor/conf.d/
COPY ./conf/gunicorn.conf /etc/supervisor/conf.d/
COPY ./conf/requirements.txt /
RUN /usr/local/bin/python -m pip install --upgrade pip && pip install -r ./requirements.txt

# supervisor를 foreground로 실행시켜야 컨테이너가 꺼지지 않는다.
RUN echo '[supervisord]'  >> /etc/supervisor/supervisord.conf
RUN echo 'nodaemon=true'  >> /etc/supervisor/supervisord.conf 

WORKDIR /opt/
EXPOSE 8000
EXPOSE 8001