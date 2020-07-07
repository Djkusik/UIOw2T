FROM python:latest

RUN useradd server

WORKDIR /home/server

COPY requirements.prod requirements.prod
RUN pip install -r requirements.prod --upgrade

COPY backend backend

RUN chown -R server:server ./

WORKDIR /home/server/backend
USER server

EXPOSE 8080
CMD python server.py
