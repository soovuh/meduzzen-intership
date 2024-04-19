from fastapi.responses import JSONResponse
from fastapi.requests import Request

from app.services.shared.base_exceptions import ObjectNotFound, AlreadyExists


def handle_object_not_found(_: Request, exc: ObjectNotFound) -> JSONResponse:
    return JSONResponse(content={"message": str(exc)}, status_code=404)


def handle_object_already_exists(_: Request, exc: AlreadyExists) -> JSONResponse:
    return JSONResponse(content={"message": str(exc)}, status_code=409)
