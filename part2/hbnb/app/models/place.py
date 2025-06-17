#!/usr/bin/python3

from app.models.base_model import BaseModel

class Place(BaseModel):
    def __init__(self):
        super().__init__()
        self.title = None
        self.description = None
        self.price = None
        self.latitude = None
        self.longitude = None
        self.owner = None
        