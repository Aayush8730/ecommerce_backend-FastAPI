from typing import List
from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.auth.models import User
from app.auth.utils import get_current_user
from app.core.database import get_db
from app.products import schemas, models
from app.core.logging import logger

router = APIRouter()

@router.post("/", response_model=schemas.ProductOut)
def create_product(product_data: schemas.CreateProduct,
                   db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        logger.warning(f"Unauthorized create attempt by user {current_user.email}")
        raise HTTPException(status_code=403, detail="Not authorized")

    product = models.Product(**product_data.model_dump(), created_by=current_user.id)
    db.add(product)
    db.commit()
    db.refresh(product)

    logger.info(f"Product '{product.name}' created by admin {current_user.email} (ID: {product.id})")
    return product

@router.get("/", response_model=List[schemas.ProductOut])
def get_products(start: int = 0, end: int = 10,
                 db: Session = Depends(get_db),
                 current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        logger.warning(f"Unauthorized product list attempt by {current_user.email}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized")
    
    products = db.query(models.Product).filter(
        models.Product.created_by == current_user.id
    ).offset(start).limit(end).all()

    logger.info(f"Admin {current_user.email} fetched products from {start} to {end}")
    return products

@router.get("/{product_id}", response_model=schemas.ProductOut)
def get_product_by_id(product_id: int,
                      db: Session = Depends(get_db),
                      current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        logger.warning(f"Unauthorized product detail attempt by {current_user.email}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized")

    product = db.query(models.Product).filter(
        models.Product.id == product_id,
        models.Product.created_by == current_user.id
    ).first()

    if not product:
        logger.warning(f"Product ID {product_id} not found or unauthorized for user {current_user.email}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    logger.info(f"Admin {current_user.email} viewed product ID {product_id}")
    return product

@router.put("/{product_id}", response_model=schemas.ProductOut)
def update_product(product_id: int,
                   product_data: schemas.CreateProduct,
                   db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        logger.warning(f"Unauthorized update attempt by {current_user.email}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized")
    
    product = db.query(models.Product).filter(
        models.Product.id == product_id,
        models.Product.created_by == current_user.id
    ).first()

    if not product:
        logger.warning(f"Update failed. Product ID {product_id} not found for user {current_user.email}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found or unauthorized")

    for key, value in product_data.model_dump().items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)

    logger.info(f"Product ID {product_id} updated by admin {current_user.email}")
    return product

@router.delete("/{product_id}")
def delete_product(product_id: int,
                   db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        logger.warning(f"Unauthorized delete attempt by {current_user.email}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    product = db.query(models.Product).filter(
        models.Product.id == product_id,
        models.Product.created_by == current_user.id
    ).first()

    if not product:
        logger.warning(f"Delete failed. Product ID {product_id} not found for user {current_user.email}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found or unauthorized")

    db.delete(product)
    db.commit()
    logger.info(f"Product ID {product_id} deleted by admin {current_user.email}")
    return {"message": "Product deleted successfully"}
