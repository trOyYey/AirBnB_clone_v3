#!/usr/bin/python3
"""
application
"""
from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify
from os import getenv
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

h = getenv('HBNB_API_HOST', '0.0.0.0')
p = getenv('HBNB_API_PORT', 5000)

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_app(exception):
    """calling storage close method after requests"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ returns json 404"""
    return jsonify({'error': 'Not found'}), 404


if __name__ == "__main__":
    """
    application variables
    """
    app.run(host=h, port=p, threaded=True)
