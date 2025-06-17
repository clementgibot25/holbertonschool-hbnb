#!/usr/bin/python3

from app.models.base_model import BaseModel

class Review(BaseModel):
    def __init__(self,
                text: str,
                rating: int,
                place_id: str,
                user_id: str,
                **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.rating = rating
        self.place_id = place_id
        self.user_id = user_id