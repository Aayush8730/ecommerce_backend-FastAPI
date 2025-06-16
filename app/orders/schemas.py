from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from enum import Enum

class OrderStatus(str, Enum):
    pending = "pending"
    paid = "paid"
    cancelled = "cancelled"

class OrderItemBase(BaseModel):
    product_id: int = Field(..., gt=0, description="Product ID must be a positive integer")
    quantity: int = Field(..., gt=0, le=1000, description="Quantity must be between 1 and 1000")
    price_at_purchase: float = Field(..., gt=0, description="Price must be greater than 0")

class OrderItemResponse(OrderItemBase):
    product_name: str
    subtotal: float = Field(..., ge=0, description="Subtotal must be non-negative")

    class Config:
        form_attributes = True

class OrderCreateResponse(BaseModel):
    order_id: int
    total_amount: float = Field(..., ge=0, description="Total amount must be non-negative")
    status: OrderStatus

    class Config:
        form_attributes = True

class OrderListResponse(BaseModel):
    order_id: int
    created_at: datetime
    total_amount: float = Field(..., ge=0, description="Total amount must be non-negative")
    status: OrderStatus

    class Config:
        form_attributes = True

class OrderDetailResponse(BaseModel):
    order_id: int
    created_at: datetime
    total_amount: float = Field(..., ge=0, description="Total amount must be non-negative")
    status: OrderStatus
    items: List[OrderItemResponse]

    class Config:
        form_attributes = True
