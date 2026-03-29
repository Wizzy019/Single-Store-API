from fastapi import HTTPException
from sqlalchemy.orm import Session
from auth import hash_password, verify_password
import models

def create_user(db:Session, name:str, email:str, password:str):
    hashed = hash_password(password)
    user = models.User(name=name, email=email, hashed_password=hashed)

    existing = db.query(models.User).filter(models.User.email == email).first()
    if existing:
        return None
    
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

def create_order(db: Session, user_id: int, order_items: list):
    total_price = 0

    new_order = models.Order(
        user_id=user_id,
        total_price=0,  # temporary
        status="pending"
    )
    db.add(new_order)
    db.flush()  # get order ID

    for item in order_items:
        product = db.query(models.Product).filter(
            models.Product.id == item.product_id
        ).first()

        if not product:
            raise Exception("Product not found")

        if item.quantity > product.stock:
            raise HTTPException(status_code=400, detail="Not enough stock")

        total_price += item.quantity * product.price

        product.stock -= item.quantity

        db_item = models.OrderItem(
            order_id=new_order.id,
            product_id=product.id,
            quantity=item.quantity,
            price=product.price
        )
        db.add(db_item)

    # ✅ Set correct total price
    new_order.total_price = total_price

    db.commit()
    db.refresh(new_order)
    return new_order