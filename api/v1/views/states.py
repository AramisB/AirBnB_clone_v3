#!/usr/bin/python3
"""A new view for State objects that handles
all default RESTFul API actions"""
from api.v1.views import app_views
from models import storage
from flask import abort, request, jsonify
from models.state import State


@app_views.route('/states/', methods=['GET'],
                 strict_slashes=False)
def getStates():
    """A function to get states"""
    states = storage.all(State)
    all_states = []
    for state in states.values():
        all_states.append(state.to_dict())
    return jsonify(all_states)

@app_views.route('/states/<state_id>',
                 methods=['GET'], strict_slashes=False)
def getStateById(state_id):
    """A method to get state by id
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())

@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def deleteStateById(state_id):
    """A method to delete state by id
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/', methods=['POST'],
                 strict_slashes=False)
def createState():
    """A method to create state by id
    """
    if not request.is_json:
        abort(400, "Not a JSON")

    data = request.get_json()
    if "name" not in data:
        abort(400, "Missing name")

    state = State(**data)
    storage.save()
    return jsonify(state.to_dict()), 201

@app_views.route('/states/<state_id>', methods=['PUT'],
                 strict_slashes=False)
def editState(state_id):
    """A method to edit state by id
    """
    if not request.is_json:
        abort(400, 'Not a JSON')

    data = request.get_json()
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(state, key, value)

    storage.save()
    return jsonify(state.to_dict()), 200
