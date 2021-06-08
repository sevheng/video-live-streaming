from typing import Callable, Type

from database.base_class import BaseManager
from databases import Database
from fastapi import Depends
from starlette.requests import Request


def get_database(request: Request) -> Database:
    return request.app.state._db

def get_manager(Repo_type: Type[BaseManager]) -> Callable:
    def get_manage(db: Database = Depends(get_database)) -> Type[BaseManager]:
        return Repo_type(db)
    return get_manage
