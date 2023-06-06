from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.pkg.models.base import BaseAPIException

__all__ = ["handle_internal_exception", "handle_api_exceptions"]


def handle_api_exceptions(request: Request, exc: BaseAPIException):
    """Handle all internal exceptions which inherited from
    `BaseAPIException`."""
    _ = request

    return JSONResponse(status_code=exc.status_code, content={"message": exc.message})


def handle_internal_exception(request: Request, exc: Exception):
    """Handle all internal unhandled exceptions."""
    _ = request

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": repr(exc)},
    )
