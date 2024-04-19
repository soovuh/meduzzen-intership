from typing import Any


class ObjectNotFound(Exception):
    def __init__(self, identifier: Any, model_name: str) -> None:
        super().__init__(f"{model_name} with identifier - {identifier} not found")


class AlreadyExists(Exception):
    def __init__(self, identifier: Any, model_name: str) -> None:
        super().__init__(f"{model_name} with identifier - {identifier} already exists")
