"""
Created on 21/04/2017
@author: Aitor Gomez Goiri <aitor@gomezgoiri.net>
"""

import ConfigParser
import os


class ConfigFileReader(object):

    def __init__(self):
        self.config = ConfigParser.RawConfigParser()
        self.set_file_path(os.environ.get('CONFIG'))

    def set_file_path(self, file_path):
        if file_path:  # Ignore if it is None
            self.config.read(file_path)

    def get_jwt_secret(self):
        return self.config.get('JWT', 'secret')


configuration = ConfigFileReader()
