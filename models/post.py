from datetime import datetime

from pydantic import BaseModel, Field
from sqlalchemy import String, JSON, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from databases import SqlAlchemyBase
from .user import User, UserORM


class Post(BaseModel):
    text: str
    image: str
    author: User
    created_at: datetime = Field(default=None)

    @classmethod
    def from_custom_orm(cls, post_orm: 'PostORM', author: User = None) -> 'Post':
        return Post(
            text=post_orm.text,
            image=post_orm.image,
            created_at=post_orm.created_at,
            author=author or User.from_custom_orm(post_orm.author),
        )

    def get_html(self) -> str:
        html_test = f'''<pre>{self.text}</pre>'''
        for image in self.images:
            html_test += f'''<img src="{image}" alt="KeepTouch™">'''
        return html_test

    def to_html_compatible(self) -> dict[str, str]:
        return {
            'image_path': self.image,
            'caption': self.text,
            'author': self.author.username
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
            images=model.image,
        )
