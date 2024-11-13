#!/usr/bin/env python3
""" Module of Index views
"""
from flask import Flask, Blueprint, jsonify, abort
from api.v1.views import app_views

# Create a new blueprint for the index views
bp = Blueprint('index', __name__)

app = Flask(__name__)


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status() -> str:
    """ GET /api/v1/status
    Return:
      - the status of the API
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats/', strict_slashes=False)
def stats() -> str:
    """ GET /api/v1/stats
    Return:
      - the number of each objects
    """
    from models.user import User
    stats = {}
    stats['users'] = User.count()
    return jsonify(stats)


@app_views.route('/unauthorized', methods=['GET'], strict_slashes=False)
def unauthorized():
    """This endpoint will trigger a 401 Unauthorized error"""
    abort(401)


# New /forbidden route
@app_views.route('/forbidden', methods=['GET'], strict_slashes=False)
def forbidden():
    """ This endpoint will trigger a 403 Forbidden error """
    abort(403)  # Trigger the 403 Forbidden error