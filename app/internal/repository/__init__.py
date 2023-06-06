from dependency_injector import containers, providers

from . import postgresql
from .repository import BaseRepository

__all__ = ["Repositories"]


class Repositories(containers.DeclarativeContainer):
    postgres = providers.Container(postgresql.Repositories)
