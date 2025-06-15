from pydantic import BaseModel, EmailStr, field_validator
from enum import Enum
from fastapi import Form

class UserRole(str, Enum):
    admin = "admin"
    user = "user"

def validate_password(password: str) -> bool:
    if len(password) < 8:
        return False

    has_upper = False
    has_digit = False
    has_special = False
    special_chars = "!@#$%^&*"

    for char in password:
        if char.isupper():
            has_upper = True
        elif char.isdigit():
            has_digit = True
        elif char in special_chars:
            has_special = True

    return has_upper and has_digit and has_special

class SignupRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: UserRole = UserRole.user

    @field_validator("password")
    @classmethod
    def check_password(cls, v: str) -> str:
        if not validate_password(v):
            raise ValueError("Password must be at least 8 characters long and include an uppercase letter, a digit, and a special character (!@#$%^&*).")
        return v

class SigninRequest(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def check_password(cls, v: str) -> str:
        if not validate_password(v):
            raise ValueError("Password must be at least 8 characters long and include an uppercase letter, a digit, and a special character (!@#$%^&*).")
        return v

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str

    @classmethod
    def as_form(
        cls,
        token: str = Form(...),
        new_password: str = Form(...)
    ):
        return cls(token=token, new_password=new_password)

    @field_validator("new_password")
    @classmethod
    def check_password(cls, v: str) -> str:
        if not validate_password(v):
            raise ValueError("Password must be at least 8 characters long and include an uppercase letter, a digit, and a special character (!@#$%^&*).")
        return v
