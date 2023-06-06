from dependency_injector import containers, providers

from app.internal.repository import Repositories, postgresql
from app.internal.services.shortener import ShortenerService
# from app.internal.services.data import DataService
from app.pkg.settings import settings


class Services(containers.DeclarativeContainer):
    """Containers with services."""

    configuration = providers.Configuration(
        name="settings",
        pydantic_settings=[settings],
    )

    repositories: postgresql.Repositories = providers.Container(
        Repositories.postgres,
    )

    shortener_service = providers.Factory(
        ShortenerService,
        shortener_repository=repositories.shortener_repository,
    )
