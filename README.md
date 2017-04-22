# Webofcomics-backend
Flask based HTTP API for the _Web of comics_ webapp.

## Requisites

The API expects a [MongoDB](https://www.mongodb.com/) server to be running on _localhost:27017_

To run it easily and quickly just use [Docker](https://www.docker.com/):

    docker pull mongo
    docker run -p 27017:27017 --name wocmongo -d mongo

And from that point on just use the _wocmongo_ container which will be listening on _localhost:27017_.

## Configuration

Copy _config.ini.copy_ to __config.ini__ editing the necessary values.

## Running on development mode

    ./run.sh
