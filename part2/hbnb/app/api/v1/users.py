from flask_restx import Namespace, Resource, fields, abort
from app.services.facade import hbnb_facade as facade
from app.services.user_service import user_service

def format_user_response(user):
    """Format standard pour les réponses utilisateur"""
    return {
        'id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email
    }

api = Namespace('users', description='User operations')

# User model for request documentation
user_model = api.model('User', {
    'first_name': fields.String(
        required=True,
        min_length=1,
        max_length=50,
        pattern=r"^[a-zA-Zà-ÿÀ-Ÿ\s\-']+$",
        description="User first name (letters, accents, spaces, hyphens and apostrophes only)",
        example='Marie-Louise'
    ),
    'last_name': fields.String(
        required=True,
        min_length=1,
        max_length=50,
        pattern=r"^[a-zA-Zà-ÿÀ-Ÿ\s\-']+$",
        description="User last name (letters, accents, spaces, hyphens and apostrophes only)",
        example="O'Connor"
    ),
    'email': fields.String(
        required=True,
        description='User email address',
        pattern=r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
        example="marie-louise.oconnor@example.com"
    )
})

# User response model for response documentation
user_response_model = api.model('UserResponse', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='User first name'),
    'last_name': fields.String(description='User last name'),
    'email': fields.String(description='User email address')
})

@api.route('/')
class UserList(Resource):
    @api.marshal_list_with(user_response_model)
    @api.response(200, 'Success')
    def get(self):
        """Retrieve all users"""
        users = facade.get_all_users()
        return [format_user_response(user) for user in users], 200

    @api.expect(user_model, validate=True)
    @api.marshal_with(user_response_model, code=201)
    @api.response(201, 'User created successfully')
    @api.response(400, 'Invalid input or email already registered')
    @api.response(500, 'Internal server error')
    def post(self):
        """Create a new user account"""
        try:
            data = api.payload
            new_user = facade.create_user(
                email=data['email'],
                first_name=data['first_name'],
                last_name=data['last_name']
            )
            return format_user_response(new_user), 201
            
        except ValueError as e:
            api.abort(400, str(e) or 'Invalid input data')
        except Exception as e:
            api.abort(500, 'An unexpected error occurred')




@api.route('/<user_id>')
class UserResource(Resource):
    @api.marshal_with(user_response_model)
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, 'User not found')
        return format_user_response(user), 200
        
    @api.expect(user_model, validate=True)
    @api.marshal_with(user_response_model)
    @api.response(200, 'User successfully updated')
    @api.response(400, 'Email already registered')
    @api.response(404, 'User not found')
    def put(self, user_id):
        """Update an existing user"""
        user_data = api.payload
        
        # Check if user exists
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, 'User not found')
            
        # Check if email is modified and already exists
        if 'email' in user_data and user_data['email'] != user.email:
            existing_user = facade.get_user_by_email(user_data['email'])
            if existing_user and existing_user.id != user_id:
                api.abort(400, 'Email already registered')
                
        updated_user = facade.update_user(user_id, **user_data)
        return format_user_response(updated_user), 200