from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status

from app.internal.services import Services
from app.internal.services.shortener import ShortenerService
from app.pkg.models import ShortUrlModel, FullUrlModel

__all__ = ["router"]


router = APIRouter(tags=["Shortener"], prefix="/shortener")


@router.get(
    "/",
    response_model=FullUrlModel,
    status_code=status.HTTP_200_OK,
    description="Get full url by short",
)
@inject
async def get_full_url(
    short_url: str,
    shortener_service: ShortenerService = Depends(Provide[Services.shortener_service]),
):
    return await shortener_service.get_full_url(short_url=short_url)


@router.post(
    "/",
    response_model=ShortUrlModel,
    status_code=status.HTTP_201_CREATED,
    description="Create short link",
)
@inject
async def create_short_url(
    cmd: FullUrlModel,
    shortener_service: ShortenerService = Depends(Provide[Services.shortener_service]),
):
    return await shortener_service.create_short_url(cmd=cmd)


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Delete short link",
)
@inject
async def delete_short_url(
    short_url: str,
    shortener_service: ShortenerService = Depends(Provide[Services.shortener_service]),
):
    return await shortener_service.delete_short_url(short_url=short_url)
