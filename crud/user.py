from sqlalchemy.orm import Session
from auth.password import hash_password, verify_password
from models.user import User


def create_user(db:Session, name:str, email:str, password:str, role:str):
    hashed = hash_password(password)
    user = User(name=name, email=email, hashed_password=hashed, role="user")

    existing = db.query(User).filter(User.email == email).first()
    if existing:
        return None
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def create_admin(db:Session, name:str, email:str, password:str, role:str):
    hashed = hash_password(password)

    admin = User(
        name = name,
        email = email,
        hashed_password = hashed,
        role = "admin"
    )

    existing = db.query(User).filter(User.email == email).first()
    if existing:
        return None
    
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return admin


def authenticate_user(db, email, password):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user