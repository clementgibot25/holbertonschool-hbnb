#!/usr/bin/python3

from typing import List, Optional
from app.models.amenity import Amenity
from app.persistence.repository import InMemoryRepository

class AmenityService:
    def __init__(self, repository: InMemoryRepository = None):
        self.repository = repository or InMemoryRepository()
    
    def create_amenity(self, name: str) -> Amenity:
        if not name:
            raise ValueError("Le nom de l'équipement ne peut pas être vide")
            
        # Vérifie si un équipement avec ce nom existe déjà
        existing = self.get_amenity_by_name(name)
        if existing:
            return existing
            
        amenity = Amenity(name=name)
        self.repository.add(amenity)
        return amenity
    
    def get_amenity(self, amenity_id: str) -> Optional[Amenity]:
        return self.repository.get(amenity_id)
    
    def get_amenity_by_name(self, name: str) -> Optional[Amenity]:
        amenities = self.repository.get_all()
        for amenity in amenities:
            if hasattr(amenity, 'name') and amenity.name == name:
                return amenity
        return None
    
    def get_all_amenities(self) -> List[Amenity]:
        return self.repository.get_all()
    
    def update_amenity(self, amenity_id: str, **updates) -> Optional[Amenity]:
        if 'name' in updates and not updates['name']:
            raise ValueError("Le nom de l'équipement ne peut pas être vide")
        return self.repository.update(amenity_id, updates)
    
    def delete_amenity(self, amenity_id: str) -> bool:
        if self.repository.get(amenity_id):
            self.repository.delete(amenity_id)
            return True
        return False

# Instance unique du service des équipements
amenity_service = AmenityService()