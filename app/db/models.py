from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import Column, DateTime, Integer, String, Boolean, ForeignKey, func


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(150))
    email = Column(String(255), unique=True)
    hashed_password = Column(String(100))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    companies = relationship("Company", back_populates="owner")


class Company(Base):
    __tablename__ = "companies"
    id = Column(Integer, primary_key=True)
    name = Column(String(150))
    description = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
    is_hidden = Column(Boolean, default=False)

    owner = relationship("User", back_populates="companies")
