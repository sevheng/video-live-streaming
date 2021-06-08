from fastapi import APIRouter
from streaming.views import router as streaming_router

router = APIRouter()

router.include_router(streaming_router,prefix="/api")
