#!/usr/bin/python3
'''
Create a route `/status` on the object app_views.
'''

from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from api.v1.views import app_views

classes = {'amenities': Amenity, 'cities': City,
           'places': Place, 'reviews': Review,
           'states': State, 'users': User}


@app_views.route('/status', strict_slashes=False, methods=['GET'])
def get_status():
    """get the status code"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False, methods=['GET'])
def get_count():
    """retrieves the number of each objects by type"""

    objs = {}
    for k, v in classes.items():
        objs[k] = storage.count(v)

    return jsonify(objs)
