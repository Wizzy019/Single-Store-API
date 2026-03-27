from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String,nullable=False)
    price = Column(Integer, nullable=False)
    stock = Column(Integer, nullable=False)
    description = Column(String, nullable=False)

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(ForeignKey("users.id"), Integer, nullable=False)
    total_price = Column(Integer, nullable=False)
    status = Column(String, nullable=False)

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(ForeignKey("orders.id"), Integer, nullable=False)
    product_id = Column(ForeignKey("products.id"), Integer, nullable=False)
    quantity = Column(Integer, nullable=False)