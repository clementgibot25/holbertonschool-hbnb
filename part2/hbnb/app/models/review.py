#!/usr/bin/python3

from app.models.base_model import BaseModel
from app.models.place import Place
from app.models.user import User

class Review(BaseModel):
    def __init__(self,
                text: str,
                rating: int,
                place: Place,
                user: User,
                **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user
