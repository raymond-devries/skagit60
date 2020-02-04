# pull official base image
FROM python:latest

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

RUN pip install --upgrade pip
COPY ./requirements.txt /code/
RUN pip install -r requirements.txt

COPY . /code/
RUN mkdir staticfiles
RUN mkdir mediafiles

RUN python manage.py migrate
RUN python manage.py import_peaks
RUN python manage.py import_emails
RUN python manage.py collectstatic