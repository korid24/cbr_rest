FROM python:3.9.0-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /currency && apt-get update && pip install poetry && poetry config virtualenvs.create false
WORKDIR /currency

COPY pyproject.toml /currency/
COPY poetry.lock /currency/
RUN poetry install

COPY . /currency