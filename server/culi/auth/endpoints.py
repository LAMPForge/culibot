from culi.auth.service import AuthService
from culi.config import settings
from culi.openapi import IN_DEVELOPMENT_ONLY
from culi.routing import APIRouter
from fastapi.responses import RedirectResponse


router = APIRouter(tags=["auth"], include_in_schema=IN_DEVELOPMENT_ONLY)


@router.get("/auth/logout")
async def logout() -> RedirectResponse:
    response = RedirectResponse(settings.FRONTEND_BASE_URL)
    AuthService.set_auth_cookie(response=response, value="", expires=0)
    return response
