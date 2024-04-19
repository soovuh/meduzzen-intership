from fastapi.responses import JSONResponse
from fastapi.requests import Request

from app.services.shared.base_exceptions import ObjectNotFound


def handle_object_not_found(_: Request, exc: ObjectNotFound) -> JSONResponse:
    return JSONResponse(
        content={"message": str(exc)},
        status_code=404
    )
