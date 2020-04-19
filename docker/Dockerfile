FROM python:3.7

WORKDIR /code

COPY requirements.txt /tmp/
EXPOSE 8888

RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -y sqlite3 libsqlite3-dev

RUN pip install -r /tmp/requirements.txt

# COPY winter winter

CMD ["python", "-m", "winter"]
