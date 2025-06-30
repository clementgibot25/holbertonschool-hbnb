#!/usr/bin/python3

from flask_restx import Namespace, Resource, fields
from app.services.facade import hbnb_facade as facade

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, 
                         description='Name of the amenity (e.g., WiFi, Pool, Parking)',
                         example='WiFi',
                         min_length=1)
})

# Define the response model for amenity
amenity_response = api.model('AmenityResponse', {
    'id': fields.String(description='Unique identifier of the amenity', example='550e8400-e29b-41d4-a716-446655440000'),
    'name': fields.String(description='Name of the amenity', example='WiFi'),
    'created_at': fields.DateTime(description='Creation timestamp'),
    'updated_at': fields.DateTime(description='Last update timestamp')
})

# Define the response model for list of amenities
amenities_list = api.model('AmenityList', {
    'amenities': fields.List(fields.Nested(amenity_response), description='List of amenities')
})

@api.route('/')
@api.doc(security=None)
class AmenityList(Resource):
    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Amenity successfully created', model=amenity_response)
    @api.response(400, 'Invalid input data', model=api.model('Error', {
        'message': fields.String(description='Error message', example='Name is required')
    }))
    def post(self):
        """
        Register a new amenity
        
        Use this endpoint to create a new amenity with the provided name.
        The name must be unique (case-insensitive).
        """
        if not api.payload or 'name' not in api.payload:
            api.abort(400, {'message': 'Name is required'})
            
        try:
            amenity = facade.create_amenity({'name': api.payload['name']})
            return amenity.to_dict(), 201
        except ValueError as e:
            api.abort(400, {'message': str(e)})

    @api.response(200, 'List of amenities retrieved successfully', model=amenities_list)
    def get(self):
        """
        Retrieve all amenities
        
        Returns a list of all amenities in the system.
        """
        amenities = facade.get_all_amenities()
        return {'amenities': [a.to_dict() for a in amenities]}, 200

@api.route('/<amenity_id>')
@api.doc(security=None, params={'amenity_id': 'The amenity identifier'})
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully', model=amenity_response)
    @api.response(404, 'Amenity not found', model=api.model('Error', {
        'message': fields.String(description='Error message', example='Amenity not found')
    }))
    def get(self, amenity_id):
        """
        Get amenity details
        
        Retrieve detailed information about a specific amenity by its ID.
        """
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'message': 'Amenity not found'}, 404
        return amenity.to_dict(), 200

    @api.expect(amenity_model, validate=True)
    @api.response(200, 'Amenity updated successfully', model=api.model('Success', {
        'message': fields.String(description='Success message', example='Amenity updated successfully')
    }))
    @api.response(404, 'Amenity not found', model=api.model('Error', {
        'message': fields.String(description='Error message', example='Amenity not found')
    }))
    @api.response(400, 'Invalid input data', model=api.model('Error', {
        'message': fields.String(description='Error message', example='Name is required')
    }))
    def put(self, amenity_id):
        """
        Update an amenity
        
        Update the name of an existing amenity. The name must be unique.
        """
        if not api.payload or 'name' not in api.payload:
            return {'message': 'Name is required'}, 400
            
        try:
            amenity = facade.update_amenity(amenity_id, **api.payload)
            if not amenity:
                return {'message': 'Amenity not found'}, 404
            return {'message': 'Amenity updated successfully'}, 200
        except ValueError as e:
            return {'message': str(e)}, 400
