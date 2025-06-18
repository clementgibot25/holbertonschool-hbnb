#!/usr/bin/python3

from typing import List, Optional
from app.models.user import User
from app.persistence.repository import InMemoryRepository


class UserService:
    def __init__(self, repository: InMemoryRepository = None):
        self.repository = repository or InMemoryRepository()
    
    def create_user(self, email: str, password_hash: str, first_name: str, 
                   last_name: str, is_admin: bool = False) -> User:
        if self.get_user_by_email(email):
            raise ValueError(f"Un utilisateur avec l'email {email} existe déjà.")
        
        # Crée le nouvel utilisateur
        user = User(
            email=email,
            password_hash=password_hash,
            first_name=first_name,
            last_name=last_name,
            is_admin=is_admin
        )
        
        # Sauvegarde l'utilisateur
        self.repository.add(user)
        return user
    
    def get_user(self, user_id: str) -> Optional[User]:
        return self.repository.get(user_id)
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        return self.repository.get_by_attribute('email', email)
    
    def get_all_users(self) -> List[User]:
        return self.repository.get_all()
    
    def update_user(self, user_id: str, **updates) -> Optional[User]:
        if 'email' in updates and updates['email']:
            existing = self.get_user_by_email(updates['email'])
            if existing and existing.id != user_id:
                raise ValueError(f"Un utilisateur avec l'email {updates['email']} existe déjà.")
        
        return self.repository.update(user_id, updates)
    
    def delete_user(self, user_id: str) -> bool:
        if self.repository.get(user_id):
            self.repository.delete(user_id)
            return True
        return False
    
    def authenticate(self, email: str, password_hash: str) -> Optional[User]:
        user = self.get_user_by_email(email)
        if user and user.password_hash == password_hash:
            return user
        return None
    
    def add_user_place(self, user_id: str, place_id: str) -> bool:
        """Ajoute une place à la liste des propriétés de l'utilisateur"""
        user = self.get_user(user_id)
        if not user:
            return False
            
        if place_id not in user.places:
            user.places.append(place_id)
            return True
        return False
    
    def get_user_places(self, user_id: str) -> List[str]:
        """Retourne la liste des IDs des places appartenant à l'utilisateur"""
        user = self.get_user(user_id)
        return user.places if user else []

# Instance unique du service utilisateur
user_service = UserService()
