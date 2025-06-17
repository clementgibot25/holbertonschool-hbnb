#!/usr/bin/python3

class BaseModel:
    def __init__(self):
        self.id = None
        self.created_at = None
        self.updated_at = None
    
    def touch(self):
        self.updated_at = datetime.now()

    def to_dict(self):
        return {
            'id': self.id,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
