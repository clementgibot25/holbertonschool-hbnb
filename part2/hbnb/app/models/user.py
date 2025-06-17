#!/usr/bin/python3

from app.models.base_model import BaseModel

class User(BaseModel):
    def __init__(self, email: str, password_hash: str,
                 first_name: str,
                 last_name: str,
                 is_admin: bool = False,
                 **kwargs):
        super().__init__(**kwargs)
        self.email = email
        self.password_hash = password_hash
        self.first_name = first_name
        self.last_name = last_name
        self.is_admin = is_admin
