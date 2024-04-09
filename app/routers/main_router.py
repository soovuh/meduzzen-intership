from fastapi import APIRouter
from app.routers import healthcheck


router = APIRouter()

# Additional routers
router.include_router(healthcheck.router, prefix="")
