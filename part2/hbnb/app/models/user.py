#!/usr/bin/python3

from app.models.base_model import BaseModel
class User(BaseModel):
    def __init__(self):
        super().__init__()
        self.email = str
        self.first_name = str
        self.last_name = str
        self.is_admin = bool
