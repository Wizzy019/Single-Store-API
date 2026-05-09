from fastapi import APIRouter, Depends, HTTPException
from models.user import User
from schemas.products import ProductCreate, ProductUpdate
from crud.products import create_product as create_product_crud, get_products, get_product, update_product as update_product_crud, delete_product as delete_product_crud
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

@router.get("/")
def get_all_products(db: Session = Depends(get_db)):
    return get_products(db)

@router.get("/{product_id}")
def get_single_product(product_id: int, db: Session = Depends(get_db)):
    product = get_product(db, product_id)

    if not product:
        raise HTTPException(status_code=404, detail="Product nor found")
    
    return product

@router.patch("/{product_id}")
def update_product(
    product_id: int,
    data: ProductUpdate,
    db: Session = Depends(get_db),
    __: User = Depends(admin_only)
):
    updated = update_product_crud(db, product_id, data)

    if not updated:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return updated

@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db),_: User = Depends(admin_only)):

    deleted = delete_product_crud(db, product_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return{
        "Succes" : f"product {product_id} deleted"
    }