from flask import request, url_for, jsonify, abort
from bson.objectid import ObjectId
from bson.errors import InvalidId

from webofcomics import app
from webofcomics.database import strips

# Vocabulary / terminology
# https://en.wikipedia.org/wiki/Glossary_of_comics_terminology#Panel

@app.route('/')
def index():
    return 'Hello World!'

@app.route('/comics')
def list_comics():
    return 'List comics'

def get_strip_url(strip_id):
    return url_for('get_strip', strip_id=strip_id, _external=True)

def from_db(strip):
    if not strip: abort(404)
    return {
        'url': get_strip_url(strip['_id']),
        'name': strip['name'],
        'image': strip['image']
    }

@app.route('/strips')
def list_strips():
    return jsonify([from_db(s) for s in strips.find()])

@app.route('/strips', methods=['POST'])
def insert_strip():
    return get_strip_url(strips.insert_one(request.json).inserted_id)

@app.route('/strips/<strip_id>')
def get_strip(strip_id):
    try:
        strip = strips.find_one({'_id': ObjectId(strip_id)})
        if (strip):
            return jsonify(from_db(strip))
        abort(404)
    except InvalidId:
        # I do not return 400 because the clients should not be aware of whether
        # the ID is valid according to mongo or not.
        # They should only follow links.
        abort(404)

@app.route('/strips/<strip_id>', methods=['DELETE'])
def delete_strip(strip_id):
    try:
        strip = strips.find_one_and_delete({'_id': ObjectId(strip_id)})
        return jsonify(from_db(strip))
    except InvalidId:
        # I do not return 400 because the clients should not be aware of whether
        # the ID is valid according to mongo or not.
        # They should only follow links.
        abort(404)
