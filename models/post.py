from pydantic import BaseModel
from sqlalchemy import String, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from databases import SqlAlchemyBase
from .user import User, UserORM


class Post(BaseModel):
    text: str
    images: dict[str, str] # {имя: путь}
    author: User

    @classmethod
    def from_custom_orm(cls, post_orm: 'PostORM') -> 'Post':
        return Post(
            text=post_orm.text,
            images=post_orm.images,
            author=post_orm.author,
        )

class PostORM(SqlAlchemyBase):
    __tablename__ = 'posts'

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String)
    images: Mapped[dict] = mapped_column(JSON)

    author: Mapped[UserORM] = relationship(back_populates='posts')

    @classmethod
    def from_pydantic_model(cls, model: Post) -> 'PostORM':
        return cls(
            text=model.text,
            images=model.images,
        )
