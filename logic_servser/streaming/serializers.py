from enum import Enum
from typing import Optional

from pydantic import BaseModel, validator
from pydantic.fields import Field


class StreamingStatus(str, Enum):
    playing = 'playing'
    end = 'end'
    
class StreamingBase(BaseModel):
    name: Optional[str] = None
    status: Optional[StreamingStatus] = Field()

    @validator('status')
    def validate_status(cls, v):
        if ' ' not in v:
            raise ValueError('must contain a space')
        return v.title()


class StreamingCreate(StreamingBase):
    name: str
    status: StreamingStatus

class StreamingUpdate(StreamingBase):
    pass

# class StreamingInDB(StreamingBase):
#     id: int
#     name: str
#     status: str

#     class Config:
#         orm_mode = True

class Streaming(StreamingBase):
    id: int
    name: str
    status: str
