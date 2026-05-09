from pydantic import BaseModel
from decimal import Decimal
from typing import Optional
from utils.cleanbasemodel import CleanBaseModel

class ProductCreate(BaseModel):
    name: str
    price: Decimal
    stock: int
    description:str

class ProductUpdate(CleanBaseModel):
    name: Optional[str] = None 
    price: Optional[Decimal] = None
    stock: Optional[int] = None
    description: Optional[str] = None

