#!/usr/bin/python3
"""states class object"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models.state import State
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def gstates():
    """Retrieves the list of all State"""
    list_s = []
    for state in storage.all("State").values():
        list_s.append(state.to_dict())
    return jsonify(list_s)


@app_views.route('/states/<string:state_id>', methods=['GET'],
                 strict_slashes=False)
def get_state(state_id):
    """Retrieves a State object"""
    s = storage.get(State, state_id)
    if s is None:
        abort(404)
    return jsonify(s.to_dict())


@app_views.route('/states/<string:state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Deletes a State object method"""
    s = storage.get(State, state_id)
    if s is None:
        abort(404)
    s.delete()
    storage.save()
    return (jsonify({}))


@app_views.route('/states/', methods=['POST'], strict_slashes=False)
def post_state():
    """Creates a State method"""
    if not request.is_json:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    state = State(**request.get_json())
    state.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route('/states/<string:state_id>', methods=['PUT'],
                 strict_slashes=False)
def put_state(state_id):
    """updating state method"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.is_json:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for attr, val in request.get_json().items():
        if attr not in ['id', 'created_at', 'updated_at']:
            setattr(state, attr, val)
    state.save()
    return jsonify(state.to_dict())
