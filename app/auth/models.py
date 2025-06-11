from sqlalchemy import Integer , Column , String , Enum
import enum
from sqlalchemy.orm import relationship
from app.core.database import Base

class UserRole(str,enum.Enum):
  admin = "admin"
  user = "user"

class User(Base):
  __tablename__ = "users"

  id = Column(Integer,primary_key=True,index=True)
  name = Column(String,nullable=False)
  email = Column(String,unique=True,nullable=False,index=True)
  hashed_password = Column(String,nullable=False)
  role = Column(Enum(UserRole),nullable=False,default=UserRole.user)

  
  products = relationship("Product", back_populates="creator")