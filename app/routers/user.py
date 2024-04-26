from fastapi import APIRouter, Depends, Security
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, AnyStr, Dict

from app.db.database import get_session
from app.db import models
from app.services.user.service import UserService
from app.db.repositories.user_repo import UserRepository
from app.schemas.token import TokenSchema, TokenPayload
from app.utils.jwt_auth0 import VerifyAuth0Token
from app.utils.jwt_classic import VerifyToken
from app.schemas.user import (
    UserDetail,
    SignUpRequest,
    SignInRequest,
    UserUpdateRequest,
    UserDeletedResponse,
    UserSummary,
)


router = APIRouter(prefix="/users")
auth0 = VerifyAuth0Token()
auth_classic = VerifyToken()


async def get_user_service(db: AsyncSession = Depends(get_session)) -> UserService:
    user_repository = UserRepository(models.User, db)
    return UserService(repo=user_repository)


async def get_active_user(
    user_service: UserService = Depends(get_user_service),
    auth0_token: Optional[Dict] = Security(auth0.verify),
    token: Optional[TokenPayload] = Depends(auth_classic.verify),
):
    return await user_service.get_current_user(token=token, auth0_token=auth0_token)


@router.get("/", response_model=List[UserSummary])
async def read_users(
    user_service: UserService = Depends(get_user_service),
    skip: int = 0,
    limit: int = 100,
):
    """Get all users"""
    return await user_service.get_user_list(skip, limit)


@router.get("/me", response_model=UserDetail)
async def read_current_user(
    token: Optional[TokenPayload] = Depends(auth_classic.verify),
    user_service: UserService = Depends(get_user_service),
    auth0_token: Optional[Dict] = Security(auth0.verify),
):
    """Get a user by token"""
    return await user_service.get_current_user(token=token, auth0_token=auth0_token)


@router.get("/{user_id}", response_model=UserDetail)
async def read_user(
    user_id: int, user_service: UserService = Depends(get_user_service)
):
    """Get a user by ID."""
    return await user_service.get_user(id=user_id)


@router.post("/", response_model=UserDetail)
async def create_new_user(
    user_data: SignUpRequest, user_service: UserService = Depends(get_user_service)
):
    """Create a new user (Sign Up)."""
    return await user_service.create_user(data=user_data)


@router.post("/signin", response_model=TokenSchema)
async def signin(
    data: SignInRequest, user_service: UserService = Depends(get_user_service)
):
    """User sign in"""
    return await user_service.signin_user(data=data)


@router.put("/{user_id}", response_model=UserDetail)
async def update_existing_user(
    user_id: int,
    user_data: UserUpdateRequest,
    user_service: UserService = Depends(get_user_service),
    current_user: models.User = Depends(get_active_user),
):
    """Update an existing user."""
    return await user_service.update_user(user_id, user_data, current_user)


@router.delete("/{user_id}", response_model=UserDeletedResponse)
async def delete_existing_user(
    user_id: int,
    user_service: UserService = Depends(get_user_service),
    current_user: models.User = Depends(get_active_user)
):
    """Delete an existing user."""
    return await user_service.delete_user(user_id, current_user)
