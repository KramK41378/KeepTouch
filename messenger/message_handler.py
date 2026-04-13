import logging

from databases import global_init, create_session
from models import Message
from models.message import MessageDatabase


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

