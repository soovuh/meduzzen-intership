from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_session
from app.services.crud.user import UserCRUD
from app.schemas.user import (
    UsersListResponse,
    UserDetail,
    SignUpRequest,
    UserUpdateRequest,
)


router = APIRouter(prefix="/users")


@router.get("/", response_model=UsersListResponse)
async def read_users(
    db: AsyncSession = Depends(get_session), skip: int = 0, limit: int = 100
):
    """Get all users"""
    return await UserCRUD.get_all_users(db, skip, limit)


@router.get("/{user_id}", response_model=UserDetail)
async def read_user(user_id: int, db: AsyncSession = Depends(get_session)):
    """Get a user by ID."""
    user = await UserCRUD.get_user_by_id(db, user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/", response_model=UserDetail)
async def create_new_user(
    user_data: SignUpRequest, db: AsyncSession = Depends(get_session)
):
    """Create a new user (Sign Up)."""
    user = await UserCRUD.create_user(db, user_data)

    if user is None:
        raise HTTPException(status_code=400, detail="Email already exists")
    return user


@router.put("/{user_id}", response_model=UserDetail)
async def update_existing_user(
    user_id: int, user_data: UserUpdateRequest, db: AsyncSession = Depends(get_session)
):
    """Update an existing user."""
    user = await UserCRUD.update_user(db, user_id, user_data)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/{user_id}", response_model=dict)
async def delete_existing_user(user_id: int, db: AsyncSession = Depends(get_session)):
    """Delete an existing user."""
    deleted = await UserCRUD.delete_user(db, user_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted successfully"}
