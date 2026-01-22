from pydantic import BaseModel, EmailStr
from datetime import datetime, date

class UserSchema(BaseModel):
    role:str
    email: EmailStr
    created_at: datetime

class loginSchema(BaseModel):
    email: EmailStr
    password: str

class UploadSchema(BaseModel):
    filename: str
    uploaded_at: datetime

class TransactionSchema(BaseModel):
    date: date
    description: str
    amount: float
    category: str

from pydantic import BaseModel
from typing import List

class CategorySchema(BaseModel):
    name: str
    keywords: List[str]
    active: bool = True
