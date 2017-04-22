"""
Created on 22/04/2017
@author: Aitor Gomez Goiri <aitor@gomezgoiri.net>
"""

from datetime import timedelta
from flask_jwt import JWT, current_identity
from config import configuration

class User(object):
    def __init__(self, username):
        self.id = username
        self.username = username

# Right now we allow any user, TODO: check it in mongodb!
def authenticate(username, password):
    return User(username)

def identity(payload):
    return payload['identity']

def configure_auth(app):
    app.config['SECRET_KEY'] = configuration.get_jwt_secret()
    app.config['JWT_EXPIRATION_DELTA'] = timedelta(minutes=10)
    jwt = JWT(app, authenticate, identity)
    # we could use @ jwt.payload_handler to add more info
