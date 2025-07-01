from flask_restx import Namespace, Resource, fields
from app.services.facade import hbnb_facade as facade
from app.models.user import User
from flask_jwt_extended import jwt_required, get_jwt_identity

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
    ),
    'password': fields.String(
        required=True,
        min_length=8,
        max_length=128,
        description='User password (at least 8 characters, not returned in response)',
        example='MySecurePassword123!'
    )
})

# User response model for response documentation
user_response_model = api.model('UserResponse', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='User first name'),
    'last_name': fields.String(description='User last name'),
    'email': fields.String(description='User email address')
    # Password volontairement omis pour la sécurité
})

# Registration response model
user_registration_response_model = api.model('UserRegistrationResponse', {
    'id': fields.String(description='User ID'),
    'message': fields.String(description='Registration success message')
})

@api.route('/')
class UserList(Resource):
    @api.marshal_list_with(user_response_model)
    @api.response(200, 'Success')
    def get(self):
        """
        Retrieve all users
        
        Returns a list of all users with their basic information.
        For detailed user information, use GET /users/{user_id}
        """
        users = facade.get_all_users()
        return [format_user_response(user) for user in users], 200

    @api.expect(user_model, validate=True)
    @api.marshal_with(user_registration_response_model, code=201)
    @api.response(201, 'User created successfully')
    @api.response(400, 'Invalid input or email already registered')
    @api.response(500, 'Internal server error')
    def post(self):
        """
        Register a new user
        
        Create a new user account with the provided information.
        Email must be unique across all users.
        Password will be securely hashed before storage.
        """
        try:
            data = api.payload
            # Hash the password before creating the user
            password_hash = User.hash_password(data['password'])
            
            # 🔒 Sécurité : Supprimer le password plain text de la mémoire
            data.pop('password', None)
            
            # Create user with hashed password
            new_user = facade.create_user(
                email=data['email'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                password=password_hash
            )
            # Persist user (if not already done in create_user)
            # facade.save_user(new_user)  # Uncomment if required by your architecture
            return {'id': new_user.id, 'message': 'User registered successfully'}, 201
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
        """
        Get user details by ID
        
        Retrieve detailed information about a specific user,
        including their first name, last name, and email.
        """
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, 'User not found')
        return format_user_response(user), 200
        
    @api.expect(user_model, validate=True)
    @api.marshal_with(user_response_model)
    @api.response(200, 'User successfully updated')
    @api.response(400, 'Email already registered')
    @api.response(404, 'User not found')
    @jwt_required()
    def put(self, user_id):
        """
        Update an existing user
        
        Update user information with the provided fields.
        If the email is being updated, it must remain unique across all users.
        
        Note: Only the fields included in the request will be updated.
        Other fields will remain unchanged.
        """
        current_user_id = get_jwt_identity()
        
        # Vérifier que l'utilisateur modifie son propre compte
        if current_user_id != user_id:
            api.abort(403, 'Unauthorized action')
            
        user_data = api.payload
        
        # Vérifier si l'utilisateur essaie de modifier l'email ou le mot de passe
        if ('email' in user_data and user_data['email'] != facade.get_user(user_id).email) or \
           ('password' in user_data and user_data['password'] != facade.get_user(user_id).password):
            api.abort(400, 'You cannot modify email or password')
        
        # Vérifier si l'utilisateur existe
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, 'User not found')
            
        # Vérifier si l'email est modifié et existe déjà
        if 'email' in user_data and user_data['email'] != facade.get_user(user_id).email:
            existing_user = facade.get_user_by_email(user_data['email'])
            if existing_user and existing_user.id != user_id:
                api.abort(400, 'Email already registered')
                
        updated_user = facade.update_user(user_id, **user_data)
        return format_user_response(updated_user), 200