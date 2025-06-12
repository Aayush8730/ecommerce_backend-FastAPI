from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.cart.utils import require_user_role
from app.orders import models, schemas
from app.cart.models import Cart
from app.products.models import Product



router = APIRouter()

@router.post("/checkout", response_model=schemas.OrderCreateResponse)
def checkout(
    db: Session = Depends(get_db),
    current_user=Depends(require_user_role)
):
    cart_items = db.query(Cart).filter(Cart.user_id == current_user.id).all()
    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    total = sum(item.product.price * item.quantity for item in cart_items)

    order = models.Order(user_id=current_user.id,total_amount=total,status=models.OrderStatus.paid)

    db.add(order)
    db.commit()
    db.refresh(order)

    for item in cart_items:
        order_item = models.OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price_at_purchase=item.product.price
        )
        db.add(order_item)


        product = db.query(Product).filter(Product.id == item.product_id).first()
        if product:
            product.stock -= item.quantity


    db.query(Cart).filter(Cart.user_id == current_user.id).delete() #empties the cart agian 
    db.commit()

    return {
        "order_id": order.id,
        "total_amount": order.total_amount,
        "status": order.status
    }

