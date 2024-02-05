#!/usr/bin/python3
"""Defining the states module to request the states objs"""

from flask import abort, jsonify, make_response, request

from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route(
        '/states', methods=['GET'],
        strict_slashes=False)
def get_states():
    """get all States objects"""
    objs = []

    for obj in storage.all(State).values():
        objs.append(obj.to_dict())

    return jsonify(objs)


@app_views.route(
        '/states/<state_id>', methods=['GET'],
        strict_slashes=False)
def get_state_by_id(state_id):
    """get a state object by id"""
    state = storage.all(State).get("State.{}".format(state_id))
    if not state:
        abort(404)

    return jsonify(state.to_dict())


@app_views.route(
        '/states/<state_id>', methods=['DELETE'],
        strict_slashes=False)
def delete_state(state_id):
    """delete a state object by id"""
    state = storage.all(State).get("State.{}".format(state_id))
    if not state:
        abort(404)

    state.delete()
    storage.save()
    return jsonify({})


@app_views.route(
        '/states', methods=['POST'],
        strict_slashes=False)
def create_state():
    """create a new state object"""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)

    state = State(name=request.get_json()['name'])
    state.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route(
        '/states/<state_id>', methods=['PUT'],
        strict_slashes=False)
def update_state(state_id):
    """update state object"""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    state = storage.all(State).get("State.{}".format(state_id))
    if not state:
        abort(404)

    for k, v in request.get_json().items():
        if k == "id" or k == "created_at" or k == "updated_at":
            continue
        setattr(state, k, v)

    state.save()
    return jsonify(state.to_dict())
