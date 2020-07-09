# UIOw2T
Project for "Inżynieria Oprogramowania (Software Engineering)" laboratories. It is an auto battler (like for example Teamfight Tactics) created using Python, running as a web application.

# Prerequisites

1. Docker
2. docker-compose

# Usage

## Docker

To run application locally, download source from github
``` sh
git clone https://github.com/Djkusik/UIOw2T.git
```

Then to run app, just type:
``` sh
cd UIOw2T
docker-compose build
docker-compose up
```

## Build from sources

It is possible also to build project by hand without usage of Docker.

### Install requirements
```
python -m pip install -r requirements.prod --upgrade
```

### Run server
```
cd backend
python server.py
```