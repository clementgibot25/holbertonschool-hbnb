from flask import Flask
from flask_restx import Api
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.places import api as places_ns

def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_class)
    # Enable debug mode for better error messages
    app.config['DEBUG'] = True
    
    # Initialize API with Swagger at root
    api = Api(app, 
             version='1.0', 
             title='HBnB API', 
             description='HBnB Application API',
             doc='/'  # Serve Swagger UI at the root URL
             )

    # Register namespaces with their paths
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(places_ns, path='/api/v1/places')
    return app