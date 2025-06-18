#!/usr/bin/python3

from typing import List, Optional
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.review import Review
from app.persistence.repository import InMemoryRepository

class PlaceService:
    def __init__(self, repository: InMemoryRepository = None):
        self.repository = repository or InMemoryRepository()
    
    def create_place(self, title: str, description: str, price: float,
                latitude: float, longitude: float, owner_id: str) -> Optional[Place]:
        # Création de la place
        place = Place(
            title=title,
            description=description,
            price=price,
            latitude=latitude,
            longitude=longitude,
            owner_id=owner_id
        )
        place.reviews = []
        place.amenities = []
    
        # Sauvegarde de la place
        self.repository.add(place)
    
        # Mise à jour de la liste des places de l'utilisateur
        from app.services import user_service
        user_service.add_user_place(owner_id, place.id)
    
        return place
    
    def delete_place(self, place_id: str) -> bool:
        place = self.get_place(place_id)
        if not place:
            return False
    
        # Nettoyage des références
        from app.services import user_service
        user = user_service.get_user(place.owner_id)
        if user and place_id in user.places:
            user.places.remove(place_id)
    
        # Suppression de la place
        self.repository.delete(place_id)
        return True
    
    def add_review(self, place_id: str, review: Review) -> bool:
        """Ajoute un avis à la place"""
        place = self.get_place(place_id)
        if not place:
            return False
            
        if review not in place.reviews:
            place.reviews.append(review)
            if review.place_id != place_id:
                review.place_id = place_id
            return True
        return False
    
    def get_place_reviews(self, place_id: str) -> List[Review]:
        """Récupère tous les avis d'une place"""
        place = self.get_place(place_id)
        return place.reviews if place else []
    
    def add_amenity(self, place_id: str, amenity: Amenity) -> bool:
        """Ajoute un équipement à la place"""
        place = self.get_place(place_id)
        if not place:
            return False
            
        if amenity not in place.amenities:
            place.amenities.append(amenity)
            return True
        return False
    
    def get_place_amenities(self, place_id: str) -> List[Amenity]:
        """Récupère tous les équipements d'une place"""
        place = self.get_place(place_id)
        return place.amenities if place else []
    
    def remove_amenity(self, place_id: str, amenity: Amenity) -> bool:
        """Supprime un équipement de la place"""
        place = self.get_place(place_id)
        if not place or amenity not in place.amenities:
            return False
            
        place.amenities.remove(amenity)
        return True

# Instance unique du service des lieux
place_service = PlaceService()