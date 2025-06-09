from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from app.auth.jwt_handler import create_access_token, create_refresh_token
from app.auth.utils import hash_password, verify_password
from app.auth.models import User
from app.core.database import get_db
from enum import Enum
from app.auth.schemas import SignupRequest, SigninRequest, TokenResponse

router = APIRouter()

@router.post("/signup") #decorator
def signup(request: SignupRequest, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == request.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered."
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

   
    return {"message": "User created successfully. Please sign in."}

@router.post("/signin", response_model=TokenResponse)
def signin(request: SigninRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials."
        )

    access_token = create_access_token({"sub": user.email, "role": user.role})
    refresh_token = create_refresh_token({"sub": user.email})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }
