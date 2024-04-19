from app.db import models
from app.db.repositories.base_repo import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository[models.User]):
    pass
