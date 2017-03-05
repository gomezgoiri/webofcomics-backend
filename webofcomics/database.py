from pymongo import MongoClient

client = MongoClient()
db = client.test_database

# Collections to import from views
strips = db.strips
