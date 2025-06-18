#!/usr/bin/python3

import unittest
from app.models.amenity import Amenity

class TestAmenity(unittest.TestCase):
    """Test cases for the Amenity model"""
    
    def test_amenity_creation(self):
        """Test creating a new amenity"""
        amenity = Amenity(name="Wi-Fi")
        
        self.assertEqual(amenity.name, "Wi-Fi")
        self.assertIsNotNone(amenity.id)
        self.assertIsNotNone(amenity.created_at)
        self.assertIsNotNone(amenity.updated_at)
    
    def test_amenity_str_representation(self):
        """Test the string representation of Amenity"""
        amenity = Amenity(name="Swimming Pool")
        
        self.assertIn("Amenity", str(amenity))
        self.assertIn(amenity.id, str(amenity))
        self.assertIn("Swimming Pool", str(amenity))
    
    def test_amenity_update(self):
        """Test updating an amenity's name"""
        amenity = Amenity(name="Old Name")
        old_updated_at = amenity.updated_at
        
        # Update the name
        amenity.name = "New Name"
        amenity.save()
        
        self.assertEqual(amenity.name, "New Name")
        self.assertNotEqual(amenity.updated_at, old_updated_at)

if __name__ == '__main__':
    unittest.main()