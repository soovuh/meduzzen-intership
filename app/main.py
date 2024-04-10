from fastapi import FastAPI

from app.routers.main_router import router


app = FastAPI()

app.include_router(router, prefix="")
