import logging
from typing import List, Sequence

from databases import global_init, create_session
from models import Message
from models.message import MessageDatabase
from sqlalchemy import select, Select


def get_db_filename():
    return 'db/messages.db'

class MessageHandler:
    def __init__(self) -> None:
        self.db_filename = get_db_filename()
        global_init("databases/messages.db")

    @staticmethod
    def add_message(message_model: Message) -> bool:
        try:
            with create_session() as session:
                orm_message = MessageDatabase.from_pydantic_model(message_model)
                session.add(orm_message)
                session.commit()
                return True
        except Exception as e:
            logging.error(e)
            return False

    @staticmethod
    def get_messages_by_selection(selection: Select[tuple[MessageDatabase]]) -> List[Message] | str:
        """Возвращает все сообщения из БД"""
        try:
            with create_session() as session:
                messages: Sequence[MessageDatabase] = session.scalars(selection).all()
                result: List[Message] = []
                for i in messages:
                    result.append(Message.from_custom_orm(i).model_dump())
                return result
        except Exception as e:
            logging.exception(f'Ошибка при получении сообщений из {e}')
            return f'Ошибка при получении сообщений из {e}'

    @staticmethod
    def get_all_messages() -> List[Message] | None:
        query = select(MessageDatabase).order_by(MessageDatabase.message_id)
        return MessageHandler.get_messages_by_selection(query)