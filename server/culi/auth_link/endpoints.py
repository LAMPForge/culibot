from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import RedirectResponse
from starlette.status import HTTP_202_ACCEPTED
from fastapi import Depends, Form, Request, status

from culi.auth.dependencies import WebUserOrAnonymous
from culi.auth.models import is_user
from culi.auth.service import AuthService
from culi.auth_link.schemas import AuthLinkRequest
from culi.common.http import ReturnTo
from culi.config import settings
from culi.exceptions import CuliRedirectionError
from culi.openapi import IN_DEVELOPMENT_ONLY
from culi.postgres import get_db_session
from culi.routing import APIRouter
from culi.auth_link.service import auth_link as auth_link_service, AuthLinkError

router = APIRouter(
    prefix="/auth_link", tags=["auth_link"], include_in_schema=IN_DEVELOPMENT_ONLY
)


@router.post("/request", name="auth_link:request", status_code=HTTP_202_ACCEPTED)
async def request_auth_link(
    auth_link_request: AuthLinkRequest,
    session: AsyncSession = Depends(get_db_session),
) -> None:
    auth_link, token = await auth_link_service.request(
        session, auth_link_request.email,
    )

    await auth_link_service.send(
        auth_link,
        token,
        base_url=str(settings.generate_frontend_url("/login/auth-link/authenticate")),
        extra_url_params={"return_to": auth_link_request.return_to}
        if auth_link_request.return_to
        else {},
    )


@router.post("/authenticate", name="auth_link:authenticate")
async def authenticate_auth_link(
    request: Request,
    return_to: ReturnTo,
    auth_subject: WebUserOrAnonymous,
    token: str = Form(),
    session: AsyncSession = Depends(get_db_session),
) -> RedirectResponse:
    if is_user(auth_subject):
        return RedirectResponse(return_to, 303)

    try:
        user = await auth_link_service.authenticate(session, token)
    except AuthLinkError as e:
        raise CuliRedirectionError(
            e.message, e.status_code, return_to=return_to,
        ) from e

    return AuthService.generate_login_cookie_response(
        request=request, user=user, return_to=return_to
    )
