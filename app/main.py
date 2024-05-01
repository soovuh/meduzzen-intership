import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from app.routers.main_router import router
from app.routers import handlers
from app.utils.logger import logger
from app.utils.middleware import log_middleware
from app.core.settings import settings
from app.db.database import (
    create_engine,
    create_sessionmaker,
    get_session,
    get_session_imp,
)
from app.db.redis import get_redis, get_redis_imp
from app.services.shared.base_exceptions import (
    ObjectNotFound,
    AlreadyExists,
    Expiried,
    CredentialsError,
    IncorrectData,
    AccessError,
)


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

app.add_middleware(BaseHTTPMiddleware, dispatch=log_middleware)

app.include_router(router, prefix="")

app.add_exception_handler(ObjectNotFound, handlers.handle_object_not_found)
app.add_exception_handler(AlreadyExists, handlers.handle_object_already_exists)
app.add_exception_handler(Expiried, handlers.expired)
app.add_exception_handler(CredentialsError, handlers.credentials_error)
app.add_exception_handler(IncorrectData, handlers.incorrect_data)
app.add_exception_handler(AccessError, handlers.access_error)


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

    logger.info("Starting API")
    server.run()
