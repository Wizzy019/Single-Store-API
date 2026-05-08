from typing import Optional

from pydantic import BaseModel
from decimal import Decimal


class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int
    price: Optional[Decimal] = None

class OrderCreate(BaseModel):
    items: list[OrderItemCreate]