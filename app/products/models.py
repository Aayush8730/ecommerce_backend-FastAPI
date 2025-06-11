from sqlalchemy import Column, Integer, String, Text, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    price = Column(Numeric(10, 2), nullable=False)
    stock = Column(Integer, nullable=False)
    category = Column(String(100))
    image_url = Column(Text)

    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)

    creator = relationship("User", back_populates="products")
