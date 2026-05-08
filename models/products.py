from sqlalchemy import Column, Integer, String, Numeric
from sqlalchemy.orm import relationship
from database.connection import Base


class Product(Base):
    __tablename__ = "single_store_products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    stock = Column(Integer, nullable=False)
    description = Column(String, nullable=False)