from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, current_user

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """Register a new amenity"""

        if not current_user.is_admin:
             return {'error': 'Admin privileges required'}, 403
        amenity_data = api.payload
        try:
            new_amenity = facade.create_amenity(amenity_data)
        except ValueError:
            return {'error': 'Invalid input data'}, 400
        return {'id': new_amenity.id, 'name': new_amenity.name}, 201

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        amenity_list = facade.get_all_amenities()

        if not amenity_list:
            return {'error': 'List of amenities empty'}, 404

        return [{
            'id': amenity.id,
            'name': amenity.name
        } for amenity in amenity_list], 200

@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return {'id': amenity.id, 
                'name': amenity.name
            }, 200

    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, amenity_id):
        """Update an amenity's information"""
        if not current_user.is_admin:
            return {'error': 'Admin privileges required'}, 403
        amenity_data = api.payload
        try:
            amenity = facade.get_amenity(amenity_id)
        except ValueError:
            return {'error': 'Invalid input data'}, 400
        if not amenity:
            return {'error': 'Amenity not found'}, 404       
        facade.update_amenity(amenity_id, amenity_data)
        return {'message': 'Amenity update successfully'}, 200