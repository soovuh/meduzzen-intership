from typing import Any

from app.services.shared import base_exceptions


class UserNotFound(base_exceptions.ObjectNotFound):
    def __init__(self, identifier: Any, model_name: str = "user") -> None:
        super().__init__(identifier, model_name)


class UserAlreadyExists(base_exceptions.AlreadyExists):
    def __init__(self, identifier: Any, model_name: str = "user") -> None:
        super().__init__(identifier, model_name)


class IncorrecUserData(base_exceptions.IncorrectData):
    def __init__(
        self, field_name: Any, identifier: Any, model_name: str = "user"
    ) -> None:
        super().__init__(field_name, identifier, model_name)


class UserTokenExpiried(base_exceptions.Expiried):
    def __init__(self, field_name: Any = "token", model_name: str = "user") -> None:
        super().__init__(field_name, model_name)
