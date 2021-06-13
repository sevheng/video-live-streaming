
from typing import TYPE_CHECKING, Any, List, Optional

from database.base_class import BaseManager, BaseModel
from databases import Database
from main.security import get_password_hash, verify_password
from sqlalchemy import Boolean, Column, Integer, String

from user import serializers


class User(BaseModel):
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)

class UserManager(BaseManager):
    
    table = User.__table__

    async def create(self, object: serializers.UserInDB) -> Any:
        instance = object.dict()
        hashed_password =  get_password_hash(instance.pop('password'))
        query = self.table.insert().values(hashed_password=hashed_password,**instance)
        instance['id'] = await self.db.execute(query)
        return instance

    async def get_by_email(self, email: str) -> Optional[User]:
        query = self.table.select().where(User.email == email)
        instance = await self.db.fetch_one(query)
        return User(**instance)

    async def authenticate(self, email: str, password: str) -> Optional[User]:
        user =  await self.get_by_email(email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
