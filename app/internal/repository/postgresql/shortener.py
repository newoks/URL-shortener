from app.internal.repository.postgresql.connection import get_connection
from app.internal.repository.postgresql.handlers.collect_response import (
    collect_response,
)
from app.internal.repository.repository import Repository
from app.pkg import models

__all__ = ["ShortenerRepository"]


class ShortenerRepository(Repository):
    @collect_response
    async def create(
        self,
        cmd: models.CreateShortUrlCommand
    ) -> models.ShortUrlInternal:
        q = """
            insert into urls(
                full_url, short_url_domain, short_url_code
            ) values (
                %(full_url)s,
                %(short_url_domain)s,
                %(short_url_code)s
            )
            on conflict (full_url) do update 
            set is_active = true
            returning id, full_url, short_url_domain, short_url_code;
        """
        async with get_connection() as cur:
            await cur.execute(q, cmd.to_dict())
            return await cur.fetchone()

    @collect_response
    async def update_counter_value(self) -> models.CounterModel:
        q = """
            update counters
            set value = value + 1
            where id = 1
            returning value;
        """
        async with get_connection() as cur:
            await cur.execute(q)
            return await cur.fetchone()

    @collect_response
    async def delete_short_url(
        self,
        cmd: models.FullUrlCommand,
    ) -> models.UrlModel:
        q = """
            update urls
            set is_active = false
            where short_url_code = %(short_url_code)s
            and short_url_domain = %(short_url_domain)s
            returning id, full_url, short_url_domain, short_url_code, is_active;
        """
        async with get_connection() as cur:
            await cur.execute(q, cmd.to_dict())
            return await cur.fetchone()

    @collect_response
    async def read_full_url(
        self,
        cmd: models.FullUrlCommand,
    ) -> models.FullUrlModel:
        q = """
            select full_url
            from urls
            where short_url_code = %(short_url_code)s
            and short_url_domain = %(short_url_domain)s
            and is_active = true;
        """
        async with get_connection() as cur:
            await cur.execute(q, cmd.to_dict())
            return await cur.fetchone()

    @collect_response
    async def read_short_url_code(
        self,
        cmd: models.FullUrlModel,
    ) -> models.ShortUrlInternal:
        q = """
                select id, full_url, short_url_domain, short_url_code
                from urls
                where full_url = %(full_url)s
                and is_active = true;
            """
        async with get_connection() as cur:
            await cur.execute(q, cmd.to_dict())
            return await cur.fetchone()
