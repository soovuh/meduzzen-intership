from sqlalchemy import select, delete
from typing import Generic, TypeVar, Type
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import models


Model = TypeVar("Model", bound=models.Base)


class SQLAlchemyRepository(Generic[Model]):
    """Repository for performing database queries."""

    def __init__(self, model: Type[Model], db: AsyncSession) -> None:
        self.model = model
        self._db = db

    async def create(self, data: dict) -> Model:
        try:
            instance = self.model(**data)
            self._db.add(instance)
            await self._db.commit()
            await self._db.refresh(instance)
            return instance
        except:
            return None

    async def get(self, id: int) -> Model:
        return await self._db.get(self.model, id)

    async def get_list(self, skip: int = 0, limit: int = 100) -> list[Model]:
        query = select(self.model).offset(skip).limit(limit)
        return list(await self._db.scalars(query))

    async def update(self, id: int, data: dict) -> Model:
        instance = await self.get(id)
        if instance:
            for key, value in data.items():
                setattr(instance, key, value)
            await self._db.commit()
            await self._db.refresh(instance)
            return instance
        return None

    async def delete(self, id: int) -> bool:
        instance = await self.get(id)
        if instance:
            await self._db.delete(instance)
            await self._db.commit()
            return True

        return False
