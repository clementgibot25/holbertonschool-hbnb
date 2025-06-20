#!/usr/bin/python3

"""Defines the User model for the application."""

import bcrypt
from app.models.base_model import BaseModel

class User(BaseModel):
    """Represents a user in the application.
    
    Attributes:
        email (str): User's email address (must be unique)
        password_hash (str): Hashed password for security
        first_name (str): User's first name
        last_name (str): User's last name
        is_admin (bool, optional): Whether user has admin privileges. Defaults to False.
        places (list): List of place IDs owned by the user
    """
    
    def __init__(self, email: str, password: str,
                 first_name: str,
                 last_name: str,
                 is_admin: bool = False,
                 **kwargs):
        """Initialize a new User.
        
        Args:
            email (str): User's email address
            password (str): Plain text password (will be hashed)
            first_name (str): User's first name
            last_name (str): User's last name
            is_admin (bool, optional): Admin status. Defaults to False.
            **kwargs: Additional attributes from BaseModel
        """
        super().__init__(**kwargs)
        self.email = email
        self.password_hash = self._hash_password(password)
        self.first_name = first_name
        self.last_name = last_name
        self.is_admin = is_admin
        self.places = []  # List of place IDs owned by this user

    def _hash_password(self, password: str) -> bytes:
        """Hash a password for storing.
        
        Args:
            password: Password to hash
            
        Returns:
            bytes: The hashed password
        """
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt)
        
    def check_password(self, password: str) -> bool:
        """Check if the provided password matches the stored hash.
        
        Args:
            password: Password to check
            
        Returns:
            bool: True if the password matches, False otherwise
        """
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash)
