FROM python:3.7

WORKDIR /code

RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -y sqlite3 libsqlite3-dev

COPY wait-for-it.sh /tmp/
COPY requirements.txt /tmp/
EXPOSE 8888

RUN pip install -r /tmp/requirements.txt

# COPY winter winter
