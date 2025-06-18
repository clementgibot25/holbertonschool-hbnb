#!/usr/bin/python3

from typing import List, Optional
from app.models.review import Review
from app.persistence.repository import InMemoryRepository

""" à voir si on rajoute des trucs pour admin dans le service """

class ReviewService:
    def __init__(self, repository: InMemoryRepository = None):
        self.repository = repository or InMemoryRepository()
    
    def create_review(self, text: str, rating: int, 
                     place_id: str, user_id: str) -> Review:
        review = Review(
            text=text,
            rating=rating,
            place_id=place_id,
            user_id=user_id
        )
        self.repository.add(review)
        return review
    
    def get_review(self, review_id: str) -> Optional[Review]:
        return self.repository.get(review_id)
    
    def get_all_reviews(self) -> List[Review]:
        return self.repository.get_all()
    
    def get_reviews_by_place(self, place_id: str) -> List[Review]:
        return [r for r in self.repository.get_all() 
                if getattr(r, 'place_id', None) == place_id]
    
    def get_reviews_by_user(self, user_id: str) -> List[Review]:
        return [r for r in self.repository.get_all() 
                if getattr(r, 'user_id', None) == user_id]
    
    def update_review(self, review_id: str, **updates) -> Optional[Review]:
        return self.repository.update(review_id, updates)
    
    def delete_review(self, review_id: str) -> bool:
        if self.repository.get(review_id):
            self.repository.delete(review_id)
            return True
        return False

# Instance unique du service des avis
review_service = ReviewService()