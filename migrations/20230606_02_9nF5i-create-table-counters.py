"""
create table counters
"""

from yoyo import step

__depends__ = {}

steps = [
    step(
        """
        create table if not exists counters(
            id serial primary key,
            value bigint not null
        );
        """,
        """
        drop table if exists counters;
        """
    ),
    step(
        """
        insert into counters(id, value)
        values (1, 1000000);
        """,
        """
        delete from counters
        where id = 1;
        """
    )
]
