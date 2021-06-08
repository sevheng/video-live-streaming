from typing import Any, Generic, List, TypeVar, Union

from pydantic.fields import PrivateAttr
from pydantic.generics import GenericModel

DataT = TypeVar('DataT')

class SerializerBase(GenericModel, Generic[DataT]):
    code: int = 1
    message: str = "success"

class SerializerError(SerializerBase[DataT], Generic[DataT]):
    code: int = 0
    message: str = "unsuccess"
    errors: List = []

class Serializers(SerializerBase[DataT], Generic[DataT]):
    data: List[DataT] = []

class SerializersWithPagination(Serializers[DataT], Generic[DataT]):
    per_page: int
    page: int
    total: int

class Serializer(SerializerBase[DataT], Generic[DataT]):
    data: DataT

    def dict(
        self,
        *,
        include: Union['AbstractSetIntStr', 'MappingIntStrAny'] = None,
        exclude: Union['AbstractSetIntStr', 'MappingIntStrAny'] = None,
        by_alias: bool = False,
        skip_defaults: bool = None,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,) -> 'DictStrAny':
        _dict = super().dict(include=include, exclude=exclude, by_alias=by_alias, skip_defaults=skip_defaults, exclude_unset=exclude_unset, exclude_defaults=exclude_defaults, exclude_none=exclude_none)
        _dict |= _dict['data']
        del _dict['data']
        return _dict

class Response(Generic[DataT]):
    _response : PrivateAttr 

    def __init__(self,data,per_page=10,page=1,total=1) -> None:
        if isinstance(data,List):
            self._response = SerializersWithPagination[DataT](data=data,per_page=per_page,page=page,total=total)
        else:
            if data:
                self._response = Serializer[DataT](data=data)
            else:
                self._response = SerializerError[DataT](message="Not Found")

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self._response
