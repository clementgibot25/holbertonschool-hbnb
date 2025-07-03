from re import I
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

# User update model - includes all modifiable fields
user_update_model = api.model('UserUpdate', {
    'first_name': fields.String(
        required=False,
        min_length=1,
        max_length=50,
        pattern=r"^[a-zA-Zà-ÿÀ-Ÿ\s\-']+$",
        description="User first name (letters, accents, spaces, hyphens and apostrophes only)",
        example='Marie-Louise'
    ),
    'last_name': fields.String(
        required=False,
        min_length=1,
        max_length=50,
        pattern=r"^[a-zA-Zà-ÿÀ-Ÿ\s\-']+$",
        description="User last name (letters, accents, spaces, hyphens and apostrophes only)",
        example="O'Connor"
    ),
    'email': fields.String(
        required=False,
        description='New email address (admins only)',
        pattern=r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
        example="new.email@example.com"
    ),
    'password': fields.String(
        required=False,
        min_length=8,
        max_length=128,
        description='New password (admins only, at least 8 characters)',
        example='NewSecurePassword123!'
    ),
    'is_admin': fields.Boolean(
        required=False,
        description='Admin status (admins only)',
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
        
    @api.expect(user_update_model, validate=True)
    @api.marshal_with(user_response_model)
    @api.response(200, 'User successfully updated')
    @api.response(400, 'Invalid request')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'User not found')
    @api.response(409, 'Email already in use')
    @jwt_required()
    def put(self, user_id):
        """
        Update an existing user
        
        Update user information. 
        - Regular users can only update their own first_name and last_name
        - Admins can update any user's information including is_admin status
        - Email and password can only be modified by admins
        """
        current_user_id = get_jwt_identity()
        current_user = facade.get_user(current_user_id)
        is_admin = current_user and current_user.is_admin
        
        # Vérifier que l'utilisateur modifie son propre compte ou est admin
        if current_user_id != user_id and not is_admin:
            api.abort(403, 'Unauthorized action')
            
        # Récupérer l'utilisateur à modifier
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, 'User not found')
            
        user_data = api.payload.copy()
        
        # Vérification des champs interdits pour les non-admins
        if not is_admin:
            forbidden_fields = ['email', 'password', 'id', 'is_admin']
            for field in forbidden_fields:
                if field in user_data:
                    api.abort(403, f'Admin privileges required to modify {field}')
        
        # Vérification de l'unicité de l'email si modification
        if 'email' in user_data and user_data['email'] != user.email:
            existing_user = facade.get_user_by_email(user_data['email'])
            if existing_user and existing_user.id != user_id:
                api.abort(409, 'Email already in use')
        
        # Traitement du mot de passe (hachage si fourni)
        if 'password' in user_data and user_data['password']:
            user_data['password'] = User.hash_password(user_data['password'])
        
        # Mise à jour des champs fournis
        for field, value in user_data.items():
            if hasattr(user, field) and value is not None:
                # Pour les booléens comme is_admin, on accepte explicitement False
                if isinstance(getattr(user, field), bool):
                    setattr(user, field, value)
                # Pour les chaînes, on ne met à jour que si la valeur n'est pas vide
                elif value != '':
                    setattr(user, field, value)
        
        # Sauvegarder les modifications
        facade.update_user(user.id, **{k: v for k, v in user_data.items() 
                                    if hasattr(user, k) and v is not None and v != ''})
        
        return format_user_response(user), 200

@api.route('/users/')
class AdminUserCreate(Resource):
    @jwt_required()
    @api.expect(user_model, validate=True)
    @api.marshal_with(user_registration_response_model)
    @api.response(201, 'User created successfully')
    @api.response(400, 'Invalid input or email already registered')
    @api.response(403, 'Admin privileges required')
    @api.response(500, 'Internal server error')
    def post(self):
        # Récupérer l'ID de l'utilisateur depuis le token JWT
        current_user_id = get_jwt_identity()
        print(f"[DEBUG] User ID from token: {current_user_id}")
        
        # Vérifier si l'utilisateur est admin
        current_user = facade.get_user(current_user_id)
        print(f"[DEBUG] Current user: {current_user}")
        if current_user:
            print(f"[DEBUG] User is admin: {getattr(current_user, 'is_admin', 'no is_admin attribute')}")
        
        if not current_user or not getattr(current_user, 'is_admin', False):
            print("[DEBUG] Access denied - User is not admin or doesn't exist")
            return {'error': 'Admin privileges required', 'user_id': current_user_id}, 403

        user_data = api.payload
        email = user_data.get('email')

        # Vérifier si l'email est déjà utilisé
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
                password=password_hash
            )
            return {'id': new_user.id, 'message': 'User registered successfully'}, 201
        except ValueError as e:
            api.abort(400, str(e) or 'Invalid input data')
        except Exception as e:
            api.abort(500, 'An unexpected error occurred')
