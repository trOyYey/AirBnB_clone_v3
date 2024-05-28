#!/usr/bin/python3
"""city api View"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.city import City
from models.state import State

@app_views.route('/states/<string:state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    """Retrieves the list of all City objects of a State"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    listc = []
    for city in state.cities:
        listc.append(city.to_dict())
    return jsonify(listc)


@app_views.route('/cities/<string:city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city(city_id):
    """retrieves city object"""
    c = storage.get(City, city_id)
    if c is None:
        abort(404)
    return jsonify(c.to_dict())


@app_views.route('/cities/<string:city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """deletes city object"""
    c = storage.get(City, city_id)
    if c is None:
        abort(404)
    c.delete()
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/states/<string:state_id>/cities/', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """creates a city object"""
    s = storage.get(State, state_id)
    if s is None:
        abort(404)
    if not request.is_json:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    dictt = request.get_json()
    dictt['state_id'] = state_id
    c = City(**dictt)
    c.save()
    return make_response(jsonify(c.to_dict()), 201)


@app_views.route('/cities/<string:city_id>', methods=['PUT'],
                 strict_slashes=False)
def put_city(city_id):
    """Update city object"""
    c = storage.get(City, city_id)
    if c is None:
        abort(404)
    if not request.is_json:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for attr, val in request.get_json().items():
        if attr not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(c, attr, val)
    city.save()
    return jsonify(c.to_dict()), 200
