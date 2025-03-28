from tokenize import Comment
from flask_restx import Namespace, Resource, fields, marshal
from flask_jwt_extended import jwt_required, get_jwt_identity, current_user
from app.services import facade

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'comment': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

# Define output by review_by_place
review_by_place_model = api.model('ReviewbyPlace', {
    'id': fields.String(description='Id by review'),
    'comment': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)')
})

@api.route('/reviews')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """Register a new review"""
        if not current_user:
            return {'error': 'Unauthorized access'}, 401
        
        review_data = api.payload
        place = facade.get_place(review_data["place_id"])
        if place.owner_id == current_user.id:
            return {'error': 'You cannot review your own place'}, 400
        
        all_reviews = facade.get_review_by_user_id(current_user.id)
        for _ in all_reviews:
            if _.place_id == review_data["place_id"]:
                return {'error': 'You have already reviewed this place'}, 400

        try:
            new_review = facade.create_review(review_data)
        except ValueError:
            return {'error': 'Invalid input data'}, 400
        return {'id': new_review.id, 
                'comment': new_review.comment,
                'rating': new_review.rating, 
                'user_id': new_review.user_id,
                'place_id': new_review.place_id
            }, 201

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        all_reviews = facade.get_all_reviews()
        return [{
            'id': review['id'], 
            'comment': review['comment'],
            'rating': review['rating'], 
        } for review in all_reviews], 200

@api.route('/reviews/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return {'id': review.id, 
                'comment': review.comment,
                'rating': review.rating, 
                'user_id': review.user_id,
                'place_id': review.place_id
            }, 200

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, review_id):
        """Update a review's information"""
        if not current_user:
            return {'error': 'Unauthorized access'}, 401
        if not facade.get_review(review_id):
            return {'error': 'Review not found'}
        
        existing_review = facade.get_review(review_id)
        if not current_user.is_admin:
            if existing_review.user_id != current_user.id:
                return {'error': 'Unauthorized action'}, 403
       
        review = api.payload
        
        try:
            facade.update_review(review_id, review)
        except ValueError:
            return {'error': 'Invalid input data'}, 400
        return {'message': 'Review had updated'}, 200

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @jwt_required()
    def delete(self, review_id):
        """Delete a review"""
        if not current_user:
            return {'error': 'Unauthorized access'}, 401
        existing_review = facade.get_review(review_id)
        if not existing_review:
            return {'error': 'Review not found'}, 404
        if not current_user.is_admin:
            if existing_review.user_id != current_user.id:
                return {'error': 'Unauthorized action'}, 403
        
        facade.delete_reviews(review_id)
        return {'message': 'Review deleted successfully'}, 200

@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        reviews_list = facade.get_reviews_by_place(place_id)
        if not reviews_list:
            return {'error': 'Place not found'}, 404
        marsh_reviews = []
        for review in reviews_list:
            marsh_reviews.append(marshal(review, review_by_place_model))
        return marsh_reviews, 200