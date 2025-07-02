from flask_restx import Namespace, Resource
from app.services.facade import hbnb_facade as facade
from app.models.user import User
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from flask import request
from flask_restx import fields


def format_user_response(user):
    """Format standard pour les réponses utilisateur"""
    return {
        'id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'is_admin': user.is_admin
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
    ),
    'is_admin': fields.Boolean(
        required=False,
        description='User admin status',
        example=False
    )
})

# User update model - only modifiable fields
user_update_model = api.model('UserUpdate', {
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
    ),

    'is_admin': fields.Boolean(
        required=False,
        description='User admin status',
        example=False
    )
})

# User response model for response documentation
user_response_model = api.model('UserResponse', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='User first name'),
    'last_name': fields.String(description='User last name'),
    'email': fields.String(description='User email address'),
    'is_admin': fields.Boolean(description='User admin status')
    # Password volontairement omis pour la sécurité
})

# Registration response model
user_registration_response_model = api.model('UserRegistrationResponse', {
    'id': fields.String(description='User ID'),
    'message': fields.String(description='Registration success message')
})

@api.route('/users/')
class AdminUserCreate(Resource):
    @jwt_required()
    @api.expect(user_model, validate=True)
    @api.marshal_with(user_registration_response_model)
    @api.response(201, 'User created successfully')
    @api.response(400, 'Invalid input or email already registered')
    @api.response(500, 'Internal server error')
    def post(self):
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        user_data = api.payload
        email = user_data.get('email')

        # Check if email is already in use
        if facade.get_user_by_email(email):
            return {'error': 'Email already registered'}, 400

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
                password=password_hash,
                is_admin=data['is_admin']
            )
            return {'id': new_user.id, 'message': 'User registered successfully'}, 201
        except ValueError as e:
            api.abort(400, str(e) or 'Invalid input data')
        except Exception as e:
            api.abort(500, 'An unexpected error occurred')

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

    @jwt_required()
    @api.expect(user_update_model, validate=True)
    @api.marshal_with(user_response_model)
    @api.response(200, 'User successfully updated')
    @api.response(400, 'You cannot modify email or password.')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'User not found')
    def put(self, user_id):
        """
        Update user details by ID.
        - Admin: Can update any user, including email and password
        - Regular user: Can only update their own profile (first_name, last_name only)
        """
        from app import bcrypt

        current_user = get_jwt_identity()
        user_data = api.payload
        is_admin = current_user.get('is_admin', False)
        current_user_id = current_user.get('id')

        # Vérifier si l'utilisateur existe
        target_user = facade.get_user(user_id)
        if not target_user:
            return {"error": "User not found"}, 404

        if not is_admin:
            # Utilisateur normal : restrictions
            if current_user_id != user_id:
                return {"error": "You can only update your own profile"}, 403

            # Interdire la modification de l'email ou du mot de passe
            forbidden_fields = {'email', 'password'}
            if forbidden_fields.intersection(user_data.keys()):
                return {
                    "error": "You cannot modify email or password. Only first_name and last_name are allowed."
                }, 403

        # Si admin OU utilisateur normal (après vérif), on continue :
        # Hasher le mot de passe si présent (admin seulement)
        if is_admin and "password" in user_data:
            hashed_password = bcrypt.generate_password_hash(
                user_data["password"]
            ).decode('utf-8')
            user_data["password"] = hashed_password

        # Vérifier l'unicité de l'email si modifié (admin seulement)
        if is_admin and "email" in user_data:
            existing_user = facade.get_user_by_email(user_data['email'])
            if existing_user and existing_user.id != user_id:
                return {'error': 'Email already registered'}, 400

        updated_user = facade.update_user(user_id, user_data)
        return {
            "id": updated_user.id,
            "first_name": updated_user.first_name,
            "last_name": updated_user.last_name,
            "email": updated_user.email,
            "message": "User updated successfully"
        }, 200
