from pydantic import BaseModel

class CreateProduct(BaseModel):
  name: str
  description: str
  price: float
  stock: int
  category: str
  image_url: str

class ProductOut(CreateProduct): #inherits the CreateProduct Basemodel
    id: int

    class Config:
        orm_mode = True