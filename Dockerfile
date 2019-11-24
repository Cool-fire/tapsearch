FROM python:3.6

RUN mkdir /app

WORKDIR /app

ADD ./requirements.txt .

RUN python3.6 -m venv /venv \
    && /venv/bin/pip install -r requirements.txt

WORKDIR /app
