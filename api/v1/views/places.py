#!/usr/bin/python3
"""places"""
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places')
def list_places_of_city(city_id):
    '''Retrieves a list of all Place objects in city'''
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    places = [place.to_dict() for place in storage.all("Place").values()
              if place.city_id == city_id]
    return jsonify(places)


@app_views.route('/places/<place_id>')
def get_place(place_id):
    '''Retrieves a Place object'''
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    '''Deletes'''
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    '''Creates'''
    if not request.get_json():
        abort(400, 'Not a JSON')
    name = request.json.get('name')
    user_id = request.json.get('user_id')
    if not name:
        abort(400, 'Missing name')
    if not user_id:
        abort(400, 'Missing user_id')
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    user = storage.get("User", user_id)
    if not user:
        abort(404)
    new_place = Place(name=name, user_id=user_id, city_id=city_id)
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    '''Updates a Place object'''
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200
