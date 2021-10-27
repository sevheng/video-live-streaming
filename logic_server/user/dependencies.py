
from fastapi import Depends, status
from jose import JWTError, jwt
from main.dependencies import get_manager
from main.exception_handlers import HTTPException
from main.security import decode_access_token, oauth2_scheme

from .models import User


async def get_current_user(token: str = Depends(oauth2_scheme)):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token)
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        # token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await User.objects.get_or_none(id=user_id)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.is_active == False:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
