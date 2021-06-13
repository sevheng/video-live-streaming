from fastapi import APIRouter
from streaming.views import router as streaming_router
from user.views import router as user_router

router = APIRouter()

router.include_router(streaming_router,prefix="/api/streaming")
router.include_router(user_router,prefix="/api/user")
