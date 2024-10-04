from fastapi import APIRouter
from culi.user.endpoints import router as user_router
from culi.auth.endpoints import router as auth_router
from culi.auth_link.endpoints import router as auth_link_router
from culi.integrations.google.endpoints import router as google_router

router = APIRouter(prefix="/v1")

# /users
router.include_router(auth_router)
router.include_router(auth_link_router)
router.include_router(google_router)
router.include_router(user_router)