from json import JSONDecodeError
from typing import Any, Dict

from fastapi import FastAPI
from fastapi.exceptions import HTTPException

from urlshorten.api.urls.resources import router
from urlshorten.api.exception_handlers import (
    bad_request_handler,
    http_exception_handler,
    validation_exception_handler,
)
from urlshorten.app.exceptions import AppException


def create_application() -> FastAPI:
    application = FastAPI()
    configure_healthcheck(application)
    configure_routes(application)
    configure_exception_handlers(application)

    return application


def configure_routes(application: FastAPI) -> None:
    application.include_router(router)


def configure_exception_handlers(application: FastAPI) -> None:
    application.add_exception_handler(HTTPException, http_exception_handler)
    application.add_exception_handler(JSONDecodeError, bad_request_handler)
    application.add_exception_handler(AppException, validation_exception_handler)


def configure_healthcheck(app: FastAPI) -> None:
    @app.get("/")
    async def healthcheck() -> Dict[str, Any]:
        return {
            "application": "Url Shortener Service",
            "healthy": True,
        }


app = create_application()
