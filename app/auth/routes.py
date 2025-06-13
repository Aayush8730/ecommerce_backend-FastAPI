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
    if not user or not verify_password(request.password, user.hashed_password):
        logger.warning(f"Wrong attempt to signin by {request.email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials."
        )

    access_token = create_access_token({"sub": user.email, "role": user.role})
    refresh_token = create_refresh_token({"sub": user.email})
    logger.info(f"user with email - {request.email} successfully signed in")
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
def reset_password(request: ResetPasswordRequest = Depends(ResetPasswordRequest.as_form), db: Session = Depends(get_db)):
    email = verify_reset_token(request.token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.hashed_password = hash_password(request.new_password)
    db.commit()
    logger.info(f"password updated succesfully {user.email}")
    return HTMLResponse(content="<h3>Password updated successfully</h3>")

@router.get("/reset-password-form")
def reset_password_form(token: str):
    html_content = f"""
    <html>
        <body>
            <h2>Reset Your Password</h2>
            <form method="post" action="/auth/reset-password">
                <input type="hidden" name="token" value="{token}">
                <label>New Password:</label><br>
                <input type="password" name="new_password" required><br><br>
                <button type="submit">Reset Password</button>
            </form>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)