from fastapi import APIRouter
from app.routers import healthcheck, user, company


router = APIRouter()

router.include_router(healthcheck.router, prefix="")
router.include_router(user.router, prefix="")
router.include_router(company.router, prefix="")
