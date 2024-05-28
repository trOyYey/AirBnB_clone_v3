#!/usr/bin/python3
"""hey"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage, storage_t
from models.state import State
from models.city import City
from models.user import User
from models.place import Place


@app_views.route('/cities/<string:city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """Retrieve places objects within city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    p = []
    for place in city.places:
        p.append(place.to_dict())
    return jsonify(p)


@app_views.route('/places/<string:place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """Retrieve place object"""
    p = storage.get(Place, place_id)
    if p is None:
        abort(404)
    return jsonify(p.to_dict())


@app_views.route('/places/<string:place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes place object"""
    p = storage.get(Place, place_id)
    if p is None:
        abort(404)
    p.delete()
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/cities/<string:city_id>/places/', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """creates a place object"""
    c = storage.get(City, city_id)
    if c is None:
        abort(404)
    if not request.is_json:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'user_id' not in request.get_json():
        return make_response(jsonify({'error': 'Missing user_id'}), 400)
    dic = request.get_json()
    if not storage.get(User, dic.get("user_id")):
        abort(404)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    dic['city_id'] = city_id
    p = Place(**dic)
    p.save()
    return make_response(jsonify(p.to_dict()), 201)


@app_views.route('/places/<string:place_id>', methods=['PUT'],
                 strict_slashes=False)
def put_place(place_id):
    """Update place object"""
    p = storage.get(Place, place_id)
    if p is None:
        abort(404)
    if not request.is_json:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for attr, val in request.get_json().items():
        if attr not in ['id', 'user_id', 'created_at', 'updated_at']:
            setattr(p, attr, val)
    p.save()
    return jsonify(place.to_dict()), 200
