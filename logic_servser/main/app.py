import time

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from . import config, exception_handlers, tasks, urls


def get_application():
    app = FastAPI(title=config.PROJECT_NAME, version=config.VERSION)

    # Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Exception
    app.add_exception_handler(HTTPException,exception_handlers.http_exception_handler)
    app.add_exception_handler(RequestValidationError,exception_handlers.validation_exception_handler)

    # Event
    app.add_event_handler("startup", tasks.create_start_app_handler(app))
    app.add_event_handler("shutdown", tasks.create_stop_app_handler(app))

    app.include_router(urls.router)

    return app


app = get_application()

# @app.middleware("http")
# async def add_process_time_header(request: Request, call_next):
#     start_time = time.time()
#     response = await call_next(request)
#     process_time = time.time() - start_time
#     response.headers["X-Process-Time"] = str(process_time)
#     return response
