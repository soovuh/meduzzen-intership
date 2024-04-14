from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.settings import settings, Settings


def create_engine(settings: Settings) -> AsyncEngine:
    """
    Create an asynchronous SQLAlchemy engine using the provided settings.
    """
    return create_async_engine(build_db_url(settings))


def create_sessionmaker(engine: AsyncEngine) -> async_sessionmaker:
    """
    Create an asynchronous session maker bound to the provided engine.
    """
    return async_sessionmaker(bind=engine)


def build_db_url(settings: Settings) -> str:
    """
    Build a database URL string based on the provided settings.
    """
    return f"postgresql+asyncpg://{settings.db_username}:{settings.db_password}@{settings.host}/{settings.db_name}"


async def get_session(session_maker: async_sessionmaker) -> AsyncSession:
    """
    Dependency to yield an async session from the provided session maker.
    """
    async with session_maker() as session:
        yield session