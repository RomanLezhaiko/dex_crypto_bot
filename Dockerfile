FROM python:3.11-slim

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt update && apt install \
    build-essential postgresql-client libpq-dev python3-dev -y


COPY ./requirements.txt ./requirements.txt

RUN pip install -r requirements.txt
EXPOSE 8000