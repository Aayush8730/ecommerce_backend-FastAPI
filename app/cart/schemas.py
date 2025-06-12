from pydantic import BaseModel

class AddToCart(BaseModel):
    product_id: int
    quantity: int = 1

class CartItemOut(BaseModel):
    id: int
    product_id: int
    quantity: int

    class Config:
        orm_mode = True

class UpdateQuantityChangeRequest(BaseModel):
    change: int

