# pull official base image
FROM python:latest

RUN apt-get -y update
RUN apt-get -y install goaccess

RUN rm /etc/goaccess.conf
COPY goaccess.conf /etc/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

RUN pip install --upgrade pip
COPY ./requirements.txt /code/
RUN pip install -r requirements.txt

COPY . /code/
RUN mkdir staticfiles
RUN mkdir mediafiles
RUN mkdir nginx/nginx_logs