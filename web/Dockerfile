FROM ubuntu:latest
RUN apt-get update -y && apt-get install -y \
  build-essential \
  libsqlite3-dev \
  python-dev \
  python-pip \
  sqlite3
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
