from typing import List
from jose import jwt
from jose.exceptions import JWTError
from datetime import datetime
from pydantic import ValidationError

from app.db.models import User
from app.schemas.token import TokenSchema, TokenPayload
from app.db.repositories.user_repo import UserRepository
from app.services.user import exc
from app.utils.hashing import Hasher
from app.services.shared import base_exceptions
from app.schemas.user import (
    SignUpRequest,
    UserUpdateRequest,
    UserDeletedResponse,
    SignInRequest,
)
from app.utils.jwt_classic import (
    create_access_token,
    create_refresh_token,
    JWT_SECRET_KEY,
    ALGORITHM,
)


class UserService:
    def __init__(self, repo: UserRepository) -> None:
        self._repo = repo

    async def get_user_list(self, skip: int = 0, limit: int = 100) -> List[User]:
        users = await self._repo.get_list(skip, limit)
        return users

    async def get_user(self, id: int) -> User:
        user: User | None = await self._repo.get(id=id)

        if user is None:
            raise exc.UserNotFound(identifier=id)

        return user

    async def get_current_user(self, token: str) -> User:
        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
            token_data = TokenPayload(**payload)

            if datetime.fromtimestamp(token_data.exp) < datetime.now():
                raise exc.UserTokenExpiried()

        except (JWTError, ValidationError):
            raise base_exceptions.CredentialsError()

        user: User | None = await self._repo.get_user_by_email(token_data.sub)

        if user is None:
            raise exc.UserNotFound(identifier=token_data.sub)

        return user

    async def create_user(self, data: SignUpRequest) -> User:
        data_dict = data.model_dump()

        hashed_password = Hasher.get_password_hash(data_dict["password"])
        data_dict["hashed_password"] = hashed_password
        del data_dict["password"]

        user = await self._repo.create(data=data_dict)

        if user is None:
            raise exc.UserAlreadyExists(identifier=data.email)

        return user

    async def signin_user(self, data: SignInRequest) -> TokenSchema:
        user = await self._repo.get_user_by_email(email=data.email)

        if user is None:
            raise exc.UserNotFound(identifier=data.email)

        hashed_password = user.hashed_password

        if not Hasher.verify_password(data.password, hashed_password):
            raise exc.IncorrecUserData(field_name="password", identifier=data.email)

        return {
            "access_token": create_access_token(user.email),
            "refresh_token": create_refresh_token(user.email),
        }

    async def signin_auth0_user(self, data: dict) -> TokenSchema:
        user = await self._repo.get_user_by_email(email=data["user_email"])

        if user is None:
            random_password = Hasher.generate_random_password()
            hashed_password = Hasher.get_password_hash(random_password)
            user = await self._repo.create(
                {
                    "name": data["user_name"],
                    "email": data["user_email"],
                    "hashed_password": hashed_password,
                }
            )

        return {
            "access_token": create_access_token(user.email),
            "refresh_token": create_refresh_token(user.email),
        }

    async def update_user(self, id: int, data: UserUpdateRequest) -> User:
        data_dict = data.model_dump()
        if not data.name:
            del data_dict["name"]
        if data.password:
            hashed_password = Hasher.get_password_hash(data.password)
            data_dict["hashed_password"] = hashed_password

        del data_dict["password"]

        user = await self._repo.update(id=id, data=data_dict)

        if user is None:
            raise exc.UserNotFound(identifier=id)

        return user

    async def delete_user(self, id: int) -> UserDeletedResponse:
        deleted = await self._repo.delete(id=id)

        if deleted is False:
            raise exc.UserNotFound(identifier=id)

        return UserDeletedResponse()
