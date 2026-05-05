from datetime import datetime

from pydantic import BaseModel
from sqlalchemy import String, JSON, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from databases import SqlAlchemyBase
from .user import User, UserORM


class Post(BaseModel):
    text: str
    images: list[str]
    author: User
    timestamp: datetime

    @classmethod
    def from_custom_orm(cls, post_orm: 'PostORM', author: User = None) -> 'Post':
        return Post(
            text=post_orm.text,
            images=post_orm.images,
            timestamp=post_orm.timestamp,
            author=author or User.from_custom_orm(post_orm.author),
        )

    def get_html(self) -> str:
        html_test = f'''<pre>{self.text}</pre>'''
        for image in self.images:
            html_test += f'''<img src="{image}" alt="KeepTouch™">'''
        return html_test


class PostORM(SqlAlchemyBase):
    __tablename__ = 'posts'

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String)
    images: Mapped[dict] = mapped_column(JSON)
    timestamp: Mapped[datetime] = mapped_column(DateTime)

    author: Mapped[UserORM] = relationship(back_populates='posts')

    @classmethod
    def from_pydantic_model(cls, model: Post) -> 'PostORM':
        return cls(
            text=model.text,
            images=model.images,
        )
