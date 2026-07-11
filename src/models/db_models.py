from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.core.db import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(120), nullable=False)
    age = Column(Integer, nullable=False)
    email = Column(String(255), nullable=False)
    cpf = Column(String(11), nullable=False, unique=True)
    created_on = Column(DateTime(timezone=True), server_default=func.now())
    updated_on = Column(DateTime(timezone=True), onupdate=func.now())

    account = relationship("Accounts", back_populates="user", uselist=False)

    @property
    def account_id(self) -> int | None:
        return self.account.id if self.account else None


class Accounts(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    agency = Column(String(20), nullable=False)
    created_on = Column(DateTime(timezone=True), server_default=func.now())
    updated_on = Column(DateTime(timezone=True), onupdate=func.now())
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    user = relationship("Users", back_populates="account")
