from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from auth.dependencies import admin_only
from auth.jwt_handler import create_access_token
from schemas.user import UserCreate
from crud.user import create_user, create_admin, authenticate_user
from database.connection import get_db

router = APIRouter(prefix="/auth", tags=["Auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@router.post("/signup")
def signup(user: UserCreate, db:Session = Depends(get_db)):
    created = create_user(db, user.name, user.email, user.password, user.role)
    if created is None:
        raise HTTPException(status_code=400, detail="Email already registered")
    return created

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token( data={"sub": user.email,})

    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register-admin", dependencies=[Depends(admin_only)])
def register_admin(user: UserCreate, db:Session = Depends(get_db)):
    created = create_admin(db, user.name, user.email, user.password, user.role)

    if created is None:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    return created


