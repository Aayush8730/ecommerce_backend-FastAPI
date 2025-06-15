from typing import List, Optional
from pydantic import BaseModel, Field, HttpUrl

class CreateProduct(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    description: str = Field(..., min_length=10, max_length=1000)
    price: float = Field(..., gt=0, description="Price must be greater than 0")
    stock: int = Field(..., ge=0, le=10000, description="Stock must be between 0 and 10000")
    category: str = Field(..., min_length=2, max_length=50)
    image_url: str

class ProductOut(CreateProduct):
    id: int

    class Config:
        orm_mode = True

class ProductSearchResponse(BaseModel):
    products: List[ProductOut]
    message: Optional[str] = None
