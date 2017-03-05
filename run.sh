#! /bin/bash

export FLASK_APP='webofcomics'
export FLASK_DEBUG=true

pip install -e .
flask run
