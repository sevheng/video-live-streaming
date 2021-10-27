from typing import Any

import ormar
from databases import Database
from main.config import DATABASE, SQL_METADATA
from sqlalchemy.ext.declarative import as_declarative, declared_attr

# @as_declarative()
# class BaseModel:
#     id: Any
#     __name__: str
#     # Generate __tablename__ automatically
#     @declared_attr
#     def __tablename__(cls) -> str:
#         return cls.__name__.lower()


class BaseManager:
    def __init__(self, db: Database) -> None:
        self.db = db

class BaseMeta(ormar.ModelMeta):
    database = DATABASE
    metadata = SQL_METADATA
