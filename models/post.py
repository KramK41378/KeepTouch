from pydantic import BaseModel
from sqlalchemy import String, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from databases import SqlAlchemyBase


class Post(BaseModel):
    text: str
    images: dict[str, str] # {имя: путь}


class PostORM(SqlAlchemyBase):
    __tablename__ = 'posts'

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String)
    images: Mapped[dict] = mapped_column(JSON)

    author: Mapped['User'] = relationship(back_populates='posts')
