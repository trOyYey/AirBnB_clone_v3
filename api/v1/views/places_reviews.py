#!/usr/bin/python3
""" review api route"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.place import Place
from models.review import Review
from models.user import User

@app_views.route('/places/<string:place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    """Retrieve reviews objects"""
    p = storage.get(Place, place_id)
    if p is None:
        abort(404)
    reviews = []
    for rev in p.reviews:
        rev.append(rev.to_dict())
    return jsonify(rev)


@app_views.route('/reviews/<string:review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """Retrieve review object"""
    rev = storage.get(Review, review_id)
    if rev is None:
        abort(404)
    return jsonify(rev.to_dict())


@app_views.route('/reviews/<string:review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """deletes a review object"""
    rev = storage.get(Review, review_id)
    if rev is None:
        abort(404)
    rev.delete()
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/places/<string:place_id>/reviews/', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    """create review object"""
    p = storage.get(Place, place_id)
    if p is None:
        abort(404)
    if not request.is_json:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'user_id' not in request.get_json():
        return make_response(jsonify({'error': 'Missing user_id'}), 400)
    dic = request.get_json()
    if not storage.get(User, dic.get("user_id")):
        abort(404)
    if 'text' not in request.get_json():
        return make_response(jsonify({'error': 'Missing text'}), 400)
    dic['place_id'] = place_id
    rev = Review(**dic)
    rev.save()
    return make_response(jsonify(rev.to_dict()), 201)


@app_views.route('/reviews/<string:review_id>', methods=['PUT'],
                 strict_slashes=False)
def put_review(review_id):
    """update review object"""
    rev = storage.get(Review, review_id)
    if rev is None:
        abort(404)
    if not request.is_json:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for attr, val in request.get_json().items():
        if attr not in ['id', 'user_id', 'place_id',
                        'created_at', 'updated_at']:
            setattr(rev, attr, val)
    rev.save()
    return jsonify(rev.to_dict()), 200
