import logging

from databases import Database
from fastapi import FastAPI
from main.config import DATABASE

logger = logging.getLogger(__name__)


async def connect_to_db(app: FastAPI) -> None:
    try:
        await DATABASE.connect()
        app.state._db = DATABASE
    except Exception as e:
        logger.warn("--- DB CONNECTION ERROR ---")
        logger.warn(e)
        logger.warn("--- DB CONNECTION ERROR ---")


async def close_db_connection(app: FastAPI) -> None:
    try:
        await app.state._db.disconnect()
    except Exception as e:
        logger.warn("--- DB DISCONNECT ERROR ---")
        logger.warn(e)
        logger.warn("--- DB DISCONNECT ERROR ---")
