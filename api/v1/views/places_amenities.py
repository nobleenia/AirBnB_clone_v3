#!/usr/bin/python3
"""Defining the places amenities module to request the amenities objs"""

from flask import abort, jsonify, make_response

from api.v1.views import app_views
from models import storage, storage_t
from models.amenity import Amenity
from models.place import Place


@app_views.route(
        '/places/<place_id>/amenities', methods=['GET'],
        strict_slashes=False)
def get_place_amenities(place_id):
    """get a place's amenities object by id"""
    place = storage.all(Place).get("Place.{}".format(place_id))
    if not place:
        abort(404)
    amenities = []

    if storage_t == 'db':
        for ame in place.amenities:
            amenities.append(ame.to_dict())
    else:
        for ame in storage.all(Amenity).values():
            if ame.id in place.amenity_ids:
                amenities.append(ame.to_dict())

    return jsonify(amenities)


@app_views.route(
        '/places/<place_id>/amenities/<amenity_id>',
        methods=['DELETE'],
        strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """delete an amenity from place object by id"""
    place = storage.all(Place).get("Place.{}".format(place_id))
    if not place:
        abort(404)
    ame = storage.all(Amenity).get("Amenity.{}".format(amenity_id))
    if not ame:
        abort(404)

    place_amenity = None
    if storage_t == 'db':
        for obj in place.amenities:
            if obj.id == ame.id:
                place_amenity = obj
    else:
        if ame.id in place.amenity_ids:
            place_amenity = ame
            place.amenity_ids.remove(ame.id)

    if not place_amenity:
        abort(404)

    ame.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route(
        '/places/<place_id>/amenities/<amenity_id>',
        methods=['POST'],
        strict_slashes=False)
def link_amenity_place(place_id, amenity_id):
    """link an amenity object with place"""
    place = storage.all(Place).get("Place.{}".format(place_id))
    if not place:
        abort(404)
    ame = storage.all(Amenity).get("Amenity.{}".format(amenity_id))
    if not ame:
        abort(404)

    if storage_t == "db":
        # check if the amenity already linked to place
        for obj in place.amenities:
            if obj.id == amenity_id:
                return jsonify(ame.to_dict()), 200

        place.amenities.append(ame)

    else:
        if amenity_id in place.amenity_ids:
            return jsonify(ame.to_dict()), 200

        place.amenity_ids.append(amenity_id)

    place.save()
    return make_response(jsonify(ame.to_dict()), 201)
