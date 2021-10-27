from typing import Any

from fastapi import APIRouter, Depends, Form, Query, status
from main.dependencies import get_manager
from main.exception_handlers import HTTPException
from main.serializers import Response
from user.dependencies import get_current_active_user
from user.models import User

from streaming import serializers
from streaming.models import Streaming

router = APIRouter()

@router.get("/")
async def list_streaming(per_page: int = Query(10, gt=0),page: int = Query(1, gt=0)) -> Any:
    data = await Streaming.objects.select_related("user").paginate(page,per_page).all()
    total= await Streaming.objects.count()
    return Response(serializers.Streaming,data=data,per_page=per_page,page=page,total=total)()


@router.get("/{id}")
async def retrieve_streaming(id: int) -> Any:
    instance = await Streaming.objects.get_or_none(id=id)
    if not instance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="This streaming room is unavailable.")
    return Response(serializers.Streaming,data=instance)()

@router.post("/")
async def create_streaming(
    streaming_in: serializers.StreamingCreate,
    user : User =Depends(get_current_active_user)
    ) -> Any:
    streaming_in = streaming_in.dict()
    streaming_in['status'] = serializers.StreamingStatus.pause
    streaming_in['user'] = user
    instance = await Streaming.objects.create(**streaming_in)
    
    return Response(serializers.Streaming,data=instance)()

# @router.post("/on_publish")
# async def streaming_publish(
#     name: int = Form(...),
#     manager: StreamingManager = Depends(get_manager(StreamingManager)),
#     ) -> Any:

#     instance = await manager.get(id=name)

#     if not instance:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="This streaming room is unavailable.")

#     streaming_in = serializers.StreamingUpdate(status=serializers.StreamingStatus.playing)
#     instance = serializers.Streaming(**instance)
#     instance = await manager.update(instance=instance,update_object=streaming_in)

#     return Response(serializers.Streaming,data=instance)()

# @router.post("/on_publish_done")
# async def streaming_done(
#     name: int = Form(...),
#     manager: StreamingManager = Depends(get_manager(StreamingManager)),
#     ) -> Any:
    
#     instance = await manager.get(id=name)

#     if not instance:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="This streaming room is unavailable.")

#     streaming_in = serializers.StreamingUpdate(status=serializers.StreamingStatus.end)
#     instance = serializers.Streaming(**instance)
#     instance = await manager.update(instance=instance,update_object=streaming_in)

#     return Response(serializers.Streaming,data=instance)()

