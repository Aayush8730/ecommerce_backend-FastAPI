from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.products import models, schemas
from app.core.database import get_db
from app.products.schemas import ProductSearchResponse
from app.core.logging import logger

router = APIRouter()

@router.get("/", response_model=List[schemas.ProductOut])
def list_products(
    category: Optional[str] = None,
    min_price: Optional[float] = Query(default=None, ge=0),
    max_price: Optional[float] = Query(default=None, ge=0),
    sort_by: Optional[str] = Query(default="id"),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    logger.info(f"User searched for products with: category={category}, min_price={min_price}, max_price={max_price}, sort_by={sort_by}, page={page}, page_size={page_size}")
    
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

        logger.info(f"Products fetched successfully with filters.")
        return products

    except Exception as e:
        logger.error(f"Error fetching products: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong while fetching products."
        )


@router.get("/search", response_model=ProductSearchResponse)
def search_products(
    keyword: str = Query(..., min_length=1, max_length=100),
    db: Session = Depends(get_db),
):
    logger.info(f"Search requested with keyword: {keyword}")
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

    except Exception as e:
        logger.error(f"Search error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Not able to search right now!!"
        )
    

@router.get("/{id}", response_model=schemas.ProductOut)
def get_product_detail(id: int = Path(..., ge=1), db: Session = Depends(get_db)):

    product = db.query(models.Product).filter(models.Product.id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
