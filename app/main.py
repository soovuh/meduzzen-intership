from fastapi import FastAPI

from app.core.settings import Settings
from app.routers.main_router import router


app = FastAPI()
settings = Settings()

# Include main router
app.include_router(router, prefix="")
