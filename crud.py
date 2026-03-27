from sqlalchemy.orm import Session
from auth import hash_password, verify_password
import models, schemas

def create_user(db:Session, name:str, email:str, password:str):
    hashed = hash_password(password)
    user = models.User(name=name, email=email, hashed_password=hashed)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def authenticate_user(db, email, password):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

def create_product(db:Session, name:str, price:int, stock:int, description:str):
    product = models.Product(name=name, price=price, stock=stock, description=description)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

# crud.py
def create_order(db: Session, user_id: int, order_items: list):
    # Calculate total_price automatically
    total_price = sum(item.quantity * item.price for item in order_items)
    
    new_order = models.Order(
        user_id=user_id,
        total_price=total_price,
        status="pending"
    )
    db.add(new_order)
    db.flush()  # assign new_order.id
    
    # Add each order item
    for item in order_items:
        db_item = models.OrderItem(
            order_id=new_order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=item.price
        )
        db.add(db_item)
    
    db.commit()
    db.refresh(new_order)
    return new_order