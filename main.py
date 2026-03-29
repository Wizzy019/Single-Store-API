from fastapi import FastAPI, Depends, HTTPException
import models, schemas, crud
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from database import engine, get_db
from sqlalchemy.orm import Session
from auth import create_access_token, SECRET_KEY, ALGORITHM
from jose import jwt, JWTError

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")  # matches what we stored in token
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(models.User).filter(models.User.email == email).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user
    

@app.post("/signup")
def signup(user: schemas.UserCreate, db:Session = Depends(get_db)):
    created = crud.create_user(db, user.name, user.email, user.password)
    if created is None:
        raise HTTPException(status_code=404, detail="Email already registered")
    return created

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/Protected")
def protected_route(current_user: models.User = Depends(get_current_user)):
    return {
        "messagee": "Access granted",
        "user": {
            "id" : current_user.id,
            "email": current_user.email,
            "name": current_user.name
        }
    }

@app.post("/products")
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    new_product = crud.create_product(db, product.name, product.price, product.stock, product.description)
    if new_product is None:
        raise HTTPException(status_code=400, detail="Failed to create new product")
    return new_product

@app.post("/orders")
def create_order_endpoint(order: schemas.OrderCreate,
                          db: Session = Depends(get_db),
                          current_user: models.User = Depends(get_current_user)):
    if not order.items:
        raise HTTPException(status_code=400, detail="Order must have at least one item")
    
    new_order = crud.create_order(db, user_id=current_user.id, order_items=order.items)
    return new_order