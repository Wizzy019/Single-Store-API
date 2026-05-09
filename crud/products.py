from sqlalchemy.orm import Session
from models.products import Product
from database.connection import get_db

def create_product(db:Session, name:str, price:int, stock:int, description:str):
    product = Product(name=name, price=price, stock=stock, description=description)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def get_products(db):
    return db.query(Product).all()

def get_product(db, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()

def update_product(db, product_id, data):

    product = db.query(Product).filter(Product.id == product_id).first()
    
    if not product:
        return None

    if data.name is not None:
        product.name = data.name
    if data.price is not None:
        product.price = data.price
    if data.stock is not None:
        product.stock = data.stock
    if data.description is not None:
        product.description = data.description

    db.commit()
    db.refresh(product)
    return product

def delete_product(db, product_id):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        return None
    
    db.delete(product)
    db.commit()

    return product