from enum import Enum
from typing import TYPE_CHECKING, Any, List

import sqlalchemy as sa
from database.base_class import BaseManager, BaseModel

from .serializers import Streaming, StreamingCreate, StreamingStatus

# from sqlalchemy import Column


# model = sa.Table(
#     "streaming",
#     sa.MetaData(),
#     sa.Column("id", sa.Integer, primary_key=True),
#     sa.Column("name", sa.Text, nullable=False, index=True),
#     sa.Column("status", sa.String(10), nullable=False, index=True),
# ) 

class Streaming(BaseModel):
    id = sa.Column(sa.Integer, primary_key=True)
    name  = sa.Column(sa.Text, nullable=False, index=True)
    status = sa.Column(sa.String(10), nullable=False, index=True)

class StreamingManager(BaseManager):

    table = Streaming.__table__

    async def list(self,limit: int= 20,page : int= 0) -> Any:
        offset = limit * (page - 1)
        query = self.table.select().offset(offset).limit(limit)
        instances = await self.db.fetch_all(query)
        total = await self.db.fetch_val(self.table.count())
        return instances,total

    async def get(self,id : int) -> Any:
        query = self.table.select().where(self.table.c.id == id)
        instance = await self.db.fetch_one(query)
        return instance

    async def create(self, object: StreamingCreate) -> Any:
        instance = object.dict()
        query = self.table.insert().values(**instance)
        instance['id'] = await self.db.execute(query)
        return instance

    async def update(self,instance : Streaming,update_object: StreamingCreate) -> Any:

        update_instance = update_object.dict(exclude_unset=True)

        for k,v in update_instance.items():
            setattr(instance,k,v)

        query = self.table.update().where(self.table.c.id == instance.id).values(**instance.dict())
        await self.db.execute(query)
        
        return instance



