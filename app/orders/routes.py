from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.auth.models import User
from app.core.database import get_db
from app.auth.utils import get_current_user
from app.orders import models, schemas
from app.cart.models import Cart
from app.products.models import Product
from app.cart.utils import require_user_role
from app.core.logging import logger


router = APIRouter()


@router.get("/", response_model=List[schemas.OrderListResponse])
def get_user_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_user_role)
):
    logger.info(f"User with email {current_user.email} requesting all the orders")
    orders = db.query(models.Order).filter(models.Order.user_id == current_user.id).all()
    return [
        {
            "order_id": o.id,
            "created_at": o.created_at,
            "total_amount": o.total_amount,
            "status": o.status
        } for o in orders
    ]


@router.get("/{order_id}", response_model=schemas.OrderDetailResponse)
def get_order_detail(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_user_role)
):
    logger.info(f"{current_user.email} checking for the details of the order with order id {order_id}")
    order = db.query(models.Order).filter(
        models.Order.id == order_id,
        models.Order.user_id == current_user.id
    ).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    item_data = []
    for item in order.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        item_data.append({
            "product_id": item.product_id,
            "quantity": item.quantity,
            "price_at_purchase": item.price_at_purchase,
            "product_name": product.name if product else "Unknown",
            "subtotal": float(item.price_at_purchase) * item.quantity
        })
    
    return {
        "order_id": order.id,
        "created_at": order.created_at,
        "total_amount": order.total_amount,
        "status": order.status,
        "items": item_data
    }
