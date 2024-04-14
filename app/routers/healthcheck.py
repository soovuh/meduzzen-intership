from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text

from app.db.database import get_session


router = APIRouter(prefix="/healthcheck")


@router.get("")
def health_check():
    """Perform a basic app check."""
    return {"status": 200, "detail": "ok", "result": "working"}


@router.get("/db")
async def health_check_db(db: AsyncSession = Depends(get_session)):
    try:
        result = await db.execute(text("SELECT 1"))
        return {
            "status": 200,
            "detail": "Database connection is working",
            "result": "working",
        }
    except Exception as e:
        return {"status": 500, "detail": "Database connection error", "result": "error"}
