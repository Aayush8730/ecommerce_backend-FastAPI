from fastapi import APIRouter, Form, HTTPException, Depends, status
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from app.auth.jwt_handler import create_access_token, create_refresh_token
from app.auth.services import send_reset_email
from app.auth.utils import generate_reset_token, hash_password, verify_password, verify_reset_token
from app.auth.models import User
from app.core.database import get_db
from enum import Enum
from app.auth.schemas import ForgotPasswordRequest, ResetPasswordRequest, SignupRequest, SigninRequest, TokenResponse
from app.core.logging import logger
from app.auth.utils import verify_jwt_token


router = APIRouter()

@router.post("/signup") #decorator
def signup(request: SignupRequest, db: Session = Depends(get_db)):
    logger.info(f"Attempt to signup using email {request.email}")
    existing_user = db.query(User).filter(User.email == request.email).first()
    if existing_user:
        logger.warning(f"Registration failed - email already exists {request.email}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Email already registered."
        )

    hashed_password = hash_password(request.password)  
    new_user = User(
        name=request.name,
        email=request.email,
        hashed_password=hashed_password,
        role=request.role.value 
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    logger.info(f"user created successfully with the email - {request.email} and role: {new_user.role}")
    return {"message": "User created successfully. Please sign in."}

@router.post("/signin", response_model=TokenResponse)
def signin(request: SigninRequest, db: Session = Depends(get_db)):
    logger.info(f"Attempt to signin using the email - {request.email}")

    user = db.query(User).filter(User.email == request.email).first()
    
    if not user:
        logger.warning(f"Signin failed: Email not found - {request.email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email not found. Please enter correct email or correct email format"
        )

    if not verify_password(request.password, user.hashed_password):
        logger.warning(f"Signin failed: Incorrect password for - {request.email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password."
        )

    access_token = create_access_token({"sub": user.email, "role": user.role})
    refresh_token = create_refresh_token({"sub": user.email})

    logger.info(f"User with email - {request.email} successfully signed in")

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/forgot-password")
def forgot_password(request: ForgotPasswordRequest, db: Session = Depends(get_db)):
    logger.info(f"attempt to reset the password using the free email service")
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    token = generate_reset_token(user.email)
    send_reset_email(user.email, token)
    return {"message": "Password reset email sent"}

@router.post("/reset-password")
def reset_password(request: ResetPasswordRequest , db: Session = Depends(get_db)):
    email = verify_reset_token(request.token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.hashed_password = hash_password(request.new_password)
    db.commit()
    logger.info(f"password updated succesfully {user.email}")
    return f"Password updated successfully of user {user.email}"

from app.auth.schemas import RefreshTokenRequest
from fastapi import Request


@router.post("/refresh-token", response_model=TokenResponse)
def refresh_token(
    request_data: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    payload = verify_jwt_token(request_data.refresh_token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

    email = payload.get("sub")
    if not email:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_access_token = create_access_token({"sub": user.email, "role": user.role})
    new_refresh_token = create_refresh_token({"sub": user.email})

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }
