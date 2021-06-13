from typing import Any

from fastapi import APIRouter, Depends, Form, Query, status
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
async def retrieve_streaming(
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

    streaming_in.status = serializers.StreamingStatus.pause
    instance = await manager.create(object=streaming_in)
    
    return Response[serializers.Streaming](data=instance)()

@router.post("/on_publish")
async def streaming_publish(
    name: int = Form(...),
    manager: StreamingManager = Depends(get_manager(StreamingManager)),
    ) -> Any:

    instance = await manager.get(id=name)

    if not instance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="This streaming room is unavailable.")

    streaming_in = serializers.StreamingUpdate(status=serializers.StreamingStatus.playing)
    instance = serializers.Streaming(**instance)
    instance = await manager.update(instance=instance,update_object=streaming_in)

    return Response[serializers.Streaming](data=instance)()

@router.post("/on_publish_done")
async def streaming_done(
    name: int = Form(...),
    manager: StreamingManager = Depends(get_manager(StreamingManager)),
    ) -> Any:
    
    instance = await manager.get(id=name)

    if not instance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="This streaming room is unavailable.")

    streaming_in = serializers.StreamingUpdate(status=serializers.StreamingStatus.end)
    instance = serializers.Streaming(**instance)
    instance = await manager.update(instance=instance,update_object=streaming_in)

    return Response[serializers.Streaming](data=instance)()

