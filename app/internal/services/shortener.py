import logging
import string

from starlette import status

from app.internal.repository.postgresql import ShortenerRepository
from app.pkg import models
from app.pkg.logger import get_logger

__all__ = ["ShortenerService"]

from app.pkg.models.exceptions.repository import EmptyResult
from app.pkg.models.exceptions.shortener import ShortUrlNotExists
from app.pkg.settings import settings


class ShortenerService:
    __logger: logging.Logger
    __shortener_repository: ShortenerRepository

    def __init__(
        self,
        shortener_repository: ShortenerRepository,
    ):
        self.__shortener_repository = shortener_repository
        self.__logger = get_logger(__name__)

    async def create_short_url(self, cmd: models.FullUrlModel) -> models.ShortUrlModel:
        """
        Check if there is a short url for this full url.
        If there is, then return it.
        If not, generate a new one.
        """
        try:
            result = await self.__shortener_repository.read_short_url_code(cmd=cmd)
            return models.ShortUrlModel(
                short_url=f"{result.short_url_domain}/{result.short_url_code}"
            )
        except EmptyResult:
            return await self.generate_short_url(cmd=cmd)

    async def generate_short_url(self, cmd: models.FullUrlModel) -> models.ShortUrlModel:
        """
        We get the id from the counters table and generate a short url code based on it.
        Generation based on the ID from the table guarantees us the uniqueness of the short url code.
        """
        counter = await self.__shortener_repository.update_counter_value()
        short_url_code = self.id_to_short_url_code(id=counter.value)
        result = await self.__shortener_repository.create(
            cmd=models.CreateShortUrlCommand(
                full_url=cmd.full_url,
                short_url_domain=settings.URL_DOMAIN,
                short_url_code=short_url_code,
            )
        )
        return models.ShortUrlModel(
            short_url=f"{result.short_url_domain}/{result.short_url_code}"
        )

    async def get_full_url(self, short_url: str) -> models.FullUrlModel:
        try:
            short_url_domain, short_url_code = short_url.split("/")
            return await self.__shortener_repository.read_full_url(
                cmd=models.FullUrlCommand(
                    short_url_domain=short_url_domain,
                    short_url_code=short_url_code,
                )
            )
        except EmptyResult:
            raise ShortUrlNotExists

    async def delete_short_url(self, short_url: str):
        try:
            short_url_domain, short_url_code = short_url.split("/")
            await self.__shortener_repository.delete_short_url(
                cmd=models.FullUrlCommand(
                    short_url_domain=short_url_domain,
                    short_url_code=short_url_code,
                )
            )
        except EmptyResult:
            raise ShortUrlNotExists

    @staticmethod
    def id_to_short_url_code(id: int) -> str:
        """
        A function to convert a decimal number to a number with base 62.
        """
        base62_symbols = string.ascii_uppercase + string.ascii_lowercase + string.digits
        short_url = ""

        while id > 0:
            short_url += base62_symbols[id % 62]
            id //= 62

        return short_url[len(short_url):: -1]
