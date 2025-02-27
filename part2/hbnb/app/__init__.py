from flask import Flask
from flask_restx import Api
from app.api.v1.users import api as users_ns

def create_app():
    app = Flask(__name__)
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API', doc='/api/v1/')

    # Additional namespaces for places, reviews, and amenities will be added later
    
    api.add_namespace(users_ns, path='/api/v1/users')
    return app