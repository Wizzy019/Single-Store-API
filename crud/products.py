from sqlalchemy.orm import Session
from models.products import Product

def create_product(db:Session, name:str, price:int, stock:int, description:str):
    product = Product(name=name, price=price, stock=stock, description=description)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product
