FROM python:3.11-slim

# Loglar darhol chiqsin (buferlanmasin), .pyc fayllar yozilmasin
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /usr/src/app/bot

COPY requirements.txt /usr/src/app/bot

RUN pip install --no-cache-dir -r /usr/src/app/bot/requirements.txt

COPY . /usr/src/app/bot
