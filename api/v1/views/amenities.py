#!/usr/bin/python3
"""Defining the amenities module"""

from flask import abort, jsonify, make_response, request

from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route(
        '/amenities', methods=['GET'],
        strict_slashes=False)
def get_amenities():
    """get all Amenities objects"""
    objs = []

    for obj in storage.all(Amenity).values():
        objs.append(obj.to_dict())

    return jsonify(objs)


@app_views.route(
        '/amenities/<amenity_id>', methods=['GET'],
        strict_slashes=False)
def get_amenity(amenity_id):
    """get an amenity object by id"""
    ame = storage.all(Amenity).get(f"Amenity.{amenity_id}")
    if not ame:
        abort(404)

    return jsonify(ame.to_dict())


@app_views.route(
        '/amenities/<amenity_id>', methods=['DELETE'],
        strict_slashes=False)
def delete_amenity(amenity_id):
    """delete an amenity object by id"""
    ame = storage.all(Amenity).get(f"Amenity.{amenity_id}")
    if not ame:
        abort(404)

    ame.delete()
    storage.save()
    return jsonify({})


@app_views.route(
        '/amenities', methods=['POST'],
        strict_slashes=False)
def create_amenity():
    """create a new amenity object"""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)

    ame = Amenity(name=request.get_json()['name'])
    ame.save()
    return make_response(jsonify(ame.to_dict()), 201)


@app_views.route(
        '/amenities/<amenity_id>', methods=['PUT'],
        strict_slashes=False)
def update_amenity(amenity_id):
    """update amenity object"""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    ame = storage.all(Amenity).get(f"Amenity.{amenity_id}")
    if not ame:
        abort(404)

    for k, v in request.get_json().items():
        if k == "id" or k == "created_at" or k == "updated_at":
            continue
        setattr(ame, k, v)

    ame.save()
    return jsonify(ame.to_dict()), 200
