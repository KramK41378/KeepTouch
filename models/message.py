from typing import Any, Self

from pydantic import BaseModel
from sqlalchemy import Column, Integer, String

from databases import SqlAlchemyBase


class Message(BaseModel):
    message: str
    sender: str
    receiver: str
    key: str

    @classmethod
    def from_custom_orm(cls, obj: 'MessageDatabase') -> "Message":
        return cls(
            message=obj.message,
            sender=obj.sender,
            receiver=obj.receiver,
            key=obj.key,
        )


class MessageDatabase(SqlAlchemyBase):
    __tablename__ = 'messages'
    message_id = Column(Integer, primary_key=True, autoincrement=True)
    message = Column(String, nullable=False)
    sender = Column(String, nullable=False)
    receiver = Column(String, nullable=False)
    key = Column(String, nullable=False)

    @classmethod
    def from_pydantic_model(cls, obj: Message) -> "MessageDatabase":
        return cls(
            message=obj.message,
            sender=obj.sender,
            receiver=obj.receiver,
            key=obj.key
        )

    def __repr__(self) -> str:
        return f'MessageDatabase({self.message_id=}, {self.message=}, {self.sender=}, {self.receiver=}, {self.key=})'