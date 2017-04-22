#! /bin/bash

export CONFIG='./config.ini'
export FLASK_APP='webofcomics'
export FLASK_DEBUG=true

pip install -e .
flask run
