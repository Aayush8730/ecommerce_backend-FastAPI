from pydantic import BaseModel, Field, field_validator

class AddToCart(BaseModel):
    product_id: int = Field(..., gt=0, description="Product must be greater than zero")
    quantity: int = Field(1, gt=0, le=100, description="Quantity must be greater than zero")

class CartItemOut(BaseModel):
    id: int
    product_id: int
    quantity: int

    class Config:
        orm_mode = True

class UpdateQuantityChangeRequest(BaseModel):
    change: int = Field(..., description="Change in quantity, can be positive or negative")

    @field_validator("change")
    @classmethod
    def validate_change(cls, v: int) -> int:
        if v == 0:
            raise ValueError("Quantity change cannot be zero")
        return v
