from passlib.context import CryptContext
from itsdangerous import URLSafeTimedSerializer
from app.core.config import settings
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.auth.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

serializer = URLSafeTimedSerializer(settings.SECRET_KEY)

def generate_reset_token(email: str) -> str:
    return serializer.dumps(email, salt="reset-password")

def verify_reset_token(token: str, max_age: int = 3600) -> str | None:
    try:
        return serializer.loads(token, salt="reset-password", max_age=max_age)
    except Exception:
        return None
    
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/signin")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_email: str = payload.get("sub")
        if user_email is None:
         raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(user_email == User.email).first()
    if user is None:
        raise credentials_exception
    return user
