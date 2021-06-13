from databases import DatabaseURL
from starlette.config import Config
from starlette.datastructures import Secret

config = Config(".env")

PROJECT_NAME = "Streaming Logic"
VERSION = "1.0.0"
API_PREFIX = "/api"

SECRET_KEY = config("SECRET_KEY", cast=Secret, default="secret_key")

DB_USER = config("DB_USER", cast=str)
DB_PASSWORD = config("DB_PASSWORD", cast=Secret)
DB_HOST = config("DB_HOST", cast=str, default="db")
DB_PORT = config("DB_PORT", cast=str, default="5432")
DB_NAME = config("DB_NAME", cast=str)

DATABASE_URL = config(
  "DATABASE_URL",
  cast=DatabaseURL,
  default=f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# 60 minutes * 24 hours * 8 days = 8 days
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 8
