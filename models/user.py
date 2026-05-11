from datetime import datetime

from flask_login import UserMixin
from pydantic import BaseModel, Field
from sqlalchemy import String, JSON, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from databases import SqlAlchemyBase
from .post import Post, PostORM


class User(BaseModel):
    name: str
    username: str
    email: str
    profile_image_path: str
    description: str
    hashed_password: str
    created_at: datetime | None = Field(default=None, json_schema_extra={"readOnly": True})

    posts: list[Post] | None = None

    @classmethod
    def from_custom_orm(cls, user_orm: 'UserORM') -> 'User':
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
    username: Mapped[str] = mapped_column(String, unique=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    profile_image_path: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    hashed_password: Mapped[str] = mapped_column(String)

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now()
    )

    posts: Mapped[list[PostORM]] = relationship(back_populates='users')

    @classmethod
    def from_pydantic_model(cls, model: User) -> 'UserORM':
        return cls(
            name=model.name,
            username=model.username,
            email=model.email,
            profile_image_path=model.profile_image_path,
            description=model.description,
            hashed_password=model.hashed_password,
        )

    def get_id(self):
        return str(self.username)
