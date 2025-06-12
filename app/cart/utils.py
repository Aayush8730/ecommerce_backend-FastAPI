from fastapi import Depends, HTTPException, status
from app.auth.models import User
from app.auth.utils import get_current_user  

def require_user_role(current_user: User = Depends(get_current_user)):
    if current_user.role != "user":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only users can perform this action."
        )
    return current_user


