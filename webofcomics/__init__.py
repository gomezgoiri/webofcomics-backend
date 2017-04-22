'''
Created on 05/03/2017
@author: Aitor Gomez Goiri <aitor@gomezgoiri.net>
'''

from flask import Flask, jsonify
from flask_cors import CORS
from werkzeug.exceptions import default_exceptions
from werkzeug.exceptions import HTTPException
from auth import configure_auth

app = Flask(__name__)
if app.debug:
    cors = CORS(app, origins=['http://localhost:3000'])
jwt = configure_auth(app)

'''
Function to allow customizing error description.
'''
def json_http_response(code, message):
    return jsonify(message=message, errorCode=code), code

# http://flask.pocoo.org/snippets/83/
'''
Creates a JSON-oriented Flask app.

All error responses that you don't specifically
manage yourself will have application/json content
type, and will contain JSON like this (just an example):

{ 'message': '405: Method Not Allowed' }
'''
def make_json_error(ex):
    error_code = ex.code if isinstance(ex, HTTPException) else 500
    return json_http_response(error_code, str(ex))

for code in default_exceptions.iterkeys():
    app.errorhandler(code)(make_json_error)

import webofcomics.views
