#!/usr/bin/python3

from app.models.base_model import BaseModel

class Review(BaseModel):
    def __init__(self):
        super().__init__()
        self.text = None
        self.rating = None
        self.place = None
        self.user = None
