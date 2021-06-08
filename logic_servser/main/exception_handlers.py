
from typing import Any, Dict, Optional

from fastapi import HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse

from .serializers import SerializerError

# class HTTPException(BaseHTTPException):
#     def __init__(
#         self,
#         status_code: int,
#         detail:  SerializerError = SerializerError(),
#         headers: Optional[Dict[str, Any]] = None,
#     ) -> None:
#         super().__init__(status_code=status_code, detail=detail.json())
#         self.headers = headers

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error = exc.errors()
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=SerializerError(message=error[0]['msg'],errors = error).dict(),
    )


async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=SerializerError(message=exc.detail).dict(),
    )
