# UIOw2T
[![Build Status](https://travis-ci.org/Djkusik/UIOw2T.svg?branch=master)](https://travis-ci.org/Djkusik/UIOw2T)  

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

It is possible also to build and run project by hand without usage of Docker.
We suggest using virtualenv for backend python server:

### Creating virtual environment
``` sh
python -m venv env
source env/bin/activate
```

### Install requirements
``` sh
python -m pip install -r backend/requirements.prod --upgrade
```

### Run server
``` sh
cd backend
python server.py
```

In another terminal, starting from root folder of the project:

### Build frontend
``` sh
cd uiow2t-front
yarn
```

### Run frontend
``` sh
yarn start
```
