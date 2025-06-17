# app/services/facade.py
# Import service classes
from .user_service import UserService
from .place_service import PlaceService
from .review_service import ReviewService
from .amenity_service import AmenityService
# Import specific repository implementations
from app.persistence.in_memory_user_repository import InMemoryUserRepository
from app.persistence.in_memory_place_repository import InMemoryPlaceRepository
from app.persistence.in_memory_review_repository import InMemoryReviewRepository
from app.persistence.in_memory_amenity_repository import InMemoryAmenityRepository
class HBnBFacade:
    def __init__(self):
        # 1. Instantiate SPECIFIC Repositories
        user_repo = InMemoryUserRepository()
        place_repo = InMemoryPlaceRepository()
        review_repo = InMemoryReviewRepository()
        amenity_repo = InMemoryAmenityRepository()
        # 2. Instantiate Services, INJECTING them with Repositories
        self.user_service = UserService(user_repo)
        self.place_service = PlaceService(place_repo)
        self.review_service = ReviewService(review_repo)
        self.amenity_service = AmenityService(amenity_repo)
    # Example method in the Facade that DELEGATES to the Service
    def create_user_api(self, user_data: dict):
        # The Facade calls the Service to handle business logic
        user_domain_obj = self.user_service.create_user(
            username=user_data['username'],
            email=user_data['email'],
            password=user_data['password']
        )
        return user_domain_obj # The service returns a User domain model object
    # Placeholder method for creating a user
    def create_user(self, user_data):
        # Logic will be implemented in later tasks
        pass

    # Placeholder method for fetching a place by ID
    def get_place(self, place_id):
        # Logic will be implemented in later tasks
        pass