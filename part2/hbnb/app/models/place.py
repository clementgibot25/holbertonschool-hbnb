#!/usr/bin/python3

"""Defines the Place model for the application."""

from app.models.base_model import BaseModel
from typing import List, Optional

class Place(BaseModel):
    """Represents a property listing in the application.
    
    Attributes:
        title (str): Title of the place
        description (str): Detailed description
        price (float): Price per night
        latitude (float): Geographic latitude
        longitude (float): Geographic longitude
        owner_id (str): ID of the user who owns this place
        reviews (List[Review]): List of reviews for this place
        amenities (List[Amenity]): List of amenities available at this place
    """
    
    def __init__(self,
                title: str,
                description: str,
                price: float,
                latitude: float,
                longitude: float,
                owner_id: str,
                **kwargs):
        """Initialize a new Place instance.
        
        Args:
            title (str): Title of the place
            description (str): Detailed description
            price (float): Price per night
            latitude (float): Geographic latitude
            longitude (float): Geographic longitude
            owner_id (str): ID of the user who owns this place
            **kwargs: Additional attributes from BaseModel
        """
        super().__init__(**kwargs)
        self.title = title
        self.description = description
        # Use property setters for validation
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id
        self.reviews: List['Review'] = []
        self.amenities: List['Amenity'] = []

    # --------------------
    # Property validations
    # --------------------
    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, value: float):
        try:
            value = float(value)
        except (TypeError, ValueError):
            raise ValueError("price must be a number")
        if value < 0:
            raise ValueError("price must be non-negative")
        self._price = value

    @property
    def latitude(self) -> float:
        return self._latitude

    @latitude.setter
    def latitude(self, value: float):
        try:
            value = float(value)
        except (TypeError, ValueError):
            raise ValueError("latitude must be a number")
        if not -90 <= value <= 90:
            raise ValueError("latitude must be between -90 and 90")
        self._latitude = value

    @property
    def longitude(self) -> float:
        return self._longitude

    @longitude.setter
    def longitude(self, value: float):
        try:
            value = float(value)
        except (TypeError, ValueError):
            raise ValueError("longitude must be a number")
        if not -180 <= value <= 180:
            raise ValueError("longitude must be between -180 and 180")
        self._longitude = value