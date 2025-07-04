from flask import Flask
from flask_restx import Api
from flask_bcrypt import Bcrypt
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.places import api as places_ns
from app.api.v1.auth import api as auth_ns
from flask_jwt_extended import JWTManager

# Initialize extensions
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_class)
    # Enable debug mode for better error messages
    app.config['DEBUG'] = True
    
    # Initialize API with Swagger at root + JWT Authorization
    api = Api(app, 
             version='1.0', 
             title='HBnB API', 
             description='HBnB Application API',
             doc='/',  # Serve Swagger UI at the root URL
             authorizations={
                 'Bearer': {
                     'type': 'apiKey',
                     'in': 'header',
                     'name': 'Authorization',
                     'description': 'JWT token (prefix with "Bearer ")'
                 }
             },
             security='Bearer'  # Set default security for all endpoints
             )

    # Register namespaces with their paths
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(auth_ns, path='/api/v1/auth')
    
    # Initialize extensions with app
    bcrypt.init_app(app)
    jwt.init_app(app)
    
    return app