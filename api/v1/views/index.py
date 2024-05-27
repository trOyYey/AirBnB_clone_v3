#!/usr/bin/python3
"""
indexing
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', methods=['GET'])
def status():
    """ STATUS method """
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'])
def stats():
    """ status counter """
    dictt = {}
    list_c = {
            "Amenity": "amenities",
            "City": "cities",
            "Place": "places",
            "Review": "reviews",
            "State": "states",
            "User": "users"
            }
    for cls, key in list_c.items():
        dictt[key] = storage.count(cls)
    return jsonify(dictt)
