from app.db.models import User
from app.schemas.user import (
    UsersListResponse,
    UserDetail,
    SignUpRequest,
    UserUpdateRequest,
    UserSummary
)
from app.db.repositories.user_repo import UserRepository
from app.services.user import exc
from app.utils.hashing import Hasher


class UserService:
    def __init__(self, repo: UserRepository) -> None:
        self._repo = repo
 
    async def get_user_list(self, skip: int = 0, limit: int = 100) -> UsersListResponse:
        users = await self._repo.get_list(skip, limit)
        user_summaries = [UserSummary(id=user.id, name=user.name) for user in users]
        return UsersListResponse(users=user_summaries)

    async def get_user(self, id: int) -> UserDetail:
        user: User | None = await self._repo.get(id=id)
        
        if user is None:
            raise exc.UserNotFound(identifier=id)
        
        return UserDetail(
            id=user.id,
            name=user.name,
            email=user.email,
            is_active=user.is_active,
            created_at=user.created_at
        )
        
    async def create_user(self, data: SignUpRequest) -> UserDetail:
        data_dict = data.model_dump()

        hashed_password = Hasher.get_password_hash(data_dict["password"])
        data_dict["hashed_password"] = hashed_password
        del data_dict["password"]
        
        user = await self._repo.create(data=data_dict)

        if user is None:
            raise exc.UserAlreadyExists(identifier=data.email)
        
        return UserDetail(
            id=user.id,
            name=user.name,
            email=user.email,
            is_active=user.is_active,
            created_at=user.created_at
        )
    
    async def update_user(self, id: int, data: UserUpdateRequest) -> UserDetail:
        user = await self._repo.update(id=id, data=data.model_dump())

        if user is None:
            raise exc.UserNotFound(identifier=id)
        
        return UserDetail(
            id=user.id,
            name=user.name,
            email=user.email,
            is_active=user.is_active,
            created_at=user.created_at
        )
    
    async def delete_user(self, id: int) -> None:
        deleted = await self._repo.delete(id=id)
        
        if deleted is False:
            raise exc.UserNotFound(identifier=id)
