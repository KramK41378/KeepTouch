from typing import Self

from pydantic import BaseModel
from sqlalchemy import String, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from databases import SqlAlchemyBase
from . import PostORM
from .post import Post


class User(BaseModel):
    name: str
    username: str
    profile_image_path: str
    description: str

    posts: list[Post] | None = None

    @classmethod
    def from_custom_orm(cls, user_orm: 'UserORM') -> 'User':
        user = cls(
            name=user_orm.name,
            username=user_orm.username,
            profile_image_path=user_orm.profile_image_path,
            description=user_orm.description,
        )
        user.posts = [Post.from_custom_orm(post, user) for post in user_orm.posts]
        return user

class UserORM(SqlAlchemyBase):
    __tablename__ = 'users'

    name: Mapped[str] = mapped_column(String)
    username: Mapped[str] = mapped_column(String, unique=True)
    profile_image_path: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)

    posts: Mapped[list[PostORM]] = relationship(back_populates='users')

    @classmethod
    def from_pydantic_model(cls, model: User) -> 'UserORM':
        return cls(
            name=model.name,
            username=model.username,
            profile_image_path=model.profile_image_path,
            description=model.description,
        )