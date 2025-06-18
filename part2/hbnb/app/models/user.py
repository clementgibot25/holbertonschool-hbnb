#!/usr/bin/python3

"""Defines the User model for the application."""

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
    
    def __init__(self, email: str, password_hash: str,
                 first_name: str,
                 last_name: str,
                 is_admin: bool = False,
                 **kwargs):
        """Initialize a new User instance.
        
        Args:
            email (str): User's email address
            password_hash (str): Hashed password
            first_name (str): User's first name
            last_name (str): User's last name
            is_admin (bool, optional): Admin status. Defaults to False.
            **kwargs: Additional attributes from BaseModel
        """
        super().__init__(**kwargs)
        self.email = email
        self.password_hash = password_hash
        self.first_name = first_name
        self.last_name = last_name
        self.is_admin = is_admin
        self.places = []  # List of place IDs owned by this user
