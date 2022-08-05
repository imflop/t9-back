from fastapi import (
    APIRouter,
    Depends,
    Response,
    status,
)

from ...lib.factories import settings_factory
from ...lib.settings import AppSettings


router = APIRouter()


@router.get("/health", responses={status.HTTP_200_OK: {}, status.HTTP_503_SERVICE_UNAVAILABLE: {}})
async def health(settings: AppSettings = Depends(settings_factory)) -> Response:
    if settings.host and settings.port:
        return Response(status_code=status.HTTP_200_OK)
    return Response(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
