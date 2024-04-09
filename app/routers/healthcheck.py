from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def health_check():
    """Perform a basic app check."""
    return {"status": 200, "detail": "ok", "result": "working"}
