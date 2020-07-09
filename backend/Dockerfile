FROM python:latest

RUN useradd server

WORKDIR /home/server

COPY requirements.prod requirements.prod
RUN pip install -r requirements.prod --upgrade

COPY api api
COPY game game
COPY battle_test.py client.py server.py ./

RUN chown -R server:server ./

USER server