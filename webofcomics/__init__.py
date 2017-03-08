
from flask import Flask, jsonify
from werkzeug.exceptions import default_exceptions
from werkzeug.exceptions import HTTPException

app = Flask(__name__)

"""
Creates a JSON-oriented Flask app.

All error responses that you don't specifically
manage yourself will have application/json content
type, and will contain JSON like this (just an example):

{ "message": "405: Method Not Allowed" }
"""
def make_json_error(ex):
    error_code = ex.code if isinstance(ex, HTTPException) else 500
    response = jsonify(message=str(ex), status=error_code)
    response.status_code = error_code
    return response


# http://flask.pocoo.org/snippets/83/
for code in default_exceptions.iterkeys():
    app.errorhandler(code)(make_json_error)

import webofcomics.views
