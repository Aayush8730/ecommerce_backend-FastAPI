from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.cart import models, schemas
from app.core.database import get_db
from app.auth.utils import get_current_user
from app.products.models import Product
from app.auth.models import User
from .utils import require_user_role

router = APIRouter()

@router.post("", response_model=schemas.CartItemOut)
def add_to_cart(
    item: schemas.AddToCart,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_user_role)
):
    product = db.query(Product).filter(Product.id == item.product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product not found")

    if item.quantity < 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Quantity must be at least 1")

    cart_item = db.query(models.Cart).filter_by(
        user_id=current_user.id,
        product_id=item.product_id
    ).first()

    if cart_item: #already exists 
        if cart_item.quantity + item.quantity > product.stock:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Only {product.stock - cart_item.quantity} more item's left in stock"
            )
        cart_item.quantity += item.quantity
        db.commit()
        db.refresh(cart_item)
        return cart_item
    else:
        if item.quantity > product.stock:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Only {product.stock} item's in stock"
            )

        new_cart_item = models.Cart(
            user_id=current_user.id,
            product_id=item.product_id,
            quantity=item.quantity
        )
        db.add(new_cart_item)
        db.commit()
        db.refresh(new_cart_item)
        return new_cart_item
  

@router.get("", response_model=List[schemas.CartItemOut])
def view_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_user_role),
):
    cart_items = db.query(models.Cart).filter(models.Cart.user_id == current_user.id).all()
    return cart_items

@router.patch("/{product_id}")
def modify_cart_quantity(product_id: int,
                         data: schemas.UpdateQuantityChangeRequest,
                         db: Session = Depends(get_db),
                         current_user: User = Depends(require_user_role)):


    cart_item = db.query(models.Cart).filter(
        models.Cart.user_id == current_user.id,
        models.Cart.product_id == product_id
    ).first()

    if not cart_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found in cart")

    new_quantity = cart_item.quantity + data.change

    if new_quantity < 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Quantity cannot be less than 1 or either remove the product from the cart")

    product = db.query(Product).filter(Product.id == product_id).first()
    if not product or new_quantity > product.stock:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=" sorry we are out of stock")

    cart_item.quantity = new_quantity
    db.commit()
    db.refresh(cart_item)

    return {
        "message": "Cart item quantity updated",
        "product_id": product_id,
        "new_quantity": cart_item.quantity
    }

@router.delete("/{product_id}")
def remove_from_cart(product_id: int,
                     db: Session = Depends(get_db),
                     current_user: User = Depends(get_current_user)):
    if current_user.role != "user":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    cart_item = db.query(models.Cart).filter(
        models.Cart.user_id == current_user.id,
        models.Cart.product_id == product_id
    ).first()

    if not cart_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found in cart")

    db.delete(cart_item)
    db.commit()
    return {"message": "Item removed from cart"}