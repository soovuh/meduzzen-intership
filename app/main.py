import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.main_router import router
from app.core.settings import settings
from app.db.database import (
    create_engine,
    create_sessionmaker,
    get_session,
    get_session_imp,
)
from app.db.redis import get_redis, get_redis_imp


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


def register_db(app: FastAPI) -> None:
    engine = create_engine(settings)
    session_maker = create_sessionmaker(engine)

    app.dependency_overrides[get_session] = get_session_imp(session_maker)


def register_redis(app: FastAPI) -> None:
    redis_fn = get_redis
    app.dependency_overrides[get_redis] = get_redis_imp(redis_fn)


register_db(app)
register_redis(app)


if __name__ == "__main__":
    config = uvicorn.Config(
        "app.main:app",
        port=settings.port,
        host=settings.host,
        reload=True,
        log_level="info",
    )

    server = uvicorn.Server(config)
    server.run()
