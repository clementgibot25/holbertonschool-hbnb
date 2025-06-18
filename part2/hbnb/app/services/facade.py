# app/services/facade.py
# Import service classes
from .user_service import UserService
from .place_service import PlaceService
from .review_service import ReviewService
from .amenity_service import AmenityService
# Import specific repository implementations
from typing import Dict, Optional, List
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from app.persistence.repository import InMemoryRepository


class HBnBFacade:
    """
    Façade principale de l'application HBnB qui fournit une interface unifiée
    pour accéder aux différentes fonctionnalités de l'application.
    """
    
    def __init__(self):
        # Initialisation des repositories
        user_repo = InMemoryRepository()
        place_repo = InMemoryRepository()
        review_repo = InMemoryRepository()
        amenity_repo = InMemoryRepository()
        
        # Initialisation des services avec leurs repositories respectifs
        self.user_service = UserService(user_repo)
        self.place_service = PlaceService(place_repo)
        self.review_service = ReviewService(review_repo)
        self.amenity_service = AmenityService(amenity_repo)
    
    # Méthodes utilisateur
    def create_user(self, email: str, password_hash: str, first_name: str, 
                   last_name: str, is_admin: bool = False) -> User:
        """Crée un nouvel utilisateur"""
        return self.user_service.create_user(
            email=email,
            password_hash=password_hash,
            first_name=first_name,
            last_name=last_name,
            is_admin=is_admin
        )
    
    def get_user(self, user_id: str) -> Optional[User]:
        """Récupère un utilisateur par son ID"""
        return self.user_service.get_user(user_id)
    
    # Méthodes de lieu
    def create_place(self, **kwargs) -> Place:
        """Crée un nouveau lieu"""
        return self.place_service.create_place(**kwargs)
    
    def get_place(self, place_id: str) -> Optional[Place]:
        """Récupère un lieu par son ID"""
        return self.place_service.get_place(place_id)
    
    # Méthodes d'avis
    def create_review(self, **kwargs) -> Review:
        """Crée un nouvel avis"""
        return self.review_service.create_review(**kwargs)
    
    # Méthodes de commodité
    def get_amenities(self) -> List[Amenity]:
        """Récupère toutes les commodités"""
        return self.amenity_service.get_all_amenities()
    
    def search_places(self, **filters) -> List[Place]:
        """Recherche des lieux selon des critères"""
        return self.place_service.search_places(**filters)


# Instance unique de la façade
hbnb_facade = HBnBFacade()