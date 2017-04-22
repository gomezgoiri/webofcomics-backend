"""
Created on 05/03/2017
@author: Aitor Gomez Goiri <aitor@gomezgoiri.net>
"""

from flask import request, abort, url_for, jsonify, make_response
from flask_jwt import jwt_required, current_identity

from bson.objectid import ObjectId
from bson.errors import InvalidId

# For Etag
# https://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html#sec14.24
import hashlib

from webofcomics import app, json_http_response
from webofcomics.database import strips

# Vocabulary / terminology
# https://en.wikipedia.org/wiki/Glossary_of_comics_terminology#Panel

@app.route('/')
def index():
    return 'Hello World!'

@app.route('/user')
@jwt_required()
def get_username():
    return jsonify('%s' % current_identity)

@app.route('/comics')
def list_comics():
    return 'List comics'

def get_strip_url(strip_id):
    return url_for('get_strip', strip_id=strip_id, _external=True)

def from_db(strip):
    if not strip: abort(404)
    ret = {k: v for (k, v) in strip.iteritems() if k not in ('etag', '_id')}
    ret['url'] = get_strip_url(strip['_id'])
    return ret, None if 'etag' not in strip else strip['etag']

def calculate_etag(strip):
    data = ''
    for k in sorted(strip.keys()):
        if k not in ('etag', 'lastModified'):
            data += strip[k] + ','
    return hashlib.md5(data).hexdigest()

@app.route('/strips')
def list_strips():
    def from_db_without_etag(strip):
        ret, _ = from_db(s)
        return ret
    return jsonify([from_db_without_etag(s) for s in strips.find()])

@app.route('/strips', methods=['POST'])
@jwt_required()
def insert_strip():
    return get_strip_url(strips.insert_one(request.json).inserted_id)

@app.route('/strips/<strip_id>')
def get_strip(strip_id):
    try:
        strip = strips.find_one({'_id': ObjectId(strip_id)})

        # We probably do not gain anything in terms of performance
        # using the etag in the GET and taking it from the same DB
        # as the normal response, but let's consider it for fun anyway.
        header_etag = request.headers.get('If-None-Match')
        if header_etag:
            if header_etag == '*' or header_etag == strip['etag']:
                resp, _ = json_http_response('Not modified', 304)
                resp.headers['ETag'] = strip['etag']
                return (resp, 304)

        if strip:
            strip, etag = from_db(strip)
            resp = jsonify(strip)
            if etag:
                resp.headers['ETag'] = etag
            return resp

        abort(404)
    except InvalidId:
        # I do not return 400 because the clients should not be aware of whether
        # the ID is valid according to mongo or not.
        # They should only follow links.
        abort(404)

@app.route('/strips/<strip_id>', methods=['DELETE'])
@jwt_required()
def delete_strip(strip_id):
    try:
        header_etag = request.headers.get('If-None-Match')
        strip = strips.find_one_and_delete({
            '_id': ObjectId(strip_id),
            'etag': header_etag
        })
        if strip:
            return jsonify(from_db(strip))
        else:
            strip_exists = strips.find_one({
                '_id': ObjectId(strip_id)
            })
            if strip_exists:
                abort(412)
            else:
                abort(404)
    except InvalidId:
        # I do not return 400 because the clients should not be aware of whether
        # the ID is valid according to mongo or not.
        # They should only follow links.
        abort(404)

@app.route('/strips/<strip_id>', methods=['PUT'])
@jwt_required()
def update_strip(strip_id):
    try:
        strip, etag = from_db(strips.find_one({'_id': ObjectId(strip_id)}))
        if strip:
            header_etag = request.headers.get('If-Match')
            if not etag:
                return json_http_response(400, 'An If-Match header is expected')
            else:
                if header_etag != etag:
                    abort(412)
                else:
                    # In the future do it over the modification object
                    etag = calculate_etag(strip)
                    update_result = strips.update_one(
                        { '_id': ObjectId(strip_id) },
                        {
                            '$currentDate': { 'lastModified': True},
                            '$set': {'etag': etag}
                        }
                    )
                    if update_result.acknowledged:
                        return get_strip(strip_id)
        abort(404)
    except InvalidId:
        # I do not return 400 because the clients should not be aware of whether
        # the ID is valid according to mongo or not.
        # They should only follow links.
        abort(404)
