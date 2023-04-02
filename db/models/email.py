from pymongo import MongoClient
from typing import Optional
from pydantic import BaseModel

class UserEmail(BaseModel):
    email: str