"""In-memory implementation of the Repository pattern.

This module provides a simple in-memory storage implementation of the Repository
interface, primarily used for testing and development purposes.
"""

from typing import Any, Dict, List, Optional, TypeVar, Generic
from app.persistence.repository import Repository

T = TypeVar('T')

class InMemoryRepository(Repository[T]):
    """In-memory implementation of the Repository interface.
    
    This implementation stores objects in a dictionary in memory.
    It's not persistent between application restarts.
    """
    
    def __init__(self):
        """Initialize a new in-memory repository with empty storage."""
        self._storage: Dict[str, T] = {}

    def add(self, obj: T) -> T:
        """Add a new object to the repository.
        
        Args:
            obj: The object to add (must have an 'id' attribute)
            
        Returns:
            The added object
            
        Note:
            The object's ID will be used as the dictionary key
        """
        self._storage[obj.id] = obj
        return obj

    def get(self, obj_id: str) -> Optional[T]:
        """Retrieve an object by its ID.
        
        Args:
            obj_id: The unique identifier of the object
            
        Returns:
            The object if found, None otherwise
        """
        return self._storage.get(obj_id)

    def get_all(self) -> List[T]:
        """Retrieve all objects in the repository.
        
        Returns:
            A list of all objects in the repository
        """
        return list(self._storage.values())

    def update(self, obj_id: str, data: Dict[str, Any]) -> Optional[T]:
        """Update an existing object.
        
        Args:
            obj_id: The ID of the object to update
            data: Dictionary of attributes to update
            
        Returns:
            The updated object if found, None otherwise
            
        Note:
            The object must implement an 'update' method that accepts a dictionary
            of attributes to update.
        """
        obj = self.get(obj_id)
        if obj:
            obj.update(data)
            return obj
        return None

    def delete(self, obj_id: str) -> bool:
        """Delete an object from the repository.
        
        Args:
            obj_id: The ID of the object to delete
            
        Returns:
            True if the object was deleted, False otherwise
        """
        if obj_id in self._storage:
            del self._storage[obj_id]
            return True
        return False

    def get_by_attribute(self, attr_name: str, attr_value: Any) -> List[T]:
        """Find objects by a specific attribute value.
        
        Args:
            attr_name: Name of the attribute to search by
            attr_value: Value to match against
            
        Returns:
            A list of matching objects, empty if none found
            
        Note:
            Returns only the first matching object as a single-item list
            for backward compatibility with existing code.
        """
        result = next(
            (obj for obj in self._storage.values() 
             if getattr(obj, attr_name, None) == attr_value),
            None
        )
        return [result] if result is not None else []
