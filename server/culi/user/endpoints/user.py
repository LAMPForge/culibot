from culi.auth.dependencies import WebUser
from culi.models.user import User
from culi.openapi import IN_DEVELOPMENT_ONLY
from culi.routing import APIRouter
from culi.user.schemas.user import UserRead, UserScopes

router = APIRouter(include_in_schema=IN_DEVELOPMENT_ONLY)


@router.get("/me", response_model=UserRead)
async def get_authenticated(auth_subject: WebUser) -> User:
    return auth_subject.subject


@router.get("/me/scopes", response_model=UserScopes)
async def get_authenticated_scopes(auth_subject: WebUser) -> UserScopes:
    return UserScopes(scopes=auth_subject.scopes)
