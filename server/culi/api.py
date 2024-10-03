from fastapi import APIRouter
from culi.user.endpoints import router as user_router
from culi.auth.endpoints import router as auth_router

router = APIRouter(prefix="/v1")

# /users
router.include_router(auth_router)
router.include_router(user_router)