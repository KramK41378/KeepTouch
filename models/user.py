from pydantic import BaseModel
from sqlalchemy import String, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from databases import SqlAlchemyBase
from . import PostORM
from .post import Post


class User(BaseModel):
    name: str
    username: str
    posts: list[Post]

class UserORM(SqlAlchemyBase):
    __tablename__ = 'users'

    name: Mapped[str] = mapped_column(String)
    username: Mapped[str] = mapped_column(String, unique=True)

    posts: Mapped[list[PostORM]] = relationship(back_populates='users')

