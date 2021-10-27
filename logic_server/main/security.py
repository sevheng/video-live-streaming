from datetime import datetime, timedelta
from typing import Any, Union

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext

from main import config

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/user/login")

ALGORITHM = "HS256"


def create_access_token(
    subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, str(config.SECRET_KEY), algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token:str):
    return jwt.decode(token, str(config.SECRET_KEY), algorithms=[ALGORITHM])

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
