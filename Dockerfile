FROM python:3.6
ENV PYTHONUNBUFFERED 1

# Installing OS Dependencies
RUN apt-get update && apt-get upgrade -y && apt-get install -y libsqlite3-dev
RUN pip install -U pip setuptools

RUN mkdir /my_app
WORKDIR /my_app

RUN mkdir /my_app/_requirements
COPY /my_app/_requirements /my_app/_requirements
RUN pip install -r _requirements/development.txt

ADD /my_app /my_app

# Django service
EXPOSE 8000
