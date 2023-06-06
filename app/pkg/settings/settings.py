"""Module for load settings form `.env` or if server running with parameter
`dev` from `.env.dev`"""
import pathlib
from functools import lru_cache

import pydantic
from dotenv import find_dotenv
from pydantic.env_settings import BaseSettings
from pydantic.types import PositiveInt, SecretStr


__all__ = ["Settings", "get_settings"]


class _Settings(BaseSettings):
    class Config:
        """Configuration of settings."""

        env_file_encoding = "utf-8"
        arbitrary_types_allowed = True


class Settings(_Settings):
    """Server settings.

    Formed from `.env` or `.env.dev`.
    """

    #: str: Name of API service
    API_INSTANCE_APP_NAME: str
    X_API_TOKEN: SecretStr

    # Postgresql
    POSTGRES_HOST: str
    POSTGRES_PORT: PositiveInt
    POSTGRES_USER: str
    POSTGRES_PASSWORD: SecretStr
    POSTGRES_DB: str

    # Logger
    LOGGER_LEVEL: pydantic.StrictStr
    LOGGER_DIR_PATH: pathlib.Path
    LOGGER_DIR_PATH_INTERNAL: pathlib.Path

    # Domain
    URL_DOMAIN: str


@lru_cache()
def get_settings(env_file: str = ".env") -> Settings:
    """Create settings instance."""
    return Settings(_env_file=find_dotenv(env_file))
