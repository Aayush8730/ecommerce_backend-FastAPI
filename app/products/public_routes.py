from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.products import models, schemas
from app.core.database import get_db
from app.products.schemas import ProductSearchResponse

router = APIRouter()

@router.get("/", response_model=List[schemas.ProductOut])
def list_products(
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    sort_by: Optional[str] = "id",
    page: int = 1,
    page_size: int = 10,
    db: Session = Depends(get_db)
):
    valid_sort_fields = ["price", "name", "id"]
    if sort_by not in valid_sort_fields:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid sort_by field. Must be one of: {', '.join(valid_sort_fields)}"
        )

    try:
        query = db.query(models.Product)

        if category:
            query = query.filter(models.Product.category == category)
        if min_price is not None:
            query = query.filter(models.Product.price >= min_price)
        if max_price is not None:
            query = query.filter(models.Product.price <= max_price)

        query = query.order_by(getattr(models.Product, sort_by))

        offset = (page - 1) * page_size
        products = query.offset(offset).limit(page_size).all()

        return products

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong while fetching products."
        )



@router.get("/search", response_model=ProductSearchResponse)
def search_products(
    keyword: str,
    db: Session = Depends(get_db)
):
    keyword = keyword.strip()

    try:
        keyword_pattern = f"%{keyword}%"
        products = db.query(models.Product).filter(
        models.Product.name.ilike(keyword_pattern) |
        models.Product.description.ilike(keyword_pattern) |
        models.Product.category.ilike(keyword_pattern)
        ).all()


        if not products:
            return {
                "products": [],
                "message": "No matching products found. Try describing the product in more detail."
            }

        return {
            "products": products,
            "message": None 
        }

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Not able to search right now!!"
        )
    
@router.get("/products/{id}", response_model=schemas.ProductOut)
def get_product_detail(id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
