from fastapi import status

from app.pkg.models.base import BaseAPIException

__all__ = [
    "ShortUrlNotExists",
]


class ShortUrlNotExists(BaseAPIException):
    message = "Short url does not exists"
    status_code = status.HTTP_404_NOT_FOUND
