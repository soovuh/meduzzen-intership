from typing import Any


class ObjectNotFound(Exception):
    def __init__(self, identifier: Any, model_name: str) -> None:
        super().__init__(f"{model_name} with identifier - {identifier} not found")


class AlreadyExists(Exception):
    def __init__(self, identifier: Any, model_name: str) -> None:
        super().__init__(f"{model_name} with identifier - {identifier} already exists")


class IncorrectData(Exception):
    def __init__(self, field_name: Any, identifier: Any, model_name: str) -> None:
        super().__init__(
            f"Incorrect {field_name} for {model_name} with identifier - {identifier}"
        )


class Expiried(Exception):
    def __init__(self, field_name: Any, model_name: str) -> None:
        super().__init__(f"{field_name} for {model_name} expired")


class CredentialsError(Exception):
    def __init__(self) -> None:
        super().__init__(f"Could not validate credentials")
