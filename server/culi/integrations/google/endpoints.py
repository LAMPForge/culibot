import uuid

from httpx_oauth.integrations.fastapi import OAuth2AuthorizeCallback
from httpx_oauth.oauth2 import OAuth2Token
from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import RedirectResponse

from culi.auth.dependencies import WebUserOrAnonymous
from culi.auth.models import is_user
from culi.auth.service import AuthService
from culi.common import jwt
from culi.common.http import ReturnTo
from culi.common.jwt import TYPE
from culi.config import settings
from culi.exceptions import CuliRedirectionError
from culi.integrations.google.schemas import GoogleServiceError
from culi.integrations.google.service import google_oauth_client, google as google_service
from culi.openapi import IN_DEVELOPMENT_ONLY
from culi.postgres import get_db_session
from culi.routing import APIRouter

oauth2_authorize_callback = OAuth2AuthorizeCallback(
    google_oauth_client, route_name="integrations:google:callback"
)


class OAuthCallbackError(CuliRedirectionError): ...


router = APIRouter(
    prefix="/integrations/google",
    tags=["integrations_google"],
    include_in_schema=IN_DEVELOPMENT_ONLY,
)


@router.get("/authorize", name="integrations:google:authorize")
async def authorize(
    request: Request,
    auth_subject: WebUserOrAnonymous,
    return_to: ReturnTo,
) -> RedirectResponse:
    state = {"return_to": return_to}

    if is_user(auth_subject):
        state["user_id"] = str(auth_subject.subject.id)

    encoded_state = jwt.encode(data=state, secret=settings.SECRET, type=TYPE.google_oauth)
    authorization_url = await google_oauth_client.get_authorization_url(
        redirect_uri=str(request.url_for("integrations:google:callback")),
        state=encoded_state,
        scope=[
            "https://www.googleapis.com/auth/userinfo.profile",
            "https://www.googleapis.com/auth/userinfo.email",
        ],
    )
    return RedirectResponse(authorization_url, 303)


@router.get("/callback", name="integrations:google:callback")
async def callback(
    request: Request,
    auth_subject: WebUserOrAnonymous,
    session: AsyncSession = Depends(get_db_session),
    access_token_state: tuple[OAuth2Token, str | None] = Depends(
        oauth2_authorize_callback
    ),
) -> RedirectResponse:
    token_data, state = access_token_state
    error_description = token_data.get("error_description")
    if error_description:
        raise OAuthCallbackError(error_description)
    if not state:
        raise OAuthCallbackError("No state")

    try:
        state_data = jwt.decode(
            token=state, secret=settings.SECRET, type=TYPE.google_oauth
        )
    except jwt.DecodeError as e:
        raise OAuthCallbackError("Invalid state") from e

    return_to = state_data.get("return_to", None)
    state_user_id = state_data.get("user_id")

    try:
        if (
            is_user(auth_subject)
            and state_user_id is not None
            and auth_subject.subject.id == uuid.UUID(state_user_id)
        ):
            user = await google_service.link_user(
                session, user=auth_subject.subject, token=token_data
            )
        else:
            user = await google_service.login_or_signup(session, token=token_data)
    except GoogleServiceError as e:
        raise OAuthCallbackError(e.message, e.status_code, return_to=return_to) from e

    return AuthService.generate_login_cookie_response(
        request=request, user=user, return_to=return_to
    )
