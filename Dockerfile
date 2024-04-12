FROM python:3-slim-bookworm

COPY ./workspace /app
WORKDIR /app

RUN pip3 install -r requirements.txt

VOLUME ["/app/visuals"]

ENTRYPOINT python3 main.py