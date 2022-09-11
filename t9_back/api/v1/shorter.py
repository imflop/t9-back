import typing as t

from fastapi import (
    APIRouter,
    Depends,
    Response,
    status,
    Header
)
from fastapi.responses import RedirectResponse
from starlette.requests import Request

from ...lib.factories.services import (
    link_service_factory,
    qr_service_factory,
    shorter_service_factory,
)
from ...lib.serializers.link import Link, LinkIn, LinkTest
from ...lib.services.link import LinkService
from ...lib.services.qr import QRService
from ...lib.services.shorter import ShorterService


router = APIRouter()


@router.get("/decode", status_code=status.HTTP_301_MOVED_PERMANENTLY)
async def redirect_to_origin_url(
    request: Request,
    encoded_url: t.Union[str, int],
    user_agent: t.Optional[str] = Header(None),
    shorter_service: ShorterService = Depends(shorter_service_factory),
    link_service: LinkService = Depends(link_service_factory),
) -> Response:
    real_id = shorter_service.get_real_link_id(str(encoded_url))

    if link := await link_service.get_link(real_id):
        await link_service.increase_hit_count(link, request.client.host, user_agent)
        return RedirectResponse(link.original_url)

    return Response(status_code=status.HTTP_404_NOT_FOUND, content="Not Found")


@router.get("/link/{link_id}", response_model=LinkTest)
async def get_link(
    link_id: int,
    link_service: LinkService = Depends(link_service_factory),
) -> t.Union[Response, LinkTest]:
    if link := await link_service.get_link(link_id):
        return LinkTest.from_orm(link)

    return Response(status_code=status.HTTP_404_NOT_FOUND)


@router.post("/encode", response_model=Link, status_code=status.HTTP_201_CREATED)
async def short(
    new_link: LinkIn,
    shorter_service: ShorterService = Depends(shorter_service_factory),
    link_service: LinkService = Depends(link_service_factory),
    qr_service: QRService = Depends(qr_service_factory),
) -> t.Union[Response, Link]:
    link = await link_service.save_link(new_link)

    if link.id:
        link.short_url = shorter_service.make_short_link(link.id)
        link.qr = qr_service.make_qr(link.short_url)

        return await link_service.update_link(link)

    return Response(status_code=status.HTTP_404_NOT_FOUND)
