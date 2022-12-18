FROM python:3.8

COPY ./requirements.txt /
RUN /usr/local/bin/python -m pip install --upgrade pip && pip install -r ./requirements.txt

WORKDIR /opt/
EXPOSE 8000