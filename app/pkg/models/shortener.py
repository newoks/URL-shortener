from pydantic import AnyUrl, Field

from app.pkg.models.base import BaseModel

__all__ = [
    "UrlFields",
    "UrlModel",
    "ShortUrlModel",
    "FullUrlModel",
    "CounterModel",
    "CreateShortUrlCommand",
    "FullUrlCommand",
    "ShortUrlInternal",
]


class UrlFields:
    full_url = Field(
        description="Full url",
        example="https://music.yandex.ru/album/5307396/track/38633706",
    )
    short_url = Field(
        description="Short url with domain",
        example="const.com/A8z1",
    )
    short_url_code = Field(
        description="Short url code",
        example="A8z1",
    )
    counter_value = Field(
        description="Value of counter",
        example=1000000,
    )
    short_url_domain = Field(
        description="Domain for short url",
        example="const.com",
    )
    is_active = Field(
        description="Link state. Active - true. Inactive - false",
        example=True,
    )


class BaseUrl(BaseModel):
    """Base model for url."""


class UrlModel(BaseUrl):
    id: int
    full_url: AnyUrl = UrlFields.full_url
    short_url_domain: str = UrlFields.short_url_domain
    short_url_code: str = UrlFields.short_url_code
    is_active: bool = UrlFields.is_active


class ShortUrlModel(BaseUrl):
    short_url: str = UrlFields.short_url


class FullUrlModel(BaseUrl):
    full_url: AnyUrl = UrlFields.full_url


class CounterModel(BaseUrl):
    value: int = UrlFields.counter_value


class CreateShortUrlCommand(BaseUrl):
    full_url: AnyUrl = UrlFields.full_url
    short_url_domain: str = UrlFields.short_url_domain
    short_url_code: str = UrlFields.short_url_code


class FullUrlCommand(BaseUrl):
    short_url_domain: str = UrlFields.short_url_domain
    short_url_code: str = UrlFields.short_url_code


class ShortUrlInternal(BaseUrl):
    id: int
    full_url: AnyUrl = UrlFields.full_url
    short_url_domain: str = UrlFields.short_url_domain
    short_url_code: str = UrlFields.short_url_code
