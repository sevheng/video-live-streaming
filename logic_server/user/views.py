from typing import Any

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from main import security
from main.dependencies import get_manager
from main.exception_handlers import HTTPException
from main.serializers import Response

from user import serializers

from .models import User

router = APIRouter()


@router.post("/")
async def create_user(
    user_in: serializers.UserCreate
) -> Any:
    """
    Create new user.
    """
    user = await User.objects.get_or_none(email=user_in.email)

    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    instance = await User.objects.create(**user_in.dict())
    # if settings.EMAILS_ENABLED and user_in.email:
    #     send_new_account_email(
    #         email_to=user_in.email, username=user_in.email, password=user_in.password
    #     )
    return Response(serializers.User,data=instance)()

@router.post("/login")
async def login_user(
    credential: OAuth2PasswordRequestForm = Depends()
) -> Any:

    user = await User.objects.get_or_none(email=credential.username,password=credential.password)

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    data = {
        "access_token": security.create_access_token(user.id),
        "user": serializers.User.from_orm(user)
    }

    return Response(serializers.Token,data=data)()


