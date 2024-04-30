from typing import Any

from app.services.shared import base_exceptions


class CompanyNotFound(base_exceptions.ObjectNotFound):
    def __init__(self, identifier: Any, model_name: str = "company") -> None:
        super().__init__(identifier, model_name)


class CompanyCreateError(base_exceptions.CreateError):
    def __init__(self, model_name: str = "company") -> None:
        super().__init__(model_name)
