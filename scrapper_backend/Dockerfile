FROM python:3.8-bullseye

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY requirements.txt /code/
COPY . /code/

RUN pip install -r requirements.txt

# Upgrade pip
RUN pip install --upgrade pip

# Install uWSGI
RUN pip install uwsgi

