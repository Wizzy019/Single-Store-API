from fastapi import APIRouter, Depends, HTTPException
from models.user import User
from schemas.products import ProductCreate
from crud.products import create_product as create_product_crud
from database.connection import get_db
from sqlalchemy.orm import Session
from auth.dependencies import admin_only

router = APIRouter(prefix="/products", tags=["Products"])

@router.post("/")
def create_product_endpoint(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_only)
):
    new_product = create_product_crud(
        db,
        product.name,
        product.price,
        product.stock,
        product.description
    )

    if not new_product:
        raise HTTPException(status_code=400, detail="Failed to create product")

    return new_product