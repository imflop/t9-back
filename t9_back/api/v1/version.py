from fastapi import APIRouter

from t9_back import __distribution_name__, __version__

from ...lib.serializers.common import Version


router = APIRouter()


@router.get("/version", response_model=Version)
async def version() -> Version:
    return Version(name=__distribution_name__, version=__version__)
