"""
Created on 05/03/2017
@author: Aitor Gomez Goiri <aitor@gomezgoiri.net>
"""

from pymongo import MongoClient

client = MongoClient()
db = client.test_database

# Collections to import from views
strips = db.strips
