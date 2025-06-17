from pydantic import BaseModel, EmailStr, field_validator
from enum import Enum

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

ALLOWED_DOMAINS = {"gmail.com", "yahoo.com", "nucleusteq.org"}

def validate_email_domain(email: str) -> str:
    domain = email.split("@")[-1].lower()
    if domain not in ALLOWED_DOMAINS:
        raise ValueError("Email domain must be one of: gmail.com, yahoo.com, nucleusteq.org")
    return email

class SignupRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: UserRole = UserRole.user

    @field_validator("email")
    @classmethod
    def check_email_domain(cls, v: str) -> str:
        return validate_email_domain(v)

    @field_validator("password")
    @classmethod
    def check_password(cls, v: str) -> str:
        if not validate_password(v):
            raise ValueError("Password must be at least 8 characters long and include an uppercase letter, a digit, and a special character (!@#$%^&*).")
        return v

class SigninRequest(BaseModel):
    email: EmailStr
    password: str

    @field_validator("email")
    @classmethod
    def check_email_domain(cls, v: str) -> str:
        return validate_email_domain(v)

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

    @field_validator("email")
    @classmethod
    def check_email_domain(cls, v: str) -> str:
        return validate_email_domain(v)

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str

    @field_validator("new_password")
    @classmethod
    def check_password(cls, v: str) -> str:
        if not validate_password(v):
            raise ValueError("Password must be at least 8 characters long and include an uppercase letter, a digit, and a special character (!@#$%^&*).")
        return v


class RefreshTokenRequest(BaseModel):
    refresh_token: str
