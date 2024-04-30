from sqlalchemy import select
from typing import List

from app.db import models
from app.db.repositories.base_repo import SQLAlchemyRepository, Model


class CompanyRepository(SQLAlchemyRepository[models.Company]):
    async def get_public_list(self, skip: int = 0, limit: int = 100) -> List[Model]:
        query = (
            select(self.model)
            .filter(self.model.is_hidden == False)
            .offset(skip)
            .limit(limit)
        )
        return await self._db.scalars(query)
