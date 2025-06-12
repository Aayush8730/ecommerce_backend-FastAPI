from pydantic import BaseModel
from typing import List
from datetime import datetime
from enum import Enum


class OrderStatus(str, Enum):
    pending = "pending"
    paid = "paid"
    cancelled = "cancelled"


class OrderItemBase(BaseModel):
    product_id: int
    quantity: int
    price_at_purchase: float


class OrderItemResponse(OrderItemBase):
    product_name: str
    subtotal: float

    class Config:
        orm_mode = True


class OrderCreateResponse(BaseModel):
    order_id: int
    total_amount: float
    status: OrderStatus

    class Config:
        orm_mode = True


class OrderListResponse(BaseModel):
    order_id: int
    created_at: datetime
    total_amount: float
    status: OrderStatus

    class Config:
        orm_mode = True


class OrderDetailResponse(BaseModel):
    order_id: int
    created_at: datetime
    total_amount: float
    status: OrderStatus
    items: List[OrderItemResponse]

    class Config:
        orm_mode = True
