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
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id
        self.reviews: List['Review'] = []
        self.amenities: List['Amenity'] = []

    def add_review(self, review: 'Review') -> None:
        """Add a review to this place.
        
        Args:
            review (Review): Review instance to add
        """
        if review not in self.reviews:
            self.reviews.append(review)
            if review.place_id != self.id:
                review.place_id = self.id

    def add_amenity(self, amenity: 'Amenity') -> None:
        """Add an amenity to this place.
        
        Args:
            amenity (Amenity): Amenity instance to add
        """
        if amenity not in self.amenities:
            self.amenities.append(amenity)