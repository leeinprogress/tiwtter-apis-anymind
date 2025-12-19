from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.bootstrap.config import get_settings
from app.core.exceptions import TwitterAPIError
from app.presentation.middleware.error_handler import (
    global_exception_handler,
    twitter_api_error_handler,
)
from app.presentation.middleware.logging import LoggingMiddleware

settings = get_settings()


def setup_middleware(app: FastAPI) -> None:
    if settings.cors_origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.cors_origins_list,
            allow_credentials=False,
            allow_methods=["GET"],
            allow_headers=["Accept", "Content-Type"],
        )


    app.add_middleware(LoggingMiddleware)
    app.add_exception_handler(TwitterAPIError, twitter_api_error_handler)  # type: ignore[arg-type]
    app.add_exception_handler(Exception, global_exception_handler)

