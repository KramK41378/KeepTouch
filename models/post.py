from datetime import datetime

from pydantic import BaseModel, Field
from sqlalchemy import String, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from databases import SqlAlchemyBase
from .user import User, UserORM


class Post(BaseModel):
    text: str
    image: str
    author_username: str
    created_at: datetime = Field(default=None)

    @classmethod
    def from_custom_orm(cls, post_orm: 'PostORM', author: User = None) -> 'Post':
        return Post(
            text=post_orm.text,
            image=post_orm.image,
            created_at=post_orm.created_at,
            author_username=post_orm.author_username,
        )

    def to_html_compatible(self) -> dict[str, str]:
        return {
            'image_path': self.image,
            'caption': self.text,
            'author': self.author_username
        }



class PostORM(SqlAlchemyBase):
    __tablename__ = 'posts'

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String)
    image: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())

    author_username: Mapped[str] = mapped_column(
        String, ForeignKey('users.username')
    )

    author: Mapped[UserORM] = relationship(back_populates='posts')

    @classmethod
    def from_pydantic_model(cls, model: Post) -> 'PostORM':
        return cls(
            text=model.text,
            image=model.image,
        )
