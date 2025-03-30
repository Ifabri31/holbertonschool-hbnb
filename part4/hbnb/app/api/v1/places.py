from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, current_user
from app.services import facade
from app.models import place

api = Namespace('places', description='Place operations')

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

review_model = api.model('PlaceReview', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user')
})

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'owner': fields.Nested(user_model, description='Owner of the place'),
    'amenities': fields.List(fields.Nested(amenity_model), description='List of amenities'),
    'reviews': fields.List(fields.Nested(review_model), description='List of reviews')
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """Register a new place"""
        if not current_user:
            return {'error': 'Unauthorized access'}, 401
        place_data = api.payload

        if place_data["owner_id"] != current_user.id:
            return {'error': 'Unauthorized action'}, 401

        try:
            new_place = facade.create_place(place_data)
        except ValueError:
            return {'error': 'Invalid input data'}, 400
        return {'id': new_place.id, 
                'title': new_place.title,
                'description': new_place.description,
                'price': new_place.price,
                'latitude': new_place.latitude, 
                'longitude': new_place.longitude,
                'owner_id': new_place.owner_id, 
                'amenities': new_place.amenities
            }, 201

    @api.response(200, 'List of places retrieved successfully')
    @api.response(404, 'List of places is empty')
    def get(self):
        """Retrieve a list of all places"""
        if not facade.get_all_places():
            return {'error': 'List of place is empty'}, 404
        all_places = facade.get_all_places()
        return [{'id': place['id'], 
                 'title': place['title'], 
                 'price': place['price'], 
                 'latitude': place['latitude'], 
                 'longitude': place['longitude'], 
                 'owner_id': place['owner_id']
            } for place in all_places], 200
        
@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        
        owner = facade.get_user(place.owner_id)
        all_amenities = facade.get_all_amenities()
        all_reviews = facade.get_all_reviews()
        
        return {'id': place.id, 
                'title': place.title,
                'description': place.description,''
                'price': place.price,
                'latitude': place.latitude, 
                'longitude': place.longitude,
                'owner': {
                    'id': owner.id,
                    'first_name': owner.first_name,
                    'last_name': owner.last_name,
                    'email': owner.email
                }, 
                'reviews': [{
                    'id': review['id'],
                    'comment': review['comment'],
                    'rating': review['rating']
                } for review in all_reviews if review['place_id'] == place_id],
                'amenities': [{
                    'id': amenity.id,
                    'name': amenity.name} for amenity in all_amenities if amenity.place == place.id]
        }, 200

    @api.expect(place_model, validate=True)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, place_id):
        """Update a place's information"""
        if not current_user:
            return {'error': 'Unauthorized access'}, 401
        
        place_data = api.payload
        place = facade.get_place(place_id)

        if not current_user.is_admin:
            if place.owner_id != current_user.id:
                return {'error': 'Unauthorized action'}, 403
        if not place:
            return {'error': 'Place not found'}, 404
        
        try:
            facade.update_place(place_id, place_data)
        except ValueError:
            return  {'error': 'Invalid input data'}, 400
        return {'message': 'Place updated successfully'}, 200