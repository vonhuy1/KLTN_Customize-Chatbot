FROM python:3.11

WORKDIR /code
WORKDIR /code/temp
WORKDIR /nltk_data

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN apt-get update && apt-get install -y poppler-utils

RUN mkdir -p /code
RUN mkdir -p /code/temp
RUN mkdir -p /nltk_data

USER root

RUN chmod -R 777 /nltk_data
RUN chmod -R 777 /code
RUN chmod -R 777 /code/temp

COPY ./requirements.txt /code/requirements.txt
COPY ./firebase_certificate.json /code/firebase_certificate.json
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . .


