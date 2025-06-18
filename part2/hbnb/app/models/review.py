#!/usr/bin/python3

"""Defines the Review model for the application."""

from app.models.base_model import BaseModel

class Review(BaseModel):
    """Represents a user review for a place.
    
    Attributes:
        text (str): The review content
        rating (int): Rating from 1 to 5
        place_id (str): ID of the reviewed place
        user_id (str): ID of the user who wrote the review
    """
    
    def __init__(self,
                text: str,
                rating: int,
                place_id: str,
                user_id: str,
                **kwargs):
        """Initialize a new Review instance.
        
        Args:
            text (str): The review content
            rating (int): Rating from 1 to 5
            place_id (str): ID of the reviewed place
            user_id (str): ID of the user who wrote the review
            **kwargs: Additional attributes from BaseModel
        """
        super().__init__(**kwargs)
        self.text = text
        self.rating = rating
        self.place_id = place_id
        self.user_id = user_id