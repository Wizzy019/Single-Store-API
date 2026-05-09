from fastapi import APIRouter, Depends, HTTPException
from schemas.order import OrderCreate
from models.user import User
from crud.order import create_order, get_orders, get_order
from database.connection import get_db
from sqlalchemy.orm import Session
from auth.dependencies import user_only, admin_only, get_current_user

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/")
def create_order_endpoint(order: OrderCreate,
                          db: Session = Depends(get_db),
                          current_user: User = Depends(user_only)):
    if not order.items:
        raise HTTPException(status_code=400, detail="Order must have at least one item")
    
    new_order = create_order(db, user_id=current_user.id, order_items=order.items)
    return new_order

@router.get("/", dependencies=[Depends(admin_only)])
def get_all_orders(db: Session = Depends(get_db)):
    return get_orders(db)


@router.get("/my_orders")
def get_single_order( db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    current_user_id = current_user.id

    order = get_order(db, user_id = current_user_id)

    if not order:
        raise HTTPException(status_code=404, detail="No order found for this user")
    return order