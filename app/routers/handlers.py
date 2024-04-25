from fastapi.responses import JSONResponse
from fastapi.requests import Request

from app.services.shared import base_exceptions


def handle_object_not_found(
    _: Request, exc: base_exceptions.ObjectNotFound
) -> JSONResponse:
    return JSONResponse(content={"message": str(exc)}, status_code=404)


def handle_object_already_exists(
    _: Request, exc: base_exceptions.AlreadyExists
) -> JSONResponse:
    return JSONResponse(content={"message": str(exc)}, status_code=409)


def incorrect_data(_: Request, exc: base_exceptions.IncorrectData) -> JSONResponse:
    return JSONResponse(content={"message": str(exc)}, status_code=401)


def expired(_: Request, exc: base_exceptions.Expiried) -> JSONResponse:
    return JSONResponse(content={"message": str(exc)}, status_code=401)


def credentials_error(_: Request, exc: base_exceptions.Expiried) -> JSONResponse:
    return JSONResponse(content={"message": str(exc)}, status_code=401)
