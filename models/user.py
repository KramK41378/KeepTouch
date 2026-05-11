from __future__ import annotations
from hashlib import sha512
from datetime import datetime
from typing import TYPE_CHECKING

from flask_login import UserMixin
from pydantic import BaseModel, Field
from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from databases import SqlAlchemyBase

if TYPE_CHECKING:
    from .post import Post, PostORM


class User(BaseModel):
    name: str
    username: str
    email: str
    profile_image_path: str
    description: str
    hashed_password: str
    created_at: datetime | None = Field(default=None, json_schema_extra={"readOnly": True})

    posts: list['Post'] | None = None

    @classmethod
    def from_custom_orm(cls, user_orm: 'UserORM') -> 'User':
        from .post import Post
        user = cls(
            name=user_orm.name,
            username=user_orm.username,
            email=user_orm.email,
            profile_image_path=user_orm.profile_image_path,
            description=user_orm.description,
            hashed_password=user_orm.hashed_password,
            created_at=user_orm.created_at,
        )
        user.posts = [Post.from_custom_orm(post, user) for post in user_orm.posts]
        return user


class UserORM(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    name: Mapped[str] = mapped_column(String)
    username: Mapped[str] = mapped_column(String, unique=True, primary_key=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    profile_image_path: Mapped[str] = mapped_column(String, default='date/placeholder.png')
    description: Mapped[str] = mapped_column(String, default='')
    hashed_password: Mapped[str] = mapped_column(String)

    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())

    posts: Mapped[list[PostORM]] = relationship(back_populates='author')

    @classmethod
    def from_pydantic_model(cls, model: User) -> UserORM:
        return cls(
            name=model.name,
            username=model.username,
            email=model.email,
            profile_image_path=model.profile_image_path,
            description=model.description,
            hashed_password=model.hashed_password,
        )

    def get_id(self) -> str:
        return str(self.username)

    def check_password(self, password: str) -> bool:
        hashed = sha512(password.encode('utf-8'), usedforsecurity=True).hexdigest()
        return hashed == self.hashed_password