from sqlalchemy.orm import Session
from auth import hash_password, verify_password
import model
import schemas

def create_user(db:Session, user:schemas.UserCreate):
    hashed_password = hash_password