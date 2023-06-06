"""
create table urls
"""

from yoyo import step

__depends__ = {}

steps = [
    step(
        """
        create table if not exists urls(
            id serial primary key,
            full_url varchar(255) not null,
            short_url_domain varchar(32) not null,
            short_url_code varchar(10),
            is_active bool default true,
            unique (full_url)
        );
        """,
        """
        drop table if exists urls;
        """
    )
]
