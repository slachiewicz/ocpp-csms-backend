FROM python:3.11.3-slim-bullseye

RUN apt-get update && apt-get install -y build-essential

RUN mkdir -p /usr/src/csms
WORKDIR /usr/src/csms

COPY ./src /usr/src/csms
RUN pip install --no-cache-dir -r /usr/src/csms/requirements.txt
