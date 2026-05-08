from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database.connection import engine
from database.connection import Base

from models.user import User
from models.products import Product
from models.order import Order

from routes.auth import router as auth_router
from routes.products import router as product_router
from routes.order import router as order_router
from routes.user import router as user_router

app = FastAPI()

Base.metadata.create_all(bind=engine) 

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(product_router)
app.include_router(order_router)
app.include_router(user_router)