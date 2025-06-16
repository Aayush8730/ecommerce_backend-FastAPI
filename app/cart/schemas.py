from pydantic import BaseModel, Field, field_validator

class AddToCart(BaseModel):
    product_id: int = Field(..., gt=0, description="Product must be greater than zero")
    quantity: int = Field(1, gt=0, le=100, description="Quantity must be greater than zero")

class CartItemOut(BaseModel):
    id: int
    product_id: int
    quantity: int

    class Config:
        form_attributes = True


class UpdateQuantityRequest(BaseModel):
    quantity: int = Field(..., ge=1, description="New quantity must be at least 1")

