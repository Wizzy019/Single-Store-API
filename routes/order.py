from fastapi import APIRouter, Depends, HTTPException
from schemas.order import OrderCreate
from models.user import User
from crud.order import create_order
from database.connection import get_db
from sqlalchemy.orm import Session
from auth.dependencies import user_only

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/")
def create_order_endpoint(order: OrderCreate,
                          db: Session = Depends(get_db),
                          current_user: User = Depends(user_only)):
    if not order.items:
        raise HTTPException(status_code=400, detail="Order must have at least one item")
    
    new_order = create_order(db, user_id=current_user.id, order_items=order.items)
    return new_order