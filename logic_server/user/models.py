
from typing import TYPE_CHECKING, Any, List, Optional

import ormar
from database.base_class import BaseManager, BaseMeta
from databases import Database
from main.config import SECRET_KEY
from main.security import get_password_hash, verify_password
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from user import serializers


class User(ormar.Model):

    class Meta(BaseMeta):
        tablename = 'user'

    id: int = ormar.Integer(primary_key=True)
    full_name: str = ormar.String(max_length=255)
    email: str = ormar.String(max_length=255,unique=True)
    password: str = ormar.String(max_length=128,encrypt_secret=str(SECRET_KEY), encrypt_backend=ormar.EncryptBackends.HASH)
    is_active : bool = ormar.Boolean(default=True)
    is_superuser: bool = ormar.Boolean(default=False)

    # id = Column(Integer, primary_key=True, index=True)
    # full_name = Column(String, index=True)
    # email = Column(String, unique=True, index=True, nullable=False)
    # hashed_password = Column(String, nullable=False)
    # is_active = Column(Boolean(), default=True)
    # is_superuser = Column(Boolean(), default=False)


# class UserManager(BaseManager):
    
#     table = User.__table__

#     async def create(self, object: serializers.UserInDB) -> Any:
#         instance = object.dict()
#         hashed_password =  get_password_hash(instance.pop('password'))
#         query = self.table.insert().values(hashed_password=hashed_password,**instance)
#         instance['id'] = await self.db.execute(query)
#         return instance

#     async def get_by_email(self, email: str) -> Optional[User]:
#         query = self.table.select().where(User.email == email)
#         instance = await self.db.fetch_one(query)
#         return User(**instance) if instance else None

#     async def get_by_id(self, id: str) -> Optional[User]:
#         query = self.table.select().where(User.id == int(id))
#         instance = await self.db.fetch_one(query)
#         return User(**instance) if instance else None

#     async def authenticate(self, email: str, password: str) -> Optional[User]:
#         user =  await self.get_by_email(email=email)
#         if not user:
#             return None
#         if not verify_password(password, user.hashed_password):
#             return None
#         return user
