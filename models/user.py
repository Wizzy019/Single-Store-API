from sqlalchemy import Column, Integer, String
from database.connection import Base


class User(Base):
    __tablename__ = "single_store_users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="user")