from typing import Optional
from sqlalchemy import select

from app.db import models
from app.db.repositories.base_repo import SQLAlchemyRepository, Model


class UserRepository(SQLAlchemyRepository[models.User]):
    async def get_user_by_email(self, email: str) -> Optional[Model]:
        query = select(self.model).where(self.model.email == email)
        result = await self._db.execute(query)

        return result.scalar()
