from culi.models.user import User
from culi.openapi import IN_DEVELOPMENT_ONLY
from culi.routing import APIRouter
from culi.user.schemas.user import UserRead


router = APIRouter(include_in_schema=IN_DEVELOPMENT_ONLY)


@router.get("/me", response_model=UserRead)
async def get_authenticated(auth_subject) -> User:
    return auth_subject.subject
