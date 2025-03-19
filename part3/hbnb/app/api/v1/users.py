from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, current_user
from flask_bcrypt import Bcrypt
from app import bcrypt

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
    @jwt_required()
    def post(self):
        """Register a new user"""
        if not current_user.is_admin:
            return {'error': 'Admin privileges required'}, 403
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
        all_users = facade.get_all_users()
        return [{'id': user["id"], 
                 'first_name': user["first_name"], 
                 'last_name': user["last_name"], 
                 'email': user["email"]
            } for user in all_users], 200

@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {'id': user.id, 
                'first_name': user.first_name,
                'last_name': user.last_name, 
                'email': user.email
            }, 200
    
    @api.expect(user_model, validate=True)
    @api.response(404, "User not found")
    @api.response(202, "Data updated successfully")
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, user_id):
        """Update the user datas"""
        if current_user.id != user_id and not current_user.is_admin:
            return {'error': 'Unauthorized action'}, 401
        
        user = facade.get_user(user_id)
        new_data = api.payload

        if not user:
            return {"error": "User not found"}, 404
        
        if not current_user.is_admin:
            if new_data['email'] != user.email:
                return {'error': 'You cannot modify email or password.'}, 400
            if not bcrypt.check_password_hash(new_data['password'], user.password):
                return {'error': 'You cannot modify email or password.'}, 400
        
        if new_data["email"]:
            existing_user = facade.get_user_by_email(new_data["email"])
            if existing_user and existing_user.id != user_id:
                return {'error': 'Email already in use'}, 400

        try:
            update_user = facade.update_user(user_id, new_data)
        except ValueError:
            return {'error': 'Invalid input data'}, 400
        return {'id': update_user.id, 
                'first_name': update_user.first_name,
                'last_name': update_user.last_name, 
                'email': update_user.email
            }, 202