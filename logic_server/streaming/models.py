from enum import Enum
from typing import TYPE_CHECKING, Any, List

import ormar
import sqlalchemy as sa
from database.base_class import BaseManager, BaseMeta
from sqlalchemy.orm import relationship
from user.models import User

from .serializers import Streaming, StreamingCreate, StreamingStatus

# from sqlalchemy import Column


# model = sa.Table(
#     "streaming",
#     sa.MetaData(),
#     sa.Column("id", sa.Integer, primary_key=True),
#     sa.Column("name", sa.Text, nullable=False, index=True),
#     sa.Column("status", sa.String(10), nullable=False, index=True),
# ) 

class Streaming(ormar.Model):

    class Meta(BaseMeta):
        tablename = 'streaming'

    id: int = ormar.Integer(primary_key=True)
    status: str = ormar.String(max_length=10)
    name: str = ormar.String(max_length=255)
    user: User = ormar.ForeignKey(User,name='user_id')
    
    # id = sa.Column(sa.Integer, primary_key=True)
    # status = sa.Column(sa.String(10), nullable=False, index=True)
    # name  = sa.Column(sa.Text, nullable=False, index=True)
    # user_id = sa.Column(sa.Integer,sa.ForeignKey('user.id'),nullable=False,index=True)

    # user = relationship('User')

# class StreamingManager(BaseManager):

#     table = Streaming.__table__

#     async def list(self,limit: int= 20,page : int= 0) -> Any:
#         offset = limit * (page - 1)
#         # query = self.table.select().offset(offset).limit(limit)
#         # instances = await self.db.fetch_all(query)
#         # total = await self.db.fetch_val(self.table.count())
#         instances = await Streaming
#         total=0
#         return instances,total

#     async def get(self,id : int) -> Any:
#         query = self.table.select().where(self.table.c.id == id)
#         instance = await self.db.fetch_one(query)
#         return instance

#     async def create(self, object: dict) -> Any:
#         query = self.table.insert().values(**object)
#         object['id'] = await self.db.execute(query)
#         return object

#     async def update(self,instance : Streaming,update_object: StreamingCreate) -> Any:

#         update_instance = update_object.dict(exclude_unset=True)

#         for k,v in update_instance.items():
#             setattr(instance,k,v)

#         query = self.table.update().where(self.table.c.id == instance.id).values(**instance.dict())
#         await self.db.execute(query)
        
#         return instance



