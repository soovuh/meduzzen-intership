import os
import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.main_router import router


app = FastAPI()

origins = [
    "http://127.0.0.1:8000",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="")

if __name__ == "__main__":
    host = os.getenv("HOST")
    port_str = os.getenv("PORT")

    port = int(port_str)

    config = uvicorn.Config("app.main:app", port=port, host=host, reload=True, log_level="info")
    server = uvicorn.Server(config)
    server.run()
