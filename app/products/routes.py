
from typing import List
from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.auth.models import User
from app.auth.utils import get_current_user
from app.core.database import get_db
from app.products import schemas, models

router = APIRouter()

@router.post("/", response_model=schemas.ProductOut)
def create_product( product_data: schemas.CreateProduct,db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")

    product = models.Product(**product_data.model_dump(), created_by=current_user.id)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

@router.get("/", response_model=List[schemas.ProductOut])
def get_products(start: int = 0, end: int = 10, db: Session = Depends(get_db),
                 current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized")
    
    return db.query(models.Product).filter(
        models.Product.created_by == current_user.id
    ).offset(start).limit(end).all()



@router.get("/{product_id}", response_model=schemas.ProductOut)
def get_product_by_id(product_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized")

    product = db.query(models.Product).filter(
        models.Product.id == product_id,
        models.Product.created_by == current_user.id
    ).first()

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    return product


@router.put("/{product_id}", response_model=schemas.ProductOut)
def update_product(
    product_id: int,
    product_data: schemas.CreateProduct,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized")
    
    product = db.query(models.Product).filter(
        models.Product.id == product_id,
        models.Product.created_by == current_user.id
    ).first()

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found or unauthorized")

    for key, value in product_data.model_dump().items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)
    return product



@router.delete("/{product_id}")
def delete_product(product_id: int,
                   db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    product = db.query(models.Product).filter(
        models.Product.id == product_id,
        models.Product.created_by == current_user.id
    ).first()

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found or unauthorized")

    db.delete(product)
    db.commit()
    return {"message": "Product deleted successfully"}

# app/products/routes.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.products import models, schemas

router = APIRouter()

