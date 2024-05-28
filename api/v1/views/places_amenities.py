#!/usr/bin/python3
"""places and amenities link route"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage, storage_t
from models.amenity import Amenity
from models.place import Place


@app_views.route('/places/<string:place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_place_amenities(place_id):
    """Retrieve amenity objects"""
    p = storage.get("Place", place_id)
    if p is None:
        abort(404)
    a = []
    for amenity in p.amenities:
        a.append(amenity.to_dict())

    return jsonify(a)


@app_views.route('/places/<string:place_id>/amenities/<string:amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """deletes amenity object"""
    p = storage.get("Place", place_id)
    a = storage.get("Amenity", amenity_id)
    if p is None or a is None:
        abort(404)
    if a not in p.amenities:
        abort(404)
    if storage_t == "db":
        p.amenities.remove(a)
    else:
        p.amenity_ids.remove(amenity_id)

    p.save()
    return jsonify({})


@app_views.route('/places/<string:place_id>/amenities/<string:amenity_id>',
                 methods=['POST'], strict_slashes=False)
def post_place_amenity(place_id, amenity_id):
    """create amenity object"""
    p = storage.get("Place", place_id)
    a = storage.get("Amenity", amenity_id)
    if p is None or a is None:
        abort(404)
    if a in p.amenities:
        return jsonify(amenity.to_dict())
    if storage_t == "db":
        p.amenities.append(a)
    else:
        if p.amenity_ids:
            p.amenity_ids.append(amenity_id)
        else:
            p.amenity_ids = [amenity_id]
    p.save()
    return make_response(jsonify(a.to_dict()), 201)

