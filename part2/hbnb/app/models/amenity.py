#!/usr/bin/python3

from app.models.base_model import BaseModel

class Amenity(BaseModel):
    def __init__(self,
                name: str,
                **kwargs):
        super().__init__(**kwargs)
        self.name = name
