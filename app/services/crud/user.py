from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.db.models import User
from app.schemas.user import (
    UsersListResponse,
    UserDetail,
    SignUpRequest,
    UserUpdateRequest,
    UserSummary,
)
from app.utils.hashing import Hasher
from app.utils.logger import logger


class UserCRUD:
    @staticmethod
    async def get_all_users(
        db: AsyncSession, skip: int = 0, limit: int = 100
    ) -> UsersListResponse:
        """Get all users."""
        query = select(User).order_by(User.id).offset(skip).limit(limit)
        result = await db.execute(query)
        users = result.scalars().all()
        user_summaries = [UserSummary(id=user.id, name=user.name) for user in users]
        return UsersListResponse(users=user_summaries)

    @staticmethod
    async def get_user_by_id(db: AsyncSession, user_id: int) -> UserDetail:
        """Get user by ID."""
        query = select(User).where(User.id == user_id)

        result = await db.execute(query)
        user = result.scalars().first()

        if user:
            return UserDetail(
                id=user.id,
                name=user.name,
                email=user.email,
                is_active=user.is_active,
                created_at=user.created_at,
            )
        return None

    @staticmethod
    async def create_user(db: AsyncSession, user_data: SignUpRequest) -> UserDetail:
        """Create a new user."""
        hashed_password = Hasher.get_password_hash(user_data.password)

        user = User(
            name=user_data.name, email=user_data.email, hashed_password=hashed_password
        )
        try:
            db.add(user)
            await db.commit()
            await db.refresh(user)
            logger.info(f"Created user: {user.id} - {user.name}")
            return UserDetail(
                id=user.id,
                name=user.name,
                email=user.email,
                is_active=user.is_active,
                created_at=user.created_at,
            )
        except IntegrityError as e:
            await db.rollback()
            logger.error(f"Failed to create user: {user_data.email} - {e}")
            return None

    @staticmethod
    async def update_user(
        db: AsyncSession, user_id: int, user_data: UserUpdateRequest
    ) -> UserDetail:
        """Update an existing user."""
        query = select(User).where(User.id == user_id)
        result = await db.execute(query)
        user = result.scalars().first()

        if user:
            if user_data.name:
                user.name = user_data.name
            if user_data.password:
                hashed_password = Hasher.get_password_hash(user_data.password)
                user.hashed_password = hashed_password

            await db.commit()
            await db.refresh(user)
            logger.info(f"Updated user: {user.id} - {user.name}")
            return UserDetail(
                id=user.id,
                name=user.name,
                email=user.email,
                is_active=user.is_active,
                created_at=user.created_at,
            )

        logger.error(f"User not found with id: {user_id}")
        return None

    @staticmethod
    async def delete_user(db: AsyncSession, user_id: int) -> bool:
        """Delete an existing user."""
        query = select(User).where(User.id == user_id)
        result = await db.execute(query)
        user = result.scalars().first()

        if user:
            await db.delete(user)
            await db.commit()
            logger.info(f"Deleted user: {user.id} - {user.name}")
            return True

        logger.error(f"User not found with id: {user_id}")
        return False
