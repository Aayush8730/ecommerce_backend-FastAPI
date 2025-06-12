from sqlalchemy import Integer , Column , String , Enum
import enum
from sqlalchemy.orm import relationship
from app.core.database import Base

class UserRole(str,enum.Enum):
  admin = "admin"
  user = "user"

class User(Base):
  __tablename__ = "users"
  __table_args__ = {'extend_existing': True}

  id = Column(Integer,primary_key=True,index=True)
  name = Column(String,nullable=False)
  email = Column(String,unique=True,nullable=False,index=True)
  hashed_password = Column(String,nullable=False)
  role = Column(Enum(UserRole),nullable=False,default=UserRole.user)

  
  products = relationship("Product", back_populates="creator")
  cart_items = relationship("Cart", back_populates="user")
  orders = relationship("Order", back_populates="user", cascade="all, delete")
