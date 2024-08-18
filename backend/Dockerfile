FROM python:3.12.4-slim

# python envs
ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

# COPY ./conf/daphne.conf /etc/supervisor/conf.d/
# COPY ./conf/celery.conf /etc/supervisor/conf.d/
# COPY ./requirements.txt /


# postgresql, postgis
# HTML to PDF Lib
RUN apt-get update --fix-missing && apt-get install -y \
    supervisor ffmpeg cron unzip curl \
    binutils libpq-dev gcc libproj-dev gdal-bin \
    wkhtmltopdf xvfb fontconfig

COPY . /opt/
RUN /usr/local/bin/python -m pip install --upgrade pip && pip install -r ./opt/requirements.txt

# chromiun 등 설치
RUN playwright install

# HTML to PDF Lib
COPY ./SpoqaHanSansNeo_all.zip /usr/share/fonts/
RUN unzip /usr/share/fonts/SpoqaHanSansNeo_all.zip -d /usr/share/fonts/
RUN fc-cache -f -v

# supervisor를 foreground로 실행시켜야 컨테이너가 꺼지지 않는다.
RUN echo '[supervisord]'  >> /etc/supervisor/supervisord.conf
RUN echo 'nodaemon=true'  >> /etc/supervisor/supervisord.conf 

WORKDIR /opt/
EXPOSE 8000 8001