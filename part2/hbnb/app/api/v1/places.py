#!/usr/bin/python3

"""Place resource module for handling place-related operations."""

from flask_restx import Namespace, Resource, fields, abort
from flask import request
from app.services.facade import hbnb_facade as facade


def format_place_response(place):
    """Standardize place JSON response format"""
    return {
        'id': place.id,
        'title': place.title,
        'description': place.description,
        'price': place.price,
        'latitude': place.latitude,
        'longitude': place.longitude,
        'owner_id': place.owner_id
    }

api = Namespace('places', description='Place operations')

place_model = api.model('Place', {
    'title': fields.String(
        required=True,
        min_length=1,
        max_length=100,
        description='Title of the place',
        example='Cozy Studio in Paris'
    ),
    'description': fields.String(
        required=True,
        min_length=1,
        max_length=500,
        description='Detailed description of the place',
        example='A lovely studio apartment located in the heart of the city.'
    ),
    'price': fields.Float(
        required=True,
        description='Price per night (must be positive)',
        example=85.0,
    ),
    'latitude': fields.Float(
        required=True,
        description='Geographic latitude',
        example=48.8566
    ),
    'longitude': fields.Float(
        required=True,
        description='Geographic longitude',
        example=2.3522
    ),
    'owner_id': fields.String(
        required=True,
        description='ID of the user who owns this place',
        example='user_12345'
    )
})

place_response_model = api.model('PlaceResponse', {
    'id': fields.String(description='Place ID'),
    'title': fields.String(description='Title of the place'),
    'description': fields.String(description='Detailed description of the place'),
    'price': fields.Float(description='Price per night'),
    'latitude': fields.Float(description='Latitude'),
    'longitude': fields.Float(description='Longitude'),
    'owner_id': fields.String(description='Owner user ID')
})


@api.route('/')
class PlaceList(Resource):
    @api.marshal_list_with(place_response_model)
    @api.response(200, 'Success')
    def get(self):
        """Retrieve all places."""
        places = facade.place_service.get_all_places()
        return [format_place_response(p) for p in places], 200

    @api.expect(place_model, validate=True)
    @api.marshal_with(place_response_model, code=201)
    @api.response(201, 'Place created successfully')
    @api.response(400, 'Invalid input')
    @api.response(500, 'Internal server error')
    def post(self):
        """Create a new place."""
        try:
            data = api.payload
            # Basic validation for price
            if data['price'] < 0:
                abort(400, 'Price must be non-negative')
            new_place = facade.create_place(**data)
            return format_place_response(new_place), 201
        except ValueError as e:
            abort(400, str(e) or 'Invalid input data')
        except Exception:
            abort(500, 'An unexpected error occurred')


@api.route('/<place_id>')
@api.param('place_id', 'The place identifier')
class PlaceResource(Resource):
    @api.marshal_with(place_response_model)
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID."""
        place = facade.get_place(place_id)
        if not place:
            abort(404, 'Place not found')
        return format_place_response(place), 200

    @api.expect(place_model, validate=True)
    @api.marshal_with(place_response_model)
    @api.response(200, 'Place successfully updated')
    @api.response(404, 'Place not found')
    def put(self, place_id):
        """Update an existing place."""
        updates = api.payload
        place = facade.place_service.update_place(place_id, **updates)
        if not place:
            abort(404, 'Place not found')
        return format_place_response(place), 200

    @api.response(204, 'Place deleted')
    @api.response(404, 'Place not found')
    def delete(self, place_id):
        """Delete a place by ID."""
        deleted = facade.place_service.delete_place(place_id)
        if not deleted:
            abort(404, 'Place not found')
        return '', 204

