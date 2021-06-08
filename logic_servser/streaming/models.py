from enum import Enum
from typing import TYPE_CHECKING, Any, List

import sqlalchemy as sa
from database.base_class import BaseManager

from .serializers import StreamingCreate, StreamingStatus

# from sqlalchemy import Column, Integer, MetaData, String, Table, Text

model = sa.Table(
    "streaming",
    sa.MetaData(),
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("name", sa.Text, nullable=False, index=True),
    sa.Column("status", sa.String(10), nullable=False, index=True),
)

class StreamingManager(BaseManager):

    async def list(self,limit: int= 20,page : int= 0) -> Any:
        query = model.select().offset(limit * page).limit(limit)
        instances = await self.db.fetch_all(query)
        total = await self.db.fetch_val(model.count())
        return instances,total

    async def get(self,id : int) -> Any:
        query = model.select().where(model.c.id == id).where(model.c.status != StreamingStatus.end)
        instance = await self.db.fetch_one(query)
        return instance

    async def create(self, object: StreamingCreate) -> Any:
        instance = object.dict()
        query = model.insert().values(**instance)
        instance['id'] = await self.db.execute(query)
        return instance



