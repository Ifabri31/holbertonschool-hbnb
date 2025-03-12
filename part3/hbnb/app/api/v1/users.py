from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity


api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        user_data = api.payload
        # Simulate email uniqueness check (to be replaced by real validation with persistence)
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400
        # Check if the data provided are correct
        try:
            new_user = facade.create_user(user_data)
        except ValueError:
            return {'error': 'Invalid input data'}, 400
        # Already OK
        return {'id': new_user.id, 'message': 'User created successfully'}, 201
    
    @api.response(200, 'List of users is successfully retrivied')
    @api.response(404, 'Users list empty')
    def get(self):
        """Get all users"""
        if not facade.get_all_users():
            return {'error': 'User list empty'}, 404
        return facade.get_all_users(), 200

@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {'id': user.id, 'first_name': user.first_name,
                'last_name': user.last_name, 'email': user.email}, 200
    
    @api.expect(user_model, validate=True)
    @api.response(404, "User not found")
    @api.response(202, "Data updated successfully")
    @api.response(400, 'Invalid input data')
    @jwt_required
    def put(self, user_id):
        """Update the user datas"""
        new_data = api.payload
        current_user = get_jwt_identity()  # Retrieve the user's identity from the token
        user = facade.get_user(user_id)
        if not user:
            return {"error": "User not found"}, 404
        try:
            facade.update_user(user_id, new_data)
        except ValueError:
            return {'error': 'Invalid input data'}, 400
        return {'message': f'Hello, user {current_user["id"]}'}, 200