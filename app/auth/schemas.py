from pydantic import EmailStr , BaseModel
from enum import Enum

class UserRole(str, Enum):
    admin = "admin"
    user = "user"

class SignupRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: UserRole = UserRole.user

class SigninRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
