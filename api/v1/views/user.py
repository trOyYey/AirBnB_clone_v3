#!/usr/bin/python3
"""User api route"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """Retrieve users objects"""
    lis = []
    for user in storage.all(User).values():
        lis.append(user.to_dict())
    return jsonify(lis)


@app_views.route('/users/<string:user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user(user_id):
    """Retrieve user object"""
    u = storage.get(User, user_id)
    if u is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<string:user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """deletes a user object"""
    u = storage.get(User, user_id)
    if u is None:
        abort(404)
    u.delete()
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/users/', methods=['POST'], strict_slashes=False)
def post_user():
    """create user object"""
    if not request.is_json:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'email' not in request.get_json():
        return make_response(jsonify({'error': 'Missing email'}), 400)
    if 'password' not in request.get_json():
        return make_response(jsonify({'error': 'Missing password'}), 400)
    u = User(**request.get_json())
    u.save()
    return make_response(jsonify(u.to_dict()), 201)


@app_views.route('/users/<string:user_id>', methods=['PUT'],
                 strict_slashes=False)
def put_user(user_id):
    """update user object"""
    u = storage.get(User, user_id)
    if u is None:
        abort(404)
    if not request.is_json:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for attr, val in request.get_json().items():
        if attr not in ['id', 'created_at', 'updated_at', 'email']:
            setattr(u, attr, val)
    u.save()
    return jsonify(user.to_dict()), 200
