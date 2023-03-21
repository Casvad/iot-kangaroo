import os

from pydantic import BaseModel


class User(BaseModel):
    id: str = os.urandom(24).hex()
    email: str
    password: str
