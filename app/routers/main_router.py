from fastapi import APIRouter
from routers import healthcheck


router = APIRouter()

# Additional routers
router.include_router(healthcheck.router, prefix="")
