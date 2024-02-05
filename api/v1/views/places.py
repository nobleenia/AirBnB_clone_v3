#!/usr/bin/python3
"""Defining the places module to request the places objs"""

from flask import abort, jsonify, make_response, request

from api.v1.views import app_views
from models import storage, storage_t
from models.city import City
from models.place import Place
from models.state import State
from models.user import User


@app_views.route(
        '/cities/<city_id>/places', methods=['GET'],
        strict_slashes=False)
def get_places(city_id):
    """get all places objects"""
    city = storage.all(City).get(f"City.{city_id}")
    if not city:
        abort(404)

    objs = []
    for obj in city.places:
        objs.append(obj.to_dict())

    return jsonify(objs)


@app_views.route(
        '/places/<place_id>', methods=['GET'],
        strict_slashes=False)
def get_place(place_id):
    """get a place object by id"""
    place = storage.all(Place).get(f"Place.{place_id}")
    if not place:
        abort(404)

    return jsonify(place.to_dict())


@app_views.route(
        '/places/<place_id>', methods=['DELETE'],
        strict_slashes=False)
def delete_place(place_id):
    """delete a place object by id"""
    place = storage.all(Place).get(f"Place.{place_id}")
    if not place:
        abort(404)

    place.delete()
    storage.save()
    return jsonify({})


@app_views.route(
        '/cities/<city_id>/places', methods=['POST'],
        strict_slashes=False)
def create_place(city_id):
    """create a new place object"""
    city = storage.all(City).get(f"City.{city_id}")
    if not city:
        abort(404)

    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'user_id' not in request.get_json():
        return make_response(jsonify({'error': 'Missing user_id'}), 400)

    user_id = request.get_json()['user_id']
    user = storage.all(User).get(f"User.{user_id}")
    if not user:
        abort(404)

    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)

    name = request.get_json()['name']
    place = Place(city_id=city_id, user_id=user_id, name=name)
    place.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route(
        '/places/<place_id>', methods=['PUT'],
        strict_slashes=False)
def update_place(place_id):
    """update place object"""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    place = storage.all(Place).get(f"Place.{place_id}")
    if not place:
        abort(404)

    ignor = ["id", "created_at", "updated_at", "user_id", "city_id"]
    for k, v in request.get_json().items():
        if k in ignor:
            continue
        setattr(place, k, v)

    place.save()
    return jsonify(place.to_dict())


@app_views.route(
        '/places_search', methods=['POST'],
        strict_slashes=False)
def search_place():
    """serach and filter places"""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    list_states_ids = request.get_json().get("states")
    list_cities_ids = request.get_json().get('cities')
    list_amenities_ids = request.get_json().get('amenities')
    list_places = []

    if not list_states_ids and not list_cities_ids:
        list_places = storage.all(Place).values()

    if list_states_ids:
        for s_id in list_states_ids:
            state = storage.all(State).get(f"State.{s_id}")
            if state:
                for c in state.cities:
                    list_places.extend(c.places)

    if list_cities_ids:
        for c_id in list_cities_ids:
            city = storage.all(City).get(f"City.{c_id}")
            if city:
                list_places.extend(city.places)
    # remove any duplicates
    list_places = list(set(list_places))
    if list_amenities_ids:
        for place in list_places:
            place_ame = []
            if storage_t == "db":
                place_ame = [ame.id for ame in place.amenities]
            else:
                place_ame = place.amenity_ids

            if not all(ame_id in place_ame for ame_id in list_amenities_ids):
                list_places.remove(place)
    places = []
    for p in list_places:
        p_dict = p.to_dict().copy()

        if "amenities" in p.to_dict():
            del p_dict["amenities"]
        places.append(p_dict)

    return jsonify(places)
