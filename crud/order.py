from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.products import Product
from models.order import Order, OrderItem

def create_order(db: Session, user_id: int, order_items: list):
    total_price = 0

    new_order = Order(
        user_id=user_id,
        total_price=0,  # temporary
        status="pending"
    )
    db.add(new_order)
    db.flush()  # get order ID

    for item in order_items:
        product = db.query(Product).filter(
           Product.id == item.product_id
        ).first()

        if not product:
            raise Exception("Product not found")

        if item.quantity > product.stock:
            raise HTTPException(status_code=400, detail="Not enough stock")

        total_price += item.quantity * product.price

        product.stock -= item.quantity

        db_item = OrderItem(
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