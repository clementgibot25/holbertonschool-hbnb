#!/usr/bin/python3

"""Defines the User model for the application."""

from app.models.base_model import BaseModel

class User(BaseModel):
    """Represents a user in the application.
    
    Attributes:
        email (str): The user's email address (must be unique)
        first_name (str): The user's first name
        last_name (str): The user's last name
        is_admin (bool): Whether the user has admin privileges
        places (list): List of place IDs owned by this user
    """
    
    def __init__(self, email: str, first_name: str, last_name: str, 
                 is_admin: bool = False, **kwargs):
        """Initialize a new User instance.
        
        Args:
            email: The user's email address
            first_name: The user's first name
            last_name: The user's last name
            is_admin: Whether the user has admin privileges
            **kwargs: Additional attributes from BaseModel
        """
        super().__init__(**kwargs)
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.is_admin = is_admin
        self.places = []  # List of place IDs owned by this user
