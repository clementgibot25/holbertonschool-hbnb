#!/usr/bin/python3

"""Defines the Amenity model for the application."""

from app.models.base_model import BaseModel

class Amenity(BaseModel):
    """Represents an amenity that can be associated with places.
    
    Attributes:
        name (str): The name of the amenity (e.g., 'WiFi', 'Pool', 'Parking')
    """
    
    def __init__(self, name: str, **kwargs):
        """Initialize a new Amenity instance.
        
        Args:
            name (str): The name of the amenity
            **kwargs: Additional attributes from BaseModel
        """
        super().__init__(**kwargs)
        self.name = name
