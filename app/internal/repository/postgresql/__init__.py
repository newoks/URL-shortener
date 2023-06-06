from dependency_injector import containers, providers

from .shortener import ShortenerRepository


class Repositories(containers.DeclarativeContainer):
    shortener_repository = providers.Factory(ShortenerRepository)
