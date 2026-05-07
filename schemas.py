from typing import Optional

from pydantic import BaseModel, EmailStr
from decimal import Decimal

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class ProductCreate(BaseModel):
    name: str
    price: Decimal
    stock: int
    description:str

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int
    price: Optional[Decimal] = None

class OrderCreate(BaseModel):
    items: list[OrderItemCreate]