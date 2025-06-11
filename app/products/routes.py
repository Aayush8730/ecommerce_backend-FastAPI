
from fastapi import APIRouter, Depends, HTTPException, status
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
