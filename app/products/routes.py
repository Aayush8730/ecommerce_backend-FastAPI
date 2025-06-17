from typing import List
from fastapi import APIRouter, Body, Depends, Path, Query, status
from sqlalchemy.orm import Session
from app.auth.models import User
from app.auth.utils import get_current_user
from app.core.database import get_db
from app.products import schemas, models
from app.utils.handlers import ProductNotFound, UnauthorizedAction

router = APIRouter()

@router.post("", response_model=schemas.ProductOut)
def create_product(product_data: schemas.CreateProduct,
                   db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise UnauthorizedAction()

    product = models.Product(**product_data.model_dump(), created_by=current_user.id)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@router.get("", response_model=List[schemas.ProductOut])
def get_products(start: int = Query(default=None, ge=0),
                 end: int = Query(default=None, ge=0),
                 db: Session = Depends(get_db),
                 current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise UnauthorizedAction()
    
    return db.query(models.Product).filter(
        models.Product.created_by == current_user.id
    ).offset(start).limit(end).all()


@router.get("/{product_id}", response_model=schemas.ProductOut)
def get_product_by_id(product_id: int = Path(..., gt=0),
                      db: Session = Depends(get_db),
                      current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise UnauthorizedAction()

    product = db.query(models.Product).filter(
        models.Product.id == product_id,
        models.Product.created_by == current_user.id
    ).first()

    if not product:
        raise ProductNotFound(product_id)

    return product


@router.put("/{product_id}", response_model=schemas.ProductOut)
def update_product(product_data: schemas.CreateProduct,
                   product_id: int = Path(..., ge=1),
                   db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise UnauthorizedAction()

    product = db.query(models.Product).filter(
        models.Product.id == product_id,
        models.Product.created_by == current_user.id
    ).first()

    if not product:
        raise ProductNotFound(product_id)

    for key, value in product_data.model_dump().items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)
    return product


@router.delete("/{product_id}")
def delete_product(product_id: int = Path(..., gt=0),
                   db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise UnauthorizedAction()

    product = db.query(models.Product).filter(
        models.Product.id == product_id,
        models.Product.created_by == current_user.id
    ).first()

    if not product:
        raise ProductNotFound(product_id)

    db.delete(product)
    db.commit()
    return {"message": "Product deleted successfully"}
