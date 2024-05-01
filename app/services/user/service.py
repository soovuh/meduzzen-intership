from typing import List, Dict, Optional

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

    async def get_current_user(
        self, token: Optional[TokenPayload], auth0_token: Optional[Dict]
    ) -> User:
        if auth0_token:
            user = await self._repo.get_user_by_email(email=auth0_token["user_email"])

            if user is None:
                random_password = Hasher.generate_random_password()
                hashed_password = Hasher.get_password_hash(random_password)
                user = await self._repo.create(
                    {
                        "name": auth0_token["user_name"],
                        "email": auth0_token["user_email"],
                        "hashed_password": hashed_password,
                    }
                )
            return user
        elif token:
            user: User | None = await self._repo.get_user_by_email(token.sub)

            if user is None:
                raise exc.UserNotFound(identifier=token.sub)

            return user
        raise base_exceptions.CredentialsError()

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

    async def update_user(
        self,
        id: int,
        data: UserUpdateRequest,
        current_user: User,
    ) -> User:

        if not current_user.id == id:
            raise base_exceptions.CredentialsError()

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

    async def delete_user(self, id: int, current_user: User) -> UserDeletedResponse:

        if not current_user.id == id:
            raise base_exceptions.CredentialsError()

        deleted = await self._repo.delete(id=id)

        if deleted is False:
            raise exc.UserNotFound(identifier=id)

        return UserDeletedResponse()
