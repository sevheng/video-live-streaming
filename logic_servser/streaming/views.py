from typing import Any

from fastapi import APIRouter, Depends, Query, status
from main.dependencies import get_manager
from main.exception_handlers import HTTPException
from main.serializers import Response

from streaming import serializers
from streaming.models import StreamingManager

router = APIRouter()

@router.get("/")
async def list_streaming(
    per_page: int = Query(10, gt=0),
    page: int = Query(1, gt=0),
    manager: StreamingManager = Depends(get_manager(StreamingManager))
    ) -> Any:
    data,total = await manager.list(limit=per_page,page=page)
    return Response[serializers.Streaming](data=data,per_page=per_page,page=page,total=total)()


@router.get("/{id}")
async def list_streaming(
    id: int,
    manager: StreamingManager = Depends(get_manager(StreamingManager))
    ) -> Any:
    instance = await manager.get(id=id)
    if not instance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="This streaming room is unavailable.")
    return Response[serializers.Streaming](data=instance)()

@router.post("/")
async def create_streaming(
    streaming_in: serializers.StreamingCreate,
    manager: StreamingManager = Depends(get_manager(StreamingManager)),
    ) -> Any:

    instance = await manager.create(object=streaming_in)
    
    return Response[serializers.Streaming](data=instance)()

