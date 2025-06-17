#!/usr/bin/python3

from app.models.base_model import BaseModel
from typing import List, Optional

class Place(BaseModel):
    def __init__(self,
                title: str,
                description: str,
                price: float,
                latitude: float,
                longitude: float,
                owner_id: str,  # Utilisation de l'ID du propriétaire
                **kwargs):
        super().__init__(**kwargs)
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id  # Stockage de l'ID du propriétaire
        self.reviews: List['Review'] = []
        self.amenities: List['Amenity'] = []

    def add_review(self, review: 'Review') -> None:
        """Ajoute un avis à la place"""
        if review not in self.reviews:
            self.reviews.append(review)
            if review.place_id != self.id:
                review.place_id = self.id

    def add_amenity(self, amenity: 'Amenity') -> None:
        """Ajoute un équipement à la place"""
        if amenity not in self.amenities:
            self.amenities.append(amenity)