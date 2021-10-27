import inspect
from typing import Any, Generic, List, TypeVar, Union

from fastapi import Form
from pydantic import BaseModel
from pydantic.fields import PrivateAttr, Type
from pydantic.generics import GenericModel

DataT = TypeVar('DataT')

def as_form(cls: Type[BaseModel]) -> Type[BaseModel]:
    """
    Adds an `as_form` class method to decorated models. The `as_form` class
    method can be used with `FastAPI` endpoints.

    Args:
        cls: The model class to decorate.

    Returns:
        The decorated class.

    """

    def make_form_parameter(field: BaseModel) -> Any:
        """
        Converts a field from a `Pydantic` model to the appropriate `FastAPI`
        parameter type.

        Args:
            field: The field to convert.

        Returns:
            Either the result of `Form`, if the field is not a sub-model, or
            the result of `Depends` if it is.

        """
        if issubclass(field.type_, BaseModel):
            # This is a sub-model.
            assert hasattr(field.type_, "as_form"), (
                f"Sub-model class for {field.name} field must be decorated with"
                f" `as_form` too."
            )
            return Depends(field.type_.as_form)
        else:
            return Form(field.default) if not field.required else Form(...)

    new_params = [
        inspect.Parameter(
            field.alias,
            inspect.Parameter.POSITIONAL_ONLY,
            default=make_form_parameter(field),
        )
        for field in cls.__fields__.values()
    ]

    async def _as_form(**data):
        return cls(**data)

    sig = inspect.signature(_as_form)
    sig = sig.replace(parameters=new_params)
    _as_form.__signature__ = sig
    setattr(cls, "as_form", _as_form)
    return cls

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

class Response():
    _response : PrivateAttr 

    def __init__(self,serializer_class,data,per_page=10,page=1,total=1) -> None:
        if isinstance(data,List):
            self._response = SerializersWithPagination[serializer_class](data=data,per_page=per_page,page=page,total=total)
        else:
            if data:
                self._response = Serializer[serializer_class](data=data)
            else:
                self._response = SerializerError[serializer_class](message="Not Found")

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self._response
