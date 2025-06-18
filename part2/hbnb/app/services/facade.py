"""Facade module providing a unified interface to the HBnB application services.

This module implements the Facade pattern to provide a simplified interface
to the complex subsystem of services and repositories in the application.
"""

from typing import Dict, Optional, List
from .user_service import UserService
from .place_service import PlaceService
from .review_service import ReviewService
from .amenity_service import AmenityService
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from app.persistence.in_memory_repository import InMemoryRepository


class HBnBFacade:
    """Main facade for the HBnB application.
    
    This class provides a unified interface to access all the application's
    functionality, abstracting away the complexity of the underlying services
    and repositories.
    """
    
    def __init__(self):
        """Initialize the HBnB facade with all required services and repositories.
        
        Sets up in-memory repositories and initializes the corresponding services.
        """
        # Initialize repositories
        user_repo = InMemoryRepository()
        place_repo = InMemoryRepository()
        review_repo = InMemoryRepository()
        amenity_repo = InMemoryRepository()
        
        # Initialize services with their respective repositories
        self.user_service = UserService(user_repo)
        self.place_service = PlaceService(place_repo)
        self.review_service = ReviewService(review_repo)
        self.amenity_service = AmenityService(amenity_repo)
    
    # User methods
    def create_user(self, email: str, password_hash: str, first_name: str, 
                   last_name: str, is_admin: bool = False) -> User:
        """Create a new user.
        
        Args:
            email: User's email address (must be unique)
            password_hash: Hashed password for security
            first_name: User's first name
            last_name: User's last name
            is_admin: Whether the user has admin privileges
            
        Returns:
            The newly created User instance
        """
        return self.user_service.create_user(
            email=email,
            password_hash=password_hash,
            first_name=first_name,
            last_name=last_name,
            is_admin=is_admin
        )
    
    def get_user(self, user_id: str) -> Optional[User]:
        """Retrieve a user by their ID.
        
        Args:
            user_id: The unique identifier of the user
            
        Returns:
            The User instance if found, None otherwise
        """
        return self.user_service.get_user(user_id)
    
    # Place methods
    def create_place(self, **kwargs) -> Place:
        """Create a new place.
        
        Args:
            **kwargs: Keyword arguments for place creation
            
        Returns:
            The newly created Place instance
        """
        return self.place_service.create_place(**kwargs)
    
    def get_place(self, place_id: str) -> Optional[Place]:
        """Retrieve a place by its ID.
        
        Args:
            place_id: The unique identifier of the place
            
        Returns:
            The Place instance if found, None otherwise
        """
        return self.place_service.get_place(place_id)
    
    # Review methods
    def create_review(self, **kwargs) -> Review:
        """Create a new review.
        
        Args:
            **kwargs: Keyword arguments for review creation
            
        Returns:
            The newly created Review instance
        """
        return self.review_service.create_review(**kwargs)
    
    # Amenity methods
    def get_amenities(self) -> List[Amenity]:
        """Retrieve all amenities.
        
        Returns:
            A list of all Amenity instances
        """
        return self.amenity_service.get_all_amenities()
    
    def search_places(self, **filters) -> List[Place]:
        """Search for places based on filters.
        
        Args:
            **filters: Keyword arguments for filtering places
            
        Returns:
            A list of Place instances matching the filters
        """
        return self.place_service.search_places(**filters)

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Retrieve a user by their email address.
        
        Args:
            email: The email address to search for
            
        Returns:
            The User instance if found, None otherwise
        """
        return self.user_service.get_user_by_email(email)

# Singleton instance of the facade
hbnb_facade = HBnBFacade()