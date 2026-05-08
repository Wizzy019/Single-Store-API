from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, DateTime, func
from sqlalchemy.orm import relationship
from database.connection import Base


class Order(Base):
    __tablename__ = "single_store_orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("single_store_users.id"), nullable=False)
    total_price = Column(Numeric(12, 2), nullable=False)
    status = Column(String, default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship to items
    items = relationship(
        "OrderItem", back_populates="order", cascade="all, delete-orphan"
    )


class OrderItem(Base):
    __tablename__ = "single_store_order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("single_store_orders.id"), nullable=False)
    product_id = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)

    # Relationship back to order
    order = relationship("Order", back_populates="items")