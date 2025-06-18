#!/usr/bin/python3

"""Defines the base model class for all models in the application."""

import uuid
from datetime import datetime


class BaseModel:
    """Base class for all models with common attributes and methods."""

    def __init__(self):
        """Initialize a new model instance with unique ID and timestamps."""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        """Update the updated_at timestamp to current time."""
        self.updated_at = datetime.now()

    def update(self, data):
        """
        Update model attributes with provided dictionary.
        
        Args:
            data (dict): Dictionary of attributes to update
        """
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()  # Update the updated_at timestamp
