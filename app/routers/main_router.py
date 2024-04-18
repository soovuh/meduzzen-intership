from fastapi import APIRouter
from app.routers import healthcheck, user


router = APIRouter()

router.include_router(healthcheck.router, prefix="")
router.include_router(user.router, prefix="")
