from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import models, schemas, crud
from database import engine, get_db
from sqlalchemy.orm import Session
from auth.dependencies import get_current_user, admin_only, user_only
from routes.auth import router as auth_router

app = FastAPI()

app.include_router(auth_router)

models.Base.metadata.create_all(bind=engine) 

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db), current_user: models.User = Depends(admin_only)):
    new_product = crud.create_product(db, product.name, product.price, product.stock, product.description)
    if new_product is None:
        raise HTTPException(status_code=400, detail="Failed to create new product")
    return new_product

@app.post("/orders")
def create_order_endpoint(order: schemas.OrderCreate,
                          db: Session = Depends(get_db),
                          current_user: models.User = Depends(user_only)):
    if not order.items:
        raise HTTPException(status_code=400, detail="Order must have at least one item")
    
    new_order = crud.create_order(db, user_id=current_user.id, order_items=order.items)
    return new_order